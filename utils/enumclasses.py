'''
En este archivo están las classes que heredan de Enum, y sirve más que nada para 
simplificar la lectura de algunos valores recurrentes.

'''
from PySide6.QtGui import (QColor)

from enum import (Enum, StrEnum, IntEnum)


class LabelFeedbackStyle(StrEnum):
    '''Clase con StrEnum con estilos predefinidos para darle a los QLabel 
    dependiendo de si son válidos los datos del QTableView asociado o no.'''
    VALID = '''font-family: 'Verdana'; 
            font-size: 16px; 
            letter-spacing: 0px; 
            word-spacing: 0px; 
            background-color: rgb(88, 223, 171); 
            color: #111;'''
    INVALID = '''font-family: 'Verdana'; 
                font-size: 16px; 
                letter-spacing: 0px; 
                word-spacing: 0px; 
                color: #f00; 
                border: 1px solid #f00; 
                background-color: rgb(255, 185, 185);'''





class TableViewId(IntEnum):
    '''Clase con IntEnum con "IDs" para cada uno de los QTableView.'''
    INVEN_TABLE_VIEW = 0
    SALES_TABLE_VIEW = 1
    DEBTS_TABLE_VIEW = 2





class InventoryPriceType(IntEnum):
    '''IntEnum con los 2 tipos de precios que se pueden modificar en la tabla Inventario 
    en la base de datos.'''
    NORMAL = 1
    COMERCIAL = 2





class TableFontColor(Enum):
    '''Enum con QColors para la tipografía de QTableViews.'''
    DEF_COLOR = QColor(17, 17, 17, 255)
    CONTRAST_RED = QColor(218, 17, 17, 255)
    CONTRAST_WHITE = QColor(238, 238, 238, 255)





class TableBgColors(Enum):
    '''Enum con QColors para columnas de QTableViews. Contiene sus versiones normales 
    y las variantes de color para filas alternantes.'''
    LOW_STOCK_ROW = QColor(245, 165, 165, 255)
    UNIT_PRICE_ROW = QColor(253, 214, 118, 200)
    COMERC_PRICE_ROW = QColor(251, 189, 173, 200)
    SALES_LOWER_PAID = QColor(226, 180, 177, 255)





class ModelHeaders(Enum):
    '''Enum con tuples[headers] para las QTableViews que usan los MODELOS DE DATOS.'''
    INVENTORY_HEADERS = ("Categoría", "Nombre del producto", "Descripción", 
                         "Stock", "Precio normal", "Precio comercial")
    SALES_HEADERS = ("Detalle de venta", "Cantidad", "Producto", "Costo total", 
                     "Abonado", "Fecha y hora")
    DEBTS_HEADERS = ("Datos de la persona", "productos", "Saldo")





class DBQueries(IntEnum):
    '''IntEnum con las operaciones CRUD a base de datos.'''
    SELECT_COUNT = 0
    SELECT_REGISTERS = 1
    DELETE_REGISTERS = 2
    UPDATE_REGISTERS = 3
    INSERT_REGISTERS = 4





# estilos generales para widgets
class WidgetStyle(StrEnum):
    '''Clase de tipo 'strEnum' con estilos generales para aplicar a los widgets.'''
    LABEL_NEUTRAL_VAL = "color: #555; border: none; background-color: rgba(200,200,200,0.7);"
    FIELD_VALID_VAL = "border: 1px solid #40dc26; background-color: rgba(185, 224, 164, 0.7);"
    FIELD_INVALID_VAL = "border: 1px solid #dc2627; background-color: rgba(224, 164, 164, 0.7);"





# mensajes predeterminados para logging
class LoggingMessage(StrEnum):
    '''Clase de tipo 'strEnum' con mensajes predeterminados para mostrar en las funciones de logging.'''
    DEBUG_DB_SINGLE_SELECT_SUCCESS = "Consulta SELECT realizada exitosamente"
    DEBUG_DB_MULT_SELECT_SUCCESS = "Todas las consultas SELECT finalizadas exitosamente"
    ERROR_DB_SELECT = "Error en consulta SELECT"
    
    DEBUG_DB_SINGLE_UPDATE_SUCCESS = "Consulta UPDATE realizada exitosamente"
    DEBUG_DB_MULT_UPDATE_SUCCESS = "Todas las consultas UPDATE finalizadas exitosamente"
    ERROR_DB_UPDATE = "Error en consulta UPDATE"
    
    DEBUG_DB_SINGLE_INSERT_SUCCESS = "Consulta INSERT realizada exitosamente"
    DEBUG_DB_MULT_INSERT_SUCCESS = "Todas las consultas INSERT finalizadas exitosamente"
    ERROR_DB_INSERT = "Error en consulta INSERT"
    
    DEBUG_DB_SINGLE_DELETE_SUCCESS = "Consulta DELETE realizada exitosamente"
    DEBUG_DB_MULT_DELETE_SUCCESS = "Todas las consultas DELETE finalizadas exitosamente"
    ERROR_DB_DELETE = "Error en consulta DELETE"
    
    WORKER_SUCCESS = "WORKER terminó de ejecutarse correctamente"





