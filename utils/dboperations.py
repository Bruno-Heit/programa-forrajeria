'''
En este archivo están las operaciones a la base de datos sencillas que no requieren 
de MULTITHREADING por tardar poco para ejecutarse... Son operaciones CRUD simples 
que tienen la intención de no generar resultados masivos.

También contiene la clase 'DatabaseRepository' que, usando el patrón de diseño de 
repositorio, contiene las consultas a bases de datos generales.

Contiene direcciones generales relacionadas con base de datos.

Por último coloqué acá la función 'pyinstallerCompleteResourcePath' para evitar 
'circular import' con 'utils/functionutils'.
'''
import os # para obtener el 'relative path' de algunos archivos cuando se ejecutan luego de empaquetarse con pyinstaller...
import sys # sirve para lo mismo que el módulo 'os'.

from sqlite3 import (connect, Connection, Cursor, ProgrammingError, Error as sqlite3Error)
from typing import (Any)
import logging
from datetime import (datetime)
from re import (Match, compile, fullmatch, search, IGNORECASE)
from platformdirs import (user_data_dir)
import os

from utils.enumclasses import (Regex, DateAndTimeFormat, ProgramValues as PV)


# direcciones
DATABASE_DIR = user_data_dir(appname=PV.APP_NAME.value,
                             appauthor=PV.APP_AUTHOR.value,
                             ensure_exists=True) + "/database/db_gestion.db"
DATABASE_MEMORY:str = ":memory:"
DATABASE_MEMORY_SHARED:str = "file::memory:?cache=shared"



# repositorio de base de datos
class DatabaseRepository():
    '''Clase repositorio y "context manager" para realizar operaciones a la 
    base de datos.'''
    
    def __init__(self, db_path:str=DATABASE_DIR) -> None:
        self._db_path:str = db_path
        self._connection:Connection = None
    
    
    def __enter__(self):
        self._connection = createConnection(
            db_name=self._db_path,
            shared_memory_db=True if self._db_path == DATABASE_MEMORY_SHARED else False
            )
        return self
    
    
    def __exit__(self, exc_type, exc_value, exc_trc) -> None:
        if exc_type:
            logging.critical(f"{exc_type}:{exc_value}")
            
        self._connection.close()
        return None
    
    
    def executeScript(self, sql:str) -> bool:
        '''
        Ejecuta el script ingresado.

        Parámetros
        ----------
        sql : str
            script a ejecutar
        
        Retorna
        -------
        bool
            True si el script se ejecutó exitosamente, sino False
        '''
        cursor = self._connection.cursor()    
        try:
            cursor.executescript(sql)
            self._connection.commit()
        
        except (ProgrammingError, sqlite3Error) as err:
            self._connection.rollback()
            logging.critical(f"{err}")
            return False
        
        return True
    
    
    def __executeQuery(self, sql:str, params:tuple=None, executemany:bool=False) -> Cursor:
        '''
        Realiza la consulta entregada independientemente del tipo y devuelve el cursor 
        con el resultado.

        Parámetros
        ----------
        sql : str
            Consulta de tipo CRUD
        params : tuple, opcional
            Parámetros de la consulta, por defecto es None
        executemany: bool, opcional
            Flag que determina si la misma consulta se debe ejecutar múltiples veces 
            con diferentes valores de parámetros. NOTA: executemany requiere que 'params' 
            también tenga un valor asignado

        Retorna
        -------
        Cursor
            Cursor con los registros resultantes sin filtrar de la consulta
        '''
        cursor = self._connection.cursor()
        match executemany:
            case False:
                try:
                    if params:
                        cursor.execute(sql, params)
                    else:
                        cursor.execute(sql)
                    self._connection.commit()
                
                except sqlite3Error as err:
                    self._connection.rollback()
                    logging.critical(f"{err}")
            
            case True:
                try:
                    cursor.executemany(sql, params)
                    self._connection.commit()
                
                except ProgrammingError as err:
                    self._connection.rollback()
                    logging.critical(f"{err}")
                
                except sqlite3Error as err:
                    self._connection.rollback()
                    logging.critical(f"{err}")
        
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
    
    
    def updateRegisters(self, upd_sql:str, upd_params:tuple, executemany:bool=False) -> None:
        '''
        Realiza una consulta de tipo UPDATE.

        Parámetros
        ----------
        upd_sql : str
            Consulta para actualizar los registros coincidentes
        upd_params : tuple
            Parámetros para la consulta
        executemany: bool, opcional
        Flag que determina si la misma consulta se debe ejecutar múltiples veces 
        con diferentes valores de parámetros

        Retorna
        -------
        None
        '''
        self.__executeQuery(upd_sql, upd_params, executemany)
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



