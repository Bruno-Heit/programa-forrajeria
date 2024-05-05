from PySide6.QtWidgets import (QDialog, QDialogButtonBox, QLineEdit, QCompleter, QListWidget, QListWidgetItem, 
                               QWidget, QVBoxLayout)
from PySide6.QtCore import (QRegularExpression, QObject, Qt, Signal, QSize, QThread)
from PySide6.QtGui import (QRegularExpressionValidator, QIntValidator, QIcon)

from ui.ui_productDialog import Ui_Dialog
from ui.ui_saleDialog import Ui_saleDialog
from ui.ui_listproduct import Ui_listProduct
from ui.ui_debtorDataDialog import Ui_debtorDataDialog
from ui.ui_debtsTable_debtorDetails import Ui_debtorDetails

from resources import (rc_icons)

from re import (search, Match, sub)
from utils.functionutils import *
from utils.workerclasses import *
from utils.dboperations import *

from sqlite3 import (Error as sqlite3Error)
from phonenumbers import (parse, format_number, is_valid_number, PhoneNumber, PhoneNumberFormat, NumberParseException)
from enum import (Enum)


# Enum con estilos generales para labels
class WidgetStyle(Enum):
    '''
    Clase de tipo 'Enum' con estilos generales para aplicar a los widgets.
    '''
    LABEL_NEUTRAL_VAL:str = "color: #555; border: none; background-color: rgba(200,200,200,0.7);"
    FIELD_VALID_VAL:str = "border: 1px solid #40dc26; background-color: rgba(185, 224, 164, 0.7);"
    FIELD_INVALID_VAL:str = "border: 1px solid #dc2627; background-color: rgba(224, 164, 164, 0.7);"
    



# Dialog con datos de un producto
class ProductDialog(QDialog):
    '''QDialog creado al presionar el botón 'MainWindow.btn_add_product_inventory'. Sirve para crear un nuevo registro 
    de producto en la tabla "Productos" en la base de datos.'''
    def __init__(self):
        super(ProductDialog, self).__init__()
        self.productDialog_ui = Ui_Dialog()
        self.productDialog_ui.setupUi(self)
        self.productDialog_ui.buttonBox.button(QDialogButtonBox.Ok).setText("Aceptar")
        # esconde widgets
        self.productDialog_ui.label_nameWarning.hide()
        self.productDialog_ui.label_stockWarning.hide()
        self.productDialog_ui.label_categoryWarning.hide()
        self.productDialog_ui.label_unitPriceWarning.hide()
        self.productDialog_ui.label_comercialPriceWarning.hide()
        
        # desactiva desde el principio el botón "Aceptar"
        self.productDialog_ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
        self.productDialog_ui.buttonBox.button(QDialogButtonBox.Cancel).setText("Cancelar")
        self.productDialog_ui.buttonBox.setStyleSheet("QDialogButtonBox QPushButton[text='Cancelar'] {\
                                                        background-color: #ff4949;\
                                                      }\
                                                      QDialogButtonBox QPushButton[text='Cancelar']:hover,\
                                                      QDialogButtonBox QPushButton[text='Cancelar']:pressed {\
                                                        background-color: #faa;\
                                                      }")
        comboBox_categories:list[str] = getProductsCategories()
        self.productDialog_ui.cb_productCategory.addItems(comboBox_categories)
        
        # validators
        name_validator = ProductNameValidator(self.productDialog_ui.lineedit_productName)
        stock_validator = ProductStockValidator(self.productDialog_ui.lineedit_productStock)
        unit_price_validator = ProductUnitPriceValidator(self.productDialog_ui.lineedit_productUnitPrice)
        comerc_price_validator = ProductComercPriceValidator(self.productDialog_ui.lineedit_productComercialPrice)
        self.productDialog_ui.lineedit_productName.setValidator(name_validator)
        self.productDialog_ui.lineedit_productStock.setValidator(stock_validator)
        self.productDialog_ui.lineedit_productUnitPrice.setValidator(unit_price_validator)
        self.productDialog_ui.lineedit_productComercialPrice.setValidator(comerc_price_validator)
        
        # completers
        self.productDialog_ui.lineedit_productName.setCompleter(createCompleter(type=3))

        # flags de validación
        self.VALID_STOCK:bool = None
        self.VALID_NAME:bool = None
        self.VALID_CATEGORY:bool = None
        self.VALID_UNIT_PRICE:bool = None
        self.VALID_COMERCIAL_PRICE:bool = None

        #--- SEÑALES --------------------------------------------------
        name_validator.validationSucceded.connect(lambda: self.validatorOnValidationSucceded('name'))
        stock_validator.validationSucceded.connect(lambda: self.validatorOnValidationSucceded('stock'))
        unit_price_validator.validationSucceded.connect(lambda: self.validatorOnValidationSucceded('unit_price'))
        comerc_price_validator.validationSucceded.connect(lambda: self.validatorOnValidationSucceded('comerc_price'))
        
        name_validator.validationFailed.connect(lambda error_message: self.validatorOnValidationFailed(
            field_validated='name',
            error_message=error_message))
        stock_validator.validationFailed.connect(lambda error_message: self.validatorOnValidationFailed(
            field_validated='stock',
            error_message=error_message))
        unit_price_validator.validationFailed.connect(lambda error_message: self.validatorOnValidationFailed(
            field_validated='unit_price',
            error_message=error_message))
        comerc_price_validator.validationFailed.connect(lambda error_message: self.validatorOnValidationFailed(
            field_validated='comerc_price',
            error_message=error_message))
        
        self.productDialog_ui.cb_productCategory.currentIndexChanged.connect(self.__checkProductCategoryValidity)
        self.productDialog_ui.lineedit_productStock.editingFinished.connect(lambda: self.formatField('stock'))
        self.productDialog_ui.lineedit_productUnitPrice.editingFinished.connect(lambda: self.formatField('unit_price'))
        self.productDialog_ui.lineedit_productComercialPrice.editingFinished.connect(lambda: self.formatField('comerc_price'))
        
        self.productDialog_ui.buttonBox.accepted.connect(self.addProductToDatabase)
    
    #### MÉTODOS #####################################################
    @Slot(str)
    def validatorOnValidationSucceded(self, field_validated:str) -> None:
        '''
        Cambia el valor del flag asociado al campo que fue validado 'field_validated' a True, cambia el 
        QSS del campo y esconde el QLabel asociado al campo.
        Al finalizar, llama a 'self.verifyFieldsValidity' para comprobar si el resto de campos son válidos.
        
        PARAMS:
        - field_validated: el campo que fue validado. Sus posibles valores son:
            - name: se validó el campo de nombre del producto.
            - stock: se validó el campo de stock del producto.
            - unit_price: se validó el campo de precio unitario del producto.
            - comerc_price: se validó el campo de precio comercial del producto.
        
        Retorna None.
        '''
        match field_validated:
            case 'name':
                self.VALID_NAME = True
                self.productDialog_ui.lineedit_productName.setStyleSheet(WidgetStyle.FIELD_VALID_VAL.value)
                self.productDialog_ui.label_nameWarning.hide()
            
            case 'stock':
                self.VALID_STOCK = True
                self.productDialog_ui.lineedit_productStock.setStyleSheet(WidgetStyle.FIELD_VALID_VAL.value)
                self.productDialog_ui.label_stockWarning.hide()
            
            case 'unit_price':
                self.VALID_UNIT_PRICE = True
                self.productDialog_ui.lineedit_productUnitPrice.setStyleSheet(WidgetStyle.FIELD_VALID_VAL.value)
                self.productDialog_ui.label_unitPriceWarning.hide()
            
            case 'comerc_price':
                self.VALID_COMERCIAL_PRICE = True
                self.productDialog_ui.lineedit_productComercialPrice.setStyleSheet(WidgetStyle.FIELD_VALID_VAL.value)
                self.productDialog_ui.label_comercialPriceWarning.hide()
        
        self.verifyFieldsValidity()
        return None
    
    
    @Slot(str, str)
    def validatorOnValidationFailed(self, field_validated:str, error_message:str) -> None:
        '''
        Cambia el valor del flag asociado al campo que fue validado 'field_validated' a False, cambia el 
        QSS del campo y muestra el QLabel asociado al campo con el mensaje 'error_message' con feedback.
        
        Retorna None.
        '''
        match field_validated:
            case 'name':
                self.VALID_NAME = False
                self.productDialog_ui.lineedit_productName.setStyleSheet(WidgetStyle.FIELD_INVALID_VAL.value)
                self.productDialog_ui.label_nameWarning.show()
                self.productDialog_ui.label_nameWarning.setText(error_message)
            
            case 'stock':
                self.VALID_STOCK = False
                self.productDialog_ui.lineedit_productStock.setStyleSheet(WidgetStyle.FIELD_INVALID_VAL.value)
                self.productDialog_ui.label_stockWarning.show()
                self.productDialog_ui.label_stockWarning.setText(error_message)
            
            case 'unit_price':
                self.VALID_UNIT_PRICE = False
                self.productDialog_ui.lineedit_productUnitPrice.setStyleSheet(WidgetStyle.FIELD_INVALID_VAL.value)
                self.productDialog_ui.label_unitPriceWarning.show()
                self.productDialog_ui.label_unitPriceWarning.setText(error_message)
            
            case 'comerc_price':
                self.VALID_COMERCIAL_PRICE = False
                self.productDialog_ui.lineedit_productComercialPrice.setStyleSheet(WidgetStyle.FIELD_INVALID_VAL.value)
                self.productDialog_ui.label_comercialPriceWarning.show()
                self.productDialog_ui.label_comercialPriceWarning.setText(error_message)
        
        return None
    
    
    @Slot(str)
    def formatField(self, field_to_format:str) -> None:
        '''
        Dependiendo del campo 'field_to_format' formatea el texto y lo asigna en el QLineEdit correspondiente.
        
        Retorna None.
        '''
        match field_to_format:
            case 'stock': # cambia los puntos decimales por comas
                self.productDialog_ui.lineedit_productStock.setText(self.productDialog_ui.lineedit_productStock.text().replace(".",","))
            
            case 'unit_price': # cambia los puntos decimales por comas
                self.productDialog_ui.lineedit_productUnitPrice.setText(self.productDialog_ui.lineedit_productUnitPrice.text().replace(".",","))
            
            case 'comerc_price': # cambia los puntos decimales por comas
                self.productDialog_ui.lineedit_productComercialPrice.setText(self.productDialog_ui.lineedit_productComercialPrice.text().replace(".",","))
        
        return None
    
    
    @Slot()
    def __checkProductCategoryValidity(self) -> None:
        '''
        Verifica si 'cb_productCategory' tiene una categoría seleccionada. Si la tiene, se considera válido y 
        'self.VALID_CATEGORY' será True, sino False. Modifica el texto de 'label_categoryWarning' de acuerdo a las 
        condiciones, y el estilo del campo.
        Al finalizar, si el campo es válido llama a 'self.verifyFieldsValidity' para comprobar si el resto de campos 
        son válidos.
        
        Retorna None.
        '''
        # reinicio la validez de la categoría
        self.VALID_CATEGORY = True
        current_text:str = self.productDialog_ui.cb_productCategory.currentText().strip()
        # si no se eligió una categoría para el producto...
        if current_text == "":
            self.VALID_CATEGORY = False
            self.productDialog_ui.cb_productCategory.setCurrentIndex(-1)
        if self.productDialog_ui.cb_productCategory.currentIndex() == -1:
            self.VALID_CATEGORY = False
            self.productDialog_ui.label_categoryWarning.setText("Se debe seleccionar una categoría para el producto")
            self.productDialog_ui.cb_productCategory.setStyleSheet(WidgetStyle.FIELD_INVALID_VAL.value)

        if current_text and self.VALID_CATEGORY:
            self.productDialog_ui.label_categoryWarning.setText("")
            self.productDialog_ui.cb_productCategory.setStyleSheet(WidgetStyle.FIELD_VALID_VAL.value)
            self.verifyFieldsValidity()
        else:
            self.productDialog_ui.cb_productCategory.setStyleSheet(WidgetStyle.FIELD_INVALID_VAL.value)
        return None


    def verifyFieldsValidity(self) -> None:
        '''
        Es llamada desde los métodos 'self.validatorOnValidationSucceded' y 'self.__checkProductCategoryValidity'.
        
        Verifica que todos los campos tengan valores válidos. Compara si todos son válidos y activa o desactiva el 
        botón "Aceptar" dependiendo del caso.
        
        Retorna None.
        '''
        valid:tuple[bool] = (
            self.VALID_NAME,
            self.VALID_CATEGORY,
            self.VALID_STOCK,
            self.VALID_UNIT_PRICE,
            self.VALID_COMERCIAL_PRICE
        )
        # verifica si todos los valores de la tupla son True y activa o desactiva el botón...
        if all(valid):
            self.productDialog_ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)
        else:
            self.productDialog_ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
        return None


    # funciones del botón Ok
    def __getFieldsData(self) -> tuple[str]:
        '''
        Es llamada desde 'self.addProductToDatabase'.
        
        Obtiene todos los datos introducidos en los campos y los devuelve como una tupla de strings.
        
        Retorna un tuple[str].
        '''
        # obtengo los datos de los campos
        data:tuple[str] = (
            self.productDialog_ui.lineedit_productName.text().strip(),
            self.productDialog_ui.lineedit_productDescription.text().strip(),
            self.productDialog_ui.lineedit_productStock.text().replace(",","."),
            self.productDialog_ui.lineedit_measurementUnit.text().strip(),
            self.productDialog_ui.lineedit_productUnitPrice.text().replace(",",".").strip(),
            self.productDialog_ui.lineedit_productComercialPrice.text().replace(",",".").strip(),
            self.productDialog_ui.cb_productCategory.currentText()
        )
        return data


    @Slot()
    def addProductToDatabase(self) -> None:
        '''
        Es llamada cuando se presiona el botón "Aceptar".
        
        Obtiene los datos de los campos y hace una consulta INSERT INTO a la base de datos.
        
        Retorna None.
        '''
        try:
            conn = createConnection("database/inventario.db")
            cursor = conn.cursor()
            
            if self.productDialog_ui.buttonBox.button(QDialogButtonBox.Ok).isEnabled() == False:
                return None
            data:tuple[str] = self.__getFieldsData()
            sql = "INSERT INTO Productos(nombre,descripcion,stock,unidad_medida,precio_unit,precio_comerc,IDcategoria,eliminado) VALUES(?,?,?,?,?,?,(SELECT IDcategoria FROM Categorias WHERE nombre_categoria=?),0);"

            cursor.execute(sql, data)
            conn.commit()
            
        except sqlite3Error as err:
            conn.rollback()
            print(f"{err.sqlite_errorcode}: {err.sqlite_errorname} / {err}")
            
        finally:
            conn.close()
        
        return None


