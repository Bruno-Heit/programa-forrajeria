'''
En este archivo están todas las clases de WORKER THREADS
'''
from PySide6.QtCore import (QObject, Signal, Slot)

from utils.functionutils import (createConnection)
from utils.enumclasses import (LoggingMessage)
from utils.dboperations import (DatabaseRepository)

from sqlite3 import (Connection, Error as sqlite3Error)
from typing import (Any, Iterable)
import logging
        


class WorkerSelect(QObject):
    '''Clase WORKER que se encarga de ejecutar las consultas de tipo READ a la base de datos.'''
    countFinished = Signal(tuple) # se emite cuando se termina la consulta de COUNT(). emite tuple[int, int], teniendo 
                                  # la tupla las dimensiones del "batch" ([filas, columnas])
    registerProgress = Signal(tuple) # envía un tuple[int,[Any]] con cada registro coincidente (el 'int' se obtiene de 
                                     # 'enumerate' y sirve solamente para actualizar en MainWindow el QProgressBar de 
                                     # la tabla relacionada, lo más importante es el tuple interno '[Any]').
    finished = Signal(int) # si hubo algún error envía 0, sino 1. Se emite cuando se termina la consulta de registros.

    def __init__(self) -> None:
        super(WorkerSelect, self).__init__()


    @Slot(str,str,tuple,tuple)
    def executeReadQuery(self, data_sql:str, data_params:tuple=None, 
                         count_sql:str=None, count_params:tuple=None) -> None:
        '''
        Hace la consulta SELECT a la base de datos y devuelve los valores de las filas seleccionadas. 
        
        PARAMS:
        - data_sql: la consulta para obtener registros a ejecutar.
        - data_params: los parámetros de la consulta 'data_sql'. Por defecto es None.
        - count_sql: (opcional) la consulta READ COUNT() a ejecutar. Por defecto es None.
        - count_params: (opcional) los parámetros de la consulta 'count_sql'. Por defecto es None.
        
        SEÑALES:
        La señal 'finished' emite:
        - 0: si no se pudo establecer una conexión con la base de datos.
        - 1: si no hubo errores.
        
        La señal 'countFinished' emite un int que representa la cantidad de registros coincidentes.
        
        La señal 'registerProgress' emite un tuple[int,[Any]], donde 'int' representa el progreso de lectura y '[Any]' 
        es el registro actual.
        '''
        count_query:int # guarda el COUNT() de registros
        data_query:list[Any] # guarda los registros obtenidos
        signal:tuple[int,Any] = None
        
        # TODO: limitar la cantidad de registros a 150
        with DatabaseRepository() as repo:
            # si recibió 'count_sql' hace la consulta COUNT() y manda la cantidad de registros encontrados...
            if count_sql:
                self.countFinished.emit(
                    (repo.selectRowCount(count_sql,count_params),
                    repo.selectColumnCount(data_sql, data_params),)
                    )
            
            # luego obtiene los registros y los envía de a uno...
            data_query = repo.selectRegisters(
                data_sql, data_params if data_params else None)
            for n,reg in enumerate(data_query):
                # signal = tuple((n, reg))
                self.registerProgress.emit( tuple((n, reg)) )
        
        self.finished.emit(1) #* todo bien
        logging.debug(LoggingMessage.DEBUG_DB_MULT_SELECT_SUCCESS)





