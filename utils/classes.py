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

from sqlite3 import (Error as sqlite3Error)



# Dialog con datos de un producto
class ProductDialog(QDialog):
    '''QDialog creado al presionar el botón 'MainWindow.btn_add_product_inventory'. Sirve para crear un nuevo registro 
    de producto en la tabla "Productos" en la base de datos.'''
    def __init__(self):
        super(ProductDialog, self).__init__()
        self.productDialog_ui = Ui_Dialog()
        self.productDialog_ui.setupUi(self)
        self.productDialog_ui.buttonBox.button(QDialogButtonBox.Ok).setText("Aceptar")
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
        name_re = QRegularExpression(".*")
        float_re = QRegularExpression("[0-9]{0,9}[.|,]?[0-9]{0,2}")

        name_validator = QRegularExpressionValidator(name_re, self.productDialog_ui.lineedit_productName)
        self.productDialog_ui.lineedit_productName.setValidator(name_validator)
        stock_validator = QRegularExpressionValidator(float_re, self.productDialog_ui.lineedit_productStock)
        self.productDialog_ui.lineedit_productStock.setValidator(stock_validator)
        unitPrice_validator = QRegularExpressionValidator(float_re, self.productDialog_ui.lineedit_productUnitPrice)
        self.productDialog_ui.lineedit_productUnitPrice.setValidator(unitPrice_validator)
        comercialPrice_validator = QRegularExpressionValidator(float_re, self.productDialog_ui.lineedit_productComercialPrice)
        self.productDialog_ui.lineedit_productComercialPrice.setValidator(comercialPrice_validator)
        
        # completers
        createCompleter(self.productDialog_ui.lineedit_productName, type=3)

        # flags de validación
        self.VALID_STOCK:bool = None
        self.VALID_NAME:bool = None
        self.VALID_CATEGORY:bool = None
        self.VALID_UNIT_PRICE:bool = None
        self.VALID_COMERCIAL_PRICE:bool = None

        #--- SEÑALES --------------------------------------------------
        self.productDialog_ui.lineedit_productName.textChanged.connect(self.__checkProductNameValidity)
        
        self.productDialog_ui.cb_productCategory.currentIndexChanged.connect(self.__checkProductCategoryValidity)
        
        self.productDialog_ui.lineedit_productStock.textChanged.connect(lambda: self.__checkProductStockValidity())
        self.productDialog_ui.lineedit_productStock.editingFinished.connect(lambda: self.__checkProductStockValidity(True))
        
        self.productDialog_ui.lineedit_productUnitPrice.textChanged.connect(lambda: self.__checkProductUnitPriceValidity(False))
        self.productDialog_ui.lineedit_productUnitPrice.editingFinished.connect(lambda: self.__checkProductUnitPriceValidity(True))
        
        self.productDialog_ui.lineedit_productComercialPrice.textChanged.connect(lambda: self.__checkProductComercialPriceValidity(False))
        self.productDialog_ui.lineedit_productComercialPrice.editingFinished.connect(lambda: self.__checkProductComercialPriceValidity(True))
        
        self.productDialog_ui.buttonBox.accepted.connect(self.addProductToDatabase)
    
    #### MÉTODOS #####################################################
    # funciones de validación de campos
    @Slot(bool)
    def __checkProductStockValidity(self, editing_finished:bool = False) -> None:
        '''Verifica si 'lineedit_productStock' tiene un nombre válido. Si es válido 'self.VALID_STOCK' será True, sino 
        False. Modifica el texto de 'label_stockWarning' de acuerdo a las condiciones, y el estilo del campo. Retorna 'None'.'''
        stock:int | float | str

        # reinicio la validez del stock
        self.VALID_STOCK = True

        # si es texto vacío o si no es un número...
        if self.productDialog_ui.lineedit_productStock.text().strip() == "" or self.productDialog_ui.lineedit_productStock.text().replace(",","").replace(".","").isnumeric() == False:
            self.VALID_STOCK = False
            self.productDialog_ui.label_stockWarning.setText("El stock debe ser un número")
        # sino, formatea el valor
        else:
            stock = self.productDialog_ui.lineedit_productStock.text().replace(",",".")

            if editing_finished and self.productDialog_ui.lineedit_productStock.text().endswith("."):
                stock = self.productDialog_ui.lineedit_productStock.text().replace(".","")
            
            # intenta convertir el valor a int ó a float
            try:
                stock = int(self.productDialog_ui.lineedit_productStock.text()) if float(self.productDialog_ui.lineedit_productStock.text()).is_integer() else float(self.productDialog_ui.lineedit_productStock.text())
            except ValueError:
                pass
            # reemplaza al texto del lineedit por el nuevo formateado
            self.productDialog_ui.lineedit_productStock.setText(str(stock))

        # si es válido, borra el mensaje de error y cambia el estilo del lineedit
        if self.VALID_STOCK:
            self.productDialog_ui.label_stockWarning.setText("")
            self.productDialog_ui.lineedit_productStock.setStyleSheet("border: 1px solid #0f0; background-color: rgb(185, 255, 185);")
        else:
            self.productDialog_ui.lineedit_productStock.setStyleSheet("border: 1px solid #f00; background-color: rgb(255, 185, 185);")
        self.verifyFieldsValidity()
        return None


    @Slot()
    def __checkProductNameValidity(self) -> None:
        '''
        Verifica si 'lineedit_productName' tiene valores válidos. Si son válidos 'self.VALID_NAME' será True, sino 
        False. Modifica el texto de 'label_nameWarning' de acuerdo a las condiciones, y el estilo del campo. 
        
        Retorna None.
        '''
        # reinicio la validez del nombre
        self.VALID_NAME = True
        
        # si el producto no tiene nombre (si el campo está vacío)...
        if self.productDialog_ui.lineedit_productName.text() == "":
            self.VALID_NAME = False
            self.productDialog_ui.label_nameWarning.setText("El producto debe tener un nombre")
        
        # hace un SELECT a la Productos para ver si ya existe ese nombre...
        if self.VALID_NAME and makeReadQuery("SELECT nombre FROM Productos WHERE nombre = ?;", (self.productDialog_ui.lineedit_productName.text(),)):
            self.VALID_NAME = False
            self.productDialog_ui.label_nameWarning.setText("Ya existe un producto con ese nombre")
        
        if self.VALID_NAME:
            self.productDialog_ui.label_nameWarning.setText("")
            self.productDialog_ui.lineedit_productName.setStyleSheet("border: 1px solid #0f0; background-color: rgb(185, 255, 185);")
        else:
            self.productDialog_ui.lineedit_productName.setStyleSheet("border: 1px solid #f00; background-color: rgb(255, 185, 185);")
        self.verifyFieldsValidity()
        return None


    @Slot()
    def __checkProductCategoryValidity(self) -> None:
        '''Verifica si 'cb_productCategory' tiene una categoría seleccionada. Si la tiene, se considera válido y 
        'self.VALID_CATEGORY' será True, sino False. Modifica el texto de 'label_categoryWarning' de acuerdo a las 
        condiciones, y el estilo del campo. Retorna 'None'.'''
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
            self.productDialog_ui.cb_productCategory.setStyleSheet("border: 1px solid #f00; background-color: rgb(255, 185, 185);")

        if current_text and self.VALID_CATEGORY:
            self.productDialog_ui.label_categoryWarning.setText("")
            self.productDialog_ui.cb_productCategory.setStyleSheet("border: 1px solid #0f0; background-color: rgb(185, 255, 185);")
        else:
            self.productDialog_ui.cb_productCategory.setStyleSheet("border: 1px solid #f00; background-color: rgb(255, 185, 185);")
        self.verifyFieldsValidity()
        return None


    @Slot(bool)
    def __checkProductUnitPriceValidity(self, editing_finished:bool) -> None:
        '''Verifica si 'lineedit_productUnitPrice' tiene un precio válido. Si es válido 'self.VALID_UNIT_PRICE' será True, 
        sino False. Modifica el texto de 'label_unitPriceWarning' de acuerdo a las condiciones, y el estilo del campo. Retorna 
        'None'.'''
        # reinicio la validez del precio unitario
        self.VALID_UNIT_PRICE = True
        value:str = self.productDialog_ui.lineedit_productUnitPrice.text()
        if not editing_finished:
            value_is_numeric:str = self.productDialog_ui.lineedit_productUnitPrice.text().replace(",","").replace(".","")
            # si el campo está vacío o no es un número...
            if value == "" or value_is_numeric.isnumeric() == False:
                self.VALID_UNIT_PRICE = False
                self.productDialog_ui.label_unitPriceWarning.setText("El precio unitario debe ser un número")
            # EAFP: intenta convertir el valor a float() para ver si es número...
            try:
                # antes de ver si es float(), reemplazo las comas decimales por puntos, si tiene...
                unit_price = float(self.productDialog_ui.lineedit_productUnitPrice.text().replace(",","."))
                if unit_price < 0:
                    self.VALID_UNIT_PRICE = False
                    self.productDialog_ui.label_unitPriceWarning.setText("El precio unitario debe ser mayor o igual a 0")
            except ValueError:
                pass
        # si se presionó Enter (o se terminó de editar)...
        else:
            if value != "":
                # si el número empieza o termina en "." ó ","...
                if value.startswith((",",".")) or value.endswith((",",".")):
                    # EAFP: intenta convertirlo a float y cambia el texto en el lineedit
                    try:
                        unit_price = self.productDialog_ui.lineedit_productUnitPrice.text().replace(",",".")
                        unit_price = round(float(unit_price), 2)
                        self.productDialog_ui.lineedit_productUnitPrice.setText(str(unit_price))
                    except ValueError:
                        pass
                # si el número es sólo "," ó "."...
                if value == "." or value == ",":
                    unit_price = "0.0"
                    self.productDialog_ui.lineedit_productUnitPrice.setText(unit_price)
            else:
                self.VALID_UNIT_PRICE = False
                self.productDialog_ui.label_unitPriceWarning.setText("El precio unitario debe ser un número")
        # si el campo tiene un valor Y es válido...
        if value != "" and self.VALID_UNIT_PRICE:
            self.productDialog_ui.label_unitPriceWarning.setText("")
            self.productDialog_ui.lineedit_productUnitPrice.setStyleSheet("border: 1px solid #0f0; background-color: rgb(185, 255, 185);")
        # sino, si es inválido (no importa si está vacío)...
        elif not self.VALID_UNIT_PRICE:
            self.productDialog_ui.lineedit_productUnitPrice.setStyleSheet("border: 1px solid #f00; background-color: rgb(255, 185, 185);")
        self.verifyFieldsValidity()
        return None


    @Slot()
    def __checkProductComercialPriceValidity(self, editing_finished:bool) -> None:
        '''Verifica si 'lineedit_productComercialPrice' tiene un precio válido. Si es válido 'self.VALID_COMERCIAL_PRICE' 
        será True, sino False. Al ser este campo opcional, no se considera inválido el campo vacío. Modifica el texto de 
        'label_comercialPriceWarning' de acuerdo a las condiciones, y el estilo del campo. Retorna 'None'.'''
        value = self.productDialog_ui.lineedit_productComercialPrice.text()
        if not editing_finished:
            # quita todos los "." y ",", sino no lo considera un número el método 'isnumeric()'
            value_is_numeric = value.replace(",","").replace(".","")
            # si no es un número...
            if value != "" and value_is_numeric.isnumeric() == False:
                self.VALID_COMERCIAL_PRICE = False
                self.productDialog_ui.label_comercialPriceWarning.setText("El precio comercial debe ser un número")
            # EAFP (otra vez)
            try:
                # reemplaza comas decimales por puntos, luego convierte el str a float y verifica si es negativo...
                comercial_price = self.productDialog_ui.lineedit_productComercialPrice.text().replace(",",".")
                comercial_price = round(float(comercial_price), 2)
                if comercial_price < 0 and self.productDialog_ui.lineedit_productComercialPrice.text() != "":
                    self.VALID_COMERCIAL_PRICE = False
                    self.productDialog_ui.label_comercialPriceWarning.setText("El precio comercial debe ser mayor o igual a 0")
            except ValueError:
                pass
        # si se presionó Enter o se terminó de editar...
        else:
            if value != "":
                # si el número empieza o termina en "." ó ","...
                if value.startswith((",",".")) or value.endswith((",",".")):
                    # EAFP: intenta convertirlo a float y cambia el texto en el lineedit
                    try:
                        comercial_price = self.productDialog_ui.lineedit_productComercialPrice.text().replace(",",".")
                        comercial_price = round(float(comercial_price), 2)
                        self.productDialog_ui.lineedit_productComercialPrice.setText(str(comercial_price))
                        self.VALID_COMERCIAL_PRICE = True
                    except ValueError:
                        pass
                # si el número es sólo "," ó "."...
                if value == "." or value == ",":
                    comercial_price = "0.0"
                    self.productDialog_ui.lineedit_productComercialPrice.setText(comercial_price)
                    self.VALID_COMERCIAL_PRICE = True
            else:
                self.VALID_COMERCIAL_PRICE = True
        # si el campo tiene un valor Y es válido...
        if value != "" and self.VALID_COMERCIAL_PRICE:
            self.productDialog_ui.label_comercialPriceWarning.setText("")
            self.productDialog_ui.lineedit_productComercialPrice.setStyleSheet("border: 1px solid #0f0; background-color: rgb(185, 255, 185);")
        # sino, si es inválido (no importa si está vacío)...
        elif not self.VALID_COMERCIAL_PRICE:
            self.productDialog_ui.lineedit_productComercialPrice.setStyleSheet("border: 1px solid #f00; background-color: rgb(255, 185, 185);")
        self.verifyFieldsValidity()
        return None


    def verifyFieldsValidity(self) -> None:
        '''
        Es llamada desde cada método de tipo '__check...'.
        
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
            self.productDialog_ui.lineedit_productStock.text().replace(".",""),
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
        Crea una instancia de 'workerclasses.DbInsertWorker' para que haga la consulta INSERT en un QThread diferente.
        
        Retorna None.
        '''
        self.INSERT_THREAD = QThread()
        self.insert_worker = DbInsertWorker()
        
        self.insert_worker.moveToThread(self.INSERT_THREAD)
        
        if self.productDialog_ui.buttonBox.button(QDialogButtonBox.Ok).isEnabled() == False:
            return None
        data:tuple[str] = self.__getFieldsData()
        sql = "INSERT INTO Productos(nombre,descripcion,stock,unidad_medida,precio_unit,precio_comerc,IDcategoria) VALUES(?,?,?,?,?,?,(SELECT IDcategoria FROM Categorias WHERE nombre_categoria=?));"
        
        # makeInsertQuery(sql, data)
        self.INSERT_THREAD.started.connect(lambda: self.insert_worker.executeInsertQuery(
            data_sql=sql,
            data_params=data))
        self.insert_worker.finished.connect(self.INSERT_THREAD.quit)
        self.insert_worker.finished.connect(self.INSERT_THREAD.wait)
        self.INSERT_THREAD.finished.connect(self.insert_worker.deleteLater)
        
        self.INSERT_THREAD.start()
        return None
    




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

        # esconde los campos de datos del deudor
        self.saleDialog_ui.debtor_data.setEnabled(False)
        self.saleDialog_ui.debtor_data.hide()

        # QCompleters
        createCompleter(self.saleDialog_ui.lineEdit_debtorName, 1)
        createCompleter(self.saleDialog_ui.lineEdit_debtorSurname, 2)

        # validators
        float_re = QRegularExpression("[0-9]{0,9}(\.|,)?[0-9]{0,2}")

        quantityValidator = QRegularExpressionValidator(float_re, self.saleDialog_ui.lineEdit_productQuantity)
        self.saleDialog_ui.lineEdit_productQuantity.setValidator(quantityValidator)

        totalPaidValidator = QRegularExpressionValidator(float_re, self.saleDialog_ui.lineEdit_totalPaid)
        self.saleDialog_ui.lineEdit_totalPaid.setValidator(totalPaidValidator)


        self.saleDialog_ui.lineEdit_postalCode.setValidator(QIntValidator(1, 9_999))
        
        # flags de validación
        self.VALID_DEBTOR_NAME:bool = None
        self.VALID_DEBTOR_SURNAME:bool = None
        self.VALID_PHONE_NUMBER:bool = True # el número de tel. es opcional, así que si está vacío es válido...
        self.VALID_POSTAL_CODE:bool = True # y el código postal también

        #--- SEÑALES --------------------------------------------------
        self.saleDialog_ui.lineEdit_saleDetail.editingFinished.connect(self.validateInputFields)

        self.saleDialog_ui.comboBox_productName.currentIndexChanged.connect(self.validateInputFields)

        self.saleDialog_ui.lineEdit_productQuantity.textChanged.connect(self.validateInputFields)

        self.saleDialog_ui.lineEdit_totalPaid.editingFinished.connect(self.validateInputFields)
        
        self.saleDialog_ui.checkBox_comercialPrice.clicked.connect(self.validateInputFields)
        
        self.saleDialog_ui.dateTimeEdit.dateTimeChanged.connect(self.validateInputFields)
        
        self.saleDialog_ui.lineEdit_debtorName.textChanged.connect(self.__validateDebtorNameField)
        
        self.saleDialog_ui.lineEdit_debtorSurname.textChanged.connect(self.__validateDebtorSurnameField)
        
        self.saleDialog_ui.lineEdit_phoneNumber.textChanged.connect(self.__validateDebtorPhoneNumberField)
        
        self.saleDialog_ui.lineEdit_postalCode.textChanged.connect(self.__validateDebtorPostalCodeField)
        
        self.saleDialog_ui.buttonBox.accepted.connect(lambda: self.handleOkClicked())

    #### MÉTODOS #####################################################
    # funciones de validación de datos
    def __validateNameField(self) -> bool:
        '''Verifica si el campo de nombre del producto es válido; cambia el texto de 'label_productName_feedback'
        dependiendo de la condición y el estilo del campo. Retorna True si es válido, sino False. '''
        valid_name = True
        # si no se eligió el nombre del producto...
        if self.saleDialog_ui.comboBox_productName.currentText().strip() == "":
            valid_name = False
            self.saleDialog_ui.comboBox_productName.setCurrentIndex(-1)
        if self.saleDialog_ui.comboBox_productName.currentIndex() == -1:
            valid_name = False
            self.saleDialog_ui.label_productName_feedback.setText("El campo de nombre del producto no puede estar vacío")
            self.saleDialog_ui.comboBox_productName.setStyleSheet("border: 1px solid #f00; background-color: rgb(255, 185, 185);")

        if valid_name:
            self.saleDialog_ui.label_productName_feedback.setText("")
            self.saleDialog_ui.comboBox_productName.setStyleSheet("border: 1px solid #0f0; background-color: rgb(185, 255, 185);")
        return valid_name


    def __getProductTotalCost(self, productName:str, quantity:int, is_comercial_price:bool) -> float:
        '''Hace una consulta SELECT a la base de datos y obtiene el precio (unitario o comercial) del producto. 
        Retorna un 'float'.'''
        conn = createConnection("database/inventario.db")
        if not conn:
            return None
        cursor = conn.cursor()
        # NOTE: SQLite3 por alguna razón no permite pasar nombres de columnas como parámetro, así que hay que 
        # escribirlos explícitamente, de ahí que haga el match a continuación...
        match is_comercial_price:
            case True:
                sql:str = "SELECT ? * precio_comerc FROM Productos WHERE nombre = ?;"
            case False:
                sql:str = "SELECT ? * precio_unit FROM Productos WHERE nombre = ?;"
        params = (quantity, productName,)
        totalCost = cursor.execute(sql, params).fetchone()[0]
        return totalCost


    def __getCurrentProductStock(self, productName:str) -> tuple:
        '''Hace una consulta SELECT y obtiene el stock actual del producto ingresado. Retorna una tupla con el stock 
        como número y la unidad de medida como 'str'.'''
        conn:Connection | None
        stock:int | float
        measurement_unit:str

        conn = createConnection("database/inventario.db")
        if not conn:
            return None
        cursor = conn.cursor()
        query = cursor.execute("SELECT stock, unidad_medida FROM Productos WHERE nombre = ?;", (productName,)).fetchone()
        if len(query) == 2:
            stock, measurement_unit = [q for q in query]
        else:
            stock = query[0]
            measurement_unit = ""
        # intenta convertir el stock a int
        try:
            stock = int(stock) if float(stock).is_integer() else float(stock)
        except:
            pass
        return stock, measurement_unit


    def __validateQuantityField(self) -> bool:
        '''Verifica si el campo de cantidad del producto es válido; cambia el texto de 'label_productQuantity_feedback'
        dependiendo de la condición; además cambia el texto de 'label_productTotalCost' y muestra el costo total; cambia 
        el estilo del campo. Retorna True si es válido, sino False.'''
        valid_quantity = True
        cb_curr_idx = self.saleDialog_ui.comboBox_productName.currentIndex()
        quantity:int|float = 0

        # si es texto está vacío o si no es un número...
        if self.saleDialog_ui.lineEdit_productQuantity.text().strip() == "" or self.saleDialog_ui.lineEdit_productQuantity.text().replace(".","").replace(",","").isnumeric() == False:
            valid_quantity = False
            self.saleDialog_ui.label_productQuantity_feedback.setText("El stock debe ser un número")
        else:
            # verifico si la cantidad introducida es mayor al stock disponible...
            if self.saleDialog_ui.comboBox_productName.currentIndex() != -1:
                current_stock, measurement_unit = self.__getCurrentProductStock(self.saleDialog_ui.comboBox_productName.itemText(cb_curr_idx))
                try:
                    if float(current_stock) < float(self.saleDialog_ui.lineEdit_productQuantity.text().strip()):
                        valid_quantity = False
                        self.saleDialog_ui.label_productQuantity_feedback.setText(f"El stock disponible es de {current_stock} {measurement_unit}")
                except ValueError:
                    pass
        
        # si el stock es válido...
        if valid_quantity:
            self.saleDialog_ui.label_productQuantity_feedback.setText("")
            self.saleDialog_ui.lineEdit_productQuantity.setStyleSheet("border: 1px solid #0f0; background-color: rgb(185, 255, 185);")
            
            try:
                quantity = int(self.saleDialog_ui.lineEdit_productQuantity.text()) if float(self.saleDialog_ui.lineEdit_productQuantity.text().replace(",",".")).is_integer() else float(self.saleDialog_ui.lineEdit_productQuantity.text().replace(",","."))
            except ValueError:
                pass
            # obtiene el precio (unitario o comercial) del producto, en tanto se haya seleccionado un producto...
            if self.saleDialog_ui.comboBox_productName.currentIndex() != -1:
                # si la checkbox de precio comercial está checkeada obtiene el precio comercial...
                if self.saleDialog_ui.checkBox_comercialPrice.isChecked():
                    totalCost = self.__getProductTotalCost(self.saleDialog_ui.comboBox_productName.itemText(cb_curr_idx), quantity, True)
                # sino obtiene el precio unitario (el normal)...
                else:
                    totalCost = self.__getProductTotalCost(self.saleDialog_ui.comboBox_productName.itemText(cb_curr_idx), quantity, False)
                
                try:
                    totalCost = round(float(totalCost), 2)
                except:
                    pass

                totalCost = "NO DISPONIBLE" if totalCost is None or totalCost == ("" or "0" or "0.0" or 0.0 or 0) else f"$ {totalCost}"
                self.saleDialog_ui.label_productTotalCost.setText(f"<html><head/><body><p><span style=\" font-size:20px; color: #111;\">COSTO TOTAL </span><span style=\" font-size: 20px; color: #22577a;\">{totalCost}</span></p></body></html>")
        # si el stock es inválido...
        else:
            self.saleDialog_ui.lineEdit_productQuantity.setStyleSheet("border: 1px solid #f00; background-color: rgb(255, 185, 185);")
        return valid_quantity


    def __validatePaidField(self) -> bool:
        '''Verifica si el campo de cantidad abonada es válido; cambia el texto de 'label_totalPaid_feedback'
        dependiendo de la condición; además muestra o esconde 'debtor_data' con los campos de datos del deudor 
        dependiendo de si el valor ingresado es menor al total a pagar o no; cambia el estilo del campo. Retorna 
        True si es válido, sino False'''
        valid_total_paid:bool = True
        total_paid = None # guarda el total pagado (no confundir con el costo total)
        value = self.saleDialog_ui.lineEdit_totalPaid.text().replace(",","").replace(".","")
        # si el campo está vacío o no es un número...
        if self.saleDialog_ui.lineEdit_totalPaid.text() == "" or value.isnumeric() == False:
            valid_total_paid = False
            self.saleDialog_ui.label_totalPaid_feedback.setText("La cantidad abonada debe ser un número")
        # EAFP: intenta convertir el valor a float() para ver si es número...
        try:
            total_paid = self.saleDialog_ui.lineEdit_totalPaid.text().replace(",",".")
            if float(total_paid) < 0:
                valid_total_paid = False
                self.saleDialog_ui.label_totalPaid_feedback.setText("La cantidad abonada debe ser mayor o igual a 0")
        except ValueError:
            pass
        
        if valid_total_paid:
            self.saleDialog_ui.label_totalPaid_feedback.setText("")
            self.saleDialog_ui.lineEdit_totalPaid.setStyleSheet("border: 1px solid #0f0; background-color: rgb(185, 255, 185);")
            re_total_cost:Match = search(">[$] [0-9]+[.]?[0-9]*<", self.saleDialog_ui.label_productTotalCost.text())
            if re_total_cost:
                re_total_cost:str = re_total_cost.group()
                try:
                    re_total_cost = float(re_total_cost.strip("><").replace(" ","").replace(">","").replace("$",""))
                    total_paid = float(total_paid)
                except ValueError:
                    pass
            
            # verifica si lo abonado es menor ó mayor al costo total (se considera deuda/a favor)
            if self.saleDialog_ui.lineEdit_totalPaid.text() != "" and total_paid != re_total_cost:
                if total_paid != re_total_cost:
                    self.setSaleDialogSize(615, 525, False)
                    self.updateDebtorDataWidgetsState(True)
            else:
                self.setSaleDialogSize(615, 295, True)
                self.updateDebtorDataWidgetsState(False)
        else:
            self.saleDialog_ui.lineEdit_totalPaid.setStyleSheet("border: 1px solid #f00; background-color: rgb(255, 185, 185);")
        return valid_total_paid


    @Slot()
    def __validateDebtorNameField(self) -> None:
        '''Verifica si el campo de nombre del deudor es válido; cambia el texto de 'label_debtorName_feedback'
        dependiendo de la condición, y cambia el estilo del campo. 'self.VALID_DEBTOR_NAME' es True si es válido, 
        sino False. Retorna 'None'.'''
        # validación de datos
        self.VALID_DEBTOR_NAME = True
        # verifica que no esté vacío
        if self.saleDialog_ui.lineEdit_debtorName.text().strip() == "":
            self.VALID_DEBTOR_NAME = False
            self.saleDialog_ui.label_debtorName_feedback.setText("Se necesita un nombre")
            self.saleDialog_ui.lineEdit_debtorName.setStyleSheet("border: 1px solid #f00; background-color: rgb(255, 185, 185);")
        else:
            self.saleDialog_ui.label_debtorName_feedback.setText("")
            self.saleDialog_ui.lineEdit_debtorName.setStyleSheet("border: 1px solid #0f0; background-color: rgb(185, 255, 185);")
        self.validateInputFields()
        return None


    @Slot()
    def __validateDebtorSurnameField(self) -> None:
        '''Verifica si el campo de apellido del deudor es válido; cambia el texto de 'label_debtorSurname_feedback'
        dependiendo de la condición, y cambia el estilo del campo. 'self.VALID_DEBTOR_SURNAME' es True si es válido, 
        sino False. Retorna 'None'.'''
        self.VALID_DEBTOR_SURNAME = True
        # verifica que no esté vacío
        if self.saleDialog_ui.lineEdit_debtorSurname.text().strip() == "":
            self.VALID_DEBTOR_SURNAME = False
            self.saleDialog_ui.label_debtorSurname_feedback.setText("Se necesita un apellido")
            self.saleDialog_ui.lineEdit_debtorSurname.setStyleSheet("border: 1px solid #f00; background-color: rgb(255, 185, 185);")
        else:
            self.saleDialog_ui.label_debtorSurname_feedback.setText("")
            self.saleDialog_ui.lineEdit_debtorSurname.setStyleSheet("border: 1px solid #0f0; background-color: rgb(185, 255, 185);")
        self.validateInputFields()
        return None
    

    @Slot()
    def __validateDebtorPhoneNumberField(self) -> None:
        '''Verifica si el campo de número de teléfono es válido; cambia el texto de 'label_phoneNumber_feedback' dependiendo 
        de la condición, y cambia el estilo del campo. Retorna 'True' si es válido, sino 'False'.'''
        self.VALID_PHONE_NUMBER = True
        phone_number:str = self.saleDialog_ui.lineEdit_phoneNumber.text().replace(" ", "").replace("+", "").replace("-", "")[2:]
        # si no está vacío...
        if phone_number != "":
            # si tiene menos de 6 dígitos (phone_number no tiene los primeros 2 dígitos, por eso pongo 4)...
            if 0 < len(phone_number) < 4:
                self.VALID_PHONE_NUMBER = False
                self.saleDialog_ui.label_phoneNumber_feedback.setText("El número de teléfono es muy corto (mín.: 6)")
            elif len(phone_number) > 15:
                self.VALID_PHONE_NUMBER = False
                self.saleDialog_ui.label_phoneNumber_feedback.setText("El número de teléfono es muy largo (máx.: 15)")
            else:
                self.saleDialog_ui.label_phoneNumber_feedback.setText("")
        else:
            self.saleDialog_ui.label_phoneNumber_feedback.setText("")
        # cambia el estilo del lineedit del teléfono...
        if self.VALID_PHONE_NUMBER:
            self.saleDialog_ui.lineEdit_phoneNumber.setStyleSheet("border: 1px solid #0f0; background-color: rgb(185, 255, 185);")
        else:
            self.saleDialog_ui.lineEdit_phoneNumber.setStyleSheet("border: 1px solid #f00; background-color: rgb(255, 185, 185);")
        self.validateInputFields()
        return self.VALID_PHONE_NUMBER
    

    @Slot()
    def __validateDebtorPostalCodeField(self) -> None:
        '''Verifica si el campo de código postal es válido; cambia el texto de 'label_postalCode_feedback' dependiendo 
        de la condición, y cambia el estilo del campo. 'self.VALID_POSTAL_CODE' es True si es válido, sino False. Retorna 
        'None'.'''
        self.VALID_POSTAL_CODE = True
        postal_code:int
        # si no está vacío...
        if self.saleDialog_ui.lineEdit_postalCode.text().strip().replace(".", "").replace(",", "") != "":
            postal_code = int(self.saleDialog_ui.lineEdit_postalCode.text().strip().replace(".", "").replace(",", ""))
            if postal_code < 1:
                self.VALID_POSTAL_CODE = False
                self.saleDialog_ui.label_postalCode_feedback.setText("El código postal debe ser mayor a 1")
            elif postal_code > 9_999:
                self.VALID_POSTAL_CODE = False
                self.saleDialog_ui.label_postalCode_feedback.setText("El código postal debe ser menor a 9.999")
            else:
                self.saleDialog_ui.label_postalCode_feedback.setText("")
        else:
            self.saleDialog_ui.label_postalCode_feedback.setText("")
        # cambia el estilo del lineedit del código postal...
        if self.VALID_POSTAL_CODE:
            self.saleDialog_ui.lineEdit_postalCode.setStyleSheet("border: 1px solid #0f0; background-color: rgb(185, 255, 185);")
        else:
            self.saleDialog_ui.lineEdit_postalCode.setStyleSheet("border: 1px solid #f00; background-color: rgb(255, 185, 185);")
        self.validateInputFields()
        return None


    def validateInputFields(self) -> None:
        '''Verifica que todos los campos tengan valores válidos. Llama a las respectivas funciones y compara si todos \
        son válidos y activa o desactiva el botón "Aceptar" dependiendo del caso; además, si el campo de nombre del \
        producto y la cantidad del producto son válidos, crea un QCompleter para 'lineEdit_totalPaid' y coloca los \
        detalles de la venta llamando a '__setSaleDetails'.
        \nRetorna 'None'.'''
        # NOTE: como el nombre del producto, la cantidad y el total pagado están conectados no puedo conectar 
        # los métodos validadores directamente a las señales, porque haría que tuviera que llamar desde cada 
        # método a las otras funciones validadoras cada vez que se modifique un campo conectado, y provoca una 
        # sucesión infinita de recursiones que causa que crashee el programa.
        valid:tuple
        total_paid_completer:QCompleter
        pos_to_check:int
        quantity:str # quantity, junto con...
        product_name:str # product_name...
        price_type:str # y price_type sirven para pasar los valores esos a '__setSaleDetails()'.

        valid:tuple[bool] = (
            self.__validateNameField(),
            self.__validateQuantityField(),
            self.__validatePaidField(),
            self.VALID_DEBTOR_NAME,
            self.VALID_DEBTOR_SURNAME,
            self.VALID_PHONE_NUMBER,
            self.VALID_POSTAL_CODE
        )

        # si el nombre y la cantidad del producto son válidos, crea los detalles de venta y un QCompleter 
        # para 'lineEdit_totalPaid'
        if valid[0] and valid[1]:
            # coloca los detalles de la venta
            quantity = self.saleDialog_ui.lineEdit_productQuantity.text()
            product_name = self.saleDialog_ui.comboBox_productName.currentText()
            price_type = "P. COMERCIAL" if self.saleDialog_ui.checkBox_comercialPrice.isChecked() else "P. NORMAL"
            self.__setSaleDetails(quantity, product_name, price_type)
            # crea el completer con el precio
            total_paid_completer = self.createTotalPaidCompleter()
            self.saleDialog_ui.lineEdit_totalPaid.setCompleter(total_paid_completer)

            self.saleDialog_ui.lineEdit_totalPaid.textChanged.connect(total_paid_completer.setCompletionPrefix)
        
        # dependiendo de si 'debtor_data' está oculto...
        if self.saleDialog_ui.debtor_data.isHidden():
            pos_to_check = 3 # las primeras 3 posiciones deben ser True
        else:
            pos_to_check = 7 # todas las posiciones deben ser True
        if all(valid[:pos_to_check]):
            self.saleDialog_ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)
        else:
            self.saleDialog_ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
        return None


    def __setSaleDetails(self, quantity:int | float, product_name:str, price_type:str) -> None:
        '''Coloca la cantidad del producto vendido, el nombre y el tipo de precio aplicado en 'lineEdit_saleDetail'. \
        Retorna 'None'.'''
        re:Match | str
        new_text:str

        re = match("[0-9]{1,8} .{1,} (\(P. NORMAL\)|\(P. COMERCIAL\))", self.saleDialog_ui.lineEdit_saleDetail.text())
        re = re.group() if re else None
        if self.saleDialog_ui.lineEdit_saleDetail.text().strip() == re or self.saleDialog_ui.lineEdit_saleDetail.text().strip() == "":
            self.saleDialog_ui.lineEdit_saleDetail.setText(f"{quantity} de {product_name} ({price_type})")
        else:
            new_text = self.saleDialog_ui.lineEdit_saleDetail.text()
            new_text = sub("(\(P. NORMAL\)|\(P. COMERCIAL\))", "", self.saleDialog_ui.lineEdit_saleDetail.text())
            new_text = f"{new_text.strip()} ({price_type})"
            self.saleDialog_ui.lineEdit_saleDetail.setText(new_text)
        return None


    # funciones generales
    def setSaleDialogSize(self, min_width:int, min_height:int, hide_debtor_data:bool) -> None:
        '''Muestra/oculta 'debtor_data' y declara el nuevo tamaño mínimo del 'SaleDialog' y redimensiona la ventana 
        al tamaño. Retorna 'None'.'''
        self.setMinimumSize(min_width, min_height)
        self.resize(self.minimumSize())
        self.saleDialog_ui.debtor_data.setHidden(hide_debtor_data)
        # es importante habilitar 'debtor_data' porque sino no deja habilitar los widgets hijos
        self.saleDialog_ui.debtor_data.setEnabled(not hide_debtor_data)
        self.adjustSize()


    def updateDebtorDataWidgetsState(self, enable:bool) -> None:
        '''Habilita/deshabilita cada 'QLineEdit' en 'debtor_data' dependiendo del parámetro 'enable'. Retorna 'None'.'''
        # antes de habilitar/deshabilitar los widgets, hay que habilitar 'debtor_data', y lo hice en 'setSaleDialogSize'
        for lineEdit in self.saleDialog_ui.debtor_data.findChildren(QLineEdit):
            lineEdit.setEnabled(enable)


    def getFieldsData(self) -> tuple:
        '''
        Es llamado desde 'self.handleOkClicked' al principio.
        
        Obtiene todos los datos de los campos y formatea los valores.
        
        Retorna un tuple.'''
        re_total_cost: Match | float
        total_paid:float
        values:tuple
        phone_number:str | None

        # obtiene el costo total
        re_total_cost = search(">[$] [0-9]+[.]?[0-9]*<", self.saleDialog_ui.label_productTotalCost.text())
        if re_total_cost:
            re_total_cost = re_total_cost.group().strip("><").replace("$", "").replace(" ", "")
            # pasa a float el costo total
            try:
                re_total_cost = round(float(re_total_cost), 2)
            except ValueError:
                pass

        # pasa a float el valor abonado
        try:
            total_paid:float = round(float(self.saleDialog_ui.lineEdit_totalPaid.text()), 2)
        except ValueError:
            total_paid = self.saleDialog_ui.lineEdit_totalPaid.text()

        # si debtor_data está oculto es porque la cantidad abonada es igual o mayor al total a pagar...
        if self.saleDialog_ui.debtor_data.isHidden():
            values = (
                self.saleDialog_ui.lineEdit_saleDetail.text().strip(),
                self.saleDialog_ui.comboBox_productName.currentText(),
                self.saleDialog_ui.lineEdit_productQuantity.text(),
                self.saleDialog_ui.checkBox_comercialPrice.isChecked(),
                re_total_cost,
                total_paid,
                self.saleDialog_ui.dateTimeEdit.text()
                )
        # sino, es porque la cantidad abonada es menor al total a pagar...
        else:
            # obtengo y formateo el número de teléfono...
            phone_number = self.saleDialog_ui.lineEdit_phoneNumber.text().replace(" ", "")
            # si el largo es menor o igual a 5 se considera vacío (porque podría ser "+--", "+54--", o un número inválido...)
            if len(phone_number) <= 5:
                phone_number = ""
            elif len(phone_number) > 5 and phone_number.endswith("-"):
                phone_number.rstrip("-")
            
            values = (
                self.saleDialog_ui.lineEdit_saleDetail.text().strip(), # 0
                self.saleDialog_ui.comboBox_productName.currentText(), # 1
                self.saleDialog_ui.lineEdit_productQuantity.text(), # 2
                self.saleDialog_ui.checkBox_comercialPrice.isChecked(), # 3
                re_total_cost, # 4
                total_paid, # 5
                self.saleDialog_ui.dateTimeEdit.text(), # 6
                # title() hace que cada palabra comience con mayúsculas...
                self.saleDialog_ui.lineEdit_debtorName.text().title(), # 7
                self.saleDialog_ui.lineEdit_debtorSurname.text().title(), # 8
                phone_number, # 9
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
        - self.getFieldsData: para obtener los valores formateados de los campos.
        - self.__updateProductStock: para actualizar (luego de los INSERT) el stock en tabla "Productos".
        
        Retorna None.
        '''
        #NOTE: siempre se insertan datos en Ventas y Detalle_Ventas, pero si el "total abonado" no es igual 
        #      al "costo total" entonces se insertan datos también en Deudas y Deudores.

        # obtiene los valores formateados de los campos...
        values:tuple = self.getFieldsData()

        #! hago las consultas sin llamar funciones porque necesito tratarlas como una transacción, es decir, 
        #! se hacen todas las consultas INSERT o ninguna...
        conn = createConnection("database/inventario.db")
        if not conn:
            return None
        cursor = conn.cursor()
        
        #! lo pongo entre un try-except porque si falla necesito hacer un rollback
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
                sql_debt:str = "INSERT INTO Deudas(fecha_hora, total_adeudado, IDdeudor) VALUES(?, ?, (SELECT IDdeudor FROM Deudores WHERE nombre = ? AND apellido = ?) );"
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
            print(f"{err.sqlite_errorcode}: {err.sqlite_errorname} / {err}")
        
        finally:
            conn.close()
        return None


    def createTotalPaidCompleter(self) -> QCompleter:
        '''Crea un QCompleter para 'lineEdit_totalPaid' con el valor de 'label_productTotalCost'. Retorna un QCompleter.'''
        completer:QCompleter
        re_total_cost:Match | None | str

        # obtiene el costo total
        re_total_cost = search(">[$] [0-9]+[.]?[0-9]*<", self.saleDialog_ui.label_productTotalCost.text())
        if re_total_cost:
            re_total_cost = re_total_cost.group().strip("><").replace("$", "").replace(" ", "")

        completer = QCompleter([re_total_cost], parent=self.saleDialog_ui.lineEdit_totalPaid)
        completer.setCompletionMode(completer.CompletionMode.InlineCompletion)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)

        return completer





# item de la lista del formulario de Ventas
class ListItem(QWidget):
    '''Item creado dinámicamente dentro de la lista de formulario de ventas 'MainWindow.sales_input_list'. Sirve para 
    seleccionar un producto, la cantidad vendida, el tipo de precio (comercial o normal) y darle alguna descripción a 
    la venta.'''
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
    allFieldsValid = Signal(object) # usado en ListItem
    deletedItem = Signal(str) # usado en ListItem
    debtorChosen = Signal(object) # usado en DebtorDataDialog



# Dialog con datos de deudores
class DebtorDataDialog(QDialog):
    def __init__(self):
        super(DebtorDataDialog, self).__init__()
        self.debtorData = Ui_debtorDataDialog()
        self.debtorData.setupUi(self)
        self.dataValidation = DebtorDataValidation(self.debtorData.lineEdit_debtorName, self.debtorData.lineEdit_debtorSurname, self.debtorData.lineEdit_phoneNumber, self.debtorData.lineEdit_postalCode)

        # señal que determina si se eligió un deudor (uso self.signal.debtorChosen) (si se eligió, es 1, sino 0)
        self.signalToParent = SignalToParent()
        

        createCompleter(self.debtorData.lineEdit_debtorName, type=1)
        createCompleter(self.debtorData.lineEdit_debtorSurname, type=2)

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
    def validateFields(self, type:str) -> None:
        '''Llama a funciones de la clase 'DebtorDataValidation' para validar el campo especificado en el argumento 'type', \
        y cambia el estilo de los campos y los labels de feedback correspondientes de acuerdo a la validación. Al final activa \
        o desactiva el botón "Aceptar".
        \nRetorna 'None'.'''
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
    

    def handleOkClicked(self) -> None:
        '''Obtiene los datos de los campos formateados e inserta los valores en la base de datos en las tablas de \
        "Deudores" (si no existe el deudor). Al final envía una señal con el ID, nombre y apellido del deudor al \
        método 'MainWindow.handleFinishedSale' confirmando que se eligió un deudor. 
        \nRetorna 'None'.'''
        # obtiene los valores formateados de los campos...
        values:tuple = self.getFieldsData()
        sql:str
        params:tuple
        query:int

        # verifica si el deudor existe en Deudores
        sql  = "SELECT COUNT(*) FROM Deudores WHERE nombre = ? AND apellido = ?;"
        params = (values[0], values[1],)
        query = makeReadQuery(sql, params)[0][0] # si el deudor no existe devuelve 0

        # si no existe ese deudor, lo agrega...
        if not query:
            # declara la consulta sql y params de Deudores y hace la consulta...
            sql = "INSERT INTO Deudores(nombre, apellido, num_telefono, direccion, codigo_postal) VALUES(?, ?, ?, ?, ?);"
            params = (values[0], values[1], values[2], values[3], values[4],)
            makeInsertQuery(sql, params)

        # trae el ID, el nombre y el apellido del deudor para luego mandarlo a MainWindow en la señal 'debtorChosen'
        query = makeReadQuery("SELECT IDdeudor, nombre, apellido FROM Deudores WHERE nombre = ? AND apellido = ?;", (values[0], values[1],))[0]

        # envía señal comunicando que sí se eligió un deudor
        self.signalToParent.debtorChosen.emit(query)
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