# ==============================================================================================================


# Dialog con datos de la venta -y del deudor si se debe algo/hay algo a favor-
class SaleDialog(QDialog):
    '''QDialog creado al presionar el botón 'MainWindow.btn_add_product_sales'. Sirve para crear un nuevo registro 
    de venta en la tabla "Ventas", de detalles de venta en "Detalle_Ventas", de deuda en "Deudas" (si hay diferencia 
    entre lo abonado y el costo total) y de deudor en "Deudores" (si hay deuda) en la base de datos.'''
    def __init__(self):
        super(SaleDialog, self).__init__()
        self.saleDialog_ui = Ui_saleDialog()
        self.saleDialog_ui.setupUi(self)

        self.setWindowTitle("Nueva venta")

        self.saleDialog_ui.buttonBox.button(QDialogButtonBox.Ok).setText("Aceptar")
        # desactiva desde el principio el botón "Aceptar"
        self.saleDialog_ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
        self.saleDialog_ui.buttonBox.button(QDialogButtonBox.Cancel).setText("Cancelar")
        self.saleDialog_ui.buttonBox.setStyleSheet("QDialogButtonBox QPushButton[text='Cancelar'] {\
                                                        background-color: #ff4949;\
                                                      }\
                                                      QDialogButtonBox QPushButton[text='Cancelar']:hover,\
                                                      QDialogButtonBox QPushButton[text='Cancelar']:pressed {\
                                                        background-color: #faa;\
                                                      }")
        self.saleDialog_ui.comboBox_productName.addItems(getProductNames())
        self.saleDialog_ui.dateTimeEdit.setStyleSheet(
            "QDateTimeEdit {\
                background-color: #fff;\
            }\
            \
            \
            QCalendarWidget QAbstractItemView {\
                background-color: #fff;\
                selection-background-color: #38a3a5;\
            }\
            QCalendarWidget QToolButton {\
                background-color: #22577a;\
                color: #fff;\
            }\
            QCalendarWidget QToolButton:hover,\
            QCalendarWidget QToolButton:pressed {\
                background-color: #38a3a5;\
                color: #111;\
            }\
            \
            \
            QCalendarWidget QWidget#qt_calendar_prevmonth{\
                qproperty-icon: url(':/icons/arrow-left-white.svg')\
            }\
            QCalendarWidget QWidget#qt_calendar_nextmonth{\
                qproperty-icon: url(':/icons/arrow-right-white.svg')\
            }")
        self.saleDialog_ui.dateTimeEdit.setDateTime(QDateTime.currentDateTime())

        # esconde widgets
        self.saleDialog_ui.label_productName_feedback.hide()
        self.saleDialog_ui.label_productQuantity_feedback.hide()
        self.saleDialog_ui.label_totalPaid_feedback.hide()

        # esconde los campos de datos del deudor
        self.saleDialog_ui.debtor_data.setEnabled(False)
        self.saleDialog_ui.debtor_data.hide()

        # QCompleters #! estos completers son "iniciales" y cambian cuando el usuario escribe en uno de ellos.
                      #! Al principio tienen todos los valores de nombres/apellidos de la base de datos, pero 
                      #! al ingresar por ej. un nombre el campo de apellido se actualiza con los apellidos que 
                      #! coincidan con ese nombre, y viceversa. Eso se maneja en 'onDebtorNameAndSurnameEditingFinished'.
        self.saleDialog_ui.lineEdit_debtorName.setCompleter(createCompleter(type=1))
        self.saleDialog_ui.lineEdit_debtorSurname.setCompleter(createCompleter(type=2))

        # validadores de venta
        self.sale_detail_validator = SaleDetailsValidator(self.saleDialog_ui.lineEdit_saleDetail)
        self.quantity_validator = SaleQuantityValidator(self.saleDialog_ui.lineEdit_productQuantity)
        self.total_paid_validator = SalePaidValidator(self.saleDialog_ui.lineEdit_totalPaid)
        self.saleDialog_ui.lineEdit_saleDetail.setValidator(self.sale_detail_validator)
        self.saleDialog_ui.lineEdit_productQuantity.setValidator(self.quantity_validator)
        self.saleDialog_ui.lineEdit_totalPaid.setValidator(self.total_paid_validator)
        # validadores de cuenta corriente
        self.debtor_name_validator = DebtorNameValidator(self.saleDialog_ui.lineEdit_debtorName)
        self.debtor_surname_validator = DebtorSurnameValidator(self.saleDialog_ui.lineEdit_debtorSurname)
        self.phone_number_validator = DebtorPhoneNumberValidator(self.saleDialog_ui.lineEdit_phoneNumber)
        self.postal_code_validator = DebtorPostalCodeValidator(self.saleDialog_ui.lineEdit_postalCode)
        self.saleDialog_ui.lineEdit_debtorName.setValidator(self.debtor_name_validator)
        self.saleDialog_ui.lineEdit_debtorSurname.setValidator(self.debtor_surname_validator)
        self.saleDialog_ui.lineEdit_phoneNumber.setValidator(self.phone_number_validator)
        self.saleDialog_ui.lineEdit_postalCode.setValidator(self.postal_code_validator)
        
        # flags de validación
        self.VALID_FIELDS:dict[str,bool|None] = {
            'PRODUCT_NAME': None,
            'PRODUCT_QUANTITY': None,
            'PRODUCT_PAID': None,
            'DEBTOR_NAME': None,
            'DEBTOR_SURNAME': None,
            'DEBTOR_PHONE_NUMBER': True, # el número de tel. es opcional, así que si está vacío es válido...
            'DEBTOR_POSTAL_CODE': True # y el código postal también
        }
        
        # variables
        self.TOTAL_COST:float|None = None # se obtiene en __setDetailsAndCost, si el precio está disponible, sino es None
        
        
        #--- SEÑALES --------------------------------------------------
        # combobox nombre de producto (venta)
        self.saleDialog_ui.comboBox_productName.currentIndexChanged.connect(self.validateProductNameField)
        
        # lineedit cantidad (venta)
        self.saleDialog_ui.lineEdit_productQuantity.editingFinished.connect(lambda: self.formatField('product_quantity'))
        
        self.quantity_validator.validationSucceded.connect(lambda: self.validatorOnValidationSucceded('product_quantity'))
        self.quantity_validator.validationFailed.connect(lambda error_message: self.validatorOnValidationFailed(
            field_validated='product_quantity',
            error_message=error_message))
        
        # checkbox de tipo de precio (venta)
        self.saleDialog_ui.checkBox_comercialPrice.clicked.connect(
            lambda: self.handleNameAndQuantityAndPriceChange() if self.VALID_FIELDS['PRODUCT_QUANTITY'] else None)
        
        # lineedit total pago (venta)
        self.saleDialog_ui.lineEdit_totalPaid.editingFinished.connect(self.onTotalPaidEditingFinished)
        
        self.total_paid_validator.validationSucceded.connect(lambda: self.validatorOnValidationSucceded('product_total_paid'))
        self.total_paid_validator.validationFailed.connect(lambda error_message: self.validatorOnValidationFailed(
            field_validated='product_total_paid',
            error_message=error_message))
        
        # lineedit nombre (cuenta corriente)
        self.saleDialog_ui.lineEdit_debtorName.editingFinished.connect(lambda: self.onDebtorNameAndSurnameEditingFinished(
            field_validated='debtor_name'))
        
        self.debtor_name_validator.validationSucceded.connect(lambda: self.validatorOnValidationSucceded('debtor_name'))
        self.debtor_name_validator.validationFailed.connect(lambda error_message: self.validatorOnValidationFailed(
            field_validated='debtor_name',
            error_message=error_message))
        
        # lineedit apellido (cuenta corriente)
        self.saleDialog_ui.lineEdit_debtorSurname.editingFinished.connect(lambda: self.onDebtorNameAndSurnameEditingFinished(
            field_validated='debtor_surname'))
        
        self.debtor_surname_validator.validationSucceded.connect(lambda: self.validatorOnValidationSucceded('debtor_surname'))
        self.debtor_surname_validator.validationFailed.connect(lambda error_message: self.validatorOnValidationFailed(
            field_validated='debtor_surname',
            error_message=error_message))
        
        # lineedit núm. de tel. (cuenta corriente)
        self.saleDialog_ui.lineEdit_phoneNumber.editingFinished.connect(lambda: self.formatField('debtor_phone_num'))
        
        self.phone_number_validator.validationSucceded.connect(lambda: self.validatorOnValidationSucceded('debtor_phone_num'))
        self.phone_number_validator.validationFailed.connect(lambda error_message: self.validatorOnValidationFailed(
            field_validated='debtor_phone_num',
            error_message=error_message))
        
        # lineedit cód. postal (cuenta corriente)
        self.postal_code_validator.validationSucceded.connect(lambda: self.validatorOnValidationSucceded('debtor_postal_code'))
        self.postal_code_validator.validationFailed.connect(lambda error_message: self.validatorOnValidationFailed(
            field_validated='debtor_postal_code',
            error_message=error_message))
        
        # botón Ok (Aceptar)
        self.saleDialog_ui.buttonBox.accepted.connect(self.handleOkClicked)

    #### MÉTODOS #####################################################
    @Slot(str)
    def validatorOnValidationSucceded(self, field_validated:str) -> None:
        '''
        Cambia el valor del flag asociado al campo que fue validado 'field_validated' a True, cambia el 
        QSS del campo y esconde el QLabel asociado al campo, excepto si 'debtor_quantity' donde no esconde 
        el QLabel sino que cambia su QSS.
        Al finalizar, llama a 'self.verifyFieldsValidity' para comprobar si el resto de campos son válidos.
        
        PARAMS:
        - field_validated: el campo que se valida. Admite los siguientes valores:
            - product_quantity: se valida el campo de cantidad del producto.
            - product_total_paid: se valida el campo de total abonado del producto.
            - debtor_name: se valida el campo de nombre del deudor.
            - debtor_surname: se valida el campo de apellido del deudor.
            - debtor_phone_num: se valida el campo de teléfono del deudor.
            - debtor_postal_code: se valida el campo de código postal del deudor.
        
        Retorna None.
        '''
        match field_validated:
            case 'product_quantity':
                # sólo puedo validar completamente la cantidad cuando el nombre sea válido
                if self.VALID_FIELDS['PRODUCT_NAME']:
                    self.VALID_FIELDS['PRODUCT_QUANTITY'] = True
                    self.saleDialog_ui.lineEdit_productQuantity.setStyleSheet(WidgetStyle.FIELD_VALID_VAL.value)
                    self.saleDialog_ui.label_productQuantity_feedback.setText(f"El stock disponible es de {self.quantity_validator.AVAILABLE_STOCK[0]} {self.quantity_validator.AVAILABLE_STOCK[1]}")
                
                    # actualiza los detalles de venta, costo total y crea un completer para el campo de total abonado
                    self.handleNameAndQuantityAndPriceChange()
                
                # sea el nombre válido o no, igualmente cambia los estilos del label y el lineedit
                self.saleDialog_ui.label_productQuantity_feedback.setStyleSheet(WidgetStyle.LABEL_NEUTRAL_VAL.value)
                self.saleDialog_ui.lineEdit_productQuantity.setStyleSheet(WidgetStyle.FIELD_VALID_VAL.value)
                if not "El stock disponible" in self.saleDialog_ui.label_productQuantity_feedback.text():
                    self.saleDialog_ui.label_productQuantity_feedback.setText("")

            
            case 'product_total_paid':
                self.VALID_FIELDS['PRODUCT_PAID'] = True
                self.saleDialog_ui.lineEdit_totalPaid.setStyleSheet(WidgetStyle.FIELD_VALID_VAL.value)
                self.saleDialog_ui.label_totalPaid_feedback.hide()
            
            case 'debtor_name':
                self.VALID_FIELDS['DEBTOR_NAME'] = True
                self.saleDialog_ui.lineEdit_debtorName.setStyleSheet(WidgetStyle.FIELD_VALID_VAL.value)
                self.saleDialog_ui.label_debtorName_feedback.hide()
            
            case 'debtor_surname':
                self.VALID_FIELDS['DEBTOR_SURNAME'] = True
                self.saleDialog_ui.lineEdit_debtorSurname.setStyleSheet(WidgetStyle.FIELD_VALID_VAL.value)
                self.saleDialog_ui.label_debtorSurname_feedback.hide()
            
            case 'debtor_phone_num':
                self.VALID_FIELDS['DEBTOR_PHONE_NUMBER'] = True
                if self.saleDialog_ui.lineEdit_phoneNumber.text() != "":
                    self.saleDialog_ui.lineEdit_phoneNumber.setStyleSheet(WidgetStyle.FIELD_VALID_VAL.value)
                else:
                    self.saleDialog_ui.lineEdit_phoneNumber.setStyleSheet("")
                
                self.saleDialog_ui.label_phoneNumber_feedback.hide()
            
            case 'debtor_postal_code':
                self.VALID_FIELDS['DEBTOR_POSTAL_CODE'] = True
                if self.saleDialog_ui.lineEdit_postalCode.text() != "":
                    self.saleDialog_ui.lineEdit_postalCode.setStyleSheet(WidgetStyle.FIELD_VALID_VAL.value)
                else:
                    self.saleDialog_ui.lineEdit_postalCode.setStyleSheet("")
                    
                self.saleDialog_ui.label_postalCode_feedback.hide()
        
        self.verifyFieldsValidity()
        return None
        
    
    @Slot(str, str)
    def validatorOnValidationFailed(self, field_validated:str, error_message:str) -> None:
        '''
        Cambia el valor del flag asociado al campo que fue validado 'field_validated' a False, cambia el 
        QSS del campo y muestra el QLabel asociado al campo con el mensaje 'error_message' con feedback.
        
        PARAMS:
        - field_validated: el campo que se valida. Admite los siguientes valores:
            - product_quantity: se valida el campo de cantidad del producto.
            - product_total_paid: se valida el campo de total abonado del producto.
            - debtor_name: se valida el campo de nombre del deudor.
            - debtor_surname: se valida el campo de apellido del deudor.
            - debtor_phone_num: se valida el campo de teléfono del deudor.
            - debtor_postal_code: se valida el campo de código postal del deudor.
        
        Retorna None.
        '''
        match field_validated:
            case 'product_quantity':
                self.VALID_FIELDS['PRODUCT_QUANTITY'] = False
                self.saleDialog_ui.lineEdit_productQuantity.setStyleSheet(WidgetStyle.FIELD_INVALID_VAL.value)
                self.saleDialog_ui.label_productQuantity_feedback.show()
                # resetea el estilo del campo (por defecto es rojo, igual que los otros de feedback)
                self.saleDialog_ui.label_productQuantity_feedback.setStyleSheet("")
                self.saleDialog_ui.label_productQuantity_feedback.setText(error_message)
            
            case 'product_total_paid':
                self.VALID_FIELDS['PRODUCT_PAID'] = False
                self.saleDialog_ui.lineEdit_totalPaid.setStyleSheet(WidgetStyle.FIELD_INVALID_VAL.value)
                self.saleDialog_ui.label_totalPaid_feedback.show()
                self.saleDialog_ui.label_totalPaid_feedback.setText(error_message)
            
            case 'debtor_name':
                self.VALID_FIELDS['DEBTOR_NAME'] = False
                self.saleDialog_ui.lineEdit_debtorName.setStyleSheet(WidgetStyle.FIELD_INVALID_VAL.value)
                self.saleDialog_ui.label_debtorName_feedback.show()
                self.saleDialog_ui.label_debtorName_feedback.setText(error_message)
            
            case 'debtor_surname':
                self.VALID_FIELDS['DEBTOR_SURNAME'] = False
                self.saleDialog_ui.lineEdit_debtorSurname.setStyleSheet(WidgetStyle.FIELD_INVALID_VAL.value)
                self.saleDialog_ui.label_debtorSurname_feedback.show()
                self.saleDialog_ui.label_debtorSurname_feedback.setText(error_message)
            
            case 'debtor_phone_num':
                self.VALID_FIELDS['DEBTOR_PHONE_NUMBER'] = False
                self.saleDialog_ui.lineEdit_phoneNumber.setStyleSheet(WidgetStyle.FIELD_INVALID_VAL.value)
                self.saleDialog_ui.label_phoneNumber_feedback.show()
                self.saleDialog_ui.label_phoneNumber_feedback.setText(error_message)
            
            case 'debtor_postal_code':
                self.VALID_FIELDS['DEBTOR_POSTAL_CODE'] = False
                self.saleDialog_ui.lineEdit_postalCode.setStyleSheet(WidgetStyle.FIELD_INVALID_VAL.value)
                self.saleDialog_ui.label_postalCode_feedback.show()
                self.saleDialog_ui.label_postalCode_feedback.setText(error_message)
        
        self.verifyFieldsValidity()
        return None

    
    def __getCurrentProductStock(self, product_name:str) -> tuple[float,str]:
        '''
        Hace una consulta SELECT y obtiene el stock actual del producto ingresado. 
        
        Retorna una tupla con el stock como número y la unidad de medida como 'str'.
        '''
        conn:Connection | None
        stock:float
        measurement_unit:str

        conn = createConnection("database/inventario.db")
        if not conn:
            return None
        cursor = conn.cursor()
        query = cursor.execute("SELECT stock, unidad_medida FROM Productos WHERE nombre = ?;", (product_name,)).fetchone()
        if len(query) == 2:
            stock, measurement_unit = [q for q in query]
        else:
            stock = query[0]
            measurement_unit = ""
        
        try:
            stock = float(stock)
        except:
            pass
        return stock, measurement_unit
    
    
    @Slot()
    def validateProductNameField(self) -> None:
        '''
        Es llamado desde la señal 'currentIndexChanged' cuando el campo validado es el de nombre del producto.
        
        Este método hace lo siguiente:
        1. actualiza self.VALID_FIELDS['PRODUCT_NAME'] dependiendo de la validez del campo...
        2. esconde/muestra y cambia el texto de 'label_productName_feedback' dependiendo de la validez...
        3. cambia el estilo del QLabel de feedback asociado y del propio QComboBox...
        4. coloca el stock disponible en 'label_productQuantity_feedback' con un estilo personalizado.
        5. si el campo es válido obtiene el stock del producto y lo guarda en 'SaleQuantityValidator.AVAILABLE_STOCK'.
        6. si el campo es válido comprueba si también lo es la cantidad y de ser ambos válidos llama a 
        'self.__setSaleDetails' y a 'self.__setProductTotalCost'.
        
        Este método llama a:
        - SaleQuantityValidator.setsetAvailableStock: para almacenar en el validador de cantidad el 
        stock disponible.
        - self.__getCurrentProductStock: para actualizar el stock disponible en 'self.AVAILABLE_STOCK'.
        - self.__setSaleDetails: para actualizar los detalles de venta.
        - self.__setProductTotalCost: para actualizar el costo total de la venta.
        
        Retorna None.
        '''
        # si no se eligió el nombre del producto asigna el índice -1
        if self.saleDialog_ui.comboBox_productName.currentText().strip() == "":
            self.VALID_FIELDS['PRODUCT_NAME'] = False
            self.saleDialog_ui.comboBox_productName.setCurrentIndex(-1)
        
        # si no hay un producto seleccionado (si índice es -1)...
        if self.saleDialog_ui.comboBox_productName.currentIndex() == -1:
            self.VALID_FIELDS['PRODUCT_NAME'] = False
            self.saleDialog_ui.label_productName_feedback.show()
            self.saleDialog_ui.label_productName_feedback.setText("El campo de nombre del producto no puede estar vacío")
            self.saleDialog_ui.comboBox_productName.setStyleSheet(WidgetStyle.FIELD_INVALID_VAL.value)
        
        # si el campo es válido...
        else:
            self.VALID_FIELDS['PRODUCT_NAME'] = True
            self.saleDialog_ui.label_productName_feedback.hide()
            self.saleDialog_ui.comboBox_productName.setStyleSheet(WidgetStyle.FIELD_VALID_VAL.value)
            
            # guarda el stock del producto en el validador de cantidad
            self.quantity_validator.setAvailableStock(self.__getCurrentProductStock(
                self.saleDialog_ui.comboBox_productName.itemText(self.saleDialog_ui.comboBox_productName.currentIndex()) ))
            
            # coloca el stock en 'label_productQuantity_feedback'
            self.saleDialog_ui.label_productQuantity_feedback.show()
            self.saleDialog_ui.label_productQuantity_feedback.setStyleSheet(WidgetStyle.LABEL_NEUTRAL_VAL.value)
            self.saleDialog_ui.label_productQuantity_feedback.setText(f"El stock disponible es de {self.quantity_validator.AVAILABLE_STOCK[0]} {self.quantity_validator.AVAILABLE_STOCK[1]}")
            
            #? llama a validar la cantidad porque, si se modificó primero la cantidad y el válida, y luego 
            #? se elige un nombre de producto que es válido pero no tiene esa cantidad en stock entonces 
            #? el campo de cantidad devuelve un "falso positivo"... de ésta forma se arregla
            self.quantity_validator.validate(self.saleDialog_ui.lineEdit_productQuantity.text(), 0)
            
            # si también la cantidad es válida, actualiza los detalles de venta y el costo total...
            if self.VALID_FIELDS['PRODUCT_QUANTITY']:
                self.handleNameAndQuantityAndPriceChange()
            
        return None


    @Slot()
    def handleNameAndQuantityAndPriceChange(self) -> None:
        '''
        Es llamado desde:
        - self.validateProductNameField: cuando el índice de 'comboBox_productName' cambia.
        - self.validatorOnValidationSucceded: cuando el valor de 'lineEdit_productQuantity' cambia.
        - la señal 'checkBox_comercialPrice.clicked': cuando el estado de 'checkBox_comercialPrice' cambia.
        
        Cambia el texto del QLabel de precio total, coloca los detalles de la venta en su QLineEdit 
        y crea un QCompleter para el campo de cantidad abonada.
        Coloca el costo total en 'SalePaidValidator.TOTAL_COST' y llama a su método 'validate()'.
        Por último, al finalizar llama a 'self.verifyFieldsValidity'.
        
        Este método llama a:
        - self.__setDetailsAndCost: para actualizar los detalles de venta y el costo total.
        - SalePaidValidator.validate: para revalidar el campo de 'lineEdit_totalPaid'.
        - self.verifyFieldsValidity: para revisar el estado de validez de los campos y cambiar el estado 
        de visibilidad de 'debtor_data'.
        
        Retorna None.
        '''
        # cambia los detalles de venta y el label con el costo total
        self.__setDetailsAndCost()
        
        # coloca el costo total en el validador 'SalePaidValidator.TOTAL_COST' y llama a validate()
        self.total_paid_validator.TOTAL_COST = self.TOTAL_COST
        self.total_paid_validator.validate(self.saleDialog_ui.lineEdit_totalPaid.text(), 0)
        
        # coloca un completer en self.lineEdit_totalPaid
        if self.TOTAL_COST:
            total_paid_completer = QCompleter([ str(self.TOTAL_COST).replace(".",",") ])
            total_paid_completer.setCompletionMode(QCompleter.CompletionMode.InlineCompletion)
            
            self.saleDialog_ui.lineEdit_totalPaid.setCompleter(total_paid_completer)
            
            # establece el modo de completado a medida que se escribe
            self.saleDialog_ui.lineEdit_totalPaid.textChanged.connect(total_paid_completer.setCompletionPrefix)
        
        # verifica otra vez la validez de los campos y cambia la visiblidad de debtor_data
        self.verifyFieldsValidity(TOGGLE_DEBTOR_DATA=True)
        return None
    
    
    def __setDetailsAndCost(self) -> str:
        '''
        Es llamado desde 'self.handleNameAndQuantityAndPriceChange'.
        
        Obtiene el precio normal ó comercial dependiendo de si 'checkBox_comercialPrice' está checkeada, luego 
        obtiene el costo desde la base de datos y lo calcula a partir de la cantidad ingresada y cambia el texto 
        de 'label_productTotalCost' de acuerdo al costo total.
        Luego coloca la cantidad del producto vendido, el nombre y el tipo de precio aplicado en 'lineEdit_saleDetail'.
        
        Retorna el costo total como str, y además con el texto "NO DISPONIBLE" si no existe.
        '''
        total_cost:float|str # si existe el float, sino un str con "NO DISPONIBLE"
        pattern:Pattern = compile(
            pattern="[0-9]{1,8}(\.|,)?[0-9]{0,2}\sde .{1,}\s(\([\s]*P[\s]*\.[\s]*NORMAL[\s]*\)|\([\s]*P[\s]*\.[\s]*COMERCIAL[\s]*\))$",
            flags=IGNORECASE)
        re:Match | str
        new_text:str
        
        # ======== PRECIO ====================================================
        # obtiene el precio normal/comercial
        conn = createConnection("database/inventario.db")
        cursor = conn.cursor()
        
        if self.saleDialog_ui.checkBox_comercialPrice.isChecked():
            sql = "SELECT ? * precio_comerc FROM Productos WHERE nombre = ?;"
        else:
            sql = "SELECT ? * precio_unit FROM Productos WHERE nombre = ?;"
        params = (
            float(self.saleDialog_ui.lineEdit_productQuantity.text().replace(",",".")),
            self.saleDialog_ui.comboBox_productName.itemText(self.saleDialog_ui.comboBox_productName.currentIndex()),)
        
        # obtiene el costo total
        total_cost = cursor.execute(sql, params).fetchone()[0]
        
        # si el valor no existe en base de datos devuelve TypeError
        try:
            if total_cost == 0 or total_cost == 0.0:
                total_cost = "NO DISPONIBLE"
            
            else:
                total_cost = f"$ {round(float(total_cost), 2)}"
                total_cost = total_cost.replace(".",",")
            
        except TypeError: # no puede convertir None a float
            total_cost = "NO DISPONIBLE"
        
        # coloca el precio total
        self.saleDialog_ui.label_productTotalCost.setText(f"<html><head/><body><p><span style=\" font-size:20px; color: #111;\">COSTO TOTAL </span><span style=\" font-size: 20px; color: #22577a;\">{total_cost}</span></p></body></html>")
        
        # guarda en una variable global el costo total
        self.TOTAL_COST = float(total_cost.lstrip("$").replace(" ","").replace(",",".")) if total_cost != "NO DISPONIBLE" else None
        
        # ======== DETALLES DE LA VENTA ======================================
        
        # obtiene los valores de cantidad, nombre del producto y tipo de precio (normal ó comercial)
        quantity = self.saleDialog_ui.lineEdit_productQuantity.text()
        product_name = self.saleDialog_ui.comboBox_productName.currentText()
        price_type = "P. COMERCIAL" if self.saleDialog_ui.checkBox_comercialPrice.isChecked() else "P. NORMAL"

        re = match(pattern, self.saleDialog_ui.lineEdit_saleDetail.text())
        re = re.group() if re else None
        # verifica si 'pattern' coincide, y si coincide reemplaza el texto (significa que no lo escribió el usuario)
        if self.saleDialog_ui.lineEdit_saleDetail.text().strip() == re or self.saleDialog_ui.lineEdit_saleDetail.text().strip() == "":
            self.saleDialog_ui.lineEdit_saleDetail.setText(f"{quantity} de {product_name} ({price_type})")
        
        # si no coincide es porque lo escribió el usuario (sólo reemplaza el tipo de precio)
        else:
            new_text = self.saleDialog_ui.lineEdit_saleDetail.text()
            new_text = sub(
                pattern="(\([\s]*P[\s]*\.[\s]*NORMAL[\s]*\)|\([\s]*P[\s]*\.[\s]*COMERCIAL[\s]*\))$",
                repl="",
                string=self.saleDialog_ui.lineEdit_saleDetail.text(),
                flags=IGNORECASE)
            new_text = f"{new_text.strip()} ({price_type})"
            
            self.saleDialog_ui.lineEdit_saleDetail.setText(new_text)
        
        return None

    
    @Slot()
    def onTotalPaidEditingFinished(self) -> None:
        '''
        Es llamado desde la señal 'editingFinished' de 'lineEdit_totalPaid'.
        
        Llama a 'self.formatField' para formatear el valor del QLineEdit y luego llama a 'self.verifyFieldsValidity'.
        
        Retorna None.
        '''
        self.formatField(field_to_format='product_total_paid')
        
        self.verifyFieldsValidity(TOGGLE_DEBTOR_DATA=True)
        
        return None


    @Slot()
    def onDebtorNameAndSurnameEditingFinished(self, field_validated:str) -> None:
        '''
        Es llamado desde la señal 'editingFinished' de 'lineEdit_debtorName'|'lineEdit_debtorSurname'.
        
        Crea un QCompleter para el campo opuesto, es decir, si 'field_validated' es 'debtor_name' crea un 
        completer para 'debtor_surname', y viceversa.
        Llama al método 'self.formatField' para formatear los campos y si existe esa combinación de nombre y 
        apellido busca el número de teléfono, la dirección y el código postal existente del usuario y los 
        coloca en sus respectivos campos, luego desactiva los campos para evitar su modificación.
        
        Retorna None.
        '''
        debtor_data:list[tuple[str,str,str]]
        
        self.formatField(field_to_format=field_validated)
        
        # crea QCompleters
        if field_validated == 'debtor_name': # crea completer para apellidos que coincidan con el nombre
            self.saleDialog_ui.lineEdit_debtorSurname.setCompleter(
                createCompleter(sql="SELECT apellido FROM Deudores WHERE nombre = ?",
                                params=(self.saleDialog_ui.lineEdit_debtorName.text(),)
                                )
                )
        
        elif field_validated == 'debtor_surname': # crea completer para nombres que coincidan con el apellido
            self.saleDialog_ui.lineEdit_debtorName.setCompleter(
                createCompleter(sql="SELECT nombre FROM Deudores WHERE apellido = ?",
                                params=(self.saleDialog_ui.lineEdit_debtorSurname.text(),)
                                )
                )
        
        # si ambos campos son válidos es porque ambos campos se llenaron, y coloca los datos en los campos restantes
        if self.VALID_FIELDS['DEBTOR_NAME'] and self.VALID_FIELDS['DEBTOR_SURNAME']:
            # obtengo los datos desde la cta. cte.
            debtor_data = makeReadQuery(
                sql="SELECT num_telefono, direccion, codigo_postal FROM Deudores WHERE (nombre = ?) AND (apellido = ?);",
                params=(self.saleDialog_ui.lineEdit_debtorName.text(), self.saleDialog_ui.lineEdit_debtorSurname.text(), ))
            
            # los coloco en sus campos (si se encontraron coincidencias)
            if len(debtor_data) > 0:
                self.saleDialog_ui.lineEdit_phoneNumber.setText( str(debtor_data[0][0]) )
                self.saleDialog_ui.lineEdit_direction.setText( str(debtor_data[0][1]) )
                self.saleDialog_ui.lineEdit_postalCode.setText( str(debtor_data[0][2]) )
                
                self.saleDialog_ui.lineEdit_phoneNumber.setEnabled(False)
                self.saleDialog_ui.lineEdit_direction.setEnabled(False)
                self.saleDialog_ui.lineEdit_postalCode.setEnabled(False)
            
            else:
                self.saleDialog_ui.lineEdit_phoneNumber.setEnabled(True)
                self.saleDialog_ui.lineEdit_direction.setEnabled(True)
                self.saleDialog_ui.lineEdit_postalCode.setEnabled(True)
        
        return None


    @Slot(str)
    def formatField(self, field_to_format:str) -> None:
        '''
        Es llamado desde cada QLineEdit que deba ser formateado, y desde los métodos 'self.onTotalPaidEditingFinished'|
        'onDebtorNameAndSurnameEditingFinished' y desde la señal 'editingFinished' de 'lineEdit_phoneNumber'.
        
        Dependiendo del campo 'field_to_format' formatea el texto y lo asigna en el campo correspondiente.
        
        PARAMS:
        - field_to_format: el campo a formatear. Admite los siguientes valores:
            - product_quantity: formatea el campo de cantidad del producto.
            - product_total_paid: formatea el campo de total abonado del producto.
            - debtor_name: formatea el campo de nombre del deudor.
            - debtor_surname: formatea el campo de apellido del deudor.
            - debtor_phone_num: formatea el campo de teléfono del deudor.

        Retorna None.
        '''
        field_text:str
        phone_number:PhoneNumber # se usa cuando el campo a formatear es el de núm. de teléfono
        
        match field_to_format:
            case 'product_quantity': # cambia puntos por comas, si termina con "." ó "," lo saca
                field_text = self.saleDialog_ui.lineEdit_productQuantity.text()
                if field_text.endswith((",",".")):
                    field_text = field_text.rstrip(",")
                    field_text = field_text.rstrip(".")
                field_text = field_text.replace(".",",")
                self.saleDialog_ui.lineEdit_productQuantity.setText(field_text)
            
            case 'product_total_paid': # cambia puntos por comas, si termina con "." ó "," lo saca
                field_text = self.saleDialog_ui.lineEdit_totalPaid.text()
                if field_text.endswith((",",".")):
                    field_text = field_text.rstrip(",")
                    field_text = field_text.rstrip(".")
                field_text = field_text.replace(".",",")
                self.saleDialog_ui.lineEdit_totalPaid.setText(field_text)
            
            case 'debtor_name': # pasa a minúsculas y pone en mayúsculas la primera letra de cada nombre
                field_text = self.saleDialog_ui.lineEdit_debtorName.text()
                field_text = field_text.lower().title()
                self.saleDialog_ui.lineEdit_debtorName.setText(field_text)
            
            case 'debtor_surname': # pasa a minúsculas y pone en mayúsculas la primera letra de cada apellido
                field_text = self.saleDialog_ui.lineEdit_debtorSurname.text()
                field_text = field_text.lower().title()
                self.saleDialog_ui.lineEdit_debtorSurname.setText(field_text)
            
            case 'debtor_phone_num': # agrega un "+" al principio (si no tiene) y formatea el núm. estilo internacional
                field_text = self.saleDialog_ui.lineEdit_phoneNumber.text()
                try:
                    phone_number = parse(f"+{field_text}")
                    if is_valid_number(phone_number):
                        field_text = format_number(phone_number, PhoneNumberFormat.INTERNATIONAL)
                
                except NumberParseException as err:
                    logging.error(err)
                    field_text = self.saleDialog_ui.lineEdit_phoneNumber.text()
                
                self.saleDialog_ui.lineEdit_phoneNumber.setText(field_text)
        
        return None


    def verifyFieldsValidity(self, TOGGLE_DEBTOR_DATA:bool=None) -> None:
        '''
        Es llamado desde los métodos 'self.validatorOnValidationSucceded'|'self.validatorOnValidationFailed'|
        'onTotalPaidEditingFinished'|'self.handleNameAndQuantityAndPriceChange'.
        
        Revisa si todos los campos tienen valores válidos y activa/desactiva el botón "Aceptar" dependiendo del caso, 
        y además muestra/esconde 'debtor_data' dependiendo del parámetro 'TOGGLE_DEBTOR_DATA'. Para actualizar el estado 
        de visibilidad y activar/desactivar 'debtor_data' llama a 'self.__updateDebtorDataVisibility'.
        
        PARAMS:
        - TOGGLE_DEBTOR_DATA: flag que determina si mostrar/ocultar 'debtor_data'. Por defecto es None. Es enviado 
        cuando el método es llamado desde 'onTotalPaidEditingFinished'|'self.handleNameAndQuantityAndPriceChange'.
        
        Retorna None.
        '''
        pos_to_check:int = self.__updateDebtorDataVisibility(TOGGLE_DEBTOR_DATA) #? si debtor_data está escondido no hay 
                                                                                 #? cantidad que vaya a cuenta corriente, y 
                                                                                 #? no necesita verificar si los datos del 
                                                                                 #? deudor son válidos, por lo que verifica 
                                                                                 #? si el nombre del producto, la cantidad y 
                                                                                 #? lo abonado son válidos.
        fields_validity:list
        
        # toma los valores de self.VALID_FIELDS y los guarda en una lista (para luego aplicar 'list slicing')
        fields_validity = [value for value in self.VALID_FIELDS.values()]
        
        # verifica si todos los valores de self.VALID_FIELDS son True y activa o desactiva el botón...
        if self.TOTAL_COST and all(fields_validity[:pos_to_check]):
            self.saleDialog_ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)
        
        # si lo abonado es diferente al costo total desactiva el botón "Aceptar"
        else:
            self.saleDialog_ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
        
        return None


    def __updateDebtorDataVisibility(self, TOGGLE_DEBTOR_DATA:bool=None) -> int:
        '''
        Es llamado desde 'self.verifyFieldsValidity'.
        
        Cambia la visibilidad y activa/desactiva todos los widgets de 'debtor_data' según el valor de 
        'lineEdit_totalPaid'. Para eso llama a 'self.__setSaleDialogSize'.
        
        Retorna un int con la cantidad de posiciones de 'self.VALID_FIELDS' de las que verificar su validez.
        '''
        pos_to_check:int = 3
        # verifica si el costo total fue calculado y si lineEdit_totalPaid tiene texto...
        if self.TOTAL_COST and self.saleDialog_ui.lineEdit_totalPaid.text().strip():
            
            # ...luego ve si lo abonado es igual al costo total
            if float(self.saleDialog_ui.lineEdit_totalPaid.text().replace(",",".")) == self.TOTAL_COST:
                self.__setSaleDialogSize(615, 295, True) if TOGGLE_DEBTOR_DATA else None
            
            else:
                self.__setSaleDialogSize(615, 525, False) if TOGGLE_DEBTOR_DATA else None
                pos_to_check = 7
            
        return pos_to_check


    # funciones generales
    def __setSaleDialogSize(self, min_width:int, min_height:int, hide_debtor_data:bool) -> None:
        '''
        Es llamado desde 'self.__updateDebtorDataVisibility'.
        
        Muestra/oculta 'debtor_data', declara el nuevo tamaño mínimo del SaleDialog y redimensiona la ventana 
        al tamaño.
        
        Retorna None.
        '''
        self.setMinimumSize(min_width, min_height)
        
        self.resize(self.width(), self.minimumHeight())

        self.saleDialog_ui.debtor_data.setHidden(hide_debtor_data)
        # es importante habilitar 'debtor_data' porque sino no deja habilitar los widgets hijos
        self.saleDialog_ui.debtor_data.setEnabled(not hide_debtor_data)
        
        # antes de habilitar/deshabilitar los widgets, hay que habilitar 'debtor_data'
        for lineEdit in self.saleDialog_ui.debtor_data.findChildren(QLineEdit):
            lineEdit.setEnabled(not hide_debtor_data)
        
        # y esconde los labels de feedback (sólo si se muestra debtor_data)
        if not self.saleDialog_ui.debtor_data.isHidden():
            self.saleDialog_ui.label_debtorName_feedback.hide()
            self.saleDialog_ui.label_debtorSurname_feedback.hide()
            self.saleDialog_ui.label_phoneNumber_feedback.hide()
            self.saleDialog_ui.label_postalCode_feedback.hide()
            
            # desactiva el botón "Aceptar"
            self.saleDialog_ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
        
        else:
            # activa el botón "Aceptar"
            self.saleDialog_ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)
        
        return None


    def __getFieldsData(self) -> tuple:
        '''
        Es llamado desde 'self.handleOkClicked'.
        
        Obtiene todos los datos de los campos y formatea los valores.
        
        Retorna un tuple.
        '''
        total_paid:float
        values:tuple

        # pasa a float el valor abonado
        try:
            total_paid:float = float(self.saleDialog_ui.lineEdit_totalPaid.text().replace(",","."))
        
        except ValueError:
            total_paid = self.saleDialog_ui.lineEdit_totalPaid.text()

        # si debtor_data está oculto es porque la cantidad abonada es igual o mayor al total a pagar...
        if self.saleDialog_ui.debtor_data.isHidden():
            values = (
                self.saleDialog_ui.lineEdit_saleDetail.text().strip(), # 0, detalle de venta
                self.saleDialog_ui.comboBox_productName.currentText(), # 1, nombre del producto
                self.saleDialog_ui.lineEdit_productQuantity.text(), # 2, cantidad
                self.saleDialog_ui.checkBox_comercialPrice.isChecked(), # 3, precio comercial
                self.TOTAL_COST, # 4, costo total
                total_paid, # 5, total abonado
                self.saleDialog_ui.dateTimeEdit.text() # 6, fecha y hora
                )
        
        # sino, es porque la cantidad abonada es menor al total a pagar...
        else:
            values = (
                self.saleDialog_ui.lineEdit_saleDetail.text().strip(), # 0
                self.saleDialog_ui.comboBox_productName.currentText(), # 1
                self.saleDialog_ui.lineEdit_productQuantity.text(), # 2
                self.saleDialog_ui.checkBox_comercialPrice.isChecked(), # 3
                self.TOTAL_COST, # 4
                total_paid, # 5
                self.saleDialog_ui.dateTimeEdit.text(), # 6
                # title() hace que cada palabra comience con mayúsculas...
                self.saleDialog_ui.lineEdit_debtorName.text().title(), # 7
                self.saleDialog_ui.lineEdit_debtorSurname.text().title(), # 8
                self.saleDialog_ui.lineEdit_phoneNumber.text(), # 9
                self.saleDialog_ui.lineEdit_direction.text().title(), # 10
                self.saleDialog_ui.lineEdit_postalCode.text() # 11
                )
        return values


    @Slot()
    def handleOkClicked(self) -> None:
        '''
        Es llamado una vez que se presiona el botón "Aceptar".
        
        Este método obtiene los datos formateados de los campos, declara las consultas INSERT y sus parámetros, 
        realiza las consultas INSERT a la base de datos y al final actualiza el stock en la tabla "Productos".
        En éste método las consultas se hacen sin llamar a otra función, y tampoco usando MULTITHREADING, esto es 
        es así para garantizar la atomicidad e integridad de los datos.
        
        Este método llama a:
        - self.__getFieldsData: para obtener los valores formateados de los campos.
        - self.__updateProductStock: para actualizar (luego de los INSERT) el stock en tabla "Productos".
        
        Retorna None.
        '''
        #? siempre se insertan datos en Ventas y Detalle_Ventas, pero si el "total abonado" no es igual 
        #? al "costo total" entonces se insertan datos también en Deudas y Deudores.

        # obtiene los valores formateados de los campos...
        values:tuple = self.__getFieldsData()

        #! hago las consultas sin llamar funciones porque necesito tratarlas como una transacción, es decir, 
        #! se hacen todas las consultas INSERT o ninguna...
        conn = createConnection("database/inventario.db")
        if not conn:
            return None
        cursor = conn.cursor()
        
        #! lo pongo entre un try-except porque si falla algo necesito hacer un rollback
        try:
            # declara la consulta sql y params de Ventas y hace la consulta...
            sql_sales:str = "INSERT INTO Ventas(fecha_hora, detalles_venta) VALUES(?,?);"
            params_sales:tuple = (values[6], values[0],)
            cursor.execute(sql_sales, params_sales)
            conn.commit()

            # si el largo de 'values' es de 12, es porque hay una deuda/cantidad a favor dentro de la compra...
            if len(values) == 12:
                # verifica si el deudor en Deudores existe
                sql_verify:str = "SELECT COUNT(*) FROM Deudores WHERE nombre = ? AND apellido = ?;"
                params_verify:tuple = (values[7], values[8],)
                verify_query = makeReadQuery(sql_verify, params_verify)[0][0]

                # si no existe ese deudor, lo agrega...
                if not verify_query:
                    # declara la consulta sql y params de Deudores y hace la consulta...
                    sql_debtor:str = "INSERT INTO Deudores(nombre, apellido, num_telefono, direccion, codigo_postal) VALUES(?, ?, ?, ?, ?);"
                    params_debtor:tuple = (values[7], values[8], values[9], values[10], values[11],)
                    cursor.execute(sql_debtor, params_debtor)
                    conn.commit()
                
                # declara la consutla sql y params de Deudas y hace la consulta...
                sql_debt:str = "INSERT INTO Deudas(fecha_hora, total_adeudado, IDdeudor, eliminado) VALUES(?, ?, (SELECT IDdeudor FROM Deudores WHERE nombre = ? AND apellido = ?), 0);"
                params_debt:tuple = (values[6], round(values[4] - values[5],2), values[7], values[8],)
                cursor.execute(sql_debt, params_debt)
                conn.commit()

                # al final, declara la consulta y los parámetros para Detalle_Ventas...
                sql_saleDetail:str = "INSERT INTO Detalle_Ventas(cantidad, costo_total, IDproducto, IDventa, abonado, IDdeuda) VALUES(?,?,(SELECT IDproducto FROM Productos WHERE nombre = ?), (SELECT IDventa FROM Ventas WHERE fecha_hora = ? AND detalles_venta = ?),?, (SELECT IDdeuda FROM Deudas WHERE fecha_hora = ? AND IDdeudor = (SELECT IDdeudor FROM Deudores WHERE nombre = ? AND apellido = ?) ) );"
                params_saleDetail:tuple = (values[2], values[4], values[1], values[6], values[0], values[5], values[6], values[7], values[8],)
            
            # si lo abonado es igual al total...
            else:
                # declara la consulta sql y los params de Detalle_Ventas (solamente de esa tabla)...
                sql_saleDetail:str = "INSERT INTO Detalle_Ventas(cantidad, costo_total, IDproducto, IDventa, abonado, IDdeuda) VALUES(?, ?, (SELECT IDproducto FROM Productos WHERE nombre = ?), (SELECT IDventa FROM Ventas WHERE fecha_hora = ? AND detalles_venta = ?), ?, NULL);"
                params_saleDetail:tuple = (values[2], values[4], values[1], values[6], values[0], values[5],)
            
            # hace la consulta a Detalle_Ventas
            cursor.execute(sql_saleDetail, params_saleDetail)
            conn.commit()
            
            # antes de terminar, actualiza el stock en Productos (resta al stock la cantidad vendida)
            sql_product:str = "UPDATE Productos SET stock = stock - ? WHERE nombre = ?;"
            params_product:tuple = (values[2], values[1],)
            cursor.execute(sql_product, params_product)
            conn.commit()
            
        except sqlite3Error as err:
            conn.rollback()
            logging.error(f"{err.sqlite_errorcode}: {err.sqlite_errorname} / {err}")
        
        finally:
            conn.close()
        return None