class WorkerDelete(QObject):
    '''Clase WORKER que se encarga de ejecutar las consultas de tipo DELETE a la base de datos.
    Este WORKER guarda los registros eliminados de la base de datos en archivos .csv.'''
    progress = Signal(int) # devuelve un int con el progreso que lleva borrado para actualizar el progressbar en MainWindow.
    finished = Signal(int)
    
    def executeDeleteQuery(self, params:list[tuple[int,str]], sql:str=None, mult_sql:tuple[str]=None) -> None:
        '''
        Hace la consulta DELETE a la base de datos.
        
        PARAMS
        - sql: la consulta DELETE para eliminar los registros de una tabla. Por defecto es None.
        - params: los parámetros como iterable para la consulta DELETE 'sql'. Cada '[tuple]' tiene un 'int' con el ID y un 
        'str' con un valor único del registro (ej.:nombre de un producto, fecha y hora de una venta, etc.).
        - mult_sql: consultas DELETE y sus parámetros en formato tuple[str]. Por defecto es None.
        
        Se recibe el parámetro 'mult_sql' cuando se deben realizar consultas DELETE en más de una tabla en forma 
        consecutiva (por ej.: en Detalle_Ventas se debe borrar registros de Ventas también).
        
        SEÑALES:
        La señal 'finished' emite:
        - 0: si no se pudo establecer una conexión con la base de datos.
        - 1: si no hubo errores.
        - sqlite3.Error.sqlite_errorcode: si hubo un error concreto, emite el código de error de sqlite3.
        
        La señal 'progress' emite un int que indica el progreso de borrado.
        '''
        conn = createConnection("database/inventario.db")
        if not conn:
            self.finished.emit(0) #! error con la comunicación a la base de datos
        cursor = conn.cursor()
        
        try:
            # se borra de una sola tabla (ej.: Productos)
            if sql and not mult_sql:
                for n,param in enumerate(params):
                    cursor.execute(sql, param)
                    conn.commit()
                    self.progress.emit(n)
                logging.debug(LoggingMessage.DEBUG_DB_MULT_DELETE_SUCCESS)
            
            # se borra de más de una tabla (ej.: Detalle_Ventas, Ventas y Deudas)
            elif not sql and mult_sql:
                for n,param in enumerate(params):
                    for sql in mult_sql:
                        cursor.execute(sql, param[:sql.count("?")])
                        conn.commit()
                    self.progress.emit(n)
                logging.debug(LoggingMessage.DEBUG_DB_MULT_DELETE_SUCCESS)
            
        
        except sqlite3Error as err: #! errores de base de datos, consultas, etc.
            conn.rollback()
            logging.critical(LoggingMessage.ERROR_DB_DELETE, f"{err.sqlite_errorcode}: {err.sqlite_errorname} / {err}")
            self.finished.emit(err.sqlite_errorcode)
            
        finally:
            conn.close()
            
        self.finished.emit(1) #* todo bien





class WorkerInsert(QObject):
    '''Clase WORKER que se encarga de ejecutar las consultas de tipo INSERT a la base de datos.'''
    progress = Signal(int)
    finished = Signal(int)
    
    
    @Slot(str,tuple,bool)
    def executeInsertQuery(self, data_sql:str, data_params:tuple=None) -> None:
        '''
        Hace la consulta INSERT a la base de datos.
        
        PARAMS:
        - data_sql: la consulta con el registro a insertar.
        - data_params: los parámetros de la consulta 'data_sql'. Por defecto es None.
        
        SEÑALES:
        La señal 'finished' emite:
        - 0: si no se pudo establecer una conexión con la base de datos.
        - 1: si no hubo errores.
        - sqlite3.Error.sqlite_errorcode: si hubo un error concreto, emite el código de error de sqlite3.
        '''
        conn = createConnection("database/inventario.db")
        if not conn:
            self.finished.emit(0) #! error con la comunicación de la base de datos
        cursor = conn.cursor()
        
        try:
            cursor.execute(data_sql, data_params) if data_params else cursor.execute(data_sql)
            
            conn.commit()
            logging.debug(LoggingMessage.DEBUG_DB_MULT_INSERT_SUCCESS)
            self.finished.emit(1) #* todo bien
            
        except sqlite3Error as err:
            conn.rollback()
            logging.critical(LoggingMessage.ERROR_DB_INSERT, f"{err.sqlite_errorcode}: {err.sqlite_errorname} / {err}")
            self.finished.emit(err.sqlite_errorcode) #! error al realizar el insert
            
        finally:
            conn.close()
        
        return None





class WorkerUpdate(QObject):
    '''Clase WORKER que se encarga de ejecutar las consultas de tipo UPDATE a la base de datos.
    Este WORKER es usado también para marcar registros como eliminados en la columna "eliminado" en la base de datos.'''
    progress = Signal(int)
    finished = Signal(int)
    
    
    @Slot(str,tuple,bool)
    def executeUpdateQuery(self, sql:str, params:Iterable[tuple]) -> None:
        '''
        Hace la consulta UPDATE a la base de datos.
        La señal 'finished' emite:
        - 0: si no se pudo establecer una conexión con la base de datos
        - 1: si no hubo errores
        - sqlite3.Error: si hubo un error concreto, emite el código de error de sqlite3
        La señal 'progress' emite un 'int' que indica el progreso de actualización.
        
        Parámetros
        ----------
        sql: str
            consulta UPDATE a ejecutar
        params: Iterable[tuple]
            parámetros para consulta
        
        Retorna
        -------
        None
        '''
        conn = createConnection("database/inventario.db")
        if not conn:
            self.finished.emit(0) #! error con la comunicación de la base de datos
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
            self.finished.emit(err) #! error al realizar el update
                
        finally:
            conn.close()
            
        self.finished.emit(1) #* todo bien
        return None