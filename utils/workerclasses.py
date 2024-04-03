'''
En este archivo están todas las clases de WORKER THREADS
'''
from PySide6.QtCore import (QObject, Signal)

from functionutils import (createConnection)

from sqlite3 import (Connection)
from typing import (Any)


class DbReadWorker(QObject):
    '''Clase WORKER que se encarga de ejecutar las consultas de tipo READ a la base de datos.'''
    progress = Signal(object) # envía una list[Any] por cada registro coincidente
    finished = Signal(int) # si hubo algún error envía 0, sino 1

    def executeReadQuery(self, sql:str, params:tuple = None) -> list:
        '''Hace la consulta SELECT a la base de datos y devuelve los valores de las filas seleccionadas. Retorna una 'list' 
        con los valores.'''
        query:list[Any]
        conn:Connection|None

        conn = createConnection("database/inventario.db")
        if not conn:
            self.finished.emit(0) #! si hubo un error devuelve 0
        cursor = conn.cursor()
        query = cursor.execute(sql).fetchall() if not params else cursor.execute(sql, params).fetchall()
        conn.close()
        for reg in query:
            self.progress.emit(reg)
        self.finished.emit(1) #* todo bien

        # TODO: conectar estas señales al MainWindow