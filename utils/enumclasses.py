'''
En este archivo están las classes que heredan de Enum, y sirve más que nada para 
simplificar la lectura de algunos valores recurrentes.

'''
from PySide6.QtGui import (QColor)

from resources import (rc_icons)

from enum import (Enum, StrEnum, IntEnum)


class ProgramValues(StrEnum):
    '''
    Clase **StrEnum** con directrices y valores necesarios para el correcto 
    funcionamiento del programa, tales como el nombre del programa, del autor, 
    ó direcciones específicas constantes.
    '''
    APP_NAME = "Gestion-Forraje Torres"
    APP_AUTHOR = "SoftwareGestion" # éste valor sólo se usa en Windows





class SettingsDirs(StrEnum):
    '''
    Clase **StrEnum** con las direcciones de los valores guardados en las 
    configuraciones del programa.
    '''
    MW_SIZE = "MainWindow/size"
    MW_POSITION = "MainWindow/position"
    MW_GEOMETRY = "MainWindow/geometry"
    MW_STATE = "MainWindow/windowState"
    




class DateAndTimeFormat(StrEnum):
    '''
    Clase StrEnum con los formatos de fecha y hora admitidos por el programa.
    Las declaraciones de fechas y horas usadas siguen los siguientes patrones:
    
    - las usadas **internamente** en el programa tienen el prefijo "***LOCAL***"
    - las usadas en la **base de datos** tienen el sufijo "***ISO_8601***"
    - las usadas como **directivas** para los objetos *datetime* tienen el 
    prefijo "***DIR***"
    '''
    # fecha
    LOCAL_DATE_FORMAT = "d/M/yyyy"
    DIR_LOCAL_DATE_FORMAT = "%d/%m/%Y"
    DATE_ISO_8601 = "yyyy-MM-dd"
    
    # hora
    LOCAL_TIME_FORMAT = "HH:mm:ss"
    
    # fecha y hora
    LOCAL_DATETIME_FORMAT = "d/M/yyyy HH:mm:ss"
    DIR_LOCAL_DATETIME_FORMAT = "%d/%m/%Y %H:%M:%S"
    DATETIME_ISO_8601 = "yyyy-MM-d HH:mm:ss"
    DIR_DATETIME_ISO_8601 = "%Y-%m-%d %H:%M:%S"





class DateTimeRanges(IntEnum):
    '''
    Clase IntEnum con los valores máximos de los rangos de valores posibles 
    seleccionables en **QDateTimeEdits** y sus subclases.
    '''
    MAX_DAYS_DIFF = 180





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





class ProgressBarStyle(StrEnum):
    '''
    Clase StrEnum con estilos predeterminados para aplicar a las QProgressBars 
    dependiendo de la operación que se lleva a cabo en la tabla asociada.
    '''
    DELETION =  ''' QProgressBar::chunk {
                        background-color: qlineargradient(spread:reflect, x1:0.119, y1:0.426, 
                        x2:0.712045, y2:0.926, stop:0.0451977 rgba(255, 84, 87, 255), 
                        stop:0.59887 rgba(255, 161, 71, 255));
                    }'''





class TablesAndListsObjName(StrEnum):
    '''Clase StrEnum con los "object names" de las tablas y lista usadas en el 
    programa. La principal razón del uso de esta clase es para usarse dentro 
    de EventFilters y darle estilos a las tablas y listas.'''
    INVEN_TABLE_VIEW = "tv_inventory_data"
    SALES_TABLE_VIEW = "tv_sales_data"
    SALES_INPUT_LIST = "sales_input_list"
    DEBTS_TABLE_VIEW = "tv_debts_data"
    BAL_PRODS_TABLE_VIEW = "tv_balance_products"





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
    CONTRAST_GREEN = QColor(13, 180, 13, 255)
    CONTRAST_WHITE = QColor(238, 238, 238, 255)





