'''
En este archivo se encuentran los QValidators -y sus variantes- que he tenido que modificar 
para poder lograr una mejor validación de datos en QComboBoxes, QLineEdits, QDateTimeEdits y 
demás widgets donde el usuario pueda ingresar datos.
'''
from PySide6.QtCore import (Signal, QLocale)
from PySide6.QtGui import (QValidator, QRegularExpressionValidator, QIntValidator, QDoubleValidator)

from utils.dboperations import *

from re import (fullmatch, compile, Pattern, IGNORECASE)


#¡ search bars ========================================================================================
class SearchBarValidator(QValidator):
    '''Validador para las barras de búsquedas. A diferencia de otros validadores, este no emite señales.'''
    def __init__(self, parent=None):
        super(SearchBarValidator, self).__init__()
        self.pattern:Pattern = compile("[^;\"']*", flags=IGNORECASE)
    
    
    def validate(self, text: str, pos: int) -> object:
        if text.strip() == "": # si el campo está vacío devuelve Acceptable
            return self.State.Acceptable, text, pos
        
        elif fullmatch(self.pattern, text): # si coincide el patrón devuelve Acceptable
            return self.State.Acceptable, text, pos
        
        else: # en cualquier otro caso devuelve Invalid
            return self.State.Invalid, text, pos



#¡ tabla INVENTARIO ===================================================================================
class ProductNameValidator(QValidator):
    '''Validador para los campos donde el usuario pueda modificar el nombre de un producto.'''
    validationSucceded = Signal() # se emite cuando el estado es 'Acceptable'. Sirve para esconder el label con feedback
    validationFailed = Signal(str) # se emite cuando el estado es 'Invalid', envía un str con feedback para mostrar
    
    def __init__(self, parent=None):
        super(ProductNameValidator, self).__init__()
        self.pattern:Pattern = compile("[^;\"']{1,50}", flags=IGNORECASE)
    
    
    def validate(self, text: str, pos: int) -> object:
        # lista para verificar si el nombre existe en la base de datos
        names:list = [name[0] for name in makeReadQuery("SELECT nombre FROM Productos WHERE nombre = ?;", (text,))]
        
        if text in names: # si el nombre ya existe devuelve Intermediate
            self.validationFailed.emit("El nombre del producto ya existe")
            return QValidator.State.Intermediate, text, pos
        
        elif text.strip() == "": # si el campo está vacío devuelve Intermediate
            self.validationFailed.emit("El campo del nombre del producto no puede estar vacío")
            return QValidator.State.Intermediate, text, pos
        
        elif fullmatch(self.pattern, text): # si coincide el patrón devuelve Acceptable
            self.validationSucceded.emit()
            return QValidator.State.Acceptable, text, pos
        
        else: # en cualquier otro caso devuelve Invalid
            self.validationFailed.emit("El nombre del producto es inválido")
            return QValidator.State.Invalid, text, pos





class ProductStockValidator(QRegularExpressionValidator):
    '''Validador para los campos donde el usuario pueda modificar el stock y la unidad de medida de un producto.'''
    validationSucceded = Signal()
    validationFailed = Signal(str)
    
    def __init__(self, parent=None):
        super(ProductStockValidator, self).__init__()
        self.pattern:Pattern = compile("[0-9]{1,8}(\.|,)?[0-9]{0,2} ?[a-zA-Z]{0,20}", IGNORECASE)
    
    
    def fixup(self, text: str) -> str:        
        while text.split(" ")[0].endswith((".", ",")):
            text = text.rstrip(",")
            text = text.rstrip(".")
        return super().fixup(text)
    
    
    def validate(self, text: str, pos: int) -> object:
        
        if text.strip() == "":
            self.validationFailed.emit("El campo de stock no puede estar vacío")
            return QRegularExpressionValidator.State.Intermediate, text, pos
        
        elif fullmatch(self.pattern, text):
            self.validationSucceded.emit()
            return QRegularExpressionValidator.State.Acceptable, text, pos
        
        elif text.split(" ")[0].endswith((".", ",")): # llama automáticamente a fixup()
            return QRegularExpressionValidator.State.Invalid, text, pos
        
        else:
            self.validationFailed.emit("El stock del producto es inválido")
            return QRegularExpressionValidator.State.Invalid, text, pos





