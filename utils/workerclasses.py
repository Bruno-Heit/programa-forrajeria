"""
En este archivo están todas las clases de WORKER THREADS
"""

from PySide6.QtCore import QObject, Signal, Slot, QThread

from utils.functionutils import createConnection
from utils.enumclasses import LoggingMessage, TableViewId, WorkerType, WorkerPriority
from utils.dboperations import DatabaseRepository, DATABASE_DIR

from sqlite3 import Connection, Error as sqlite3Error
from typing import Any, Iterable
import itertools
import logging


class Worker(QObject):
    """
    Clase base para la creación de **Workers**, contiene declaraciones de
    señales y métodos básicos que utilizarán las subclases de **Worker**.

    **NOTA**: ésta clase no debe instanciarse directamente, para implementar
    **Workers** se deben utilizar las diferentes subclases.

    Los **Workers** ejecutan acciones de forma asíncrona al programa principal
    y son especialmente útiles para realizar operaciones que puedan tardar
    bastante tiempo sin bloquear el *thread principal*.

    Señales
    -------
    countFinished : es emitida cuando se termina de contar los registros
        coincidentes, emite un **int** que representa la cantidad de registros.
    progress : se emite a medida que se avanza con cada registro, emite un
        **int** con el progreso que lleva.
    finished : es emitida una vez que se terminó de ejecutar el worker.
    """

    countFinished: Signal = Signal(int)
    progress: Signal = Signal(Any)
    finished: Signal = Signal()

    def __init__(self) -> None:
        super(Worker, self).__init__()
        self._canceled: bool = False
        return None

    def cancel(self) -> None:
        """
        Cancela la ejecución del **Worker** y muestra un *log* avisando de la
        cancelación.
        """
        self._canceled = True
        logging.debug(LoggingMessage.WORKER_CANCEL_REQUESTED)
        return None

    def isCanceled(self) -> bool:
        """
        Verifica si la tarea del **Worker** fue detenida.

        Retorna
        -------
        bool
            flag que determina si la tarea está detenida
        """
        return self._canceled


class WorkerSelect(Worker):
    """
    Subclase especializada de **Worker** que se encarga de ejecutar las
    consultas de tipo **READ** a la base de datos.

    SEÑALES
    -------
    countFinished : señal reimplementada; es emitida cuando se termina de
        contar los registros coincidentes, emite una **tuple[int, int]** que
        representa las dimensiones del *batch* (filas, columnas).
    registerProgress : es emitida a medida que se recorren los registros
        obtenidos, emite un **tuple[int,[Any]]** donde **int** representa el
        progreso y **[Any]** es el registro actual.
    """

    countFinished = Signal(
        tuple
    )  # se emite cuando se termina la consulta de COUNT(). emite tuple[int, int], teniendo
    # la tupla las dimensiones del "batch" ([filas, columnas])
    registerProgress = Signal(
        tuple
    )  # envía un tuple[int,[Any]] con cada registro coincidente (el 'int' se obtiene de
    # 'enumerate' y sirve solamente para actualizar en MainWindow el QProgressBar de
    # la tabla relacionada, lo más importante es el tuple interno '[Any]').

    def __init__(
        self,
        data_sql: str,
        data_params: tuple = None,
        count_sql: str = None,
        count_params: tuple = None,
    ) -> None:
        """
        Inicializa el objeto **WorkerSelect**.

        Parámetros
        ----------
        data_sql: str
            Consulta de tipo **SELECT**
        data_params: tuple, opcional
            Parámetros de la consulta **SELECT**, por defecto ***None***
        count_sql: str, opcional
            Consulta de tipo **SELECT COUNT()** para obtener la cantidad de
            registros coincidentes, por defecto ***None***
        count_params: tuple, opcional
            Parámetros de la consulta **SELECT COUNT()**, por defecto
            ***None***
        """
        super(WorkerSelect, self).__init__()
        self._data_sql: str = data_sql
        self._data_params: tuple | None = data_params
        self._count_sql: str | None = count_sql
        self._count_params: tuple | None = count_params

    @Slot()
    def run(self) -> None:
        """
        Hace la consulta **SELECT** a la base de datos y emite los valores de
        las filas seleccionadas.
        """
        data_query: list[Any]  # guarda los registros obtenidos

        if self.isCanceled():
            logging.debug(LoggingMessage.WORKER_CANCELED)
            self.finished.emit()
            return None

        with DatabaseRepository() as repo:
            # si recibió 'count_sql' hace la consulta COUNT() y manda la
            # cantidad de registros encontrados...
            if self._count_sql:
                self.countFinished.emit(
                    (
                        repo.selectRowCount(self._count_sql, self._count_params),
                        repo.selectColumnCount(self._data_sql, self._data_params),
                    )
                )

            # luego obtiene los registros y los envía de a uno...
            data_query = repo.selectRegisters(
                data_sql=self._data_sql,
                data_params=self._data_params if self._data_params else None,
            )
            for n, reg in enumerate(data_query):
                match self.isCanceled():
                    case False:
                        self.registerProgress.emit(tuple((n, reg)))
                    case True:
                        logging.debug(LoggingMessage.WORKER_CANCELED)
                        self.finished.emit()
                        return None

        logging.debug(LoggingMessage.DEBUG_DB_MULT_SELECT_SUCCESS)
        self.finished.emit()