# ==============================================================================================================


# item de la lista del formulario de Ventas
class ListItem(QWidget):
    '''
    Item creado dinámicamente dentro de la lista de formulario de ventas 'MainWindow.sales_input_list'. Sirve para 
    seleccionar un producto, la cantidad vendida, el tipo de precio (comercial o normal) y darle alguna descripción a 
    la venta.
    '''
    # TODO2: declarar señales de SignalToParent en esta clase
    
    def __init__(self, listWidget:QListWidget, listWidgetItem:QListWidgetItem, newObjectName:str):
        super(ListItem, self).__init__()
        self.listItem = Ui_listProduct()
        self.listItem.setupUi(self)
        self.listWidget = listWidget
        self.listWidgetItem = listWidgetItem
        # asigno el ícono para el botón de borrar el item actual
        icon:QIcon = QIcon()
        icon.addFile(":/icons/x-white.svg")
        self.listItem.btn_deleteCurrentProduct.setIcon(icon)
        self.listItem.btn_deleteCurrentProduct.setIconSize(QSize(28, 28))

        # cambia el 'objectName' del ListItem
        self.setObjectName(newObjectName)

        # instancio la señal que se manda a sales_input_list (al método addSalesInputListItem)
        self.signalToParent = SignalToParent()

        # lleno el combobox de nombres
        self.listItem.comboBox_productName.addItems(getProductNames())
        
        # TODO1: colocar validadores en los campos necesarios
        
        # validators
        floatRe:QRegularExpression = QRegularExpression("[0-9]{0,9}(\.|,)?[0-9]{0,2}")
        self.listItem.lineEdit_productQuantity.setValidator(QRegularExpressionValidator(floatRe, self.listItem.lineEdit_productQuantity))

        #--- SEÑALES --------------------------------------------------
        self.listItem.btn_deleteCurrentProduct.clicked.connect(lambda: self.deleteCurrentProduct())

        self.listItem.comboBox_productName.currentIndexChanged.connect(lambda: self.validateFields(False))

        self.listItem.lineEdit_productQuantity.textChanged.connect(lambda: self.validateFields(False))
        self.listItem.lineEdit_productQuantity.editingFinished.connect(lambda: self.validateFields(True))

        self.listItem.checkBox_comercialPrice.stateChanged.connect(lambda: self.validateFields(False))
        
    #### MÉTODOS #####################################################
    # eliminar el item actual
    @Slot()
    def deleteCurrentProduct(self) -> None:
        '''
        Emite una señal a 'MainWindow.sales_input_list' (al método 'MainWindow.addSalesInputListItem') de que se 
        eliminó el item y elimina el item actual de la lista.
        
        Retorna None.
        '''
        self.listWidget.takeItem(self.listWidget.row(self.listWidgetItem))
        self.signalToParent.deletedItem.emit(self.objectName())
        return None


    # métodos de validación
    def validateProductName(self, curr_index:int) -> None:
        '''
        Valida que el nombre del producto introducido sea válido, muestra un mensaje en 'label_nameFeedback'.
        
        Retorna un bool.
        '''
        valid_name:bool = True

        # valido el nombre
        if curr_index == -1:
            valid_name = False
            self.listItem.label_nameFeedback.setStyleSheet("border: 1px solid #f00; background-color: rgb(255, 185, 185);")
            self.listItem.label_nameFeedback.setText("Se debe seleccionar un producto")
        return valid_name


    def validateProductQuantity(self, curr_text:str, editing_finished:bool = False) -> bool:
        '''
        Valida que la cantidad introducida sea válida, muestra un mensaje en 'label_quantityFeedback'.
        
        Retorna un bool.
        '''
        valid_quantity:bool = True
        curr_stock:float | int | str
        
        # formatea el valor
        curr_text = curr_text.replace(",", ".")
        if curr_text.endswith("."):
            curr_text = curr_text.replace(".", "")
        elif curr_text.startswith("."):
            curr_text = f"0{curr_text}"
        # si se terminó de editar, reemplaza el valor en el lineedit
        if editing_finished:
            self.listItem.lineEdit_productQuantity.setText(curr_text)

        # valida la cantidad
        if curr_text == "": # si está vacío...
            valid_quantity = False
            self.listItem.label_quantityFeedback.setStyleSheet("border: 1px solid #f00; background-color: rgb(255, 185, 185);")
            self.listItem.label_quantityFeedback.setText("Se debe ingresar una cantidad")
        else:
            try: # verifica si es igual a 0...
                if float(curr_text) == 0:
                    valid_quantity = False
                    self.listItem.label_quantityFeedback.setStyleSheet("border: 1px solid #f00; background-color: rgb(255, 185, 185);")
                    self.listItem.label_quantityFeedback.setText("La cantidad debe ser mayor a 0")
            except:
                pass

            if curr_text != "" and self.listItem.comboBox_productName.currentIndex() != -1 and valid_quantity: # sino,ve si es mayor al stock disponible...
                curr_stock = makeReadQuery("SELECT stock FROM Productos WHERE nombre = ?", (self.listItem.comboBox_productName.itemText(self.listItem.comboBox_productName.currentIndex()), ))[0][0]
                try:
                    curr_stock = int(curr_stock) if float(curr_stock).is_integer() else float(curr_stock)
                    if float(curr_text) > curr_stock:
                        valid_quantity = False
                        self.listItem.label_quantityFeedback.setStyleSheet("border: 1px solid #f00; background-color: rgb(255, 185, 185);")
                        self.listItem.label_quantityFeedback.setText(f"La cantidad es mayor al stock (stock: {curr_stock})")
                except:
                    pass
        return valid_quantity


    @Slot(bool)
    def validateFields(self, le_editing_finished:bool = False) -> None:
        '''
        Actúa como nexo para validar el nombre del producto y la cantidad cuando se emitan señales desde el campo 
        del nombre del producto (QComboBox), la cantidad (QLineEdit) o el tipo de precio (QCheckBox). 
        Envía una señal a 'MainWindow.sales_input_list' (al método 'MainWindow.addSalesInputListItem') con el valor 
        (True o False). 
        
        También pone el foco en éste item de 'MainWindow.sales_input_list'.
        
        Retorna None.
        '''
        combobox_curr_index:int = self.listItem.comboBox_productName.currentIndex()
        le_curr_text:str = self.listItem.lineEdit_productQuantity.text()
        valid:tuple = (
            self.validateProductName(combobox_curr_index),
            self.validateProductQuantity(le_curr_text, True if le_editing_finished else False)
        )

        # pone el foco en el item
        self.listWidget.setCurrentItem(self.listWidgetItem)

        if valid[0]: # si el nombre del producto es válido...
            self.listItem.label_nameFeedback.setStyleSheet("")
            self.listItem.label_nameFeedback.setText("")

        if valid[1]: # si la cantidad es válida...
            self.listItem.label_quantityFeedback.setStyleSheet("")
            self.listItem.label_quantityFeedback.setText("")

        if all(valid): # si ambos son válidos...
            self._setLabelMeasurementUnit()
            self._setTotalCost()
            self._setSaleDetails()
        else:
            self._setTotalCost(False)

        # envía una señal a MainWindow.sales_input_list (al método MainWindow.addSalesInputListItem)
        if "NO DISPONIBLE" in self.listItem.label_subtotal.text() or self.listItem.label_subtotal.text() == "SUBTOTAL":
            self.signalToParent.allFieldsValid.emit({self.objectName():False})
        else:
            self.signalToParent.allFieldsValid.emit({self.objectName():True})

        return None


    # métodos generales
    def _setLabelMeasurementUnit(self) -> None:
        '''
        Si 'self.VALID_NAME' y 'self.VALID_QUANTITY' son True, hace una consulta SELECT a la base de datos y 
        obtiene la unidad de medida del producto.
        
        Retorna None.
        '''
        m_unit:str

        m_unit = makeReadQuery("SELECT unidad_medida FROM Productos WHERE nombre = ?;", (self.listItem.comboBox_productName.itemText(self.listItem.comboBox_productName.currentIndex()),) )[0][0]
        self.listItem.label_productMeasurementUnit.setText(m_unit)
        self.listItem.label_productMeasurementUnit.adjustSize()
        return None


    def _setTotalCost(self, all_valid:bool = True) -> None:
        '''
        Si el nombre y la cantidad son válidos, hace una consulta SELECT a la base de datos y obtiene el precio del 
        producto, y si 'checkBox_comercialPrice' está marcada obtiene el precio comercial.
        
        Calcula el precio total y lo reemplaza en 'label_subtotal'.
        
        Retorna None.
        '''
        col_name:str
        sql:str
        price:float | None | str

        if all_valid:
            col_name = 'precio_unit' if not self.listItem.checkBox_comercialPrice.isChecked() else 'precio_comerc'
            sql = f"SELECT {col_name} FROM Productos WHERE IDproducto = (SELECT IDproducto FROM Productos WHERE nombre = ?);"
            # obtiene el precio
            price = makeReadQuery(sql, (self.listItem.comboBox_productName.itemText(self.listItem.comboBox_productName.currentIndex()), ))[0][0]
            try:
                price = round( float(price) * float(self.listItem.lineEdit_productQuantity.text() ), 2)
            except:
                pass
            if not price: # si 'price' es None es porque el producto no tiene precio comercial
                price = "NO DISPONIBLE"
            # reemplaza 'label_subtotal'
            if price:
                self.listItem.label_subtotal.setText(f"<html><head/><body><p><span style= 'font-size: 18px; color: #22577a;'>{price}</span></p></body></html>")
        else:
            self.listItem.label_subtotal.setText("SUBTOTAL")
        return None


    def _setSaleDetails(self) -> None:
        '''
        Si 'lineEdit_saleDetail' no fue rellenado para cuando se completen los campos del nombre del producto 
        y la cantidad, este método llena el campo de detalles de venta con el nombre del producto, la cantidad vendida 
        y el tipo de precio que se pagó.
        
        Si el campo de 'lineEdit_saleDetail' ya tenía contenido escrito, sólo coloca si el precio fue el normal o el 
        comercial.
        
        Retorna None.
        '''
        product_name:str
        quantity:str
        price_type:str
        re:Match | None | str
        new_text:str # sólo se usa si el detalle fue escrito manualmente para poner el tipo de precio (normal o comercial)

        # obtiene el tipo de precio pagado
        price_type:str = "P. NORMAL" if not self.listItem.checkBox_comercialPrice.isChecked() else "P. COMERCIAL"

        # verifica que, si lineEdit_saleDetail tiene texto, que no sea similar a...
        re = match("[0-9]{1,8} .{1,} (\(P. NORMAL\)|\(P. COMERCIAL\))", self.listItem.lineEdit_saleDetail.text())
        re = re.group() if re else None
        if (self.listItem.lineEdit_saleDetail.text().strip() == re) or (self.listItem.lineEdit_saleDetail.text().strip() == ""):
            # obtiene los valores de los otros campos
            product_name:str = self.listItem.comboBox_productName.itemText(self.listItem.comboBox_productName.currentIndex())
            quantity:str = self.listItem.lineEdit_productQuantity.text()
            # llena el campo de detalles de la venta
            self.listItem.lineEdit_saleDetail.setText(f"{quantity} de {product_name} ({price_type})")
        else:
            new_text = self.listItem.lineEdit_saleDetail.text()
            new_text = sub("(\(P. NORMAL\)|\(P. COMERCIAL\))", "", self.listItem.lineEdit_saleDetail.text())
            new_text = f"{new_text.strip()} ({price_type})"
            self.listItem.lineEdit_saleDetail.setText(new_text)
        return None





