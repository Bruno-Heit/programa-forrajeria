'''
En este archivo están las operaciones a la base de datos sencillas, que no requieren 
de MULTITHREADING por tardar poco para ejecutarse... Son operaciones CRUD simples 
que tienen la intención no generar resultados masivos. Además coloco la clase 
'DatabaseRepository' que, usando el patrón de diseño de repositorio, contiene las 
consultas a bases de datos generales.

Además coloqué acá la función 'pyinstallerCompleteResourcePath' para evitar 
'circular import' con 'utils/functionutils'.
'''
import os # para obtener el 'relative path' de algunos archivos cuando se ejecutan luego de empaquetarse con pyinstaller...
import sys # sirve para lo mismo que el módulo 'os'.

from sqlite3 import (connect, Connection, Cursor, Error as sqlite3Error, ProgrammingError)
from typing import (Any)
import logging
from contextlib import closing
from re import (Match, compile, search, IGNORECASE)


class DatabaseRepository():
    '''Clase repositorio y "context manager" para realizar operaciones a la base de datos.'''
    
    def __init__(self, db_path:str="database/inventario.db") -> None:
        self._db_path:str = db_path
        self._connection:Connection = None
    
    
    def __enter__(self):
        self._connection = createConnection(self._db_path)
        return self
    
    
    def __exit__(self, exc_type, exc_value, traceback) -> None:
        if exc_type:
            self._connection.rollback()
            logging.critical(f"{exc_type}: {exc_value}")
            
        else:
            if self._connection:
                self._connection.commit()
                self._connection.close()
        return False
    
    
    def __executeQuery(self, sql:str, params:tuple=None) -> Cursor:
        '''
        Realiza la consulta entregada independientemente del tipo y devuelve el cursor 
        con el resultado.

        Parámetros
        ----------
        sql : str
            Consulta de tipo CRUD
        params : tuple, opcional
            Parámetros de la consulta, por defecto es None

        Retorna
        -------
        Cursor
            Cursor con los registros resultantes sin filtrar de la consulta
        '''
        cursor:Cursor = self._connection.cursor()
        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)
        return cursor
    
    
    def selectRowCount(self, count_sql:str, count_params:tuple=None) -> int:
        '''
        Realiza una consulta de tipo SELECT COUNT() y devuelve la cantidad de registros coincidentes 
        en la base de datos.

        Parámetros
        ----------
        count_sql : str
            Consulta para obtener la cantidad de registros coincidentes.
        count_params : tuple, opcional
            Parámetros para la consulta, por defecto es None.

        Retorna
        -------
        int
            Cantidad de registros coincidentes.
        '''
        return self.__executeQuery(sql=count_sql, params=count_params).fetchone()[0]
    
    
    def selectColumnCount(self, sel_sql:str, sel_params:tuple[Any]=None) -> int:
        '''
        Realiza una consulta de tipo SELECT y devuelve la cantidad de columnas seleccionadas 
        por la consulta.

        Parámetros
        ----------
        sel_sql : str
            Consulta de tipo SELECT para obtener n columnas de un registro cualquiera

        Retorna
        -------
        int
            Cantidad de columnas seleccionadas
        '''
        sel_sql = self.__addLimitClauseToQuery(sel_sql)
        return len(self.__executeQuery(sel_sql, sel_params).description)
    
    
    def selectRegisters(self, data_sql:str, data_params:tuple=None) -> list[tuple[Any]]:
        '''
        Realiza una consulta de tipo SELECT y devuelve todos los registros coincidentes en la base de datos.

        Parámetros
        ----------
        data_sql : str
            Consulta para obtener los registros coincidentes.
        data_params : tuple, opcional
            Parámetros para la consulta, por defecto es None

        Retorna
        -------
        list[tuple[Any]]
            Lista con todos los registros coincidentes en formato tupla[Any].
        '''
        return self.__executeQuery(data_sql, data_params).fetchall()
    
    
    def updateRegisters(self, upd_sql:str, upd_params:tuple) -> None:
        '''
        Realiza una consulta de tipo UPDATE.

        Parámetros
        ----------
        upd_sql : str
            Consulta para actualizar los registros coincidentes.
        upd_params : tuple
            Parámetros para la consulta.

        Retorna
        -------
        None
        '''
        self.__executeQuery(upd_sql, upd_params)
        return None


    def deleteRegisters(self, del_sql:str, del_params:tuple) -> None:
        '''
        Realiza una consulta de tipo DELETE.

        Parámetros
        ----------
        del_sql : str
            Consulta para eliminar los registros coincidentes.
        del_params : tuple
            Parámetros de la consulta.

        Retorna
        -------
        None
        '''
        self.__executeQuery(del_sql, del_params)
        return None
        

    def insertRegister(self, ins_sql:str, ins_params:tuple=None) -> None:
        '''
        Realiza una consulta de tipo INSERT e inserta un registro nuevo.

        Parámetros
        ----------
        ins_sql : str
            Consulta para insertar un registro.
        ins_params : tuple, opcional
            Parámetros de la consulta, por defecto es None.

        Retorna
        -------
        None
        '''
        self.__executeQuery(ins_sql, ins_params)
        return None


    def __addLimitClauseToQuery(self, query:str) -> str:
        '''
        Comprueba si la consulta contiene la cláusula 'LIMIT 1', sino la agrega. Comprende 
        la posibilidad de estar presente la cláusula OFFSET y agrega LIMIT antes de 
        OFFSET de ser necesario.

        Parámetros
        ----------
        query : str
            Consulta SELECT a la que agregar LIMIT

        Retorna
        -------
        str
            Consulta SELECT con cláusula LIMIT al final
        '''
        limit_pattern:Match = compile("(LIMIT)", flags=IGNORECASE)
        offset_pattern:Match = compile("(OFFSET)", flags=IGNORECASE)
        
        limit_match:Match | None = search(limit_pattern, query)
        offset_match:Match | None = search(offset_pattern, query)
        
        offset_pos:int
        
        # si no hay cláusula LIMIT...
        if not limit_match:
            if offset_match: # añade LIMIT antes de OFFSET (si OFFSET está)
                offset_pos = offset_match.start()
                query = f"{query[:offset_pos]} LIMIT 1 {query[offset_pos:]}"
        
            else: # añade LIMIT al final antes de ";" (si termina en ";")
                if query.strip().endswith(";"):
                    query = f"{query.strip()[:-1]} LIMIT 1;"
                else:
                    query = f"{query.strip()} LIMIT 1;"
        return query