class WorkerDelete(Worker):
    """
    Subclase especializada de **Worker** que se encarga de ejecutar las
    consultas de tipo **DELETE** | **UPDATE** a la base de datos.
    Las operaciones **UPDATE** que maneja son aquellas que tengan la
    naturaleza de marcar como *eliminados* algunos registros.
    """

    def __init__(
        self,
        del_params: Iterable[Any] | dict[list],
        table_viewID: TableViewId,
        del_sql: str = None,
        mult_sql: tuple[str] = None,
    ) -> None:
        """
        Inicializa el objeto **WorkerDelete**.

        Parámetros
        ----------
        table_viewID : TableViewId
            vista a la que se referencia
        del_params : Iterable[Any] | dict[list]
            parámetros para la/s consulta/s **DELETE**; será un **dict[list]**
            cuando las tablas afectadas sean las de Ventas, cada **dict**
            tiene los IDs necesarios para la consulta
        del_sql: str, opcional
            Consulta de tipo **DELETE**; se usa cuando se realizan consultas
            **DELETE** a una sola tabla, por defecto ***None***
        mult_sql : tuple[str], opcional
            consultas **DELETE** y sus parámetros en formato **tuple[str]**;
            se usa cuando se realizan consultas **DELETE** en más de una tabla
            consecutivamente, por defecto ***None***
        """
        super(WorkerDelete, self).__init__()
        self._table_viewID: TableViewId = table_viewID
        self._del_sql: str = del_sql
        self._del_params: Iterable[Any] | dict[list] = del_params
        self._mult_sql: tuple[str] = mult_sql

    def run(self) -> None:
        """
        Hace la consulta **DELETE** a la base de datos y emite los valores de
        las filas borradas.
        """
        if self.isCanceled():
            logging.debug(LoggingMessage.WORKER_CANCELED)
            self.finished.emit()
            return None

        with DatabaseRepository() as db_repo:
            match self._table_viewID:
                # ? INVENTARIO: sólo usa una consulta y un ID, itera el ID
                case TableViewId.INVEN_TABLE_VIEW:
                    # recorre cada parámetro y hace la consulta
                    for n, param in enumerate(self._del_params):
                        match self.isCanceled():
                            case False:
                                db_repo.updateRegisters(
                                    upd_sql=self._del_sql, upd_params=param
                                )
                                self.progress.emit(n)

                            case True:
                                logging.debug(LoggingMessage.WORKER_CANCELED)
                                self.finished.emit()
                                return None

                # ? VENTAS: params es 'dict[list]' y cada item tiene los IDs
                # ? necesarios para las 3 tablas... itera sobre las consultas
                # ? y también sobre cada ID...
                case TableViewId.SALES_TABLE_VIEW:
                    # recorre cada (consulta, item)
                    for n, (sql, (_, values)) in enumerate(
                        zip(self._mult_sql, self._del_params.items())
                    ):
                        match self.isCanceled():
                            case False:
                                # recorre cada ID
                                for val in values:
                                    db_repo.updateRegisters(
                                        upd_sql=sql, upd_params=(val,)
                                    )
                                self.progress.emit(n)

                            case True:
                                logging.debug(LoggingMessage.WORKER_CANCELED)
                                self.finished.emit()
                                return None

                # ? DEUDAS: itera sobre cada ID y luego cada consulta...
                case TableViewId.DEBTS_TABLE_VIEW:
                    # recorre cada ID...
                    for n, param in enumerate(self._del_params):
                        match self.isCanceled():
                            case False:
                                # recorre cada consulta...
                                for sql in self._mult_sql:
                                    db_repo.updateRegisters(
                                        upd_sql=sql, upd_params=param
                                    )
                                self.progress.emit(n)

                            case True:
                                logging.debug(LoggingMessage.WORKER_CANCELED)
                                self.finished.emit()
                                return None

        logging.debug(LoggingMessage.DEBUG_DB_MULT_DELETE_SUCCESS)
        self.finished.emit()


