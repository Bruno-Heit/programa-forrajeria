'''
    Este archivo contiene todas las subclases de QDialogs, de widgets con 
    interfaces gráficas o modelos de datos simples (que no heredan de 
    QAbstractItemModel).
    Los modelos de datos simples mencionados son principalmente usados 
    dentro de las propias subclases declaradas en este archivo, pero no 
    necesariamente exclusivos de ellas, y el principal uso es para facilitar 
    la validación de datos.
'''

from numpy import (ndarray, array)

from PySide6.QtWidgets import (QDialog, QDialogButtonBox, QLineEdit, QCompleter, 
                               QWidget, QGraphicsDropShadowEffect, QListWidgetItem)
from PySide6.QtCore import (Signal, QSize, QRect, QPropertyAnimation, QEasingCurve, 
                            QPoint, QSignalBlocker)
from PySide6.QtGui import (QIcon, QShowEvent, QCursor, QKeyEvent, QColor, QCloseEvent, 
                           QTextCursor, QMouseEvent)

from ui.ui_productDialog import Ui_Dialog
from ui.ui_saleDialog import Ui_saleDialog
from ui.ui_listproduct import Ui_listProduct
from ui.ui_debtorDataDialog import Ui_debtorDataDialog
from ui.ui_debts_balanceProductsList import Ui_ProductsBalance
from ui.ui_categoriesDescEditDialog import Ui_CategoryDescEditDialog

from resources import (rc_icons)

from utils.functionutils import *
from utils.workerclasses import *
from utils.dboperations import *
from utils.enumclasses import (WidgetStyle, InventoryPriceType, 
                               ProductFields, SaleFields, DebtsFields, 
                               InvModelCols, SalesModelCols, DebtorFullName, 
                               DebtorModelCols, DebtsModelCols, ModelHeaders, 
                               LabelFeedbackStyle, InvViewCols, SalesViewCols, 
                               DebtorViewCols, DebtsViewCols,
                               SaleDialogDimensions, DateAndTimeFormat)
from utils.model_classes import (ProductsBalanceModel)
from utils.proxy_models import (ProductsBalanceProxyModel)
from utils.productbalancedelegate import (ProductsBalanceDelegate)
from utils.customvalidators import (SearchBarValidator, ProductReduceDebtValidator, 
                                    CategoryDescValidator)
from utils.eventfilters import (BackgroundEventFilter, CategoryDescTextEditEventFilter)
from ui.customCalendars import (CustomCalendar)

from sqlite3 import (Error as sqlite3Error)
from phonenumbers import (parse, format_number, is_valid_number, 
                          PhoneNumber, PhoneNumberFormat, 
                          NumberParseException)
from re import (sub)
from datetime import (datetime)


# PRODUCTOS ====================================================================================================


class ProductValues(QObject):
    '''
    Clase que contiene los valores de los campos de ProductDialog. El principal 
    uso de la clase es para "simular" un MODELO DE DATOS, ya que no usa 
    exactamente la misma metodología para guardar los datos, y al mismo tiempo 
    maneja mediante señales los cambios en los datos más relevantes.
    '''
    validityChanged:Signal = Signal() # se emite para activar/desactivar el botón 'Ok' del dialog
    
    
    def __init__(self) -> None:
        super(ProductValues, self).__init__()
        self.__name:str = None
        self.__category:str = None
        self.__description:str = ""
        self.__stock_quantity:float = None
        self.__stock_unit:str = ""
        self.__normal_price:float = None
        self.__comercial_price:float = ""
        
        # validez de datos
        self.__FIELDS_VALIDITY:dict[str, bool] = {
            ProductFields.NAME.name: None,
            ProductFields.CATEGORY.name: None,
            ProductFields.STOCK_QUANTITY.name: None,
            ProductFields.NORMAL_PRICE.name: None,
            ProductFields.COMERCIAL_PRICE.name: True
        }
        return None
    
    
    # setters
    def setProductName(self, product_name:str) -> None:
        '''
        Guarda el nombre del producto.

        Parámetros
        ----------
        product_name : str
            el nuevo nombre de producto
        '''
        if self.__name != product_name:
            self.__name = product_name
        return None
    
    
    def setCategory(self, category:str) -> None:
        '''
        Guarda la categoría.

        Parámetros
        ----------
        category : str
            la nueva categoría del producto
        '''
        if self.__category != category:
            self.__category = category
        return None
    
    
    def setDescription(self, description:str) -> None:
        '''
        Guarda la descripción del producto.

        Parámetros
        ----------
        description : str
            la nueva descripción del producto
        '''
        self.__description = description
        return None
    
    
    def setStockQuantity(self, stock:str) -> None:
        '''
        Guarda el stock del producto.

        Parámetros
        ----------
        stock : str
            el nuevo stock del producto
        '''
        if self.__stock_quantity != stock:
            self.__stock_quantity = stock
        return None
    
    
    def setStockUnit(self, stock_unit:str) -> None:
        '''
        Guarda la unidad de medida usada en el stock.

        Parámetros
        ----------
        stock_unit : str
            la nueva unidad de medida del stock
        '''
        self.__stock_unit = stock_unit
        return None
    
    
    def setMeasurementUnit(self, measurement_unit:str) -> None:
        '''
        Guarda la unidad de medida.

        Parámetros
        ----------
        measurement_unit : str
            la nueva unidad de medida
        '''
        self.__stock_unit = measurement_unit
        return None
    
    
    def setNormalPrice(self, normal_price:str) -> None:
        '''
        Guarda el precio normal.

        Parámetros
        ----------
        normal_price : str
            el nuevo precio normal
        '''
        if self.__normal_price != normal_price:
            self.__normal_price = normal_price
        return None
    
    
    def setComercialPrice(self, comercial_price:str) -> None:
        '''
        Guarda el precio comercial.

        Parámetros
        ----------
        comercial_price : str
            el nuevo precio comercial
        '''
        if self.__comercial_price != comercial_price:
            self.__comercial_price = comercial_price
        return None
    
    
    def setFieldValidity(self, field:ProductFields, validity:bool) -> None:
        '''
        Guarda el valor de verdad del campo especificado. Emite la señal 
        'validityChanged'.
        
        Parámetros
        ----------
        field : ProductFields
            campo al que asignarle el nuevo valor de verdad
        validity : bool
            nuevo valor de verdad del campo
        '''
        match field:
            case ProductFields.NAME:
                self.__FIELDS_VALIDITY[ProductFields.NAME.name] = validity
            
            case ProductFields.CATEGORY:
                self.__FIELDS_VALIDITY[ProductFields.CATEGORY.name] = validity
            
            case ProductFields.STOCK_QUANTITY:
                self.__FIELDS_VALIDITY[ProductFields.STOCK_QUANTITY.name] = validity
            
            case ProductFields.NORMAL_PRICE:
                self.__FIELDS_VALIDITY[ProductFields.NORMAL_PRICE.name] = validity
            
            case ProductFields.COMERCIAL_PRICE:
                self.__FIELDS_VALIDITY[ProductFields.COMERCIAL_PRICE.name] = validity
        
        self.validityChanged.emit()
        return None
    
    
    # getters
    def getProductName(self) -> str:
        return self.__name
    
    
    def getCategory(self) -> str:
        return self.__category
    
    
    def getDescription(self) -> str:
        return self.__description
    
    
    def getStockQuantity(self) -> str:
        return str(self.__stock_quantity)
    
    
    def getStockUnit(self) -> str:
        return self.__stock_unit
    
    
    def getNormalPrice(self) -> str:
        return str(self.__normal_price)
    
    
    def getComercialPrice(self) -> str:
        return str(self.__comercial_price if self.__comercial_price else 0)
    
    
    def isAllValid(self) -> bool:
        '''
        Devuelve un valor de verdad que determina si todos los campos tienen 
        valores válidos.

        Retorna
        -------
        bool
            flag que determina si todos los campos son válidos
        '''
        return all(self.__FIELDS_VALIDITY.values())





# Dialog con datos de un producto
class ProductDialog(QDialog):
    '''QDialog creado al presionar el botón 'MainWindow.btn_add_product_inventory'. 
    Sirve para crear un nuevo registro de producto en la tabla "Productos" en la base de datos.'''
    dataFilled:Signal = Signal(object) # emite un dict con todos los datos introducidos a MainWindow
    
    def __init__(self, db_path:str=DATABASE_DIR):
        '''
        Inicializa un **QDialog** que permite al usuario ingresar datos de un 
        producto a la base de datos.

        Parámetros
        ----------
        db_path : str, opcional
            *path* de la base de datos utilizada, por defecto DATABASE_DIR
        '''
        super(ProductDialog, self).__init__()
        self.productDialog_ui = Ui_Dialog()
        self.productDialog_ui.setupUi(self)
        
        self.product_values = ProductValues()
        
        self._db_path = db_path
        
        self.setup_validators()
        
        self.setup_ui()
        
        # completer
        self.productDialog_ui.lineedit_productName.setCompleter(
            createCompleter(type=3)
        )
        
        self.setup_signals()
        return None
    
    
    #### MÉTODOS #####################################################
    def setup_validators(self) -> None:
        self.name_validator = ProductNameValidator(
            self.productDialog_ui.lineedit_productName
        )
        self.description_validator = QRegularExpressionValidator(
            Regex.GENERIC_CHARS_TO_AVOID.value,
            self.productDialog_ui.lineedit_productDescription
        )
        self.stock_validator = ProductStockValidator(
            pattern=Regex.PROD_STOCK_QUANTITY.value,
            parent=self.productDialog_ui.lineedit_productStock
        )
        self.stock_unit_validator = QRegularExpressionValidator(
            Regex.GENERIC_CHARS_TO_AVOID.value,
            self.productDialog_ui.lineedit_measurementUnit
        )
        self.unit_price_validator = ProductUnitPriceValidator(
            self.productDialog_ui.lineedit_productUnitPrice
        )
        self.comerc_price_validator = ProductComercPriceValidator(
            self.productDialog_ui.lineedit_productComercialPrice
        )
        
        self.productDialog_ui.lineedit_productName.setValidator(self.name_validator)
        self.productDialog_ui.lineedit_productDescription.setValidator(self.description_validator)
        self.productDialog_ui.lineedit_productStock.setValidator(self.stock_validator)
        self.productDialog_ui.lineedit_measurementUnit.setValidator(self.stock_unit_validator)
        self.productDialog_ui.lineedit_productUnitPrice.setValidator(self.unit_price_validator)
        self.productDialog_ui.lineedit_productComercialPrice.setValidator(self.comerc_price_validator)
        
        return None
    

    def setup_ui(self) -> None:
        self.productDialog_ui.buttonBox.button(QDialogButtonBox.Ok).setText("Aceptar")
        self.__hideWidgets()
        # desactiva desde el principio el botón "Aceptar"
        self.productDialog_ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
        self.productDialog_ui.buttonBox.button(QDialogButtonBox.Cancel).setText("Cancelar")
        comboBox_categories:list[str] = getProductsCategories(self._db_path)
        self.productDialog_ui.cb_productCategory.addItems(comboBox_categories)
        
        self.__setInitialStyles()
        return None
    
    
    def __hideWidgets(self) -> None:
        '''
        Método simple que esconde los widgets iniciales al instanciarse 
        el QDialog.
        '''
        # esconde widgets
        self.productDialog_ui.label_nameWarning.hide()
        self.productDialog_ui.label_stockWarning.hide()
        self.productDialog_ui.label_categoryWarning.hide()
        self.productDialog_ui.label_unitPriceWarning.hide()
        self.productDialog_ui.label_comercialPriceWarning.hide()
        return None
    
    
    def __setInitialStyles(self):
        '''
        Coloca íconos y establece stylesheets iniciales en los widgets.
        '''
        # flecha del combobox
        self.productDialog_ui.frame_productCategory.setStyleSheet(WidgetStyle.DEF_COMBOBOX_ARROW_ICON.value)
        
        self.productDialog_ui.buttonBox.setStyleSheet(WidgetStyle.DIALOG_CANCEL_BTN_STYLE.value)
        return None
    
    
    def setup_signals(self) -> None:
        # formateo de campos
        self.productDialog_ui.lineedit_productName.editingFinished.connect(
            lambda: self.formatField(ProductFields.NAME)
        )
        self.productDialog_ui.lineedit_productStock.editingFinished.connect(
            lambda: self.formatField(ProductFields.STOCK_QUANTITY)
        )
        self.productDialog_ui.lineedit_measurementUnit.editingFinished.connect(
            lambda: self.formatField(ProductFields.STOCK_UNIT)
        )
        self.productDialog_ui.lineedit_productUnitPrice.editingFinished.connect(
            lambda: self.formatField(ProductFields.NORMAL_PRICE)
        )
        self.productDialog_ui.lineedit_productComercialPrice.editingFinished.connect(
            lambda: self.formatField(ProductFields.COMERCIAL_PRICE)
        )
        
        # guardar datos de campos opcionales
        self.productDialog_ui.lineedit_productDescription.editingFinished.connect(
            lambda: self.product_values.setDescription(
                self.productDialog_ui.lineedit_productDescription.text()
            )
        )
        self.productDialog_ui.lineedit_measurementUnit.editingFinished.connect(
            lambda: self.product_values.setStockUnit(
                self.productDialog_ui.lineedit_measurementUnit.text()
            )
        )
        
        # validación
        self.name_validator.validationSucceeded.connect(
            lambda: self.validatorOnValidationSucceded(ProductFields.NAME)
        )
        self.stock_validator.validationSucceeded.connect(
            lambda: self.validatorOnValidationSucceded(ProductFields.STOCK_QUANTITY)
        )
        self.unit_price_validator.validationSucceeded.connect(
            lambda: self.validatorOnValidationSucceded(ProductFields.NORMAL_PRICE)
        )
        self.comerc_price_validator.validationSucceeded.connect(
            lambda: self.validatorOnValidationSucceded(ProductFields.COMERCIAL_PRICE)
        )
        
        self.name_validator.validationFailed.connect(
            lambda error_message: self.validatorOnValidationFailed(
                field_validated=ProductFields.NAME,
                error_message=error_message
            )
        )
        self.stock_validator.validationFailed.connect(
            lambda error_message: self.validatorOnValidationFailed(
                field_validated=ProductFields.STOCK_QUANTITY,
                error_message=error_message
            )
        )
        self.unit_price_validator.validationFailed.connect(
            lambda error_message: self.validatorOnValidationFailed(
                field_validated=ProductFields.NORMAL_PRICE,
                error_message=error_message
            )
        )
        self.comerc_price_validator.validationFailed.connect(
            lambda error_message: self.validatorOnValidationFailed(
                field_validated=ProductFields.COMERCIAL_PRICE,
                error_message=error_message
            )
        )
        
        self.productDialog_ui.cb_productCategory.currentIndexChanged.connect(
            self.__checkProductCategoryValidity)
        
        # pseudo-modelo de datos
        self.product_values.validityChanged.connect(self.toggleOkButton)
        
        # otros
        self.productDialog_ui.buttonBox.accepted.connect(self.addProductToDatabase)
        
        return None
    
    
    @Slot(object)
    def formatField(self, field_to_format:ProductFields) -> None:
        '''
        Dependiendo del campo formatea el texto y lo asigna nuevamente en el 
        QLineEdit correspondiente.
        
        Parámetros
        ----------
        field_to_format: ProductFields
            El campo que hay que formatear
        '''
        text:str
        
        match field_to_format:
            case ProductFields.NAME:
                self.productDialog_ui.lineedit_productName.setText(
                    self.productDialog_ui.lineedit_productName.text().strip()
                )
            
            case ProductFields.STOCK_QUANTITY:
                text = self.productDialog_ui.lineedit_productStock.text().replace(".",",")
                if text.endswith(","):
                    text = text.rstrip(",")
                self.productDialog_ui.lineedit_productStock.setText(text)
            
            case ProductFields.STOCK_UNIT:
                self.productDialog_ui.lineedit_measurementUnit.setText(
                    self.productDialog_ui.lineedit_measurementUnit.text().strip()
                )
            
            case ProductFields.NORMAL_PRICE:
                text = self.productDialog_ui.lineedit_productUnitPrice.text().replace(".",",")
                if text.endswith(","):
                    text = text.rstrip(",")
                self.productDialog_ui.lineedit_productUnitPrice.setText(text)
            
            case ProductFields.COMERCIAL_PRICE:
                text = self.productDialog_ui.lineedit_productComercialPrice.text().replace(".",",")
                if text.endswith(","):
                    text = text.rstrip(",")
                self.productDialog_ui.lineedit_productComercialPrice.setText(text)
        
        return None
    
    
    @Slot(object)
    def validatorOnValidationSucceded(self, field_validated:ProductFields) -> None:
        '''
        Cambia el valor del flag asociado al campo que fue validado a True, 
        cambia el QSS del campo y esconde el QLabel asociado al campo. 
        
        Parámetros
        ----------
        field_validated: ProductFields
            El campo validado
        '''
        match field_validated:
            case ProductFields.NAME:
                self.product_values.setFieldValidity(field_validated, True)
                self.product_values.setProductName(
                    product_name=self.productDialog_ui.lineedit_productName.text()
                )
                
                self.productDialog_ui.lineedit_productName.setStyleSheet(
                    WidgetStyle.FIELD_VALID_VAL.value
                )
                self.productDialog_ui.label_nameWarning.hide()
            
            case ProductFields.STOCK_QUANTITY:
                self.product_values.setFieldValidity(field_validated, True)
                self.product_values.setStockQuantity(
                    stock=self.productDialog_ui.lineedit_productStock.text().replace(",",".")
                )
                
                self.productDialog_ui.lineedit_productStock.setStyleSheet(WidgetStyle.FIELD_VALID_VAL.value)
                self.productDialog_ui.label_stockWarning.hide()
            
            case ProductFields.NORMAL_PRICE:
                self.product_values.setFieldValidity(field_validated, True)
                self.product_values.setNormalPrice(
                    normal_price=self.productDialog_ui.lineedit_productUnitPrice.text().replace(",",".")
                )
                
                self.productDialog_ui.lineedit_productUnitPrice.setStyleSheet(WidgetStyle.FIELD_VALID_VAL.value)
                self.productDialog_ui.label_unitPriceWarning.hide()
            
            case ProductFields.COMERCIAL_PRICE:
                self.product_values.setFieldValidity(field_validated, True)
                self.product_values.setComercialPrice(
                    comercial_price=self.productDialog_ui.lineedit_productComercialPrice.text().replace(",", ".")
                )
                
                if not self.productDialog_ui.lineedit_productComercialPrice.text():
                    self.productDialog_ui.lineedit_productComercialPrice.setStyleSheet("")
                
                else:
                    self.productDialog_ui.lineedit_productComercialPrice.setStyleSheet(WidgetStyle.FIELD_VALID_VAL.value)
                self.productDialog_ui.label_comercialPriceWarning.hide()
        return None
    
    
    @Slot(object, str)
    def validatorOnValidationFailed(self, field_validated:ProductFields, error_message:str) -> None:
        '''
        Cambia el valor del flag asociado al campo que validado a False, 
        cambia el QSS del campo y muestra el QLabel asociado al campo con el 
        mensaje 'error_message' con feedback.
        
        Parámetros
        ----------
        field_validated: ProductFields
            El campo que validado
        error_message: str
            El mensaje de error para mostrar como feedback
        '''
        match field_validated:
            case ProductFields.NAME:
                self.product_values.setFieldValidity(field_validated, False)
                
                self.productDialog_ui.lineedit_productName.setStyleSheet(
                    WidgetStyle.FIELD_INVALID_VAL.value
                )
                self.productDialog_ui.label_nameWarning.show()
                self.productDialog_ui.label_nameWarning.setText(error_message)
            
            case ProductFields.STOCK_QUANTITY:
                self.product_values.setFieldValidity(field_validated, False)
                
                self.productDialog_ui.lineedit_productStock.setStyleSheet(
                    WidgetStyle.FIELD_INVALID_VAL.value
                )
                self.productDialog_ui.label_stockWarning.show()
                self.productDialog_ui.label_stockWarning.setText(error_message)
            
            case ProductFields.NORMAL_PRICE:
                self.product_values.setFieldValidity(field_validated, False)
                
                self.productDialog_ui.lineedit_productUnitPrice.setStyleSheet(
                    WidgetStyle.FIELD_INVALID_VAL.value
                )
                self.productDialog_ui.label_unitPriceWarning.show()
                self.productDialog_ui.label_unitPriceWarning.setText(error_message)
            
            case ProductFields.COMERCIAL_PRICE:
                self.product_values.setFieldValidity(field_validated, False)
                
                self.productDialog_ui.lineedit_productComercialPrice.setStyleSheet(
                    WidgetStyle.FIELD_INVALID_VAL.value
                )
                self.productDialog_ui.label_comercialPriceWarning.show()
                self.productDialog_ui.label_comercialPriceWarning.setText(error_message)
        return None
        
    
    @Slot()
    def __checkProductCategoryValidity(self) -> None:
        '''
        Verifica si 'cb_productCategory' tiene una categoría seleccionada. Si 
        la tiene, se considera válido y 'self.VALID_CATEGORY' será True, sino 
        False. Modifica el texto de 'label_categoryWarning' de acuerdo a las 
        condiciones, y el estilo del campo.
        Al finalizar, si el campo es válido comprueba si el resto de campos 
        son válidos.
        '''
        if not self.productDialog_ui.cb_productCategory.currentText().strip():
            self.productDialog_ui.cb_productCategory.setCurrentIndex(-1)
        
        # verifica la validez del campo
        if self.productDialog_ui.cb_productCategory.currentIndex() == -1:
            self.product_values.setFieldValidity(ProductFields.CATEGORY, False)
            self.product_values.setCategory(category="")
            
            self.productDialog_ui.label_categoryWarning.setText(
                "Se debe seleccionar una categoría para el producto"
            )
            self.productDialog_ui.cb_productCategory.setStyleSheet(
                WidgetStyle.FIELD_INVALID_VAL.value
            )

        else:
            self.product_values.setFieldValidity(ProductFields.CATEGORY, True)
            self.product_values.setCategory(
                self.productDialog_ui.cb_productCategory.itemText(
                    self.productDialog_ui.cb_productCategory.currentIndex()
                )
            )
            
            self.productDialog_ui.label_categoryWarning.setText("")
            self.productDialog_ui.cb_productCategory.setStyleSheet(
                WidgetStyle.FIELD_VALID_VAL.value
            )
        return None


    @Slot()
    def toggleOkButton(self) -> None:
        '''
        Verifica si todos los valores son válidos y activa o desactiva el 
        botón "Aceptar" dependiendo del caso.
        '''
        if self.product_values.isAllValid():
            self.productDialog_ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)
        else:
            self.productDialog_ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
        return None


    # botón "Aceptar"
    @Slot()
    def addProductToDatabase(self) -> None:
        '''
        Obtiene los datos de los campos y hace una consulta INSERT a la base 
        de datos.
        Emite la señal 'dataFilled' con los datos introducidos a MainWindow 
        para poder actualizar el MODELO DE DATOS.
        '''
        with DatabaseRepository(self._db_path) as db_repo:
            db_repo.insertRegister(
                ins_sql= '''INSERT INTO Productos(
                                nombre,
                                descripcion,
                                stock,
                                unidad_medida,
                                precio_unit,
                                precio_comerc,
                                IDcategoria,
                                eliminado) 
                            VALUES(
                                ?,
                                ?,
                                ?,
                                ?,
                                ?,
                                ?,
                                (SELECT IDcategoria 
                                 FROM Categorias 
                                 WHERE nombre_categoria=?),
                                0);''',
                ins_params=(
                    self.product_values.getProductName(),
                    self.product_values.getDescription(),
                    float(self.product_values.getStockQuantity()),
                    self.product_values.getStockUnit(),
                    float(self.product_values.getNormalPrice()),
                    float(self.product_values.getComercialPrice()),
                    self.product_values.getCategory()
                )
            )
            
            # emite los datos a MainWindow
            self.dataFilled.emit(
                {
                    'product_ID': db_repo.selectRegisters( # obtengo el último ID, el del nuevo producto
                        ''' SELECT IDproducto 
                            FROM Productos 
                            ORDER BY IDproducto DESC 
                            LIMIT 1;''')[0][0],
                    'product_name': self.product_values.getProductName(),
                    'product_description': self.product_values.getDescription(),
                    'product_stock': float(self.product_values.getStockQuantity()),
                    'product_measurement_unit': self.product_values.getStockUnit(),
                    'product_unit_price': float(self.product_values.getNormalPrice()),
                    'product_comercial_price': float(self.product_values.getComercialPrice()),
                    'product_category': self.product_values.getCategory()
                }
            )
        return None