class TableBgColors(Enum):
    '''Enum con QColors para columnas de QTableViews. Contiene sus versiones normales 
    y las variantes de color para filas alternantes.'''
    LOW_STOCK_ROW = QColor(245, 165, 165, 255)
    UNIT_PRICE_ROW = QColor(253, 214, 118, 200)
    COMERC_PRICE_ROW = QColor(251, 189, 173, 200)
    
    SALES_LOWER_PAID = QColor(226, 180, 177, 255)
    
    DEBTS_POSITIVE_BALANCE = QColor(226, 180, 177, 255)
    DEBTS_NEGATIVE_BALANCE = QColor(180, 226, 177, 255)
    DEBTS_CERO_BALANCE = QColor(230, 230, 230, 255)
    DEBTS_CONTACT = QColor(170, 170, 210, 255)





class ModelHeaders(Enum):
    '''Enum con tuples[headers] para las QTableViews que usan los MODELOS DE DATOS.'''
    INVENTORY_HEADERS = ("Categoría", "Nombre del producto", "Descripción", 
                         "Stock", "Precio normal", "Precio comercial")
    
    SALES_HEADERS = ("Detalle de venta", "Cantidad", "Producto", "Costo total", 
                     "Abonado", "Fecha y hora")
    
    DEBTS_HEADERS = ("Nombre", "Apellido", "Teléfono", "Dirección", "Código postal", "Balance")
    
    PRODS_BAL_HEADERS = ("Fecha y hora", "Descripción", "Saldo")





class DBQueries(IntEnum):
    '''IntEnum con las operaciones CRUD a base de datos.'''
    SELECT_COUNT = 0
    SELECT_REGISTERS = 1
    DELETE_REGISTERS = 2
    UPDATE_REGISTERS = 3
    INSERT_REGISTERS = 4





class CommonCategories(StrEnum):
    '''
    StrEnum con categorías comunes. Estas categorías no se pueden eliminar de 
    la base de datos o sirven para mostrar todos los productos de todas las 
    categorías al mismo tiempo.
    '''
    SHOW_ALL = "MOSTRAR TODOS"
    MISC = "Varios"





# estilos generales para widgets
class WidgetStyle(StrEnum):
    '''Clase de tipo 'strEnum' con estilos generales para aplicar a los widgets.'''
    LABEL_NEUTRAL_VAL = "color: #555; background-color: rgba(200,200,200,0.7);"
    FIELD_VALID_VAL = "color: #fff; background-color: #9DD367;"
    FIELD_INVALID_VAL = "color: #fff; background-color: #F65755;"
    
    DIALOG_CANCEL_BTN_STYLE ='''QDialogButtonBox QPushButton[text='Cancelar'] {
                                    background-color: #fff;
                                    color: #111;
                                    border: 1px solid #aaa;
                                }
                                QDialogButtonBox QPushButton[text='Cancelar']:hover,
                                QDialogButtonBox QPushButton[text='Cancelar']:pressed,
                                QDialogButtonBox QPushButton[text='Cancelar']:focus {
                                    background-color: #ccc;
                                }'''
    
    LABEL_RICHTEXT_NEUTRAL = "font-size:20px; color: #fff;"
    LABEL_RICHTEXT_CONTENT = "font-size:20px; color: #415a77;"
    
    DEF_COMBOBOX_FILTER_ICON = "QComboBox::down-arrow {image: url(':/icons/filter.svg');}"
    DEF_COMBOBOX_ARROW_ICON = "QComboBox::down-arrow {image: url(':/icons/chevron-down.svg');}"
    
    DEF_DATEEDIT_ARROW_ICON = "QDateEdit::down-arrow {image: url(':/icons/chevron-down.svg');}"
    DEF_DATETIMEEDIT_ARROW_ICON = "QDateTimeEdit::down-arrow {image: url(':/icons/chevron-down.svg');}"





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





# tipos de campos a validar para el dialog de Productos
class ProductFields(IntEnum):
    '''Clase de tipo 'IntEnum' con los campos de los cuales se guarda registro 
    cuando se debe ingresar Ventas.'''
    PRODUCT_ID = 0
    NAME = 1
    CATEGORY = 2
    DESCRIPTION = 3
    STOCK_QUANTITY = 4
    STOCK_UNIT = 5
    NORMAL_PRICE = 6
    COMERCIAL_PRICE = 7