# TODO: implementar correctamente esto (no es urgente)
class WorkerUpdate(Worker):
    """
    Clase **Worker** que se encarga de ejecutar las consultas de tipo
    **UPDATE** a la base de datos.

    Este **Worker** es usado también para marcar registros como eliminados en
    la columna *eliminado* en la base de datos.
    """

    def __init__(self, upd_sql: str, upd_params: tuple) -> None:
        """
        Inicializa el objeto **WorkerUpdate**.

        Parámetros
        ----------
        upd_sql : str
            Consulta de tipo **UPDATE**
        upd_params : tuple
            Parámetros de la consulta **UPDATE**
        """
        super(WorkerUpdate, self).__init__()
        self._upd_sql: str = upd_sql
        self._upd_params: tuple = upd_params

    @Slot()
    def run(self) -> None:
        """
        Hace la consulta **UPDATE** a la base de datos.
        """
        if self.isCanceled():
            logging.debug(LoggingMessage.WORKER_CANCELED)
            self.finished.emit()
            return None

        self.countFinished.emit(len(self._upd_params))

        with DatabaseRepository() as db_repo:
            for n, param in enumerate(self._upd_params):
                match self.isCanceled():
                    case False:
                        db_repo.updateRegisters(upd_sql=self._upd_sql, upd_params=param)
                        self.progress.emit(n)
                        # TODO: emitir los datos para actualizar el modelo
                    case True:
                        logging.debug(LoggingMessage.WORKER_CANCELED)
                        self.finished.emit()
                        return None

            logging.debug(LoggingMessage.DEBUG_DB_MULT_UPDATE_SUCCESS)

        self.finished.emit()
        return None


class WorkerManager(QObject):
    """
    Clase **WorkerManager** que administra las operaciones **SELECT**,
    **UPDATE** y **DELETE** como si fueran tareas (*tasks*) y se encarga de
    ejecutarlas en un único **QThread**.
    Las operaciones siguen una jerarquía de importancia: la operación más
    importante (mayor prioridad)
    """

    taskStarted: Signal = Signal(str)
    taskFinished: Signal = Signal(str)

    def __init__(self, parent=None) -> None:
        super(WorkerManager, self).__init__(parent)

        self.task_queue: list = []  # lista con las tareas a ejecutar
        self._counter: itertools.count = (
            itertools.count()
        )  # contador para evitar problemas de orden en prioridades

        self._current_thread: QThread = None
        self._current_worker: type[Worker] = None
        self._is_running: bool = False
        return None

    def addTask(
        self, worker: type[Worker], priority: WorkerPriority = WorkerPriority.HIGH
    ) -> None:
        """
        Añade una tarea nueva a realizar por medio del **Worker** especificado
        y teniendo en cuenta la prioridad especificada.

        Parámetros
        ----------
        worker : type[Worker]
            subclase de **Worker** a ejecutar
        priority : WorkerPriority, opcional
            prioridad que darle a la tarea, por defecto *WorkerPriority.HIGH*
        """
        count = next(self._counter)
        self.task_queue.append((priority, count, worker))
        # ordena según prioridad y orden de llegada
        self.task_queue.sort(key=lambda x: (x[0], x[1]))

        if not self._is_running:
            self.__startNextTask()
        return None

    def __startNextTask(self) -> None:
        """
        Intenta iniciar la siguiente tarea en la cola teniendo en cuenta la
        prioridad de cada tarea.
        """
        if not self.task_queue:
            self._is_running = False
            return None

        self._is_running = True

        # obtiene la tarea con mayor prioridad
        priority, count, worker = self.task_queue.pop(0)

        self.__startWorker(worker)
        return None

    def __startWorker(self, worker: type[Worker]) -> None:
        """
        Inicia un **QThread** y le asigna el **Worker** especificado para
        realizar la consulta a la base de datos de forma asíncrona, conecta
        sus señales y slots.
        Al finalizar llama nuevamente al método *'__startNextTask'* para
        continuar ejecutando tareas si hay más en cola.

        Parámetros
        ----------
        worker : type[Worker]
            instancia de tipo **Worker** que ejecutar
        """
        thread: QThread = QThread()
        worker.moveToThread(thread)

        thread.started.connect(worker.run)
        worker.finished.connect(thread.quit)
        worker.finished.connect(worker.deleteLater)
        thread.finished.connect(thread.deleteLater)

        thread.finished.connect(self.__startNextTask)

        self._current_thread = thread
        self._current_worker = worker

        thread.start()
        return None

    def clearTasks(self) -> None:
        """
        Borra todas las tareas pendientes.
        """
        self.task_queue.clear()
        return None

    def stopCurrentTask(self) -> None:
        """
        Intenta cancelar la ejecución del **Worker** actual.
        """
        if self._current_worker and hasattr(self._current_worker, "cancel"):
            self._current_worker.cancel()
        return None
