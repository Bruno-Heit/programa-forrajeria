'''
    Ésta clase en principio iría dentro del archivo 
    'utils/delegates.py' pero ya que desde el delegado 
    de la tabla de deudas se llama a un dialog del 
    archivo 'utils/classes.py' y desde ahí de nuevo al 
    archivo 'utils/delegates.py' se crea un error de tipo 
    CircularImport, por lo que decidí mover la clase 
    delegado del dialog a su propio archivo separado.
'''


from PySide6.QtWidgets import (QWidget, QStyledItemDelegate, QStyleOptionViewItem, 
                               QComboBox, QLineEdit, QDateTimeEdit)
from PySide6.QtCore import (Qt, QModelIndex, QSize, QPersistentModelIndex, 
                            QAbstractItemModel, Slot, QDateTime)

from utils.enumclasses import (LabelFeedbackStyle, TableViewColumns, Regex)
from utils.functionutils import (DATETIME_FORMAT)
from utils.customvalidators import (ProductBalanceValidator, SaleDetailsValidator)

from re import (compile, IGNORECASE, search, sub)


class ProductsBalanceDelegate(QStyledItemDelegate):
    '''Clase DELEGADO que se encarga de personalizar/editar celdas del QTableView 
    de los productos adeudados.'''
    
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
        
        elif isinstance(editor, QLineEdit):
            editor.setText(
                str(index.model().data(
                    index, Qt.ItemDataRole.DisplayRole)
                )
            )
        return None


    def setModelData(self, editor: QLineEdit | QDateTimeEdit, 
                     model: QAbstractItemModel, 
                     index: QModelIndex | QPersistentModelIndex) -> None:
        match index.column():
            case TableViewColumns.PRODS_BAL_DATETIME.value:
                editor:QDateTimeEdit
                value = editor.text()
            
            case TableViewColumns.PRODS_BAL_DESCRIPTION.value:
                value = editor.text().strip()
                pattern = compile(Regex.SALES_DETAILS_PRICE_TYPE.value, IGNORECASE)
                
                # busca en el valor el patrón de (P. PÚBLICO) ó (P. COMERCIAL)
                _price_type = search(pattern, value)
                
                # verifica si alguno de esos strings está, sino lo coloca al final
                if not search(pattern, value):
                    _price_type = search(pattern, model.data(index, Qt.ItemDataRole.DisplayRole))
                    _price_type = str(_price_type.group()).upper()
                    
                    value = f"{value} {_price_type}"
                
                # si SÍ ESTÁ lo reemplaza...
                else:
                    _price_type = str(_price_type.group()).upper().replace(" ", "")
                    value = sub(pattern, _price_type, value)
            
            case TableViewColumns.PRODS_BAL_BALANCE.value:
                value = editor.text().replace(",",".")
                if value.endswith((",",".")):
                        value = value.rstrip(",.")
        
        model.setData(index, value, Qt.ItemDataRole.EditRole)
        return None


    def updateEditorGeometry(self, editor: QComboBox | QLineEdit, option: QStyleOptionViewItem, 
                             index: QModelIndex | QPersistentModelIndex) -> None:
        editor.setGeometry(option.rect)
        return None


    def sizeHint(self, option: QStyleOptionViewItem, index: QModelIndex) -> QSize:
        return super().sizeHint(option, index)