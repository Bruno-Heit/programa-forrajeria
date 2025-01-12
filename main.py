import sys
from numpy import (empty, ndarray)
from typing import (Any, Iterable)

from PySide6.QtWidgets import (QApplication, QMainWindow, QLineEdit, QTableView, 
                               QCheckBox, QAbstractItemView, QDateTimeEdit, QListWidgetItem, 
                               QLabel)
from PySide6.QtCore import (QModelIndex, Qt, QThread, Slot)
from PySide6.QtGui import (QIcon)

from utils.classes import (ProductDialog, SaleDialog, ListItemWidget, ListItemValues, 
                           DebtorDataDialog, DebtsTablePersonData, WidgetStyle, ListItemFields)
from ui.ui_mainwindow import (Ui_MainWindow)
from utils.functionutils import *
from utils.model_classes import (InventoryTableModel, SalesTableModel)
from utils.delegates import (InventoryDelegate, SalesDelegate)
from utils.workerclasses import (WorkerSelect, WorkerUpdate, WorkerDelete)
from utils.dboperations import (DatabaseRepository)
from utils.customvalidators import (SalePaidValidator)
from utils.enumclasses import (LoggingMessage, DBQueries, ModelHeaders, TableViewId, 
                               LabelFeedbackStyle, InventoryPriceType, TypeSideBar, 
                               TableViewColumns)

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
        
        #* modelo de datos de Inventario
        self.inventory_data_model:InventoryTableModel = InventoryTableModel()
        self.ui.tv_inventory_data.setModel(self.inventory_data_model)
        
        #* modelo de datos de Ventas
        self.sales_data_model:SalesTableModel = SalesTableModel()
        self.ui.tv_sales_data.setModel(self.sales_data_model)
        
        #* delegado de inventario
        self.inventory_delegate = InventoryDelegate()
        self.ui.tv_inventory_data.setItemDelegate(self.inventory_delegate)
        
        #* delegado de ventas
        self.sales_delegate = SalesDelegate(self.ui.dateTimeEdit_sale.displayFormat())
        self.ui.tv_sales_data.setItemDelegate(self.sales_delegate)
        
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
        
        # en el formulario de Ventas coloca el tiempo en que se inició el programa
        self.ui.dateTimeEdit_sale.setDateTime(QDateTime.currentDateTime())
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
        #? Los acumuladores de datos sirven para hacer operaciones sobre los modelos de datos 
        #? y la base de datos en "batches" y mejorar el rendimiento de la aplicación en general
        self._inv_model_data_acc:ndarray[Any] = None #? acumulador temporal de datos para modelo de Inventario.
        self._UPD_BATCH_SIZE:int = None # al modificar precios en porcentajes, sirve para hacerlo en batches.
        self.__upd_reg_count:int = 0 # se usa con 'self._UPD_BATCH_SIZE' y 'self._inv_model_data_acc', 
                                        # cuenta por qué registro va pasando desde el modelo a MainWindow.
        
        #¡ ======== variables de ventas =======================================
        self._sales_model_data_acc:ndarray[Any] = None #? acumulador temp. de datos para modelo de Ventas.
        
        self.SALES_ITEM_NUM:int = 0 # contador para crear nombres de items en 
                                    # 'input_sales_data'.
        self.DICT_ITEMS_VALUES:dict[str, dict] = {} # tiene los valores de cada 'ListItemWidget'.
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
            table_viewID=TableViewId.INVEN_TABLE_VIEW,
            ACCESSED_BY_LIST=True,
            SHOW_ALL=True if item.text() == "MOSTRAR TODOS" else False
            )
        )
        self.ui.tables_ListWidget.itemActivated.connect(lambda item: self.fillTableView(
            table_viewID=TableViewId.INVEN_TABLE_VIEW,
            ACCESSED_BY_LIST=True,
            SHOW_ALL=True if item.text() == "MOSTRAR TODOS" else False
            )
        )

        #* (CREATE) añadir nuevo producto a tabla 'tv_inventory_data'
        self.ui.btn_add_product_inventory.clicked.connect(lambda: self.handleTableCreateRow(TableViewId.INVEN_TABLE_VIEW))
        
        #* (DELETE) eliminar un producto de 'tv_inventory_data'
        self.ui.btn_delete_product_inventory.clicked.connect(lambda: self.handleTableDeleteRows(TableViewId.INVEN_TABLE_VIEW))
        
        #* (UPDATE) modificar celdas de 'tv_inventory_data' (sin porcentajes)
        self.inventory_data_model.dataToUpdate.connect(
            lambda params: self.__onInventoryModelDataToUpdate(
                column=params[0], IDproduct=params[1], new_val=params[2]))
        
        #* delegado de inventario
        self.inventory_delegate.fieldIsValid.connect(self.__onDelegateValidationSucceded)
        self.inventory_delegate.fieldIsInvalid.connect(self.__onDelegateValidationFailed)
        
        #* inventory_sideBar
        self.ui.inventory_checkbuttons_buttonGroup.buttonPressed.connect(self.handlePressedCheckbox)
        self.ui.inventory_checkbuttons_buttonGroup.buttonClicked.connect(self.handleClickedCheckbox)
        
        self.ui.checkbox_unit_prices.stateChanged.connect(self.handleCheckboxStateChange)
        
        self.ui.checkbox_comercial_prices.stateChanged.connect(self.handleCheckboxStateChange)
        
        #* lineedit de porcentajes
        self.ui.lineEdit_percentage_change.editingFinished.connect(self.onLePercentageEditingFinished)
        self.ui.lineEdit_percentage_change.validator().validationSucceeded.connect(
            self.__onPercentageValidatorSucceded)
        self.ui.lineEdit_percentage_change.validator().validationFailed.connect(
            self.__onPercentageValidatorFailed)

        #¡========= VENTAS ====================================================
        #* (READ) cargar con ventas 'tv_sales_data'
        self.ui.tab2_toolBox.currentChanged.connect(lambda curr_index: self.fillTableView(
            table_viewID=TableViewId.SALES_TABLE_VIEW, SHOW_ALL=True) if curr_index == 1 else None)
        
        self.ui.tabWidget.currentChanged.connect(lambda index: self.ui.tab2_toolBox.setCurrentIndex(0) if index == 1 else None)
        
        #* (CREATE) añadir una venta a 'tv_sales_data'
        self.ui.btn_add_product_sales.clicked.connect(lambda: self.handleTableCreateRow(TableViewId.SALES_TABLE_VIEW))
        
        #* (DELETE) eliminar ventas de 'tv_sales_data'
        self.ui.btn_delete_product_sales.clicked.connect(lambda: self.handleTableDeleteRows(TableViewId.SALES_TABLE_VIEW))
        
        #* (UPDATE) modificar celdas de 'tv_sales_data'
        self.sales_data_model.dataToUpdate.connect(
            lambda params: self.__onSalesModelDataToUpdate(
                column=params['column'],
                IDsales_detail=params['IDsales_detail'],
                new_val=params['new_value'],
                quantity_index=params['quantity_index'] if 'quantity_index' in params else None
            )
        )
        
        #* delegado de ventas
        self.sales_delegate.fieldIsValid.connect(self.__onDelegateValidationSucceded)
        self.sales_delegate.fieldIsInvalid.connect(self.__onDelegateValidationFailed)
        
        #* formulario de ventas
        self.ui.btn_add_product.clicked.connect(self.addSalesInputListItem)
        
        self.ui.lineEdit_paid.editingFinished.connect(self.onSalePaidEditingFinished)
        
        self.ui.btn_end_sale.clicked.connect(self.onFinishedSale)

        #¡========= DEUDAS ====================================================
        # TODO PRINCIPAL: SEGUIR CON PARTE DE DEUDAS
        #* (READ) cargar con deudas 'tv_debts_data'
        self.ui.tabWidget.currentChanged.connect(lambda curr_index: self.fillTableView(
            table_viewID=TableViewId.DEBTS_TABLE_VIEW, SHOW_ALL=True) if curr_index == 2 else None)
        
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
        self.ui.label_feedbackDebts.hide()
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
    def setNpDataAccumulator(self, table_viewID:TableViewId,
                            model_shape:tuple[int, int]) -> None:
        '''
        Dependiendo de la VISTA usada, crea un 'numpy.ndarray' vacío con 
        las dimensiones especificadas.

        Parámetros
        ----------
        table_viewID : TableViewId
            el QTableView al que se referencia
        model_shape: tuple[int, int]
            Tupla con las dimensiones del arreglo

        Retorna
        -------
        None
        '''
        match table_viewID.name:
            case "INVEN_TABLE_VIEW": # Productos
                self._inv_model_data_acc = empty(
                    shape=model_shape,
                    dtype=object)
            
            case "SALES_TABLE_VIEW": # Ventas
                self._sales_model_data_acc = empty(
                    shape=model_shape,
                    dtype=object)
            
            case "DEBTS_TABLE_VIEW": # Ctas. Ctes.
                ...
        return None


    #¡ tablas (READ)
    @Slot(QTableView, bool, bool)
    def fillTableView(self, table_viewID:TableViewId, ACCESSED_BY_LIST:bool=False, SHOW_ALL:bool=False) -> None:
        '''
        Este método hace lo siguiente:
        - Limpia las variables de IDs asociadas con el QTableView.
        - Dependiendo del QTableView que se tenga que llenar, declara las consultas SELECT.
        - Instancia e inicializa un QThread y un worker para llenar el modelo de datos asociado 
        al QTableView.

        Parámetros
        ----------
        table_viewID : TableViewId
            QTableView que se referencia
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
        
        # crea las consultas para obtener el COUNT() de filas y los registros 
        # para llenar la tabla
        match table_viewID.name:
            case "INVEN_TABLE_VIEW":
                # si se seleccionó una categoría desde 'tables_ListWidget', cambia 
                # hacia la pestaña de inventario...
                if ACCESSED_BY_LIST:
                    self.ui.tabWidget.setCurrentWidget(
                        self.ui.tabWidget.findChild(QWidget, "tab1_inventory"))
                count_sql, data_sql = getTableViewsSqlQueries(
                    table_viewID=TableViewId.INVEN_TABLE_VIEW,
                    ACCESSED_BY_LIST=ACCESSED_BY_LIST,
                    SHOW_ALL=SHOW_ALL)
                
                if not SHOW_ALL and ACCESSED_BY_LIST:
                    count_params = (self.ui.tables_ListWidget.currentItem().text(),)
                    data_params = (self.ui.tables_ListWidget.currentItem().text(),)
                self.ui.label_feedbackInventory.hide()


            case "SALES_TABLE_VIEW":
                count_sql, data_sql = getTableViewsSqlQueries(
                    table_viewID=TableViewId.SALES_TABLE_VIEW
                )
                self.ui.label_feedbackSales.hide()


            case "DEBTS_TABLE_VIEW":
                # TODO: declarar consultas sql para también traer los datos necesarios
                ...
        
        self.__instanciateSelectWorkerAndThread(
            table_viewID=table_viewID,
            data_sql=data_sql,
            data_params=data_params,
            count_sql=count_sql,
            count_params=count_params
        )
        return None
    
    
    def __instanciateSelectWorkerAndThread(self, table_viewID:QTableView, data_sql:str, 
                                           data_params:tuple=..., count_sql:str=..., 
                                           count_params:tuple=...) -> None:
        '''
        Inicializa un QThread y un worker para realizar un tipo de consultas a la base de 
        datos de forma asíncrona, conecta sus señales y slots.

        Parámetros
        ----------
        table_viewID: TableViewId
            QTableView asociado al modelo de datos y QProgressBar que hay que actualizar.
        data_sql: str
            Consulta de tipo SELECT
        data_params: tuple, opcional
            Parámetros de la consulta SELECT
        count_sql: str, opcional
            Consulta de tipo SELECT COUNT() para obtener la cantidad de registros coincidentes
        count_params: tuple, opcional
            Parámetros de la consulta SELECT COUNT()

        Retorna
        -------
        None
        '''
        self.select_thread = QThread()
        self.select_worker = WorkerSelect()
        
        self.select_worker.moveToThread(self.select_thread)
        
        self.select_thread.started.connect(
            lambda: self.select_worker.executeReadQuery(
                data_sql=data_sql, data_params=data_params,
                count_sql=count_sql, count_params=count_params
            )
        )
        self.select_worker.countFinished.connect(
            lambda model_shape: self.__workerOnCountFinished(
                table_viewID=table_viewID,
                model_shape=model_shape
            )
        )
        self.select_worker.registerProgress.connect(
            lambda register: self.__workerOnRegisterProgress(
                register=register,
                table_viewID=table_viewID
            )
        )
        self.select_worker.finished.connect(
            lambda: self.__workerOnFinished(table_viewID=table_viewID)
        )
        self.select_worker.finished.connect(self.select_thread.quit)
        self.select_worker.finished.connect(self.select_worker.deleteLater)
        
        self.select_thread.start()
        
        return None
    
    
    @Slot()
    def __workerOnCountFinished(self, table_viewID:TableViewId, model_shape:tuple[int, int]=None) -> None:
        '''
        Instancia un acumulador numpy.array para los datos del modelo, y actualiza el estado 
        del QProgressBar asociado al QTableView.

        Parámetros
        ----------
        table_viewID: TableViewID
            QTableView que se referencia
        model_shape: tuple[int, int]
            Dimensiones del modelo de datos, se usa para instanciar el acumulador

        Retorna
        -------
        None
        '''
        self.setNpDataAccumulator(
            table_viewID=table_viewID,
            model_shape=model_shape
        )
        
        self.__updateProgressBar(
            table_viewID=table_viewID,
            max_val=model_shape[0]
        )
        return None
    
    
    @Slot(tuple, QTableView)
    def __workerOnRegisterProgress(self, register:tuple[Any], table_viewID:TableViewId) -> None:
        '''
        A medida que se progresa con los registros leídos guarda los IDs necesarios de cada registro, 
        acumula los registros en una variable y actualiza la QProgressBar asociada a ese QTableView.

        Parámetros
        ----------
        register : tuple[Any]
            El registro obtenido de la consulta SELECT, la posición [0] debe contener el progreso 
            de lectura de registros
        table_viewID : TableViewID
            QTableView al que se referencia
        
        Retorna
        -------
        None
        '''
        match table_viewID.name:
            case "INVEN_TABLE_VIEW":
                # actualiza la barra de progeso
                self.__updateProgressBar(
                    table_viewID=table_viewID,
                    max_val=None,
                    value=register[0]
                )

                # guarda en la posición actual el registro completo
                self._inv_model_data_acc[register[0]] = register[1]
            
            case "SALES_TABLE_VIEW":
                # actualiza la barra de progeso
                self.__updateProgressBar(
                    table_viewID=table_viewID,
                    max_val=None,
                    value=register[0]
                )
                
                # guarda en la posición actual el registro completo
                self._sales_model_data_acc[register[0]] = register[1]
            
            case "DEBTS_TABLE_VIEW":
                ...
        
        
        return None
    
    
    def __updateProgressBar(self, table_viewID:TableViewId, max_val:int=None, value:int=None) -> None:
        '''
        Actualiza el estado del QProgressBar correspondiente dependiendo del QTableView asociado.

        Parámetros
        ----------
        table_viewID: TableViewID
            Nombre del QTableView al cual está asociado el QProgressBar a actualizar
        max_val: int, opcional
            Valor máximo del QProgressBar, por defecto es None
        value: int, opcional
            Valor actual del QProgressBar, por defecto es None

        Retorna
        -------
        None
        '''
        match table_viewID.name:
            case "INVEN_TABLE_VIEW":
                self.ui.inventory_progressbar.show() if self.ui.inventory_progressbar.isHidden() else None
                self.ui.inventory_progressbar.setMaximum(max_val) if max_val is not None and self.ui.inventory_progressbar.maximum() != max_val else None
                self.ui.inventory_progressbar.setValue(value + 1) if value else None
            
            case "SALES_TABLE_VIEW":
                self.ui.sales_progressbar.show() if self.ui.sales_progressbar.isHidden() else None
                self.ui.sales_progressbar.setMaximum(max_val) if max_val is not None and self.ui.sales_progressbar.maximum() != max_val else None
                self.ui.sales_progressbar.setValue(value + 1) if value else None
                
            case "DEBTS_TABLE_VIEW":
                self.ui.debts_progressbar.show() if self.ui.debts_progressbar.isHidden() else None
                self.ui.debts_progressbar.setMaximum(max_val) if max_val is not None and self.ui.debts_progressbar.maximum() != max_val else None
                self.ui.debts_progressbar.setValue(value + 1) if value else None
        return None
    
    
    @Slot(str)
    def __workerOnFinished(self, table_viewID:TableViewId, READ_OPERATION:bool=True) -> None:
        '''
        Esconde la QProgressBar relacionada con el QTableView, reinicia el valor del 
        QSS de dicha QProgressBar y carga los datos en el QTableView, luego reinicia 
        los acumuladores temporales.
        
        Parámetros
        ----------
        tv_name : TableViewID
            QTableView al que se referencia
        READ_OPERATION : bool, opcional
            determina si la operación a base de datos es de lectura, sino no reinicia 
            el contenido de la tabla

        Retorna
        -------
        None
        '''
        match table_viewID.name:
            case "INVEN_TABLE_VIEW":
                self.ui.inventory_progressbar.setStyleSheet("")
                self.ui.inventory_progressbar.hide()
                
                if READ_OPERATION:
                    self.inventory_data_model.setModelData(
                        data=self._inv_model_data_acc,
                        headers=ModelHeaders.INVENTORY_HEADERS.value)
            
                # borra el acumulador temporal de datos
                self._inv_model_data_acc = None

                
            case "SALES_TABLE_VIEW":
                self.ui.sales_progressbar.setStyleSheet("")
                self.ui.sales_progressbar.hide()
                
                if READ_OPERATION:
                    self.sales_data_model.setModelData(
                        data=self._sales_model_data_acc,
                        headers=ModelHeaders.SALES_HEADERS.value)
                
                # borra el acumulador temp. de datos
                self._sales_model_data_acc = None
                
            case "DEBTS_TABLE_VIEW":
                self.ui.debts_progressbar.setStyleSheet("")
                self.ui.debts_progressbar.hide()
                ...
            
        logging.debug(LoggingMessage.WORKER_SUCCESS)
        return None


    #¡ tablas (CREATE)
    @Slot(str)
    def handleTableCreateRow(self, table_viewID:TableViewId) -> None:
        '''
        Dependiendo del QTableView al que se agregue una fila, se encarga de 
        crear una instancia del QDialog correspondiente que pide los datos 
        necesarios para la nueva fila, y si tienen señales conecta sus señales.
        
        Parámetros
        ----------
        table_viewID: TableViewId
            El QTableView al que se referencia
        
        Retorna
        -------
        None
        '''
        match table_viewID.name:
            case "INVEN_TABLE_VIEW":
                productDialog = ProductDialog() # QDialog para añadir un producto nuevo a 'tv_inventory_data'
                productDialog.setAttribute(Qt.WA_DeleteOnClose, True) # destruye el dialog cuando se cierra
                
                # conecta señal para actualizar el MODELO de inventario
                productDialog.dataFilled.connect(
                    lambda data_to_insert: self.insertDataIntoModel(
                        table_viewID=TableViewId.INVEN_TABLE_VIEW,
                        data_to_insert=data_to_insert
                    )
                )
                
                productDialog.exec()

            case "SALES_TABLE_VIEW":
                saleDialog = SaleDialog() # QDialog para añadir una venta nueva a 'tv_sales_data' (y posiblemente, una
                                          # deuda a 'tv_debts_data')
                saleDialog.setAttribute(Qt.WA_DeleteOnClose, True)
                
                # conecta señal para actualizar el MODELO de ventas
                saleDialog.dataFilled.connect(
                    lambda data_to_insert: self.insertDataIntoModel(
                        table_viewID=TableViewId.SALES_TABLE_VIEW,
                        data_to_insert=data_to_insert
                    )
                )
                
                saleDialog.exec()
            
            case "DEBTS_TABLE_VIEW":
                ...
        
        return None


    @Slot(object, dict)
    def insertDataIntoModel(self, table_viewID:TableViewId, data_to_insert:dict[Any]) -> None:
        '''
        Cuando se terminen de llenar los datos en el QDialog correspondiente, 
        éste método recibe los datos y actualiza el MODELO DE DATOS respectivo.

        Parámetros
        ----------
        table_viewID : TableViewId
            QTableView al que se refencia
        data_to_insert : dict[Any]
            datos con los que actualizar el MODELO DE DATOS correspondiente

        Retorna
        -------
        None
        '''
        match table_viewID.name:
            case 'INVEN_TABLE_VIEW':
                self.inventory_data_model.insertRows(
                    row=self.inventory_data_model.rowCount(),
                    count=1,
                    data_to_insert=data_to_insert)
            
            case 'SALES_TABLE_VIEW':
                self.__updateStockOnSaleCreation(data_to_insert=data_to_insert)
                
                # le paso los datos al modelo, excepto el flag 'THERE_IS_DEBT', 
                # porque el modelo no lo necesita
                self.sales_data_model.insertRows(
                    row=self.inventory_data_model.rowCount(),
                    count=1,
                    data_to_insert={key: value for key, value in data_to_insert.items() if 'THERE_IS_DEBT' not in key}
                )
                
                # si hay deuda también actualiza el MODELO de deudas
                if data_to_insert['THERE_IS_DEBT']:
                    ...
            
            case 'DEBTS_TABLE_VIEW':
                ...
        
        return None
    
    
    def __updateStockOnSaleCreation(self, data_to_insert:dict[Any]) -> None:
        '''
        Actualiza el stock en el MODELO de inventario cuando se agrega una nueva 
        venta al MODELO de ventas.

        Parámetros
        ----------
        data_to_insert : dict[Any]
            datos con los que actualizar el MODELO DE DATOS correspondiente

        Retorna
        -------
        None
        '''
        found_index_row:int = None
        target_index:QModelIndex
        curr_stock:str|float
        measurement_unit:str
        new_value:float
        
        # si el modelo no está vacío...
        if self.inventory_data_model.modelHasData():
            # obtengo el índice donde modificar el stock
            found_index_row = self.inventory_data_model.match(
                self.inventory_data_model.index(0, TableViewColumns.INV_PRODUCT_NAME.value), # busca desde la 1ra fila, 2da columna (de nombre).
                Qt.ItemDataRole.DisplayRole.value,          # devuelve la coincidencia como texto.
                data_to_insert['product_name'],             # el dato a buscar.
                1,                                          # cantidad de coincidencias para que deje de buscar.
                Qt.MatchFlag.MatchExactly                   # determina el criterio de búsqueda (debe ser exacto el string).
            )[0].row()                                      # obtengo del elemento [0] sólo el valor de la fila.
            
            if found_index_row is not None:
                # obtiene el stock en esa fila
                target_index = self.inventory_data_model.index(
                    found_index_row,
                    TableViewColumns.INV_STOCK.value
                )
                curr_stock, measurement_unit = target_index.data(Qt.ItemDataRole.DisplayRole).split(" ", 1)
                
                # resta al stock anterior la cantidad introducida
                try:
                    new_value = round(
                        float(curr_stock.replace(",",".").strip()) - float(data_to_insert["product_quantity"]),
                        2)
                    new_value = f"{new_value} {measurement_unit}"
                
                    self.inventory_data_model.setData(target_index, new_value, Qt.ItemDataRole.EditRole)
                
                except:
                    pass
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
                self.__deleteSalesRows()

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
        
        # # instancia y ejecuta WORKER y THREAD
        self.__instanciateDeleteWorkerAndThread(table_viewID, params_ids)
        
        return None


    def __deleteSalesRows(self, table_viewID:TableViewId=TableViewId.SALES_TABLE_VIEW) -> None:
        '''
        Elimina los productos seleccionados en el MODELO de ventas, actualiza 
        la VISTA y marca las deudas (si hay) en la base de datos como eliminadas.

        Parámetros
        ----------
        table_viewID : TableViewId, opcional
            QTableView al que se refencia

        Retorna
        -------
        None
        '''
        # obtiene las filas seleccionadas
        selected_rows = getSelectedTableRows(self.ui.tv_sales_data)
        
        if not selected_rows:
            return None
        
        # cambia la progress-bar para representar las eliminaciones
        self.ui.sales_progressbar.setMaximum(len(selected_rows))
        self.ui.sales_progressbar.setStyleSheet(
            '''QProgressBar::chunk {
                background-color: qlineargradient(spread:reflect, x1:0.119, y1:0.426, 
                    x2:0.712045, y2:0.926, stop:0.0451977 rgba(255, 84, 87, 255), 
                    stop:0.59887 rgba(255, 161, 71, 255));
                }''')
        
        # # obtiene ids de las filas seleccionadas
        params_ids = self.__getDeleteData(table_viewID, selected_rows)
        
        # actualiza el modelo de ventas
        self.sales_data_model.removeSelectedModelRows(selected_rows)
        
        # instancia y ejecuta WORKER y THREAD
        self.__instanciateDeleteWorkerAndThread(table_viewID, params_ids)
        
        return None


    def __getDeleteData(self, table_viewID:TableViewId, selected_rows:Iterable) -> Iterable[tuple | dict]:
        '''
        Obtiene los datos necesarios desde el MODELO de datos de la VISTA especifica 
        para poder realizar las consultas.

        Parámetros
        ----------
        table_viewID : TableViewId
            QTableView al que se refencia
        selected_rows : Iterable
            las filas seleccionadas en la vista

        Retorna
        -------
        Iterable[tuple | dict]
            iterable con los datos necesarios para las consultas
        '''
        data:list[Any] | dict[list] = []
        id_sales:list[Any] # tiene los IDventa.
        id_debts:list[Any] # tiene los IDdeuda.
        _placeholders:str # tiene los placeholders (?) necesarios para obtener los IDventa | IDdeuda en la consulta sql.
        
        match table_viewID.name:
            case "INVEN_TABLE_VIEW":
                # obtiene los IDs de los productos y los convierte en tuple[ID]
                for row in selected_rows:
                    data.append( (self.inventory_data_model._data[row][0],) )
                data = tuple(data)
            
            case "SALES_TABLE_VIEW":
                # obtiene los IDs de detalle de venta y los convierte en tuple[ID]
                for row in selected_rows:
                    data.append(self.sales_data_model._data[row][0])
                
                with self._db_repo as db_repo:
                    # obtiene los IDs de ventas
                    _placeholders = ','.join(['?'] * len(data)) # crea una cadena de '?,?,?...' largo como la cantidad de ids
                    
                    id_sales = db_repo.selectRegisters(
                        data_sql=f'''SELECT DISTINCT v.IDventa 
                                     FROM Ventas AS v 
                                     INNER JOIN Detalle_Ventas AS dv ON dv.IDventa = v.IDventa 
                                     WHERE dv.ID_detalle_venta IN ({_placeholders});''',
                        data_params=data
                    )
                    id_sales = [id_debt[0] for id_debt in id_sales]
                    
                    # obtiene los IDs de deudas
                    id_debts = db_repo.selectRegisters(
                        data_sql=f'''SELECT DISTINCT d.IDdeuda 
                                     FROM Deudas AS d 
                                     INNER JOIN Detalle_Ventas AS dv ON dv.IDdeuda = d.IDdeuda 
                                     WHERE dv.ID_detalle_venta IN ({_placeholders});''',
                        data_params=data
                    )
                    id_debts = [id_debt[0] for id_debt in id_debts]
                    
                    # convierte data a un dict[lista de ids]
                    data = {
                        "ID_sales_detail": data,
                        "IDsales": id_sales,
                        "IDdebts": id_debts
                    }
            
            case "DEBTS_TABLE_VIEW":
                pass
        
        return data


    def __instanciateDeleteWorkerAndThread(self, table_viewID:TableViewId, del_params:Iterable[tuple]) -> None:
        '''
        Dependiendo de la VISTA, instancia y ejecuta un WORKER y un QTHREAD para realizar 
        las consultas de eliminación a la base de datos y conecta sus señales.

        Parámetros
        ----------
        table_viewID : TableViewId
            QTableView al que se refencia
        del_params: Iterable[tuple]
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
                    table_viewID=table_viewID,
                    value=value)
                )
                
                self.update_worker.finished.connect(lambda: self.__workerOnFinished(
                    table_viewID=TableViewId.INVEN_TABLE_VIEW,
                    READ_OPERATION=False)
                )
                self.update_worker.finished.connect(self.DELETE_THREAD.quit)
                self.DELETE_THREAD.finished.connect(self.update_worker.deleteLater)
            
            case "SALES_TABLE_VIEW":
                # borra registros de Ventas y Detalle_Ventas
                mult_sql:tuple[str] = (
                    '''DELETE FROM Detalle_Ventas 
                       WHERE ID_detalle_venta = ?;''',
                    '''DELETE FROM Ventas 
                       WHERE IDventa = ?;''',
                    '''UPDATE Deudas 
                       SET eliminado = 1 
                       WHERE IDdeuda = ?;'''
                    )
                self.delete_worker = WorkerDelete()
                self.delete_worker.moveToThread(self.DELETE_THREAD)
                
                self.DELETE_THREAD.started.connect(lambda: self.delete_worker.executeDeleteQuery(
                    mult_sql=mult_sql,
                    params=del_params,
                    table_viewID=TableViewId.SALES_TABLE_VIEW)
                )
                self.delete_worker.progress.connect(lambda value: self.__updateProgressBar(
                    table_viewID=table_viewID,
                    value=value)
                )
                self.delete_worker.finished.connect(lambda: self.__workerOnFinished(
                    table_viewID=table_viewID,
                    READ_OPERATION=False) )
                
                self.delete_worker.finished.connect(self.DELETE_THREAD.quit)
                self.DELETE_THREAD.finished.connect(self.delete_worker.deleteLater)
            
            case "DEBTS_TABLE_VIEW":
                pass
            
        self.DELETE_THREAD.start()
        return None


    #¡ tablas (UPDATE)
    #¡¡ ....... inventario ........................................................................
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
    
    
    #¡¡ ....... ventas ............................................................................
    @Slot(int, int, object)
    def __onSalesModelDataToUpdate(self, column:int, IDsales_detail:int,
                                       new_val:Any, quantity_index:QModelIndex = None) -> None:
        '''
        Actualiza la base de datos con el valor nuevo de la sección de Ventas. 
        Además, en caso de que la columna modificada sea la de "producto" 
        actualiza el modelo para mostrar la unidad de medida de ese producto 
        seleccionado, y si la columna modifica es la de "fecha y hora" actualiza 
        el nuevo horario tanto en la tabla "Ventas" como en "Deudas".
        
        Parámetros
        ----------
        column : int
            Columna del item modificado
        IDsales_detail : int
            IDproducto en la base de datos del item modificado
        new_val : Any
            Valor nuevo del item
        quantity_index : QModelIndex, opcional
            índice de la columna "cantidad" en la misma fila que el producto 
            modificado, sólo se usa cuando el registro modificado es parte 
            de la columna "producto"
        
        Retorna
        -------
        None
        '''
        match column:
            case 0: # detalle de ventas
                with self._db_repo as db_repo:
                    db_repo.updateRegisters(
                        upd_sql='''UPDATE Ventas 
                                   SET detalles_venta = ? 
                                   WHERE IDventa = (
                                       SELECT IDventa 
                                       FROM Detalle_Ventas 
                                       WHERE ID_detalle_venta = ?);''',
                        upd_params=(new_val, IDsales_detail,)
                        )
            
            case 1: # cantidad (+ unidad de medida)
                with self._db_repo as db_repo:
                    db_repo.updateRegisters(
                        upd_sql='''UPDATE Detalle_Ventas 
                                   SET cantidad = ? 
                                   WHERE ID_detalle_venta = ?;''',
                        upd_params=(new_val, IDsales_detail,)
                        )
            
            case 2: # producto
                with self._db_repo as db_repo:
                    db_repo.updateRegisters(
                        upd_sql='''UPDATE Detalle_Ventas 
                                   SET IDproducto = (
                                       SELECT IDproducto 
                                       FROM Productos 
                                       WHERE nombre = ?) 
                                   WHERE ID_detalle_venta = ?;''',
                        upd_params=(new_val, IDsales_detail,)
                        )
                
                    # actualiza el modelo con la nueva unidad de medida del nuevo producto elegido
                    self.sales_data_model.updateMeasurementUnit(
                        quantity_index=quantity_index,
                        new_value=self._db_repo.selectRegisters(
                            data_sql='''SELECT unidad_medida 
                                        FROM Productos 
                                        WHERE nombre = ?;''',
                            data_params=(self.sales_data_model._data[quantity_index.row(), 4],)
                            )[0][0]
                    )
                
            case 3: # costo total
                with self._db_repo as db_repo:
                    db_repo.updateRegisters(
                        upd_sql='''UPDATE Detalle_Ventas 
                                   SET costo_total = ? 
                                   WHERE ID_detalle_venta = ?;''',
                        upd_params=(new_val, IDsales_detail)
                    )
            
            case 4: # abonado
                with self._db_repo as db_repo:
                    db_repo.updateRegisters(
                        upd_sql='''UPDATE Detalle_Ventas 
                                   SET abonado = ? 
                                   WHERE ID_detalle_venta = ?;''',
                        upd_params=(new_val, IDsales_detail)
                    )
            
            case 5: # fecha y hora
                with self._db_repo as db_repo:
                    db_repo.updateRegisters(
                        upd_sql='''UPDATE Ventas 
                                   SET fecha_hora = ? 
                                   WHERE IDventa = (
                                       SELECT IDventa 
                                       FROM Detalle_Ventas 
                                       WHERE ID_detalle_venta = ?);''',
                        upd_params=(new_val, IDsales_detail)
                    )
                    
                    db_repo.updateRegisters(
                        upd_sql='''UPDATE Deudas 
                                   SET fecha_hora = ? 
                                   WHERE IDdeuda = (
                                       SELECT IDdeuda 
                                       FROM Detalle_Ventas 
                                       WHERE ID_detalle_venta = ?);''',
                        upd_params=(new_val, IDsales_detail)
                    )
        
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
                table_viewID=TableViewId.INVEN_TABLE_VIEW,
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
    #* métodos de lineEdit_paid
    @Slot()
    def onSalePaidEditingFinished(self) -> None:
        '''
        Formatea el campo del 'lineEdit_paid' y muestra el cambio a devolver.
        
        Retorna
        -------
        None
        '''
        # formatea el campo
        field_text:str = self.ui.lineEdit_paid.text()
        
        field_text = field_text.replace(".",",")
        field_text = field_text.strip()
        field_text = field_text.rstrip(",")
        field_text = field_text.lstrip("0")
        
        self.ui.lineEdit_paid.setText(field_text)
        
        # muestra el cambio
        self.__setSaleChange()
        return None


    def __setSaleChange(self) -> None:
        '''
        Si todos los valores de los items son válidos, muestra el cambio a 
        devolver a partir del valor de 'lineEdit_paid', o si lo abonado es 
        mayor al total se muestra el cambio que se debe dar en 'label_total_change'.
        
        Retorna None.
        '''
        total_paid:float

        # si self.TOTAL_COST es None significa que hay items con valores inválidos
        if not self.TOTAL_COST:
            return None
        
        # si no hay un valor en lineEdit_paid, le pone 0
        if not self.ui.lineEdit_paid.text():
            self.ui.lineEdit_paid.setText(f"0.0")
        
        # obtiene el total abonado
        total_paid = float(self.ui.lineEdit_paid.text().replace(",","."))

        # si 'self.lineEdit_paid' tiene un valor mayor al total muestra el cambio
        if total_paid > self.TOTAL_COST:
            self.ui.label_total_change.setText(f"{round(total_paid - self.TOTAL_COST, 2)}")

        else:
            self.ui.label_total_change.setText("")
            
        return None
    

    @Slot()
    def onPaidValidationSucceded(self) -> None:
        '''
        Cambia el estilo de 'lineEdit_paid' para representar la validez del 
        campo y el valor de la variable 'self.VALID_PAID_FIELD' a True.
        
        Retorna
        -------
        None
        '''
        # si el campo es válido y no está vacío lo pone de color verde, 
        # si está vacío le quita el estilo
        self.ui.lineEdit_paid.setStyleSheet(
            WidgetStyle.FIELD_VALID_VAL.value if self.ui.lineEdit_paid.text().strip() else ""
        )
        self.VALID_PAID_FIELD = True
        
        return None
    
    
    @Slot()
    def onPaidValidationFailed(self) -> None:
        '''
        Cambia el estilo de 'lineEdit_paid' para representar la invalidez 
        del campo y el valor de la variable 'self.VALID_PAID_FIELD' a False.
        
        Retorna
        -------
        None
        '''
        self.ui.lineEdit_paid.setStyleSheet(
            WidgetStyle.FIELD_INVALID_VAL.value
        )
        self.VALID_PAID_FIELD = False
        
        return None
    
    
    #* métodos de widgets de items de lista
    @Slot()
    def addSalesInputListItem(self) -> None:
        '''
        Crea un item de tipo 'classes.ListItemWidget' que se colocará dentro 
        de 'sales_input_list', y que representa la venta de un producto, y 
        conecta sus señales.
        
        Retorna
        -------
        None
        '''
        object_name:str = f"item_{self.SALES_ITEM_NUM}"
        list_widget_item:QListWidgetItem = QListWidgetItem()
        item:ListItemWidget = ListItemWidget(obj_name=object_name)

        # incremento self.SALES_ITEM_NUM
        self.SALES_ITEM_NUM += 1
        
        #? agrego un elemento vacío a self.DICT_ITEMS_VALUES para evitar falsos 
        #? positivos y activar el botón 'btn_end_sale' sin querer cuando un 
        #? elemento es válido y hay otros que no fueron modificados aún... de 
        #? cualquier forma, este item temporal va a ser sobreescrito cuando se 
        #? modifique/borre el item
        self.DICT_ITEMS_VALUES[object_name] = {}
        
        # conecto señales
        item.deleteItem.connect(
            lambda list_item_name: self.onSalesItemDeletion(
                list_widget_item=list_widget_item,
                list_item_name=list_item_name
            )
        )
        item.fieldsValuesChanged.connect(
            lambda values: self.onSalesItemFieldsValuesChanged(
                values=values,
                object_name=object_name
            )
        )

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
    
    
    @Slot(QListWidgetItem, str)
    def onSalesItemDeletion(self, list_widget_item:QListWidgetItem, list_item_name:str) -> None:
        '''
        Elimina el item elegido de 'self.sales_input_list', actualiza la variable 
        'self.DICT_ITEMS_VALUES', y llama al método 'self.validateSalesItemsFields' 
        para validar los otros items.
        
        Parámetros
        ----------
        item_list_widget : QListWidgetItem
            el QListWidgetItem al que se referencia
        list_item_name : str
            el 'objectName' del objecto 'classes.ListItemWidget' interno de 
            'item_list_widget', funciona como id único
        
        Retorna
        -------
        None
        '''
        # quita el item a partir de la fila donde está
        self.ui.sales_input_list.takeItem(
            self.ui.sales_input_list.row(list_widget_item)
        )
        
        # actualiza el valor de la variable
        self.DICT_ITEMS_VALUES.pop(list_item_name)
            
        # reinicia el contador de nombres cuando no hay items en 'sales_input_list', 
        # y desactiva 'btn_end_sale'
        if self.ui.sales_input_list.count() == 0:
            self.SALES_ITEM_NUM = 0
            self.ui.btn_end_sale.setEnabled(False)
        
        # valida los campos
        self.validateSalesItemsFields()
        return None
    
    
    @Slot(object)
    def onSalesItemFieldsValuesChanged(self, values:dict[str, Any], object_name:str) -> None:
        '''
        Al cambiar los valores actualiza el registro de los valores en 
        'MainWindow' y valida que todos los demás sean válidos para poder 
        mostrar el total de la venta.

        Parámetros
        ----------
        values : dict[str, Any]
            valores actuales del 'ListItemWidget'
        object_name : str
            nombre del 'ListItemWidget'

        Retorna
        -------
        None
        '''
        self.DICT_ITEMS_VALUES[object_name] = values
        
        self.validateSalesItemsFields()
        return None
    
    
    def validateSalesItemsFields(self) -> None:
        '''
        Este método hace lo siguiente:
        - Si todos los campos son válidos:
            - Habilita el botón 'btn_end_sale'.
            - Obtiene el precio total y lo coloca en 'self.label_total' y lo guarda en 'self.TOTAL_COST'.
            - Crea un QCompleter para 'self.lineEdit_paid' con el precio total y los subtotales.
        - Si hay campos inválidos:
            - Deshabilita el botón 'btn_end_sale'.
            - Coloca el texto inicial en 'label_total'.
            - Coloca el valor None en 'self.TOTAL_COST'.
        
        Retorna None.
        '''
        try:
            # si 'sales_input_list' no está vacía y todos los valores son válidos...
            if (self.ui.sales_input_list.count() > 0
                and all([item[ListItemFields.IS_ALL_VALID.name] for item in self.DICT_ITEMS_VALUES.values()]) ):
                self.__onValidSalesItemsFields()

            else:
                self.ui.btn_end_sale.setEnabled(False)
                self.ui.label_total.setText("TOTAL")
                self.TOTAL_COST = None
        
        except KeyError: # salta cuando no hay key 'IS_ALL_VALID', y pasa cuando se elimina 
            # un item que fue creado y no ha sido modificado ninguno de sus valores
            self.ui.btn_end_sale.setEnabled(False)
            self.ui.label_total.setText("TOTAL")
            self.TOTAL_COST = None
        
        return None
    
    
    def __onValidSalesItemsFields(self) -> None:
        '''
        Habilita el botón 'btn_end_sale', obtiene el precio total y lo muestra, 
        por último crea un QCompleter para 'self.lineEdit_paid' con el precio 
        total y los subtotales.

        Retorna
        -------
        None
        '''
        subtotals:list[float] = [] # lista con los subtotales de los items, es usado por 'completer_values' y
                                   # y para calcular el costo total
        _total_cost:str # var. aux. que contiene el costo total
        
        # obtiene los subtotales (para obtener el total y para luego colocarlos en el completer)
        subtotals = [subtotal[ListItemFields.SUBTOTAL.name] for subtotal in self.DICT_ITEMS_VALUES.values()]
        
        # obtiene el costo total
        try:
            self.TOTAL_COST = round(sum(subtotals), 2)
        
        except TypeError: # salta cuando en subtotals hay un subtotal 'None' (esto pasa porque 
                          # se emiten varias señales desde ListItemWidget, y las primeras son 
                          # con subtotales nulos)
            return None
        
        # coloca el costo total en label_total
        _total_cost = str(self.TOTAL_COST).replace(".",",")
        self.ui.label_total.setText(
            f'''<html>
                    <head/>
                    <body>
                        <p>
                            TOTAL <span style=\" color: #22577a;\">{_total_cost}</span>
                        </p>
                    </body>
                </html>'''
            )
        
        # activa el botón btn_end_sale
        self.ui.btn_end_sale.setEnabled(True)
        
        # crea y coloca el completer con los valores
        self.__createSalesCompleter(subtotals=subtotals, total_cost=_total_cost)
        return None
    
    
    def __createSalesCompleter(self, subtotals:list[float], total_cost:str) -> None:
        '''
        Crea y coloca un QCompleter en 'lineEdit_paid' con los subtotales de los 
        productos y el costo total.

        Parámetros
        ----------
        subtotals : list[float]
            subtotales de los productos
        total_cost : str
            costo total obtenido de la sumatoria de los subtotales
        
        Retorna
        -------
        None
        '''
        completer_values:list[str] = [] # lista con todos los valores ('subtotals') 
                                        # y costo total para el completer.
        completer:QCompleter # completer para poner en lineEdit_paid.
        
        # obtengo todos los valores para el completer (total y subtotales)
        completer_values = [str(value).replace(".",",") for value in subtotals + [total_cost]] # concatena 'subtotals' y 
            # el costo total, convierte los valores a str y le cambia los "." por ",".
        
        # crea el completer para los costos en 'lineEdit_paid'
        completer = QCompleter(completer_values, parent=self.ui.lineEdit_paid)
        completer.setCompletionMode(completer.CompletionMode.InlineCompletion)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.ui.lineEdit_paid.setCompleter(completer)

        self.ui.lineEdit_paid.textChanged.connect(completer.setCompletionPrefix)

        return None
    
    
    @Slot(ListItemValues)
    def onSalesItemFieldValidation(self, list_item:ListItemValues) -> None:
        '''
        Es llamado desde la señal 'fieldsValidated' de 'classes.ListItemWidget'.
        
        Este método hace lo siguiente:
        - Actualiza 'self.DICT_ITEMS_VALUES'.
        - Verifica la validez de todos los items. Para eso llama al método 'self.validateSalesItemsFields'.
        - Cambia el contenido de 'dateTimeEdit_sale' para mostrar la hora precisa de la venta.
        
        Parámetros
        ----------
        list_item: ListItemValues
            objeto con todos los valores actualizados del item
        
        Retorna
        -------
        None
        '''
        # actualiza self.DICT_ITEMS_VALUES
        self.DICT_ITEMS_VALUES[list_item.object_name] = list_item
        
        self.validateSalesItemsFields()
        
        # cambia la hora de la venta
        self.ui.dateTimeEdit_sale.setDateTime(QDateTime.currentDateTime())
        return None
    
    
    # TODO: refactorizar parte del botón de finalizar venta, ya está terminada la parte de sales_input_list y también la de 
    # todo: la tabla con las ventas realizadas. Luego de terminar acá, tengo 2 opciones: empezar con Deudas ó empezar con las 
    # todo: search-bars.
    #* finalizando compra
    @Slot()
    def onFinishedSale(self) -> None:
        '''
        Este método hace lo siguiente:
        - Si la cantidad abonada es < al costo total:
            - Instancia y muestra un dialog de tipo 'DebtorDataDialog' con los 
            datos del deudor y maneja su señal
        - Si la cantidad abonada es >= al costo total:
            - Obtiene los datos de los campos de los items y hace las consultas 
            INSERT a Ventas y Detalle_Ventas y la consulta UPDATE a Productos 
            con el nuevo stock
            - Al finalizar, realiza los reinicios necesarios en variables
        
        Retorna
        -------
        None
        '''
        # TODO: probar si se hacen las consultas a bd cuando hay: 
        # todo: 1.deuda con deudor existente
        # todo: 2.deuda con deudor nuevo
        # todo: 3.sin deuda
        total_paid:float
        
        # obtengo el total pagado
        total_paid = self.ui.lineEdit_paid.text().replace(",",".")
        total_paid = float(total_paid if total_paid else 0.0)
        
        # si lo abonado es menor al total muestra el Dialog para manejar deudores
        if total_paid < self.TOTAL_COST:
            dialog = DebtorDataDialog()
            dialog.setAttribute(Qt.WA_DeleteOnClose, True)
            
            dialog.debtorChosen.connect(lambda debtor_id: self.finishedSaleOnDebtorChosen(
                    debtor_id=debtor_id,
                    total_paid=total_paid
                )
            )
            
            dialog.exec()
        
        # si lo abonado es >= al costo total realiza INSERT a Ventas y Detalle_Ventas, y UPDATE a Productos
        else:
            with self._db_repo as db_repo:
                for item in self.DICT_ITEMS_VALUES.values():
                    # inserta a Ventas
                    db_repo.insertRegister(
                        ins_sql= '''INSERT INTO Ventas(
                                        fecha_hora, detalles_venta) 
                                    VALUES(?, ?);''',
                        ins_params=(self.ui.dateTimeEdit_sale.text(),
                                    item[ListItemFields.SALE_DETAILS.name],)
                    )
                    
                    # inserta a Detalle_Ventas
                    db_repo.insertRegister(
                            ins_sql= '''INSERT INTO Detalle_Ventas(
                                        cantidad, costo_total, IDproducto, IDventa, abonado, IDdeuda) 
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
                            ins_params=(item[ListItemFields.QUANTITY.name],
                                        item[ListItemFields.SUBTOTAL.name],
                                        item[ListItemFields.PRODUCT_NAME.name],
                                        self.ui.dateTimeEdit_sale.text(),
                                        item[ListItemFields.SALE_DETAILS.name],
                                        item[ListItemFields.SUBTOTAL.name],)
                    )
                        
                    # actualiza en Productos
                    db_repo.updateRegisters(
                        upd_sql= '''UPDATE Productos 
                                    SET stock = stock - ? 
                                    WHERE nombre = ?;''',
                        upd_params= (item[ListItemFields.QUANTITY.name],
                                    item[ListItemFields.PRODUCT_NAME.name],)
                    )
            
            # hace los reinicios necesarios para otras ventas
            self.__resetFieldsOnFinishedSale()
        
        return None


    # TODO: refactorizar este método
    @Slot(tuple)
    def finishedSaleOnDebtorChosen(self, debtor_id:int, total_paid:float) -> None:
        '''
        Cuando se termina una venta y hay deuda se invoca este método.
        
        Este método hace lo siguiente:
            - Obtiene los datos de los campos de los items y hace las consultas 
            INSERT a Ventas, Detalle_Ventas y Deudas y la consulta UPDATE a 
            Productos con el nuevo stock.
            
            NOTA: ESTE MÉTODO NO HACE CONSULTA ALGUNA A LA TABLA "Deudores", ESAS 
            CONSULTAS SON HECHAS EN EL DIALOG 'DebtorDataDialog'.
            
            - Al finalizar realiza los reinicios necesarios.
        
        PARÁMETROS
        ----------
        debtor_id : int
            el 'IDdeudor' del deudor
        total_paid : float
            el total abonado al finalizar la venta
        
        Retorna
        -------
        None
        '''
        total_due:float = total_paid # acumulador, inicia con el valor del total abonado y se va descontando de ahí 
                                     # cada subtotal (el precio de cada producto)
        product:dict[str, Any] # valores de un solo producto
        
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
        
        # recorre cada producto y hace las consultas INSERT y UPDATE (a Productos)
        for product in self.DICT_ITEMS_VALUES.values():
            try:
                cursor.execute(
                    "INSERT INTO Ventas(fecha_hora, detalles_venta) VALUES(?,?);",
                    (self.ui.dateTimeEdit_sale.text(), product.getSaleDetails(),)
                    )
                conn.commit()
                
                # actualiza el total debido
                total_due -= product.subtotal # deuda = total abonado - subtotal
                total_due = round(total_due, 2)
                
                # Deudas y Detalle_Ventas (con IDdeuda)
                if total_due < 0: # el producto es deuda
                    cursor.execute(
                        "INSERT INTO Deudas(fecha_hora, total_adeudado, IDdeudor, eliminado) VALUES(?,?,?, 0);",
                        (self.ui.dateTimeEdit_sale.text(), abs(total_due), debtor_id))
                    conn.commit()
                    
                    cursor.execute(
                        "INSERT INTO Detalle_Ventas(cantidad, costo_total, IDproducto, IDventa, abonado, IDdeuda) VALUES(?, ?, (SELECT IDproducto FROM Productos WHERE nombre = ?),(SELECT IDventa FROM Ventas WHERE fecha_hora = ? AND detalles_venta = ?), ?, (SELECT IDdeuda FROM Deudas WHERE fecha_hora = ? AND IDdeudor = ? ORDER BY IDdeuda DESC LIMIT 1));",
                        (product.quantity, product.subtotal, product.product_name, self.ui.dateTimeEdit_sale.text(),
                        product.sale_details, round(product.subtotal - abs(total_due), 2), self.ui.dateTimeEdit_sale.text(),
                        debtor_id, )
                        )
                    conn.commit()
                    
                    total_due = 0
                
                else: # el producto NO es deuda
                    cursor.execute(
                        "INSERT INTO Detalle_Ventas(cantidad, costo_total, IDproducto, IDventa, abonado, IDdeuda) VALUES(?, ?, (SELECT IDproducto FROM Productos WHERE nombre = ?), (SELECT IDventa FROM Ventas WHERE fecha_hora = ? AND detalles_venta = ?), ?, NULL);",
                        (product.quantity, product.subtotal, product.product_name, self.ui.dateTimeEdit_sale.text(),
                        product.sale_details, product.subtotal,)
                        )
                    conn.commit()
                    
                # como última consulta de cada producto, actualiza el stock
                cursor.execute(
                    "UPDATE Productos SET stock = stock - ? WHERE nombre = ?;",
                    (product.quantity, product.product_name,)
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
        Realiza los reinicios finales para poder concretar otra venta.
        - Reinicia el contador para nombres de items 'self.SALES_ITEM_NUM'.
        - Limpia los items en 'self.DICT_ITEMS_VALUES'.
        - Limpia los campos y reasigna el valor por defecto a 'label_total'.
        - Desactiva el botón 'btn_end_sale'.
        
        Retorna
        -------
        None
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