class ProductUnitPriceValidator(QRegularExpressionValidator):
    '''Validador para los campos donde el usuario pueda modificar el precio unitario de un producto.'''
    validationSucceded = Signal()
    validationFailed = Signal(str)
    
    def __init__(self, parent=None):
        super(ProductUnitPriceValidator, self).__init__()
        self.pattern:Pattern = compile("[0-9]{1,8}(\.|,)?[0-9]{0,2}")
    
    
    def fixup(self, text: str) -> str:
        while text.endswith((".", ",")):
            text = text.rstrip(",")
            text = text.rstrip(".")
        return super().fixup(text)
    
    
    def validate(self, text: str, pos: int) -> object:
        
        if text == "":
            self.validationFailed.emit("El campo de precio unitario no puede estar vacío")
            return QRegularExpressionValidator.State.Intermediate, text, pos
        
        elif fullmatch(self.pattern, text):
            self.validationSucceded.emit()
            return QRegularExpressionValidator.State.Acceptable, text, pos
        
        elif text.endswith((",",".")): # llama automáticamente a fixup()
            return QRegularExpressionValidator.State.Invalid, text, pos
        
        else:
            self.validationFailed.emit("El precio unitario es inválido")
            return QRegularExpressionValidator.State.Invalid, text, pos





class ProductComercPriceValidator(QRegularExpressionValidator):
    '''Validador para los campos donde el usuario pueda modificar el precio comercial de un producto.'''
    validationSucceded = Signal()
    validationFailed = Signal(str)
    
    def __init__(self, parent=None):
        super(ProductComercPriceValidator, self).__init__()
        self.pattern:Pattern = compile("[0-9]{1,8}(\.|,)?[0-9]{0,2}")
    
    
    def fixup(self, text: str) -> str:
        while text.endswith((".", ",")):
            text = text.rstrip(",")
            text = text.rstrip(".")
        return super().fixup(text)
    
    
    def validate(self, text: str, pos: int) -> object:
        
        if text.strip() == "":
            self.validationSucceded.emit()
            return QRegularExpressionValidator.State.Acceptable, text, pos
        
        elif fullmatch(self.pattern, text):
            self.validationSucceded.emit()
            return QRegularExpressionValidator.State.Acceptable, text, pos
        
        elif text.endswith((",",".")): # llama automáticamente a fixup()
            return QRegularExpressionValidator.State.Invalid, text, pos
        
        else:
            self.validationFailed.emit("El precio unitario es inválido")
            return QRegularExpressionValidator.State.Invalid, text, pos





#¡ tabla VENTAS ===================================================================================
class SaleDetailsValidator(QRegularExpressionValidator):
    '''Validador para los campos donde el usuario pueda modificar los detalles de una venta.'''
    validationSucceded = Signal()
    validationFailed = Signal(str)
    
    def __init__(self, parent=None):
        super(SaleDetailsValidator, self).__init__()
        self.pattern:Pattern = compile("[^;\"']{0,256}")
    
    
    def validate(self, text: str, pos: int) -> object:
        
        if text.strip() == "" or fullmatch(self.pattern, text):
            self.validationSucceded.emit()
            return QRegularExpressionValidator.State.Acceptable, text, pos
        
        else:
            self.validationFailed.emit("El campo de detalle de venta no admite ese caracter")
            return QRegularExpressionValidator.State.Invalid, text, pos