#? La siguiente función sirve para ayudar a pyinstaller a completar el path completo a un archivo, 
#? y se tiene que hacer esto porque tiene un error y a veces no puede hacerlo.
def pyinstallerCompleteResourcePath(relative_path:str) -> str:
    '''Obtiene el path completo para el archivo especificado y lo devuelve. Retorna un 'str'.'''
    base_path:str
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def createConnection(db_name:str) -> Connection | None:
    '''Crea una conexión a la base de datos y devuelve la conexión, si no se pudo devuelve None.'''
    try:
        connection = connect(pyinstallerCompleteResourcePath(db_name))
    except sqlite3Error as err:
        logging.critical(f"{err.sqlite_errorcode}: {err.sqlite_errorname} / {err}")
        return None
    return connection


def makeReadQuery(sql:str, params:tuple = None) -> list[tuple]:
    '''
    Hace la consulta SELECT a la base de datos y devuelve los valores de las filas seleccionadas. 
    
    IMPORTANTE: esta función no muestra feedback en caso de errores.
    
    Retorna una 'list[tuple]' con los valores.
    '''
    conn = createConnection("database/inventario.db")
    if not conn:
        return
    cursor = conn.cursor()
    if not params:
        query = cursor.execute(sql).fetchall()
    else:
        query = cursor.execute(sql, params).fetchall()
    conn.close()
    return query


def makeUpdateQuery(sql:str, params:tuple) -> None:
    '''
    Hace la consulta UPDATE a la base de datos.
    
    IMPORTANTE: esta función muestra feedback mediante 'logging' en caso de errores.
    
    Retorna None.
    '''
    conn = createConnection("database/inventario.db")
    if not conn:
        return None
    cursor = conn.cursor()
    
    try:
        cursor.execute(sql, params)
        conn.commit()
    
    except sqlite3Error as err:
        conn.rollback()
        logging.critical(f"{err.sqlite_errorcode}: {err.sqlite_errorname} / {err}")
    
    finally:
        conn.close()
    return None


def makeInsertQuery(sql:str, params:tuple = None) -> None:
    '''Hace una consulta INSERT a la base de datos. 

    IMPORTANTE: esta función muestra feedback mediante 'logging' en caso de errores.
    
    Retorna None.
    '''
    conn = createConnection("database/inventario.db")
    if not conn:
        return None
    cursor = conn.cursor()
    
    try:
        if sql and params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)
        conn.commit()
    
    except sqlite3Error as err:
        conn.rollback()
        logging.critical(f"{err.sqlite_errorcode}: {err.sqlite_errorname} / {err}")
    
    finally:
        conn.close()
    
    return None