# funciones generales
#? La siguiente función sirve para ayudar a pyinstaller a completar el path completo a un archivo, 
#? y se tiene que hacer esto porque tiene un error y a veces no puede hacerlo.
def pyinstallerCompleteResourcePath(relative_path:str) -> str:
    '''
    Obtiene el *path* completo para el archivo especificado.
    
    Parámetros
    ----------
    relative_path : str
        el *path* relativo del archivo al programa
    
    Retorna
    -------
    str
        el *path* completo del archivo
    '''
    base_path:str
    full_path:str
    
    try:
        base_path = sys._MEIPASS
    
    except AttributeError as err:
        logging.error("No se encuentra el atributo 'sys._MEIPASS'")
        base_path = os.path.abspath(".")
    
    except Exception as err:
        logging.critical(err)
        base_path = os.path.abspath(".")
    
    finally:
        full_path = os.path.join(base_path, relative_path.replace("/", "\\"))
        __createDirPathIfNotExists(full_path)
    
    return full_path


def __createDirPathIfNotExists(full_path:str) -> None:
    '''
    Crea los directorios del *path* si no existen.

    Parámetros
    ----------
    full_path : str
        *path* al cual crear directorio
    '''
    os.makedirs("\\".join(full_path.split("\\")[:-1]), exist_ok=True)
    return None


def createConnection(db_name:str, shared_memory_db:bool=False) -> Connection | None:
    '''
    Crea una conexión a la base de datos y devuelve la conexión. En caso de 
    no encontrarse la dirección de la base de datos se crea una conexión en 
    memoria.
    
    Parámetros
    ----------
    db_name : str
        dirección de la base de datos
    shared_memory_db : bool
        *flag* que determina si usar una base de datos en memoria compartida
    
    Retorna
    -------
    Connection | None
        devuelve el objeto **Connection**, si no se pudo devuelve ***None***
    '''
    alt_db_path = DATABASE_MEMORY_SHARED if shared_memory_db else DATABASE_MEMORY
    try:
        connection = connect(
            db_name if db_name == alt_db_path else pyinstallerCompleteResourcePath(db_name),
            uri=True if alt_db_path == DATABASE_MEMORY_SHARED else False
        )
    
    except sqlite3Error as err:
        logging.critical(f"{err.sqlite_errorcode}: {err.sqlite_errorname} / {err}")
        connection = None

    except Exception as err:
        logging.critical(err)
        connection = None
    return connection


def makeReadQuery(sql:str, params:tuple = None) -> list[tuple]:
    '''
    Hace la consulta SELECT a la base de datos y devuelve los valores de las filas seleccionadas. 
    
    IMPORTANTE: esta función no muestra feedback en caso de errores.
    
    Retorna una 'list[tuple]' con los valores.
    '''
    conn = createConnection(DATABASE_DIR)
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
    conn = createConnection(DATABASE_DIR)
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
    conn = createConnection(DATABASE_DIR)
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


# configuraciones iniciales
def createTables(path:str=DATABASE_DIR) -> None:
    '''
    Verifica que las tablas existan dentro de la base de datos, sino las 
    crea.
    
    Parámetros
    ----------
    path : str, opcional
        *path* en el que crear la base de datos, por defecto toma el valor de 
        la variable global "DATABASE_DIR"; alternativamente se puede pasar el 
        valor de la variable "DATABASE_MEMORY" o "DATABASE_MEMORY_SHARED" para 
        crear una base de datos en memoria para hacer tests, o la dirección 
        que se desee
    '''
    res:bool
    
    with DatabaseRepository(db_path=path) as db_repo:
        res = db_repo.executeScript(
            sql= '''-- Categorias
                    CREATE TABLE IF NOT EXISTS Categorias (
                        IDcategoria      INTEGER    PRIMARY KEY AUTOINCREMENT
                                                    NOT NULL,
                        nombre_categoria TEXT (40)  NOT NULL
                                                    UNIQUE ON CONFLICT ROLLBACK,
                        descripcion      TEXT (255) 
                    );
                    
                    -- Productos
                    CREATE TABLE IF NOT EXISTS Productos (
                        IDproducto    INTEGER     PRIMARY KEY AUTOINCREMENT
                                                NOT NULL,
                        nombre        TEXT (50)   NOT NULL
                                                UNIQUE ON CONFLICT FAIL,
                        descripcion   TEXT (256),
                        stock         REAL        NOT NULL,
                        unidad_medida TEXT,
                        precio_unit   REAL        NOT NULL,
                        precio_comerc REAL,
                        IDcategoria   INTEGER     REFERENCES Categorias (IDcategoria) 
                                                NOT NULL,
                        eliminado     INTEGER (1) NOT NULL ON CONFLICT ROLLBACK
                                                DEFAULT (0) 
                    );
                    
                    -- Ventas
                    CREATE TABLE IF NOT EXISTS Ventas (
                        IDventa        INTEGER     PRIMARY KEY AUTOINCREMENT
                                                NOT NULL,
                        fecha_hora     TEXT        NOT NULL,
                        detalles_venta TEXT,
                        eliminado      INTEGER (1) DEFAULT (0) 
                                                NOT NULL ON CONFLICT ROLLBACK
                    );
                    
                    CREATE INDEX IF NOT EXISTS index_ventas_fecha_hora ON Ventas(fecha_hora);
                    
                    -- Deudores
                    CREATE TABLE IF NOT EXISTS Deudores (
                        IDdeudor      INTEGER    PRIMARY KEY AUTOINCREMENT
                                                NOT NULL,
                        nombre        TEXT (40)  NOT NULL,
                        apellido      TEXT (40)  NOT NULL,
                        num_telefono  TEXT,
                        direccion     TEXT (256),
                        codigo_postal TEXT
                    );
                    
                    -- Deudas
                    CREATE TABLE IF NOT EXISTS Deudas (
                        IDdeuda        INTEGER     PRIMARY KEY AUTOINCREMENT
                                                NOT NULL,
                        fecha_hora     TEXT        NOT NULL,
                        total_adeudado REAL        NOT NULL,
                        IDdeudor       INTEGER     REFERENCES Deudores (IDdeudor) 
                                                NOT NULL,
                        eliminado      INTEGER (1) NOT NULL ON CONFLICT ROLLBACK
                                                DEFAULT (0) 
                    );
                    
                    -- Detalle_Ventas
                    CREATE TABLE IF NOT EXISTS Detalle_Ventas (
                        ID_detalle_venta INTEGER     PRIMARY KEY AUTOINCREMENT
                                                    NOT NULL,
                        cantidad         REAL        NOT NULL,
                        costo_total      REAL        NOT NULL,
                        IDproducto       INTEGER     REFERENCES Productos (IDproducto) 
                                                    NOT NULL,
                        IDventa          INTEGER     REFERENCES Ventas (IDventa) 
                                                    NOT NULL,
                        abonado          REAL        NOT NULL,
                        IDdeuda          INTEGER     REFERENCES Deudas (IDdeuda),
                        eliminado        INTEGER (1) NOT NULL ON CONFLICT ROLLBACK
                                                    DEFAULT (0) 
                    );
            '''
        )
        
        if res:
            logging.info("tablas creadas exitosamente")
    return None


