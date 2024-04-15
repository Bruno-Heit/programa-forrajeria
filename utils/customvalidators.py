'''
En este archivo se encuentran los QValidators -y sus variantes- que he tenido que modificar 
para poder lograr una mejor validación de datos en QComboBoxes, QLineEdits y demás widgets 
donde el usuario pueda ingresar datos.
'''
# from PySide6.QtWidgets import (QTableWidget, QComboBox, QHeaderView, QTableWidgetItem, QListWidget,
                            #    QLineEdit, QLabel, QCompleter, QFrame, QWidget, QDateTimeEdit)
from PySide6.QtCore import (Signal)
from PySide6.QtGui import (QValidator)

from utils.dboperations import *


class ProductNameValidator(QValidator):
    validationFailed = Signal(str) # se emite cuando el estado es 'Invalid', envía un str con feedback para mostrar
    
    def validate(self, text: str, pos: int) -> object:
        # si el texto está vacío...
        if text.strip() == "":
            self.validationFailed.emit("El campo del nombre del producto no puede estar vacío")
            return QValidator.State.Invalid, text, pos
        
        # si el nombre ya existe en la base de datos..
        elif text in makeReadQuery("SELECT nombre FROM Productos WHERE nombre = ?", (text,)):
            self.validationFailed.emit("Ya existe un producto con ese nombre")
            return QValidator.State.Invalid, text, pos
        
        else:
            return QValidator.State.Acceptable, text, pos