# tipos de campos a validar para el formulario de Ventas
class SaleFields(IntEnum):
    '''Clase de tipo 'IntEnum' con los campos de los cuales se guarda registro 
    cuando se debe ingresar Ventas.'''
    PRODUCT_ID = 0
    PRODUCT_NAME = 1
    QUANTITY = 2
    SUBTOTAL = 3
    IS_COMERCIAL_PRICE = 4
    SALE_DETAILS = 5
    DATETIME = 6
    IS_ALL_VALID = 7
    TOTAL_COST = 8
    TOTAL_PAID = 9
    DEBTOR_NAME = 10
    DEBTOR_SURNAME = 11




# alturas predefinidas para QDialog de ventas
class SaleDialogDimensions(IntEnum):
    '''
    IntEnum con los valores de dimensiones que toma el dialog de ventas.
    '''
    WIDTH = 555
    HEIGHT_NO_DEBT = 325
    HEIGHT_WITH_DEBT = 422
    




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
class InvViewCols(IntEnum):
    '''Clase de tipo 'IntEnum' con los nombres predeterminados de las columnas 
    de las VISTAS.'''
    INV_CATEGORY = 0
    INV_PRODUCT_NAME = 1
    INV_DESCRIPTION = 2
    INV_STOCK = 3
    INV_NORMAL_PRICE = 4
    INV_COMERCIAL_PRICE = 5





class SalesViewCols(IntEnum):
    SALES_DETAIL = 0
    SALES_QUANTITY = 1
    SALES_PRODUCT_NAME = 2
    SALES_TOTAL_COST = 3
    SALES_TOTAL_PAID = 4
    SALES_DATETIME = 5





class DebtorViewCols(IntEnum):
    DEBTS_NAME = 0
    DEBTS_SURNAME = 1
    DEBTS_PHONE_NUMBER = 2
    DEBTS_DIRECTION = 3
    DEBTS_POSTAL_CODE = 4
    DEBTS_BALANCE = 5





class DebtsViewCols(IntEnum):
    PRODS_BAL_DATETIME = 0
    PRODS_BAL_DESCRIPTION = 1
    PRODS_BAL_BALANCE = 2





# columnas en los modelos de las tablas
class InvModelCols(IntEnum):
    '''Clase de tipo **IntEnum** con las columnas que maneja el modelo de 
    datos de Inventario internamente en su atributo *_data*, ya que los datos 
    internos del *MODELO DE DATOS* son diferentes a los datos que muestra la 
    *VISTA*.'''
    INV_IDPRODUCT = 0
    INV_CATEGORY_NAME = 1
    INV_NAME = 2
    INV_DESCRIPTION = 3
    INV_STOCK = 4
    INV_MEASUREMENT_UNIT = 5
    INV_NORMAL_PRICE = 6
    INV_COMERCIAL_PRICE = 7





class SalesModelCols(IntEnum):
    '''Clase de tipo **IntEnum** con las columnas que maneja el modelo de 
    datos de Ventas internamente en su atributo *_data*, ya que los datos 
    internos del *MODELO DE DATOS* son diferentes a los datos que muestra la 
    *VISTA*.'''
    SALES_ID_SALES_DETAIL = 0
    SALES_DETAIL = 1
    SALES_QUANTITY = 2
    SALES_MEASUREMENT_UNIT = 3
    SALES_PRODUCT_NAME = 4
    SALES_TOTAL_COST = 5
    SALES_TOTAL_PAID = 6
    SALES_DATETIME = 7





class DebtorFullName(IntEnum):
    '''Clase de tipo **IntEnum** con las columnas dentro de los modelos que 
    referencien al nombre completo de un deudor internamente, ya que los datos 
    internos del *MODELO DE DATOS* son diferentes a los datos que muestra la 
    *VISTA*.'''
    DEBTOR_NAME_SURNAME_MODEL_NAME = 0
    DEBTOR_NAME_SURNAME_MODEL_SURNAME = 1