# CATEGORÍAS ===================================================================================================


class CategoryDescDialog(QDialog):
    '''
    **QDialog** que permite modificar la descripción de la categoría 
    seleccionada desde MainWindow.
    
    Al cerrarse el dialog emite la señal *descriptionChanged* con la nueva 
    descripción.
    
    Éste **QDialog** sólo admite la operación UPDATE para actualizar en base 
    de datos la descripción de la categoría.
    '''
    descriptionChanged:Signal = Signal(str)
    
    def __init__(self, list_item:QListWidgetItem) -> None:
        super(CategoryDescDialog, self).__init__()
        self.categ_desc_dialog = Ui_CategoryDescEditDialog()
        self.categ_desc_dialog.setupUi(self)
        
        self.__list_item:QListWidgetItem = list_item
        
        self.text_edit_event_filter = CategoryDescTextEditEventFilter(
            self.categ_desc_dialog.te_category_desc
        )
        
        self.MAX_TEXT_LENGTH:int = 256 # longitud máxima que quiero que tenga 
            # el texto, así no ocupa tanto espacio en base de datos
        
        self.valid_category:bool = True
        
        self.setup_ui()
        self.setup_editor()
        self.setup_validators()
        self.setup_signals()
        return None
    
    
    def setup_ui(self) -> None:
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, True)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating, False)
        
        # configura los botones
        self.categ_desc_dialog.buttonBox.button(
            QDialogButtonBox.StandardButton.Save).setDefault(False)
        
        self.categ_desc_dialog.buttonBox.button(
            QDialogButtonBox.StandardButton.Save).setEnabled(False)
        self.categ_desc_dialog.buttonBox.button(
            QDialogButtonBox.StandardButton.Discard).setEnabled(True)
        
        return None
    
    
    def setup_editor(self) -> None:
        self.categ_desc_dialog.te_category_desc.setText(
            self.__list_item.toolTip() if self.__list_item.toolTip() else ""
        )
        
        # instala filtro de eventos en el textedit
        self.categ_desc_dialog.te_category_desc.installEventFilter(
            self.text_edit_event_filter
        )
        
        # coloca cantidad de caracteres en el label
        _text = self.categ_desc_dialog.te_category_desc.document(
            ).toPlainText()
        self.categ_desc_dialog.label_show_character_count.setText(
            self.categ_desc_dialog.label_show_character_count.text(
                ).replace("x", f"{len(_text)}")
        )
        
        self.categ_desc_dialog.te_category_desc.setAcceptRichText(False)
        self.categ_desc_dialog.te_category_desc.setAcceptDrops(False)
        self.categ_desc_dialog.te_category_desc.setAlignment(Qt.AlignmentFlag.AlignLeft)
        return None
    
    
    def setup_validators(self) -> None:
        self.categ_validator = CategoryDescValidator(
            MAX_LENGTH=self.MAX_TEXT_LENGTH,
            parent=self.categ_desc_dialog.te_category_desc
        )
        return None
    
    
    def setup_signals(self) -> None:
        # textedit
        self.categ_desc_dialog.te_category_desc.textChanged.connect(self.onTextChanged)
        
        self.text_edit_event_filter.focusedOut.connect(
            lambda: self.validateTextEdit(focus_out=True)
        )
        
        # botones
        self.categ_desc_dialog.buttonBox.button(
            QDialogButtonBox.StandardButton.Discard
        ).clicked.connect(self.close)
        self.categ_desc_dialog.buttonBox.button(
            QDialogButtonBox.StandardButton.Discard
        ).clicked.connect(self.reject)
        
        self.categ_desc_dialog.buttonBox.button(
            QDialogButtonBox.StandardButton.Save
        ).clicked.connect(self.onSaveClicked)
        return None
    
    
    @Slot()
    def onTextChanged(self) -> None:
        '''
        A medida que cambia el texto valida el contenido y actualiza el 
        **QLabel** que muestra los caracteres.
        '''
        self.validateTextEdit()
        self.__updateCharCountLabel( len(self.__getDocumentText()) )
        return None
    
    
    def __updateCharCountLabel(self, char_count:int) -> None:
        '''
        Actualiza el **QLabel** que muestra la cantidad de caracteres escritos 
        por el usuario y el máximo permitido.
        
        Parámetros
        ----------
        char_count : int
            cantidad de caracteres escritos por el usuario
        '''
        self.categ_desc_dialog.label_show_character_count.setText(
            f"cantidad de caracteres: {char_count}/{self.MAX_TEXT_LENGTH}"
        )
        return None
    
    
    @Slot(bool)
    def validateTextEdit(self, focus_out:bool=False) -> None:
        '''
        Valida el contenido del **QTextEdit** y formatea el texto para ignorar 
        caracteres no permitidos. Si el contenido es válido activa el botón 
        *Guardar* del **QDialog** sino lo desactiva.
        
        Parámetros
        ----------
        focus_out : bool, opcional
            flag que determina si el **QTextEdit** está fuera de foco, en ese 
            caso si es válido asigna el estilo por defecto.
        '''
        text:str = self.__getDocumentText()
        state, _, _ = self.categ_validator.validate(text, len(text))
        style:WidgetStyle
        
        match state:
            case QValidator.State.Acceptable:
                self.valid_category = True
                style = WidgetStyle.FIELD_VALID_VAL.value if not focus_out else ""
                
                self.categ_desc_dialog.te_category_desc.setStyleSheet(style)
            
            case QValidator.State.Invalid:
                self.valid_category = False
                style = WidgetStyle.FIELD_INVALID_VAL.value
                
                self.categ_desc_dialog.te_category_desc.setStyleSheet(
                    style
                )
                
                with QSignalBlocker(self.categ_desc_dialog.te_category_desc):
                    self.categ_desc_dialog.te_category_desc.setPlainText(
                        text[:-1] if len(text) <= self.MAX_TEXT_LENGTH else text[:self.MAX_TEXT_LENGTH]
                    )
                    self.categ_desc_dialog.te_category_desc.moveCursor(
                        QTextCursor.MoveOperation.End, QTextCursor.MoveMode.MoveAnchor
                    )
        
        self.__toggleSaveButton(field_valid=self.valid_category)
        return None
    
    
    def __getDocumentText(self) -> str:
        '''
        Obtiene el texto del documento del **QTextEdit** y lo devuelve como un 
        *str*.

        Retorna
        -------
        str
            el texto del documento interno del editor
        '''
        return self.categ_desc_dialog.te_category_desc.document().toPlainText()


    def __toggleSaveButton(self, field_valid:bool) -> None:
        '''
        Activa/desactiva el botón *Guardar* del **QDialog**.
        
        Parámetros
        ----------
        field_valid : bool, opcional
            flag que determina si el campo es válido, si lo es activa el botón 
            sino lo desactiva
        '''
        self.categ_desc_dialog.buttonBox.button(
            QDialogButtonBox.StandardButton.Save).setEnabled(field_valid)
        return None

    
    @Slot()
    def onSaveClicked(self) -> None:
        '''
        Obtiene la nueva descripción de la categoría y actualiza la base de 
        datos.
        Emite la señal *descriptionChanged* hacia **MainWindow** con la nueva 
        descripción.
        '''
        text:str = self.__getDocumentText()
        
        with DatabaseRepository() as db_repo:
            db_repo.updateRegisters(
                upd_sql= '''UPDATE Categorias 
                            SET descripcion = ? 
                            WHERE IDcategoria = (
                                SELECT IDcategoria 
                                FROM Categorias 
                                WHERE nombre_categoria = ?);''',
                upd_params=(text, self.__list_item.text(),)
            )
        
        self.descriptionChanged.emit(text)
        return None
    
    
    # eventos
    def keyPressEvent(self, event:QKeyEvent):
        match event.key():
            case Qt.Key.Key_Escape: # si se presiona "esc" se cierra 
                self.close()        # el dialog y se rechaza el input
                self.reject()
            
            case _:
                return super(CategoryDescDialog, self).keyPressEvent(event)
    
    
    def mousePressEvent(self, event:QMouseEvent):
        '''
        Sobreescribe el método *MousePressEvent* original.
        Captura los *clicks* fuera del **QTextEdit** y le quita el foco.
        '''
        if not self.categ_desc_dialog.te_category_desc.geometry().contains(event.pos()):
            self.categ_desc_dialog.te_category_desc.clearFocus()
            self.setFocus(Qt.FocusReason.MouseFocusReason)
        
        return super().mousePressEvent(event)


# TABLA VENTAS =================================================================================================


