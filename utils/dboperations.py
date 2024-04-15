'''
En este archivo están las operaciones a la base de datos sencillas, que no requieren 
de MULTITHREADING por tardar mucho para ejecutarse... Son operaciones CRUD simples 
que tienen la intención no generar resultados masivos.
'''
from utils.functionutils import (pyinstallerCompleteResourcePath)

from sqlite3 import (connect, Connection, Error as sqlite3Error)
import logging


def createConnection(db_name:str) -> Connection | None:
    '''Crea una conexión a la base de datos y devuelve la conexión, si no se pudo devuelve None.'''
    try:
        connection = connect(pyinstallerCompleteResourcePath(db_name))
    except sqlite3Error as err:
        print(f"{err.sqlite_errorcode}: {err.sqlite_errorname} / {err}")
        return None
    return connection


def makeReadQuery(sql:str, params:tuple = None) -> list:
    '''
    Hace la consulta SELECT a la base de datos y devuelve los valores de las filas seleccionadas. 
    
    IMPORTANTE: esta función no muestra feedback en caso de errores.
    
    Retorna una 'list' con los valores.
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
        logging.error(f">> {err.sqlite_errorcode}: {err.sqlite_errorname} / {err}")
    
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
        logging.error(f">> {err.sqlite_errorcode}: {err.sqlite_errorname} / {err}")
    
    finally:
        conn.close()
    
    return None