class DebtorModelCols(IntEnum):
    '''Clase de tipo **IntEnum** con las columnas que maneja el modelo de 
    datos de Cuentas Corrientes internamente en su atributo *_data*, ya que 
    los datos internos del *MODELO DE DATOS* son diferentes a los datos que 
    muestra la *VISTA*.'''
    DEBTS_IDDEBTOR = 0
    DEBTS_NAME = 1
    DEBTS_SURNAME = 2
    DEBTS_PHONE_NUMBER = 3
    DEBTS_DIRECTION = 4
    DEBTS_POSTAL_CODE = 5
    DEBTS_TOTAL_BALANCE = 6





class DebtsModelCols(IntEnum):
    '''Clase de tipo **IntEnum** con las columnas que maneja el modelo de 
    datos de balance de productos (deudas) internamente en su atributo 
    *_data*, ya que los datos internos del *MODELO DE DATOS* son diferentes a 
    los datos que muestra la *VISTA*.'''
    PRODS_BAL_ID_SALES_DETAIL = 0
    PRODS_BAL_DATETIME = 1
    PRODS_BAL_DESCRIPTION = 2
    PRODS_BAL_BALANCE = 3





# expresiones regulares para validadores o búsqueda
class Regex(StrEnum):
    '''
    Clase StrEnum con expresiones regulares predefinidas, creadas principalmente para 
    usarse en 'utils.customvalidators.py', pero no exclusivamente.
    '''
    GENERIC_CHARS_TO_AVOID = "[^;\"']*"
    
    ISO_8601_FORMAT = "\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}"
    
    PROD_NAME = "[^;\"']{1,50}"
    PROD_STOCK_QUANTITY = "\d{1,8}(\.|,)?\d{0,2}"
    PROD_STOCK_FULL = "(\d{1,8}(\.|,)?\d{0,2} {1}[a-zA-Z]{0,20})|(\d{1,8}(\.|,)?\d{0,2})"
    PROD_UNIT_PRICE = "\d{1,8}((\.|,){1}\d{0,2})?"
    PROD_COMERC_PRICE = "\d{0,8}((\.|,)\d{0,2})?"
    PERCENTAGE_CHANGE = "^([-+]?\d{0,4}((\.|,)\d{0,2})?)|(\d{1,8}((\.|,)\d{0,2})?)$"
    
    CATEGORY_NAME = "[^;\"']{1,41}"
    CATEGORY_DESC = "[^\"'\{\}\[\]]{0,256}"
    
    SALES_DETAILS_PRICE_TYPE = "(\([\s]*P[\s]*\.[\s]*PÚBLICO[\s]*\)|\([\s]*P[\s]*\.[\s]*COMERCIAL[\s]*\))$"
    SALES_DETAILS_FULL = "[0-9]{1,8}(\.|,)?[0-9]{0,2}\sde .{1,}\s(\([\s]*P[\s]*\.[\s]*PÚBLICO[\s]*\)|\([\s]*P[\s]*\.[\s]*COMERCIAL[\s]*\))$"
    SALES_DETAILS_EDITION = "[^;\"']{0,256}"
    SALES_QUANTITY = "[0-9]{1,8}(\.|,)?[0-9]{0,2}"
    SALES_TOTAL_COST = "[0-9]{1,8}(\.|,)?[0-9]{0,2}"
    SALES_PAID = "[\d]{0,8}(\.|,)?[\d]{0,2}"
    
    DEBTS_NAME = "[^;\"'\[\]]{1,40}"
    DEBTS_SURNAME = "[^;\"'\[\]]{1,40}"
    DEBTS_PHONE_NUMB = "\+?[0-9 -]{0,20}"
    DEBTS_DIRECTION = "[^;\"']{0,256}"
    
    PRODS_BAL_BALANCE = "[+-]?[\d]{0,8}(\.|,)?[\d]{0,2}"