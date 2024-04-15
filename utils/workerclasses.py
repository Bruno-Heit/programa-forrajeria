'''
En este archivo están todas las clases de WORKER THREADS
'''
from PySide6.QtCore import (QObject, Signal, Slot)

from utils.functionutils import (createConnection)

from sqlite3 import (Connection, Error as sqlite3Error)
from typing import (Any)
import logging



class DbReadWorker(QObject):
    '''Clase WORKER que se encarga de ejecutar las consultas de tipo READ a la base de datos.'''
    countFinished = Signal(int) # se emite cuando se termina la consulta de COUNT().
    registerProgress = Signal(tuple) # envía un tuple[int,[Any]] con cada registro coincidente (el 'int' se obtiene de 
                                     # 'enumerate' y sirve solamente para actualizar en MainWindow el QProgressBar de 
                                     # la tabla relacionada, lo más importante es el tuple interno '[Any]').
    finished = Signal(int) # si hubo algún error envía 0, sino 1. Se emite cuando se termina la consulta de registros.


    @Slot(str,str,tuple,tuple)
    def executeReadQuery(self, data_sql:str, data_params:tuple=None, count_sql:str=None, count_params:tuple=None) -> None:
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
        conn:Connection|None
        signal:tuple[int,Any] = None
        
        conn = createConnection("database/inventario.db")
        if not conn:
            self.finished.emit(0) #! error con la comunicación a la base de datos
        cursor = conn.cursor()

        # si recibió 'count_sql' hace la consulta COUNT() y manda la cantidad de registros encontrados...
        if count_sql:
            count_query = cursor.execute(count_sql).fetchone()[0] if not count_params else cursor.execute(count_sql, count_params).fetchone()[0]
            self.countFinished.emit(count_query)
        
        # luego obtiene los registros los envía de a uno...
        data_query = cursor.execute(data_sql).fetchall() if not data_params else cursor.execute(data_sql, data_params).fetchall()
        for n,reg in enumerate(data_query):
            signal = tuple((n, reg))
            self.registerProgress.emit(signal)
            
        self.finished.emit(1) #* todo bien
        conn.close()





class DbDeleteWorker(QObject):
    '''Clase WORKER que se encarga de ejecutar las consultas de tipo DELETE a la base de datos.
    Este WORKER guarda los registros eliminados de la base de datos en archivos .csv.'''
    progress = Signal(int) # devuelve un int con el progreso que lleva borrado para actualizar el progressbar en MainWindow.
    finished = Signal(int)
    
    def executeDeleteQuery(self, params:list[tuple[int,str]], sql:str=None, mult_sql:tuple[str]=None) -> None:
        '''
        Hace la consulta DELETE a la base de datos.
        
        PARAMS:
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
            if sql and not mult_sql:
                for n,param in enumerate(params):
                    cursor.execute(sql, param)
                    conn.commit()
                    self.progress.emit(n)
                    logging.debug(f">> Consulta DELETE a ID={param[0]} realizada exitosamente...")
                logging.debug(f">> Todas las consultas DELETE terminadas.")
                
            elif not sql and mult_sql:
                for n,param in enumerate(params):
                    for sql in mult_sql:
                        cursor.execute(sql, param[:sql.count("?")])
                        conn.commit()
                    logging.debug(f">> Consulta DELETE a ID={param[0]} realizada exitosamente...")
                    self.progress.emit(n)
                logging.debug(f">> Todas las consultas DELETE terminadas.")
                
            
        except sqlite3Error as err: #! errores de base de datos, consultas, etc.
            conn.rollback()
            logging.error(f">> {err.sqlite_errorcode}: {err.sqlite_errorname} / {err}")
            self.finished.emit(err.sqlite_errorcode)
            
        finally:
            conn.close()
            
        self.finished.emit(1) #* todo bien
        conn.close()





class DbInsertWorker(QObject):
    '''Clase WORKER que se encarga de ejecutar las consultas de tipo INSERT a la base de datos.'''
    finished = Signal(int) # emite 0 si no se pudo establecer comunicación con la base de datos, sino 1.
    
    
    @Slot(str,tuple,bool)
    def executeInsertQuery(self, data_sql:str, data_params:tuple=None, SINGLE_REG:bool=True) -> None:
        '''
        Hace la consulta INSERT a la base de datos.
        
        PARAMS:
        - data_sql: la consulta con el registro a insertar.
        - data_params: los parámetros de la consulta 'data_sql'. Por defecto es None.
        - SINGLE_REG: flag que determina si solo se inserta un registro. Por defecto es True.
        
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
        
        if SINGLE_REG:
            try:
                cursor.execute(data_sql, data_params) if data_params else cursor.execute(data_sql)
                logging.debug(f">> Consulta INSERT realizada exitosamente...")
                
                conn.commit()
                self.finished.emit(1) #* todo bien
                
            except sqlite3Error as err:
                conn.rollback()
                logging.error(f">> {err.sqlite_errorcode}: {err.sqlite_errorname} / {err}")
                self.finished.emit(err.sqlite_errorcode) #! error al realizar el insert
                
            finally:
                conn.close()
        return None





class DbUpdateWorker(QObject):
    '''Clase WORKER que se encarga de ejecutar las consultas de tipo UPDATE a la base de datos.
    Este WORKER es usado también para marcar registros como eliminados en la columna "eliminado" en la base de datos.'''
    progress = Signal(int)
    finished = Signal(int)
    
    
    @Slot(str,tuple,bool)
    def executeUpdateQuery(self, sql:str, params:tuple[int,str]) -> None:
        '''
        Hace la consulta UPDATE a la base de datos.
        
        PARAMS:
        - sql: consulta UPDATE a ejecutar.
        - params: parámetros para consulta 'sql'. Guarda como 'int' el ID del registro y como 'str' un dato 
        de un registro único.
        
        SEÑALES:
        La señal 'finished' emite:
        - 0: si no se pudo establecer una conexión con la base de datos.
        - 1: si no hubo errores.
        - sqlite3.Error.sqlite_errorcode: si hubo un error concreto, emite el código de error de sqlite3.
        
        La señal 'progress' emite un 'int' que indica el progreso de actualización.
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
                logging.debug(f">> Consulta UPDATE a ID={param[0]} realizada exitosamente...")
            logging.debug(f">> Todas las consultas UPDATE terminadas.")
            
        except sqlite3Error as err:
            conn.rollback()
            logging.error(f">> {err.sqlite_errorcode}: {err.sqlite_errorname} / {err}")
            self.finished.emit(err.sqlite_errorcode) #! error al realizar el update
                
        finally:
            conn.close()
            
        self.finished.emit(1) #* todo bien
        return None