def ensureDateTimeISOformat() -> None:
    '''
    Realiza modificaciones a la base de datos corrigiendo el formato de fecha 
    de todas las columnas de las tablas *Ventas* y *Deudas* para usar el 
    formato **ISO 8601** si no lo hacían.
    '''
    registers:list[tuple[Any]]
    changes:int = 0
    
    with DatabaseRepository() as db_repo:
        # actualiza Ventas
        registers= db_repo.selectRegisters(
            data_sql='''SELECT IDventa, fecha_hora 
                        FROM Ventas;'''
        )
        
        for IDsale, curr_dt in registers:
            if curr_dt is None or __is_ISO_format(curr_dt):
                continue
            
            try: # intenta convertir el formato anterior al formato ISO 8601
                db_repo.updateRegisters(
                    upd_sql= '''UPDATE Ventas 
                                SET fecha_hora = ? 
                                WHERE IDventa = ?;''',
                    upd_params=(
                        __datetime_to_ISO_format(curr_dt),
                        IDsale,
                    )
                )
                changes += 1
            
            except ValueError:
                _warning_msg = "La fecha {curr_dt} es inválida"
                logging.warning(_warning_msg)
    
        _info_msg = f"Fechas de Ventas actualizadas correctamente al formato ISO 8601 -> nro. cambios: {changes}"
        logging.info(_info_msg)
        
        changes = 0
        
        # actualiza Deudas
        registers= db_repo.selectRegisters(
            data_sql='''SELECT IDdeuda, fecha_hora 
                        FROM Deudas;'''
        )
        
        for IDdebt, curr_dt in registers:
            if curr_dt is None or __is_ISO_format(curr_dt):
                continue
            
            try: # intenta convertir el formato anterior al formato ISO 8601
                db_repo.updateRegisters(
                    upd_sql= '''UPDATE Deudas 
                                SET fecha_hora = ? 
                                WHERE IDdeuda = ?;''',
                    upd_params=(
                        __datetime_to_ISO_format(curr_dt),
                        IDdebt,
                    )
                )
                changes += 1
            
            except ValueError:
                _warning_msg = "La fecha {curr_dt} es inválida"
                logging.warning(_warning_msg)
        
        _info_msg = f"Fechas de Deudas actualizadas correctamente al formato ISO 8601 -> nro. cambios: {changes}"
        logging.info(_info_msg)
    return None


def __is_ISO_format(date_time:str) -> bool:
    '''
    Verifica si la fecha y hora ingresada siguen el formato **ISO 8601**.

    Parámetros
    ----------
    date_time : str
        fecha y hora que verificar

    Retorna
    -------
    bool
        flag que determina si la fecha y hora siguen el formato **ISO 8601**
    '''
    return fullmatch(Regex.ISO_8601_FORMAT.value, date_time) is not None


def __datetime_to_ISO_format(date_time:str) -> str:
    '''
    Convierte la fecha y hora ingresadas al formato **ISO 8601**.

    Parámetros
    ----------
    date_time : str
        fecha y hora que convertir

    Retorna
    -------
    str
        fecha y hora en formato **ISO 8601**
    '''
    date_time = date_time.replace("-", "/")
    _dt = datetime.strptime(date_time, DateAndTimeFormat.DIR_LOCAL_DATETIME_FORMAT.value)
    return _dt.strftime(DateAndTimeFormat.DIR_DATETIME_ISO_8601.value)
