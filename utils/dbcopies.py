'''
Este módulo tiene funciones que sirven para hacer copias de seguridad de la base de 
datos "database/inventario.db", y además para hacer copias de los registros ELIMINADOS 
de las diferentes tablas a archivos CSV que sirven a modo de "histórico/copias".

Cuando se muestran datos en las tablas, primero se intenta obtener datos desde "inventario.db", 
pero si se elimina algún registro va a devolver error, por lo que, de ser necesario, se deben 
buscar algunos registros en los archivos históricos.

EJEMPLO:
    se quiere mostrar un producto vendido, pero ese producto ya no está disponible en "inventario.db",
    al buscarse en la base de datos no se encontrará y devolverá un error. 
    Entonces se busca en el historial de productos y así se completa el registro a mostrar.
    (Lo mismo sucede con las ventas o cuentas corrientes).


DIAGRAMA DE ACCESO A REGISTROS:
                ACCEDER A REGISTRO
                        ┃
                        ↓
              ¿ESTÁ EN inventario.db?
                    SI      NO
            ┏━━━━━━━┛       ┗━━━━━━━┓
            ┃                       ┃
            ┃          EL REGISTRO FUE ELIMINADO DE LA B.D., 
            ┃                BUSCA EN EL HISTORIAL
            ┃                       ┃
    ACCEDE AL REGISTRO              ↓
            ↓                 ┍━━━━━━━━━━━━━━━━━┓
    ┏━━━━━━━━━━━━━━━┓       ┏━┻━━━━━━━━━━━━━━━┓ ┃
    ┃ inventario.db ┃       ┃ historiales.csv ┃ ┃━┓
    ┃      ...      ┃       ┃       ...       ┃ ┃ ┃
    ┃      ...      ┃       ┃       ...       ┃ ┃ ┃
    ┃      ...      ┃       ┃       ...       ┃━┛ ┃
    ┗━━━━━━┳━━━━━━━━┛       ┗━━━┳━━━━━━━━━━━━━┛   ┃
           ┃                    ┗━━━━━━━━━━━━━━━━━┛
           ┃                        ┃
           ┗━━━━━━━━━━━━┳━━━━━━━━━━━┛
                        ↓
                DEVUELVE EL REGISTRO
'''                                 

import sqlite3
from sqlite3 import Connection
from functionutils import (createConnection)
import os


def saveAllDatabaseTables(n_records:int=-1) -> None:
    '''Hace un recorrido de todas las tablas y guarda los últimos 'n_records' registros.
    \nPor defecto 'n_records' es -1, lo que significa que guarda todos los registros de todas las tablas \
    en archivos.
    \nRetorna 'None'.'''
    conn:Connection = createConnection("inventario.db")
    cursor = conn.cursor()
    
    # TODO 1: crear función que verifique si la base de datos existe, sino que la cree.
    # TODO 2: crear función que verifique si todas las tablas existen, sino que las cree.
    # TODO 3: crear función que verifique si todos los archivos de tipo historial.csv existen, sino que los cree.
    # TODO 4: crear función que permita obtener los registros que se borran y mandarlos a cada archivo historial.csv.


def verifyDatabaseExistence(db_name:str) -> None:
    '''Verifica si existe la base de datos 'db_name' y si no existe la crea. 
    \nRetorna None.'''
    if not os.path.exists("../database/inventario.db"):
        # TODO: escribir código para crear base de datos (obtenerlo de sqlite)
        pass