class SaleQuantityValidator(QRegularExpressionValidator):
    '''Validador para los campos donde el usuario pueda modificar la cantidad de un producto.'''
    validationSucceded = Signal()
    validationFailed = Signal(str)
    
    def __init__(self, parent=None):
        super(SaleQuantityValidator, self).__init__()
        self.AVAILABLE_STOCK:tuple[float,str] = None
        self.pattern:Pattern = compile("[0-9]{1,8}(\.|,)?[0-9]{0,2}")
    
    
    def setAvailableStock(self, stock:tuple[float,str]) -> None:
        '''
        Coloca el valor de 'stock' en 'self.AVAILABLE_STOCK'.
        
        'stock[0]' representa la cantidad como float en stock del producto, y 'stock[1]' representa la unidad de 
        medida como str.
        
        Retorna None.
        '''
        self.AVAILABLE_STOCK = stock
        return None
    
    
    def fixup(self, text: str) -> str:
        while text.split(" ")[0].endswith((".", ",")):
            text = text.rstrip(",")
            text = text.rstrip(".")
        return super().fixup(text)
    
    
    def validate(self, text: str, pos: int) -> object:
        
        if text.strip() == "":
            self.validationFailed.emit("La cantidad no puede estar vacía")
            return QRegularExpressionValidator.State.Intermediate, text, pos
        
        elif fullmatch(self.pattern, text):
            try:
                # si el stock disponible existe y es menor que la cantidad introducida devuelve Invalid
                if self.AVAILABLE_STOCK and float(text.replace(",",".")) > self.AVAILABLE_STOCK[0]:
                    self.validationFailed.emit(f"Cantidad mayor al stock (stock: {self.AVAILABLE_STOCK[0]} {self.AVAILABLE_STOCK[1]})")
                    return QRegularExpressionValidator.State.Invalid, text, pos
                    
            except TypeError as err:
                logging.error(err)
            
            self.validationSucceded.emit()
            return QRegularExpressionValidator.State.Acceptable, text, pos
        
        elif text.split(" ")[0].endswith((".", ",")): # si pasa, automáticamente llama a 'fixup' y lo corrige, y el programa sigue como si nada...
            return QRegularExpressionValidator.State.Invalid, text, pos
        
        else:
            self.validationFailed.emit("La cantidad es inválida")
            return QRegularExpressionValidator.State.Invalid, text, pos





class SaleTotalCostValidator(QRegularExpressionValidator):
    '''Validador para los campos donde el usuario pueda modificar el costo total de un producto.'''
    validationSucceded = Signal()
    validationFailed = Signal(str)
    
    
    def __init__(self, parent=None):
        super(SaleTotalCostValidator, self).__init__()
        self.pattern:Pattern = compile("[0-9]{1,8}(\.|,)?[0-9]{0,2}")
    
    def fixup(self, text: str) -> str:
        while text.endswith((".", ",")):
            text = text.rstrip(",")
            text = text.rstrip(".")
        return super().fixup(text)
    
    
    def validate(self, text: str, pos: int) -> object:
        if text.strip() == "":
            self.validationFailed.emit("El campo de costo total no puede estar vacío")
            return QRegularExpressionValidator.State.Intermediate, text, pos
        
        elif fullmatch(self.pattern, text):
            self.validationSucceded.emit()
            return QRegularExpressionValidator.State.Acceptable, text, pos
        
        elif text.endswith((".", ",")): # si pasa, automáticamente llama a 'fixup' y lo corrige, y el programa sigue como si nada...
            return QRegularExpressionValidator.State.Invalid, text, pos
        
        else:
            self.validationFailed.emit("El costo total es inválido")
            return QRegularExpressionValidator.State.Invalid, text, pos





class SalePaidValidator(QValidator):
    '''Validador para los campos donde el usuario pueda modificar la cantidad paga de un producto.'''
    validationSucceded = Signal()
    validationFailed = Signal(str)
    
    def __init__(self, parent=None, is_optional:bool=False):
        super(SalePaidValidator, self).__init__()
        self.is_optional = is_optional
        self.pattern:Pattern = compile("[\d]{0,8}(\.|,)?[\d]{0,2}")
    
    
    def validate(self, text: str, pos: int) -> object:
        
        if self.is_optional and text == "": # si el campo es opcional y está vacío emite Acceptable
            self.validationSucceded.emit()
            return QValidator.State.Acceptable, text, pos
        
        elif not self.is_optional and text == "": # si el campo es obligatorio y está vacío emite Itermediate
            self.validationFailed.emit("El campo del total abonado no puede estar vacío")
            return QValidator.State.Intermediate, text, pos
        
        elif fullmatch(self.pattern, text):
            self.validationSucceded.emit()
            return QIntValidator.State.Acceptable, text, pos

        else:
            self.validationFailed.emit("El valor abonado es inválido")
            return QValidator.State.Invalid, text, pos