# subclase con métodos de validación para las clases que manejen datos de deudores
class DebtorDataValidation():
    '''Clase que se encarga de llevar a cabo la validación de datos de deudores. Es usada en la clase 'DebtorDataDialog'.'''
    def __init__(self, name:QLineEdit, surname:QLineEdit, phone_number:QLineEdit, postal_code:QLineEdit):
        self.name:QLineEdit = name
        self.surname:QLineEdit = surname
        self.phone_number:QLineEdit = phone_number
        self.postal_code:QLineEdit = postal_code

        self.VALID_FIELDS:dict[str:bool] = {'name': None,
                                            'surname': None,
                                            'phone_number':True,
                                            'postal_code':True}

    #### MÉTODOS #####################################################
    def validateDebtorNameField(self) -> None:
        '''Valida que el nombre del deudor no esté vacío y cambia el valor de verdad de 'VALID_FIELDS["name"]'. Retorna 'None'.'''
        self.VALID_FIELDS['name'] = False if self.name.text().strip() == "" else True
        return None
    

    def validateDebtorSurnameField(self) -> None:
        '''Valida que el apellido del deudor no esté vacío y cambia el valor de verdad de 'VALID_FIELDS["surname"]'. Retorna 'None'.'''
        self.VALID_FIELDS['surname'] = False if self.surname.text().strip() == "" else True
        return None
    

    def validateDebtorPhoneNumberField(self) -> None:
        '''Valida que el número de teléfono del deudor no sea muy corto y cambia el valor de verdad de 'VALID_FIELDS["phone_number"]'. Retorna 'None'.'''
        phone_number:str = self.phone_number.text().replace(" ", "").replace("+", "").replace("-", "")[2:]
        
        # si no está vacío y tiene menos de 6 dígitos (phone_number no tiene los primeros 2 dígitos, por eso pongo 4)...
        if phone_number != "" and (0 < len(phone_number) < 4):
            self.VALID_FIELDS['phone_number'] = False
        else:
            self.VALID_FIELDS['phone_number'] = True
        return None
    

    def validateDebtorPostalCodeField(self) -> None:
        '''Valida que el código postal del deudor no sea menor a 1 y cambia el valor de verdad de 'VALID_FIELDS["postal_code"]. Retorna 'None'.'''
        postal_code:int = int(self.postal_code.text().strip().replace(".", "").replace(",", "")) if self.postal_code.text() != "" else ""
        self.postal_code.setText(str(postal_code))

        if self.postal_code.text() and postal_code < 1:
            self.VALID_FIELDS['postal_code'] = False
        else:
            self.VALID_FIELDS['postal_code'] = True
        return None





