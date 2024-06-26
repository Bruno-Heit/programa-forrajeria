'''
    En este archivo se encuentran las clases DELEGADOS 
    que se usan para personalizar y editar las VISTAS
'''
from PySide6.QtWidgets import (QWidget, QStyledItemDelegate, QStyleOptionViewItem, 
                               QComboBox, QLineEdit)
from PySide6.QtGui import (QPainter, QColor, QPen)
from PySide6.QtCore import (Qt, QModelIndex, QSize, QPersistentModelIndex, 
                            QAbstractItemModel)

from utils.enumclasses import (TableBgColors, TableFontColor)
from utils.functionutils import (getProductsCategories, createCompleter)
from utils.customvalidators import (ProductNameValidator, ProductStockValidator, 
                                    ProductUnitPriceValidator, ProductComercPriceValidator)


class InventoryDelegate(QStyledItemDelegate):
    '''Clase DELEGADO que se encarga de personalizar/editar celdas del QTableView de inventario.'''
    
    def createEditor(self, parent: QWidget, option: QStyleOptionViewItem, 
                     index: QModelIndex | QPersistentModelIndex) -> QWidget:
        editor:QWidget
        
        # TODO: colocar señales para cuando el input sea válido o inválido
        match index.column():
            case 0: # categoría
                editor = QComboBox(parent)
                editor.setEditable(False)
                editor.setFrame(False)
                editor.addItems(getProductsCategories())
                editor.setPlaceholderText("Seleccionar una categoría")
            
            case 1: # nombre
                editor = QLineEdit(parent)
                editor.setCompleter(createCompleter(type=3))
                editor.setMaxLength(50)
                editor.setValidator(ProductNameValidator(editor))
            
            case 2: # descripción
                editor = QLineEdit(parent)
                editor.setMaxLength(200)
            
            case 3: # stock
                editor = QLineEdit(parent)
                editor.setMaxLength(31)
                editor.setValidator(ProductStockValidator(editor))
                
            case 4: # precio unitario
                editor = QLineEdit(parent)
                editor.setMaxLength(10)
                editor.setValidator(ProductUnitPriceValidator(editor))
            
            case 5: # precio comercial
                editor = QLineEdit(parent)
                editor.setMaxLength(10)
                editor.setValidator(ProductComercPriceValidator(editor))
        return editor
    
    
    def setEditorData(self, editor: QComboBox | QLineEdit, index: QModelIndex | QPersistentModelIndex) -> None:
        if isinstance(editor, QComboBox):
            editor.setCurrentText(index.data(Qt.ItemDataRole.DisplayRole))
        
        else:
            editor.setText(index.data(Qt.ItemDataRole.DisplayRole))
        
        return None
    
    
    def setModelData(self, editor: QComboBox | QLineEdit, model: QAbstractItemModel, 
                     index: QModelIndex | QPersistentModelIndex) -> None:
        if isinstance(editor, QComboBox):
            value = editor.currentText()
            
        else:
            value = editor.text().strip()
            if (index.column() == 3) and ( value.split(" ")[0].endswith((",",".")) ):
                full_value = value.split(" ")
                value = " ".join([full_value[0].rstrip(",."), full_value[1]])
                
            elif (index.column() == 4 or index.column() == 5) and ( value.endswith((",", ".")) ):
                value = value.rstrip(",.")
            
        model.setData(index, value, Qt.ItemDataRole.EditRole)
        return None
    
    
    def updateEditorGeometry(self, editor: QComboBox | QLineEdit, option: QStyleOptionViewItem, 
                             index: QModelIndex | QPersistentModelIndex) -> None:
        editor.setGeometry(option.rect)
        return None
    
    def sizeHint(self, option: QStyleOptionViewItem, index: QModelIndex) -> QSize:
        return super().sizeHint(option, index)
    