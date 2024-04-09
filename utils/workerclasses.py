'''
En este archivo están todas las clases de WORKER THREADS
'''
from PySide6.QtCore import (QObject, Signal, Slot)

from utils.functionutils import (createConnection)

from sqlite3 import (Connection, Error as sqlite3Error)
from typing import (Any)



class DbReadWorker(QObject):
    '''Clase WORKER que se encarga de ejecutar las consultas de tipo READ a la base de datos.'''
    countFinished = Signal(int) # se emite cuando se termina la consulta de COUNT().
    registerProgress = Signal(tuple) # envía un tuple[int[Any]] con cada registro coincidente (el 'int' se obtiene de 
                                     # 'enumerate' y sirve solamente para actualizar en MainWindow el QProgressBar de 
                                     # la tabla relacionada, lo más importante es el tuple interno '[Any]').
    finished = Signal(int) # si hubo algún error envía 0, sino 1. Se emite cuando se termina la consulta de registros.


    @Slot(str,str,tuple,tuple)
    def executeReadQuery(self, data_sql:str, data_params:tuple=None, count_sql:str=None, count_params:tuple=None) -> None:
        '''
        Hace la consulta SELECT a la base de datos y devuelve los valores de las filas seleccionadas. 
        
        - data_sql: la consulta para obtener registros a ejecutar.
        - data_params: los parámetros de la consulta 'data_sql'. Por defecto es None.
        - count_sql: (opcional) la consulta READ COUNT() a ejecutar. Por defecto es None.
        - count_params: (opcional) los parámetros de la consulta 'count_sql'. Por defecto es None.
        
        La señal 'finished' emite:
        - 0: si no se pudo establecer una conexión con la base de datos.
        - 1: si no hubo errores.
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



class DbInsertWorker(QObject):
    finished = Signal(int) # emite 0 si no se pudo establecer comunicación con la base de datos, sino 1.
    
    
    @Slot(str,tuple,bool)
    def executeInsertQuery(self, data_sql:str, data_params:tuple=None, SINGLE_REG:bool=True) -> None:
        '''
        Hace la consulta INSERT a la base de datos.
        
        - data_sql: la consulta con el registro a insertar.
        - data_params: los parámetros de la consulta 'data_sql'. Por defecto es None.
        - SINGLE_REG: flag que determina si solo se inserta un registro. Por defecto es True.
        
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
                conn.commit()
                
                self.finished.emit(1) #* todo bien
                
            except sqlite3Error as err:
                self.finished.emit(err.sqlite_errorcode) #! error al realizar el insert
                
            finally:
                conn.close()
        return None