class SaleValues(QObject):
    '''
    Clase que contiene los valores de los campos de SaleDialog. El principal 
    uso de la clase es para "simular" un MODELO DE DATOS, ya que no usa 
    exactamente la misma metodología para guardar los datos, y al mismo tiempo 
    maneja mediante señales los cambios en los datos más relevantes.
    '''
    saleDetailChanged:Signal = Signal(str)
    productNameChanged:Signal = Signal(str)
    priceCheckboxEnabled:Signal = Signal(bool) # si se elige un producto que no tiene precio comercial 
        # esta señal notifica al dialog que debe desactivar la checkbox, sino la activa
    quantityChanged:Signal = Signal(float)
    priceTypeChanged:Signal = Signal(bool)
    totalCostChanged:Signal = Signal(float)
    totalPaidChanged:Signal = Signal(float)
    costIsDiffThanPaid:Signal = Signal(bool) # se emite para mostrar/esconder el frame de deudor en el dialog
    datetimeChanged:Signal = Signal(str)
    validityChanged:Signal = Signal() # se emite para activar/desactivar el botón 'Ok' del dialog
    debtorNameChanged:Signal = Signal(str)
    debtorSurnameChanged:Signal = Signal(str)
    
    
    def __init__(self) -> None:
        super(SaleValues, self).__init__()
        self.__sale_detail:str = ""
        self.__product_name:str = None
        self.__quantity:float = None
        self.__is_comercial_price:bool = False
        self.__total_cost:float = None
        self.__total_paid:float = None
        self.__datetime:str = ""
        
        # cuenta corriente
        self.__THERE_IS_DEBT:bool = False # flag que determina si en el dialog 'debtor_data' está 
            # activo o no, si lo está entonces se debe agregar a una cuenta corriente
        self.__debtor_name:str = None
        self.__debtor_surname:str = None
        
        # validez de datos
        self.__FIELDS_VALIDITY:dict[str, bool] = {
            SaleFields.PRODUCT_NAME.name: None,
            SaleFields.QUANTITY.name: None,
            SaleFields.TOTAL_PAID.name: None,
            SaleFields.DEBTOR_NAME.name: None,
            SaleFields.DEBTOR_SURNAME.name: None,
        }
        
        self.setup_signals()
        return None
    
    
    def setup_signals(self) -> None:
        self.productNameChanged.connect(self.setTotalCost)
        self.quantityChanged.connect(self.setTotalCost)
        self.priceTypeChanged.connect(self.setTotalCost)
        
        self.totalCostChanged.connect(
            lambda: self.setSaleDetail(sale_detail=None)
        )
        self.totalCostChanged.connect(self.isCostDifferentThanPaid)
        self.totalPaidChanged.connect(self.isCostDifferentThanPaid)
        return None
    
    
    # setters
    @Slot(str)
    def setSaleDetail(self, sale_detail:str=None) -> None:
        '''
        Guarda el detalle de la venta.

        Parámetros
        ----------
        sale_detail : str, opcional
            el nuevo detalle de la venta, si es None es porque se actualiza 
            de forma programática, sino es porque el usuario lo escribió
        '''
        price_type:str = "P. COMERCIAL" if self.__is_comercial_price else "P. PÚBLICO"
        _quantity:str = "..."
        _product_name:str = "..."
        new_sale_detail:str = None
        _pattern:Pattern
        
        match sale_detail:
            case None: # generado programáticamente
                _quantity = _quantity if not self.__quantity else self.__quantity
                _product_name = _product_name if not self.__product_name else self.__product_name
                self.__sale_detail = f"{_quantity} de {_product_name} ({price_type})"
            
            case _: # lo escribió el usuario
                _pattern = compile(
                    Regex.SALES_DETAILS_PRICE_TYPE.value,
                    flags=IGNORECASE)
                new_sale_detail = sub(
                    pattern=_pattern,
                    repl="",
                    string=sale_detail
                )
                new_sale_detail = f"{new_sale_detail.strip()} ({price_type})"
                self.__sale_detail = new_sale_detail
        
        self.saleDetailChanged.emit(self.__sale_detail)
        return None
    
    
    def setProductName(self, product_name:str) -> None:
        '''
        Guarda el nombre del producto.
        Éste método emite las siguientes señales:
        - 'productNameChanged' con el nuevo nombre
        - 'priceCheckboxEnabled' para notificar que el precio comercial está 
        o no disponible

        Parámetros
        ----------
        product_name : str
            el nuevo nombre de producto
        '''
        if self.__product_name != product_name:
            self.__product_name = product_name
            
            self.priceCheckboxEnabled.emit(
                self.__comercialPriceExists(self.__product_name)
            )
            self.productNameChanged.emit(self.__product_name)
        return None
    
    
    def __comercialPriceExists(self, product_name:str) -> bool:
        '''
        Determina si existe un precio comercial asociado al producto elegido.

        Parámetros
        ----------
        product_name : str
            el nombre de producto elegido

        Retorna
        -------
        bool
            True si el producto tiene precio comercial, sino False
        '''
        comerc_price:float|None|str # si None o str es porque no tiene precio comercial
        
        with DatabaseRepository() as db_repo:
            comerc_price = db_repo.selectRegisters(
                data_sql='''SELECT precio_comerc 
                            FROM Productos 
                            WHERE nombre = ?;''',
                data_params=(product_name,)
            )[0][0]
        
        return True if comerc_price else False
    
    
    def setQuantity(self, quantity:str) -> None:
        '''
        Guarda la cantidad. Emite la señal 'quantityChanged' con la nueva 
        cantidad.

        Parámetros
        ----------
        quantity : str
            la nueva cantidad del producto
        '''
        if self.__quantity != quantity:
            self.__quantity = quantity
            self.quantityChanged.emit(self.__quantity)
        return None
    
    
    def setPriceType(self, price_type:InventoryPriceType) -> None:
        '''
        Guarda el tipo de precio. Emite la señal 'priceTypeChanged' con el 
        nuevo tipo de precio.

        Parámetros
        ----------
        price_type : InventoryPriceType
            el nuevo tipo de precio
        '''
        match price_type:
            case InventoryPriceType.NORMAL:
                self.__is_comercial_price = False
            
            case InventoryPriceType.COMERCIAL:
                self.__is_comercial_price = True
        
        self.priceTypeChanged.emit(self.__is_comercial_price)
        return None
    
    
    def setDebtFlag(self, there_is_debt:bool) -> None:
        '''
        Actualiza el valor del flag interno del modelo que se usa para saber 
        qué valores es necesario validar.

        Parámetros
        ----------
        there_is_debt : bool
            flag que determina si hay diferencia entre el costo total y lo 
            abonado
        '''
        self.__THERE_IS_DEBT = there_is_debt
        return None
    
    
    def setDebtorName(self, debtor_name:str) -> None:
        '''
        Guarda el nombre del propietario de la cuenta corriente. Emite la 
        señal 'debtorNameChanged' con el nuevo nombre.

        Parámetros
        ----------
        debtor_name : str
            el nuevo nombre
        '''
        if self.__debtor_name != debtor_name:
            self.__debtor_name = debtor_name
            self.debtorNameChanged.emit(self.__debtor_name)
        return None
    
    
    def setDebtorSurname(self, debtor_surname:str) -> None:
        '''
        Guarda el apellido del propietario de la cuenta corriente. Emite la 
        señal 'debtorSurnameChanged' con el nuevo apellido.

        Parámetros
        ----------
        debtor_surname : str
            el nuevo apellido
        '''
        if self.__debtor_surname != debtor_surname:
            self.__debtor_surname = debtor_surname
            self.debtorSurnameChanged.emit(self.__debtor_surname)
        return None
    
    
    @Slot()
    def setTotalCost(self) -> None:
        '''
        Calcula el total a partir del precio del producto y la cantidad, y 
        emite la señal 'totalCostChanged'.
        
        Nota: El precio es obtenido desde la base de datos en este método.
        '''
        if self.isProductNameValid() and self.isQuantityValid():
            self.__total_cost = self.__getPrice()
        
        else:
            self.__total_cost = None
        
        self.totalCostChanged.emit(self.__total_cost)
        return None
    
    
    def __getPrice(self) -> float | None:
        '''
        Obtiene el precio correspondiente (comercial o normal) de la base de 
        datos y lo devuelve si existe.
        
        Retorna
        -------
        float | None
            será un float si el precio existe y es mayor a 0, sino None
        '''
        with DatabaseRepository() as db_repo:
            match self.getPriceType():
                # si el precio es comercial...
                case InventoryPriceType.COMERCIAL:
                        total_cost = db_repo.selectRegisters(
                            data_sql='''SELECT ? * precio_comerc 
                                        FROM Productos 
                                        WHERE nombre = ?;''',
                            data_params=(
                                self.__quantity,
                                self.__product_name,
                            )
                        )
                
                # si es normal...
                case InventoryPriceType.NORMAL:
                        total_cost = db_repo.selectRegisters(
                            data_sql='''SELECT ? * precio_unit 
                                        FROM Productos 
                                        WHERE nombre = ?;''',
                            data_params=(
                                self.__quantity,
                                self.__product_name,
                            )
                        )
        
        if total_cost:
            total_cost = total_cost[0][0]
        return total_cost if total_cost else None
    
    
    def setTotalPaid(self, total_paid:float) -> None:
        '''
        Guarda el valor de la cantidad abonada. Emite la señal 
        'totalPaidChanged'.

        Parámetros
        ----------
        total_paid : float
            el total abonado
        '''
        if self.__total_paid != total_paid:
            self.__total_paid = total_paid
            self.totalPaidChanged.emit(self.__total_paid)
        return None
    
    
    def setDatetime(self, datetime:QDateTime) -> None:
        '''
        Guarda la fecha y hora de la venta en formato str.

        Parámetros
        ----------
        datetime : QDateTime
            la fecha y hora de la venta
        '''
        self.__datetime = datetime.toString(DateAndTimeFormat.LOCAL_DATETIME_FORMAT.value)
        self.datetimeChanged.emit(self.__datetime)
        return None
    
    
    def setFieldValidity(self, field:SaleFields, validity:bool) -> None:
        '''
        Guarda el valor de verdad del campo especificado. Emite la señal 
        'validityChanged'.
        
        Parámetros
        ----------
        field : SaleFields
            campo al que asignarle el nuevo valor de verdad
        validity : bool
            nuevo valor de verdad del campo
        '''
        match field:
            case SaleFields.PRODUCT_NAME:
                self.__FIELDS_VALIDITY[SaleFields.PRODUCT_NAME.name] = validity
            
            case SaleFields.QUANTITY:
                self.__FIELDS_VALIDITY[SaleFields.QUANTITY.name] = validity
            
            case SaleFields.TOTAL_PAID:
                self.__FIELDS_VALIDITY[SaleFields.TOTAL_PAID.name] = validity
            
            case SaleFields.DEBTOR_NAME:
                self.__FIELDS_VALIDITY[SaleFields.DEBTOR_NAME.name] = validity
            
            case SaleFields.DEBTOR_SURNAME:
                self.__FIELDS_VALIDITY[SaleFields.DEBTOR_SURNAME.name] = validity
        
        self.validityChanged.emit()
        return None
    
    
    # getters
    def getSaleDetail(self) -> str:
        return self.__sale_detail
    
    
    def getProductName(self) -> str:
        return str(self.__product_name)
    
    
    def getQuantity(self) -> str:
        return str(self.__quantity)
    
    
    def getPriceType(self) -> InventoryPriceType:
        return InventoryPriceType.NORMAL if not self.__is_comercial_price else InventoryPriceType.COMERCIAL
    
    
    def getLocalDatetime(self) -> str:
        return str(self.__datetime)
    
    
    def getISO8601Datetime(self) -> str:
        # intenta convertir a formato ISO 8601...
        _dt = local_to_ISO8601(self.__datetime)
        return self.__datetime if not _dt else _dt
    
    
    def isProductNameValid(self) -> bool:
        '''
        Retorna un valor de verdad que determina la validez del nombre del 
        producto.

        Retorna
        -------
        bool
            validez del nombre del producto, será True si el nombre del 
            producto es válido, si no fue introducido retorna False
        '''
        return False if not self.__FIELDS_VALIDITY[SaleFields.PRODUCT_NAME.name] else True
    
    
    def isQuantityValid(self) -> bool:
        '''
        Retorna un valor de verdad que determina la validez de la cantidad.

        Retorna
        -------
        bool
            validez de la cantidad, True si es válida sino False
        '''
        return False if not self.__FIELDS_VALIDITY[SaleFields.QUANTITY.name] else True


    def thereIsDebt(self) -> bool:
        '''
        Devuelve el valor del flag interno de deuda.

        Retorna
        -------
        bool
            el valor del flag interno de deuda, que será True si hay 
            diferencia entre el costo total y lo abonado, sino False
        '''
        return self.__THERE_IS_DEBT
    

    def isAllValid(self) -> bool:
        '''
        Devuelve un valor de verdad que determina si todos los campos tienen 
        valores válidos. Éste método usa el valor del flag interno 
        '__THERE_IS_DEBT' para corroborar la validez de sólo los campos 
        necesarios.

        Retorna
        -------
        bool
            flag que determina si todos los campos son válidos
        '''
        pos_to_check:int = len(self.__FIELDS_VALIDITY.values())
        pos_to_check = pos_to_check if self.thereIsDebt() else pos_to_check - 2 # si no hay deuda no tiene 
            # en cuenta los campos de nombre y apellido del deudor.
        return all( list(self.__FIELDS_VALIDITY.values())[:pos_to_check] )


    @Slot()
    def isCostDifferentThanPaid(self) -> None:
        '''
        Verifica si el costo total es diferente a lo abonado y actualiza el 
        flag de deuda en el modelo.
        Emite la señal 'costIsDiffThanPaid'.
        '''
        if self.getTotalCost() != self.getTotalPaid():
            self.setDebtFlag(there_is_debt=True)
            self.costIsDiffThanPaid.emit(True)
        
        else:
            self.setDebtFlag(there_is_debt=False)
            self.costIsDiffThanPaid.emit(False)
            
        return None


    def getTotalCost(self) -> str | None:
        '''
        Retorna el costo total si existe como str, sino retorna None.
        La razón de retorna el costo como str es para poder agregarse el valor 
        directamente a un QCompleter sin necesidad de hacer type-casting.

        Retorna
        -------
        str | None
            si existe es el costo total como str, sino None
        '''
        return str(self.__total_cost) if self.__total_cost else None


    def getTotalPaid(self) -> str | None:
        '''
        Retorna el total abonado si existe como str, sino retorna None.

        Retorna
        -------
        str | None
            si existe es el costo total como str, sino None
        '''
        return str(self.__total_paid) if self.__total_paid else None


    def getDebtorName(self) -> str:
        return self.__debtor_name
    
    
    def getDebtorSurname(self) -> str:
        return self.__debtor_surname





