'''
En este archivo están las operaciones a la base de datos sencillas, que no requieren 
de MULTITHREADING por tardar mucho para ejecutarse... Son operaciones CRUD simples 
que tienen la intención no generar resultados masivos.

Además coloqué acá la función 'pyinstallerCompleteResourcePath' para evitar 
'circular import' con 'utils/functionutils'.
'''
import os # para obtener el 'relative path' de algunos archivos cuando se ejecutan luego de empaquetarse con pyinstaller...
import sys # sirve para lo mismo que el módulo 'os'.

from sqlite3 import (connect, Connection, Error as sqlite3Error)
import logging


'''
La siguiente función sirve para ayudar a pyinstaller a completar el path completo a un archivo, 
y se tiene que hacer esto porque tiene un error y a veces no puede hacerlo.
'''
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
        print(f"{err.sqlite_errorcode}: {err.sqlite_errorname} / {err}")
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
        logging.critical(f">> {err.sqlite_errorcode}: {err.sqlite_errorname} / {err}")
    
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
        logging.critical(f">> {err.sqlite_errorcode}: {err.sqlite_errorname} / {err}")
    
    finally:
        conn.close()
    
    return None
