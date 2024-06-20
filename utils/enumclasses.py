'''
En este archivo están las classes que heredan de Enum, y sirve más que nada para 
simplificar la lectura de algunos valores recurrentes.

'''

from enum import (Enum, StrEnum, IntEnum)


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