# Dialog con datos de la venta -y del deudor si se debe algo/hay algo a favor-
class SaleDialog(QDialog):
    '''
    QDialog creado al presionar el botón 'MainWindow.btn_add_product_sales'. 
    Sirve para crear un nuevo registro de venta en la tabla "Ventas", de 
    detalles de venta en "Detalle_Ventas" y de deuda en "Deudas" (si hay 
    diferencia entre lo abonado y el costo total) en la base de datos.

    Éste QDialog, una vez presionado el botón "Aceptar", emite mediante la 
    señal 'dataFilled' un dict[str, Any] con los valores necesarios a 
    'MainWindow' para actualizar desde allí el MODELO DE DATOS de la tabla.
    '''
    minHeightChanged:Signal = Signal(int) # emite el nuevo minimumHeight, sirve para activar/desactivar el botón Ok.
    dataFilled:Signal = Signal(object) # emite un dict con todos los datos introducidos a MainWindow.
    
    def __init__(self):
        super(SaleDialog, self).__init__()
        self.saleDialog_ui = Ui_saleDialog()
        self.saleDialog_ui.setupUi(self)
        
        # pseudo-modelo de datos
        self.sale_values = SaleValues()

        # nombres y apellidos de cuentas corrientes
        self.DEBTORS_FULL_NAMES:dict[str, tuple[str]] = self.__getNameAndSurname()
        
        self.saleDialog_ui.cb_debtor_name.addItems(self.DEBTORS_FULL_NAMES.keys())
        self.saleDialog_ui.cb_debtor_name.setCurrentIndex(-1)
        self.saleDialog_ui.cb_debtor_surname.addItems(self.DEBTORS_FULL_NAMES.values())
        self.saleDialog_ui.cb_debtor_surname.setCurrentIndex(-1)
        
        self.setup_ui()
        
        self.setup_validators()
        
        self.setup_signals()
        
        #? por alguna razón, si desactivo antes el botón "Aceptar" no lo 
        #? desactiva, así que lo hago al final
        self.saleDialog_ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
        return None
    
    
    def setup_ui(self) -> None:
        '''
        Método que sirve para simplificar la lectura del método 'self.__init__'.
        Contiene inicializaciones y ajustes de algunos Widgets.
        
        
        '''
        self.setWindowTitle("Nueva venta")

        self.saleDialog_ui.buttonBox.button(QDialogButtonBox.Ok).setText("Aceptar")
        self.saleDialog_ui.buttonBox.button(QDialogButtonBox.Cancel).setText("Cancelar")
        
        self.__setInitialStyles()
        
        self.saleDialog_ui.comboBox_productName.addItems(getProductNames())
        
        with QSignalBlocker(self.saleDialog_ui.dateTimeEdit):
            self.saleDialog_ui.dateTimeEdit.setCalendarWidget(
                CustomCalendar(self.saleDialog_ui.dateTimeEdit)
            )
            self.saleDialog_ui.dateTimeEdit.setDateTime(
                QDateTime.currentDateTime()
            )
        
        self.sale_values.setDatetime(self.saleDialog_ui.dateTimeEdit.dateTime())

        # esconde widgets
        self.saleDialog_ui.label_productName_feedback.hide()
        self.saleDialog_ui.label_productQuantity_feedback.hide()
        self.saleDialog_ui.label_totalPaid_feedback.hide()

        # esconde los campos de datos del deudor        
        self.__setSaleDialogSize(
            min_width=SaleDialogDimensions.WIDTH.value,
            min_height=SaleDialogDimensions.HEIGHT_NO_DEBT.value,
            hide_debtor_data=True
        )
        return None
    
    
    def __setInitialStyles(self):
        '''
        Coloca íconos y establece stylesheets iniciales en los widgets.
        '''
        self.accept_icon = QIcon() # botón "Aceptar"
        self.cancel_icon = QIcon() # botón "Cancelar"
        
        # flecha del combobox
        self.saleDialog_ui.sale_data.setStyleSheet(WidgetStyle.DEF_COMBOBOX_ARROW_ICON.value)
        self.saleDialog_ui.debtor_data.setStyleSheet(WidgetStyle.DEF_COMBOBOX_ARROW_ICON.value)
        
        self.saleDialog_ui.buttonBox.setStyleSheet(WidgetStyle.DIALOG_CANCEL_BTN_STYLE.value)
        
        self.saleDialog_ui.dateTimeEdit.setStyleSheet(
            ''' QCalendarWidget QWidget#qt_calendar_prevmonth{
                    qproperty-icon: url(':/icons/prev-month.svg')
                }
                QCalendarWidget QWidget#qt_calendar_nextmonth{
                    qproperty-icon: url(':/icons/next-month.svg')
                }''')
        return None
    
    
    def setup_validators(self) -> None:
        # validadores de venta
        self.sale_detail_validator = SaleDetailsValidator(self.saleDialog_ui.lineEdit_saleDetail)
        self.quantity_validator = SaleQuantityValidator(self.saleDialog_ui.lineEdit_productQuantity)
        self.total_paid_validator = SalePaidValidator(self.saleDialog_ui.lineEdit_totalPaid)
        
        self.saleDialog_ui.lineEdit_saleDetail.setValidator(self.sale_detail_validator)
        self.saleDialog_ui.lineEdit_productQuantity.setValidator(self.quantity_validator)
        self.saleDialog_ui.lineEdit_totalPaid.setValidator(self.total_paid_validator)
        return None
    
    
    def __getNameAndSurname(self) -> dict[str, tuple[str]]:
        '''
        Obtiene los nombres y apellidos de cada cuenta corriente.

        Retorna
        -------
        dict[str, tuple[str]]
            diccionario con nombres como claves y tuplas de [apellido] como 
            valor de cada cuenta corriente
        '''
        full_name:list[tuple[str, str]]
        full_name_as_dict:dict[str, list[str]] = {}
        
        with DatabaseRepository() as db_repo:
            full_name = db_repo.selectRegisters(
                data_sql='''SELECT nombre, apellido 
                            FROM Deudores 
                            WHERE nombre <> "[ELIMINADO]" AND 
                              apellido <> "[ELIMINADO]";'''
            )
            
            for name, surname in full_name:
                if name in full_name_as_dict:
                    full_name_as_dict[name].append(surname)
                
                else:
                    full_name_as_dict[name] = [surname]
            
            [tuple(full_name_as_dict[name]) for name in full_name_as_dict.keys()]
        
        return full_name_as_dict
    
    
    def setup_signals(self) -> None:
        # detalles de venta
        self.saleDialog_ui.lineEdit_saleDetail.editingFinished.connect(
            lambda: self.sale_values.setSaleDetail(
                self.saleDialog_ui.lineEdit_saleDetail.text()
            )
        )
        self.sale_values.saleDetailChanged.connect(
            lambda sale_detail: self.saleDialog_ui.lineEdit_saleDetail.setText(sale_detail)
        )
        
        # combobox nombre de producto
        self.saleDialog_ui.comboBox_productName.currentIndexChanged.connect(
            self.validateProductNameField
        )
        
        # lineedit cantidad
        self.saleDialog_ui.lineEdit_productQuantity.editingFinished.connect(
            lambda: self.formatField(SaleFields.QUANTITY)
        )
        
        self.quantity_validator.validationSucceeded.connect(
            lambda: self.validatorOnValidationSucceded(SaleFields.QUANTITY)
        )
        self.quantity_validator.validationFailed.connect(
            lambda error_message: self.validatorOnValidationFailed(
                field_validated=SaleFields.QUANTITY,
                error_message=error_message
            )
        )
        
        # checkbox de tipo de precio
        self.sale_values.priceCheckboxEnabled.connect(self.onPriceCheckboxEnabled)
        self.saleDialog_ui.checkBox_comercialPrice.checkStateChanged.connect(
            self.onCheckboxChanged
        )
        
        # lineedit total pago
        self.saleDialog_ui.lineEdit_totalPaid.editingFinished.connect(
            lambda: self.formatField(SaleFields.TOTAL_PAID)
        )
        
        self.total_paid_validator.validationSucceeded.connect(
            lambda: self.validatorOnValidationSucceded(
                field_validated=SaleFields.TOTAL_PAID
            )
        )
        self.total_paid_validator.validationFailed.connect(
            lambda error_message: self.validatorOnValidationFailed(
                field_validated=SaleFields.TOTAL_PAID,
                error_message=error_message
            )
        )
        
        # datetimeedit
        self.saleDialog_ui.dateTimeEdit.dateTimeChanged.connect(self.sale_values.setDatetime)
        
        # señal de cambio de tamaño del dialog
        self.minHeightChanged.connect(self.toggleOkButton)
        
        # señales del pseudo-modelo de datos
        self.sale_values.totalCostChanged.connect(self.onTotalCostChanged)
        
        self.sale_values.validityChanged.connect(self.toggleOkButton)
        
        self.sale_values.costIsDiffThanPaid.connect(self.onCostIsDifferentThanPaid)
        
        self.sale_values.debtorNameChanged.connect(self.onDebtorNameChanged)
        
        # combobox nombre (cuenta corriente)
        self.saleDialog_ui.cb_debtor_name.currentTextChanged.connect(self.onDebtorNameTextChanged)
        
        # combobox apellido (cuenta corriente)
        self.saleDialog_ui.cb_debtor_surname.currentIndexChanged.connect(self.onDebtorSurnameIndexChanged)
        
        # botón Ok (Aceptar)
        self.saleDialog_ui.buttonBox.accepted.connect(self.handleOkClicked)
        return None
    
    
    @Slot(str)
    def validatorOnValidationSucceded(self, field_validated:SaleFields) -> None:
        '''
        Cambia el valor del flag asociado al campo que fue validado a True, 
        cambia el QSS del campo y esconde el QLabel asociado al campo.
        
        Parámetros
        ----------
        field_validated : SaleFields
            el campo validado, admite los siguientes valores:
            - SaleFields.QUANTITY: campo de cantidad del producto
            - SaleFields.TOTAL_PAID: campo de total abonado del producto
        '''
        match field_validated:
            case SaleFields.QUANTITY:
                self.sale_values.setFieldValidity(SaleFields.QUANTITY, True)
                self.sale_values.setQuantity(
                    quantity=self.saleDialog_ui.lineEdit_productQuantity.text().replace(",",".")
                )
                self.saleDialog_ui.lineEdit_productQuantity.setStyleSheet(WidgetStyle.FIELD_VALID_VAL.value)
                self.saleDialog_ui.label_productQuantity_feedback.hide()
            
            case SaleFields.TOTAL_PAID:
                self.sale_values.setFieldValidity(SaleFields.TOTAL_PAID, True)
                self.sale_values.setTotalPaid(self.saleDialog_ui.lineEdit_totalPaid.text().replace(",","."))
                
                self.saleDialog_ui.lineEdit_totalPaid.setStyleSheet(WidgetStyle.FIELD_VALID_VAL.value)
                self.saleDialog_ui.label_totalPaid_feedback.hide()
        return None
        
    
    @Slot(str, str)
    def validatorOnValidationFailed(self, field_validated:SaleFields, error_message:str) -> None:
        '''
        Cambia el valor del flag asociado al campo validado a False, cambia el 
        QSS del campo y muestra el QLabel asociado al campo con el mensaje 
        de error.
        
        Parámetros
        ----------
        field_validated : SaleFields
            el campo que se valida, admite los siguientes valores:
            - SaleFields.QUANTITY: campo de cantidad del producto
            - SaleFields.TOTAL_PAID: campo de total abonado del producto
        '''
        match field_validated:
            case SaleFields.QUANTITY:
                self.sale_values.setFieldValidity(field_validated, False)
                self.sale_values.setQuantity("")
                
                self.saleDialog_ui.lineEdit_productQuantity.setStyleSheet(WidgetStyle.FIELD_INVALID_VAL.value)
                # resetea el estilo del campo (por defecto es rojo, igual que los otros de feedback)
                self.saleDialog_ui.label_productQuantity_feedback.show()
                self.saleDialog_ui.label_productQuantity_feedback.setText(error_message)
            
            case SaleFields.TOTAL_PAID:
                self.sale_values.setFieldValidity(field_validated, False)
                
                self.saleDialog_ui.lineEdit_totalPaid.setStyleSheet(WidgetStyle.FIELD_INVALID_VAL.value)
                self.saleDialog_ui.label_totalPaid_feedback.show()
                self.saleDialog_ui.label_totalPaid_feedback.setText(error_message)
        return None


    @Slot()
    def validateProductNameField(self) -> None:
        '''
        Este método hace lo siguiente:
        1. actualiza la validez del campo
        2. esconde/muestra y cambia el texto de feedback
        3. cambia el estilo del QLabel de feedback asociado y del QComboBox
        4. coloca el stock disponible en 'label_productQuantity_feedback' con 
        un estilo personalizado
        5. si el campo es válido obtiene el stock del producto y lo guarda en 
        'SaleQuantityValidator.AVAILABLE_STOCK'
        6. si el campo es válido comprueba si también lo es la cantidad y de 
        ser ambos válidos llama a 'self.onFieldsChange'
        '''
        current_product:str
        
        # si no se eligió el nombre del producto asigna el índice -1
        if self.saleDialog_ui.comboBox_productName.currentText().strip() == "":
            self.saleDialog_ui.comboBox_productName.setCurrentIndex(-1)
        
        # si no hay un producto seleccionado (si índice es -1)...
        if self.saleDialog_ui.comboBox_productName.currentIndex() == -1:
            self.sale_values.setFieldValidity(SaleFields.PRODUCT_NAME, False)
            self.sale_values.setProductName("")
            self.saleDialog_ui.label_productName_feedback.show()
            self.saleDialog_ui.label_productName_feedback.setText(
                "El campo de nombre del producto no puede estar vacío"
            )
            self.saleDialog_ui.comboBox_productName.setStyleSheet(
                WidgetStyle.FIELD_INVALID_VAL.value
            )
        
        # si el campo es válido...
        else:
            current_product:str = self.saleDialog_ui.comboBox_productName.itemText(
                self.saleDialog_ui.comboBox_productName.currentIndex()
            )
            
            self.sale_values.setFieldValidity(SaleFields.PRODUCT_NAME, True)
            self.sale_values.setProductName(current_product)
            
            self.saleDialog_ui.label_productName_feedback.hide()
            self.saleDialog_ui.comboBox_productName.setStyleSheet(
                WidgetStyle.FIELD_VALID_VAL.value
            )
        return None


    @Slot(bool)
    def onPriceCheckboxEnabled(self, is_enabled:bool) -> None:
        '''
        Habilita/deshabita el QCheckBox de precio comercial si el producto 
        elegido tiene o no precio comercial

        Parámetros
        ----------
        is_enabled : bool
            flag que determina si activar o no el QCheckBox
        '''
        if not is_enabled:
            self.saleDialog_ui.checkBox_comercialPrice.setCheckState(
                Qt.CheckState.Unchecked
            )
        self.saleDialog_ui.checkBox_comercialPrice.setEnabled(is_enabled)
        return None
    
    
    @Slot(Qt.CheckState)
    def onCheckboxChanged(self, checkstate:Qt.CheckState) -> None:
        '''
        Actualiza el valor del estado del QCheckbox en el pseudo-modelo de 
        datos.

        Parámetros
        ----------
        checkstate : Qt.CheckState
            el nuevo estado del QCheckbox
        '''
        match checkstate:
            case Qt.CheckState.Checked:
                self.sale_values.setPriceType(InventoryPriceType.COMERCIAL)
            
            case Qt.CheckState.Unchecked:
                self.sale_values.setPriceType(InventoryPriceType.NORMAL)
        
        return None
    
    
    @Slot(str)
    def onSaleDetailChanged(self, sale_detail:str) -> None:
        '''
        Actualiza el detalle de la venta en el QLineEdit.

        Parámetros
        ----------
        sale_detail : str
            el nuevo detalle de venta
        '''
        self.saleDialog_ui.lineEdit_saleDetail.setText(sale_detail)
        return None
    
    
    @Slot()
    def onTotalCostChanged(self) -> None:
        '''
        Cambia el texto del QLabel de precio total y crea un QCompleter para 
        el campo de cantidad abonada.
        '''
        total_cost:str | None = self.sale_values.getTotalCost()
        total_paid_completer:QCompleter
        
        if total_cost:
            # coloca un completer en self.lineEdit_totalPaid
            total_cost = total_cost.replace(".",",")
            
            total_paid_completer = QCompleter([total_cost])
            total_paid_completer.setCompletionMode(
                QCompleter.CompletionMode.InlineCompletion
            )
            self.saleDialog_ui.lineEdit_totalPaid.setCompleter(
                total_paid_completer
            )
            
            self.saleDialog_ui.lineEdit_totalPaid.textChanged.connect(
                total_paid_completer.setCompletionPrefix
            )
            
            # actualiza el label de costo total
            self.saleDialog_ui.label_productTotalCost.setText(
                f'''<html>
                        <head/>
                        <body>
                            <p>
                                <span style={WidgetStyle.LABEL_RICHTEXT_NEUTRAL.value}>COSTO TOTAL </span>
                                <span style={WidgetStyle.LABEL_RICHTEXT_CONTENT.value}>$ {total_cost}</span>
                            </p>
                        </body>
                    </html>'''
            )
        return None
    
    
    @Slot()
    def onDebtorNameTextChanged(self, current_name:str) -> None:
        '''
        Reinicia los apellidos del QComboBox de apellidos y actualiza el nombre 
        de la cuenta corriente y su validez en SaleValues. Si el nombre no es 
        válido guarda una cadena vacía.
        
        Parámetros
        ----------
        current_name : str
            el nombre ingresado
        '''
        self.saleDialog_ui.cb_debtor_surname.clear()
        
        if current_name in self.DEBTORS_FULL_NAMES:
            self.sale_values.setDebtorName(debtor_name=current_name)
            self.sale_values.setFieldValidity(
                field=SaleFields.DEBTOR_NAME,
                validity=True
            )
        
        else:
            self.sale_values.setDebtorName(debtor_name='')
            self.sale_values.setFieldValidity(
                field=SaleFields.DEBTOR_NAME,
                validity=False
            )
        return None
    
    
    @Slot(str)
    def onDebtorNameChanged(self, debtor_name:str) -> None:
        '''
        Actualiza los datos del combobox de apellido para mostrar los apellidos 
        coincidentes.

        Parámetros
        ----------
        debtor_name : str
            el nombre ingresado
        '''
        if debtor_name:
            self.saleDialog_ui.cb_debtor_surname.addItems(
                self.DEBTORS_FULL_NAMES[debtor_name]
            )
        return None
    
    
    @Slot(int)
    def onDebtorSurnameIndexChanged(self, index:int) -> None:
        '''
        Actualiza el apeliido de la cuenta corriente y su validez en 
        SaleValues. Si el apellido no es válido guarda una cadena vacía.

        Parámetros
        ----------
        index : int
            el índice actual del QComboBox
        '''
        # si el índice es -1 es porque la combobox está vacía
        if index != -1:
            self.sale_values.setDebtorSurname(
                debtor_surname=self.saleDialog_ui.cb_debtor_surname.itemText(index)
            )
            self.sale_values.setFieldValidity(
                field=SaleFields.DEBTOR_SURNAME,
                validity=True)
        
        else:
            self.sale_values.setDebtorSurname(debtor_surname='')
            self.sale_values.setFieldValidity(
                field=SaleFields.DEBTOR_SURNAME,
                validity=False)
        return None


    @Slot(str)
    def formatField(self, field_to_format:SaleFields) -> None:
        '''
        Formatea el texto del campo y lo asigna nuevamente en el campo.
        
        Parámetros
        ----------
        field_to_format: SaleFields
            el campo a formatear, admite los siguientes valores:
            - SaleFields.QUANTITY: campo de cantidad del producto
            - SaleFields.TOTAL_PAID: campo de total abonado del producto
        '''
        field_text:str
        
        match field_to_format:
            case SaleFields.QUANTITY:
                field_text = self.saleDialog_ui.lineEdit_productQuantity.text()
                if field_text.endswith((",",".")):
                    field_text = field_text.rstrip(",")
                    field_text = field_text.rstrip(".")
                field_text = field_text.replace(".",",")
                self.saleDialog_ui.lineEdit_productQuantity.setText(field_text)
            
            case SaleFields.TOTAL_PAID:
                field_text = self.saleDialog_ui.lineEdit_totalPaid.text()
                if field_text.endswith((",",".")):
                    field_text = field_text.rstrip(",")
                    field_text = field_text.rstrip(".")
                field_text = field_text.replace(".",",")
                self.saleDialog_ui.lineEdit_totalPaid.setText(field_text)
        
        return None


    def toggleOkButton(self) -> None:
        '''
        Activa/desactiva el botón "Aceptar" dependiendo de si todos los campos 
        son válidos.
        '''
        if self.sale_values.isAllValid():
            self.saleDialog_ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)
        
        else:
            self.saleDialog_ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
        return None


    @Slot(bool)
    def onCostIsDifferentThanPaid(self, is_different:bool) -> None:
        '''
        Si hay diferencia entre el costo total y lo que abona el cliente éste 
        método amplía el QDialog y muestra campos para elegir la cuenta 
        corriente a la que asignar la diferencia.

        Parámetros
        ----------
        is_different : bool
            flag que determina si hay diferencia entre el costo total y lo 
            abonado
        '''
        match is_different:
            case True:
                self.__setSaleDialogSize(
                    min_width=SaleDialogDimensions.WIDTH.value,
                    min_height=SaleDialogDimensions.HEIGHT_WITH_DEBT.value,
                    hide_debtor_data=False
                )
            
            case False:
                self.__setSaleDialogSize(
                    min_width=SaleDialogDimensions.WIDTH.value,
                    min_height=SaleDialogDimensions.HEIGHT_NO_DEBT.value,
                    hide_debtor_data=True
                )
        return None
    
    
    def __setSaleDialogSize(self, min_width:int, min_height:int, hide_debtor_data:bool) -> None:
        '''
        Muestra/oculta 'debtor_data', declara el nuevo tamaño mínimo del 
        SaleDialog y redimensiona la ventana al tamaño.
        Emite la señal 'minHeightChanged'.
        '''
        self.setMinimumSize(min_width, min_height)
        
        self.resize(self.width(), self.minimumHeight())

        self.saleDialog_ui.debtor_data.setHidden(hide_debtor_data)
        # es importante habilitar 'debtor_data' porque sino no deja habilitar los widgets hijos
        self.saleDialog_ui.debtor_data.setEnabled(not hide_debtor_data)
        
        # antes de habilitar/deshabilitar los widgets, hay que habilitar 'debtor_data'
        self.saleDialog_ui.cb_debtor_name.setEnabled(not hide_debtor_data)
        self.saleDialog_ui.cb_debtor_surname.setEnabled(not hide_debtor_data)
        
        self.minHeightChanged.emit(self.minimumHeight())
        return None


    @Slot()
    def handleOkClicked(self) -> None:
        '''
        Hace las consultas INSERT a la base de datos con los valores 
        insertados, luego emite la señal 'dataFilled' con los valores que 
        necesita MainWindow para actualizar el MODELO DE DATOS de la tabla 
        de Ventas.
        NOTA: ni en éste dialog ni en la sección de la tabla de Ventas se 
        realizan UPDATES al stock de los productos.
        '''
        with DatabaseRepository() as db_repo:
            # Ventas
            db_repo.insertRegister(
                ins_sql= '''INSERT INTO Ventas(fecha_hora, detalles_venta) 
                            VALUES(?,?);''',
                ins_params=(
                    self.sale_values.getISO8601Datetime(),
                    self.sale_values.getSaleDetail()
                )
            )
           
            #? siempre se insertan datos en Ventas y Detalle_Ventas, pero si el 
            #? total abonado no es igual al "costo total" entonces se insertan 
            #? datos también en Deudas y Deudores...
            if self.sale_values.thereIsDebt():
                # Deudas
                db_repo.insertRegister(
                    ins_sql= '''INSERT INTO Deudas(
                                fecha_hora,
                                total_adeudado,
                                IDdeudor,
                                eliminado) 
                                VALUES(
                                    ?,
                                    ?,
                                    (SELECT IDdeudor 
                                        FROM Deudores 
                                        WHERE nombre = ? 
                                        AND apellido = ?), 
                                    0);''',
                    ins_params=(
                        self.sale_values.getISO8601Datetime(),
                        round(
                            float(self.sale_values.getTotalCost()) - float(self.sale_values.getTotalPaid()),
                            2
                        ),
                        self.sale_values.getDebtorName(),
                        self.sale_values.getDebtorSurname()
                        )
                )
                
                # Detalle_Ventas
                db_repo.insertRegister(
                    ins_sql= '''INSERT INTO Detalle_Ventas(
                                    cantidad,
                                    costo_total,
                                    IDproducto, 
                                    IDventa,
                                    abonado,
                                    IDdeuda) 
                                VALUES(
                                    ?,
                                    ?,
                                    (SELECT IDproducto 
                                     FROM Productos 
                                     WHERE nombre = ?),
                                    (SELECT IDventa 
                                     FROM Ventas 
                                     WHERE fecha_hora = ? 
                                     AND detalles_venta = ?),
                                    ?,
                                    (SELECT IDdeuda 
                                        FROM Deudas 
                                        WHERE fecha_hora = ? 
                                        AND IDdeudor = (
                                            SELECT IDdeudor 
                                            FROM Deudores 
                                            WHERE nombre = ? 
                                            AND apellido = ?))
                                    );''',
                    ins_params=(
                        float(self.sale_values.getQuantity()),
                        float(self.sale_values.getTotalCost()),
                        self.sale_values.getProductName(),
                        self.sale_values.getISO8601Datetime(),
                        self.sale_values.getSaleDetail(),
                        float(self.sale_values.getTotalPaid()),
                        self.sale_values.getISO8601Datetime(),
                        self.sale_values.getDebtorName(),
                        self.sale_values.getDebtorSurname()
                    )
                )
            
            # si lo abonado es igual al total...
            else:
                # Detalle_Ventas
                db_repo.insertRegister(
                    ins_sql= '''INSERT INTO Detalle_Ventas(
                                    cantidad,
                                    costo_total,
                                    IDproducto,
                                    IDventa,
                                    abonado,
                                    IDdeuda)
                                VALUES(
                                    ?,
                                    ?,
                                    (SELECT IDproducto 
                                     FROM Productos 
                                     WHERE nombre = ?),
                                    (SELECT IDventa 
                                     FROM Ventas 
                                     WHERE fecha_hora = ? 
                                     AND detalles_venta = ?),
                                    ?,
                                    NULL);''',
                ins_params=(
                    float(self.sale_values.getQuantity()),
                    float(self.sale_values.getTotalCost()),
                    self.sale_values.getProductName(),
                    self.sale_values.getISO8601Datetime(),
                    self.sale_values.getSaleDetail(),
                    float(self.sale_values.getTotalPaid())
                    )
                )
            
            # self.__emitDataFilled(values=values)
        
        self.__emitDataFilled()
        return None
    
    
    def __emitDataFilled(self) -> None:
        '''
        Convierte los datos recibidos en un diccionario y los emite por medio 
        de la señal 'dataFilled' a MainWindow para, desde ahí, actualizar el 
        MODELO DE DATOS.
        '''
        values_to_dict:dict[str, Any] = {}
        
        with DatabaseRepository() as db_repo:
            values_to_dict = {
                'IDsale_detail': db_repo.selectRegisters(
                    data_sql='''SELECT ID_detalle_venta 
                                FROM Detalle_Ventas 
                                ORDER BY ID_detalle_venta DESC 
                                LIMIT 1;''')[0][0],
                'sale_detail': self.sale_values.getSaleDetail(),
                'product_quantity': float(self.sale_values.getQuantity()),
                'product_measurement_unit': db_repo.selectRegisters(
                    data_sql='''SELECT 
                                COALESCE(unidad_medida, '')
                                FROM Productos 
                                WHERE nombre = ?;''',
                    data_params=(self.sale_values.getProductName(),) )[0][0],
                'product_name': self.sale_values.getProductName(),
                'total_cost': float(self.sale_values.getTotalCost()),
                'total_paid': float(self.sale_values.getTotalPaid()),
                'datetime': self.sale_values.getLocalDatetime(),
            }
        
        self.dataFilled.emit(values_to_dict)
        return None


# FORMULARIO VENTAS ============================================================================================


