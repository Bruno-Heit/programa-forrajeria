from PySide6.QtWidgets import (QWidget, QStyledItemDelegate, QStyleOptionViewItem, 
                               QComboBox, QLineEdit, QDateTimeEdit)
from PySide6.QtCore import (Qt, QModelIndex, QSize, QPersistentModelIndex, 
                            QAbstractItemModel, Slot, QDateTime)

from utils.enumclasses import (LabelFeedbackStyle, TableViewColumns)
from utils.functionutils import (DATETIME_FORMAT)
from utils.customvalidators import (ProductBalanceValidator, SaleDetailsValidator)


class ProductsBalanceDelegate(QStyledItemDelegate):
    '''Clase DELEGADO que se encarga de personalizar/editar celdas del QTableView 
    de los productos adeudados.'''
    
    # TODO: reimplementar todos los métodos
    
    def createEditor(self, parent:QWidget, option: QStyleOptionViewItem, 
                     index:QModelIndex | QPersistentModelIndex) -> QWidget:
        editor:QLineEdit | QDateTimeEdit
        validator = None
        match index.column():
            case TableViewColumns.PRODS_BAL_DATETIME.value:
                editor = QDateTimeEdit(parent)
                editor.setDisplayFormat(DATETIME_FORMAT)
                editor.setCalendarPopup(True)
            
            case TableViewColumns.PRODS_BAL_DESCRIPTION.value:
                editor = QLineEdit(parent)
                validator = SaleDetailsValidator(editor)
                validator.validationSucceeded.connect(
                    lambda: self.__onValidField(editor)
                )
                validator.validationFailed.connect(
                    lambda: self.__onInvalidField(editor)
                )
                editor.setValidator(validator)
            
            case TableViewColumns.PRODS_BAL_BALANCE.value:
                editor = QLineEdit(parent)
                validator = ProductBalanceValidator(editor)
                validator.validationSucceeded.connect(
                    lambda: self.__onValidField(editor)
                )
                validator.validationFailed.connect(
                    lambda: self.__onInvalidField(editor)
                )
                editor.setValidator(validator)
        return editor
    
    
    @Slot()
    def __onValidField(self, editor:QLineEdit):
        '''
        Cambia el estilo del campo para representar la validez.
        '''
        editor.setStyleSheet(LabelFeedbackStyle.VALID.value)
        return None
    
    
    @Slot(str)
    def __onInvalidField(self, editor:QLineEdit):
        '''
        Cambia el estilo del campo para representar la invalidez.
        '''
        editor.setStyleSheet(LabelFeedbackStyle.INVALID.value)
        return None


    def setEditorData(self, editor: QLineEdit | QDateTimeEdit,
                      index: QModelIndex | QPersistentModelIndex) -> None:
        if isinstance(editor, QDateTimeEdit):
            cell_datetime = QDateTime.fromString(
                    index.data(Qt.ItemDataRole.DisplayRole),
                    DATETIME_FORMAT
            )
            editor.setDateTime(cell_datetime)
        
        elif isinstance(editor, QDateTimeEdit):
            editor.setText(index.model().data(index, Qt.ItemDataRole.DisplayRole))
        return None


    def setModelData(self, editor: QLineEdit, 
                     model: QAbstractItemModel, 
                     index: QModelIndex | QPersistentModelIndex) -> None:
        
        #* formateo de datos
        match index.column():
            case TableViewColumns.DEBTS_POSTAL_CODE.value:
                value = editor.text().replace(",","").replace(".","").strip()
            
            case _:
                value:str = editor.text().strip()
        
        model.setData(index, value, Qt.ItemDataRole.EditRole)
        return None


    def updateEditorGeometry(self, editor: QComboBox | QLineEdit, option: QStyleOptionViewItem, 
                             index: QModelIndex | QPersistentModelIndex) -> None:
        editor.setGeometry(option.rect)
        return None


    def sizeHint(self, option: QStyleOptionViewItem, index: QModelIndex) -> QSize:
        return super().sizeHint(option, index)