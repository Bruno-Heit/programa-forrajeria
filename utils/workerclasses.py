'''
En este archivo están todas las clases de WORKER THREADS
'''
from PySide6.QtCore import (QObject, Signal, Slot, QThread)

from utils.functionutils import (createConnection)
from utils.enumclasses import (LoggingMessage, TableViewId, WorkerType, WorkerPriority)
from utils.dboperations import (DatabaseRepository, DATABASE_DIR)

from sqlite3 import (Connection, Error as sqlite3Error)
from typing import (Any, Iterable)
import itertools
import logging


class Worker(QObject):
    '''
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
    '''
    countFinished:Signal = Signal(int)
    progress:Signal = Signal(Any)
    finished:Signal = Signal()
    
    def __init__(self) -> None:
        super(Worker, self).__init__()
        self._canceled:bool = False
        return None
    
    def cancel(self) -> None:
        '''
        Cancela la ejecución del **Worker** y muestra un *log* avisando de la 
        cancelación.
        '''
        self._canceled = True
        logging.debug(LoggingMessage.WORKER_CANCEL_REQUESTED)
        return None
    
    def isCanceled(self) -> bool:
        '''
        Verifica si la tarea del **Worker** fue detenida.

        Retorna
        -------
        bool
            flag que determina si la tarea está detenida
        '''
        return self._canceled





class WorkerSelect(Worker):
    '''
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
    '''
    countFinished = Signal(tuple) # se emite cuando se termina la consulta de COUNT(). emite tuple[int, int], teniendo 
                                  # la tupla las dimensiones del "batch" ([filas, columnas])
    registerProgress = Signal(tuple) # envía un tuple[int,[Any]] con cada registro coincidente (el 'int' se obtiene de 
                                     # 'enumerate' y sirve solamente para actualizar en MainWindow el QProgressBar de 
                                     # la tabla relacionada, lo más importante es el tuple interno '[Any]').

    def __init__(self, data_sql:str, data_params:tuple=None, 
                 count_sql:str=None, count_params:tuple=None) -> None:
        '''
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
        '''
        super(WorkerSelect, self).__init__()
        self._data_sql:str = data_sql
        self._data_params:tuple | None = data_params
        self._count_sql:str | None = count_sql
        self._count_params:tuple | None = count_params


    @Slot()
    def run(self) -> None:
        '''
        Hace la consulta **SELECT** a la base de datos y devuelve los valores 
        de las filas seleccionadas.
        '''
        data_query:list[Any] # guarda los registros obtenidos
        
        if self.isCanceled():
            logging.debug(LoggingMessage.WORKER_CANCELED)
            self.finished.emit()
            return None
        
        with DatabaseRepository() as repo:
            # si recibió 'count_sql' hace la consulta COUNT() y manda la cantidad de registros encontrados...
            if self._count_sql:
                self.countFinished.emit(
                    (repo.selectRowCount(self._count_sql,self._count_params),
                     repo.selectColumnCount(self._data_sql, self._data_params),
                    )
                )
            
            # luego obtiene los registros y los envía de a uno...
            data_query = repo.selectRegisters(
                data_sql=self._data_sql,
                data_params=self._data_params if self._data_params else None
            )
            for n,reg in enumerate(data_query):
                match self.isCanceled():
                    case False:
                        self.registerProgress.emit( tuple((n, reg)) )
                    case True:
                        logging.debug(LoggingMessage.WORKER_CANCELED)
                        self.finished.emit()
                        return None
        
        logging.debug(LoggingMessage.DEBUG_DB_MULT_SELECT_SUCCESS)
        self.finished.emit()




# todo: implementar también los siguientes workers como subclases de Worker