# TODO: HACER QUE SE PUEDA INGRESAR EL PRECIO PAGADO, Y DE AHÍ QUE SE CALCULE LA CANTIDAD DEL PRODUCTO (en lugar de hacer que la cantidad sea la única forma 
# todo: de ingresar el dato de cuánto lleva... es decir, que se pueda ingresar la cantidad ó el total de lo que lleva de ese producto y se calcule el otro 
# todo: campo, respectivamente)
# valores de los campos de ListItemWidget
class ListItemValues(QObject):
    '''
    Clase que contiene los valores de los campos de ListItemWidget. El principal 
    uso de la clase es para "simular" un MODELO DE DATOS, ya que no usa exactamente 
    la misma metodología para guardar los datos, y al mismo tiempo maneja mediante 
    señales los cambios en los datos más relevantes.
    '''
    productNameChanged:Signal = Signal(str) # emite el nuevo nombre.
    quantityChanged:Signal = Signal(float) # emite la nueva cantidad.
    priceTypeChanged:Signal = Signal(object) # emite el nuevo tipo de precio como 'InventoryPriceType'.
    subtotalChanged:Signal = Signal(object) # emite el nuevo subtotal, que puede ser float 
                                            # ó None (None si es inválido o no fue calculado).
    saleDetailsChanged:Signal = Signal(str) # emite el nuevo detalle de la venta.
    
    
    def __init__(self, object_name:str):
        super(ListItemValues, self).__init__()
        
        self.object_name:str = object_name
        self.__product_id:int = None
        
        self.__product_name:str = None
        self.__quantity:int = None
        self.__subtotal:float = None
        
        self.__is_comercial_price:bool = self.setPriceType()
        self.__sale_details:str = ''
        
        # validez de los datos
        self.__FIELDS_VALIDITY:dict[str, bool | None] = { #? guarda valores True | False | None, siendo el valor de verdad 
            SaleFields.PRODUCT_NAME.value: None, #? en realidad triestado, True y False representan la validez del 
            SaleFields.QUANTITY.value: None      #? del valor en el campo, si es None es porque está vacío el campo.
        }
        
        #* señales
        self.productNameChanged.connect(self.setSubtotal)
        self.quantityChanged.connect(self.setSubtotal)
        self.priceTypeChanged.connect(self.setSubtotal)
        self.subtotalChanged.connect(lambda: self.setSaleDetails(curr_sale_detail=self.__sale_details))
        
        return None
    
    
    # setters
    def setProductId(self, product_id:int=None) -> None:
        '''
        Guarda el IDproducto.
        
        Parámetros
        ----------
        product_id : int, opcional
            IDproducto del producto, por defecto es None
        
        
        '''
        self.__product_id = product_id
        return None
    
    
    def setProductName(self, product_name:str=None) -> None:
        '''
        Guarda el nombre del producto, actualiza el IDproducto actual y emite 
        la señal 'productNameChanged' si el nombre del producto cambió.
        
        Parámetros
        ----------
        product_name : str, opcional
            nombre del producto, por defecto es None
        
        
        '''
        self.__product_name = product_name
        self.__onProductNameChange(product_name)
        
        return None
    
    
    def __onProductNameChange(self, product_name:str=None) -> None:
        '''
        Actualiza el IDproducto actual y emite la señal 'productNameChanged' 
        si el nombre del producto cambió.
        
        Parámetros
        ----------
        product_name : str, opcional
            nombre del producto, por defecto es None
        
        
        '''
        # actualiza el IDproducto
        with DatabaseRepository() as db_repo:
            self.setProductId(
                db_repo.selectRegisters(
                    data_sql='''SELECT IDproducto 
                                FROM Productos 
                                WHERE nombre = ?;''',
                    data_params=(product_name,)
                )[0][0]
            )
        
        # emite el nombre de producto
        self.productNameChanged.emit(product_name)
        return None
    
    
    def setQuantity(self, quantity:float=None) -> None:
        '''
        Guarda la cantidad y emite la señal 'quantityChanged' si la cantidad 
        cambió.
        
        Parámetros
        ----------
        quantity : float, opcional
            cantidad del producto, por defecto es None
        
        
        '''
        self.__quantity = quantity
        self.quantityChanged.emit(quantity)
        return None
    
    
    @Slot()
    def setSubtotal(self) -> None:
        '''
        Calcula el subtotal a partir del precio del producto y la cantidad, y 
        emite la señal 'subtotalChanged'.
        Nota: El precio es obtenido desde la base de datos en este método.
        
        
        '''
        self.__subtotal = None if not self.isAllValid() else self.__getPrice()
        
        self.subtotalChanged.emit(self.__subtotal)
        return None
    
    
    def __getPrice(self) -> float | None:
        '''
        Obtiene el precio correspondiente (comercial o normal) de la base de 
        datos y lo devuelve si existe.
        
        Retorna
        -------
        float | None
            será un float si el precio existe y es mayor a 0, sino None
        '''
        with DatabaseRepository() as db_repo:
            match self.isComercialPrice():
                # si el precio es comercial...
                case True:
                        total_cost = db_repo.selectRegisters(
                            data_sql='''SELECT ? * precio_comerc 
                                        FROM Productos 
                                        WHERE nombre = ?;''',
                            data_params=(
                                self.__quantity,
                                self.__product_name,
                            )
                        )
                
                # si es normal...
                case False:
                        total_cost = db_repo.selectRegisters(
                            data_sql='''SELECT ? * precio_unit 
                                        FROM Productos 
                                        WHERE nombre = ?;''',
                            data_params=(
                                self.__quantity,
                                self.__product_name,
                            )
                        )
        
        if total_cost:
            total_cost = total_cost[0][0]
        return total_cost if total_cost else None
    
    
    def setPriceType(self, price_type:InventoryPriceType=InventoryPriceType.NORMAL) -> None:
        '''
        Guarda el tipo de precio del producto y emite la señal 'priceTypeChanged'.
        
        Parámetros
        ----------
        price_type : InventoryPriceType, opcional
            tipo de precio del producto, por defecto es NORMAL
        
        
        '''
        self.__is_comercial_price = False if price_type == InventoryPriceType.NORMAL else True
        self.priceTypeChanged.emit(price_type)
        return None
    
    
    @Slot(object)
    def setSaleDetails(self, curr_sale_detail:str) -> None:
        '''
        Guarda el detalle de la venta y emite la señal 'saleDetailsChanged'.
        
        Parámetros
        ----------
        curr_sale_detail : str
            el detalle de la venta actual, sobre el que se hacen cambios si no 
            fue modificado por el usuario
        
        
        '''
        pattern:Pattern = compile(pattern=Regex.SALES_DETAILS_FULL.value, flags=IGNORECASE)
        new_text:str
        
        price_type:str = "P. COMERCIAL" if self.isComercialPrice() else "P. PÚBLICO"

        if self.isAllValid():
            # si el patrón coincide reemplaza el texto (significa que no lo escribió 
            # el usuario)
            if fullmatch(pattern, curr_sale_detail) or curr_sale_detail.strip() == "":
                self.__sale_details = f"{self.getQuantity()} de {self.getProductName()} ({price_type})"
            
            # si no coincide es porque lo escribió el usuario (sólo reemplaza el tipo de precio)
            else:
                new_text = curr_sale_detail
                new_text = sub(
                    pattern=Regex.SALES_DETAILS_PRICE_TYPE.value,
                    repl="",
                    string=curr_sale_detail,
                    flags=IGNORECASE)
                new_text = f"{new_text.strip()} ({price_type})"
                
                self.__sale_details = new_text
            
            self.saleDetailsChanged.emit(self.__sale_details)
        return None
    
    
    def setFieldValidity(self, field:SaleFields, validity:bool) -> None:
        '''
        Guarda el valor de verdad del campo especificado.
        
        Parámetros
        ----------
        field : SaleFields
            campo al que asignarle el nuevo valor de verdad, debe ser 
            'SaleFields.PRODUCT_NAME' ó 'SaleFields.QUANTITY'
        validity : bool | None
            nuevo valor de verdad del campo
        
        
        '''
        match field:
            case SaleFields.PRODUCT_NAME:
                self.__FIELDS_VALIDITY[SaleFields.PRODUCT_NAME.value] = validity
            
            case SaleFields.QUANTITY:
                self.__FIELDS_VALIDITY[SaleFields.QUANTITY.value] = validity
        
        return None
    
    
    # getters
    def getProductId(self) -> int | None:
        '''
        Devuelve el IDproducto.

        Retorna
        -------
        int | None
            el valor será int si existe, sino None
        '''
        return self.__product_id
    
    
    def getProductName(self) -> str | None:
        '''
        Devuelve el nombre del producto.

        Retorna
        -------
        str | None
            el valor será str si existe, sino None
        '''
        return self.__product_name
    
    
    def getQuantity(self) -> float | None:
        '''
        Devuelve la cantidad.

        Retorna
        -------
        float | None
            el valor será float si existe, sino None
        '''
        return self.__quantity
    
    
    def getSubtotal(self) -> float | None:
        '''
        Devuelve el subtotal de la compra actual.

        Retorna
        -------
        float | None
            el valor será float si existe, sino None
        '''
        return self.__subtotal
    
    
    def isComercialPrice(self) -> bool:
        '''
        Devuelve un valor de verdad que determina si el precio a cobrar es 
        comercial.

        Retorna
        -------
        bool
            devuelve True si es comercial, en cualquier otro caso False
        '''
        return True if self.__is_comercial_price else False
    
    
    def getSaleDetails(self) -> str:
        '''
        Devuelve el detalle de la venta.

        Retorna
        -------
        str
        '''
        return self.__sale_details
    
    
    def isNameValid(self) -> bool | None:
        '''
        Devuelve True | False dependiendo de si el campo de nombre del producto 
        es válido o no.

        Retorna
        -------
        bool | None
            valor de verdad del campo de nombre del producto, si es None es 
            porque el nombre del producto aún no fue validado
        '''
        return self.__FIELDS_VALIDITY[SaleFields.PRODUCT_NAME.value]
    
    
    def isQuantityValid(self) -> bool | None:
        '''
        Devuelve True | False dependiendo de si el campo de cantidad del producto 
        es válido o no.

        Retorna
        -------
        bool | None
            valor de verdad del campo de cantidad, si es None es porque la 
            cantidad del producto aún no fue validada
        '''
        return self.__FIELDS_VALIDITY[SaleFields.QUANTITY.value]
    
    
    def isAllValid(self) -> bool:
        '''
        Devuelve un valor de verdad que determina si ambos valores (el nombre 
        y la cantidad) son válidos.

        Retorna
        -------
        bool
            será True sólo si ambos valores son válidos, sino False
        '''
        return all(self.__FIELDS_VALIDITY.values())
    
    
    def getValues(self) -> dict[str, Any]:
        '''
        Devuelve todos los valores del producto actual.

        Retorna
        -------
        dict[str, Any]
            diccionario con los nombre de los campos con sus respectivos 
            valores
        '''
        return {
            SaleFields.PRODUCT_ID.name: self.getProductId(),
            SaleFields.PRODUCT_NAME.name: self.getProductName(),
            SaleFields.QUANTITY.name: self.getQuantity(),
            SaleFields.SUBTOTAL.name: self.getSubtotal(),
            SaleFields.IS_COMERCIAL_PRICE.name: self.isComercialPrice(),
            SaleFields.SALE_DETAILS.name: self.getSaleDetails(),
            SaleFields.IS_ALL_VALID.name: self.isAllValid()
        }
    
    
    def __repr__(self) -> str:
        return f'''[ID {self.__product_id}]{self.object_name}: \
            \n\tproduct_name: {self.__product_name}\
            \tquantity: {self.__quantity}\
            \tsubtotal: {self.__subtotal}\
            \n\tis_comercial_price: {self.__is_comercial_price}\
            \n\tsale_details: {self.__sale_details}\
            \n\tall_valid: {self.isAllValid()}'''





# item de tipo widget de la lista del formulario de Ventas
class ListItemWidget(QWidget):
    '''
    Item creado dinámicamente dentro de la lista de formulario de ventas 
    'MainWindow.sales_input_list'. Sirve para seleccionar un producto, 
    la cantidad vendida, el tipo de precio (comercial o normal) y darle 
    alguna descripción a la venta.
    '''
    fieldsValuesChanged = Signal(object) # emite un dict[SaleFields, Any] 
                                         # con todos los valores de los campos.
    deleteItem = Signal(str) # emite el 'objectName' del item.
    
    def __init__(self, obj_name:str):
        super(ListItemWidget, self).__init__()
        self.listItem = Ui_listProduct()
        self.listItem.setupUi(self)
        
        self.setup_ui(obj_name=obj_name)
        
        self.field_values:ListItemValues = ListItemValues(object_name=self.objectName())
        
        self.setup_validators()
        
        self.setup_signals()
        return None


    def setup_ui(self, obj_name:str) -> None:
        '''
        Método que sirve para simplificar la lectura del método 'self.__init__'.
        Contiene inicializaciones y ajustes de algunos Widgets.
        
        Parámetros
        ----------
        obj_name : str
            nombre único del objecto actual, a modo de identificador
        
        
        '''
        # desactiva checkBox_comercialPrice
        self.listItem.checkBox_comercialPrice.setEnabled(False)
        
        # coloca el objectName
        self.setObjectName(obj_name)
        
        # esconde labels de feedback
        self.listItem.label_nameFeedback.hide()
        self.listItem.label_quantityFeedback.hide()
        
        self.__setInitialStyles()
        
        # lleno el combobox de nombres
        self.listItem.comboBox_productName.addItems(getProductNames())
        self.listItem.comboBox_productName.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
        return None
    
    
    def __setInitialStyles(self):
        '''
        Coloca íconos y establece stylesheets iniciales en los widgets.
        '''
        # asigno el ícono para el botón de borrar el item actual
        self.listItem.btn_deleteCurrentProduct.setIcon(QIcon(":/icons/close.svg"))
        self.listItem.btn_deleteCurrentProduct.setIconSize(QSize(32, 32))
        return None
    
    
    def setup_validators(self) -> None:
        self.quantity_validator = SaleQuantityValidator(self.listItem.lineEdit_productQuantity)
        self.sale_detail_validator = SaleDetailsValidator(self.listItem.lineEdit_saleDetail)
        self.listItem.lineEdit_saleDetail.setValidator(self.sale_detail_validator)
        self.listItem.lineEdit_productQuantity.setValidator(self.quantity_validator)
        
        return None
    
    
    def setup_signals(self) -> None:
        '''
        Al igual que los métodos 'self.setup_ui', este método tiene el objeto 
        de simplificar la lectura del método 'self.__init__'.
        Contiene las declaraciones de señales/slots de Widgets ya existentes 
        desde la instanciación de 'MainWindow'.
        
        
        '''
        #--- SEÑALES --------------------------------------------------
        # nombre de producto
        self.listItem.comboBox_productName.currentIndexChanged.connect(self.onComboboxIndexChange)
        
        # cantidad de producto
        self.listItem.lineEdit_productQuantity.editingFinished.connect(self.onQuantityEditingFinished)
        
        self.quantity_validator.validationSucceeded.connect(self.validatorOnValidationSucceded)
        self.quantity_validator.validationFailed.connect(self.validatorOnValidationFailed)
        
        # checkbox tipo de precio
        self.listItem.checkBox_comercialPrice.checkStateChanged.connect(self.onCheckStateChange)
        
        # cambios en el detalle de venta
        self.listItem.lineEdit_saleDetail.editingFinished.connect(
            lambda: self.onSaleDetailEdit(
                text=self.listItem.lineEdit_saleDetail.text()
            )
        )
        
        # cambios en ListItemValues
        self.field_values.subtotalChanged.connect(self.onSubtotalChanged)
        self.field_values.saleDetailsChanged.connect(self.onSaleDetailsChange)
        
        self.field_values.subtotalChanged.connect(self.onFieldValuesChanged)
        self.field_values.saleDetailsChanged.connect(self.onFieldValuesChanged)
        
        # botón borrar elemento
        self.listItem.btn_deleteCurrentProduct.clicked.connect(self.deleteCurrentItem)
        return None
    
    
    #### MÉTODOS #####################################################
    #* eliminar el item actual
    @Slot()
    def deleteCurrentItem(self) -> None:
        '''
        Emite la señal 'deletedItem' al QListWidget 'MainWindow.sales_input_list' 
        para eliminar éste item de la lista.
        '''
        self.deleteItem.emit(self.objectName())
        self.deleteLater()
        return None


    #* validación
    @Slot(str)
    def validatorOnValidationSucceded(self) -> None:
        '''
        Si además el nombre es válido, cambia el valor del flag asociado al 
        campo de cantidad a True y cambia el QSS del campo.
        NOTA: redimensiona 'ListItemWidget' para que se pueda mostrar el mensaje 
        correctamente.
        '''
        _avail_stock:tuple[float, str] # stock disponible
        
        # actualiza la validez y la cantidad
        self.field_values.setFieldValidity(SaleFields.QUANTITY, True)
            
        # cambia el estilo de los campos
        self.listItem.lineEdit_productQuantity.setStyleSheet(
            WidgetStyle.FIELD_VALID_VAL.value
        )
        
        if self.field_values.isNameValid():
            # actualiza el mensaje de stock
            _avail_stock = self.quantity_validator.getAvailableStock()
            self.listItem.label_quantityFeedback.setText(f"stock disponible: {_avail_stock[0]} {_avail_stock[1]}")
            
        # cambia los estilos del label y el lineedit
        self.listItem.label_quantityFeedback.setStyleSheet(WidgetStyle.LABEL_NEUTRAL_VAL.value)
        self.listItem.lineEdit_productQuantity.setStyleSheet(WidgetStyle.FIELD_VALID_VAL.value)
        
        # si no hay mensaje de stock disponible en el label lo pone en blanco
        if not "stock disponible" in self.listItem.label_quantityFeedback.text():
            self.listItem.label_quantityFeedback.setStyleSheet("")
            self.listItem.label_quantityFeedback.hide()
        
        # ajusta el tamaño del label
        self.listItem.label_quantityFeedback.adjustSize()
        
        return None
        
    
    @Slot(str)
    def validatorOnValidationFailed(self, error_message:str) -> None:
        '''
        Actualiza la cantidad dentro de 'ListItemValues' y cambia el valor del 
        flag asociado al campo de cantidad a False, muestra el mensaje de 
        error en el QLabel asociado al campo con feedback y cambia su estilo.
        
        Parámetros
        ----------
        error_message : str
            mensaje de error para mostrar al usuario
        
        
        '''
        self.field_values.setFieldValidity(SaleFields.QUANTITY, False)
        
        # actualiza la cantidad aunque sea el valor inválido
        self.field_values.setQuantity(
            self.listItem.lineEdit_productQuantity.text().replace(",",".")
        )
        
        self.listItem.lineEdit_productQuantity.setStyleSheet(
            WidgetStyle.FIELD_INVALID_VAL.value
        )
        self.listItem.label_quantityFeedback.show()
        
        # resetea el estilo del campo (por defecto es rojo, igual que los otros de feedback)
        self.listItem.label_quantityFeedback.setStyleSheet("")
        self.listItem.label_quantityFeedback.setText(error_message)
        
        return None


    #* combobox de nombre
    @Slot()
    def onComboboxIndexChange(self) -> None:
        '''
        Valida el campo de nombre de producto y si es válido actualiza el stock 
        en el validador de cantidad y lo muestra.
        Si ambos campos (nombre de producto y cantidad) son válidos, actualiza 
        el detalle de venta o el precio dependiendo del tipo de precio 
        seleccionado, y también actualiza 'field_values' con el nombre.
        
        
        '''
        # si no hay un producto seleccionado...
        if self.listItem.comboBox_productName.currentIndex() == -1:
            self.field_values.setFieldValidity(SaleFields.PRODUCT_NAME, False)
            
            self.listItem.label_nameFeedback.show()
            self.listItem.label_nameFeedback.setText("Se debe seleccionar un producto")
            self.listItem.comboBox_productName.setStyleSheet(
                WidgetStyle.FIELD_INVALID_VAL.value
            )
        
        # si el campo es válido...
        else:
            self.field_values.setFieldValidity(SaleFields.PRODUCT_NAME, True)
            
            self.listItem.label_nameFeedback.hide()
            self.listItem.comboBox_productName.setStyleSheet(
                WidgetStyle.FIELD_VALID_VAL.value
            )
            
            self.__onValidProductName(
                curr_name=self.listItem.comboBox_productName.itemText(
                    self.listItem.comboBox_productName.currentIndex()
                )
            )
        
        return None
    
    
    def __onValidProductName(self, curr_name:str) -> None:
        '''
        si el nombre del producto elegido es válido actualiza el stock en el 
        validador de cantidad y lo muestra y también coloca la unidad de medida
        en el label de cantidad.
        Si ambos campos (nombre de producto y cantidad) son válidos, actualiza 
        el detalle de venta o el precio dependiendo del tipo de precio 
        seleccionado, y también actualiza 'field_values' con el nombre.
        
        Parámetros
        ----------
        curr_name : str
            nombre actual del combobox
        '''
        # actualiza el stock disponible en el validador de cantidad...
        self.__updateAvailableStock()
        # ...y muestra el stock disponible
        self.__showAvailableStock()
        
        # muestra también la unidad de medida al lado del lineedit de cantidad
        self.listItem.label_productMeasurementUnit.setText(
            getCurrentProductStock(
                product_name=self.listItem.comboBox_productName.itemText(
                    self.listItem.comboBox_productName.currentIndex()
                )
            )[1]
        )
        
        #? llama a validar la cantidad porque, si se modificó primero la 
        #? cantidad y es válida, y luego se elige un nombre de producto 
        #? que es válido pero no tiene esa cantidad en stock entonces el 
        #? campo de cantidad devuelve un "falso positivo"... así se arregla
        self.quantity_validator.validate(
            self.listItem.lineEdit_productQuantity.text(),
            0
        )
        
        # habilita/deshabilita el checkbox de precio comercial
        self.__toggleCheckboxOnProductName(curr_name=curr_name)
        
        # actualiza 'self.field_values' con el nombre
        self.field_values.setProductName(product_name=curr_name)
        
        return None


    def __updateAvailableStock(self) -> None:
        '''
        Actualiza el stock disponible en el validador de cantidad a partir del 
        producto seleccionado.
        '''
        self.quantity_validator.setAvailableStock(
                getCurrentProductStock(
                    self.listItem.comboBox_productName.itemText(
                        self.listItem.comboBox_productName.currentIndex()
                    )
                )
            )
        return None


    def __showAvailableStock(self) -> None:
        '''
        Muestra el stock disponible en un label debajo de la cantidad vendida.
        '''
        # coloca el stock en 'label_quantityFeedback'
        self.listItem.label_quantityFeedback.show()
        self.listItem.label_quantityFeedback.setStyleSheet(
            WidgetStyle.LABEL_NEUTRAL_VAL.value
        )
        self.listItem.label_quantityFeedback.setText(
            "El stock disponible es de {} {}".format(
                self.quantity_validator.AVAILABLE_STOCK[0], self.quantity_validator.AVAILABLE_STOCK[1]
            )
        )
        return None


    def __toggleCheckboxOnProductName(self, curr_name:str) -> None:
        '''
        activa/desactiva el checkbox de precio comercial dependiendo de 
        si el producto actualmente seleccionado tiene un precio comercial 
        o no.

        Parámetros
        ----------
        curr_name : str
            nombre de producto seleccionado
        '''
        registers:Any
        
        with DatabaseRepository() as db_repo:
            # obtiene el precio comercial
            registers = db_repo.selectRegisters(
                data_sql='''SELECT precio_comerc 
                            FROM Productos 
                            WHERE nombre = ?;''',
                data_params=(curr_name,)
            )[0][0]
            
            # la desmarca
            self.listItem.checkBox_comercialPrice.setChecked(False)
            
            # si no es un valor NULO (0, 0.0, None, etc...) activa el checkbox
            if registers:
                self.listItem.checkBox_comercialPrice.setEnabled(True)
            
            # sino lo desactiva
            else:
                self.listItem.checkBox_comercialPrice.setEnabled(False)
                self.field_values.setPriceType(InventoryPriceType.NORMAL)

        return None
    

    #* checkbox de tipo de precio
    def onCheckStateChange(self, state:Qt.CheckState) -> None:
        '''
        Actualiza el valor de 'field_values.is_comercial_price' con el nuevo 
        estado de la checkbox y actualiza el precio y el detalle de la venta.

        Parámetros
        ----------
        state : Qt.CheckState
            estado actual del checkbox
        '''
        match state:
            case state.Unchecked:
                # actualiza 'self.field_values'
                self.field_values.setPriceType(InventoryPriceType.NORMAL)
            
            case state.Checked:
                # actualiza 'self.field_values'
                self.field_values.setPriceType(InventoryPriceType.COMERCIAL)
                
        return None


    @Slot()
    def onQuantityEditingFinished(self) -> None:
        '''
        Formatea el texto del campo y lo vuelve a asignar al campo de cantidad 
        y actualiza 'self.field_values'.
        '''
        # cambia puntos por comas, si termina con "." ó "," lo saca
        field_text = self.listItem.lineEdit_productQuantity.text()
        
        field_text = field_text.rstrip(",.")
        field_text = field_text.replace(".",",")
        
        self.listItem.lineEdit_productQuantity.setText(field_text)
        
        # actualiza 'self.field_values'
        self.field_values.setQuantity(
            float(field_text.replace(",","."))
        )
        
        return None


    @Slot(object)
    def onSubtotalChanged(self, subtotal:float | None) -> None:
        '''
        Muestra el costo en la interfaz. Emite la señal 'subtotalChanged'.
        
        Parámetros
        ----------
        subtotal : float | None
            el subtotal de la venta actual, será float si existe y es válido 
            sino None
        '''
        _style:str
        
        # si el valor es None devuelve TypeError
        try:
            match subtotal:
                case 0: # si es 0 ó 0.0 no calcula
                    subtotal = "SUBTOTAL"
            
                case _: # intenta convertir el valor a float
                    subtotal = f"$ {round(float(subtotal), 2)}"
                    subtotal = subtotal.replace(".",",")
                    _style = WidgetStyle.LABEL_RICHTEXT_CONTENT.value
                    
            
        except TypeError: # no puede convertir None a float
            subtotal = "SUBTOTAL"
            _style = WidgetStyle.LABEL_RICHTEXT_NEUTRAL.value
        
        # personaliza el texto del label del subtotal
            
        self.listItem.label_subtotal.setText(
            f'''<html>
                    <head/>
                    <body>
                        <p>
                            <span style={_style}>{subtotal}</span>
                        </p>
                    </body>
                </html>'''
        )
        return None


    @Slot(str)
    def onSaleDetailEdit(self, text:str) -> None:
        '''
        Modifica los detalles de la venta cuando son modificados por el usuario.

        Parámetros
        ----------
        text : str
            el detalle de la venta introducido
        '''
        self.field_values.setSaleDetails(curr_sale_detail=text)
        return None
    
    
    @Slot(str)
    def onSaleDetailsChange(self, text:str) -> None:
        '''
        Cambia el texto del QLineEdit de detalle de venta.

        Parámetros
        ----------
        text : str
            el detalle de la venta a mostrar
        '''
        self.listItem.lineEdit_saleDetail.setText(text)
        return None


    @Slot()
    def onFieldValuesChanged(self) -> None:
        '''
        Emite la señal 'fieldValuesChanged' con todos los valores de los campos 
        cuando algún campo de 'ListItemValues' cambia.
        '''
        self.fieldsValuesChanged.emit(self.field_values.getValues())
        return None


