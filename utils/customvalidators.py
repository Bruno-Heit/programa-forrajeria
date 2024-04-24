'''
En este archivo se encuentran los QValidators -y sus variantes- que he tenido que modificar 
para poder lograr una mejor validación de datos en QComboBoxes, QLineEdits, QDateTimeEdits y 
demás widgets donde el usuario pueda ingresar datos.
'''
from PySide6.QtCore import (Signal)
from PySide6.QtGui import (QValidator, QRegularExpressionValidator)

from utils.dboperations import *

from re import (fullmatch, compile, Pattern, IGNORECASE)


#¡ tabla INVENTARIO ===================================================================================
class ProductNameValidator(QValidator):
    '''Validador para los campos donde el usuario pueda modificar el nombre de un producto.'''
    validationSucceded = Signal() # se emite cuando el estado es 'Acceptable'. Sirve para esconder el label con feedback
    validationFailed = Signal(str) # se emite cuando el estado es 'Invalid', envía un str con feedback para mostrar
    
    
    def validate(self, text: str, pos: int) -> object:
        # patrón de input permitido
        pattern:Pattern = compile("[^;\"']{1,50}", flags=IGNORECASE)
        # lista para verificar si el nombre existe en la base de datos
        names:list = [name[0] for name in makeReadQuery("SELECT nombre FROM Productos WHERE nombre = ?;", (text,))]
        
        if text in names: # si el nombre ya existe devuelve Intermediate
            self.validationFailed.emit("El nombre del producto ya existe")
            return QValidator.State.Intermediate, text, pos
        
        elif text.strip() == "": # si el campo está vacío devuelve Intermediate
            self.validationFailed.emit("El campo del nombre del producto no puede estar vacío")
            return QValidator.State.Intermediate, text, pos
        
        elif fullmatch(pattern, text): # si coincide el patrón devuelve Acceptable
            self.validationSucceded.emit()
            return QValidator.State.Acceptable, text, pos
        
        else: # en cualquier otro caso devuelve Invalid
            self.validationFailed.emit("El nombre del producto es inválido")
            return QValidator.State.Invalid, text, pos





class ProductStockValidator(QRegularExpressionValidator):
    '''Validador para los campos donde el usuario pueda modificar el stock y la unidad de medida de un producto.'''
    validationSucceded = Signal()
    validationFailed = Signal(str)
    
    
    def fixup(self, text: str) -> str:        
        while text.split(" ")[0].endswith((".", ",")):
            text = text.rstrip(",")
            text = text.rstrip(".")
        return super().fixup(text)
    
    
    def validate(self, text: str, pos: int) -> object:
        pattern:Pattern = compile("[0-9]{1,8}(\.|,)?[0-9]{0,2} ?[a-zA-Z]{0,20}", IGNORECASE)
        
        if text.strip() == "":
            self.validationFailed.emit("El campo de stock no puede estar vacío")
            return QRegularExpressionValidator.State.Intermediate, text, pos
        
        elif fullmatch(pattern, text):
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
    
    
    def fixup(self, text: str) -> str:
        while text.endswith((".", ",")):
            text = text.rstrip(",")
            text = text.rstrip(".")
        return super().fixup(text)
    
    
    def validate(self, text: str, pos: int) -> object:
        pattern:Pattern = compile("[0-9]{1,8}(\.|,)?[0-9]{0,2}")
        
        if text.strip() == "":
            self.validationFailed.emit("El campo de precio unitario no puede estar vacío")
            return QRegularExpressionValidator.State.Intermediate, text, pos
        
        elif fullmatch(pattern, text):
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
    
    
    def fixup(self, text: str) -> str:
        while text.endswith((".", ",")):
            text = text.rstrip(",")
            text = text.rstrip(".")
        return super().fixup(text)
    
    
    def validate(self, text: str, pos: int) -> object:
        pattern:Pattern = compile("[0-9]{1,8}(\.|,)?[0-9]{0,2}")
        
        if text.strip() == "":
            self.validationSucceded.emit()
            return QRegularExpressionValidator.State.Acceptable, text, pos
        
        elif fullmatch(pattern, text):
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
    
    
    def validate(self, text: str, pos: int) -> object:
        pattern:Pattern = compile("[^;\"']{0,255}")
        
        if text.strip() == "" or fullmatch(pattern, text):
            self.validationSucceded.emit()
            return QRegularExpressionValidator.State.Acceptable, text, pos
        
        else:
            self.validationFailed.emit("El campo de detalle de venta no admite ese caracter")
            return QRegularExpressionValidator.State.Invalid, text, pos





class SaleQuantityValidator(QRegularExpressionValidator):
    '''Validador para los campos donde el usuario pueda modificar la cantidad de un producto.'''
    validationSucceded = Signal()
    validationFailed = Signal(str)
    
    
    def fixup(self, text: str) -> str:
        while text.split(" ")[0].endswith((".", ",")):
            text = text.rstrip(",")
            text = text.rstrip(".")
        return super().fixup(text)
    
    
    def validate(self, text: str, pos: int) -> object:
        pattern:Pattern = compile("[0-9]{1,8}(\.|,)?[0-9]{0,2}")
        
        if text.strip() == "":
            self.validationFailed.emit("El campo de cantidad no puede estar vacío")
            return QRegularExpressionValidator.State.Intermediate, text, pos
        
        elif fullmatch(pattern, text):
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
    
    
    def fixup(self, text: str) -> str:
        while text.endswith((".", ",")):
            text = text.rstrip(",")
            text = text.rstrip(".")
        return super().fixup(text)
    
    
    def validate(self, text: str, pos: int) -> object:
        pattern:Pattern = compile("[0-9]{1,8}(\.|,)?[0-9]{0,2}")
        
        if text.strip() == "":
            self.validationFailed.emit("El campo de costo total no puede estar vacío")
            return QRegularExpressionValidator.State.Intermediate, text, pos
        
        elif fullmatch(pattern, text):
            self.validationSucceded.emit()
            return QRegularExpressionValidator.State.Acceptable, text, pos
        
        elif text.endswith((".", ",")): # si pasa, automáticamente llama a 'fixup' y lo corrige, y el programa sigue como si nada...
            return QRegularExpressionValidator.State.Invalid, text, pos
        
        else:
            self.validationFailed.emit("El costo total es inválido")
            return QRegularExpressionValidator.State.Invalid, text, pos





class SalePaidValidator(QRegularExpressionValidator):
    '''Validador para los campos donde el usuario pueda modificar el costo total de un producto.'''
    validationSucceded = Signal()
    validationFailed = Signal(str)
    
    
    def fixup(self, text: str) -> str:
        while text.endswith((".", ",")):
            text = text.rstrip(",")
            text = text.rstrip(".")
        return super().fixup(text)
    
    
    def validate(self, text: str, pos: int) -> object:
        pattern:Pattern = compile("[0-9]{1,8}(\.|,)?[0-9]{0,2}")
        
        
        if text.strip() == "":
            self.validationFailed.emit("El campo del total abonado no puede estar vacío")
            return QRegularExpressionValidator.State.Intermediate, text, pos
        
        elif fullmatch(pattern, text):
            self.validationSucceded.emit()
            return QRegularExpressionValidator.State.Acceptable, text, pos
        
        elif text.endswith((".", ",")): # si pasa, automáticamente llama a 'fixup' y lo corrige, y el programa sigue como si nada...
            return QRegularExpressionValidator.State.Invalid, text, pos
        
        else:
            self.validationFailed.emit("El valor abonado es inválido")
            return QRegularExpressionValidator.State.Invalid, text, pos