class WorkerDelete(QObject):
    '''
    Clase **Worker** que se encarga de ejecutar las consultas de tipo DELETE 
    a la base de datos.
    '''
    progress = Signal(int) # devuelve un int con el progreso que lleva borrado para actualizar el progressbar en MainWindow.
    finished = Signal(int)
    
    def executeDeleteQuery(self, params:Iterable[Any] | dict[str, list], sql:str=None, 
                           mult_sql:tuple[str]=None, table_viewID:TableViewId=TableViewId.INVEN_TABLE_VIEW) -> None:
        '''
        Hace la consulta DELETE a la base de datos.
        
        Parámetros
        ----------
        params : Iterable[Any] | dict[list]
            parámetros para la consulta DELETE, será un **dict[list]** cuando 
            el parámetro **mult_sql** sea diferente de ***None***. Cada 
            **dict** tiene los IDs necesarios para la consulta
        sql : str, opcional
            consulta DELETE para eliminar registros de una tabla
        mult_sql : tuple[str], opcional
            consultas DELETE y sus parámetros en formato **tuple[str]**, se 
            recibe cuando se deben realizar consultas DELETE en más de una 
            tabla en forma consecutiva
        table_viewID : TableViewId, opcional
            vista a la que se referencia
        '''
        conn = createConnection(DATABASE_DIR)
        if not conn:
            self.finished.emit()
            return None
        cursor = conn.cursor()
        
        try:
            match table_viewID:
                case TableViewId.INVEN_TABLE_VIEW:
                    for n,param in enumerate(params):
                        cursor.execute(sql, param)
                        conn.commit()
                        self.progress.emit(n)
                    logging.debug(LoggingMessage.DEBUG_DB_MULT_DELETE_SUCCESS)
            
                # al ser de VENTAS, params es 'dict[list]', donde cada item 
                # tiene los IDs necesarios para las 3 tablas
                case TableViewId.SALES_TABLE_VIEW:
                    # recorre cada (consulta sql, item) simultáneamente
                    for n, ( sql, (_, values) ) in enumerate( zip(mult_sql, params.items()) ):
                        for val in values:
                            cursor.execute(sql, (val,))
                            conn.commit()
                        self.progress.emit(n)
                    logging.debug(LoggingMessage.DEBUG_DB_MULT_DELETE_SUCCESS)
                
                case TableViewId.DEBTS_TABLE_VIEW:
                    for n, param in enumerate(params):
                        for sql in mult_sql:
                            cursor.execute(sql, param)
                            conn.commit()
                        self.progress.emit(n)
                    logging.debug(LoggingMessage.DEBUG_DB_MULT_DELETE_SUCCESS)
        
        except sqlite3Error as err: #! errores de base de datos, consultas, etc.
            conn.rollback()
            logging.critical(LoggingMessage.ERROR_DB_DELETE, f"{err.sqlite_errorcode}: {err.sqlite_errorname} / {err}")
            
        finally:
            conn.close()
            self.finished.emit()
            





class WorkerInsert(QObject):
    '''
    Clase **Worker** que se encarga de ejecutar las consultas de tipo INSERT 
    a la base de datos.
    '''
    progress = Signal(int)
    finished = Signal(int)
    
    
    @Slot(str,tuple,bool)
    def executeInsertQuery(self, data_sql:str, data_params:tuple=None) -> None:
        '''
        Hace la consulta INSERT a la base de datos.
        
        Parámetros
        ----------
        data_sql : str
            la consulta con el registro a insertar
        data_params : tuple
            los parámetros de la consulta, por defecto ***None***
        '''
        conn = createConnection(DATABASE_DIR)
        if not conn:
            self.finished.emit()
            return None
        cursor = conn.cursor()
        
        try:
            cursor.execute(data_sql, data_params) if data_params else cursor.execute(data_sql)
            
            conn.commit()
            logging.debug(LoggingMessage.DEBUG_DB_MULT_INSERT_SUCCESS)
            
        except sqlite3Error as err:
            conn.rollback()
            logging.critical(LoggingMessage.ERROR_DB_INSERT, f"{err.sqlite_errorcode}: {err.sqlite_errorname} / {err}")
            
        finally:
            self.finished.emit()
            conn.close()