# DEUDORES (VENTA FINALIZADA) | (SECCIÓN DE CUENTA CORRIENTE) ==================================================


class DebtorFullName(QObject):
    '''
    Clase que contiene el nombre y apellido en los campos de Deudas.
    Mediante señales maneja los cambios que se realizan.
    '''
    nameChanged:Signal = Signal(str)
    surnameChanged:Signal = Signal(str)
    fullNameChecked:Signal = Signal(bool) # si existe la combinación de nombre 
        # y apellido emite True (no debe existir, no puede haber duplicados), 
        # sino emite False.
    
    
    def __init__(self) -> None:
        super(DebtorFullName, self).__init__()
        
        self.__debtor_name:str = None
        self.__debtor_surname:str = None
        
        # validez de los datos
        self.__FIELDS_VALIDITY:dict[str, bool | None] = {
            DebtsFields.NAME.name: None,
            DebtsFields.SURNAME.name: None
        }
        
        self.setup_signals()
        return None
    
    
    def setup_signals(self) -> None:
        self.nameChanged.connect(self.__checkFullNameCombination)
        self.surnameChanged.connect(self.__checkFullNameCombination)
        return None
    
    
    # setters
    def setName(self, name:str) -> None:
        '''
        Guarda el nombre. Emite la señal 'nameChanged'.

        Parámetros
        ----------
        name : str
            nombre del titular de la cuenta corriente

        
        '''
        self.__debtor_name = name
        self.nameChanged.emit(self.__debtor_name)
        return None
    
    
    def setSurname(self, surname:str) -> None:
        '''
        Guarda el apellido. Emite la señal 'surnameChanged'.

        Parámetros
        ----------
        surname : str
            apellido del titular de la cuenta corriente

        
        '''
        self.__debtor_surname = surname
        self.surnameChanged.emit(self.__debtor_surname)
        return None


    def setFieldValidity(self, field:DebtsFields, validity:bool) -> None:
        '''
        Guarda el valor de verdad del campo especificado.
        
        Parámetros
        ----------
        field : DebtsFields
            campo al que asignarle el nuevo valor de verdad, admite los 
            valores 'NAME' y 'SURNAME'
        validity : bool
            nuevo valor de verdad del campo
        
        
        '''
        match field:
            case DebtsFields.NAME:
                self.__FIELDS_VALIDITY[DebtsFields.NAME.name] = validity
            
            case DebtsFields.SURNAME:
                self.__FIELDS_VALIDITY[DebtsFields.SURNAME.name] = validity
            
            case _:
                pass
        return None


    @Slot()
    def __checkFullNameCombination(self) -> None:
        '''
        Verifica si en la base de datos ya existe una combinación así de nombre 
        y apellido y emite la señal 'fullNameChecked' con un diccionario con el 
        número de teléfono, dirección y código postal, sino existe emite None.

        
        '''
        data_count:list[tuple]
        if self.isNameValid() and self.isSurnameValid():
            data_count = makeReadQuery(
                    sql='''SELECT COUNT(*) 
                           FROM Deudores 
                           WHERE nombre = ? AND 
                                 apellido = ?;''',
                    params=(self.getName(), self.getSurname(),)
                )
            
            # si existe esa combinación de nombre y apellido...
            if len(data_count) > 0:
                self.fullNameChecked.emit(True)
            
            # si no existe esa combinación...
            else:
                self.fullNameChecked.emit(False)
        return None
    
    
    # getters
    def getName(self) -> str | None:
        '''
        Devuelve el nombre del deudor.

        Retorna
        -------
        str | None
            el nombre del deudor si existe, sino None
        '''
        return self.__debtor_name
    
    
    def getSurname(self) -> str | None:
        '''
        Devuelve el apellido del deudor.

        Retorna
        -------
        str | None
            el apellido del deudor si existe, sino None
        '''
        return self.__debtor_surname


    def isNameValid(self) -> bool:
        '''
        Devuelve un valor de verdad que determina si el nombre es válido.

        Retorna
        -------
        bool
            será True sólo si el nombre es válido, sino False
        '''
        return True if self.__FIELDS_VALIDITY[DebtsFields.NAME.name] else False
    
    
    def isSurnameValid(self) -> bool:
        '''
        Devuelve un valor de verdad que determina si el apellido es válido.

        Retorna
        -------
        bool
            será True sólo si el apellido es válido, sino False
        '''
        return True if self.__FIELDS_VALIDITY[DebtsFields.SURNAME.name] else False





class DebtorContact(QObject):
    '''
    Clase que contiene el número de teléfono, dirección y código postal en los 
    campos de Deudas.
    Mediante señales maneja los cambios que se realizan.
    '''
    phoneChanged:Signal = Signal(str)
    directionChanged:Signal = Signal(str)
    postalCodeChanged:Signal = Signal(str)
    
    def __init__(self) -> None:
        super(DebtorContact, self).__init__()
        
        self.__debtor_phone_num:str = None
        self.__debtor_direction:str = None
        self.__debtor_postal_code:str = None
        
        # validez de los datos
        self.__FIELDS_VALIDITY:dict[str, bool | None] = {
            DebtsFields.PHONE_NUMB.name: None,
            DebtsFields.DIRECTION.name: None,
            DebtsFields.POSTAL_CODE.name: None
        }
        
        return None
    
    
    # setters
    def setPhoneNumber(self, phone_numb:str = None) -> None:
        '''
        Guarda el número de teléfono. Emite la señal 'phoneChanged'.

        Parámetros
        ----------
        phone_numb : str, opcional
            número de teléfono del titular de la cuenta corriente, por defecto 
            es None

        
        '''
        self.__debtor_phone_num = phone_numb
        self.phoneChanged.emit(self.__debtor_phone_num)
        return None


    def setDirection(self, direction:str = None) -> None:
        '''
        Guarda la dirección. Emite la señal 'directionChanged'.

        Parámetros
        ----------
        direction : str, opcional
            dirección del titular de la cuenta corriente, por defecto es None

        
        '''
        self.__debtor_direction = direction
        self.directionChanged.emit(self.__debtor_direction)
        return None


    def setPostalCode(self, postal_code:str = None) -> None:
        '''
        Guarda el número de teléfono.  Emite la señal 'postalCodeChanged'.

        Parámetros
        ----------
        postal_code : str, opcional
            código postal del titular de la cuenta corriente, por defecto es None

        
        '''
        self.__debtor_postal_code = postal_code
        self.postalCodeChanged.emit(str(self.__debtor_postal_code))
        return None
    
    
    def setFieldValidity(self, field:DebtsFields, validity:bool) -> None:
        '''
        Guarda el valor de verdad del campo especificado.
        
        Parámetros
        ----------
        field : DebtsFields
            campo al que asignarle el nuevo valor de verdad, admite los 
            valores 'PHONE_NUMB', 'DIRECTION' Y 'POSTAL_CODE'
        validity : bool
            nuevo valor de verdad del campo
        
        
        '''
        match field:
            case DebtsFields.PHONE_NUMB:
                self.__FIELDS_VALIDITY[DebtsFields.PHONE_NUMB.name] = validity
            
            case DebtsFields.DIRECTION:
                self.__FIELDS_VALIDITY[DebtsFields.DIRECTION.name] = validity
            
            case DebtsFields.POSTAL_CODE:
                self.__FIELDS_VALIDITY[DebtsFields.POSTAL_CODE.name] = validity
            
            case _:
                pass
        return None


    # getters
    def getPhoneNumber(self) -> str:
        '''
        Devuelve el número de teléfono del deudor.

        Retorna
        -------
        str
            el número de teléfono del deudor
        '''
        return self.__debtor_phone_num if self.__debtor_phone_num else ''
    
    
    def getDirection(self) -> str:
        '''
        Devuelve la dirección del deudor.

        Retorna
        -------
        str
            la dirección del deudor
        '''
        return self.__debtor_direction if self.__debtor_direction else ''
    

    def getPostalCode(self) -> int:
        '''
        Devuelve el código postal del deudor, si no fue especificado en algún 
        momento devuelve 0, que es un valor inválido para el campo (admite valores 
        entre 1 y 9.999).

        Retorna
        -------
        int
            el código postal del deudor, si no fue introducido devuelve 0 (es 
            un valor inválido)
        '''
        return int(self.__debtor_postal_code) if self.__debtor_postal_code else ''





# valores de los campos de deudores (formulario de ventas cuando hay deuda)
# class DebtorDataValues(QObject):
class DebtorDataValues(DebtorFullName, DebtorContact):
    '''
    Clase que contiene los valores de los campos de DebtorDataDialog. El principal 
    uso de la clase es para "simular" un MODELO DE DATOS, ya que no usa exactamente 
    la misma metodología para guardar los datos, y al mismo tiempo maneja mediante 
    señales los cambios en los datos más relevantes.
    '''
    fullNameChecked:Signal = Signal(object) # sobreescribe la señal original, si 
        # la combinación de nombre y apellido existe devuelve un dict[str, str] 
        # con tel., dirección y cód. postal del deudor, sino emite None.
    
    
    def __init__(self) -> None:
        super(DebtorDataValues, self).__init__()
        
        # validez de los datos
        self.__FIELDS_VALIDITY:dict[str, bool | None] = {
            DebtsFields.NAME.name: None,
            DebtsFields.SURNAME.name: None
        }
        
        return None
    
    
    # método reimplementado de DebtorFullName
    def setup_signals(self) -> None:
        self.nameChanged.connect(self.__checkFullNameCombination)
        self.surnameChanged.connect(self.__checkFullNameCombination)
        return None
    
    
    # método reimplementado de DebtorFullName | DebtorContact
    def setFieldValidity(self, field:DebtsFields, validity:bool) -> None:
        '''
        Guarda el valor de verdad del campo especificado.
        
        Parámetros
        ----------
        field : DebtsFields
            campo al que asignarle el nuevo valor de verdad
        validity : bool
            nuevo valor de verdad del campo
        
        
        '''
        match field:
            case DebtsFields.NAME:
                self.__FIELDS_VALIDITY[DebtsFields.NAME.name] = validity
            
            case DebtsFields.SURNAME:
                self.__FIELDS_VALIDITY[DebtsFields.SURNAME.name] = validity
            
            case DebtsFields.PHONE_NUMB:
                self.__FIELDS_VALIDITY[DebtsFields.PHONE_NUMB.name] = validity
            
            case DebtsFields.DIRECTION:
                self.__FIELDS_VALIDITY[DebtsFields.DIRECTION.name] = validity
            
            case DebtsFields.POSTAL_CODE:
                self.__FIELDS_VALIDITY[DebtsFields.POSTAL_CODE.name] = validity
        
        return None


    # método reimplementado de DebtorFullName
    @Slot()
    def __checkFullNameCombination(self) -> None:
        '''
        Verifica si en la base de datos ya existe una combinación así de nombre 
        y apellido y emite la señal 'fullNameChecked' con un diccionario con el 
        número de teléfono, dirección y código postal, sino existe emite None.

        
        '''
        if self.isNameValid() and self.isSurnameValid():
            debtor_data = makeReadQuery(
                    sql='''SELECT num_telefono, direccion, codigo_postal 
                           FROM Deudores 
                           WHERE nombre = ? AND 
                                 apellido = ?;''',
                    params=(self.getName(), self.getSurname(),)
                )
            
            # si existe esa combinación de nombre y apellido...
            if len(debtor_data) > 0:
                self.fullNameChecked.emit(
                    {DebtsFields.PHONE_NUMB.name: str(debtor_data[0][0]),
                     DebtsFields.DIRECTION.name: str(debtor_data[0][1]),
                     DebtsFields.POSTAL_CODE.name: str(debtor_data[0][2])}
                )
            
            # si no existe esa combinación...
            else:
                self.fullNameChecked.emit(None)
        return None


    # método reimplementado de DebtorFullName
    def isNameValid(self) -> bool:
        '''
        Devuelve un valor de verdad que determina si el nombre es válido.

        Retorna
        -------
        bool
            será True sólo si el nombre es válido, sino False
        '''
        return True if self.__FIELDS_VALIDITY[DebtsFields.NAME.name] else False
    
    
    # método reimplementado de DebtorFullName
    def isSurnameValid(self) -> bool:
        '''
        Devuelve un valor de verdad que determina si el apellido es válido.

        Retorna
        -------
        bool
            será True sólo si el apellido es válido, sino False
        '''
        return True if self.__FIELDS_VALIDITY[DebtsFields.SURNAME.name] else False
        
    
    def isAllValid(self) -> bool:
        '''
        Devuelve un valor de verdad que determina si todos los valores son 
        válidos, teniendo en cuenta que la dirección, el número de teléfono 
        y el código postal son opcionales.

        Retorna
        -------
        bool
            será True sólo si los valores son válidos, sino False
        '''
        return all(self.__FIELDS_VALIDITY.values())


    # dunder methods
    def __repr__(self) -> str:
        return f'''nombre: {self.getName()} (NAME_VALID={self.isNameValid()})\
            \napellido: {self.getSurname()} (SURNAME_VALID={self.isSurnameValid()})\
            \n\tnúm. tel.: {self.getPhoneNumber()}\
            \n\tdirección: {self.getDirection()}\
            \n\tcódigo postal: {self.getPostalCode()}\
            \n\t\tALL_VALID= {self.isAllValid()}'''