# tipos de sidebars
class TypeSideBar(IntEnum):
    '''Clase de tipo 'IntEnum' con valores que sirven para identificar las sidebars.'''
    CATEGORIES_SIDEBAR = 1
    PERCENTAGES_SIDEBAR = 2





# [ListItemValues] tipos de campos a validar para el formulario de Ventas
class ListItemFields(IntEnum):
    '''Clase de tipo 'IntEnum' con los campos de los cuales se guarda registro 
    cuando se debe ingresar Ventas dede el formulario de ventas.'''
    PRODUCT_ID = 0
    PRODUCT_NAME = 1
    QUANTITY = 2
    SUBTOTAL = 3
    IS_COMERCIAL_PRICE = 4
    SALE_DETAILS = 5
    IS_ALL_VALID = 6





# tipos de campos a validar para Deudas
class DebtsFields(IntEnum):
    '''Clase de tipo 'IntEnum' con los campos de los cuales se guarda registro 
    cuando se debe ingresar Deudas.'''
    NAME = 0
    SURNAME = 1
    PHONE_NUMB = 2
    DIRECTION = 3
    POSTAL_CODE = 4


# nombres predeterminados de columnas de tablas
class TableViewColumns(IntEnum):
    '''Clase de tipo 'IntEnum' con los nombres predeterminados de las columnas de las 
    VISTAS.'''
    INV_CATEGORY = 0
    INV_PRODUCT_NAME = 1
    INV_DECRIPTION = 2
    INV_STOCK = 3
    INV_NORMAL_PRICE = 4
    INV_COMERCIAL_PRICE = 5
    
    SALES_DETAIL = 0
    SALES_QUANTITY = 1
    SALES_PRODUCT_NAME = 2
    SALES_TOTAL_COST = 3
    SALES_TOTAL_PAID = 4
    SALES_DATETIME = 5
    
    ...
    # TODO: poner acá los nombres de columnas de tabla de Deudas


class TableModelDataColumns(IntEnum):
    '''Clase de tipo 'IntEnum' con las columnas que maneja cada modelo de datos 
    internamente en su respectivo atributo '_data', ya que los datos internos del 
    MODELO DE DATOS son diferentes a los datos que muestra la VISTA.'''
    INV_IDPRODUCT = 0
    INV_CATEGORY_NAME = 1
    INV_NAME = 2
    INV_DESCRIPTION = 3
    INV_STOCK = 4
    INV_MEASUREMENT_UNIT = 5
    INV_NORMAL_PRICE = 6
    INV_COMERCIAL_PRICE = 7
    
    SAL_ID_SALES_DETAIL = 0
    SAL_SALES_DETAIL = 1
    SAL_QUANTITY = 2
    SAL_MEASUREMENT_UNIT = 3
    SAL_NAME = 4
    SAL_TOTAL_COST = 5
    SAL_PAID = 6
    SAL_DATETIME = 7
    
    ...
    # TODO: poner acá las columnas internas del modelo de tabla de Deudas




# expresiones regulares para validadores o búsqueda
class Regex(StrEnum):
    '''
    Clase StrEnum con expresiones regulares predefinidas, creadas principalmente para 
    usarse en 'utils.customvalidators.py', pero no exclusivamente.
    '''
    SEARCH_BAR = "[^;\"']*"
    
    PROD_NAME = "[^;\"']{1,50}"
    PROD_STOCK = "(\d{1,8}(\.|,)?\d{0,2} {1}[a-zA-Z]{0,20})|(\d{1,8}(\.|,)?\d{0,2})"
    PROD_UNIT_PRICE = "\d{1,8}((\.|,){1}\d{0,2})?"
    PROD_COMERC_PRICE = "\d{0,8}((\.|,)\d{0,2})?"
    PERCENTAGE_CHANGE = "^([-+]?\d{0,4}((\.|,)\d{0,2})?)|(\d{1,8}((\.|,)\d{0,2})?)$"
    
    SALES_DETAILS_PRICE_TYPE = "(\([\s]*P[\s]*\.[\s]*PÚBLICO[\s]*\)|\([\s]*P[\s]*\.[\s]*COMERCIAL[\s]*\))$"
    SALES_DETAILS_FULL = "[0-9]{1,8}(\.|,)?[0-9]{0,2}\sde .{1,}\s(\([\s]*P[\s]*\.[\s]*PÚBLICO[\s]*\)|\([\s]*P[\s]*\.[\s]*COMERCIAL[\s]*\))$"
    SALES_QUANTITY = "[0-9]{1,8}(\.|,)?[0-9]{0,2}"
    # TODO: seguir poniendo acá las expresiones de los validadores