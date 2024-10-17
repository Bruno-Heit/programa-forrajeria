'''
    En este archivo se encuentran las clases DELEGADOS 
    que se usan para personalizar y editar las VISTAS
'''
from PySide6.QtWidgets import (QWidget, QStyledItemDelegate, QStyleOptionViewItem, 
                               QComboBox, QLineEdit, QDateTimeEdit)
from PySide6.QtCore import (Qt, QModelIndex, QSize, QPersistentModelIndex, 
                            QAbstractItemModel, Signal, Slot, QDateTime)

from utils.enumclasses import (TableViewId)
from utils.functionutils import (getProductsCategories, createCompleter, getProductNames)
from utils.customvalidators import (ProductNameValidator, ProductStockValidator, 
                                    ProductUnitPriceValidator, ProductComercPriceValidator,
                                    SaleDetailsValidator, SaleQuantityValidator, 
                                    SaleTotalCostValidator, SalePaidValidator)


#¡ == DELEGADO DE PRODUCTOS =======================================================================


class InventoryDelegate(QStyledItemDelegate):
    '''Clase DELEGADO que se encarga de personalizar/editar celdas del QTableView de inventario, 
    además, normalmente, el método 'setModelData' se encarga de validar datos, pero en este caso 
    no es necesario ya que cada editor (dependiendo de la columna) tiene un validador.'''
    fieldIsValid:Signal = Signal(object) # extensión de 'validator.validationSucceeded', 
                                   # emite hacia MainWindow un TableViewId.
    fieldIsInvalid:Signal = Signal(object) # extensión de 'validator.validationFailed',
                                        # emite hacia MainWindow tuple(TableViewId, 
                                        # feedback como str).
    
    def createEditor(self, parent: QWidget, option: QStyleOptionViewItem, 
                     index: QModelIndex | QPersistentModelIndex) -> QWidget:
        editor:QWidget
        validator = None
        
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
                validator = ProductNameValidator(
                    prev_name=index.data(Qt.ItemDataRole.DisplayRole),
                    parent=editor)
                validator.validationSucceeded.connect(self.__onValidField)
                validator.validationFailed.connect(self.__onInvalidField)
                editor.setValidator(validator)
            
            case 2: # descripción
                editor = QLineEdit(parent)
                editor.setMaxLength(200)
            
            case 3: # stock
                editor = QLineEdit(parent)
                editor.setMaxLength(31)
                validator = ProductStockValidator(parent=editor)
                validator.validationSucceeded.connect(self.__onValidField)
                validator.validationFailed.connect(self.__onInvalidField)
                editor.setValidator(validator)
                
            case 4: # precio unitario
                editor = QLineEdit(parent)
                editor.setMaxLength(10)
                validator = ProductUnitPriceValidator(editor)
                validator.validationSucceeded.connect(self.__onValidField)
                validator.validationFailed.connect(self.__onInvalidField)
                editor.setValidator(validator)
            
            case 5: # precio comercial
                editor = QLineEdit(parent)
                editor.setMaxLength(10)
                validator = ProductComercPriceValidator(editor)
                validator.validationSucceeded.connect(self.__onValidField)
                validator.validationFailed.connect(self.__onInvalidField)
                editor.setValidator(validator)
        return editor
    
    
    @Slot()
    def __onValidField(self):
        '''
        Emite la señal 'fieldIsValid' hacia MainWindow. Funciona principalmente 
        como una extensión de la señal 'validator.validationSucceeded'.

        Retorna
        -------
        None
        '''
        self.fieldIsValid.emit(TableViewId.INVEN_TABLE_VIEW)
        return None
    
    
    @Slot(str)
    def __onInvalidField(self, feedback_text:str):
        '''
        Emite la señal 'fieldIsValid' hacia MainWindow. Funciona principalmente 
        como una extensión de la señal 'validator.validationSucceeded'.

        Parámetros
        ----------
        feedback_text: str
            Texto con feedback para mostrar al usuario

        Retorna
        -------
        None
        '''
        self.fieldIsInvalid.emit((TableViewId.INVEN_TABLE_VIEW, feedback_text))
        return None
    
    
    def setEditorData(self, editor: QComboBox | QLineEdit,
                      index: QModelIndex | QPersistentModelIndex) -> None:
        if isinstance(editor, QComboBox):
            editor.setCurrentText(index.data(Qt.ItemDataRole.DisplayRole))
        
        else:
            editor.setText(index.data(Qt.ItemDataRole.DisplayRole))
        
        return None
    
    
    def setModelData(self, editor: QComboBox | QLineEdit, model: QAbstractItemModel, 
                     index: QModelIndex | QPersistentModelIndex) -> None:
        
        col:int = index.column()
        
        #* formateo de datos
        if isinstance(editor, QComboBox):
            value = editor.currentText()
            
        else:
            value = editor.text().strip()
            # col 3 es stock
            if (col == 3) and ( value.split(" ")[0].endswith((",",".")) ):
                full_value = value.split(" ")
                try:
                    value = " ".join([full_value[0].rstrip(",."), full_value[1]])
                except IndexError: # devuelve IndexError cuando no se escribe la unidad de medida
                    value = full_value[0].rstrip(",.")
            
            # col 4 es precio normal, col 5 es precio comercial
            elif (col == 4 or col == 5) and ( value.endswith((",", ".")) ):
                value = value.rstrip(",.")
            
            editor.setText(value)
        
        model.setData(index, value, Qt.ItemDataRole.EditRole)
        return None
    
    
    def updateEditorGeometry(self, editor: QComboBox | QLineEdit, option: QStyleOptionViewItem, 
                             index: QModelIndex | QPersistentModelIndex) -> None:
        editor.setGeometry(option.rect)
        return None
    
    
    def sizeHint(self, option: QStyleOptionViewItem, index: QModelIndex) -> QSize:
        return super().sizeHint(option, index)