# Dialog con datos de deudores
class DebtorDataDialog(QDialog):
    '''
    QDialog con datos de deudores. Se usa en 'MainWindow' cuando se presiona 
    'MainWindow.btn_end_sale' y el total abonado es menor al costo total, y
    también en Deudas para agregar una nueva deuda.
    
    Emite la señal 'debtorChosen' con el IDdeudor si se llenaron los datos necesarios 
    del deudor, sino emite -1.
    
    Parámetros
    ----------
    return_model_data : bool, opcional
        determina si al hacer click en el botón 'Ok' el QDialog debe emitir la 
        señal 'dataToInsert' con los datos para actualizar el MODELO de Deudas; 
        se usa para poder actualizar automáticamente el MODELO de Deudas
    '''
    debtorChosen = Signal(int) # emite el IDdeudor una vez elegido deudor
    dataToInsert = Signal(object)
    
    def __init__(self, return_model_data:bool=False):
        super(DebtorDataDialog, self).__init__()
        self.debtorData = Ui_debtorDataDialog()
        self.debtorData.setupUi(self)
        
        self.__return_model_data:bool = return_model_data
        
        # instancia de DebtorDataValues, un "pseudomodelo de datos" para 
        # guardar los datos
        self.debtor_values:DebtorDataValues = DebtorDataValues()
        
        self.setup_ui()
        self.setup_variables()
        self.setup_signals()
        return None


    def setup_ui(self) -> None:
        self.debtorData.buttonBox.button(QDialogButtonBox.Ok).setText("Aceptar")
        self.debtorData.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)

        self.debtorData.buttonBox.button(QDialogButtonBox.Cancel).setText("Cancelar")
        self.debtorData.buttonBox.setStyleSheet("QDialogButtonBox QPushButton[text='Cancelar'] {\
                                                        background-color: #ff4949;\
                                                      }\
                                                      QDialogButtonBox QPushButton[text='Cancelar']:hover,\
                                                      QDialogButtonBox QPushButton[text='Cancelar']:pressed {\
                                                        background-color: #faa;\
                                                      }")
        
        # esconde los labels de feedback
        self.debtorData.label_debtorName_feedback.hide()
        self.debtorData.label_debtorSurname_feedback.hide()
        self.debtorData.label_phoneNumber_feedback.hide()
        self.debtorData.label_postalCode_feedback.hide()
        return None
    
    
    def setup_variables(self) -> None:
        # completers
        self.debtorData.lineEdit_debtorName.setCompleter(createCompleter(type=1))
        self.debtorData.lineEdit_debtorSurname.setCompleter(createCompleter(type=2))

        # validadores
        self.debtor_name_validator = DebtorNameValidator(self.debtorData.lineEdit_debtorName)
        self.debtor_surname_validator = DebtorSurnameValidator(self.debtorData.lineEdit_debtorSurname)
        self.phone_number_validator = DebtorPhoneNumberValidator(self.debtorData.lineEdit_phoneNumber)
        self.direction_validator = DebtorDirectionValidator(self.debtorData.lineEdit_direction)
        self.postal_code_validator = DebtorPostalCodeValidator(self.debtorData.lineEdit_postalCode)
        
        self.debtorData.lineEdit_debtorName.setValidator(self.debtor_name_validator)
        self.debtorData.lineEdit_debtorSurname.setValidator(self.debtor_surname_validator)
        self.debtorData.lineEdit_phoneNumber.setValidator(self.phone_number_validator)
        self.debtorData.lineEdit_direction.setValidator(self.direction_validator)
        self.debtorData.lineEdit_postalCode.setValidator(self.postal_code_validator)
        
        return None
    
    
    def setup_signals(self) -> None:
        #* nombre
        self.debtor_name_validator.validationSucceeded.connect(
            lambda: self.validatorOnValidationSucceded(DebtsFields.NAME)
        )
        self.debtor_name_validator.validationFailed.connect(
            lambda error_message: self.validatorOnValidationFailed(
                field_validated=DebtsFields.NAME,
                error_message=error_message
            )
        )
        self.debtor_name_validator.validationSucceeded.connect(self.onFieldChanged)
        
        self.debtorData.lineEdit_debtorName.editingFinished.connect(
            self.onNameEditingFinished
        )
        self.debtor_name_validator.validationFailed.connect(self.onFieldChanged)
        
        self.debtor_values.nameChanged.connect(
            lambda new_val: self.__updateFieldValue(
                field_to_update=DebtsFields.NAME,
                new_val=new_val
            )
        )
        self.debtor_values.nameChanged.connect(self.onFieldChanged)
        
        #* apellido
        self.debtor_surname_validator.validationSucceeded.connect(
            lambda: self.validatorOnValidationSucceded(DebtsFields.SURNAME)
        )
        self.debtor_surname_validator.validationSucceeded.connect(self.onFieldChanged)
        self.debtor_surname_validator.validationFailed.connect(
            lambda error_message: self.validatorOnValidationFailed(
                field_validated=DebtsFields.SURNAME,
                error_message=error_message)
        )
        self.debtor_surname_validator.validationFailed.connect(self.onFieldChanged)
        
        self.debtorData.lineEdit_debtorSurname.editingFinished.connect(
            self.onSurnameEditingFinished
        )
        
        self.debtor_values.surnameChanged.connect(
            lambda new_val: self.__updateFieldValue(
                field_to_update=DebtsFields.SURNAME,
                new_val=new_val
            )
        )
        self.debtor_values.surnameChanged.connect(self.onFieldChanged)
        
        #* número de teléfono
        self.phone_number_validator.validationSucceeded.connect(
            lambda: self.validatorOnValidationSucceded(DebtsFields.PHONE_NUMB)
        )
        self.phone_number_validator.validationFailed.connect(
            lambda error_message: self.validatorOnValidationFailed(
                field_validated=DebtsFields.PHONE_NUMB,
                error_message=error_message)
        )
        
        self.debtorData.lineEdit_phoneNumber.editingFinished.connect(
            lambda: self.formatField(DebtsFields.PHONE_NUMB)
        )
        
        self.debtor_values.phoneChanged.connect(
            lambda new_val: self.__updateFieldValue(
                field_to_update=DebtsFields.PHONE_NUMB,
                new_val=new_val
            )
        )
        self.debtor_values.phoneChanged.connect(self.onFieldChanged)
        
        #* dirección
        self.direction_validator.validationSucceeded.connect(
            lambda: self.validatorOnValidationSucceded(DebtsFields.DIRECTION)
        )
        self.direction_validator.validationFailed.connect(
            lambda error_message: self.validatorOnValidationFailed(
                field_validated=DebtsFields.DIRECTION,
                error_message=error_message)
        )
        
        self.debtorData.lineEdit_direction.editingFinished.connect(
            lambda: self.debtor_values.setDirection(
                direction=self.debtorData.lineEdit_direction.text()
            )
        )
        self.debtor_values.directionChanged.connect(
            lambda new_val: self.__updateFieldValue(
                field_to_update=DebtsFields.DIRECTION,
                new_val=new_val
            )
        )
        self.debtor_values.directionChanged.connect(self.onFieldChanged)
        
        #* código postal
        self.postal_code_validator.validationSucceeded.connect(
            lambda: self.validatorOnValidationSucceded(DebtsFields.POSTAL_CODE)
        )
        self.postal_code_validator.validationFailed.connect(
            lambda error_message: self.validatorOnValidationFailed(
                field_validated=DebtsFields.POSTAL_CODE,
                error_message=error_message
            )
        )
        
        self.debtorData.lineEdit_postalCode.editingFinished.connect(
            lambda: self.debtor_values.setPostalCode(
                postal_code=self.debtorData.lineEdit_postalCode.text()
            )
        )
        
        self.debtor_values.postalCodeChanged.connect(
            lambda new_val: self.__updateFieldValue(
                field_to_update=DebtsFields.POSTAL_CODE,
                new_val=new_val
            )
        )
        self.debtor_values.postalCodeChanged.connect(self.onFieldChanged)
        
        #* combinación de nombre y apellido verificada
        self.debtor_values.fullNameChecked.connect(self.onFullNameChecked)
        
        #* botón "Aceptar"
        self.debtorData.buttonBox.accepted.connect(self.handleOkClicked)
        return None


    @Slot(object)
    def validatorOnValidationSucceded(self, field_validated:DebtsFields) -> None:
        '''
        Cambia el valor del flag asociado al campo que fue validado 'field_validated' 
        a True, cambia el QSS del campo y esconde el label de feedback asociado 
        al campo.
        NOTA: en caso de que el nombre y el apellido existan, los demás datos no 
        serán validados.
        
        Parámetros
        ----------
        field_validated : DebtsFields
            el campo que se valida
        
        
        '''
        
        self.debtor_values.setFieldValidity(
            field=field_validated,
            validity=True
        )
        
        match field_validated:
            case DebtsFields.NAME:
                self.debtorData.lineEdit_debtorName.setStyleSheet(
                    WidgetStyle.FIELD_VALID_VAL.value
                )
                self.debtorData.label_debtorName_feedback.hide()
            
            case DebtsFields.SURNAME:
                self.debtorData.lineEdit_debtorSurname.setStyleSheet(
                    WidgetStyle.FIELD_VALID_VAL.value
                )
                self.debtorData.label_debtorSurname_feedback.hide()
            
            case DebtsFields.PHONE_NUMB:
                #? antes de cambiar el estilo del tel. verifica si está activado 
                #? el campo, porque sino significa que el nombre y apellido 
                #? existen (no se deben modificar desde acá los datos estos, 
                #? se debe hacer desde la sección de Deudas)
                if (self.debtorData.lineEdit_phoneNumber.isEnabled() 
                        and self.debtorData.lineEdit_phoneNumber.text()):
                    self.debtorData.lineEdit_phoneNumber.setStyleSheet(
                        WidgetStyle.FIELD_VALID_VAL.value
                    )
                
                else:
                    self.debtorData.lineEdit_phoneNumber.setStyleSheet("")
                
                self.debtorData.label_phoneNumber_feedback.hide()
            
            case DebtsFields.POSTAL_CODE:
                #? al igual que con el tel., verifica si el campo está habilitado, 
                #? por la misma razón
                if (self.debtorData.lineEdit_postalCode.isEnabled() and 
                        self.debtorData.lineEdit_postalCode.text()):
                    self.debtorData.lineEdit_postalCode.setStyleSheet(
                        WidgetStyle.FIELD_VALID_VAL.value
                    )
                
                else:
                    self.debtorData.lineEdit_postalCode.setStyleSheet("")
                    
                self.debtorData.label_postalCode_feedback.hide()
        return None
    
    
    @Slot(object, str)
    def validatorOnValidationFailed(self, field_validated:DebtsFields, error_message:str) -> None:
        '''
        Cambia el valor del flag asociado al campo que fue validado 'field_validated' 
        a False, cambia el QSS del campo y muestra el QLabel asociado al campo 
        con el mensaje 'error_message' con feedback.
        
        Parámetros
        ----------
        field_validated : DebtsFields
            el campo que se valida
        error_message : str
            el mensaje de error a mostrar al usuario
        
        
        '''
        self.debtor_values.setFieldValidity(
            field=field_validated,
            validity=False
        )
        
        match field_validated:
            case DebtsFields.NAME:
                self.debtorData.lineEdit_debtorName.setStyleSheet(
                    WidgetStyle.FIELD_INVALID_VAL.value
                )
                self.debtorData.label_debtorName_feedback.show()
                self.debtorData.label_debtorName_feedback.setText(error_message)
            
            case DebtsFields.SURNAME:
                self.debtorData.lineEdit_debtorSurname.setStyleSheet(
                    WidgetStyle.FIELD_INVALID_VAL.value
                )
                self.debtorData.label_debtorSurname_feedback.show()
                self.debtorData.label_debtorSurname_feedback.setText(error_message)
            
            case DebtsFields.PHONE_NUMB:
                self.debtorData.lineEdit_phoneNumber.setStyleSheet(
                    WidgetStyle.FIELD_INVALID_VAL.value
                )
                self.debtorData.label_phoneNumber_feedback.show()
                self.debtorData.label_phoneNumber_feedback.setText(error_message)
            
            case DebtsFields.POSTAL_CODE:
                self.debtorData.lineEdit_postalCode.setStyleSheet(
                    WidgetStyle.FIELD_INVALID_VAL.value
                )
                self.debtorData.label_postalCode_feedback.show()
                self.debtorData.label_postalCode_feedback.setText(error_message)
        
        # self.__toggleOkButton()
        return None
    
        
    @Slot(str)
    def formatField(self, field_to_format:DebtsFields) -> None:
        '''
        Dependiendo del campo formatea el texto y lo actualiza en self.debtor_values.
        
        Parámetros
        ----------
        field_to_format : DebtsFields
            el campo a formatear, admite los siguientes valores:
            - NAME: formatea el campo de nombre del deudor
            - SURNAME: formatea el campo de apellido del deudor
            - PHONE_NUMB: formatea el campo de teléfono del deudor

        
        '''
        field_text:str
        phone_number:PhoneNumber # se usa cuando el campo a formatear es el de núm. de teléfono
        
        match field_to_format:
            case DebtsFields.NAME:
                # pasa a minúsculas y pone en mayúsculas la primera letra de cada nombre
                field_text = self.debtorData.lineEdit_debtorName.text()
                field_text = field_text.lower().title()
                self.debtor_values.setName(field_text)
            
            case DebtsFields.SURNAME:
                # pasa a minúsculas y pone en mayúsculas la primera letra de cada apellido
                field_text = self.debtorData.lineEdit_debtorSurname.text()
                field_text = field_text.lower().title()
                self.debtor_values.setSurname(field_text)
            
            case DebtsFields.PHONE_NUMB:
                # agrega un "+" al principio (si no tiene) y formatea el núm. estilo internacional
                field_text = self.debtorData.lineEdit_phoneNumber.text()
                try:
                    phone_number = parse(f"+{field_text}")
                    if is_valid_number(phone_number):
                        field_text = format_number(phone_number, PhoneNumberFormat.INTERNATIONAL)
                
                except NumberParseException as err:
                    logging.error(err)
                    field_text = self.debtorData.lineEdit_phoneNumber.text()
                
                self.debtor_values.setPhoneNumber(field_text)
        
        return None
    
    
    @Slot(str)
    def __updateFieldValue(self, field_to_update:DebtsFields, new_val:str) -> None:
        '''
        Actualiza el valor viejo del campo por el nuevo.

        Parámetros
        ----------
        field_to_update : DebtsFields
            el campo con cuyo valor se debe actualizar
        new_val : str
            nuevo valor para el campo

        
        '''
        match field_to_update:
            case DebtsFields.NAME:
                self.debtorData.lineEdit_debtorName.setText(new_val)
            
            case DebtsFields.SURNAME:
                self.debtorData.lineEdit_debtorSurname.setText(new_val)
                
            case DebtsFields.PHONE_NUMB:
                self.debtorData.lineEdit_phoneNumber.setText(new_val)
            
            case DebtsFields.DIRECTION:
                self.debtorData.lineEdit_direction.setText(new_val)
            
            case DebtsFields.POSTAL_CODE:
                self.debtorData.lineEdit_postalCode.setText(new_val)
                
        return None
    
        
    @Slot()
    def onNameEditingFinished(self) -> None:
        '''
        Formatea el campo de nombre y crea un QCompleter para el campo de 
        apellido.
        
        
        '''
        self.formatField(field_to_format=DebtsFields.NAME)
        
        self.debtorData.lineEdit_debtorSurname.setCompleter(
            createCompleter(
                sql='''SELECT DISTINCT apellido 
                       FROM Deudores 
                       WHERE nombre = ?''',
                params=(self.debtor_values.getName(),)
            )
        )
        return None
    
    
    @Slot()
    def onSurnameEditingFinished(self) -> None:
        '''
        Formatea el campo de apellido y crea un QCompleter para el campo de 
        nombre.
        
        
        '''
        self.formatField(field_to_format=DebtsFields.SURNAME)
        
        self.debtorData.lineEdit_debtorName.setCompleter(
            createCompleter(
                sql='''SELECT DISTINCT nombre 
                       FROM Deudores 
                       WHERE apellido = ?''',
                params=(self.debtor_values.getSurname(),)
            )
        )
        return None
    
    
    @Slot(object)
    def onFullNameChecked(self, debtor_data:dict[str, str] | None) -> None:
        '''
        Si la combinación de nombre y apellido existe actualiza el modelo con 
        los valores correspondientes y los deshabilita para evitar su 
        modificación, sino los habilita.
        
        Parámetros
        ----------
        debtor_data : dict[str, str] | None
            diccionario con el número de teléfono, dirección y código postal 
            del deudor si existe la combinación de nombre y apellido, sino 
            existe es None

        
        '''
        if debtor_data:
            # deshabilita los campos
            self.debtorData.lineEdit_phoneNumber.setEnabled(False)
            self.debtorData.lineEdit_direction.setEnabled(False)
            self.debtorData.lineEdit_postalCode.setEnabled(False)
        
            # actualiza el modelo con los valores nuevos
            self.debtor_values.setPhoneNumber(debtor_data[DebtsFields.PHONE_NUMB.name])
            self.debtor_values.setDirection(debtor_data[DebtsFields.DIRECTION.name])
            self.debtor_values.setPostalCode(debtor_data[DebtsFields.POSTAL_CODE.name])
            
        else:
            # habilita los campos
            self.debtorData.lineEdit_phoneNumber.setEnabled(True)
            self.debtorData.lineEdit_direction.setEnabled(True)
            self.debtorData.lineEdit_postalCode.setEnabled(True)
        return None
    
    
    @Slot()
    def onFieldChanged(self) -> None:
        '''
        Verifica si todos los valores son válidos y habilita o deshabilita el 
        botón "Aceptar".

        
        '''
        # activa o desactiva el botón "Aceptar" si todos los campos son válidos
        if self.debtor_values.isAllValid():
            self.debtorData.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)
        
        else:
            self.debtorData.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
        
        return None
    
    
    @Slot()
    def handleOkClicked(self) -> None:
        '''
        Inserta los valores en la base de datos en las tablas de "Deudores" 
        (si no existe el deudor). 
        Al final emite la señal 'debtorChosen' con el "IDdeudor" del deudor 
        confirmando que se eligió un deudor.
        
        
        '''
        count_query:int # consulta para ver si existe el Deudor
        debtor_id:int # IDdeudor para emitir a MainWindow

        with DatabaseRepository() as db_repo:
            # verifica si el deudor existe en Deudores
            count_query = makeReadQuery(
                sql= '''SELECT COUNT(*) 
                        FROM Deudores 
                        WHERE nombre = ? 
                            AND apellido = ?;''',
                params=(self.debtor_values.getName(),
                        self.debtor_values.getSurname(),)
                )[0][0] # si el deudor no existe devuelve 0
    
            # si no existe ese deudor, lo agrega...
            if not count_query:
                # INSERT a Deudores
                db_repo.insertRegister(
                    ins_sql= '''INSERT INTO Deudores(
                                    nombre,
                                    apellido,
                                    num_telefono,
                                    direccion,
                                    codigo_postal) 
                                VALUES(?, ?, ?, ?, ?);''',
                    ins_params=(self.debtor_values.getName(),
                                self.debtor_values.getSurname(),
                                self.debtor_values.getPhoneNumber(),
                                self.debtor_values.getDirection(),
                                self.debtor_values.getPostalCode())
                )
                
                logging.debug(LoggingMessage.DEBUG_DB_SINGLE_INSERT_SUCCESS)

            # manda a MainWindow el IDdeudor en la señal 'debtorChosen'
            debtor_id = makeReadQuery(
                    sql= '''SELECT IDdeudor 
                            FROM Deudores 
                            WHERE nombre = ? 
                                AND apellido = ?;''',
                    params=(self.debtor_values.getName(),
                            self.debtor_values.getSurname(),)
                )[0][0]
            
            # si se llamó desde Ventas, sólo emite el IDdeudor
            if not self.__return_model_data:
                # emite señal avisando que SÍ se eligió un deudor, con el IDdeudor
                self.debtorChosen.emit(debtor_id)
            
            # si se llamó desde Deudas emite los datos para actualizar el MODELO
            else:
                self.dataToInsert.emit(
                    {DebtorModelCols.DEBTS_IDDEBTOR.name: debtor_id,
                     DebtorModelCols.DEBTS_NAME.name: self.debtor_values.getName(),
                     DebtorModelCols.DEBTS_SURNAME.name: self.debtor_values.getSurname(),
                     DebtorModelCols.DEBTS_PHONE_NUMBER.name: self.debtor_values.getPhoneNumber(),
                     DebtorModelCols.DEBTS_DIRECTION.name: self.debtor_values.getDirection(),
                     DebtorModelCols.DEBTS_POSTAL_CODE.name: self.debtor_values.getPostalCode(),
                     DebtorModelCols.DEBTS_TOTAL_BALANCE.name: 0.0}
                )
        
        return None


