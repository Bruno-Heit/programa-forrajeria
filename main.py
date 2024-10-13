import sys
from numpy import (empty, ndarray)
from typing import (Any, Iterable)

from PySide6.QtWidgets import (QApplication, QMainWindow, QLineEdit, QTableView, 
                               QCheckBox, QAbstractItemView, QDateTimeEdit, QListWidgetItem, 
                               QLabel)
from PySide6.QtCore import (QModelIndex, Qt, QThread, Slot)
from PySide6.QtGui import (QIcon)

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
                               LabelFeedbackStyle, InventoryPriceType, TypeSideBar)

from resources import (rc_icons)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # inicializa ajustes personalizados de widgets
        self.setup_ui()
        
        # declara/instancia variables
        self.setup_variables()
        
        # repositorio de base de datos
        self._db_repo:DatabaseRepository = DatabaseRepository()
        
        # modelos de datos
        self.inventory_data_model:InventoryTableModel = InventoryTableModel()
        self.ui.tv_inventory_data.setModel(self.inventory_data_model)
        
        # delegados
        self.inventory_delegate = InventoryDelegate()
        self.ui.tv_inventory_data.setItemDelegate(self.inventory_delegate)
        
        # declara e instancia variables
        self.setup_variables()
        
        #! la declaración de señales se hace al final
        self.setup_signals()
        return None


    def setup_ui(self) -> None:
        '''
        Método que sirve para simplificar la lectura del método 'self.__init__'.
        Contiene inicializaciones y ajustes de algunos Widgets.
        
        Retorna
        -------
        None
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
        # las checkboxes de porcentajes son exclusivas
        self.ui.inventory_checkbuttons_buttonGroup.setExclusive(True)
        return None    


    def setup_variables(self) -> None:
        '''
        Al igual que el método 'self.setup_ui' y 'self.setup_signals', este 
        método tiene el objeto de simplificar la lectura del método 'self.__init__'.
        Contiene las declaraciones de variables locales que se usan a lo largo de la 
        ejecución del programa.
        
        Retorna
        -------
        None
        '''
        #¡ ======== variables de 'search bars' ================================
        # TODO: reimplementar funcionalidad de search bars

        #¡ ======== variable de inventario ====================================
        # TODO: eliminar el uso de 'self.IDs_products', acceder desde el modelo a los IDs
        self.IDs_products:list = [] # var. de 'tv_inventory_data' que tiene los 
                                    # IDs de los productos.
        #? Los acumuladores de datos sirven para hacer operaciones sobre los modelos de datos 
        #? y la base de datos en "batches" y mejorar el rendimiento de la aplicación en general
        self._inv_model_data_acc:ndarray[Any] = None # acumulador temporal de datos para los modelos
        self._UPD_BATCH_SIZE:int = None # cuando se modifican precios en porcentajes, sirve para 
                                        # hacerlo en batches.
        self.__upd_reg_count:int = 0 # se usa con 'self._UPD_BATCH_SIZE' y 'self._inv_model_data_acc', 
                                        # cuenta por qué registro va pasando desde el modelo a MainWindow.
        
        #¡ ======== variables de ventas =======================================
        self.ui.dateTimeEdit_sale.setDateTime(QDateTime.currentDateTime())
        
        self.IDs_saleDetails:list = [] # var. de 'tv_sales_data' que tiene los 
                                       # IDs de las ventas en Detalle_Ventas.
        self.SALES_ITEM_NUM:int = 0 # contador para crear nombres de items en 
                                    # 'input_sales_data'.
        self.DICT_ITEMS_VALUES:dict[str,ListItemValues] = {} # tiene los valores 
                                                             # de cada 'ListItemWidget'.
        self.VALID_PAID_FIELD:bool = None # True si lineEdit_paid es válido, sino False.
        self.TOTAL_COST:float = None # guarda el costo total de 'label_total' como 
                                     # float, para no tener que buscarlo con regex

        #¡ ======== variables de deudas =======================================
        
        # TODO: mostrar deudas
        # TODO: permitir agregar deuda
        # TODO: permitir eliminar deuda
        # TODO: permitir modificar deuda
        return None


    def setup_signals(self) -> None:
        '''
        Al igual que los métodos 'self.setup_ui' y 'self.setup_variables', este 
        método tiene el objeto de simplificar la lectura del método 'self.__init__'.
        Contiene las declaraciones de señales/slots de Widgets ya existentes 
        desde la instanciación de 'MainWindow'.
        
        Retorna
        -------
        None
        '''
        #¡========= INVENTARIO ================================================
        #* abrir/cerrar side bars
        self.ui.btn_side_barToggle.clicked.connect(lambda: self.toggleSideBar(
            TypeSideBar.CATEGORIES_SIDEBAR))
        
        self.ui.btn_inventory_sideBarToggle.clicked.connect(lambda: self.toggleSideBar(
            TypeSideBar.PERCENTAGES_SIDEBAR))
        
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
        self.ui.btn_delete_product_inventory.clicked.connect(lambda: self.handleTableDeleteRows(TableViewId.INVEN_TABLE_VIEW))
        
        #* (UPDATE) modificar celdas de 'tv_inventory_data' (sin porcentajes)
        self.inventory_data_model.dataToUpdate.connect(
            lambda params: self.__onInventoryModelDataToUpdate(
                column=params[0], IDproduct=params[1], new_val=params[2]))
        
        # delegados
        self.inventory_delegate.fieldIsValid.connect(self.__onDelegateValidationSucceded)
        self.inventory_delegate.fieldIsInvalid.connect(self.__onDelegateValidationFailed)
        
        #* inventory_sideBar
        self.ui.inventory_checkbuttons_buttonGroup.buttonPressed.connect(self.handlePressedCheckbox)
        self.ui.inventory_checkbuttons_buttonGroup.buttonClicked.connect(self.handleClickedCheckbox)
        
        self.ui.checkbox_unit_prices.stateChanged.connect(self.handleCheckboxStateChange)
        
        self.ui.checkbox_comercial_prices.stateChanged.connect(self.handleCheckboxStateChange)
        
        # señales del lineedit de porcentajes
        self.ui.lineEdit_percentage_change.editingFinished.connect(self.onLePercentageEditingFinished)
        self.ui.lineEdit_percentage_change.validator().validationSucceeded.connect(
            self.__onPercentageValidatorSucceded)
        self.ui.lineEdit_percentage_change.validator().validationFailed.connect(
            self.__onPercentageValidatorFailed)

        #¡========= VENTAS ====================================================
        #* (READ) cargar con ventas 'tv_sales_data'
        self.ui.tab2_toolBox.currentChanged.connect(lambda curr_index: self.fillTableView(
            self.ui.tv_sales_data, SHOW_ALL=True) if curr_index == 1 else None)
        
        self.ui.tabWidget.currentChanged.connect(lambda index: self.ui.tab2_toolBox.setCurrentIndex(0) if index == 1 else None)
        
        #* (CREATE) añadir una venta a 'tv_sales_data'
        self.ui.btn_add_product_sales.clicked.connect(lambda: self.handleTableCreateRow(self.ui.tv_sales_data))
        
        #* (DELETE) eliminar ventas de 'tv_sales_data'
        self.ui.btn_delete_product_sales.clicked.connect(lambda: self.handleTableDeleteRows(TableViewId.SALES_TABLE_VIEW))
        
        #* (UPDATE) modificar celdas de 'tv_sales_data'
        # TODO: reimplementar UPDATES de Ventas
        # self.ui.tv_sales_data.doubleClicked.connect(lambda: self.handleTableUpdateItem(self.ui.tv_sales_data, self.ui.tv_sales_data.currentIndex()) )
        
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
        
        Retorna
        -------
        None
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
        
        Retorna
        -------
        None
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
        Inicializa los validadores predefinidos (de widgets que conforman la GUI 
        base, no creados dinámicamente) y conecta sus señales y slots.
        
        Retorna
        -------
        None
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
            PercentageValidator(self.ui.lineEdit_percentage_change))
        
        # señales/slots
        self.total_paid_validator.validationSucceeded.connect(self.onPaidValidationSucceded)
        self.total_paid_validator.validationFailed.connect(self.onPaidValidationFailed)
        
        return None


    #¡ método de sidebars
    @Slot(object)
    def toggleSideBar(self, sidebar_type:TypeSideBar) -> None:
        '''
        Abre o cierra el sidebar, muestra o esconde sus widgets internos 
        y alterna la selección/edición en la tabla de inventario.

        Parámetros
        ----------
        sidebar_type : TypeSideBar
            El sidebar que se está modificando

        Retorna
        -------
        None
        '''
        perc_sidebar_opened:bool = False # se usa cuando el sidebar es el de 
                                         # porcentajes, para permitir o prohibir
                                         # selección y edición en la VISTA
        
        match sidebar_type.value:
            case 1: # sidebar de categorías
                toggleSideBar(
                    side_bar=self.ui.side_bar,
                    parent=self.ui.centralwidget,
                    body=self.ui.side_bar_body)
                # limpia la selección
                self.ui.tv_inventory_data.selectionModel().clearSelection()
                return None
            
            case 2: # sidebar de porcentajes
                perc_sidebar_opened = toggleSideBar(
                    side_bar=self.ui.inventory_sideBar,
                    parent=self.ui.main_inventory_frame,
                    body=self.ui.inventory_side_bar_body,
                    max_width=200
                )
                self.ui.tv_inventory_data.selectionModel().clearSelection()
        
        # alterna la selección y la edición...
        self.__alterViewSelEditAndParameters(perc_sidebar_opened)
        
        return None


    def __alterViewSelEditAndParameters(self, sidebar_opened:bool) -> None:
        '''
        Alterna la selección y edición en la VISTA 'tv_inventory_data' 
        dependiendo de si se abrió o cerró el sidebar de porcentajes, y
        cambia el estado de las checkboxes.

        Parámetros
        ----------
        sidebar_opened : bool
            Flag que determina si el sidebar de porcentajes se abrió 
            o cerró

        Retorna
        -------
        None
        '''
        match sidebar_opened:
            case True: # desactiva la selección y edición
                self.ui.tv_inventory_data.setEditTriggers(
                    QAbstractItemView.EditTrigger.NoEditTriggers)
                self.ui.tv_inventory_data.setSelectionBehavior(
                    QAbstractItemView.SelectionBehavior.SelectRows)
                self.ui.tv_inventory_data.setSelectionMode(
                    QAbstractItemView.SelectionMode.MultiSelection)
                # cambia el estado de las checkboxes
                self.ui.inventory_checkbuttons_buttonGroup.setExclusive(False)
                self.ui.checkbox_unit_prices.setChecked(False)
                self.ui.checkbox_comercial_prices.setChecked(False)
            
            case False: # activa la selección y edición
                self.ui.tv_inventory_data.setEditTriggers(
                    QAbstractItemView.EditTrigger.DoubleClicked)
                self.ui.tv_inventory_data.setSelectionBehavior(
                    QAbstractItemView.SelectionBehavior.SelectItems)
                self.ui.tv_inventory_data.setSelectionMode(
                    QAbstractItemView.SelectionMode.ExtendedSelection)
                # cambia la selección/deselección de las checkboxes
                self.ui.inventory_checkbuttons_buttonGroup.setExclusive(True)
            
        return None
    
    
    #¡ métodos de acumulador de datos
    def setNpDataAccumulator(self, tv_name:str,
                            model_shape:tuple[int, int]) -> None:
        '''
        Dependiendo de la VISTA usada, crea un 'numpy.ndarray' vacío con 
        las dimensiones especificadas.

        Parámetros
        ----------
        tv_name : str
            La VISTA que se referencia
        model_shape: tuple[int, int]
            Tupla con las dimensiones del arreglo

        Retorna
        -------
        None
        '''
        match tv_name:
            case "tv_inventory_data": # Productos
                self._inv_model_data_acc = empty(shape=model_shape, dtype=object)
            
            case "tv_sales_data": # Ventas
                pass
            
            case "tv_debts_data": # Ctas. Ctes.
                pass
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
        
        self.__startWorker(table_view, data_sql, data_params, count_sql, count_params)
        return None
    
    
    def __startWorker(self, table_view:QTableView, data_sql:str, data_params:tuple=None, count_sql:str=None, 
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
        self.setNpDataAccumulator(tv_name, model_shape)
        
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
        A medida que el WORKER encuentra registros guarda los IDs de los registros 
        coincidentes en una variable asociada a cada QTableView.
        
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
        QSS de dicha QProgressBar y carga los datos en el QTableView, luego reinicia 
        los acumuladores temporales.
        Si 'READ_OPERATION' es False es porque se realizaron otras consultas a la base 
        de datos (DELETE / INSERT) y el QTableView debe ser recargado.
        
        Parámetros
        ----------
            tv_name: QTableView
                nombre del QTableView al que se referencia
            READ_OPERATION: bool, opcional
                Flag que determina si la operación que se hizo fue de llenado (READ) a un 
                QTableView, por defecto es True

        Retorna
        -------
        None
        '''
        match tv_name:
            case "tv_inventory_data":
                self.ui.inventory_progressbar.setStyleSheet("")
                self.ui.inventory_progressbar.hide()
                # if not READ_OPERATION:
                #     # recarga la tabla
                #     try:
                #         self.fillTableView(table_view=self.ui.tv_inventory_data, SHOW_ALL=True)
                #     except AttributeError: # salta porque se intenta recargar la tabla pero nunca se llenó anteriormente
                #         pass
                # else:
                #     pass
                if READ_OPERATION:
                    self.inventory_data_model.setModelData(
                        data=self._inv_model_data_acc,
                        headers=ModelHeaders.INVENTORY_HEADERS.value)
            
                # borra el acumulador temporal de datos
                self._inv_model_data_acc = None

                
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
        Dependiendo del QTableView al que se agregue una fila, se encarga de 
        crear una instancia del QDialog correspondiente que pide los datos 
        necesarios para la nueva fila. Al final, recarga la tabla correspondiente 
        llamando a 'self.fillTableView'.
        
        Parámetros
        ----------
        table_view: QTableView
            El QTableView al que se referencia
        
        Retorna
        -------
        None
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
    @Slot(QTableView)
    def handleTableDeleteRows(self, table_viewID:TableViewId) -> None:
        '''
        Elimina los registros seleccionados en la VISTA correspondiente y modifica la base 
        de datos, además actualiza el estado de la progress-bar relacionada con la VISTA.
        NOTA: Este método NO ELIMINA LOS REGISTROS DE "Productos" NI "Deudas", LOS MARCA 
        COMO "ELIMINADOS" EN LA BASE DE DATOS. EN CAMBIO SÍ ELIMINA LOS REGISTROS DE "Ventas" 
        Y "Detalle_Ventas".
        
        Parámetros
        ----------
        table_viewID : TableViewId
            QTableView al que se refencia
        
        Retorna
        -------
        None
        '''
        match table_viewID.name:
            case "INVEN_TABLE_VIEW":
                self.__deleteInventoryRows()
            
            case "SALES_TABLE_VIEW":
                # TODO: una vez creado el modelo de ventas, obtener los datetime desde dicho modelo
                pass
                # dateTime_to_delete = self.__getTableElementsToDelete(table_view, selected_rows)
                
                # # obtiene ids de las filas seleccionadas
                # ids_to_delete = [self.IDs_saleDetails[n_id] for n_id in selected_rows]
                
                # mult_sql:tuple[str] = (
                #     "DELETE FROM Ventas WHERE IDventa = (SELECT IDventa FROM Detalle_Ventas WHERE ID_detalle_venta = ?) AND fecha_hora = ?;",
                #     "DELETE FROM Detalle_Ventas WHERE ID_detalle_venta = ?;",
                #     )
                
                # # une 'ids_to_delete' y 'dateTime_to_delete' en una lista[(id, fecha_y_hora)]
                # params = [(id, datetime) for id,datetime in zip(ids_to_delete, dateTime_to_delete)]
                
                # self.ui.sales_progressbar.setMaximum(len(params))
                # self.ui.sales_progressbar.setStyleSheet("QProgressBar::chunk {background-color: qlineargradient(spread:reflect, x1:0.119, y1:0.426, x2:0.712045, y2:0.926, stop:0.0451977 rgba(255, 84, 87, 255), stop:0.59887 rgba(255, 161, 71, 255));}")

            case "DEBTS_TABLE_VIEW":
                pass
        return None
    
    
    def __deleteInventoryRows(self, table_viewID:TableViewId=TableViewId.INVEN_TABLE_VIEW) -> None:
        '''
        Elimina los productos seleccionados en el MODELO de inventario, actualiza 
        la VISTA y marca el producto en la base de datos como eliminado.

        Parámetros
        ----------
        table_viewID : TableViewId, opcional
            QTableView al que se refencia

        Retorna
        -------
        None
        '''
        # obtiene las filas seleccionadas
        selected_rows = getSelectedTableRows(self.ui.tv_inventory_data)
        
        if not selected_rows:
            return None
        
        # cambia la progress-bar para representar las eliminaciones
        self.ui.inventory_progressbar.setMaximum(len(selected_rows))
        self.ui.inventory_progressbar.setStyleSheet(
            '''QProgressBar::chunk {
                background-color: qlineargradient(spread:reflect, x1:0.119, y1:0.426, 
                                                  x2:0.712045, y2:0.926, stop:0.0451977 
                                                  rgba(255, 84, 87, 255), 
                                                  stop:0.59887 rgba(255, 161, 71, 255));
                }''')
        
        # obtiene los ids para las consultas
        params_ids = self.__getDeleteData(table_viewID, selected_rows)
        
        # actualiza el MODELO de datos
        self.inventory_data_model.removeSelectedModelRows(selected_rows)
        
        # instancia y ejecuta WORKER y THREAD
        # self.__instanciateDeleteWorkerAndThread(table_viewID, params_ids)
        
        return None


    def __getDeleteData(self, table_viewID:TableViewId, selected_rows:Iterable) -> Iterable:
        '''
        Obtiene los datos necesarios desde el MODELO de datos de la VISTA especifica 
        para poder realizar las consultas.
        Si la VISTA es:
            1. Inventario: obtiene los IDs de los productos
            ...

        Parámetros
        ----------
        table_viewID : TableViewId
            QTableView al que se refencia

        Retorna
        -------
        Iterable
            iterable con los datos necesarios para las consultas
        '''
        data:list[Any] = []
        
        match table_viewID.name:
            case "INVEN_TABLE_VIEW":
                # obtiene los IDs de los productos
                for row in selected_rows:
                    data.append(self.inventory_data_model._data[row][0])
            
            case "SALES_TABLE_VIEW":
                pass
            
            case "DEBTS_TABLE_VIEW":
                pass
        
        return tuple(data)


    def __instanciateDeleteWorkerAndThread(self, table_viewID:TableViewId, del_params:Iterable) -> None:
        '''
        Dependiendo de la VISTA, instancia y ejecuta un WORKER y un QTHREAD para realizar 
        las consultas de eliminación a la base de datos y conecta sus señales.

        Parámetros
        ----------
        table_viewID : TableViewId
            QTableView al que se refencia
        del_params: Iterable
            parámetros necesarios para realizar las consultas UPDATE/DELETE

        Retorna
        -------
        None
        '''
        self.DELETE_THREAD = QThread()
        
        match table_viewID.name:
            case "INVEN_TABLE_VIEW":
                self.update_worker = WorkerUpdate()
                self.update_worker.moveToThread(self.DELETE_THREAD)
                
                self.DELETE_THREAD.started.connect(lambda: self.update_worker.executeUpdateQuery(
                    sql="UPDATE Productos SET eliminado = 1 WHERE IDproducto = ?",
                    params=del_params)
                    )
                self.update_worker.progress.connect(lambda value: self.__updateProgressBar(
                    tv_name=self.ui.tv_inventory_data.objectName(),
                    value=value)
                    )
                
                self.update_worker.finished.connect(lambda: self.__workerOnFinished(
                    tv_name=self.ui.tv_inventory_data.objectName(),
                    READ_OPERATION=False)
                    )
                self.update_worker.finished.connect(self.DELETE_THREAD.quit)
                self.DELETE_THREAD.finished.connect(self.update_worker.deleteLater)
            
            case "SALES_TABLE_VIEW":
                pass
                # self.delete_worker = WorkerDelete()
                # self.delete_worker.moveToThread(self.DELETE_THREAD)
                # self.DELETE_THREAD.started.connect(lambda: self.delete_worker.executeDeleteQuery(
                #     params=params,
                #     mult_sql=mult_sql))
                # self.delete_worker.progress.connect(lambda value: self.__updateProgressBar(
                #     tv_name=table_view.objectName(),
                #     value=value))
                # self.delete_worker.finished.connect(lambda: self.__workerOnFinished(
                #     tv_name=table_view.objectName(),
                #     READ_OPERATION=False) )
                # self.delete_worker.finished.connect(self.DELETE_THREAD.quit)
                # self.DELETE_THREAD.finished.connect(self.delete_worker.deleteLater)
            
            case "DEBTS_TABLE_VIEW":
                pass
            
        self.DELETE_THREAD.start()
        return None


    #¡ tablas (UPDATE)
    @Slot(int, int, object)
    def __onInventoryModelDataToUpdate(self, column:int, IDproduct:int,
                                       new_val:Any | list[str]) -> None:
        '''
        Actualiza la base de datos con el valor nuevo de Productos. En caso de 
        que las columnas sean de precio unitario o precio comercial también 
        actualiza el total adeudado en la tabla Deudas.
        
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
        var_loaded:bool = None # se usa al modificar en batches los precios, 
                               # flag que determina si se terminó de cargar 
                               # el acumulador
        
        match column:
            case 0: # categoría
                with self._db_repo as db_repo:
                    db_repo.updateRegisters(
                        upd_sql='''UPDATE Productos 
                                SET IDcategoria = (
                                    SELECT IDcategoria FROM Categorias 
                                    WHERE nombre_categoria = ?) 
                                WHERE IDproducto = ?;''',
                        upd_params=(new_val, IDproduct,)
                        )
            
            case 1: # nombre del producto
                with self._db_repo as db_repo:
                    db_repo.updateRegisters(
                        upd_sql='''UPDATE Productos 
                                SET nombre = ? 
                                WHERE IDproducto = ?;''',
                        upd_params=(new_val, IDproduct,)
                        )
            
            case 2: # descripción
                with self._db_repo as db_repo:
                    db_repo.updateRegisters(
                        upd_sql='''UPDATE Productos 
                                SET descripcion = ? 
                                WHERE IDproducto = ?;''',
                        upd_params=(new_val, IDproduct,)
                        )
            
            case 3: # stock
                with self._db_repo as db_repo:
                    db_repo.updateRegisters(
                        upd_sql='''UPDATE Productos 
                                SET stock = ?, unidad_medida = ? 
                                WHERE IDproducto = ?;''',
                        upd_params=(new_val[0], new_val[1], IDproduct,)
                        )
            
            case 4: # precio normal
                # si el sidebar de porcentajes está abierto se modifican porcentajes
                if not self.ui.inventory_side_bar_body.isHidden():
                    # actualiza contador de registros y acumulador
                    var_loaded = self.__updateInventoryPricesBatchVar(
                        price_type=InventoryPriceType.NORMAL,
                        IDproduct=IDproduct,
                        new_value=new_val)
                    
                    if var_loaded:
                        self.__resetInventoryUpdateVariables()
                        
                        # actualiza en Productos
                        with self._db_repo as db_repo:
                            db_repo.updateRegisters(
                                upd_sql='''UPDATE Productos 
                                        SET precio_unit = ? 
                                        WHERE IDproducto = ?;''',
                                upd_params=self._inv_model_data_acc,
                                executemany=True
                                )
                        
                        # actualiza en Deudas
                        self.__updateDebtsOnPriceChange(
                            price_type=InventoryPriceType.NORMAL,
                            executemany=True
                            )
                
                # se modifica un solo precio
                else:
                    # actualiza en Productos
                    with self._db_repo as db_repo:
                        db_repo.updateRegisters(
                            upd_sql='''UPDATE Productos
                                    SET precio_unit = ?
                                    WHERE IDproducto = ?;''',
                            upd_params=(new_val, IDproduct,),
                        )
                    
                    # actualiza en Deudas
                    self.__updateDebtsOnPriceChange(
                        price_type=InventoryPriceType.NORMAL,
                        params=(IDproduct,)
                    )
            
            case 5: # precio comercial
                # si el sidebar de porcentajes está abierto se modifican porcentajes
                if not self.ui.inventory_side_bar_body.isHidden():
                    var_loaded = self.__updateInventoryPricesBatchVar(
                        price_type=InventoryPriceType.COMERCIAL,
                        IDproduct=IDproduct,
                        new_value=new_val)
                    
                    if var_loaded:
                        self.__resetInventoryUpdateVariables()
                    
                        with self._db_repo as db_repo:
                            # actualiza en Productos
                            db_repo.updateRegisters(
                                upd_sql='''UPDATE Productos 
                                        SET precio_comerc = ? 
                                        WHERE IDproducto = ?;''',
                                upd_params=self._inv_model_data_acc,
                                executemany=True
                                )
                    
                        # actualiza en Deudas
                        self.__updateDebtsOnPriceChange(
                            price_type=InventoryPriceType.COMERCIAL,
                            executemany=True
                            )
                
                # modifica un solo precio
                else:
                    # actualiza en Productos
                    with self._db_repo as db_repo:
                        db_repo.updateRegisters(
                            upd_sql='''UPDATE Productos
                                    SET precio_comerc = ?
                                    WHERE IDproducto = ?;''',
                            upd_params=(new_val, IDproduct,),
                        )
                    
                    # actualiza en Deudas
                    self.__updateDebtsOnPriceChange(
                        price_type=InventoryPriceType.COMERCIAL,
                        params=(IDproduct,)
                    )
        
        return None


    def __updateInventoryPricesBatchVar(self, price_type:InventoryPriceType, IDproduct:int, new_value:float=None) -> bool:
        '''
        Actualiza el contador de registros 'self.__upd_reg_count' y el acumulador 
        de registros 'self._inv_model_data_acc' con los valores nuevos recibidos.
        Al terminar de llenarse el acumulador reinicia el contador.

        Parámetros
        ----------
        price_type : InventoryPriceType
            Tipo de precio al que se referencia. Admite NORMAL o COMERCIAL
        IDproduct : int
            ID del producto que hay que modificar
        new_value : float, opcional
            El nuevo valor del producto, por defecto None. Si es None es porque 
            el usuario no introdujo un nuevo valor COMERCIAL

        Retorna
        -------
        bool
            Cuando se termina de guardar los registros en la variable devuelve 
            True, sino devuelve False
        '''
        has_finished:bool = False
        
        if self.__upd_reg_count <= self._UPD_BATCH_SIZE - 1:
            # coloca el valor del precio nuevo
            match price_type:
                case InventoryPriceType.NORMAL:
                    self._inv_model_data_acc[self.__upd_reg_count, 0] = new_value
                
                case InventoryPriceType.COMERCIAL:
                    self._inv_model_data_acc[self.__upd_reg_count, 0] = new_value if new_value else 0
                
            # coloca el valor del IDproducto
            self._inv_model_data_acc[self.__upd_reg_count, 1] = IDproduct
            
            # actualiza el contador
            self.__upd_reg_count += 1

            # Si el contador llega al tamaño del batch, se reinicia
            if self.__upd_reg_count == self._UPD_BATCH_SIZE:
                self.__upd_reg_count = 0
                has_finished = True
        
        return has_finished

 
    def __updateDebtsOnPriceChange(self, price_type:InventoryPriceType, params:tuple[int]=None, executemany:bool=False) -> None:
        '''
        Actualiza el precio normal / comercial de un producto en Deudas cuando 
        se actualiza en la tabla Productos.

        Parámetros
        ----------
        price_type: InventoryPriceType
            El tipo de precio a cambiar en base de datos
        params: tuple[int], opcional
            Se usa cuando no se modifican los precios en porcentajes, recibe 
            una tupla con el IDproduct del producto
        executemany: bool, opcional
            Flag que determina si ejecutar una (False) o más veces (True) la 
            consulta update a la base de datos
        
        Retorna
        -------
        None
        '''
        match price_type.name:
            case "NORMAL":
                # actualiza en Deudas
                with self._db_repo as db_repo:
                    db_repo.updateRegisters(
                        upd_sql='''
                            UPDATE Deudas 
                            SET total_adeudado = CASE Detalle_Ventas.abonado
                                WHEN 0 THEN Productos.precio_unit
                                ELSE ROUND(Productos.precio_unit - Detalle_Ventas.abonado, 2)
                            END
                            FROM Detalle_Ventas, Ventas, Productos
                            WHERE 
                                Productos.IDproducto = ? AND
                                Detalle_Ventas.IDproducto = Productos.IDproducto AND
                                Deudas.IDdeuda = Detalle_Ventas.IDdeuda AND 
                                Detalle_Ventas.IDventa = Ventas.IDventa AND 
                                Ventas.detalles_venta LIKE "%(P. NORMAL)%";''',
                            upd_params=self._inv_model_data_acc[:, 1:] if not params else params,
                            executemany=executemany
                            )
        
            case "COMERCIAL":
                # actualiza en Deudas
                with self._db_repo as db_repo:
                    db_repo.updateRegisters(
                        upd_sql='''
                            UPDATE Deudas 
                            SET total_adeudado = CASE Detalle_Ventas.abonado
                                WHEN 0 THEN Productos.precio_comerc
                                ELSE ROUND(Productos.precio_comerc - Detalle_Ventas.abonado, 2)
                            END
                            FROM Detalle_Ventas, Ventas, Productos
                            WHERE 
                                Productos.IDproducto = ? AND
                                Detalle_Ventas.IDproducto = Productos.IDproducto AND
                                Deudas.IDdeuda = Detalle_Ventas.IDdeuda AND 
                                Detalle_Ventas.IDventa = Ventas.IDventa AND 
                                Ventas.detalles_venta LIKE "%(P. COMERCIAL)%";''',
                        upd_params=self._inv_model_data_acc[:, 1:] if not params else params,
                        executemany=executemany
                    )
        
        return None
    
    
    def __resetInventoryUpdateVariables(self) -> None:
        '''
        Reinicia el valor de las variables usadas durante la actualización a la 
        base de datos del modelo de datos de inventario.

        Retorna
        -------
        None
        '''
        self.__upd_reg_count = 0
        self._UPD_BATCH_SIZE = 0
        return None
    
    
    #! reimplementar método y luego borrar
    def __tableComboBoxOnCurrentTextChanged(self, table_view:QTableView, curr_index:QModelIndex, 
                                            combobox:QComboBox) -> None:
        new_unit:str | None # y el valor de la unidad ya seleccionado.
        quantity:float | int # cantidad seleccionada.

        match table_view.objectName():
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


    #! reimplementar método y luego borrar
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


    #! reimplementar método y luego borrar
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


    @Slot(object)
    def __onDelegateValidationSucceded(self, table_viewID:TableViewId) -> None:
        '''
        Esconde los labels de feedback relacionados con la VISTA a la que se 
        referencia.

        Parámetros
        ----------
        table_viewID : TableViewId
            QTableView al que se refencia

        Retorna
        -------
        None
        '''
        match table_viewID.name:
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


    #¡### INVENTARIO ##################################################
    # funciones de inventory_sideBar
    @Slot(QCheckBox)
    def handlePressedCheckbox(self, checkbox:QCheckBox) -> None:
        '''
        Alterna el estado de exclusividad del grupo de checkboxes, lo que 
        permite seleccionar/deseleccionar las checkboxes libremente, y se usa 
        en conjunto con 'handleClickedCheckbox'.
        
        Parámetros
        ----------
        checkbox: QCheckBox
            El checkbox al que se referencia
        
        Retorna
        -------
        None
        '''
        checkbox.group().setExclusive(not checkbox.isChecked())
        return None


    @Slot(QCheckBox)
    def handleClickedCheckbox(self, checkbox:QCheckBox) -> None:
        '''
        Alterna el estado de exclusividad del grupo de checkboxes, lo que 
        permite seleccionar/deseleccionar las checkboxes libremente, y se usa 
        en conjunto con 'handlePressedCheckbox'.
        
        Parámetros
        ----------
        checkbox: QCheckBox
            El checkbox al que se referencia
        
        Retorna
        -------
        None
        '''
        checkbox.group().setExclusive(True)


    @Slot()
    def handleCheckboxStateChange(self) -> None:
        '''
        Al checkear cualquier checkbox habilita el 'lineEdit_percentage_change', 
        sino lo deshabilita.
        
        Retorna
        -------
        None
        '''
        if (self.ui.checkbox_unit_prices.isChecked() or 
            self.ui.checkbox_comercial_prices.isChecked()):
            self.ui.lineEdit_percentage_change.setEnabled(True)
            
        else:
            self.ui.lineEdit_percentage_change.setEnabled(False)
        return None


    @Slot()
    def __onPercentageValidatorSucceded(self) -> None:
        '''
        Esconde el label de feedback de porcentajes.

        Retorna
        -------
        None
        '''
        self.ui.label_feedbackChangePercentage.hide()
        return None


    @Slot(str)
    def __onPercentageValidatorFailed(self, error_message:str) -> None:
        '''
        Muestra el label con feedback y cambia la hoja de estilos del label.
        
        Parámetros
        ----------
        feedback : str
            Texto como feedback a mostrar en el label
        
        Retorna
        -------
        None
        '''
        self.ui.label_feedbackChangePercentage.show()
        self.ui.label_feedbackChangePercentage.setText(error_message)
        self.ui.label_feedbackChangePercentage.setStyleSheet(LabelFeedbackStyle.INVALID.value)
        return None


    @Slot()
    def onLePercentageEditingFinished(self) -> None:
        ''' 
        A partir de las filas seleccionadas calcula los precios nuevos y 
        actualiza el modelo de datos, luego inicializa el acumulador de 
        datos.
        NOTA: la actualización de la base de datos se hace luego de la 
        actualización del modelo de datos, y no se hace en éste método, 
        se hace en 'self.__onInventoryModelDataToUpdate'.
        
        Retorna
        -------
        None
        '''
        new_values:tuple[float] # tuplas con los valores nuevos
        selected_rows:dict[int, list[QModelIndex, float]] # key=fila, value=lista[índice, nuevo valor]
        
        try:
            text:float = float(self.ui.lineEdit_percentage_change.text().replace(",","."))
        except ValueError:
            return None
        
        if text:
            selected_rows = getSelectedTableRows(
                tableView=self.ui.tv_inventory_data,
                indexes_in_col=4 if self.ui.checkbox_unit_prices.isChecked() else 5
                )
            
            if not selected_rows:
                return None
            
            # convierto a 'selected_rows' de -> 'dict[int, QModelIndex]'
            #                             a  -> 'dict[int, list[QModelIndex, float]]'
            selected_rows = {key:[idx,] for key, idx in selected_rows.items()}
            
            # obtiene los precios nuevos (tupla[precio nuevo])
            new_values = self.__calculateNewPrices(text, tuple(selected_rows.keys()))
            
            # agrega los precios nuevos a la lista del diccionario
            for i, (key, value) in enumerate(selected_rows.items()):
                value.append(new_values[i])
                
            # actualiza self._UPD_BATCH_SIZE con el total de registros a actualizar
            self._UPD_BATCH_SIZE = len(new_values)
            
            # reinicio y especifico dimensiones del acumulador
            self.setNpDataAccumulator(
                tv_name=self.ui.tv_inventory_data.objectName(),
                model_shape=(self._UPD_BATCH_SIZE, 2) # array[nuevo valor][IDproducto]
            )
            # paso al modelo los nuevos valores
            for (key, value) in selected_rows.items():
                self.ui.tv_inventory_data.model().setData(
                    index=value[0],
                    value=value[1])
            
        return None


    def __calculateNewPrices(self, percentage:float, 
                             selected_rows:tuple[int]) -> tuple[float]:
        '''
        Calcula los aumentos/decrementos en los precios unitarios o comerciales 
        dependiendo de cuál es la checkbox marcada y devuelve los precios nuevos.
        
        Parámetros
        ----------
        percentage : float
            Porcentaje de incremento/decremento
        selected_rows: tuple[int]
            Filas seleccionadas en la vista
        
        Retorna
        -------
        tuple[float]
            Tupla con tuplas internas con cada precio nuevo en formato float
        '''
        new_values:dict[int,float] = {}
        col_value:float # valor de la columna de precio (unitario o comercial)
        
        # si está activada la checkbox de precios unitarios...
        if self.ui.checkbox_unit_prices.isChecked():
            for row in selected_rows:
                # obtengo el precio unitario de cada celda
                col_value = float(self.ui.tv_inventory_data.model()._data[row][6])
                    
                # asigna el valor nuevo
                new_values[row] = round(col_value + (col_value * percentage / 100), 2)

        # sino, si está activada la checkbox de precios comerciales...
        else:
            for row in selected_rows:
                if self.ui.tv_inventory_data.model()._data[row][7]:
                    col_value = float(self.ui.tv_inventory_data.model()._data[row][7])
                   
                    # asigna el valor nuevo
                    new_values[row] = round(col_value + (col_value * percentage / 100), 2)
                
                else:
                    new_values[row] = 0.0
            
        return tuple(new_values.values())


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