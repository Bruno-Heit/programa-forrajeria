from PySide6.QtWidgets import (QDialog, QDialogButtonBox, QLineEdit, QCompleter, QWidget)
from PySide6.QtCore import (Signal, QSize)
from PySide6.QtGui import (QIntValidator, QIcon)

from ui.ui_productDialog import Ui_Dialog
from ui.ui_saleDialog import Ui_saleDialog
from ui.ui_listproduct import Ui_listProduct
from ui.ui_debtorDataDialog import Ui_debtorDataDialog
from ui.ui_debtsTable_debtorDetails import Ui_debtorDetails

from resources import (rc_icons)

from utils.functionutils import *
from utils.workerclasses import *
from utils.dboperations import *
from utils.enumclasses import *

from sqlite3 import (Error as sqlite3Error)
from phonenumbers import (parse, format_number, is_valid_number, PhoneNumber, PhoneNumberFormat, NumberParseException)


# PRODUCTOS ====================================================================================================


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


# TABLA VENTAS =================================================================================================


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
        Es llamado desde la señal 'validationSucceded' de los validadores.
        
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
                if self.saleDialog_ui.lineEdit_phoneNumber.text() != "" and self.saleDialog_ui.lineEdit_phoneNumber.isEnabled():
                    self.saleDialog_ui.lineEdit_phoneNumber.setStyleSheet(WidgetStyle.FIELD_VALID_VAL.value)
                else:
                    self.saleDialog_ui.lineEdit_phoneNumber.setStyleSheet("")
                
                self.saleDialog_ui.label_phoneNumber_feedback.hide()
            
            case 'debtor_postal_code':
                self.VALID_FIELDS['DEBTOR_POSTAL_CODE'] = True
                if self.saleDialog_ui.lineEdit_postalCode.text() != "" and self.saleDialog_ui.lineEdit_postalCode.isEnabled():
                    self.saleDialog_ui.lineEdit_postalCode.setStyleSheet(WidgetStyle.FIELD_VALID_VAL.value)
                else:
                    self.saleDialog_ui.lineEdit_postalCode.setStyleSheet("")
                    
                self.saleDialog_ui.label_postalCode_feedback.hide()
        
        self.verifyFieldsValidity()
        return None
        
    
    @Slot(str, str)
    def validatorOnValidationFailed(self, field_validated:str, error_message:str) -> None:
        '''
        Es llamado desde la señal 'validationFailed' de los validadores.
        
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
        'self.handleNameAndQuantityAndPriceChange'.
        
        Este método llama a:
        - SaleQuantityValidator.setsetAvailableStock: para almacenar en el validador de cantidad el 
        stock disponible.
        - functionutils.getCurrentProductStock: para actualizar el stock disponible en 'self.AVAILABLE_STOCK'.
        - self.handleNameAndQuantityAndPriceChange: para actualizar los detalles y el costo total de la venta.
        
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
            self.quantity_validator.setAvailableStock(getCurrentProductStock(
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
    
    
    def __setDetailsAndCost(self) -> None:
        '''
        Es llamado desde 'self.handleNameAndQuantityAndPriceChange'.
        
        Obtiene el precio normal ó comercial dependiendo de si 'checkBox_comercialPrice' está checkeada, luego 
        obtiene el costo desde la base de datos y lo calcula a partir de la cantidad ingresada y cambia el texto 
        de 'label_productTotalCost' de acuerdo al costo total.
        Luego coloca la cantidad del producto vendido, el nombre y el tipo de precio aplicado en 'lineEdit_saleDetail'.
        
        Retorna None.
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
                createCompleter(sql="SELECT DISTINCT apellido FROM Deudores WHERE nombre = ?",
                                params=(self.saleDialog_ui.lineEdit_debtorName.text(),)
                                )
                )
        
        elif field_validated == 'debtor_surname': # crea completer para nombres que coincidan con el apellido
            self.saleDialog_ui.lineEdit_debtorName.setCompleter(
                createCompleter(sql="SELECT DISTINCT nombre FROM Deudores WHERE apellido = ?",
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
                self.saleDialog_ui.lineEdit_phoneNumber.setEnabled(False)
                self.saleDialog_ui.lineEdit_direction.setEnabled(False)
                self.saleDialog_ui.lineEdit_postalCode.setEnabled(False)
            
                self.saleDialog_ui.lineEdit_phoneNumber.setText( str(debtor_data[0][0]) )
                self.saleDialog_ui.lineEdit_direction.setText( str(debtor_data[0][1]) )
                self.saleDialog_ui.lineEdit_postalCode.setText( str(debtor_data[0][2]) )
            
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
            try:
                # ...luego ve si lo abonado es igual al costo total
                if float(self.saleDialog_ui.lineEdit_totalPaid.text().replace(",",".")) == self.TOTAL_COST:
                    self.__setSaleDialogSize(615, 295, True) if TOGGLE_DEBTOR_DATA else None
            
                else:
                    self.__setSaleDialogSize(615, 525, False) if TOGGLE_DEBTOR_DATA else None
                    pos_to_check = 7
            
            except ValueError as err: # salta este error más que nada cuando se intenta escribir "-" en lineEdit_totalPaid
                logging.error(err)
            
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


# FORMULARIO VENTAS ============================================================================================


# valores de los campos de ListItemWidget
class ListItemValues():
    '''
    Clase que contiene los valores de los campos de ListItemWidget. El principal uso de la clase es para 
    emitir de forma más sencilla los valores desde ListWidgetItem a MainWindow.
    '''
    def __init__(self, object_name:str, product_name:str=None, quantity:float=None, subtotal:float=None, ALL_VALID:bool=False):
        self.object_name:str = object_name
        
        self.product_name:str = product_name
        self.quantity:float = quantity
        self.subtotal:float = subtotal
        
        self.is_comercial_price:bool = None
        self.sale_details:str = None
        
        self.ALL_VALID:bool = ALL_VALID





# item de tipo widget de la lista del formulario de Ventas
class ListItemWidget(QWidget):
    '''
    Item creado dinámicamente dentro de la lista de formulario de ventas 'MainWindow.sales_input_list'. Sirve para 
    seleccionar un producto, la cantidad vendida, el tipo de precio (comercial o normal) y darle alguna descripción a 
    la venta.
    '''
    fieldsValidated = Signal(object) # emite un objeto tipo 'ListItemValues' con todos los valores de los campos
    deleteItem = Signal(str) # emite el 'objectName' del item
    
    def __init__(self, obj_name:str):
        super(ListItemWidget, self).__init__()
        self.listItem = Ui_listProduct()
        self.listItem.setupUi(self)
        # desactiva checkBox_comercialPrice
        self.listItem.checkBox_comercialPrice.setEnabled(False)
        # coloca el objectName
        self.setObjectName(obj_name)
        
        # esconde labels de feedback
        self.listItem.label_nameFeedback.hide()
        self.listItem.label_quantityFeedback.hide()
        
        # asigno el ícono para el botón de borrar el item actual
        icon:QIcon = QIcon()
        icon.addFile(":/icons/x-white.svg")
        self.listItem.btn_deleteCurrentProduct.setIcon(icon)
        self.listItem.btn_deleteCurrentProduct.setIconSize(QSize(28, 28))
        
        # lleno el combobox de nombres
        self.listItem.comboBox_productName.addItems(getProductNames())

        # validadores
        self.quantity_validator = SaleQuantityValidator(self.listItem.lineEdit_productQuantity)
        self.sale_detail_validator = SaleDetailsValidator(self.listItem.lineEdit_saleDetail)
        self.listItem.lineEdit_saleDetail.setValidator(self.sale_detail_validator)
        self.listItem.lineEdit_productQuantity.setValidator(self.quantity_validator)
        
        # variables
        self.VALID_FIELDS:dict[str,bool|None] = {
            'PRODUCT_NAME':None,
            'PRODUCT_QUANTITY':None
        }
        self.TOTAL_COST:float|None = None # se obtiene en __setDetailsAndCost, si el precio está disponible, sino es None
        self.field_values:ListItemValues = ListItemValues(object_name=self.objectName()) # inicializa el objeto, y es llenado 
                                                                                         # con valores en las funciones 
                                                                                         # validadoras correspondientes a cada 
                                                                                         # campo.

        #--- SEÑALES --------------------------------------------------
        # nombre de producto
        self.listItem.comboBox_productName.currentIndexChanged.connect(self.validateProductNameField)
        
        # cantidad de producto
        self.listItem.lineEdit_productQuantity.editingFinished.connect(self.formatQuantityField)
        
        self.quantity_validator.validationSucceded.connect(self.validatorOnValidationSucceded)
        self.quantity_validator.validationFailed.connect(self.validatorOnValidationFailed)
        
        # checkbox tipo de precio
        self.listItem.checkBox_comercialPrice.stateChanged.connect(self.handleNameAndQuantityAndPriceChange)
        
        # botón borrar elemento
        self.listItem.btn_deleteCurrentProduct.clicked.connect(self.deleteCurrentItem)

        
    #### MÉTODOS #####################################################
    # eliminar el item actual
    @Slot()
    def deleteCurrentItem(self) -> None:
        '''
        Es llamado desde la señal 'clicked' de 'btn_deleteCurrentProduct'.
        
        Emite la señal 'deletedItem' al QListWidget 'MainWindow.sales_input_list' (es conectada en el método 
        'MainWindow.addSalesInputListItem') de que se eliminó el item y elimina éste item de la lista.
        
        Retorna None.
        '''
        self.deleteItem.emit(self.objectName())
        self.deleteLater()
        return None


    @Slot(str)
    def validatorOnValidationSucceded(self) -> None:
        '''
        Es llamado desde la señal 'validationFailed' del validador de cantidad.
        
        Cambia el valor del flag asociado al campo de cantidad a True y cambia el QSS del campo.
        Activa 'checkBox_comercialPrice', y al finalizar llama a 'self.verifyFieldsValidity' para 
        comprobar si el nombre es válido.
        
        NOTA: redimensiona 'ListItemWidget' para que se pueda mostrar el mensaje correctamente.
        
        Retorna None.
        '''
        # sólo puedo validar completamente la cantidad cuando el nombre sea válido
        if self.VALID_FIELDS['PRODUCT_NAME']:
            self.VALID_FIELDS['PRODUCT_QUANTITY'] = True
            self.listItem.lineEdit_productQuantity.setStyleSheet(WidgetStyle.FIELD_VALID_VAL.value)
            self.listItem.label_quantityFeedback.setText(f"El stock disponible es de {self.quantity_validator.AVAILABLE_STOCK[0]} {self.quantity_validator.AVAILABLE_STOCK[1]}")
            
            # actualiza los detalles de venta y costo total
            self.handleNameAndQuantityAndPriceChange()
        
        # sea el nombre válido o no, igualmente cambia los estilos del label y el lineedit
        self.listItem.label_quantityFeedback.setStyleSheet(WidgetStyle.LABEL_NEUTRAL_VAL.value)
        self.listItem.lineEdit_productQuantity.setStyleSheet(WidgetStyle.FIELD_VALID_VAL.value)
        
        if not "El stock disponible" in self.listItem.label_quantityFeedback.text():
            self.listItem.label_quantityFeedback.setText("")
        
        self.listItem.checkBox_comercialPrice.setEnabled(True)
        
        # ajusta el tamaño del label
        self.listItem.label_quantityFeedback.adjustSize()
        
        self.verifyFieldsValidity()
        return None
        
    
    @Slot(str)
    def validatorOnValidationFailed(self, error_message:str) -> None:
        '''
        Cambia el valor del flag asociado al campo de cantidad a False, cambia el QSS del campo y muestra el 
        mensaje 'error_message' en el QLabel asociado al campo con feedback.
        Desactiva 'checkBox_comercialPrice' si el campo de cantidad está vacío.
        
        Retorna None.
        '''
        self.VALID_FIELDS['PRODUCT_QUANTITY'] = False
        self.listItem.lineEdit_productQuantity.setStyleSheet(WidgetStyle.FIELD_INVALID_VAL.value)
        self.listItem.label_quantityFeedback.show()
        # resetea el estilo del campo (por defecto es rojo, igual que los otros de feedback)
        self.listItem.label_quantityFeedback.setStyleSheet("")
        self.listItem.label_quantityFeedback.setText(error_message)
        
        self.listItem.checkBox_comercialPrice.setEnabled(False) if not self.listItem.lineEdit_productQuantity.text() else None
        
        self.verifyFieldsValidity()
        return None


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
        'self.handleNameAndQuantityAndPriceChange'.
        7. Si el campo es válido, asigna el nuevo valor en 'ListItemValues.product_name'.
        
        Este método llama a:
        - SaleQuantityValidator.setsetAvailableStock: para almacenar en el validador de cantidad el 
        stock disponible.
        - functionutils.getCurrentProductStock: para actualizar el stock disponible en 'self.AVAILABLE_STOCK'.
        - self.handleNameAndQuantityAndPriceChange: para actualizar los detalles y el costo total de la venta.
        
        Retorna None.
        '''
        # si no se eligió el nombre del producto asigna el índice -1
        if self.listItem.comboBox_productName.currentText().strip() == "":
            self.listItem.comboBox_productName.setCurrentIndex(-1)
        
        # si no hay un producto seleccionado (si índice es -1)...
        if self.listItem.comboBox_productName.currentIndex() == -1:
            self.VALID_FIELDS['PRODUCT_NAME'] = False
            self.listItem.label_nameFeedback.show()
            self.listItem.label_nameFeedback.setText("Se debe seleccionar un producto")
            self.listItem.comboBox_productName.setStyleSheet(WidgetStyle.FIELD_INVALID_VAL.value)
        
        # si el campo es válido...
        else:
            self.VALID_FIELDS['PRODUCT_NAME'] = True
            self.listItem.label_nameFeedback.hide()
            self.listItem.comboBox_productName.setStyleSheet(WidgetStyle.FIELD_VALID_VAL.value)
            
            # guarda el stock del producto en el validador de cantidad
            self.quantity_validator.setAvailableStock(getCurrentProductStock(
                self.listItem.comboBox_productName.itemText(self.listItem.comboBox_productName.currentIndex()) ))
            
            # coloca el stock en 'label_quantityFeedback'
            self.listItem.label_quantityFeedback.show()
            self.listItem.label_quantityFeedback.setStyleSheet(WidgetStyle.LABEL_NEUTRAL_VAL.value)
            self.listItem.label_quantityFeedback.setText(f"El stock disponible es de {self.quantity_validator.AVAILABLE_STOCK[0]} {self.quantity_validator.AVAILABLE_STOCK[1]}")
            
            #? llama a validar la cantidad porque, si se modificó primero la cantidad y el válida, y luego 
            #? se elige un nombre de producto que es válido pero no tiene esa cantidad en stock entonces 
            #? el campo de cantidad devuelve un "falso positivo"... de ésta forma se arregla
            self.quantity_validator.validate(self.listItem.lineEdit_productQuantity.text(), 0)
            
            # si también la cantidad es válida, actualiza los detalles de venta y el costo total...
            if self.VALID_FIELDS['PRODUCT_QUANTITY']:
                self.handleNameAndQuantityAndPriceChange()
                
                # actualiza 'self.field_values'
                self.field_values.product_name = self.listItem.comboBox_productName.itemText(
                    self.listItem.comboBox_productName.currentIndex())
        
        return None


    @Slot()
    def handleNameAndQuantityAndPriceChange(self) -> None:
        '''
        Es llamado desde:
        - self.validateProductNameField: cuando el índice de 'comboBox_productName' cambia.
        - self.validatorOnValidationSucceded: cuando el valor de 'lineEdit_productQuantity' cambia.
        - la señal 'checkBox_comercialPrice.clicked': cuando el estado de 'checkBox_comercialPrice' cambia.
        
        Asigna el valor True|False a 'ListItemValues.is_comercial_price' dependiendo del estado de 
        'checkBox_comercialPrice', cambia el texto del QLabel de subtotal, coloca los detalles de la 
        venta en su QLineEdit. Por último, al finalizar llama a 'self.verifyFieldsValidity'.
        
        Este método llama a:
        - self.__setDetailsAndCost: para actualizar los detalles de venta y el costo total.
        - self.verifyFieldsValidity: para revisar el estado de validez de los campos.
        
        Retorna None.
        '''
        # actualiza 'self.field_values'
        self.field_values.is_comercial_price = True if self.listItem.checkBox_comercialPrice.isChecked() else False
        
        # cambia los detalles de venta y el label con el costo total
        self.__setDetailsAndCost()
        
        self.verifyFieldsValidity()
        return None


    @Slot()
    def formatQuantityField(self) -> None:
        '''
        Es llamado desde la señal 'editingFinished' de 'lineEdit_productQuantity'.
        
        Formatea el texto del campo y lo vuelve a asignar al campo de cantidad, además asigna el nuevo 
        valor de cantidad a 'ListItemValues.quantity'.
        
        Retorna None.
        '''
        # cambia puntos por comas, si termina con "." ó "," lo saca
        field_text = self.listItem.lineEdit_productQuantity.text()
        
        if field_text.endswith((",",".")):
            field_text = field_text.rstrip(",")
            field_text = field_text.rstrip(".")
        
        field_text = field_text.replace(".",",")
        
        self.listItem.lineEdit_productQuantity.setText(field_text)
        
        # actualiza 'self.field_values'
        self.field_values.quantity = float(field_text)
        
        return None


    def verifyFieldsValidity(self) -> None:
        '''
        Es llamado desde los métodos 'self.validatorOnValidationSucceded'|'self.validatorOnValidationFailed'|
        'self.handleNameAndQuantityAndPriceChange'.
        
        Revisa si los campos de nombre y cantidad tienen valores válidos y emite la señal 'fieldsValidated' 
        a MainWindow con 'self.field_values', objeto de tipo 'ListItemValues'.
        
        Retorna None.
        '''
        # verifica si todos los valores de self.VALID_FIELDS son True y emite la señal a MainWindow...
        if self.TOTAL_COST and all(self.VALID_FIELDS.values()):
            self.field_values.ALL_VALID = True
            self.fieldsValidated.emit(self.field_values)

        else:
            self.field_values.ALL_VALID = False
            self.fieldsValidated.emit(self.field_values)
        
        return None


    def __setDetailsAndCost(self) -> None:
        '''
        Es llamado desde 'self.handleNameAndQuantityAndPriceChange'.
        
        Obtiene el precio normal ó comercial dependiendo de si 'checkBox_comercialPrice' está checkeada, luego 
        obtiene el costo desde la base de datos y lo calcula a partir de la cantidad ingresada y cambia el texto 
        de 'label_subtotal' de acuerdo al costo total.
        Luego coloca la cantidad del producto vendido, el nombre y el tipo de precio aplicado en 'lineEdit_saleDetail'.
        Actualiza 'self.field_values', objeto de tipo 'ListItemValues', con el subtotal y los detalles de la venta.
        
        Retorna None.
        '''
        total_cost:float|str # si existe el float, sino un str con "SUBTOTAL"
        pattern:Pattern = compile(
            pattern="[0-9]{1,8}(\.|,)?[0-9]{0,2}\sde .{1,}\s(\([\s]*P[\s]*\.[\s]*NORMAL[\s]*\)|\([\s]*P[\s]*\.[\s]*COMERCIAL[\s]*\))$",
            flags=IGNORECASE)
        re:Match | str
        new_text:str
        
        # ======== PRECIO ====================================================
        conn = createConnection("database/inventario.db")
        cursor = conn.cursor()
        
        if all(self.VALID_FIELDS.values()):
            if self.listItem.checkBox_comercialPrice.isChecked():
                sql = "SELECT ? * precio_comerc FROM Productos WHERE nombre = ?;"
            else:
                sql = "SELECT ? * precio_unit FROM Productos WHERE nombre = ?;"
            params = (
                float(self.listItem.lineEdit_productQuantity.text().replace(",",".")),
                self.listItem.comboBox_productName.itemText(self.listItem.comboBox_productName.currentIndex()),)
            
            # obtiene el costo total
            total_cost = cursor.execute(sql, params).fetchone()[0]
        
        else:
            total_cost = 0
        
        # si el valor no existe en base de datos devuelve TypeError
        try:
            if total_cost == 0 or total_cost == 0.0:
                total_cost = "SUBTOTAL"
            
            else:
                total_cost = f"$ {round(float(total_cost), 2)}"
                total_cost = total_cost.replace(".",",")
            
        except TypeError: # no puede convertir None a float
            total_cost = "SUBTOTAL"
        
        # coloca el precio total
        self.listItem.label_subtotal.setText(f"<html><head/><body><p><span style=\" font-size: 20px; color: #22577a;\">{total_cost}</span></p></body></html>")
        
        # guarda en una variable global el costo total
        self.TOTAL_COST = float(total_cost.lstrip("$").replace(" ","").replace(",",".")) if total_cost != "SUBTOTAL" else None
        
        # actualiza 'self.field_values'
        self.field_values.subtotal = self.TOTAL_COST
        
        # ======== DETALLES DE LA VENTA ======================================
        
        # obtiene los valores de cantidad, nombre del producto y tipo de precio (normal ó comercial)
        quantity = self.listItem.lineEdit_productQuantity.text()
        product_name = self.listItem.comboBox_productName.currentText()
        price_type = "P. COMERCIAL" if self.listItem.checkBox_comercialPrice.isChecked() else "P. NORMAL"

        re = match(pattern, self.listItem.lineEdit_saleDetail.text())
        re = re.group() if re else None
        # verifica si 'pattern' coincide, y si coincide reemplaza el texto (significa que no lo escribió el usuario)
        if self.listItem.lineEdit_saleDetail.text().strip() == re or self.listItem.lineEdit_saleDetail.text().strip() == "":
            self.listItem.lineEdit_saleDetail.setText(f"{quantity} de {product_name} ({price_type})")
        
        # si no coincide es porque lo escribió el usuario (sólo reemplaza el tipo de precio)
        else:
            new_text = self.listItem.lineEdit_saleDetail.text()
            new_text = sub(
                pattern="(\([\s]*P[\s]*\.[\s]*NORMAL[\s]*\)|\([\s]*P[\s]*\.[\s]*COMERCIAL[\s]*\))$",
                repl="",
                string=self.listItem.lineEdit_saleDetail.text(),
                flags=IGNORECASE)
            new_text = f"{new_text.strip()} ({price_type})"
            
            self.listItem.lineEdit_saleDetail.setText(new_text)
        
        # actualiza 'self.field_values'
        self.field_values.sale_details = self.listItem.lineEdit_saleDetail.text()
        
        return None


# DEUDORES =====================================================================================================


# Dialog con datos de deudores
class DebtorDataDialog(QDialog):
    '''
    QDialog con datos de deudores. Se usa en 'MainWindow' cuando se presiona 'MainWindow.btn_end_sale' y 
    el total abonado es menor al costo total.
    '''
    debtorChosen = Signal(object) # emite una tuple[IDdeudor,nombre,apellido] una vez elegido deudor
    
    def __init__(self):
        super(DebtorDataDialog, self).__init__()
        self.debtorData = Ui_debtorDataDialog()
        self.debtorData.setupUi(self)
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
        
        # completers
        self.debtorData.lineEdit_debtorName.setCompleter(createCompleter(type=1))
        self.debtorData.lineEdit_debtorSurname.setCompleter(createCompleter(type=2))

        # TODO: colocar validadores para los campos que necesiten
        # validadores
        self.debtor_name_validator = DebtorNameValidator(self.debtorData.lineEdit_debtorName)
        self.debtor_surname_validator = DebtorSurnameValidator(self.debtorData.lineEdit_debtorSurname)
        self.phone_number_validator = DebtorPhoneNumberValidator(self.debtorData.lineEdit_phoneNumber)
        self.postal_code_validator = DebtorPostalCodeValidator(self.debtorData.lineEdit_postalCode)
        self.debtorData.lineEdit_debtorName.setValidator(self.debtor_name_validator)
        self.debtorData.lineEdit_debtorSurname.setValidator(self.debtor_surname_validator)
        self.debtorData.lineEdit_phoneNumber.setValidator(self.phone_number_validator)
        self.debtorData.lineEdit_postalCode.setValidator(self.postal_code_validator)
        
        # variables
        self.VALID_FIELDS:dict[str,bool] = {
            'DEBTOR_NAME':None,
            'DEBTOR_SURNAME':None,
            'DEBTOR_PHONE_NUMBER':True,
            'DEBTOR_POSTAL_CODE':True
        }
        

        #--- SEÑALES --------------------------------------------------
        # nombre
        self.debtor_name_validator.validationSucceded.connect(lambda: self.validatorOnValidationSucceded('DEBTOR_NAME'))
        self.debtor_name_validator.validationFailed.connect(lambda error_message: self.validatorOnValidationFailed(
            field_validated='DEBTOR_NAME',
            error_message=error_message))
        
        self.debtorData.lineEdit_debtorName.editingFinished.connect(lambda: self.onDebtorNameAndSurnameEditingFinished(
            field_validated='DEBTOR_NAME'))
        
        # apellido
        self.debtor_surname_validator.validationSucceded.connect(lambda: self.validatorOnValidationSucceded('DEBTOR_SURNAME'))
        self.debtor_surname_validator.validationFailed.connect(lambda error_message: self.validatorOnValidationFailed(
            field_validated='DEBTOR_SURNAME',
            error_message=error_message))
        
        self.debtorData.lineEdit_debtorSurname.editingFinished.connect(lambda: self.onDebtorNameAndSurnameEditingFinished(
            field_validated='DEBTOR_SURNAME'))
        
        # número de teléfono
        self.phone_number_validator.validationSucceded.connect(lambda: self.validatorOnValidationSucceded('DEBTOR_PHONE_NUMBER'))
        self.phone_number_validator.validationFailed.connect(lambda error_message: self.validatorOnValidationFailed(
            field_validated='DEBTOR_PHONE_NUMBER',
            error_message=error_message))
        
        self.debtorData.lineEdit_phoneNumber.editingFinished.connect(lambda: self.formatField('DEBTOR_PHONE_NUMBER'))
        
        # código postal
        self.postal_code_validator.validationSucceded.connect(lambda: self.validatorOnValidationSucceded('DEBTOR_POSTAL_CODE'))
        self.postal_code_validator.validationFailed.connect(lambda error_message: self.validatorOnValidationFailed(
            field_validated='DEBTOR_POSTAL_CODE',
            error_message=error_message))
        
        # botón "Aceptar"
        self.debtorData.buttonBox.accepted.connect(lambda: self.handleOkClicked())

    #### MÉTODOS #####################################################
    @Slot(str)
    def validatorOnValidationSucceded(self, field_validated:str) -> None:
        '''
        Es llamado desde la señal 'validationSucceded' de los validadores.
        
        Cambia el valor del flag asociado al campo que fue validado 'field_validated' a True, cambia el 
        QSS del campo y esconde el QLabel asociado al campo.
        Al finalizar, llama a 'self.verifyFieldsValidity' para comprobar si el resto de campos son válidos.
        
        PARAMS:
        - field_validated: el campo que se valida. Admite los siguientes valores:
            - DEBTOR_NAME: se valida el campo de nombre del deudor.
            - DEBTOR_SURNAME: se valida el campo de apellido del deudor
            - DEBTOR_PHONE_NUMBER: se valida el campo de número de teléfono del deudor.
            - DEBTOR_POSTAL_CODE: se valida el campo de código postal del deudor.
        
        Retorna None.
        '''
        match field_validated:
            case 'DEBTOR_NAME':
                self.VALID_FIELDS['DEBTOR_NAME'] = True
                self.debtorData.lineEdit_debtorName.setStyleSheet(WidgetStyle.FIELD_VALID_VAL.value)
                self.debtorData.label_debtorName_feedback.hide()
            
            case 'DEBTOR_SURNAME':
                self.VALID_FIELDS['DEBTOR_SURNAME'] = True
                self.debtorData.lineEdit_debtorSurname.setStyleSheet(WidgetStyle.FIELD_VALID_VAL.value)
                self.debtorData.label_debtorSurname_feedback.hide()
            
            case 'DEBTOR_PHONE_NUMBER':
                self.VALID_FIELDS['DEBTOR_PHONE_NUMBER'] = True
                if self.debtorData.lineEdit_phoneNumber.text() != "" and self.debtorData.lineEdit_phoneNumber.isEnabled():
                    self.debtorData.lineEdit_phoneNumber.setStyleSheet(WidgetStyle.FIELD_VALID_VAL.value)
                else:
                    self.debtorData.lineEdit_phoneNumber.setStyleSheet("")
                
                self.debtorData.label_phoneNumber_feedback.hide()
            
            case 'DEBTOR_POSTAL_CODE':
                self.VALID_FIELDS['DEBTOR_POSTAL_CODE'] = True
                if self.debtorData.lineEdit_postalCode.text() != "" and self.debtorData.lineEdit_postalCode.isEnabled():
                    self.debtorData.lineEdit_postalCode.setStyleSheet(WidgetStyle.FIELD_VALID_VAL.value)
                else:
                    self.debtorData.lineEdit_postalCode.setStyleSheet("")
                    
                self.debtorData.label_postalCode_feedback.hide()
        
        self.verifyFieldsValidity()
        
        return None
    
    
    @Slot(str, str)
    def validatorOnValidationFailed(self, field_validated:str, error_message:str) -> None:
        '''
        Es llamado desde la señal 'validationFailed' de los validadores.
        
        Cambia el valor del flag asociado al campo que fue validado 'field_validated' a False, cambia el 
        QSS del campo y muestra el QLabel asociado al campo con el mensaje 'error_message' con feedback.
        
        PARAMS:
        - field_validated: el campo que se valida. Admite los siguientes valores:
            - DEBTOR_NAME: se valida el campo de nombre del deudor.
            - DEBTOR_SURNAME: se valida el campo de apellido del deudor
            - DEBTOR_PHONE_NUMBER: se valida el campo de número de teléfono del deudor.
            - DEBTOR_POSTAL_CODE: se valida el campo de código postal del deudor.
        
        Retorna None.
        '''
        match field_validated:
            case 'DEBTOR_NAME':
                self.VALID_FIELDS['DEBTOR_NAME'] = False
                self.debtorData.lineEdit_debtorName.setStyleSheet(WidgetStyle.FIELD_INVALID_VAL.value)
                self.debtorData.label_debtorName_feedback.show()
                self.debtorData.label_debtorName_feedback.setText(error_message)
            
            case 'DEBTOR_SURNAME':
                self.VALID_FIELDS['DEBTOR_SURNAME'] = False
                self.debtorData.lineEdit_debtorSurname.setStyleSheet(WidgetStyle.FIELD_INVALID_VAL.value)
                self.debtorData.label_debtorSurname_feedback.show()
                self.debtorData.label_debtorSurname_feedback.setText(error_message)
            
            case 'DEBTOR_PHONE_NUMBER':
                self.VALID_FIELDS['DEBTOR_PHONE_NUMBER'] = False
                self.debtorData.lineEdit_phoneNumber.setStyleSheet(WidgetStyle.FIELD_INVALID_VAL.value)
                self.debtorData.label_phoneNumber_feedback.show()
                self.debtorData.label_phoneNumber_feedback.setText(error_message)
            
            case 'DEBTOR_POSTAL_CODE':
                self.VALID_FIELDS['DEBTOR_POSTAL_CODE'] = False
                self.debtorData.lineEdit_postalCode.setStyleSheet(WidgetStyle.FIELD_INVALID_VAL.value)
                self.debtorData.label_postalCode_feedback.show()
                self.debtorData.label_postalCode_feedback.setText(error_message)
        
        self.verifyFieldsValidity()
        return None
    
    
    @Slot(str)
    def formatField(self, field_to_format:str) -> None:
        '''
        Es llamado desde la señal 'editingFinished' de 'lineEdit_phoneNumber' | desde el método 
        'self.onDebtorNameAndSurnameEditingFinished'.
        
        Dependiendo del campo 'field_to_format' formatea el texto y lo asigna en el campo correspondiente.
        
        PARAMS:
        - field_to_format: el campo a formatear. Admite los siguientes valores:
            - DEBTOR_NAME: formatea el campo de nombre del deudor.
            - DEBTOR_SURNAME: formatea el campo de apellido del deudor.
            - DEBTOR_PHONE_NUMBER: formatea el campo de teléfono del deudor.

        Retorna None.
        '''
        field_text:str
        phone_number:PhoneNumber # se usa cuando el campo a formatear es el de núm. de teléfono
        
        match field_to_format:
            case 'DEBTOR_NAME': # pasa a minúsculas y pone en mayúsculas la primera letra de cada nombre
                field_text = self.debtorData.lineEdit_debtorName.text()
                field_text = field_text.lower().title()
                self.debtorData.lineEdit_debtorName.setText(field_text)
            
            case 'DEBTOR_SURNAME': # pasa a minúsculas y pone en mayúsculas la primera letra de cada apellido
                field_text = self.debtorData.lineEdit_debtorSurname.text()
                field_text = field_text.lower().title()
                self.debtorData.lineEdit_debtorSurname.setText(field_text)
            
            case 'DEBTOR_PHONE_NUMBER': # agrega un "+" al principio (si no tiene) y formatea el núm. estilo internacional
                field_text = self.debtorData.lineEdit_phoneNumber.text()
                try:
                    phone_number = parse(f"+{field_text}")
                    if is_valid_number(phone_number):
                        field_text = format_number(phone_number, PhoneNumberFormat.INTERNATIONAL)
                
                except NumberParseException as err:
                    logging.error(err)
                    field_text = self.debtorData.lineEdit_phoneNumber.text()
                
                self.debtorData.lineEdit_phoneNumber.setText(field_text)
        
        return None
    
    
    def verifyFieldsValidity(self) -> None:
        '''
        Es llamado desde los métodos 'self.validatorOnValidationSucceded' | 'self.validatorOnValidationFailed'.
        
        Verifica si todos los campos son válidos y activa o desactiva el botón "Aceptar".
        
        Retorna None.
        '''
        # activa o desactiva el botón "Aceptar" si todos los campos son válidos
        if all(self.VALID_FIELDS.values()):
            self.debtorData.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)
        else:
            self.debtorData.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
        return None
    

    @Slot()
    def onDebtorNameAndSurnameEditingFinished(self, field_validated:str) -> None:
        '''
        Es llamado desde la señal 'editingFinished' de 'lineEdit_debtorName' | 'lineEdit_debtorSurname'.
        
        Crea un QCompleter para el campo opuesto, es decir, si 'field_validated' es 'DEBTOR_NAME' crea un 
        completer para 'DEBTOR_SURNAME', y viceversa.
        Llama al método 'self.formatField' para formatear los campos y si existe esa combinación de nombre y 
        apellido busca el número de teléfono, la dirección y el código postal existente del usuario y los 
        coloca en sus respectivos campos, luego desactiva los campos para evitar su modificación.
        
        Retorna None.
        '''
        debtor_data:list[tuple[str,str,str]]
        
        self.formatField(field_to_format=field_validated)
        
        # crea QCompleters
        if field_validated == 'DEBTOR_NAME': # crea completer para apellidos que coincidan con el nombre
            self.debtorData.lineEdit_debtorSurname.setCompleter(
                createCompleter(sql="SELECT DISTINCT apellido FROM Deudores WHERE nombre = ?",
                                params=(self.debtorData.lineEdit_debtorName.text(),)
                                )
                )
        
        elif field_validated == 'DEBTOR_SURNAME': # crea completer para nombres que coincidan con el apellido
            self.debtorData.lineEdit_debtorName.setCompleter(
                createCompleter(sql="SELECT DISTINCT nombre FROM Deudores WHERE apellido = ?",
                                params=(self.debtorData.lineEdit_debtorSurname.text(),)
                                )
                )
        
        # si ambos campos son válidos es porque ambos campos se llenaron, y coloca los datos en los campos restantes
        if self.VALID_FIELDS['DEBTOR_NAME'] and self.VALID_FIELDS['DEBTOR_SURNAME']:
            # obtengo los datos desde la cta. cte.
            debtor_data = makeReadQuery(
                sql="SELECT num_telefono, direccion, codigo_postal FROM Deudores WHERE (nombre = ?) AND (apellido = ?);",
                params=(self.debtorData.lineEdit_debtorName.text(), self.debtorData.lineEdit_debtorSurname.text(), ))
            
            # los coloco en sus campos (si se encontraron coincidencias)
            if len(debtor_data) > 0:
                self.debtorData.lineEdit_phoneNumber.setEnabled(False)
                self.debtorData.lineEdit_direction.setEnabled(False)
                self.debtorData.lineEdit_postalCode.setEnabled(False)
                
                self.debtorData.lineEdit_phoneNumber.setText( str(debtor_data[0][0]) )
                self.debtorData.lineEdit_direction.setText( str(debtor_data[0][1]) )
                self.debtorData.lineEdit_postalCode.setText( str(debtor_data[0][2]) )
            
            else:
                self.debtorData.lineEdit_phoneNumber.setEnabled(True)
                self.debtorData.lineEdit_direction.setEnabled(True)
                self.debtorData.lineEdit_postalCode.setEnabled(True)
        
        return None
    
    
    # botón Aceptar

    def getFieldsData(self) -> dict[str, str]:
        '''
        Es llamado desde 'self.handleOkClicked'.
        
        Obtiene todos los datos de los campos y los formatea de ser necesario.
        
        Retorna un dict[str,str] con los valores.
        '''
        # title() hace que cada palabra comience con mayúsculas...
        values = {
            'name':self.debtorData.lineEdit_debtorName.text().title(), # 0, nombre
            'surname':self.debtorData.lineEdit_debtorSurname.text().title(), # 1, apellido
            'phone_num':self.debtorData.lineEdit_phoneNumber.text(), # 2, número de teléfono
            'direction':self.debtorData.lineEdit_direction.text().title(), # 3, dirección
            'postal_code':self.debtorData.lineEdit_postalCode.text() # 4, código postal
        }
        return values
    

    @Slot()
    def handleOkClicked(self) -> None:
        '''
        Es llamado desde la señal 'clicked' del botón "Aceptar".
        
        Obtiene los datos de los campos formateados e inserta los valores en la base de datos en las tablas de 
        "Deudores" (si no existe el deudor). Al final emite la señal 'debtorChosen' con el "IDdeudor", "nombre" 
        y "apellido" del deudor al método 'MainWindow.handleFinishedSale' confirmando que se eligió un deudor.
        
        Retorna None.
        '''
        # obtiene los valores formateados de los campos...
        values:dict[str,str] = self.getFieldsData()
        count_query:int
        query:tuple # tiene una tupla con IDdeudor, nombre y apellido

        # verifica si el deudor existe en Deudores
        count_query = makeReadQuery(
            sql="SELECT COUNT(*) FROM Deudores WHERE nombre = ? AND apellido = ?;",
            params=(values['name'], values['surname'],)
            )[0][0] # si el deudor no existe devuelve 0

        try:
            conn = createConnection("database/inventario.db")
            cursor = conn.cursor()
            
            # si no existe ese deudor, lo agrega...
            if not count_query:
                # declara la consulta sql y params de Deudores y hace la consulta...
                cursor.execute(
                    "INSERT INTO Deudores(nombre, apellido, num_telefono, direccion, codigo_postal) VALUES(?, ?, ?, ?, ?);",
                    (values['name'], values['surname'], values['phone_num'], values['direction'], values['postal_code'],)
                    )
                
                conn.commit()
                logging.debug(LoggingMessage.DEBUG_DB_SINGLE_INSERT_SUCCESS)

            # trae el ID, el nombre y el apellido del deudor para luego mandarlo a MainWindow en la señal 'debtorChosen'
            query = makeReadQuery(
                sql="SELECT IDdeudor, nombre, apellido FROM Deudores WHERE (nombre = ?) AND (apellido = ?);",
                params=(values['name'], values['surname'],)
                )[0]

            # envía señal comunicando que sí se eligió un deudor, y envía un tuple(IDdeudor, nombre y apellido)
            self.debtorChosen.emit(query)
            
        except sqlite3Error as err:
            conn.rollback()
            logging.error(LoggingMessage.ERROR_DB_INSERT, f"{err.sqlite_errorcode}: {err.sqlite_errorname} / {err}")
        
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