# DEUDORES (SECCIÓN CUENTA CORRIENTE) ==========================================================================


class ProductsBalanceDialog(QDialog):
    '''
    QDialog con formato Popup que contiene los productos en cuenta corriente 
    de la persona seleccionada en la tabla de Cuentas Corrientes en MainWindow.
    
    Al cerrarse el dialog emite la señal 'balanceChanged' con el nuevo balance.
    
    Éste QDialog admite las siguientes operaciones sobre la tabla que contiene:
        - READ: para mostrar los productos
        - UPDATE: para modificar campos de los productos
        - DELETE: para marcar como eliminadas las deudas de los productos
    '''
    balanceChanged:Signal = Signal(float)
    
    def __init__(self, debtor_id:int, curr_balance:float, table_view:QTableView) -> None:
        super(ProductsBalanceDialog, self).__init__()
        self.products_balance_dialog = Ui_ProductsBalance()
        self.products_balance_dialog.setupUi(self)
        
        self.debtor_id:int = debtor_id
        self.balance:float = curr_balance
        self.__table_view:QTableView = table_view
        
        self.__products_balance_data:ndarray = self.__getDebtorProducts()
        
        self.setup_ui()
        self.setup_validators()
        self.setup_model()
        self.setup_delegate()
        self.setup_signals()
        return None
    
    
    def setup_ui(self) -> None:
        # crea el dialog como ventana sin frame
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | 
                            Qt.WindowType.Popup)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, True)
        
        # aplica efecto drop-shadow al central widget
        self.shadow_effect = QGraphicsDropShadowEffect()
        self.shadow_effect.setBlurRadius(20)
        self.shadow_effect.setOffset(7, 7)
        self.shadow_effect.setColor(QColor(34, 87, 122, 220))
        self.products_balance_dialog.central_widget.setGraphicsEffect(self.shadow_effect)
        
        # crea animación para mostrar el dialog
        self.fade_in_anim = QPropertyAnimation(self, b"windowOpacity")
        self.fade_in_anim.setDuration(100)
        self.fade_in_anim.setStartValue(0)
        self.fade_in_anim.setEndValue(1)
        self.fade_in_anim.setEasingCurve(QEasingCurve.Type.InCubic)
        
        # coloca íconos y otros estilos
        self.search_icon = QIcon(":/icons/search.svg")
        self.products_balance_dialog.search_bar.addAction(self.search_icon, QLineEdit.ActionPosition.LeadingPosition)
        
        self.delete_debt_icon = QIcon(":/icons/trash-register.svg")
        self.products_balance_dialog.btn_delete_debt.setIcon(self.delete_debt_icon)
        
        # sobreescribe el evento Paint (mediante un filtro de eventos)
        self.event_filter = BackgroundEventFilter(self.products_balance_dialog.tv_balance_products)
        self.products_balance_dialog.tv_balance_products.viewport().installEventFilter(self.event_filter)
        return None
    
    
    def setup_validators(self) -> None:
        # search bar
        self.search_bar_validator = SearchBarValidator(
            self.products_balance_dialog.search_bar
        )
        
        self.products_balance_dialog.search_bar.setValidator(
            self.search_bar_validator
        )
        
        # lineedit para reducir deudas
        self.le_reduce_debt_validator = ProductReduceDebtValidator(
            self.products_balance_dialog.le_reduce_debt
        )
        
        self.products_balance_dialog.le_reduce_debt.setValidator(
            self.le_reduce_debt_validator
        )
        return None
    
    
    def setup_model(self) -> None:
        # modelo de datos
        self.products_balance_model = ProductsBalanceModel(
            data=self.__products_balance_data,
            headers=ModelHeaders.PRODS_BAL_HEADERS.value
        )
        
        # proxy model
        self.products_balance_proxy_model = ProductsBalanceProxyModel()
        self.products_balance_proxy_model.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.products_balance_proxy_model.setSourceModel(self.products_balance_model)
        
        # table view
        self.products_balance_dialog.tv_balance_products.setModel(self.products_balance_proxy_model)
        self.products_balance_dialog.tv_balance_products.setSortingEnabled(True)
        
        # selection model
        self.tv_selection_model = self.products_balance_dialog.tv_balance_products.selectionModel()
        
        setTableViewPolitics(self.products_balance_dialog.tv_balance_products)
        return None
    
    
    def setup_delegate(self) -> None:
        self.products_balance_delegate = ProductsBalanceDelegate(
            self.products_balance_dialog.tv_balance_products
        )
        self.products_balance_dialog.tv_balance_products.setItemDelegate(
            self.products_balance_delegate
        )
        return None
    
    
    def setup_signals(self) -> None:
        # actualización del modelo de datos
        self.products_balance_model.dataToUpdate.connect(
            lambda data: self.updateValuesInDatabase(
                column=data['column'],
                IDsales_detail=data['ID_sales_detail'],
                new_val=data['new_value']
            )
        )
        # search bar
        self.products_balance_dialog.search_bar.textChanged.connect(
            self.products_balance_proxy_model.setFilterRegularExpression
        )
        self.products_balance_dialog.search_bar.textChanged.connect(
            lambda: self.products_balance_dialog.search_bar.setStyleSheet(
                LabelFeedbackStyle.VALID.value
            )
        )
        self.products_balance_dialog.search_bar.inputRejected.connect(
            lambda: self.products_balance_dialog.search_bar.setStyleSheet(
                LabelFeedbackStyle.INVALID.value
            )
        )
        
        # checkbox para mostrar/ocultar historial
        self.products_balance_dialog.checkbox_show_all_products.checkStateChanged.connect(
            self.setModelDataOnCheckStateChange
        )
        
        # lineedit para reducir deudas
        self.products_balance_dialog.le_reduce_debt.textChanged.connect(
            lambda: self.products_balance_dialog.le_reduce_debt.setStyleSheet(
                LabelFeedbackStyle.VALID.value
            )
        )
        self.products_balance_dialog.le_reduce_debt.inputRejected.connect(
            lambda: self.products_balance_dialog.le_reduce_debt.setStyleSheet(
                LabelFeedbackStyle.INVALID.value
            )
        )
        self.le_reduce_debt_validator.isEmpty.connect(
            lambda: self.products_balance_dialog.le_reduce_debt.setStyleSheet("")
        )
        
        self.products_balance_dialog.le_reduce_debt.returnPressed.connect(
            self.formatLineEditReduceDebtValue
        )
        self.products_balance_dialog.le_reduce_debt.returnPressed.connect(
            self.onLEReduceDebtReturnPressed
        )
        
        # cambio de selección en la tabla
        self.tv_selection_model.selectionChanged.connect(
            self.toggleDeleteDebtButton
        )
        
        # eliminación de deudas
        self.products_balance_dialog.btn_delete_debt.clicked.connect(
            self.onDeleteDebts
        )
        
        self.products_balance_proxy_model.baseModelRowsSelected.connect(
            self.__onProductsBalanceBaseModelRowsSelected
        )
        return None


    # mostrar productos (SELECT)
    def __getDebtorProducts(self, show_all:bool=False) -> ndarray:
        '''
        Retorna los productos que el deudor tiene en su cuenta corriente junto 
        con la fecha y hora en la que se realizó la venta y el saldo.

        Parámetros
        ----------
        show_all : bool, opcional
            flag que determina si retornar todos los productos que el cliente 
            alguna vez tuvo en su cuenta corriente

        Retorna
        -------
        ndarray
            ndarray[[ID_detalle_venta, fecha y hora, descripción, saldo]]
        '''
        _date_time:str | datetime
        dt:str | datetime
        
        with DatabaseRepository() as db_repo:
            match show_all:
                case True: # selecciona todas las deudas
                    data = db_repo.selectRegisters(
                        data_sql='''SELECT dv.ID_detalle_venta,
                                        d.fecha_hora,
                                        v.detalles_venta,
                                        d.total_adeudado
                                    FROM Productos AS p,
                                        Detalle_Ventas AS dv,
                                        Ventas AS v,
                                        Deudas AS d,
                                        Deudores AS de
                                    WHERE de.IDdeudor = ? AND 
                                        dv.IDproducto = p.IDproducto AND 
                                        dv.IDdeuda = d.IDdeuda AND 
                                        dv.IDventa = v.IDventa AND 
                                        d.IDdeudor = de.IDdeudor;''',
                        data_params=(self.debtor_id,)
                    )
                
                case False: # selecciona las deudas con eliminado = 0
                    data = db_repo.selectRegisters(
                        data_sql='''SELECT dv.ID_detalle_venta,
                                        d.fecha_hora,
                                        v.detalles_venta,
                                        d.total_adeudado
                                    FROM Productos AS p,
                                        Detalle_Ventas AS dv,
                                        Ventas AS v,
                                        Deudas AS d,
                                        Deudores AS de
                                    WHERE de.IDdeudor = ? AND 
                                        dv.IDproducto = p.IDproducto AND 
                                        dv.IDdeuda = d.IDdeuda AND 
                                        dv.IDventa = v.IDventa AND 
                                        d.IDdeudor = de.IDdeudor AND 
                                        d.eliminado = 0;''',
                        data_params=(self.debtor_id,)
                    )
        
        # intenta convertir la fecha y hora a objeto 'datetime'
        if data:
            for i, reg in enumerate(data):
                _date_time = reg[1]
                reg = list(reg)
                try:
                    dt = datetime.strptime(_date_time, DateAndTimeFormat.DIR_DATETIME_ISO_8601.value)
                    _date_time = dt.strftime(DateAndTimeFormat.DIR_LOCAL_DATETIME_FORMAT.value)

                except (ValueError, TypeError) as err:
                    logging.error(f"Error al convertir fecha y hora a objeto 'datetime': {err}")
                    _date_time = reg[1]

                finally:
                    reg[1] = _date_time
                    reg = tuple(reg)
                    data[i] = reg
        
        return array(data, dtype=object)

    
    def setModelDataOnCheckStateChange(self) -> None:
        '''
        Actualiza los datos del MODELO DE DATOS con respecto al estado de la 
        checkbox.
        '''
        match self.products_balance_dialog.checkbox_show_all_products.isChecked():
            case True:
                self.__products_balance_data = self.__getDebtorProducts(show_all=True)
            
            case False:
                self.__products_balance_data = self.__getDebtorProducts(show_all=False)
        
        self.products_balance_model.setModelData(
            data=self.__products_balance_data,
            headers=ModelHeaders.PRODS_BAL_HEADERS.value
        )
        return None
    
    
    # eliminar productos (DELETE)
    def toggleDeleteDebtButton(self) -> None:
        '''
        Activa/desactiva el botón que permite eliminar registros de la tabla 
        según haya o no registros seleccionados.
        '''
        self.products_balance_dialog.btn_delete_debt.setEnabled(
            self.tv_selection_model.hasSelection()
        )
        return None
    
    
    @Slot()
    def onDeleteDebts(self) -> None:
        '''
        Marca como eliminadas las deudas de los productos seleccionados y al 
        finalizar reinicia la selección de items en la tabla.
        '''
        selected_rows = getSelectedTableRows(
            tableView=self.products_balance_dialog.tv_balance_products
        )
        if not selected_rows:
            return None
        
        # elimina los registros del modelo de datos
        self.products_balance_proxy_model.removeSelectedRows(selected_rows)
        
        self.tv_selection_model.clear()
        return None
    
    
    def __onProductsBalanceBaseModelRowsSelected(
        self, base_model_rows_selected:tuple[int]) -> None:
        '''
        Marca como eliminadas las deudas seleccionadas.

        Parámetros
        ----------
        base_model_rows_selected : tuple[int]
            las filas mapeadas del MODELO BASE seleccionadas para eliminar en 
            la base de datos
        '''
        ids_to_delete:list[int] = []
        
        # obtiene los ID_detalle_venta de los productos y los convierte en tuple[ID]
        for row in base_model_rows_selected:
            ids_to_delete.append(
                self.products_balance_proxy_model.getSaleDetailID(row)
            )
        
        # marca como eliminados los registros
        for id in ids_to_delete:
            self.updateValuesInDatabase(
                column=DebtsViewCols.PRODS_BAL_BALANCE.value,
                IDsales_detail=id,
                new_val=0
            )
        
        return None


    # actualizar productos (UPDATE)
    @Slot(int, int, object)
    def updateValuesInDatabase(self, column:int, IDsales_detail:int,
                                       new_val:Any) -> None:
        '''
        Actualiza la base de datos con el valor nuevo de la sección de Deudas. 
        Además, en caso de que la columna modificada sea la de "fecha y hora" 
        actualiza el nuevo horario en la tabla "Ventas" y en "Deudas".
        
        Parámetros
        ----------
        column : int
            Columna del item modificado
        IDsales_detail : int
            IDproducto en la base de datos del item modificado
        new_val : Any
            Valor nuevo del item
        
        Retorna
        -------
        None
        '''
        with DatabaseRepository() as db_repo:
            match column:
                case DebtsViewCols.PRODS_BAL_DATETIME.value:
                    # intenta convertir a formato ISO 8601...
                    _datetime_to_iso = local_to_ISO8601(new_val)
                    _datetime_to_iso = new_val if not _datetime_to_iso else _datetime_to_iso
                    
                    db_repo.updateRegisters(
                        upd_sql= '''UPDATE Ventas 
                                    SET fecha_hora = ? 
                                    WHERE IDventa = (
                                        SELECT IDventa 
                                        FROM Detalle_Ventas 
                                        WHERE ID_detalle_venta = ?);''',
                        upd_params=(_datetime_to_iso, IDsales_detail)
                    )
                    
                    db_repo.updateRegisters(
                        upd_sql= '''UPDATE Deudas 
                                    SET fecha_hora = ? 
                                    WHERE IDdeuda = (
                                        SELECT IDdeuda 
                                        FROM Detalle_Ventas 
                                        WHERE ID_detalle_venta = ?);''',
                        upd_params=(_datetime_to_iso, IDsales_detail)
                    )
                
                case DebtsViewCols.PRODS_BAL_DESCRIPTION.value:
                    db_repo.updateRegisters(
                        upd_sql= '''UPDATE Ventas 
                                    SET detalles_venta = ? 
                                    WHERE IDventa = (
                                        SELECT IDventa 
                                        FROM Detalle_Ventas 
                                        WHERE ID_detalle_venta = ?);''',
                        upd_params=(new_val, IDsales_detail,)
                    )
                
                case DebtsViewCols.PRODS_BAL_BALANCE.value:
                    db_repo.updateRegisters(
                        upd_sql= '''UPDATE Deudas
                                    SET 
                                        total_adeudado = ?,
                                        eliminado = CASE WHEN ? = 0 THEN 1 ELSE 0 END
                                    WHERE IDdeuda = (
                                        SELECT IDdeuda 
                                        FROM Detalle_Ventas 
                                        WHERE ID_detalle_venta = ?
                                    );''',
                        upd_params=(new_val, new_val, IDsales_detail)
                    )
        
        return None


    # reducir deuda de productos seleccionados (UPDATE también)
    @Slot()
    def formatLineEditReduceDebtValue(self) -> None:
        '''
        Formatea el valor del QLineEdit usado para reducir las deudas de los 
        productos y lo vuelve a asignar al QLineEdit.
        '''
        value:str | float = self.products_balance_dialog.le_reduce_debt.text()
        
        value = value.replace(",",".").strip()
        if value.endswith("."):
            value.rstrip(".")
        
        self.products_balance_dialog.le_reduce_debt.setText(value)
        return None
    
    
    @Slot()
    def onLEReduceDebtReturnPressed(self) -> None:
        '''
        Obtiene los valores de los índices y descuenta en total la cantidad 
        ingresada de los productos seleccionados.
        
        Sigue la siguiente lógica:
            - si la cantidad ingresada es mayor o igual al total adeudado 
            del producto cancela la deuda de ese producto y el resto de 
            la cantidad ingresada es descontada del siguiente producto.
            - si la cantidad ingresada es menor al total adeudado del producto 
            reduce la deuda por la cantidad ingresada.
        '''
        _mapped_indexes:list[QModelIndex] = self.__getSelectedMappedIndexes()
        value:float = float(self.products_balance_dialog.le_reduce_debt.text())
        _idx_balance:float
        
        # descuenta la cantidad especificada
        for idx in _mapped_indexes:
            _idx_balance = float(idx.data(Qt.ItemDataRole.DisplayRole))
            
            # si el valor es mayor o igual anula la deuda
            if value >= _idx_balance:
                value -= _idx_balance
                value = round(value, 2)
                self.products_balance_model.setData(
                    index=idx,
                    value=0.0
                )
            
            # si el valor es menor descuenta el valor y deja de iterar
            else:
                self.products_balance_model.setData(
                    index=idx,
                    value=round(_idx_balance - value, 2)
                )
                value = 0 # ya no queda más que repartir, sale del bucle
            
            # sale del bucle al haber descontado todo lo ingresado como valor
            if not value:
                break
            
        return None
    
    
    def __getSelectedMappedIndexes(self) -> list[QModelIndex]:
        '''
        Obtiene los índices ya mapeados seleccionados en la VISTA para usarse 
        en el MODELO DE DATOS BASE.

        Retorna
        -------
        list[QModelIndex]
            lista con todos los índices meapeados del MODELO DE DATOS BASE
        '''
        selected_rows:tuple[int] # filas seleccionadas
        table_view = self.products_balance_dialog.tv_balance_products
        proxy_model = self.products_balance_proxy_model
        col = DebtsViewCols.PRODS_BAL_BALANCE.value
        
        # obtengo las filas seleccionadas
        selected_rows = getSelectedTableRows(tableView=table_view)
        
        # mapea los índices
        return [proxy_model.mapToSource(proxy_model.index(row, col)) for row in selected_rows]

    
    # eventos
    def showEvent(self, event:QShowEvent):
        '''
        Reimplementación de 'showEvent'. 
        Lo uso en este caso para poder colocar el dialog cerca del cursor 
        cuando se crea y para mostrar el dialog con una animación.
        '''
        geometry:QRect = self.geometry()
        table_rect:QRect = self.__table_view.rect()
        table_top_left:QPoint = self.__table_view.mapToGlobal(table_rect.topLeft())
        table_bottom_right:QPoint = self.__table_view.mapToGlobal(table_rect.bottomRight())
        
        geometry.moveTopRight(QCursor().pos())
        
        self.setMaximumHeight(table_rect.height())
        
        # corrijo la posición para que no se salga del table view
        x, y = geometry.x(), geometry.y()
        width, height = geometry.width(), geometry.height()
        
        # si se sale por la derecha...
        if x + width > table_bottom_right.x():
            x = table_bottom_right.x() - width
        
        # si se sale por la izquierda...
        if x < table_top_left.x():
            x = table_top_left.x()
        
        # si se sale por abajo...
        if y + height > table_bottom_right.y():
            y = table_bottom_right.y() - height
        
        # si se sale por arriba...
        if y < table_top_left.y():
            y = table_top_left.y()
            
        self.setGeometry(x, y, width, height)
        
        # muestra el dialog con una animación
        self.fade_in_anim.start()
        return super(ProductsBalanceDialog, self).showEvent(event)


    def keyPressEvent(self, event:QKeyEvent):
        match event.key():
            case Qt.Key.Key_Escape: # si se presiona "esc" se cierra 
                self.close()        # el dialog y se rechaza el input
                self.reject()
            
            case Qt.Key.Key_Delete: # si se presiona "delete" se borran los 
                self.onDeleteDebts()  # productos seleccionados
            
            case _:
                return super(ProductsBalanceDialog, self).keyPressEvent(event)


    def closeEvent(self, event:QCloseEvent):
        self.balanceChanged.emit(self.products_balance_model.getBalance())
        return super(ProductsBalanceDialog, self).closeEvent(event)