class WorkerUpdate(QObject):
    '''
    Clase **Worker** que se encarga de ejecutar las consultas de tipo UPDATE 
    a la base de datos.
    
    Este **Worker** es usado también para marcar registros como eliminados en 
    la columna *eliminado* en la base de datos.
    '''
    progress = Signal(int)
    finished = Signal(int)
    
    
    @Slot(str,tuple,bool)
    def executeUpdateQuery(self, sql:str, params:Iterable[tuple]) -> None:
        '''
        Hace la consulta UPDATE a la base de datos.
        
        Parámetros
        ----------
        sql: str
            consulta UPDATE a ejecutar
        params: Iterable[tuple]
            parámetros para consulta
        '''
        conn = createConnection(DATABASE_DIR)
        if not conn:
            self.finished.emit()
            return None
        cursor = conn.cursor()
        
        try:
            for n,param in enumerate(params):
                cursor.execute(sql, param)
                conn.commit()
                self.progress.emit(n)
            logging.debug(LoggingMessage.DEBUG_DB_MULT_UPDATE_SUCCESS)
            
        except sqlite3Error as err:
            conn.rollback()
            logging.critical(LoggingMessage.ERROR_DB_UPDATE, f"{err}")
                
        finally:
            conn.close()
            self.finished.emit()





class WorkerManager(QObject):
    '''
    Clase **WorkerManager** que administra las operaciones **SELECT**, 
    **UPDATE** y **DELETE** como si fueran tareas (*tasks*) y se encarga de 
    ejecutarlas en un único **QThread**.
    Las operaciones siguen una jerarquía de importancia: la operación más 
    importante (mayor prioridad)
    '''
    taskStarted:Signal = Signal(str)
    taskFinished:Signal = Signal(str)
    
    def __init__(self, parent=None) -> None:
        super(WorkerManager, self).__init__(parent)
        
        self.task_queue:list = [] # lista con las tareas a ejecutar
        self._counter:itertools.count = itertools.count() # contador para evitar problemas de orden en prioridades
        
        self._current_thread:QThread = None
        self._current_worker:type[Worker] = None
        self._is_running:bool = False
        return None
    
    
    def addTask(self, worker:type[Worker], 
                priority:WorkerPriority=WorkerPriority.HIGH) -> None:
        '''
        Añade una tarea nueva a realizar por medio del **Worker** especificado 
        y teniendo en cuenta la prioridad especificada.

        Parámetros
        ----------
        worker : type[Worker]
            subclase de **Worker** a ejecutar
        priority : WorkerPriority, opcional
            prioridad que darle a la tarea, por defecto *WorkerPriority.HIGH*
        '''
        count = next(self._counter)
        self.task_queue.append((priority, count, worker))
        # ordena según prioridad y orden de llegada
        self.task_queue.sort(key=lambda x: (x[0], x[1]))
        
        if not self._is_running:
            self.__startNextTask()
        return None
    
    def __startNextTask(self) -> None:
        '''
        Intenta iniciar la siguiente tarea en la cola teniendo en cuenta la 
        prioridad de cada tarea.
        '''
        if not self.task_queue:
            self._is_running = False
            return None
        
        self._is_running = True
        
        # obtiene la tarea con mayor prioridad
        priority, count, worker = self.task_queue.pop(0)
        
        self.__startWorker(worker)
        return None
    
    def __startWorker(self, worker:type[Worker]) -> None:
        '''
        Inicia un **QThread** y le asigna el **Worker** especificado para 
        realizar la consulta a la base de datos de forma asíncrona, conecta 
        sus señales y slots.

        Parámetros
        ----------
        worker : type[Worker]
            instancia de tipo **Worker** que ejecutar
        '''
        thread:QThread = QThread()
        worker.moveToThread(thread)
        
        # todo: en MainWindow conectar el resto de señales a slots
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
        '''
        Borra todas las tareas pendientes.
        '''
        self.task_queue.clear()
        return None
    
    def stopCurrentTask(self) -> None:
        '''
        Intenta cancelar la ejecución del **Worker** actual.
        '''
        if self._current_worker and hasattr(self._current_worker, "cancel"):
            self._current_worker.cancel()
        return None