# se usa en las clases ListItem y DebtorDataDialog
class SignalToParent(QObject):
    '''Señales para usar en las clases 'ListItem' y 'DebtorDataDialog'.'''
    allFieldsValid = Signal(object) # usado en ListItem
    deletedItem = Signal(str) # usado en ListItem
    debtorChosen = Signal(object) # usado en DebtorDataDialog





# Dialog con datos de deudores
class DebtorDataDialog(QDialog):
    '''QDialog con datos de deudores.'''
    def __init__(self):
        super(DebtorDataDialog, self).__init__()
        self.debtorData = Ui_debtorDataDialog()
        self.debtorData.setupUi(self)
        self.dataValidation = DebtorDataValidation(self.debtorData.lineEdit_debtorName, self.debtorData.lineEdit_debtorSurname, self.debtorData.lineEdit_phoneNumber, self.debtorData.lineEdit_postalCode)

        # señal que determina si se eligió un deudor (uso self.signal.debtorChosen) (si se eligió, es 1, sino 0)
        self.signalToParent = SignalToParent()
        

        self.debtorData.lineEdit_debtorName.setCompleter(createCompleter(type=1))
        self.debtorData.lineEdit_debtorSurname.setCompleter(createCompleter(type=2))

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

        self.debtorData.lineEdit_postalCode.setValidator(QIntValidator(1, 9_999))

        #--- SEÑALES --------------------------------------------------
        self.debtorData.lineEdit_debtorName.textChanged.connect(lambda: self.validateFields(type='name'))
        
        self.debtorData.lineEdit_debtorSurname.textChanged.connect(lambda: self.validateFields(type='surname'))
        
        self.debtorData.lineEdit_phoneNumber.textChanged.connect(lambda: self.validateFields(type='phone_number'))
        
        self.debtorData.lineEdit_postalCode.textChanged.connect(lambda: self.validateFields(type='postal_code'))
        # Ok
        self.debtorData.buttonBox.accepted.connect(lambda: self.handleOkClicked())
        # Cancel
        self.debtorData.buttonBox.rejected.connect(lambda: self.signalToParent.debtorChosen.emit(0))

    #### MÉTODOS #####################################################
    @Slot(str)
    def validateFields(self, type:str) -> None:
        '''
        Llama a métodos de la clase 'DebtorDataValidation' para validar el campo especificado en el argumento 'type', 
        y cambia el estilo de los campos y los labels de feedback correspondientes de acuerdo a la validación. 
        Al final activa o desactiva el botón "Aceptar".
        
        Retorna None.
        '''
        match type:
            case 'name':
                self.dataValidation.validateDebtorNameField()
                if not self.dataValidation.VALID_FIELDS['name']:
                    self.debtorData.label_debtorName_feedback.setText("Se necesita un nombre")
                    self.debtorData.lineEdit_debtorName.setStyleSheet("border: 1px solid #f00; background-color: rgb(255, 185, 185);")
                else:
                    self.debtorData.label_debtorName_feedback.setText("")
                    self.debtorData.lineEdit_debtorName.setStyleSheet("border: 1px solid #0f0; background-color: rgb(185, 255, 185);")

            case 'surname':
                self.dataValidation.validateDebtorSurnameField()
                if not self.dataValidation.VALID_FIELDS['surname']:
                    self.debtorData.label_debtorSurname_feedback.setText("Se necesita un apellido")
                    self.debtorData.lineEdit_debtorSurname.setStyleSheet("border: 1px solid #f00; background-color: rgb(255, 185, 185);")
                else:
                    self.debtorData.label_debtorSurname_feedback.setText("")
                    self.debtorData.lineEdit_debtorSurname.setStyleSheet("border: 1px solid #0f0; background-color: rgb(185, 255, 185);")
            
            case 'phone_number':
                self.dataValidation.validateDebtorPhoneNumberField()
                if not self.dataValidation.VALID_FIELDS['phone_number']:
                    self.debtorData.label_phoneNumber_feedback.setText("El número de teléfono es muy corto (mín.: 6)")
                    self.debtorData.lineEdit_phoneNumber.setStyleSheet("border: 1px solid #f00; background-color: rgb(255, 185, 185);")
                else:
                    self.debtorData.label_phoneNumber_feedback.setText("")
                    self.debtorData.lineEdit_phoneNumber.setStyleSheet("border: 1px solid #0f0; background-color: rgb(185, 255, 185);")

            case 'postal_code':
                self.dataValidation.validateDebtorPostalCodeField()
                if not self.dataValidation.VALID_FIELDS['postal_code']:
                    self.debtorData.label_postalCode_feedback.setText("El código postal debe ser mayor a 1")
                    self.debtorData.lineEdit_postalCode.setStyleSheet("border: 1px solid #f00; background-color: rgb(255, 185, 185);")
                else:
                    self.debtorData.label_postalCode_feedback.setText("")
                    self.debtorData.lineEdit_postalCode.setStyleSheet("border: 1px solid #0f0; background-color: rgb(185, 255, 185);")
        
        # activa o desactiva el botón "Aceptar" si todos los campos son válidos
        if all(self.dataValidation.VALID_FIELDS.values()):
            self.debtorData.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)
        else:
            self.debtorData.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
        return None
    

    def getFieldsData(self) -> tuple:
        '''Obtiene todos los datos de los campos y formatea los valores. Retorna una tupla con los valores.'''
        # obtengo y formateo el número de teléfono...
        phone_number:str | None = self.debtorData.lineEdit_phoneNumber.text().replace(" ", "")
        re_valid_ph_number:Match | None = match("\+[0-9]{2}-[0-9]{4}-[0-9]*", phone_number)
        # si no coincide con el patrón es porque debe estar vacío
        if not re_valid_ph_number:
            phone_number = ""

        if phone_number.endswith("-"):
            phone_number.rstrip("-")
        
        # guardo los valores
        values = (self.debtorData.lineEdit_debtorName.text().title(),
                  self.debtorData.lineEdit_debtorSurname.text().title(),
                  phone_number,
                  self.debtorData.lineEdit_direction.text().title(),
                  self.debtorData.lineEdit_postalCode.text())
        return values
    

    @Slot()
    def handleOkClicked(self) -> None:
        '''
        Es llamado una vez que se presiona el botón "Aceptar".
        
        Obtiene los datos de los campos formateados e inserta los valores en la base de datos en las tablas de 
        "Deudores" (si no existe el deudor). Al final envía una señal con el ID, nombre y apellido del deudor al 
        método 'MainWindow.handleFinishedSale' confirmando que se eligió un deudor.
        
        Retorna None.
        '''
        # obtiene los valores formateados de los campos...
        values:tuple = self.getFieldsData()
        sql:str
        params:tuple
        query:int

        # verifica si el deudor existe en Deudores
        sql  = "SELECT COUNT(*) FROM Deudores WHERE nombre = ? AND apellido = ?;"
        params = (values[0], values[1],)
        query = makeReadQuery(sql, params)[0][0] # si el deudor no existe devuelve 0

        try:
            conn = createConnection("database/inventario.db")
            cursor = conn.cursor()
            
            # si no existe ese deudor, lo agrega...
            if not query:
                # declara la consulta sql y params de Deudores y hace la consulta...
                sql = "INSERT INTO Deudores(nombre, apellido, num_telefono, direccion, codigo_postal) VALUES(?, ?, ?, ?, ?);"
                params = (values[0], values[1], values[2], values[3], values[4],)
                cursor.execute(sql, params)
                conn.commit()

            # trae el ID, el nombre y el apellido del deudor para luego mandarlo a MainWindow en la señal 'debtorChosen'
            query = makeReadQuery(
                "SELECT IDdeudor, nombre, apellido FROM Deudores WHERE nombre = ? AND apellido = ?;",
                (values[0], values[1],))[0]

            # envía señal comunicando que sí se eligió un deudor
            self.signalToParent.debtorChosen.emit(query)
            
        except sqlite3Error as err:
            conn.rollback()
            print(f"{err.sqlite_errorcode}: {err.sqlite_errorname} / {err}")
        
        finally:
            conn.close()
        
        return None





