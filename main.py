import sys
from numpy import (empty, ndarray)
from typing import (Any)

from PySide6.QtWidgets import (QApplication, QMainWindow, QLineEdit, QTableView, 
                               QCheckBox, QAbstractItemView, QDateTimeEdit, QListWidgetItem, 
                               QLabel)
from PySide6.QtCore import (QModelIndex, Qt, QThread, Slot)
from PySide6.QtGui import (QIntValidator, QIcon)

from utils.classes import (ProductDialog, SaleDialog, ListItemWidget, ListItemValues, 
                           DebtorDataDialog, DebtsTablePersonData, WidgetStyle)
from ui.ui_mainwindow import (Ui_MainWindow)
from utils.functionutils import *
from utils.model_classes import (InventoryTableModel)
from utils.delegates import (InventoryDelegate)
from utils.workerclasses import (WorkerSelect, WorkerDelete, WorkerUpdate)
from utils.dboperations import (DatabaseRepository)
from utils.customvalidators import (SalePaidValidator)
from utils.enumclasses import (LoggingMessage, DBQueries, ModelHeaders, TableViewId, 
                               LabelFeedbackStyle, InventoryPriceType)

from resources import (rc_icons)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setup_ui()
        
        # repositorio de base de datos
        self._db_repo:DatabaseRepository = DatabaseRepository()
        
        # modelos de datos
        self.inventory_data_model:InventoryTableModel = InventoryTableModel()
        self.ui.tv_inventory_data.setModel(self.inventory_data_model)
        
        # delegados
        self.inventory_delegate = InventoryDelegate()
        self.ui.tv_inventory_data.setItemDelegate(self.inventory_delegate)
        
        # variables de modelos de datos
        #? Los acumuladores de datos sirven para cargar datos en los modelos de datos 
        #? en "batches" y mejorar el rendimiento de la aplicación de forma general
        self._inv_model_data_acc:ndarray[Any] # acumulador temporal de datos para los modelos

        #* ======== variables de 'search bars' ================================
        # TODO: reimplementar funcionalidad de search bars

        #* ======== variable de inventario ====================================
        self.IDs_products:list = [] # var. de 'tv_inventory_data' que tiene los IDs de los productos
        
        #* ======== variables de ventas =======================================
        self.ui.dateTimeEdit_sale.setDateTime(QDateTime.currentDateTime())
        
        self.IDs_saleDetails:list = [] # var. de 'tv_sales_data' que tiene los IDs de las ventas en Detalle_Ventas
        self.SALES_ITEM_NUM:int = 0 # contador para crear nombres de items en 'input_sales_data'
        self.DICT_ITEMS_VALUES:dict[str,ListItemValues] = {} # tiene los valores de cada ListItemWidget
        self.VALID_PAID_FIELD:bool = None # True si lineEdit_paid es válido, sino False
        self.TOTAL_COST:float = None # guarda el costo total de 'label_total' como float, para no tener que buscarlo con regex

        #* ======== variables de deudas =======================================
        
        # TODO: mostrar deudas
        # TODO: permitir agregar deuda
        # TODO: permitir eliminar deuda
        # TODO: permitir modificar deuda
        
        self.setup_signals() #! la declaración de señales se hace al final
        return None


    def setup_ui(self) -> None:
        '''
        Método que sirve para simplificar la lectura del método 'self.__init__'.
        Contiene inicializaciones y ajustes de algunos Widgets.
        '''
        self.setWindowTitle("herramienta de gestión - Forrajería Torres")
        set_tables_ListWidgetItemsTooltip(self.ui.tables_ListWidget, getCategoriesDescription())
        self.__hideWidgets() # esconde algunos widgets inicialmente
        self.__initGeneralValidators() # inicializa validadores existentes
        self.__addIconsToWidgets() # añade íconos a los widgets
        # políticas de QTableViews
        setTableViewPolitics(self.ui.tv_inventory_data)
        setTableViewPolitics(self.ui.tv_sales_data)
        setTableViewPolitics(self.ui.tv_debts_data)
        return None    


    def setup_signals(self) -> None:
        '''
        Al igual que el método 'self.setup_ui', este método tiene el objeto 
        de simplificar la lectura del método 'self.__init__'.
        Contiene las declaraciones de señales/slots de Widgets ya existentes 
        desde la instanciación de 'MainWindow'.
        '''
        #¡========= INVENTARIO ================================================
        #* abrir/cerrar side bars
        self.ui.btn_side_barToggle.clicked.connect(lambda: toggleSideBar(
            self.ui.side_bar, self.ui.centralwidget, self.ui.side_bar_body))
        
        self.ui.btn_inventory_sideBarToggle.clicked.connect(lambda: toggleSideBar(
            self.ui.inventory_sideBar, self.ui.main_inventory_frame, self.ui.inventory_side_bar_body, 200))
        
        #* (READ) cargar con productos 'tv_inventory_data'
        self.ui.tables_ListWidget.itemClicked.connect(lambda item: self.fillTableView(
            self.ui.tv_inventory_data,
            ACCESSED_BY_LIST=True,
            SHOW_ALL=True if item.text() == "MOSTRAR TODOS" else False))
        self.ui.tables_ListWidget.itemActivated.connect(lambda item: self.fillTableView(
            self.ui.tv_inventory_data,
            ACCESSED_BY_LIST=True,
            SHOW_ALL=True if item.text() == "MOSTRAR TODOS" else False))

        #* (CREATE) añadir nuevo producto a tabla 'tv_inventory_data'
        self.ui.btn_add_product_inventory.clicked.connect(lambda: self.handleTableCreateRow(self.ui.tv_inventory_data))
        
        # TODO: reimplementar las funciones de DELETE
        #* (DELETE) eliminar un producto de 'tv_inventory_data'
        self.ui.btn_delete_product_inventory.clicked.connect(lambda: self.handleTableDeleteRows(self.ui.tv_inventory_data))
        
        # TODO: reimplementar las funciones de UPDATE
        #* (UPDATE) modificar celdas de 'tv_inventory_data'
        self.inventory_data_model.dataToUpdate.connect(
            lambda params: self.__onInventoryModelDataToUpdate(
                column=params[0], IDproduct=params[1], new_val=params[2]))
        
        self.inventory_delegate.fieldIsValid.connect(self.__onDelegateValidationSucceded)
        self.inventory_delegate.fieldIsInvalid.connect(self.__onDelegateValidationFailed)
        
        #* cambio de selección de 'tv_inventory_data'
        # TODO: reimplementar cambios en las selecciones de los table views
        # self.ui.tv_inventory_data.itemSelectionChanged.connect(lambda: self.handleSelectionChange(self.ui.tv_inventory_data))
        
        #* inventory_sideBar
        self.ui.inventory_checkbuttons_buttonGroup.buttonPressed.connect(self.handlePressedCheckbutton)
        self.ui.inventory_checkbuttons_buttonGroup.buttonClicked.connect(self.handleClickedCheckbutton)
        
        self.ui.checkbox_unit_prices.stateChanged.connect(self.handleCheckboxStateChange)
        
        self.ui.checkbox_comercial_prices.stateChanged.connect(self.handleCheckboxStateChange)
        
        self.ui.lineEdit_percentage_change.editingFinished.connect(self.handleLineeditPercentageEditingFinished)

        #¡========= VENTAS ====================================================
        #* (READ) cargar con ventas 'tv_sales_data'
        self.ui.tab2_toolBox.currentChanged.connect(lambda curr_index: self.fillTableView(
            self.ui.tv_sales_data, SHOW_ALL=True) if curr_index == 1 else None)
        
        
        self.ui.tabWidget.currentChanged.connect(lambda index: self.ui.tab2_toolBox.setCurrentIndex(0) if index == 1 else None)
        
        #* (CREATE) añadir una venta a 'tv_sales_data'
        self.ui.btn_add_product_sales.clicked.connect(lambda: self.handleTableCreateRow(self.ui.tv_sales_data))
        
        #* (DELETE) eliminar ventas de 'tv_sales_data'
        self.ui.btn_delete_product_sales.clicked.connect(lambda: self.handleTableDeleteRows(self.ui.tv_sales_data))
        
        #* (UPDATE) modificar celdas de 'tv_sales_data'
        self.ui.tv_sales_data.doubleClicked.connect(lambda: self.handleTableUpdateItem(self.ui.tv_sales_data, self.ui.tv_sales_data.currentIndex()) )
        # self.ui.tv_sales_data.itemSelectionChanged.connect(lambda: self.handleSelectionChange(self.ui.tv_sales_data))
        
        #* formulario de ventas
        self.ui.btn_add_product.clicked.connect(self.addSalesInputListItem)
        
        self.ui.lineEdit_paid.editingFinished.connect(self.onSalePaidEditingFinished)
        
        self.ui.btn_end_sale.clicked.connect(self.handleFinishedSale)

        #¡========= DEUDAS ====================================================
        # TODO PRINCIPAL: SEGUIR CON PARTE DE DEUDAS
        #* (READ) cargar con deudas 'tv_debts_data'
        self.ui.tabWidget.currentChanged.connect(lambda curr_index: self.fillTableView(
            self.ui.tv_debts_data, SHOW_ALL=True) if curr_index == 2 else None)
        
        return None
    
    
    def __addIconsToWidgets(self) -> None:
        '''
        Simplemente le coloca los íconos que le corresponde a cada Widget. 
        
        Retorna None.
        '''
        icon:QIcon = QIcon()
        
        # botones de side bars
        icon.addFile(":/icons/menu-white.svg")
        self.ui.btn_side_barToggle.setIcon(icon)
        self.ui.btn_inventory_sideBarToggle.setIcon(icon)

        # botones para añadir registros
        icon.addFile(":/icons/plus-white.svg")
        self.ui.btn_add_product_inventory.setIcon(icon)
        self.ui.btn_add_product.setIcon(icon)
        self.ui.btn_add_product_sales.setIcon(icon)
        self.ui.btn_add_debt.setIcon(icon)

        # botones para eliminar registros
        icon.addFile(":/icons/minus-circle-white.svg")
        self.ui.btn_delete_product_inventory.setIcon(icon)
        self.ui.btn_delete_product_sales.setIcon(icon)
        self.ui.btn_delete_debt.setIcon(icon)

        # botón para terminar venta
        icon.addFile(":/icons/check-white.svg")
        self.ui.btn_end_sale.setIcon(icon)
        
        # botones de search bars
        icon.addFile(":/icons/chevron-left-white.svg")
        self.ui.btn_inventory_prev_search_result.setIcon(icon)
        self.ui.btn_sales_prev_search_result.setIcon(icon)
        self.ui.btn_debts_prev_search_result.setIcon(icon)
        
        icon.addFile(":/icons/chevron-right-white.svg")
        self.ui.btn_inventory_next_search_result.setIcon(icon)
        self.ui.btn_sales_next_search_result.setIcon(icon)
        self.ui.btn_debts_next_search_result.setIcon(icon)
        
        return None


    def __hideWidgets(self) -> None:
        '''
        Método simple que esconde los widgets necesarios al iniciar el programa.
        
        Retorna None.
        '''
        # ocultar widgets
        self.ui.side_bar_body.hide()
        self.ui.inventory_side_bar_body.hide()
        self.ui.label_feedbackInventory.hide()
        self.ui.label_feedbackChangePercentage.hide()
        self.ui.label_feedbackSales.hide()
        self.ui.inventory_progressbar.hide()
        self.ui.sales_progressbar.hide()
        self.ui.debts_progressbar.hide()
        return None


    def __initGeneralValidators(self) -> None:
        '''
        Inicializa los validadores predefinidos (de widgets que conforman la GUI base, no creados 
        dinámicamente) y conecta sus señales y slots.
        
        Retorna None.
        '''
        # validadores
        self.inventory_search_bar_validator = SearchBarValidator(self.ui.inventory_searchBar)
        self.sales_search_bar_validator = SearchBarValidator(self.ui.sales_searchBar)
        self.debts_search_bar_validator = SearchBarValidator(self.ui.debts_searchBar)
        self.ui.inventory_searchBar.setValidator(self.inventory_search_bar_validator)
        self.ui.sales_searchBar.setValidator(self.sales_search_bar_validator)
        self.ui.debts_searchBar.setValidator(self.debts_search_bar_validator)
        
        self.total_paid_validator = SalePaidValidator(self.ui.lineEdit_paid, is_optional=True)
        self.ui.lineEdit_paid.setValidator(self.total_paid_validator)

        self.ui.lineEdit_percentage_change.setValidator(
            QIntValidator(-9_999_999, 99_999_999, self.ui.lineEdit_percentage_change))
        
        # señales/slots
        self.total_paid_validator.validationSucceeded.connect(self.onPaidValidationSucceded)
        self.total_paid_validator.validationFailed.connect(self.onPaidValidationFailed)
        
        return None


    #¡ tablas (READ)
    @Slot(QTableView, bool, bool)
    def fillTableView(self, table_view:QTableView, ACCESSED_BY_LIST:bool=False, SHOW_ALL:bool=False) -> None:
        '''
        Este método hace lo siguiente:
        - Limpia las variables de IDs asociadas con el QTableView.
        - Dependiendo del QTableView que se tenga que llenar, declara las consultas SELECT.
        - Instancia e inicializa un QThread y un worker para llenar el modelo de datos asociado 
        al QTableView.

        Parámetros
        ----------
        table_view : QTableView
            El QTableView que se referencia
        ACCESSED_BY_LIST : bool, opcional
            Flag que será True si se seleccionó un item desde 'tables_ListWidget', sino False, por defecto es False
        SHOW_ALL : bool, opcional
            Flag que determina si se muestran todos los elementos del QTableView, por defecto es False

        Retorna
        -------
        None
        '''
        count_sql:str = "" # consulta de tipo COUNT()
        count_params:tuple[Any] = None # params de la consulta COUNT()
        
        data_sql:str = "" # consulta que pide los registros
        data_params:tuple[Any] = None # params de la consulta de registros
        
        # crea las consultas para obtener el COUNT() de filas y los registros para llenar la tabla
        match table_view.objectName():
            case "tv_inventory_data":
                self.IDs_products.clear() # limpia los IDs
                # si se seleccionó una categoría desde 'tables_ListWidget', cambia hacia la pestaña de inventario...
                if ACCESSED_BY_LIST:
                    self.ui.tabWidget.setCurrentWidget(self.ui.tabWidget.findChild(QWidget, "tab1_inventory"))
                count_sql, data_sql = getTableViewsSqlQueries(table_view.objectName(), ACCESSED_BY_LIST, SHOW_ALL)
                
                if not SHOW_ALL and ACCESSED_BY_LIST:
                    count_params = (self.ui.tables_ListWidget.currentItem().text(),)
                    data_params = (self.ui.tables_ListWidget.currentItem().text(),)
                self.ui.label_feedbackInventory.hide()


            case "tv_sales_data":
                self.IDs_saleDetails.clear() # limpia los IDs
                count_sql, data_sql = getTableViewsSqlQueries(table_view.objectName(), ACCESSED_BY_LIST, SHOW_ALL)
                self.ui.label_feedbackSales.hide()


            case "tv_debts_data":
                # TODO: declarar consultas sql para también traer los datos necesarios
                pass
                # getTableViewsSqlQueries()
        
        self.startWorker(table_view, data_sql, data_params, count_sql, count_params)
        return None
    
    
    def startWorker(self, table_view:QTableView, data_sql:str, data_params:tuple=None, count_sql:str=None, 
                    count_params:tuple=None, db_operation:int=DBQueries.SELECT_REGISTERS.value) -> None:
        '''
        Inicializa un QThread y un worker para realizar un tipo de consultas a la base de 
        datos de forma asíncrona, conecta sus señales y slots.

        Parámetros
        ----------
        table_view: QTableView
            QTableView asociado al modelo de datos y QProgressBar que hay que actualizar.
        data_sql: str
            Consulta de tipo CRUD
        data_params: tuple, opcional
            Parámetros de la consulta, por defecto es None
        count_sql: str, opcional
            Consulta de tipo SELECT COUNT() para obtener la cantidad de registros coincidentes
        count_params: tuple, opcional
            Parámetros de la consulta de tipo SELECT COUNT()
        db_operation : int, opcional
            Flag que determina el tipo de operación que lleva a cabo el worker, por defecto es 1 (SELECT)

        Retorna
        -------
        None
        '''
        match db_operation:
            case DBQueries.SELECT_REGISTERS.value:
                self.select_thread = QThread()
                self.select_worker = WorkerSelect()
                self.select_worker.moveToThread(self.select_thread)
                
                self.select_thread.started.connect(
                    lambda: self.select_worker.executeReadQuery(
                        data_sql=data_sql, data_params=data_params,
                        count_sql=count_sql, count_params=count_params)
                    )
                self.select_worker.countFinished.connect(
                    lambda model_shape: self.__workerOnCountFinished(
                        tv_name=table_view.objectName(), model_shape=model_shape)
                    )
                self.select_worker.registerProgress.connect(
                    lambda register: self.__workerOnRegisterProgress(
                        register=register,table_view=table_view)
                    )
                self.select_worker.finished.connect(
                    lambda: self.__workerOnFinished(
                        tv_name=table_view.objectName())
                    )
                self.select_worker.finished.connect(self.select_thread.quit)
                self.select_worker.finished.connect(self.select_worker.deleteLater)
                
                self.select_thread.start()
            
            case DBQueries.DELETE_REGISTERS.value:
                pass
            
            case DBQueries.UPDATE_REGISTERS.value:
                pass
            
            case _:
                pass
        
        return None
    
    
    @Slot()
    def __workerOnCountFinished(self, tv_name:str, model_shape:tuple[int, int]=None) -> None:
        '''
        Instancia un acumulador numpy.array para los datos del modelo, y actualiza el estado 
        del QProgressBar asociado al QTableView.

        Parámetros
        ----------
        tv_name : str
            Nombre del QTableView que se referencia
        model_shape: tuple[int, int]
            Dimensiones del modelo de datos, se usa para instanciar el acumulador

        Retorna
        -------
        None
        '''
        self._inv_model_data_acc = empty(shape=model_shape, dtype=object)
        
        self.__updateProgressBar(tv_name=tv_name, max_val=model_shape[0])
    
    
    @Slot(tuple, QTableView)
    def __workerOnRegisterProgress(self, register:tuple[Any], table_view:QTableView) -> None:
        '''
        A medida que se progresa con los registros leídos guarda los IDs necesarios de cada registro, 
        acumula los registros en una variable y actualiza la QProgressBar asociada a ese QTableView.

        Parámetros
        ----------
        register : tuple[Any]
            El registro obtenido de la consulta SELECT
        table_view : QTableView
            QTableView al que se referencia
        
        Retorna
        -------
        None
        '''
        self.__saveTableViewIDs(
            tv_name=table_view.objectName(), register_id=register[1][0]
            )
        self.__updateProgressBar(
            tv_name=table_view.objectName(),max_val=None, value=register[0]
            )

        # guarda en la posición actual (register[0] marca el progreso de 
        # lectura) el registro completo
        self._inv_model_data_acc[register[0]] = register[1]
        
        return None
    
    
    def __updateProgressBar(self, tv_name:str, max_val:int=None, value:int=None) -> None:
        '''
        Actualiza el estado del QProgressBar correspondiente dependiendo del QTableView asociado.

        Parámetros
        ----------
        tv_name : str
            Nombre del QTableView al cual está asociado el QProgressBar a actualizar
        max_val : int, opcional
            Valor máximo del QProgressBar, por defecto es None
        value : int, opcional
            Valor actual del QProgressBar, por defecto es None

        Retorna
        -------
        None
        '''
        match tv_name:
            case "tv_inventory_data":
                self.ui.inventory_progressbar.show() if self.ui.inventory_progressbar.isHidden() else None
                self.ui.inventory_progressbar.setMaximum(max_val) if max_val is not None and self.ui.inventory_progressbar.maximum() != max_val else None
                self.ui.inventory_progressbar.setValue(value + 1) if value else None
            
            case "tv_sales_data":
                self.ui.sales_progressbar.show() if self.ui.sales_progressbar.isHidden() else None
                self.ui.sales_progressbar.setMaximum(max_val) if max_val is not None and self.ui.sales_progressbar.maximum() != max_val else None
                self.ui.sales_progressbar.setValue(value + 1) if value else None
                
            case "tv_debts_data":
                self.ui.debts_progressbar.show() if self.ui.debts_progressbar.isHidden() else None
                self.ui.debts_progressbar.setMaximum(max_val) if max_val is not None and self.ui.debts_progressbar.maximum() != max_val else None
                self.ui.debts_progressbar.setValue(value + 1) if value else None
        return None
    
    
    def __saveTableViewIDs(self, tv_name:str, register_id:int) -> None:
        '''
        A medida que el WORKER encuentra registros guarda los IDs de los registros coincidentes en 
        una variable asociada a cada QTableView.
        
        Parámetros
        ----------
        tv_name: str
            Nombre del QTableView al que referencia
        register_id: int
            ID del registro actual para guardar en una variable
        
        Retorna None.
        '''
        match tv_name:
            case "tv_inventory_data":
                self.IDs_products.append(register_id)
                
            case "tv_sales_data":
                self.IDs_saleDetails.append(register_id)
            
            case "tv_debts_data":
                pass
        return None
    

    @Slot(str)
    def __workerOnFinished(self, tv_name:str, READ_OPERATION:bool=True) -> None:
        '''
        Esconde la QProgressBar relacionada con el QTableView, reinicia el valor del 
        QSS de dicha QProgressBar y carga los datos en el QTableView. Si 'READ_OPERATION' 
        es False es porque se realizaron otras consultas a la base de datos (DELETE / INSERT) 
        y el QTableView debe ser recargado.
        
        Parámetros
        ----------
            tv_name: nombre del QTableView al que se referencia
            READ_OPERATION: flag que determina si la operación que se hizo fue de llenado (READ) a un 
            QTableView, por defecto es True

        Retorna
        -------
        None
        '''
        match tv_name:
            case "tv_inventory_data":
                self.ui.inventory_progressbar.setStyleSheet("")
                self.ui.inventory_progressbar.hide()
                if not READ_OPERATION:
                    # recarga la tabla
                    try:
                        self.fillTableView(table_view=self.ui.tv_inventory_data, SHOW_ALL=True)
                    except AttributeError: # salta porque se intenta recargar la tabla pero nunca se llenó anteriormente
                        pass
                else:
                    pass
                self.inventory_data_model.setModelData(
                    data=self._inv_model_data_acc,
                    headers=ModelHeaders.INVENTORY_HEADERS.value)

                
            case "tv_sales_data":
                self.ui.sales_progressbar.setStyleSheet("")
                self.ui.sales_progressbar.hide()
                if not READ_OPERATION:
                    # recarga la tabla
                    self.fillTableView(table_view=self.ui.tv_sales_data, SHOW_ALL=True)
                else:
                    pass
                    # self.ui.tv_sales_data.resizeRowsToContents()
                
            case "tv_debts_data":
                self.ui.debts_progressbar.setStyleSheet("")
                self.ui.debts_progressbar.hide()
                if not READ_OPERATION:
                    # recarga la tabla
                    self.fillTableView(table_view=self.ui.tv_debts_data, SHOW_ALL=True)
                else:
                    pass
                    # self.ui.tv_debts_data.resizeRowsToContents()
            
        logging.debug(LoggingMessage.WORKER_SUCCESS)
        return None



    #¡ tablas (CREATE)
    @Slot(str)
    def handleTableCreateRow(self, table_view:QTableView) -> None:
        '''
        Dependiendo del QTableView al que se agregue una fila, se encarga de crear una instancia del QDialog 
        correspondiente que pide los datos necesarios para la nueva fila.
        
        Al final, recarga la tabla correspondiente llamando a 'self.fillTableView'.
        
        Retorna None.
        '''
        match table_view.objectName():
            case "tv_inventory_data":
                productDialog = ProductDialog() # QDialog para añadir un producto nuevo a 'tv_inventory_data'
                productDialog.setAttribute(Qt.WA_DeleteOnClose, True) # destruye el dialog cuando se cierra
                productDialog.exec()

            case "tv_sales_data":
                saleDialog = SaleDialog() # QDialog para añadir una venta nueva a 'tv_sales_data' (y posiblemente, una
                                          # deuda a 'tv_debts_data')
                saleDialog.setAttribute(Qt.WA_DeleteOnClose, True)
                saleDialog.exec()
        
        return None



    #¡ tablas (DELETE)
    def __getTableElementsToDelete(self, table_view:QTableView, selected_rows:list) -> tuple | None:
        '''
        Dependiendo de cuál sea 'table_view', obtiene los nombres de los productos de 'tv_inventory_data' ó la fecha 
        y hora de 'tv_sales_data'. 
        
        - table_view: QTableView al que se referencia.
        - selected_rows: lista con las filas seleccionadas del 'table_view'.
        
        Retorna una tupla con los registros a eliminar, o None si no hay elementos seleccionados.
        '''
        if not selected_rows:
            return None
        
        registers_to_delete:list = [None]*len(selected_rows)
        
        match table_view.objectName():
            # obtiene los nombres de los productos a borrar
            case "tv_inventory_data":
                for pos,row in enumerate(selected_rows):
                    registers_to_delete[pos] = table_view.item(row, 1).text()
            
            # obtiene la fecha y hora de las ventas a borrar
            case "tv_sales_data":
                for pos,row in enumerate(selected_rows):
                    registers_to_delete[pos] = table_view.item(row, 5).text()
            
        return tuple(registers_to_delete)


    @Slot(QTableView)
    def handleTableDeleteRows(self, table_view:QTableView) -> None:
        '''
        NOTA: Este método NO ELIMINA LOS REGISTROS DE "Productos" NI "Deudas", LOS MARCA COMO "ELIMINADOS" EN LA 
        BASE DE DATOS. EN CAMBIO SÍ ELIMINA LOS REGISTROS DE "Ventas" Y "Detalle_Ventas".
        
        Este método hace lo siguiente:
        - Dependiendo del 'table_view' del que se tengan que borrar registros, se encarga de declarar las 
        consultas sql y los parámetros necesarios para luego hacer las consultas UPDATE que marcan como "eliminado" 
        los registros en la clase 'workerclasses.WorkerDelete'.
        - Cambia el QSS del QProgressBar asociado a 'table_view'.
        - Especifica el valor máximo del QProgressBar asociado a 'table_view'.
        - Crea una instancia de WORKER y QThread y conecta sus señales/slots.
        
        Este método llama a:
        - functionutils.getSelectedTableRows: para obtener las filas seleccionas del 'table_view'.
        - self.__getTableElementsToDelete: para obtener datos sobre los registros a marcar como eliminados.
        - self.__updateProgressBar: para especificar el valor máximo de la QProgressBar asociada a 'table_view'.
        
        Retorna None.
        '''
        selected_rows:tuple # las posiciones de self.IDs_products/self.IDs_saleDetails donde están los registros seleccionados
        ids_to_delete:list # los IDs de los registros a eliminar (necesario para consulta)
        productnames_to_delete:list|None # los nombres de los registros a eliminar de "Productos"
        dateTime_to_delete:list|None # las fechas y horas de los registros a eliminar de "Ventas" y "Detalle_Ventas"

        mark_sql:str = None # consulta UPDATE para marcar "eliminado" los registros (Productos y Deudas)
        mult_sql:tuple[str] = None # se usa para borrar de Detalle_Ventas y Ventas.
        params:list[tuple] = None # lista[(id, nombre)] si es Productos; ó lista[(id,fecha_hora)] si es Detalle_Ventas
        
        selected_rows = getSelectedTableRows(table_view)
        
        if not selected_rows:
            return None
        
        
        match table_view.objectName():
            case "tv_inventory_data":
                productnames_to_delete = self.__getTableElementsToDelete(table_view, selected_rows)
                
                # a partir de las filas seleccionadas, obtiene de self.IDs_products los ids para la consulta
                ids_to_delete = [self.IDs_products[n_id] for n_id in selected_rows]
                
                mark_sql = "UPDATE Productos SET eliminado = 1 WHERE IDproducto = ? AND nombre = ?;"
                
                # une 'ids_to_delete' y 'productnames_to_delete' en una lista[(id, nombre)]
                params = [(id, name) for id,name in zip(ids_to_delete, productnames_to_delete)]
                
                self.ui.inventory_progressbar.setMaximum(len(params))
                self.ui.inventory_progressbar.setStyleSheet("QProgressBar::chunk {background-color: qlineargradient(spread:reflect, x1:0.119, y1:0.426, x2:0.712045, y2:0.926, stop:0.0451977 rgba(255, 84, 87, 255), stop:0.59887 rgba(255, 161, 71, 255));}")
            
            
            case "tv_sales_data":
                dateTime_to_delete = self.__getTableElementsToDelete(table_view, selected_rows)
                
                # obtiene ids de las filas seleccionadas
                ids_to_delete = [self.IDs_saleDetails[n_id] for n_id in selected_rows]
                
                mult_sql:tuple[str] = (
                    "DELETE FROM Ventas WHERE IDventa = (SELECT IDventa FROM Detalle_Ventas WHERE ID_detalle_venta = ?) AND fecha_hora = ?;",
                    "DELETE FROM Detalle_Ventas WHERE ID_detalle_venta = ?;",
                    )
                
                # une 'ids_to_delete' y 'dateTime_to_delete' en una lista[(id, fecha_y_hora)]
                params = [(id, datetime) for id,datetime in zip(ids_to_delete, dateTime_to_delete)]
                
                self.ui.sales_progressbar.setMaximum(len(params))
                self.ui.sales_progressbar.setStyleSheet("QProgressBar::chunk {background-color: qlineargradient(spread:reflect, x1:0.119, y1:0.426, x2:0.712045, y2:0.926, stop:0.0451977 rgba(255, 84, 87, 255), stop:0.59887 rgba(255, 161, 71, 255));}")


            case "tv_debts_data":
                pass
        
        #? inicializa WORKER y THREAD, y conecta señales/slots
        self.DELETE_THREAD = QThread()
        # si mark_sql != None es porque se deben MARCAR "eliminados" los registros, sino se deben ELIMINAR        
        if mark_sql:
            self.update_worker = WorkerUpdate()
            self.update_worker.moveToThread(self.DELETE_THREAD)
            self.DELETE_THREAD.started.connect(lambda: self.update_worker.executeUpdateQuery(
                sql=mark_sql,
                params=params))
            self.update_worker.progress.connect(lambda value: self.__updateProgressBar(
                tv_name=table_view.objectName(),
                value=value))
            self.update_worker.finished.connect(lambda: self.__workerOnFinished(
                tv_name=table_view.objectName(),
                READ_OPERATION=False) )
            self.update_worker.finished.connect(self.DELETE_THREAD.quit)
            self.DELETE_THREAD.finished.connect(self.update_worker.deleteLater)
            
        # sino, se deben borrar completamente (no marcar como "eliminados")
        else:
            self.delete_worker = WorkerDelete()
            self.delete_worker.moveToThread(self.DELETE_THREAD)
            self.DELETE_THREAD.started.connect(lambda: self.delete_worker.executeDeleteQuery(
                params=params,
                mult_sql=mult_sql))
            self.delete_worker.progress.connect(lambda value: self.__updateProgressBar(
                tv_name=table_view.objectName(),
                value=value))
            self.delete_worker.finished.connect(lambda: self.__workerOnFinished(
                tv_name=table_view.objectName(),
                READ_OPERATION=False) )
            self.delete_worker.finished.connect(self.DELETE_THREAD.quit)
            self.DELETE_THREAD.finished.connect(self.delete_worker.deleteLater)
            
        self.DELETE_THREAD.start()
        return None


    #¡ tablas (UPDATE)
    @Slot(int, int, object)
    def __onInventoryModelDataToUpdate(self, column:int, IDproduct:int, 
                                       new_val:Any | list[str]) -> None:
        '''
        Actualiza la base de datos con el valor nuevo de Productos.
        
        Parámetros
        ----------
        column : int
            Columna del item modificado
        IDproduct : int
            IDproducto en la base de datos del item modificado
        new_val : Any | list[str]
            Valor nuevo del item, sólo será list[str] cuando la columna 
            modificada en el modelo sea la de stock (3), en ese caso 
            new_val será una lista[stock, unidad de medida]
        
        Retorna
        -------
        None
        '''
        upd_sql:str
        upd_params:tuple = None
        prev_val:float = None # cuando se actualiza precio normal o precio comercial, se debe 
                              # actualizar el valor también en Deudas, así que antes obtiene el 
                              # valor anterior para calcular el porcentaje de cambio.
        
        match column:
            case 0: # categoría
                upd_sql='''UPDATE Productos 
                        SET IDcategoria = (
                            SELECT IDcategoria FROM Categorias 
                            WHERE nombre_categoria = ?) 
                        WHERE IDproducto = ?;'''
                upd_params=(new_val, IDproduct,)
            
            case 1: # nombre del producto
                upd_sql='''UPDATE Productos 
                        SET nombre = ? 
                        WHERE IDproducto = ?;'''
                upd_params=(new_val, IDproduct,)
            
            case 2: # descripción
                upd_sql='''UPDATE Productos 
                        SET descripcion = ? 
                        WHERE IDproducto = ?;'''
                upd_params=(new_val, IDproduct,)
            
            case 3: # stock
                upd_sql='''UPDATE Productos 
                        SET stock = ?, unidad_medida = ? 
                        WHERE IDproducto = ?;'''
                upd_params=(new_val[0], new_val[1], IDproduct,)
            
            case 4: # precio normal
                # TODO: corregir, cuando el usuario pagó algo de un producto y luego se modifica el 
                # todo: costo del producto a 0, y luego se vuelve a un valor diferente a 0, se debe 
                # todo: tomar en cuenta lo que el usuario pagó por ese producto anteriormente y DESCONTARLO.
                # obtiene el valor anterior del producto
                with self._db_repo as db_repo:
                    prev_val = db_repo.selectRegisters(
                        data_sql='''SELECT precio_unit 
                                    FROM Productos 
                                    WHERE IDproducto = ?;''',
                        data_params=(IDproduct,)
                        )[0][0]
                
                # no tiene sentido hacer consultas a base de datos si
                # no se modificaron los precios
                if float(prev_val) == float(new_val):
                    return None
                
                # actualiza en Productos
                upd_sql='''UPDATE Productos 
                        SET precio_unit = ? 
                        WHERE IDproducto = ?;'''
                upd_params=(float(new_val), IDproduct,)
                
                self.__updateDebtsOnPriceChange(
                    float(new_val), prev_val, IDproduct, InventoryPriceType.NORMAL
                    )
            
            case 5: # precio comercial
                # TODO: corregir, cuando el usuario pagó algo de un producto y luego se modifica el 
                # todo: costo del producto a 0, y luego se vuelve a un valor diferente a 0, se debe 
                # todo: tomar en cuenta lo que el usuario pagó por ese producto anteriormente y DESCONTARLO.
                # obtiene el valor anterior del producto
                with self._db_repo as db_repo:
                    prev_val = db_repo.selectRegisters(
                        data_sql='''SELECT precio_comerc 
                                    FROM Productos 
                                    WHERE IDproducto = ?;''',
                        data_params=(IDproduct,)
                        )[0][0]
                
                # no tiene sentido hacer consultas a base de datos si
                # no se modificaron los precios
                if float(prev_val) == float(new_val):
                    return None
                
                # actualiza en Productos
                upd_sql='''UPDATE Productos 
                           SET precio_comerc = ? 
                           WHERE IDproducto = ?;'''
                upd_params=(float(new_val), IDproduct,)
                
                self.__updateDebtsOnPriceChange(
                    float(new_val), prev_val, IDproduct, InventoryPriceType.COMERCIAL
                )
                
        with self._db_repo as db_repo:
            db_repo.updateRegisters(upd_sql=upd_sql, upd_params=upd_params)
        
        return None

    
    def __updateDebtsOnPriceChange(self, new_val:float, prev_val:str, IDproduct:int, 
                                   price_type:InventoryPriceType) -> None:
        '''
        Actualiza el precio normal / precio comercial de un producto en Deudas 
        cuando se actualiza en la tabla Productos.

        Parámetros
        ----------
        new_val: str
            El nuevo precio del producto
        prev_val: str
            El precio anterior del producto en base de datos
        IDproduct: int
            ID del producto cuyo precio fue modificado
        price_type: InventoryPriceType
            El tipo de precio a cambiar en base de datos
        
        Retorna
        -------
        None
        '''
        upd_sql:str
        upd_params:tuple
        
        match price_type.name:
            case "NORMAL":
                upd_sql = '''UPDATE Deudas 
                            SET total_adeudado = CASE Detalle_Ventas.abonado 
                                WHEN 0 THEN ? -- si no pagó el valor nuevo es "new_val"
                                ELSE ROUND(? - Detalle_Ventas.abonado, 2) -- si pagó algo hago: "new_val" - Detalle_Ventas.abonado
                            END 
                            FROM Detalle_Ventas, Ventas 
                            WHERE 
                                Deudas.IDdeuda = Detalle_Ventas.IDdeuda AND 
                                Detalle_Ventas.IDproducto = ? AND 
                                Detalle_Ventas.IDventa = Ventas.IDventa AND 
                                Ventas.detalles_venta LIKE '%(P. NORMAL)%';'''
                upd_params = (new_val, new_val, IDproduct,)
        
            case "COMERCIAL":
                upd_sql = '''UPDATE Deudas 
                            SET total_adeudado = CASE Detalle_Ventas.abonado 
                                WHEN 0 THEN ? 
                                ELSE ROUND(? - Detalle_Ventas.abonado, 2)
                            END 
                            FROM Detalle_Ventas, Ventas 
                            WHERE 
                                Deudas.IDdeuda = Detalle_Ventas.IDdeuda AND 
                                Detalle_Ventas.IDproducto = ? AND 
                                Detalle_Ventas.IDventa = Ventas.IDventa AND 
                                Ventas.detalles_venta LIKE '%(P. COMERCIAL)%';'''
                upd_params = (new_val, new_val, IDproduct,)
        
        # actualiza total_adeudado en Deudas
        with self._db_repo as db_repo:
            db_repo.updateRegisters(
                upd_sql=upd_sql,
                upd_params=upd_params
                )
        return None
    
    
    def __tableComboBoxOnCurrentTextChanged(self, table_view:QTableView, curr_index:QModelIndex, 
                                            combobox:QComboBox) -> None:
        '''
        Declara la consulta sql y los parámetros y luego hace la consulta UPDATE a la base de datos con el nuevo 
        dato seleccionado a partir del nuevo texto de 'combobox'. Reemplaza el valor anterior de la celda por el
        nuevo. Al finalizar, elimina todos los QComboBox de 'table_view'.
        
        PARAMS:
        - table_view: QTableView al que se referencia.
        - curr_index: representa las coordenadas del item en 'table_view'.
        - combobox: representa al QComboBox afectado.
        
        Retorna None.
        '''
        new_unit:str | None # y el valor de la unidad ya seleccionado.
        quantity:float | int # cantidad seleccionada.

        match table_view.objectName():
            # case "tv_inventory_data":
            #     self._db_repo.updateRegisters(
            #         upd_sql="UPDATE Productos SET IDcategoria = (SELECT IDcategoria FROM Categorias WHERE nombre_categoria = ?) WHERE IDproducto = ?;",
            #         upd_params=(combobox.currentText(), str(self.IDs_products[curr_index.row()]),) )
            #     table_view.item(curr_index.row(), curr_index.column()).setText(combobox.currentText())


            case "tv_sales_data":
                # actualiza el producto en Detalle_Ventas
                self._db_repo.updateRegisters(
                    upd_sql="UPDATE Detalle_Ventas SET IDproducto = (SELECT IDproducto FROM Productos WHERE nombre = ?) WHERE ID_detalle_venta = ?;",
                    upd_params=(combobox.currentText(), str(self.IDs_saleDetails[curr_index.row()]),) )
                table_view.item(curr_index.row(), curr_index.column()).setText(f"{combobox.currentText()}")

                # obtengo la cantidad de la columna "cantidad" para luego unirlo a la unidad de medida
                quantity = table_view.item(curr_index.row(), 1).text().split(" ")[0].strip()

                # obtengo la unidad de medida del producto actual para colocarlo en la columna "cantidad"
                new_unit = self._db_repo.selectRegisters(data_sql="SELECT unidad_medida FROM Productos WHERE nombre = ?;",
                                         data_params=(combobox.currentText(),) )[0][0]
                table_view.item(curr_index.row(), 1).setText(f"{quantity} {new_unit}")

        combobox.deleteLater()
        # remueve los widgets de las celdas (para que se puedan modificar sólo una vez al mismo tiempo las comboboxes)
        removeTableCellsWidgets(table_view)
        # vuelve a activar el ordenamiento de la tabla
        # table_view.setSortingEnabled(True)
        return None


    @Slot(QTableView, QModelIndex, QLineEdit, str)
    def __tableLineEditOnReturnPressed(self, table_view:QTableView, curr_index:QModelIndex, lineedit:QLineEdit, prev_text:str) -> None:
        '''
        Este método es llamado desde la señal 'self.lineedit.returnPressed' y sólo se ejecutará cuando el input 
        sea válido ('validador.State.Acceptable').
        
        Declara la consulta sql y los parámetros y luego hace la consulta UPDATE a la base de datos con el nuevo 
        dato ingresado a partir del nuevo texto introducido en 'lineedit'. Luego sustituye el valor actual de 
        la celda por el nuevo.
        Al finalizar, remueve 'lineedit' de la celda de 'table_view'.
        
        Este método llama a:
        - self._db_repo.updateRegisters: para realizar las consultas UPDATE.
        - removeTableCellsWidgets: para quitar los QLineEdit de 'table_view'.
        
        PARAMS:
        - table_view: el QTableView al que se referencia.
        - curr_index: índice de la celda seleccionada de 'table_view'.
        - lineedit: el QLineEdit que envía la señal.
        - prev_text: el texto que había antes en la celda.
        
        Retorna None.
        '''
        full_stock:list[str] # var. aux. con el texto completo del stock
        percentage_diff:float # el porcentaje de diferencia entre el valor viejo y el nuevo, se usa junto a new_total_debt...
        new_debt_term:float # para calcular el nuevo valor en Deudas.total_adeudado. new_debt_term es el segundo término de la 
                             # expresión "total_adeudado * (1 + percentage_diff / 100)", siendo "(1 + percentage_diff / 100)".
        
        pattern:Pattern # patrón para buscar (P.NORMAL)|(P.COMERCIAL) en lineedit.text()
        price_type:Match # var. aux. con substring (P.NORMAL)|(P.COMERCIAL) obtenido de 'prev_text'
        lineedit_text:str # var. aux. placeholder para formatear texto de celdas


        match table_view.objectName():
            # case "tv_inventory_data":
                # match curr_index.column():
                #     pass
                    # case 1: # nombre
                    #     self._db_repo.updateRegisters(
                    #         upd_sql="UPDATE Productos SET nombre = ? WHERE IDproducto = ?;",
                    #         upd_params=( lineedit.text(), str(self.IDs_products[curr_index.row()]), ))
                    #     # reemplaza el valor anterior con el nuevo
                    #     table_view.item(curr_index.row(), curr_index.column()).setText(lineedit.text().strip())
                    
                    # case 2: # descripción
                    #     self._db_repo.updateRegisters(upd_sql="UPDATE Productos SET descripcion = ? WHERE IDproducto = ?;",
                    #                     upd_params=( lineedit.text(), str(self.IDs_products[curr_index.row()]), ))
                    #     # reemplaza el valor anterior con el nuevo
                    #     table_view.item(curr_index.row(), curr_index.column()).setText(lineedit.text().strip())
                    
                    # case 3: # stock
                    #     # obtiene la cantidad de stock y la unidad de medida (si tiene)
                    #     full_stock = lineedit.text().replace(",",".").split(" ") # pos. 0 tiene cantidad de stock y pos. 1 tiene unidad de medida
                    #     full_stock.append("") if len(full_stock) == 1 else None
                        
                    #     self._db_repo.updateRegisters(
                    #         upd_sql="UPDATE Productos SET stock = ?, unidad_medida = ? WHERE IDproducto = ?;",
                    #         upd_params=(full_stock[0], full_stock[1], str(self.IDs_products[curr_index.row()]), ))
                    #     # reemplaza el valor anterior con el nuevo
                    #     full_stock[0] = full_stock[0].replace(".",",")
                    #     table_view.item(curr_index.row(), curr_index.column()).setText(f"{full_stock[0]} {full_stock[1].strip()}")
                    
                    # case 4: # si es precio unitario, modifica también en Deudas precios normales
                    #     # actualiza en Productos
                    #     self._db_repo.updateRegisters(
                    #         upd_sql="UPDATE Productos SET precio_unit = ? WHERE IDproducto = ?;",
                    #         upd_params=(lineedit.text().replace(",","."), str(self.IDs_products[curr_index.row()]), ))
                        
                    #     # obtiene la expresión para calcular en Deudas el nuevo total_adeudado
                    #     prev_text = prev_text.replace(",",".")
                    #     try:
                    #         percentage_diff = (float(lineedit.text().replace(",",".")) - float(prev_text)) * 100 / float(prev_text)
                            
                    #     except ZeroDivisionError: # en caso de fallar porque el valor anterior es 0, hago que sea 0.00001
                    #         percentage_diff = (float(lineedit.text().replace(",",".")) - float(prev_text)) * 100 / (float(prev_text) + 0.00001)
                            
                    #     new_debt_term = 1 + percentage_diff / 100
                    #     sql = "UPDATE Deudas SET total_adeudado = ROUND(total_adeudado * ?, 2) WHERE IDdeuda IN (SELECT Detalle_Ventas.IDdeuda FROM Detalle_Ventas JOIN Ventas ON Detalle_Ventas.IDventa = Ventas.IDventa WHERE Detalle_Ventas.IDproducto = (SELECT IDproducto FROM Productos WHERE nombre = ?) AND Ventas.detalles_venta LIKE '%(P. NORMAL)%');"
                        
                    #     # actualiza total_adeudado en Deudas en precios normales
                    #     self._db_repo.updateRegisters(
                    #         upd_sql=sql,
                    #         upd_params=(new_debt_term, table_view.item(curr_index.row(), 1).text(),) )
                    #     # reemplaza el valor anterior con el nuevo
                    #     lineedit_text = lineedit.text().replace(".",",")
                    #     table_view.item(curr_index.row(), curr_index.column()).setText(lineedit_text.strip())
                        
                    # case 5: # si es precio comercial, modifica en Deudas precios comerciales
                    #     lineedit_text = lineedit.text().replace(",",".") if lineedit.text() else 0.0
                            
                    #     # actualiza en Productos
                    #     self._db_repo.updateRegisters(
                    #         upd_sql="UPDATE Productos SET precio_comerc = ? WHERE IDproducto = ?;",
                    #         upd_params=(str(lineedit_text), str(self.IDs_products[curr_index.row()]), ))
                        
                    #     prev_text = prev_text.replace(",",".") if prev_text else 0.0
                    #     try:
                    #         percentage_diff = (float(lineedit_text) - float(prev_text)) * 100 / float(prev_text)
                        
                    #     except ZeroDivisionError: # en caso de fallar porque el valor anterior es 0, hago que sea 0.00001
                    #         percentage_diff = (float(lineedit_text) - float(prev_text)) * 100 / (float(prev_text) + 0.00001)
                        
                    #     new_debt_term = 1 + percentage_diff / 100
                    #     sql = sql = "UPDATE Deudas SET total_adeudado = ROUND(total_adeudado * ?, 2) WHERE IDdeuda IN (SELECT Detalle_Ventas.IDdeuda FROM Detalle_Ventas JOIN Ventas ON Detalle_Ventas.IDventa = Ventas.IDventa WHERE Detalle_Ventas.IDproducto = (SELECT IDproducto FROM Productos WHERE nombre = ?) AND Ventas.detalles_venta LIKE '%(P. COMERCIAL)%');"
                        
                    #     # actualiza total_adeudado en Deudas en precios comerciales
                    #     self._db_repo.updateRegisters(
                    #         upd_sql=sql,
                    #         upd_params=(new_debt_term, table_view.item(curr_index.row(), 1).text(),) )
                        
                    #     # reemplaza el valor anterior con el nuevo
                    #     lineedit_text = lineedit.text().replace(".",",")
                    #     table_view.item(curr_index.row(), curr_index.column()).setText(lineedit_text.strip())


            case "tv_sales_data":
                match curr_index.column():
                    case 0: # detalle de venta
                        pattern = compile("(\([\s]*P[\s]*\.[\s]*NORMAL[\s]*\)|\([\s]*P[\s]*\.[\s]*COMERCIAL[\s]*\))$", IGNORECASE)
                        
                        # verifica si (P. NORMAL) | (P. COMERCIAL) está, sino lo toma de prev_text y lo coloca al final
                        if not search(pattern, lineedit.text()):
                            # obtiene (P. NORMAL) | (P. COMERCIAL) de prev_text
                            price_type = search(pattern, prev_text)
                            # lo pone en mayúsculas
                            price_type = str(price_type.group()).upper()
                            
                            lineedit_text = f"{lineedit.text()} {price_type}"
                        # si SÍ ESTÁ lo reemplaza...
                        else:
                            price_type = search(pattern, lineedit.text())
                            price_type = str(price_type.group()).upper().replace(" ", "")
                            lineedit_text = sub(pattern, price_type, lineedit.text())
                        
                        self._db_repo.updateRegisters(
                            upd_sql="UPDATE Ventas SET detalles_venta = ? WHERE IDventa = (SELECT IDventa FROM Detalle_Ventas WHERE ID_detalle_venta = ?);",
                            upd_params=(lineedit_text, str(self.IDs_saleDetails[curr_index.row()]), ))
                        table_view.item(curr_index.row(), curr_index.column()).setText(f"{lineedit_text}")
                    
                    case 1: # cantidad
                        self._db_repo.updateRegisters(
                            upd_sql="UPDATE Detalle_Ventas SET cantidad = ? WHERE ID_detalle_venta = ?;",
                            upd_params=(lineedit.text().replace(",","."), str(self.IDs_saleDetails[curr_index.row()]), ))
                        # toma la unidad de medida (si tiene) y la concatena con la nueva cantidad
                        new_prev_text = prev_text.split(" ")[1] if len(prev_text.split(" ")) > 1 else ""
                        lineedit_text = lineedit.text().replace(".",",")
                        table_view.item(curr_index.row(), curr_index.column()).setText(f"{lineedit_text} {new_prev_text}")
                    
                    case 3: # costo total
                        self._db_repo.updateRegisters(
                            upd_sql="UPDATE Detalle_Ventas SET costo_total = ? WHERE ID_detalle_venta = ?;",
                            upd_params=(lineedit.text().replace(",","."), str(self.IDs_saleDetails[curr_index.row()]), ))
                        lineedit_text = lineedit.text().replace(".",",")
                        table_view.item(curr_index.row(), curr_index.column()).setText(f"{lineedit_text.strip()}")
                    
                    case 4: # abonado
                        self._db_repo.updateRegisters(
                            upd_sql="UPDATE Detalle_Ventas SET abonado = ? WHERE ID_detalle_venta = ?;",
                            upd_params=(lineedit.text().replace(",","."), str(self.IDs_saleDetails[curr_index.row()]), ))
                        lineedit_text = lineedit.text().replace(".",",")
                        table_view.item(curr_index.row(), curr_index.column()).setText(f"{lineedit_text.strip()}")
        
        # borra el lineedit
        if table_view.cellWidget(curr_index.row(), curr_index.column()): #! veo si existe porque, por alguna razón, al
            lineedit.deleteLater()                                         #! lineedit en 'tv_sales_data' no lo encuentra.
        # remueve todos los widgets                                        #! Igualmente 'removeTableCellWidgets' le da 
        removeTableCellsWidgets(table_view)                              #! permiso al 'garbage collector' de borrarlos...
        
        # vuelvo a activar el ordenamiento de la tabla
        # table_view.setSortingEnabled(True)
        return None


    @Slot(QTableView, QModelIndex, QDateTimeEdit)
    def __tableDateTimeOnEditingFinished(self, table_view:QTableView, curr_index:QModelIndex, datetimeedit:QDateTimeEdit) -> None:
        '''
        Este método es llamado desde la señal 'self.datetimeedit.editingFinished'.
        
        Declara la consulta UPDATE y sus parámetros y luego hace la consulta a la base de datos para actualizar 
        el valor de 'datetimeedit', luego sustituye el valor actual de la celda por el nuevo.
        Al finalizar, remueve 'datetimeedit' de la celda de 'table_view'.
        
        Este método llama a:
        - self._db_repo.updateRegisters: para realizar las consultas UPDATE.
        - removeTableCellsWidgets: para quitar los QDateTimeEdit de 'table_view'.
        
        PARAMS:
        - table_view: el QTableView al que se referencia.
        - curr_index: índice de la celda seleccionada de 'table_view'.
        - datetimeedit: el QDateTimeEdit que envía la señal.
        
        Retorna None.
        '''
        match table_view.objectName():
            case "tv_sales_data":
                self._db_repo.updateRegisters(
                    upd_sql="UPDATE Ventas SET fecha_hora = ? WHERE IDventa = (SELECT IDventa FROM Detalle_Ventas WHERE ID_detalle_venta = ?);",
                    upd_params=(datetimeedit.text(), self.IDs_saleDetails[curr_index.row()], ))
                table_view.item(curr_index.row(), curr_index.column()).setText(f"{str(datetimeedit.text()).strip()}")
            
            case _:
                pass
        
        #? verifico si el calendar tiene el foco puesto porque cuando se muestra el popup cambia el foco y envía 
        #? la señal 'editingFinished' a éste método, lo que hace que se cierre instantáneamente. La comparación 
        #? de abajo hace que no se cierre el calendar y permita editar la fecha.
        if not datetimeedit.calendarWidget().hasFocus():
            datetimeedit.deleteLater()
            removeTableCellsWidgets(table_view)
        return None


    @Slot(QTableView, QModelIndex)
    def handleTableUpdateItem(self, table_view:QTableView, curr_index:QModelIndex) -> None:
        '''
        Dependiendo del 'table_view' del cual se quiera modificar una celda y dependiendo de la columna seleccionada 
        en 'curr_index' crea un QLineEdit|QComboBox|QDateTimeEdit para permitir una modificación más adecuada en esa celda.
        Además conecta las señales/slots de los widgets y sus 'validators'.

        Este método llama a:
        - functionutils.createTableColumnComboBox: para crear QComboBox.
        - functionutils.createTableColumnLineEdit: para crear QLineEdit.
        - functionutils.createTableColumnDateTimeEdit: para crear QDateTimeEdit.
        
        PARAMS:
        - table_view: el QTableView al que se referencia.
        - curr_index: índice seleccionado en 'table_view'.
        
        Retorna None.
        '''
        cell_old_text:str # texto actual de la celda.
        self.combobox:QComboBox
        self.lineedit:QLineEdit
        self.datetimeedit:QDateTimeEdit
        validator:ProductNameValidator
        
        # desactivo el ordenamiento de la tabla
        # table_view.setSortingEnabled(False)

        if table_view.editTriggers() != QAbstractItemView.EditTrigger.NoEditTriggers:
            # cell_old_text = table_view.item(curr_index.row(), curr_index.column()).text()
            
            match table_view.objectName():
                case "tv_inventory_data":
                    self.ui.label_feedbackInventory.hide()
                    
                    match curr_index.column():
                        case 0: # categoría (QComboBox)
                            self.combobox = createTableColumnComboBox(table_view, curr_index, cell_old_text)
                            self.combobox.textActivated.connect(lambda: self.__tableComboBoxOnCurrentTextChanged(
                                table_view=table_view,
                                curr_index=curr_index,
                                combobox=self.combobox))
                            
                        case _: # nombre | descripción | stock | precio unitario | precio comercial (QLineEdit)
                            self.lineedit = createTableColumnLineEdit(table_view, curr_index)
                        
                            self.lineedit.returnPressed.connect(lambda: self.__tableLineEditOnReturnPressed(
                                table_view=self.ui.tv_inventory_data,
                                curr_index=curr_index,
                                lineedit=self.lineedit,
                                prev_text=cell_old_text))
                            
                            if curr_index.column() != 2: # diferente de descripción (no tiene validador)
                                # señal del validador
                                validator = self.lineedit.validator()
                                validator.validationSucceeded.connect(self.ui.label_feedbackInventory.hide)
                                validator.validationFailed.connect(lambda text: self.__onDelegateValidationFailed(
                                    feedback_text=text,
                                    feedback_label=self.ui.label_feedbackInventory,
                                    curr_text=self.lineedit.text(),
                                    prev_text=cell_old_text))
                
                
                case "tv_sales_data":
                    self.ui.label_feedbackSales.hide()
                    
                    match curr_index.column():
                        case 2: # producto (QComboBox)
                            self.combobox  = createTableColumnComboBox(table_view, curr_index, cell_old_text)
                            
                            self.combobox.textActivated.connect(lambda: self.__tableComboBoxOnCurrentTextChanged(
                                table_view=table_view,
                                curr_index=curr_index,
                                combobox=self.combobox))
                        
                        case 5: # fecha y hora (QDateTimeEdit)
                            self.datetimeedit = createTableColumnDateTimeEdit(table_view, curr_index)
                            
                            self.datetimeedit.editingFinished.connect(lambda: self.__tableDateTimeOnEditingFinished(
                                table_view=table_view,
                                curr_index=curr_index,
                                datetimeedit=self.datetimeedit))
                        
                        case _: # detalle de venta | cantidad | costo total | abonado (QLineEdit)
                            
                            self.lineedit = createTableColumnLineEdit(table_view, curr_index)
                            
                            self.lineedit.returnPressed.connect(lambda: self.__tableLineEditOnReturnPressed(
                                table_view=self.ui.tv_sales_data,
                                curr_index=curr_index,
                                lineedit=self.lineedit,
                                prev_text=cell_old_text))
                            
                            # señal del validador
                            validator = self.lineedit.validator()
                            validator.validationSucceeded.connect(self.ui.label_feedbackSales.hide)
                            validator.validationFailed.connect(lambda text: self.__onDelegateValidationFailed(
                                feedback_text=text,
                                feedback_label=self.ui.label_feedbackSales,
                                curr_text=self.lineedit.text(),
                                prev_text=cell_old_text))
                
                            
                case "tv_debts_data":
                    self.ui.label_feedbackDebts.hide()
                    
        return None


    @Slot(object)
    def __onDelegateValidationSucceded(self, TableViewID:TableViewId) -> None:
        '''
        Esconde los labels de feedback relacionados con la VISTA a la que se 
        referencia.

        Parámetros
        ----------
        TableViewID : TableViewId
            QTableView al que se refencia

        Retorna
        -------
        None
        '''
        match TableViewID.name:
            case "INVEN_TABLE_VIEW": # inventario
                self.ui.label_feedbackInventory.hide()
            
            case "SALES_TABLE_VIEW":
                self.ui.label_feedbackSales.hide()
                
            case "DEBTS_TABLE_VIEW":
                self.ui.label_feedbackDebts.hide()
        
        return None


    @Slot(tuple)
    def __onDelegateValidationFailed(self, feedback:tuple[TableViewId, str]) -> None:
        '''
        Muestra el label con feedback relacionado con la VISTA a la que se referencia 
        y cambia la hoja de estilos del label.
        
        Parámetros
        ----------
        feedback: tuple[TableViewId, str]
            contiene el QTableView al que se referencia y el texto como feedback a mostrar 
            en el label
        
        Retorna
        -------
        None
        '''
        match feedback[0].name:
            case "INVEN_TABLE_VIEW":
                self.ui.label_feedbackInventory.show()
                self.ui.label_feedbackInventory.setStyleSheet(LabelFeedbackStyle.INVALID.value)
                self.ui.label_feedbackInventory.setText(feedback[1])
                
            case "SALES_TABLE_VIEW":
                self.ui.label_feedbackSales.show()
                self.ui.label_feedbackSales.setStyleSheet(LabelFeedbackStyle.INVALID.value)
                self.ui.label_feedbackSales.setText(feedback[1])
                
            case "DEBTS_TABLE_VIEW":
                self.ui.label_feedbackDebts.show()
                self.ui.label_feedbackDebts.setStyleSheet(LabelFeedbackStyle.INVALID.value)
                self.ui.label_feedbackDebts.setText(feedback[1])
        return None


    #¡ método de cambios en la selección
    @Slot(QTableView)
    def handleSelectionChange(self, table_view:QTableView) -> None:
        '''
        Esta función es llamada ni bien se detecta que la selección de los items en 'table_view' cambia. 
        Verifica si hay celdas seleccionadas. Si no hay, llama a 'functionutils.removeTableCellsWidgets'.
        
        Retorna None.'''
        # obtengo los items seleccionados actualmente de las tablas
        curr_selection = table_view.selectedItems()
        if len(curr_selection) <= 1: # por alguna razón 'curr_selection' siempre tiene 1 item, nunca llega a estar vacía...
            removeTableCellsWidgets(table_view)
        return None



    #¡### INVENTARIO ##################################################
    # funciones de inventory_sideBar
    def __calculateNewPrices(self, selected_rows:tuple) -> None:
        '''Calcula los aumentos/decrementos en los precios unitarios o comerciales dependiendo de cuál es la checkbox 
        marcada en 'inventory_sideBar'; declara la consulta sql y los parámetros que recibirá, y llama a 
        '__makeUpdateQuery_prices'; finalmente, actualiza los valores en la tabla. Retorna 'None'.'''
        sql:str
        params:list[dict] = []
        # si está activada la checkbox de precios unitarios calcula cuánto será, declara los parámetros para la consulta 
        # y reemplaza el valor viejo por el nuevo...
        if self.ui.checkbox_unit_prices.isChecked():
            for row in range(len(selected_rows)):
                if self.IDs_products[selected_rows[row]] not in params:
                    try:
                        # calcula cuál es el porcentaje que el valor del lineedit representa
                        percentage = int(self.ui.lineEdit_percentage_change.text().replace(".","").replace(",",""))
                        value = float(self.ui.tv_inventory_data.item(selected_rows[row], 4).text())
                        unit_price = value + (value * percentage / 100)
                        # asigna el valor nuevo
                        params.append({'id': self.IDs_products[selected_rows[row]],
                                        'unit_pr': f"{unit_price:.2f}"})
                        self.ui.tv_inventory_data.item(selected_rows[row], 4).setText(f"{unit_price:.2f}")
                        sql:str = "UPDATE Productos SET precio_unit = :unit_pr WHERE IDproducto = :id;"
                        self._db_repo.updateRegisters(sql, params, inv_prices=True)
                    except:
                        pass

        # sino, si está activada la checkbox de precios comerciales...
        else:
            for row in range(len(selected_rows)):
                if self.IDs_products[selected_rows[row]] not in params and self.ui.tv_inventory_data.item(selected_rows[row], 5).text() != "":
                    try:
                        # calcula el valor nuevo
                        percentage = int(self.ui.lineEdit_percentage_change.text().replace(".","").replace(",",""))
                        value = float(self.ui.tv_inventory_data.item(selected_rows[row], 5).text())
                        comerc_price = value + (value * percentage / 100)
                        # asigna el valor nuevo
                        params.append({'id': self.IDs_products[selected_rows[row]],
                                       'comerc_pr': f"{comerc_price:.2f}"})
                        self.ui.tv_inventory_data.item(selected_rows[row], 5).setText(f"{comerc_price:.2f}")
                        sql:str = "UPDATE Productos SET precio_comerc = :comerc_pr WHERE IDproducto = :id;"
                        self._db_repo.updateRegisters(sql, params, inv_prices=True)
                    except:
                        pass
        return None


    def validateLineeditPercentageChange(self) -> bool:
        '''Valida el valor de entrada para 'lineEdit_percentage_change' y sino lo es muestra un mensaje en 
        'label_feedbackChangePercentage' informando el problema. Retorna 'True' si es válido, sino 'False'.'''
        is_valid:bool = True
        if self.ui.lineEdit_percentage_change.text().strip() == "":
            is_valid = False
            self.ui.label_feedbackChangePercentage.show()
            self.ui.label_feedbackChangePercentage.setStyleSheet("font-family: 'Verdana'; font-size: 16px; letter-spacing: 0px; word-spacing: 0px; color: #f44;")
            self.ui.label_feedbackChangePercentage.setText("Se debe asignar un valor de cambio")
        else:
            self.ui.label_feedbackChangePercentage.hide()
        return is_valid


    @Slot()
    def handleLineeditPercentageEditingFinished(self) -> None:
        '''Maneja los métodos asociados con 'lineEdit_percentage_change'. Llama a 'validateLineeditPercentageChange' para 
        validar el valor ingresado, y si es válido obtiene las filas seleccionadas con 'getSelectedTableRows', calcula los 
        precios nuevos y los actualiza en la base de datos con '__calculateNewPrices', además actualiza los valores en la 
        tabla. Retorna 'None'.'''
        if self.validateLineeditPercentageChange():
            selected_rows = getSelectedTableRows(self.ui.tv_inventory_data)
            self.__calculateNewPrices(selected_rows)
        return None


    @Slot()
    def handleCheckboxStateChange(self) -> None:
        '''Dependiendo de cuál se haya checkeado, permite al usuario seleccionar las filas de los productos cuyos 
        precios (unitarios o comerciales) de la tabla 'tv_inventory_data' desee incrementar/decrementar de forma porcentual. Además 
        al checkear cualquier checkbox se habilita el 'lineEdit_percentage_change', sino lo deshabilita. Retorna 'None'.'''
        if self.ui.checkbox_unit_prices.isChecked() or self.ui.checkbox_comercial_prices.isChecked():
            # cambia el modo de selección de 'tv_inventory_data', habilita el lineedit
            self.ui.tv_inventory_data.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.ui.tv_inventory_data.setSelectionBehavior(QAbstractItemView.SelectRows)
            self.ui.tv_inventory_data.setSelectionMode(QAbstractItemView.MultiSelection)
            self.ui.lineEdit_percentage_change.setEnabled(True)
        else: # vuelve a poner el modo de selección de 'tv_inventory_data' al que tiene por defecto, deshabilita el lineedit
            self.ui.tv_inventory_data.setEditTriggers(QAbstractItemView.DoubleClicked)
            self.ui.tv_inventory_data.setSelectionBehavior(QAbstractItemView.SelectItems)
            self.ui.tv_inventory_data.setSelectionMode(QAbstractItemView.ExtendedSelection)
            self.ui.lineEdit_percentage_change.setEnabled(False)
        return None
    

    # funciones de inventory_checkbuttons_buttonGroup
    @Slot(QCheckBox)
    def handlePressedCheckbutton(self, checkbox:QCheckBox) -> None:
        '''Permite seleccionar/deseleccionar un checkbox libremente, y se usa en conjunto con 'handleClickedCheckbutton'. 
        Retorna 'None'.'''
        checkbox.group().setExclusive(not checkbox.isChecked())


    @Slot(QCheckBox)
    def handleClickedCheckbutton(self, checkbox:QCheckBox) -> None:
        '''Permite seleccionar/deseleccionar un checkbox libremente, y se usa en conjunto con 'handlePressedCheckbutton'. 
        Retorna 'None'.'''
        checkbox.group().setExclusive(True)



    #¡### VENTAS ######################################################
    
    #* MÉTODOS DE VALIDADOR DE 'lineEdit_paid'
    @Slot()
    def onPaidValidationSucceded(self) -> None:
        '''
        Es llamado desde la señal 'validationSucceeded' de 'lineEdit_paid'.
        
        Cambia el estilo de 'lineEdit_paid' para representar la validez del campo y el valor de la variable 
        'self.VALID_PAID_FIELD' a True.
        
        Retorna None.
        '''
        # si el campo es válido y no está vacío lo pone de color verde, si está vacío le quita el estilo
        self.ui.lineEdit_paid.setStyleSheet(WidgetStyle.FIELD_VALID_VAL.value if self.ui.lineEdit_paid.text().strip() else "")
        self.VALID_PAID_FIELD = True
        
        return None
    
    
    @Slot()
    def onPaidValidationFailed(self) -> None:
        '''
        Es llamado desde la señal 'validationFailed' de 'lineEdit_paid'.
        
        Cambia el estilo de 'lineEdit_paid' para representar la invalidez del campo y el valor de la variable 
        'self.VALID_PAID_FIELD' a False.
        
        Retorna None.
        '''
        self.ui.lineEdit_paid.setStyleSheet(WidgetStyle.FIELD_INVALID_VAL.value)
        self.VALID_PAID_FIELD = False
        
        return None
    

    #* MÉTODOS DEL FORMULARIO DE VENTAS            
    @Slot()
    def onSalePaidEditingFinished(self) -> None:
        '''
        Es llamado desde la señal 'editingFinished' de 'lineEdit_paid'.
        
        Formatea el campo del QLineEdit y llama al método 'self.setSaleChange' para calcular y mostrar 
        el cambio.
        
        Retorna None.
        '''
        field_text:str = self.ui.lineEdit_paid.text()
        
        field_text = field_text.replace(".",",")
        field_text = field_text.strip()
        field_text = field_text.rstrip(",.") if field_text.endswith((",",".")) else field_text
        field_text = field_text.lstrip("0") if field_text.startswith("0") else field_text
        
        self.ui.lineEdit_paid.setText(field_text)
        
        self.setSaleChange()
        return None
    
    
    def __updateItemsValues(self, list_item:ListItemValues=None, item_to_delete:str=None) -> None:
        '''
        Es llamado desde los métodos 'self.onSalesItemFieldValidation' | 'self.onSalesItemDeletion' | 
        'self.addSalesInputListItem'.
        
        Actualiza el diccionario 'self.DICT_ITEMS_VALUES' a partir del valor de 'list_item' ó elimina 
        el item con nombre 'item_to_delete' del diccionario, y además si es necesario reinicia el 
        contador 'self.SALES_ITEM_NUM' y desactiva el botón 'btn_end_sale'.
        
        PARAMS:
        - list_item: objeto de tipo 'classes.ListItemValues' con todos los valores actualizados del item. 
        Es enviado el parámetro cuando el método es llamado desde los métodos 'self.onSalesItemFieldValidation' | 
        'self.addSalesInputListItem'.
        - item_to_delete: str que determina cuál item debe ser borrado. Es enviado el parámetro cuando el 
        método es llamado desde el método 'self.onSalesItemDeletion'.
        
        Retorna None.
        '''
        if not item_to_delete:
            self.DICT_ITEMS_VALUES[list_item.object_name] = list_item
        
        else:
            self.DICT_ITEMS_VALUES.pop(item_to_delete)
            
            # reinicia el contador de nombres cuando no hay items en 'sales_input_list', y desactiva 'btn_end_sale'
            if self.ui.sales_input_list.count() == 0:
                self.SALES_ITEM_NUM = 0
                self.ui.btn_end_sale.setEnabled(False)
        
        return None


    @Slot(ListItemValues)
    def onSalesItemFieldValidation(self, list_item:ListItemValues) -> None:
        '''
        Es llamado desde la señal 'fieldsValidated' de 'classes.ListItemWidget'.
        
        Este método hace lo siguiente:
        - Actualiza 'self.DICT_ITEMS_VALUES'. Para eso llama al método 'self.__updateItemsValues'.
        - Verifica la validez de todos los items. Para eso llama al método 'self.validateSalesItemsFields'.
        - Cambia el contenido de 'dateTimeEdit_sale' para mostrar la hora precisa de la venta.
        
        PARAMS:
        - list_item: objeto de tipo 'classes.ListItemValues' con todos los valores actualizados del item.
        
        Retorna None.
        '''
        # actualiza self.DICT_ITEMS_VALUES
        self.__updateItemsValues(list_item)
        
        self.validateSalesItemsFields()
        
        # cambia la hora de la venta
        self.ui.dateTimeEdit_sale.setDateTime(QDateTime.currentDateTime())
        return None
    

    def setSaleChange(self) -> None:
        '''
        Es llamado desde el método 'self.onSalePaidEditingFinished'.
        
        Si todos los valores de los items son válidos, muestra el cambio a devolver a partir del valor 
        de 'lineEdit_paid', o si lo abonado es mayor al total se muestra el cambio que se debe dar en 
        'label_total_change'.
        
        Retorna None.
        '''
        total_paid:float

        # si self.TOTAL_COST es None significa que hay items con valores inválidos
        if self.TOTAL_COST:
            # si no hay un valor en lineEdit_paid, le pone 0
            if not self.ui.lineEdit_paid.text():
                self.ui.lineEdit_paid.setText(f"0.0")
                
            # obtiene el total abonado
            total_paid = float(self.ui.lineEdit_paid.text().replace(",","."))

            # verifica si 'self.lineEdit_paid' tiene un valor mayor al total
            if total_paid > self.TOTAL_COST: # si lo abonado es mayor al total se muestra el cambio
                self.ui.label_total_change.setText(f"{round(total_paid - self.TOTAL_COST, 2)}")

            else:
                self.ui.label_total_change.setText("")
            
        return None


    def validateSalesItemsFields(self) -> None:
        '''
        Es llamado desde los métodos 'self.onSalesItemDeletion' | 'self.onSalesItemFieldValidation'.
        
        Este método hace lo siguiente:
        - Si todos los campos son válidos:
            - Habilita el botón 'btn_end_sale'.
            - Obtiene el precio total y lo coloca en 'self.label_total' y lo guarda en 'self.TOTAL_COST', si 
            hay campos inválidos en items entonces 'self.TOTAL_COST' será None.
            - Crea un QCompleter para 'self.lineEdit_paid' con el precio total y los subtotales.
        - Si hay campos inválidos:
            - Deshabilita el botón 'btn_end_sale'.
            - Coloca el texto inicial en 'label_total'.
            - Coloca el valor None en 'self.TOTAL_COST'.
        
        Retorna None.
        '''
        subtotals:list[float] = [] # lista con los subtotales de los items, es usado por 'completer_values' y
                                   # y para calcular el costo total
        total_cost:str # var. aux. que contiene el costo total
        completer_values:list[str] = [] # lista con todos los valores ('subtotals') y costo total para colocar 
                                        # en el completer
        completer:QCompleter # completer para colocar en lineEdit_paid con el total
        
        # verifica si 'sales_input_list' no está vacía y si todos los items tienen 'ALL_VALID==True'
        if self.ui.sales_input_list.count() > 0 and all( [item.ALL_VALID for item in self.DICT_ITEMS_VALUES.values()] ):
            self.ui.btn_end_sale.setEnabled(True)
            
            # obtiene los subtotales (para obtener el total y para luego colocarlos en el completer)
            subtotals = [item.subtotal for item in self.DICT_ITEMS_VALUES.values()]
            
            # obtiene el costo total
            self.TOTAL_COST = round(sum(subtotals), 2)
            
            # coloca el costo total en label_total
            total_cost = str(self.TOTAL_COST).replace(".",",")
            self.ui.label_total.setText(
                f"<html><head/><body><p>TOTAL <span style=\" color: #22577a;\">{total_cost}</span></p></body></html>"
                )
            
            # obtengo todos los valores para el completer (total y subtotales)
            completer_values = [str(value).replace(".",",") for value in subtotals + [total_cost]] # concatena 'subtotals' y 
                # el costo total, convierte los valores a str y le cambia los "." por ",".
            
            # crea el completer para los costos en 'lineEdit_paid'
            completer = QCompleter(completer_values, parent=self.ui.lineEdit_paid)
            completer.setCompletionMode(completer.CompletionMode.InlineCompletion)
            completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
            self.ui.lineEdit_paid.setCompleter(completer)

            self.ui.lineEdit_paid.textChanged.connect(completer.setCompletionPrefix)

        else:
            self.ui.btn_end_sale.setEnabled(False)
            self.ui.label_total.setText("TOTAL")
            self.TOTAL_COST = None
        
        return None
    

    @Slot(QListWidgetItem, str)
    def onSalesItemDeletion(self, list_widget_item:QListWidgetItem, list_item_name:str) -> None:
        '''
        Es llamado desde la señal 'deletedItem' del item actual declarado en 'self.addSalesInputListItem'.
        
        Elimina el item referido en 'item_list_widget' del QListWidget 'self.sales_input_list', y llama al método 
        'self.__updateItemsValues' para borrar el item con nombre 'list_item_name' en 'self.DICT_ITEMS_VALUES', 
        y llama al método 'self.validateSalesItemsFields' para validar los otros items.
        
        PARAMS:
        - item_list_widget: el QListWidgetItem al que se referencia.
        - list_item_name: el 'objectName' del objecto 'classes.ListItemWidget' interno de 'item_list_widget'.
        
        Retorna None.
        '''
        row:int = self.ui.sales_input_list.row(list_widget_item)
        self.ui.sales_input_list.takeItem(row)
        self.__updateItemsValues(item_to_delete=list_item_name)
        self.validateSalesItemsFields()
        return None


    @Slot()
    def addSalesInputListItem(self) -> None:
        '''
        Es llamado desde la señal 'clicked' de 'btn_add_product'.
        
        Crea un item de tipo 'classes.ListItemWidget' que se colocará dentro de 'sales_input_list', y que representa 
        la venta de un producto, y conecta sus señales.
        
        Retorna None.
        '''
        object_name:str = f"item_{self.SALES_ITEM_NUM}"
        list_widget_item:QListWidgetItem = QListWidgetItem()
        item:ListItemWidget = ListItemWidget(obj_name=object_name)

        # incremento self.SALES_ITEM_NUM
        self.SALES_ITEM_NUM += 1
        
        #? agrego un elemento vacío a self.DICT_ITEMS_VALUES para evitar falsos positivos y activar el botón 
        #? 'btn_end_sale' sin querer cuando un elemento es válido y hay otros que no fueron modificados aún...
        #? de cualquier forma, este item temporal va a ser sobreescrito cuando se modifique/borre el item
        self.__updateItemsValues(
            list_item=ListItemValues(
                object_name=object_name,
                ALL_VALID=False)
            )
        
        # conecto señales
        item.fieldsValidated.connect(self.onSalesItemFieldValidation)
        item.deleteItem.connect(lambda list_item_name: self.onSalesItemDeletion(list_widget_item, list_item_name))

        # coloca el widget dentro del item
        list_widget_item.setSizeHint(item.size())
        self.ui.sales_input_list.addItem(list_widget_item)
        self.ui.sales_input_list.setItemWidget(list_widget_item, item)

        # pone el foco en el item nuevo
        self.ui.sales_input_list.setFocus()
        self.ui.sales_input_list.setCurrentItem(list_widget_item)
        item.findChild(QComboBox, "comboBox_productName").setFocus()

        # desactiva btn_end_sale cuando se agrega un producto
        self.ui.btn_end_sale.setEnabled(False)
        return None


    @Slot()
    def handleFinishedSale(self) -> None:
        '''
        Es llamado desde la señal 'clicked' de 'btn_end_sale'.
        
        Este método hace lo siguiente:
        - Si la cantidad abonada es < al costo total:
            - Instancia y muestra un dialog de tipo 'DebtorDataDialog' con los datos del deudor, además conecta 
            su señal 'debtorChosen' al método 'self.finishedSaleOnDebtorChosen'.
        - Si la cantidad abonada es >= al costo total:
            - Obtiene los datos de los campos de los items y hace las consultas INSERT a Ventas y Detalle_Ventas 
            y la consulta UPDATE a Productos con el nuevo stock.
            - Al finalizar, llama al método 'self.__resetFieldsOnFinishedSale' para realizar los reinicios necesarios.
        
        Retorna None.
        '''
        total_paid:float
        product_id:int # aux. necesaria porque, si hay más de 1 item en 'sales_input_list', falla al hacer la subconsulta 
                       # en el INSERT a Detalle_Ventas... así que hago un SELECT del IDproducto y lo guardo en una var. aux.
        
        # obtengo el total pagado
        total_paid = self.ui.lineEdit_paid.text().replace(",",".")
        total_paid = float(total_paid if total_paid else 0.0)
        
        # si lo abonado es menor al total muestra el Dialog para manejar deudores
        if total_paid < self.TOTAL_COST:
            dialog = DebtorDataDialog()
            dialog.setAttribute(Qt.WA_DeleteOnClose, True)
            
            dialog.debtorChosen.connect(lambda debtor_id: self.finishedSaleOnDebtorChosen(
                debtor_id=debtor_id,
                total_paid=total_paid))
            
            dialog.exec()
        
        # si lo abonado es >= al costo total realiza INSERT a Ventas y Detalle_Ventas, y UPDATE a Productos
        else:
            conn = createConnection("database/inventario.db")
            cursor = conn.cursor()
            
            for item in self.DICT_ITEMS_VALUES.values():
                try:
                    # inserta a Ventas
                    cursor.execute(
                        "INSERT INTO Ventas(fecha_hora, detalles_venta) VALUES(?,?);",
                        (self.ui.dateTimeEdit_sale.text(), item.sale_details,)
                        )
                    conn.commit()
                    
                    # inserta a Detalle_Ventas
                    cursor.execute(
                        "INSERT INTO Detalle_Ventas(cantidad, costo_total, IDproducto, IDventa, abonado, IDdeuda) VALUES(?, ?, (SELECT IDproducto FROM Productos WHERE nombre = ?), (SELECT IDventa FROM Ventas WHERE fecha_hora = ? AND detalles_venta = ?), ?, NULL);",
                        (item.quantity, item.subtotal, item.product_name, self.ui.dateTimeEdit_sale.text(), 
                         item.sale_details, item.subtotal,)
                        )
                    conn.commit()
                    
                    # actualiza en Productos
                    cursor.execute(
                        "UPDATE Productos SET stock = stock - ? WHERE nombre = ?;",
                        (item.quantity, item.product_name,)
                    )
                    conn.commit()
                
                except sqlite3Error as err:
                    conn.rollback()
                    logging.critical(f"{err.sqlite_errorcode}: {err.sqlite_errorname} / {err}")
        
            conn.close()
            # hace los reinicios necesarios para otras ventas
            self.__resetFieldsOnFinishedSale()
        
        return None


    @Slot(tuple)
    def finishedSaleOnDebtorChosen(self, debtor_id:int, total_paid:float) -> None:
        '''
        Es llamado desde la señal 'debtorChosen' del objeto de tipo 'DebtorDataDialog' instanciado en 
        el método 'self.handleFinishedSale'.
        
        Este método hace lo siguiente:
        - Obtiene los datos de los campos de los items y hace las consultas INSERT a Ventas, Detalle_Ventas 
        y Deudas y la consulta UPDATE a Productos con el nuevo stock.
        NOTA: ESTE MÉTODO NO HACE CONSULTA ALGUNA A LA TABLA "Deudores", ESAS CONSULTAS SON HECHAS EN EL DIALOG 
        'DebtorDataDialog'.
        - Al finalizar, llama al método 'self.__resetFieldsOnFinishedSale' para realizar los reinicios necesarios.
        
        PARAMS:
        - debtor_id: int con el 'IDdeudor' emitido desde 'DebtorDataDialog'.
        - total_paid: float con el total abonado al finalizar la venta. Proviene de 'lineEdit_paid'.
        
        Retorna None.
        '''
        total_due:float = total_paid # acumulador, inicia con el valor del total abonado y se va descontando de ahí 
                                     # cada subtotal (el precio de cada producto)
        item:ListItemValues # var. usada en el 'for' que recorre 'self.DICT_ITEMS_VALUES'
        
        #? Decidí que cuando se hacen ventas (sin importar la cantidad de productos diferentes) y el comprador paga 
        #? menos del total, esa cantidad sea distribuída entre los primeros productos. 
        #? ejemplo: una persona lleva 3 productos -> 1 de $3.000, 1 de $2.000 y otro de $4.000, pero paga $4.000.
        #?     esos $4.000 se descuentan, primero, del primer producto:
        #?         $4.000 - $3.000 = $1.000
        #?         $1.000 - $2.000 = $-1.000 <-- -1.000 es lo que queda del 2do producto, más el 3er producto.
        #?     luego se agrega a Deudas los $1.000 que quedaron del 2do producto y también el 3er producto, pero 
        #?     no el 1ro que quedó pago.
        
        conn = createConnection("database/inventario.db")
        cursor = conn.cursor()
        
        # recorre cada item y hace las consultas INSERT y UPDATE (a Productos)
        for item in self.DICT_ITEMS_VALUES.values():
            try:
                cursor.execute(
                    "INSERT INTO Ventas(fecha_hora, detalles_venta) VALUES(?,?);",
                    (self.ui.dateTimeEdit_sale.text(), item.sale_details,)
                    )
                conn.commit()
                
                # actualiza el total debido
                total_due -= item.subtotal # deuda = total abonado - subtotal
                total_due = round(total_due, 2)
                
                # Deudas y Detalle_Ventas (con IDdeuda)
                if total_due < 0: # el producto es deuda
                    cursor.execute(
                        "INSERT INTO Deudas(fecha_hora, total_adeudado, IDdeudor, eliminado) VALUES(?,?,?, 0);",
                        (self.ui.dateTimeEdit_sale.text(), abs(total_due), debtor_id))
                    conn.commit()
                    
                    cursor.execute(
                        "INSERT INTO Detalle_Ventas(cantidad, costo_total, IDproducto, IDventa, abonado, IDdeuda) VALUES(?, ?, (SELECT IDproducto FROM Productos WHERE nombre = ?),(SELECT IDventa FROM Ventas WHERE fecha_hora = ? AND detalles_venta = ?), ?, (SELECT IDdeuda FROM Deudas WHERE fecha_hora = ? AND IDdeudor = ? ORDER BY IDdeuda DESC LIMIT 1));",
                        (item.quantity, item.subtotal, item.product_name, self.ui.dateTimeEdit_sale.text(),
                        item.sale_details, round(item.subtotal - abs(total_due), 2), self.ui.dateTimeEdit_sale.text(),
                        debtor_id, )
                        )
                    conn.commit()
                    
                    total_due = 0
                
                else: # el producto NO es deuda
                    cursor.execute(
                        "INSERT INTO Detalle_Ventas(cantidad, costo_total, IDproducto, IDventa, abonado, IDdeuda) VALUES(?, ?, (SELECT IDproducto FROM Productos WHERE nombre = ?), (SELECT IDventa FROM Ventas WHERE fecha_hora = ? AND detalles_venta = ?), ?, NULL);",
                        (item.quantity, item.subtotal, item.product_name, self.ui.dateTimeEdit_sale.text(),
                        item.sale_details, item.subtotal,)
                        )
                    conn.commit()
                    
                # como última consulta de cada item, actualiza el stock
                cursor.execute(
                    "UPDATE Productos SET stock = stock - ? WHERE nombre = ?;",
                    (item.quantity, item.product_name,)
                    )
                conn.commit()
            
            except sqlite3Error as err:
                conn.rollback()
                logging.critical(f"{err.sqlite_errorcode}: {err.sqlite_errorname} / {err}")
            
        conn.close()
        
        # hace los reinicios necesarios para otras ventas
        self.__resetFieldsOnFinishedSale()
        
        return None
    
    
    def __resetFieldsOnFinishedSale(self) -> None:
        '''
        Es llamado desde el método 'self.handleFinishedSale'.
        
        Luego de realizadas las consultas INSERT y UPDATE a base de datos, éste método se encarga de realizar 
        los reinicios finales para poder concretar otra venta.
        Este método hace lo siguiente:
        - Reinicia el contador para nombres de items 'self.SALES_ITEM_NUM'.
        - Limpia los items en 'self.DICT_ITEMS_VALUES'.
        - Limpia los campos y reasigna el por defecto a 'label_total'.
        - Desactiva el botón 'btn_end_sale'.
        
        Retorna None.
        '''
        # limpia 'sales_input_list'
        self.ui.sales_input_list.clear()
        
        self.SALES_ITEM_NUM = 0
        
        # limpia los items
        self.DICT_ITEMS_VALUES.clear()
        
        # coloca los textos inicial en los labels
        self.ui.label_total.setText("TOTAL")
        self.ui.label_total_change.setText("")
        
        # borra el texto en 'lineEdit_paid'
        self.ui.lineEdit_paid.setText("")
        
        self.ui.btn_end_sale.setEnabled(False)
        
        self.debtor_chosen = None
        self.ui.btn_end_sale.setEnabled(False)
        return None
    
    
    #¡### DEUDAS ######################################################
    def __fillDebtsTable(self) -> None:
        '''
        Es llamada desde 'fillTableView'.
        
        Recorre cada item y, dependiendo de la columna en la que esté, crea instancias de las siguientes clases:
        - columna 0 (nombre completo): instancia de 'DebtsTablePersonData'.
        - columna 1 (productos): ...
        Si la columna es la 2 (total adeudado) coloca el total que se adeuda.
        
        Retorna None.
        '''
        for row in range(self.ui.tv_debts_data.rowCount()):
            widget = DebtsTablePersonData(tableWidget=self.ui.tv_debts_data, full_name="nombre completo")
            self.ui.tv_debts_data.setCellWidget(row, 0, widget)
        
            





def main():
    logging.basicConfig(
        format='%(asctime)s -- (%(levelname)s) %(module)s.%(funcName)s:%(message)s',
        level=logging.DEBUG,
        datefmt='%A %d/%m/%Y %H:%M:%S')
    
    
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())
    


# MAIN #########################################################################################################
if __name__=='__main__':
    main()