#¡ == DELEGADO DE VENTAS ==========================================================================


class SalesDelegate(QStyledItemDelegate):
    '''Clase DELEGADO que se encarga de personalizar/editar celdas del QTableView de ventas, 
    además, normalmente, el método 'setModelData' se encarga de validar datos, pero en este 
    caso no es necesario ya que cada editor (dependiendo de la columna) tiene un validador.'''
    fieldIsValid:Signal = Signal(object) # extensión de 'validator.validationSucceeded', 
                                   # emite hacia MainWindow un TableViewId.
    fieldIsInvalid:Signal = Signal(object) # extensión de 'validator.validationFailed',
                                        # emite hacia MainWindow tuple(TableViewId, 
                                        # feedback como str).
    
    #* columnas: 0: detalle de venta | 
    #* 1: cantidad (+ unidad de medida) | 2: producto | 
    #* 3: costo total | 4: abonado | 5: fecha y hora
    
    def __init__(self, datetime_format:str) -> None:
        super(SalesDelegate, self).__init__()
        self._datetime_format = datetime_format
    
    
    def createEditor(self, parent:QWidget, option: QStyleOptionViewItem, 
                     index:QModelIndex | QPersistentModelIndex) -> QWidget:
        editor:QWidget
        validator = None
        
        match index.column():
            case 0: # detalle de venta
                editor = QLineEdit(parent)
                validator = SaleDetailsValidator(parent)
                validator.validationSucceeded.connect(self.__onValidField)
                validator.validationFailed.connect(self.__onInvalidField)
                editor.setValidator(validator)
            
            case 1: # cantidad
                editor = QLineEdit(parent)
                validator = SaleQuantityValidator(parent)
                validator.validationSucceeded.connect(self.__onValidField)
                validator.validationFailed.connect(self.__onInvalidField)
                editor.setValidator(validator)
            
            case 2: # producto
                editor = QComboBox(parent)
                editor.setEditable(False)
                editor.setFrame(False)
                editor.addItems(getProductNames())
                editor.setPlaceholderText("Seleccionar un producto...")
            
            case 3: # costo total
                editor = QLineEdit(parent)
                validator = SaleTotalCostValidator(parent)
                validator.validationSucceeded.connect(self.__onValidField)
                validator.validationFailed.connect(self.__onInvalidField)
                editor.setValidator(validator)
            
            case 4: # abonado
                editor = QLineEdit(parent)
                validator = SalePaidValidator(parent)
                validator.validationSucceeded.connect(self.__onValidField)
                validator.validationFailed.connect(self.__onInvalidField)

            case 5: # fecha y hora
                editor = QDateTimeEdit(parent)
                editor.setDisplayFormat(self._datetime_format)
                editor.setCalendarPopup(True)
        return editor
    
    
    @Slot()
    def __onValidField(self):
        '''
        Emite la señal 'fieldIsValid' hacia MainWindow. Funciona principalmente 
        como una extensión de la señal 'validator.validationSucceeded'.

        Retorna
        -------
        None
        '''
        self.fieldIsValid.emit(TableViewId.SALES_TABLE_VIEW)
        return None
    
    
    @Slot(str)
    def __onInvalidField(self, feedback_text:str):
        '''
        Emite la señal 'fieldIsValid' hacia MainWindow. Funciona principalmente 
        como una extensión de la señal 'validator.validationSucceeded'.

        Parámetros
        ----------
        feedback_text: str
            Texto con feedback para mostrar al usuario

        Retorna
        -------
        None
        '''
        self.fieldIsInvalid.emit((TableViewId.SALES_TABLE_VIEW, feedback_text))
        return None


    def setEditorData(self, editor: QComboBox | QLineEdit,
                      index: QModelIndex | QPersistentModelIndex) -> None:
        if isinstance(editor, QComboBox): # columna de producto
            editor.setCurrentText(index.data(Qt.ItemDataRole.DisplayRole))
        
        elif isinstance(editor, QLineEdit): # columnas de: detalle de venta | cantidad | 
                                 # costo total | abonado
            match index.column():
                case 1: # cantidad
                    editor.setText(
                        str(index.data(Qt.ItemDataRole.DisplayRole)).split(" ", 1)[0]
                    )
                    
                case _: # detalle de venta | costo total | abonado
                    editor.setText(index.data(Qt.ItemDataRole.DisplayRole))
            
        
        elif isinstance(editor, QDateTimeEdit): # columna de fecha y hora
            cell_datetime = QDateTime.fromString(
                    index.data(Qt.ItemDataRole.DisplayRole),
                    self._datetime_format
            )
            editor.setDateTime(cell_datetime)
        
        return None


    def setModelData(self, editor: QComboBox | QLineEdit | QDateTimeEdit, 
                     model: QAbstractItemModel, 
                     index: QModelIndex | QPersistentModelIndex) -> None:
        
        col:int = index.column()
        
        #* formateo de datos
        if isinstance(editor, QComboBox):
            value = editor.currentText()
            
        elif isinstance(editor, QLineEdit):
            value = editor.text().strip()
            match col:
                case 1 | 3 | 4: # cantidad | costo total | abonado
                    if value.split(" ")[0].endswith((",",".")):
                        value = value.rstrip(",.")

                case _:
                    pass
            editor.setText(value)
        
        elif isinstance(editor, QDateTimeEdit):
            value = editor.text()
        
        model.setData(index, value, Qt.ItemDataRole.EditRole)
        return None


    def updateEditorGeometry(self, editor: QComboBox | QLineEdit, option: QStyleOptionViewItem, 
                             index: QModelIndex | QPersistentModelIndex) -> None:
        editor.setGeometry(option.rect)
        return None


    def sizeHint(self, option: QStyleOptionViewItem, index: QModelIndex) -> QSize:
        return super().sizeHint(option, index)