# item de lista de Deudas
class DebtsTablePersonData(QWidget):
    def __init__(self, tableWidget:QTableWidget, full_name:str):
        super(DebtsTablePersonData, self).__init__()
        self.mainDataWidget = Ui_debtorDetails()
        self.mainDataWidget.setupUi(self)

        # TODO: preguntar a chatGPT cómo hacer que cuando se presione un botón aparezca un widget, y que dicho widget
        #       desaparezca si se hace click fuera de él.

        self.mainDataWidget.label_full_name.setText(full_name)

        icon = QIcon()
        icon.addFile(pyinstallerCompleteResourcePath("icons\chevron-downBlack.svg"))
        self.mainDataWidget.btn_expand_info.setIcon(icon)
        self.mainDataWidget.btn_expand_info.setIconSize(QSize(24, 24))

        self.BTN_STATE:int = 0 # se usa para cambiar el ícono de btn_expand_info


        # señales
        self.mainDataWidget.btn_expand_info.clicked.connect(lambda: self.toggleShowDebtorData(tableWidget))


    # Métodos
    def __createExpandedDataWidget(self) -> None:
        # TODO: preguntarle a chatGPT cómo crear un widget en ventana flotante cuando se presione btn_expand_info
        pass



    def __updateButtonIcon(self, tableWidget:QTableWidget) -> None:
        '''Dependiendo del valor de 'BTN_STATE' (0 ó 1) actualiza el ícono de 'btn_expand_info' y muestra o no el \
        widget 'expandedDetails' con los detalles del deudor.
        \nRetorna 'None'.'''
        if self.BTN_STATE:
            icon = QIcon()
            icon.addFile(pyinstallerCompleteResourcePath("icons\chevron-downBlack.svg"))
            self.mainDataWidget.btn_expand_info.setIcon(icon)

            self.BTN_STATE = 0
        else:
            icon = QIcon()
            icon.addFile(pyinstallerCompleteResourcePath("icons\chevron-upBlack.svg"))
            self.mainDataWidget.btn_expand_info.setIcon(icon)
            self.__createExpandedDataWidget()

            self.BTN_STATE = 1

        self.mainDataWidget.btn_expand_info.setIconSize(QSize(24, 24))
        tableWidget.resizeRowsToContents()
        return None


    def toggleShowDebtorData(self, tableWidget:QTableWidget) -> None:
        '''Muestra los datos disponibles sobre el deudor. 
        \nRetorna 'None'.'''
        self.__updateButtonIcon(tableWidget)

