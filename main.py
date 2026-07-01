from app import setup_app
import logging
from logging.handlers import TimedRotatingFileHandler
from utils.dboperations import createTables, ensureDateTimeISOformat
from utils.enumclasses import ProgramValues
from PySide6.QtCore import QSettings

def setup_logging() -> None:
    handler = TimedRotatingFileHandler(
        filename="program.log",
        when="midnight", # rota a medianoche,
        interval=1, # cada 1 día
        backupCount=14, # mantiene 30 días de logs
        encoding="utf-8"
    )
    
    formatter = logging.Formatter(
        "%(asctime)s - (%(levelname)s) - %(module)s.%(funcName)s - %(message)s",
        datefmt="%A %Y-%m-%d %H:%M:%S"
    )
    handler.setFormatter(formatter)
    
    logging.basicConfig(
        level=logging.DEBUG,
        handlers=[handler, logging.StreamHandler()],
    )
    return None

def setup_database() -> None:
    createTables()
    ensureDateTimeISOformat()
    return None

def main():
    # TODO: en las barras de búsqueda, filtrar a medida que el usuario teclea. Para 
    # TODO: eso hacer un "debounce" con un timer: cuando el usuario empieza a teclear 
    # TODO: iniciar/reiniciar el timer, pero sólo filtrar cuando el timer termina, 
    # TODO: de esa forma se evitar filtrar cada vez que el usuario escribe una tecla 
    # TODO: y sólo se filtra cuando el usuario dejó de escribir por un tiempo (por 
    # TODO: ej: 2 segundos)
    
    # TODO1: permitir crear ofertas
    
    # TODO2: corregir validación del nombre en inventario cuando se hace doble 
    # TODO2: click en una celda (aparece el mensaje de nombre inválido cuando el 
    # TODO2: se pierde el foco del lineedit)
    
    # TODO3 (?): cambiar la forma en que se muestran las ventas: permitir ver las 
    # TODO3 (?): ventas como páginas
    setup_logging()

    # configuraciones
    settings = QSettings(ProgramValues.APP_NAME.value, ProgramValues.APP_AUTHOR.value)

    # base de datos
    setup_database()
    
    setup_app()
    return None


# MAIN #########################################################################################################
if __name__ == "__main__":
    main()