#¡ tabla VENTAS/CUENTA CORRIENTE ===================================================================================
class DebtorNameValidator(QRegularExpressionValidator):
    '''Validador para los campos donde el usuario pueda modificar el nombre de una persona en cuenta corriente.'''
    validationSucceded = Signal()
    validationFailed = Signal(str)
    
    def __init__(self, parent=None):
        super(DebtorNameValidator, self).__init__()
        self.pattern:Pattern = compile("[^;\"']{1,40}")

    def validate(self, text: str, pos: int) -> object:
    
        if text.strip() == "":
            self.validationFailed.emit("El campo del nombre no puede estar vacío")
            return QRegularExpressionValidator.State.Intermediate, text, pos
        
        elif fullmatch(self.pattern, text):
            self.validationSucceded.emit()
            return QRegularExpressionValidator.State.Acceptable, text, pos
        
        else:
            self.validationFailed.emit("El nombre es inválido")
            return QRegularExpressionValidator.State.Invalid, text, pos





class DebtorSurnameValidator(QRegularExpressionValidator):
    '''Validador para los campos donde el usuario pueda modificar el apellido de una persona en cuenta corriente.'''
    validationSucceded = Signal()
    validationFailed = Signal(str)
    
    def __init__(self, parent=None):
        super(DebtorSurnameValidator, self).__init__()
        self.pattern:Pattern = compile("[^;\"']{1,40}")
    
    def validate(self, text: str, pos: int) -> object:
        
        if text.strip() == "":
            self.validationFailed.emit("El campo del apellido no puede estar vacío")
            return QRegularExpressionValidator.State.Intermediate, text, pos
        
        elif fullmatch(self.pattern, text):
            self.validationSucceded.emit()
            return QRegularExpressionValidator.State.Acceptable, text, pos
        
        else:
            self.validationFailed.emit("El apellido es inválido")
            return QRegularExpressionValidator.State.Invalid, text, pos





class DebtorPhoneNumberValidator(QRegularExpressionValidator):
    '''Validador para los campos donde el usuario pueda modificar el número de teléfono de una persona en cuenta corriente.'''
    validationSucceded = Signal()
    validationFailed = Signal(str)

    def __init__(self, parent=None):
        super(DebtorPhoneNumberValidator, self).__init__()
        self.pattern:Pattern = compile("\+?[0-9 -]{0,20}")
        
    def validate(self, text: str, pos: int) -> object:
        
        if text.strip() == "": # si el texto está vacío devuelve Acceptable
            self.validationSucceded.emit()
            return QRegularExpressionValidator.State.Acceptable, text, pos
        
        elif fullmatch(self.pattern, text):
            self.validationSucceded.emit()
            return QRegularExpressionValidator.State.Acceptable, text, pos
        
        else:
            self.validationFailed.emit("El número de teléfono es inválido")
            return QRegularExpressionValidator.State.Invalid, text, pos





class DebtorPostalCodeValidator(QIntValidator):
    validationSucceded = Signal()
    validationFailed = Signal(str)

    def __init__(self, parent=None):
        super(DebtorPostalCodeValidator, self).__init__()
        self.setRange(1, 9_999)
        self.setLocale(QLocale(QLocale.Language.Spanish, QLocale.Country.Argentina))

    
    def validate(self, text: str, pos: int) -> object:
        
        if text.strip() == "": # si el texto está vacío devuelve Acceptable
            self.validationSucceded.emit()
            return QIntValidator.State.Acceptable, text, pos
        
        elif text.isnumeric() and (self.bottom() <= int(text) <= self.top()):
            self.validationSucceded.emit()
            return QIntValidator.State.Acceptable, text, pos
        
        elif text.isalnum():
            self.validationFailed.emit("El código postal sólo admite números entre [1, 9.999]")
            return QIntValidator.State.Invalid, text, pos
        
        else:
            self.validationFailed.emit("El código postal es inválido")
            return QIntValidator.State.Invalid, text, pos














