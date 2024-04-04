'''
En este archivo están todas las clases de WORKER THREADS
'''
from PySide6.QtCore import (QObject, Signal)

from utils.functionutils import (createConnection)

from sqlite3 import (Connection)
from typing import (Any)


class DbReadWorker(QObject):
    '''Clase WORKER que se encarga de ejecutar las consultas de tipo READ a la base de datos.'''
    countProgress = Signal(int) # envía un int que representa el COUNT() de registros
    registerProgress = Signal(object) # envía una list[Any] con cada registro coincidente
    finished = Signal(int) # si hubo algún error envía 0, sino 1

    def executeReadQuery(self, sql:str, params:tuple = None, COUNT_OPERATION:bool=True) -> list:
        '''
        Hace la consulta SELECT a la base de datos y devuelve los valores de las filas seleccionadas. 
        
        'sql' es la consulta READ a ejecutar.
        
        'params' son los parámetros de la consulta. Por defecto es None.

        'COUNT_OPERATION' es un flag, si es True es porque la consulta es para obtener el COUNT() de registros 
        coincidentes, sino es una consulta para obtener todos los registros coincidentes.

        Retorna una 'list' con los valores.
        '''
        query:list[Any] | int # es una lista si obtiene registros, es int si obtiene COUNT() de registros
        conn:Connection|None

        conn = createConnection("database/inventario.db")
        if not conn:
            self.finished.emit(0) #! si hubo un error devuelve 0
        cursor = conn.cursor()

        if not COUNT_OPERATION:
            query = cursor.execute(sql).fetchall() if (not params) else cursor.execute(sql, params).fetchall()
            self.registerProgress.emit(reg for reg in query)
        else:
            query = cursor.execute(sql).fetchone()[0] if (not params) else cursor.execute(sql, params).fetchone()[0]
            self.countProgress.emit(query)

        conn.close()

        self.finished.emit(1) #* todo bien