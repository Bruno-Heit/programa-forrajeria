'''
    En este archivo se encuentran las clases DELEGADOS 
    que se usan para personalizar y editar las VISTAS
'''
from PySide6.QtWidgets import (QWidget, QStyledItemDelegate, QStyleOptionViewItem, 
                               QComboBox, QLineEdit, QDateTimeEdit)
from PySide6.QtCore import (Qt, QModelIndex, QSize, QPersistentModelIndex, 
                            QAbstractItemModel, Signal, Slot, QDateTime, QEvent, 
                            QObject)

from utils.enumclasses import (TableViewId, TableViewColumns, Regex)
from utils.functionutils import (getProductsCategories, createCompleter, getProductNames)
from utils.customvalidators import (ProductNameValidator, ProductStockValidator, 
                                    ProductUnitPriceValidator, ProductComercPriceValidator, 
                                    SaleDetailsValidator, SaleQuantityValidator, 
                                    SaleTotalCostValidator, SalePaidValidator,
                                    DebtorNameValidator, DebtorSurnameValidator, DebtorPhoneNumberValidator, 
                                    DebtorDirectionValidator, DebtorPostalCodeValidator)
from utils.classes import (ProductsBalanceDialog)
from utils.proxy_models import (DebtsProxyModel)

from re import (compile, IGNORECASE, search, sub)

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
            case TableViewColumns.INV_CATEGORY.value: # categoría
                editor = QComboBox(parent)
                editor.setEditable(False)
                editor.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
                editor.setFrame(False)
                editor.addItems(getProductsCategories())
                editor.setPlaceholderText("Seleccionar una categoría")
            
            case TableViewColumns.INV_PRODUCT_NAME.value: # nombre
                editor = QLineEdit(parent)
                editor.setCompleter(createCompleter(type=3))
                editor.setMaxLength(50)
                validator = ProductNameValidator(
                    prev_name=index.data(Qt.ItemDataRole.DisplayRole),
                    parent=editor)
                validator.validationSucceeded.connect(self.__onValidField)
                validator.validationFailed.connect(self.__onInvalidField)
                editor.setValidator(validator)
            
            case TableViewColumns.INV_DESCRIPTION.value: # descripción
                editor = QLineEdit(parent)
                editor.setMaxLength(200)
            
            case TableViewColumns.INV_STOCK.value: # stock
                editor = QLineEdit(parent)
                editor.setMaxLength(31)
                validator = ProductStockValidator(parent=editor)
                validator.validationSucceeded.connect(self.__onValidField)
                validator.validationFailed.connect(self.__onInvalidField)
                editor.setValidator(validator)
                
            case TableViewColumns.INV_NORMAL_PRICE.value: # precio unitario
                editor = QLineEdit(parent)
                editor.setMaxLength(10)
                validator = ProductUnitPriceValidator(editor)
                validator.validationSucceeded.connect(self.__onValidField)
                validator.validationFailed.connect(self.__onInvalidField)
                editor.setValidator(validator)
            
            case TableViewColumns.INV_COMERCIAL_PRICE.value: # precio comercial
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
            case TableViewColumns.SALES_DETAIL.value: # detalle de venta
                editor = QLineEdit(parent)
                validator = SaleDetailsValidator(parent)
                validator.validationSucceeded.connect(self.__onValidField)
                validator.validationFailed.connect(self.__onInvalidField)
                editor.setValidator(validator)
            
            case TableViewColumns.SALES_QUANTITY.value: # cantidad
                editor = QLineEdit(parent)
                validator = SaleQuantityValidator(parent)
                validator.validationSucceeded.connect(self.__onValidField)
                validator.validationFailed.connect(self.__onInvalidField)
                editor.setValidator(validator)
            
            case TableViewColumns.SALES_PRODUCT_NAME.value: # producto
                editor = QComboBox(parent)
                editor.setEditable(False)
                editor.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
                editor.setFrame(False)
                editor.addItems(getProductNames())
                editor.setPlaceholderText("Seleccionar un producto...")
            
            case TableViewColumns.SALES_TOTAL_COST.value: # costo total
                editor = QLineEdit(parent)
                validator = SaleTotalCostValidator(parent)
                validator.validationSucceeded.connect(self.__onValidField)
                validator.validationFailed.connect(self.__onInvalidField)
                editor.setValidator(validator)
            
            case TableViewColumns.SALES_TOTAL_PAID.value: # abonado
                editor = QLineEdit(parent)
                validator = SalePaidValidator(parent)
                validator.validationSucceeded.connect(self.__onValidField)
                validator.validationFailed.connect(self.__onInvalidField)

            case TableViewColumns.SALES_DATETIME.value: # fecha y hora
                editor = QDateTimeEdit(parent)
                editor.setDisplayFormat(self._datetime_format)
                editor.setCalendarPopup(True)
        return editor
    
    
    @Slot()
    def __onValidField(self):
        '''
        Emite la señal 'fieldIsValid' hacia MainWindow. Funciona principalmente 
        como una extensión de la señal 'validator.validationSucceeded'.

        
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
        if isinstance(editor, QComboBox): # producto
            value = editor.currentText()
            
        elif isinstance(editor, QLineEdit): # detalle de venta | cantidad | costo total | abonado
            value = editor.text().strip()
            match col:
                case 0: # detalle de venta
                    pattern = compile(Regex.SALES_DETAILS_PRICE_TYPE.value, IGNORECASE)
                    # busca en el valor el patrón de (P. NORMAL) ó (P. COMERCIAL)
                    price_type = search(pattern, value)
                    
                    # verifica si alguno de esos strings está, sino lo coloca al final
                    if not search(pattern, value):
                        price_type = search(pattern, model._data[index.row()][index.column() + 1])
                        price_type = str(price_type.group()).upper()
                        
                        value = f"{value} {price_type}"
                    
                    # si SÍ ESTÁ lo reemplaza...
                    else:
                        price_type = str(price_type.group()).upper().replace(" ", "")
                        value = sub(pattern, price_type, value)
                
                case 1 | 3 | 4: # cantidad | costo total | abonado
                    if value.split(" ")[0].endswith((",",".")):
                        value = value.rstrip(",.")

            editor.setText(value)
        
        elif isinstance(editor, QDateTimeEdit): # fecha y hora
            value = editor.text()
        
        model.setData(index, value, Qt.ItemDataRole.EditRole)
        return None


    def updateEditorGeometry(self, editor: QComboBox | QLineEdit, option: QStyleOptionViewItem, 
                             index: QModelIndex | QPersistentModelIndex) -> None:
        editor.setGeometry(option.rect)
        return None


    def sizeHint(self, option: QStyleOptionViewItem, index: QModelIndex) -> QSize:
        return super().sizeHint(option, index)



#¡ == DELEGADO DE DEUDAS ==========================================================================


class DebtsDelegate(QStyledItemDelegate):
    '''Clase DELEGADO que se encarga de personalizar/editar celdas del QTableView de deudas, 
    además, normalmente, el método 'setModelData' se encarga de validar datos, pero en este 
    caso no es necesario ya que cada editor (dependiendo de la columna) tiene un validador.'''
    fieldIsValid:Signal = Signal(object) # extensión de 'validator.validationSucceeded', 
                                   # emite hacia MainWindow un TableViewId.
    fieldIsInvalid:Signal = Signal(object) # extensión de 'validator.validationFailed',
                                        # emite hacia MainWindow tuple(TableViewId, 
                                        # feedback como str).
    balanceDialogCreated:Signal = Signal()
    balanceDialogFinished:Signal = Signal()
    

    def createEditor(self, parent:QWidget, option: QStyleOptionViewItem, 
                     index:QModelIndex | QPersistentModelIndex) -> QWidget:
        editor:QWidget
        validator = None
        match index.column():
            case TableViewColumns.DEBTS_NAME.value:
                editor = QLineEdit(parent)
                validator = DebtorNameValidator(editor)
                validator.validationSucceeded.connect(self.__onValidField)
                validator.validationFailed.connect(self.__onInvalidField)
                editor.setValidator(validator)
            
            case TableViewColumns.DEBTS_SURNAME.value:
                editor = QLineEdit(parent)
                validator = DebtorSurnameValidator(editor)
                validator.validationSucceeded.connect(self.__onValidField)
                validator.validationFailed.connect(self.__onInvalidField)
                editor.setValidator(validator)
            
            case TableViewColumns.DEBTS_PHONE_NUMBER.value:
                editor = QLineEdit(parent)
                validator = DebtorPhoneNumberValidator(editor)
                validator.validationSucceeded.connect(self.__onValidField)
                validator.validationFailed.connect(self.__onInvalidField)
                editor.setValidator(validator)
            
            case TableViewColumns.DEBTS_DIRECTION.value:
                editor = QLineEdit(parent)
                validator = DebtorDirectionValidator(editor)
                validator.validationSucceeded.connect(self.__onValidField)
                validator.validationFailed.connect(self.__onInvalidField)
                editor.setValidator(validator)
            
            case TableViewColumns.DEBTS_POSTAL_CODE.value:
                editor = QLineEdit(parent)
                validator = DebtorPostalCodeValidator(editor)
                validator.validationSucceeded.connect(self.__onValidField)
                validator.validationFailed.connect(self.__onInvalidField)
                editor.setValidator(validator)
        return editor
    
    
    @Slot()
    def __onValidField(self):
        '''
        Emite la señal 'fieldIsValid' hacia MainWindow. Funciona principalmente 
        como una extensión de la señal 'validator.validationSucceeded'.

        
        '''
        self.fieldIsValid.emit(TableViewId.DEBTS_TABLE_VIEW)
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

        
        '''
        self.fieldIsInvalid.emit((TableViewId.DEBTS_TABLE_VIEW, feedback_text))
        return None


    def setEditorData(self, editor: QLineEdit,
                      index: QModelIndex | QPersistentModelIndex) -> None:
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

    
    def editorEvent(self, event:QEvent, model:DebtsProxyModel, 
                    option:QStyleOptionViewItem, index:QModelIndex):
        '''
        Capta los eventos cuando se crea un editor en alguna columna. Se usa 
        acá para inicializar el Dialog personalizado que creé para mostrar 
        los productos con sus saldos.
        '''
        balance_dialog:ProductsBalanceDialog
        
        if index.column() == TableViewColumns.DEBTS_BALANCE.value:
            if event.type() == QEvent.Type.MouseButtonDblClick:
                debtor_id = model.getDebtorID(index)
                balance_dialog = ProductsBalanceDialog(
                    debtor_id=debtor_id,
                    table_view=self.parent() # le paso el table view para poder redimensionar 
                )                            # el dialog cuando se crea y no se salga del 
                                             # rectángulo del table view.
                
                # TODO: EMITIR SEÑAL CUANDO SE CIERRE EL DIALOG A MAINWINDOW PARA ACTUALIZAR EL MODELO DE DATOS DE DEUDAS CON EL NUEVO BALANCE
                #? emite el dialog a MainWindow para que se tenga una referencia, sino se cierra
                self.balanceDialogCreated.emit(balance_dialog)
                
                # emite la señal "finished" hacia MainWindow, se usa para obtener el nuevo balance
                balance_dialog.finished.connect(lambda: self.balanceDialogFinished.emit())
                
                balance_dialog.show()
                balance_dialog.raise_()
                return True
        
        return False
            





