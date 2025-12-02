import sys
from numpy import (empty, ndarray)
from typing import (Any, Iterable)

from PySide6.QtWidgets import (QApplication, QMainWindow, QTableView, 
                               QCheckBox, QAbstractItemView, QListWidgetItem, 
                               QLineEdit, QDateTimeEdit, QDateEdit, 
                               QProgressBar)
from PySide6.QtCore import (QModelIndex, Qt, QThread, Slot, QSize, QTranslator, 
                            QLibraryInfo, QSignalBlocker, QSettings)
from PySide6.QtGui import (QIcon)

from utils.classes import (ProductDialog, SaleDialog, ListItemWidget, 
                           ListItemValues, DebtorDataDialog, WidgetStyle, 
                           SaleFields, CategoryDescDialog)
from utils.messageboxes import (AskBeforeDeletion, WarnAccountHasBalance)
from ui.ui_mainwindow import (Ui_MainWindow)
from ui.customCalendars import (CustomCalendar)
from utils.functionutils import *
from utils.model_classes import (InventoryTableModel, SalesTableModel, DebtsTableModel)
from utils.delegates import (InventoryDelegate, SalesDelegate, DebtsDelegate)
from utils.workerclasses import (WorkerManager, WorkerSelect, WorkerDelete)
from utils.dboperations import (DatabaseRepository, ensureDateTimeISOformat)
from utils.customvalidators import (SalePaidValidator, CategoryNameValidator)
from utils.enumclasses import (ProgramValues, LoggingMessage, ModelHeaders, TableViewId, 
                               LabelFeedbackStyle, InventoryPriceType, TypeSideBar, 
                               InvViewCols, DebtorViewCols, ProgressBarStyle, 
                               DateAndTimeFormat, CommonCategories, 
                               DateTimeRanges, WorkerPriority)
from utils.proxy_models import (InventoryProxyModel, SalesProxyModel, DebtsProxyModel)
from utils.eventfilters import (BackgroundEventFilter, CategoryItemEventFilter, 
                                CategoryListEventFilter)
from utils.settings_manager import (SettingsManager)

from resources import (rc_icons)


class MainWindow(QMainWindow):
    def __init__(self, db_path:str=DATABASE_DIR):
        '''
        Inicializa la ventana principal de la aplicación.
        
        Parámetros
        ----------
        db_path : str, opcional
            dirección usada para la base de datos, por defecto DATABASE_DIR; 
            admite las siguientes direcciones comunes:
            - DATABASE_DIR: usa la dirección por defecto
            - DATABASE_MEMORY: usa una base de datos en memoria ("*:memory:*"), 
            útil para *tests*
            - DATABASE_MEMORY_SHARED: usa una base de datos en memoria 
            ("*file::memory:?cache=shared*"), útil para *tests* con conexiones 
            simultáneas
            Alternativamente se puede especificar una dirección diferente
        '''
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # repositorio de base de datos
        self._db_repo:DatabaseRepository = DatabaseRepository(db_path=db_path)
        
        # configuraciones
        self.config:SettingsManager = SettingsManager(
            app_name=PV.APP_NAME.value,
            organization_name=PV.APP_AUTHOR.value
        )
        
        # inicializa ajustes personalizados de widgets
        self.setup_ui()
        
        # instala event-filters
        self.install_event_filters()
        
        # declara/instancia variables
        self.setup_variables()
        
        self.setup_models()

        self.setup_delegates()
        
        # declara e instancia variables
        self.setup_variables()
        
        #! la declaración de señales se hace al final
        self.setup_inventory_signals()
        self.setup_sales_signals()
        self.setup_debts_signals()
        return None


    def setup_ui(self) -> None:
        '''
        Método que sirve para simplificar la lectura del método 'self.__init__'.
        Contiene inicializaciones y ajustes de algunos Widgets.
        
        Retorna
        -------
        None
        '''
        self.setWindowTitle(ProgramValues.APP_NAME.value)
        geometry, state = self.config.getMainWindowState()
        self.restoreGeometry(geometry) if geometry else None
        self.restoreState(state) if state else None
        
        self.__setTablesListWidgetItems()
        
        self.__hideWidgets() # esconde algunos widgets inicialmente
        
        self.__initGeneralValidators() # inicializa validadores existentes
        
        self.__setInitialIconsToWidgets() # añade íconos a los widgets...
        self.__setInitialStylesheets() # y estilos iniciales a comboboxes
        
        # políticas de QTableViews
        setTableViewPolitics(self.ui.tv_inventory_data)
        setTableViewPolitics(self.ui.tv_sales_data)
        setTableViewPolitics(self.ui.tv_debts_data)
        
        # las checkboxes de porcentajes son exclusivas
        self.ui.inventory_checkbuttons_buttonGroup.setExclusive(True)
        
        # en el formulario de Ventas coloca el tiempo en que se inició el programa
        self.ui.dateTimeEdit_sale.setDateTime(QDateTime.currentDateTime())
        
        # en los dateedit coloca la fecha de hoy
        _today:QDate = QDate.currentDate()
        
        self.__setInitDateWidgets(
            widget=self.ui.dateEdit_from_date,
            date= getWeekStartDate(_today)
        )
        self.__setInitDateWidgets(
            widget=self.ui.dateEdit_to_date,
            date=_today
        )
        self.__setInitDateWidgets(
            widget=self.ui.dateEdit_show_collected_by_day,
            date=_today
        )
            
        return None    


    def install_event_filters(self) -> None:
        '''
        Instala los filtros de eventos en los widgets.
        '''
        # categorías
        self.category_list_event_filter = CategoryListEventFilter(self.ui.tables_ListWidget)
        self.ui.tables_ListWidget.installEventFilter(self.category_list_event_filter)
        
        # productos
        self.inv_table_event_filter = BackgroundEventFilter(self.ui.tv_inventory_data)
        self.ui.tv_inventory_data.viewport().installEventFilter(self.inv_table_event_filter)
        
        # ventas
        self.sales_input_list_event_filter = BackgroundEventFilter(self.ui.sales_input_list)
        self.ui.sales_input_list.viewport().installEventFilter(self.sales_input_list_event_filter)
        
        self.sales_table_event_filter = BackgroundEventFilter(self.ui.tv_sales_data)
        self.ui.tv_sales_data.viewport().installEventFilter(self.sales_table_event_filter)
        
        # deudas
        self.debts_table_event_filter = BackgroundEventFilter(self.ui.tv_debts_data)
        self.ui.tv_debts_data.viewport().installEventFilter(self.debts_table_event_filter)
        return None


    def setup_models(self) -> None:
        '''
        Este método tiene el objeto de simplificar la lectura del método 
        'self.__init__'.
        Contiene las declaraciones de MODELOS DE DATOS y PROXY MODELS de 
        de VISTAS.
        
        Retorna
        -------
        None
        '''
        #? proxy model-modelo de datos: los DELETE e INSERT pasan por el proxy 
        #? model, los UPDATE y READ se hacen directamente al modelo.
        
        #* modelo de datos y proxy model de Inventario
        self.inventory_data_model:InventoryTableModel = InventoryTableModel()
        
        self.inventory_proxy_model:InventoryProxyModel = InventoryProxyModel()
        self.inventory_proxy_model.setSourceModel(self.inventory_data_model)
        
        self.inventory_proxy_model.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.ui.tv_inventory_data.setSortingEnabled(True)
        self.ui.tv_inventory_data.setModel(self.inventory_proxy_model)
        
        #* modelo de datos de Ventas
        self.sales_data_model:SalesTableModel = SalesTableModel()
        
        self.sales_proxy_model:SalesProxyModel = SalesProxyModel()
        self.sales_proxy_model.setSourceModel(self.sales_data_model)
        
        self.sales_proxy_model.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.ui.tv_sales_data.setSortingEnabled(True)
        self.ui.tv_sales_data.setModel(self.sales_proxy_model)
        
        #* modelo de datos de Deudas
        self.debts_data_model:DebtsTableModel = DebtsTableModel()
        
        self.debts_proxy_model:DebtsProxyModel = DebtsProxyModel()
        self.debts_proxy_model.setSourceModel(self.debts_data_model)
        
        self.debts_proxy_model.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.ui.tv_debts_data.setSortingEnabled(True)
        self.ui.tv_debts_data.setModel(self.debts_proxy_model)
        return None


    def setup_delegates(self) -> None:
        '''
        Este método tiene el objeto de simplificar la lectura del método 
        'self.__init__'.
        Contiene las declaraciones de los delegados usados en las VISTAS.
        
        Retorna
        -------
        None
        '''
        #* delegado de inventario
        self.inventory_delegate = InventoryDelegate()
        self.ui.tv_inventory_data.setItemDelegate(self.inventory_delegate)
        
        #* delegado de ventas
        self.sales_delegate = SalesDelegate(self.ui.dateTimeEdit_sale.displayFormat())
        self.ui.tv_sales_data.setItemDelegate(self.sales_delegate)
        
        #* delegado de deudas
        self.debts_delegate = DebtsDelegate(parent=self.ui.tv_debts_data)
        self.ui.tv_debts_data.setItemDelegate(self.debts_delegate)
        return None
    

    def setup_variables(self) -> None:
        '''
        Éste método tiene el objeto de simplificar la lectura del método 
        'self.__init__'.
        Contiene las declaraciones de variables locales que se usan a lo largo 
        de la ejecución del programa.
        
        Retorna
        -------
        None
        '''
        #? Los acumuladores de datos sirven para hacer operaciones sobre los 
        #? modelos de datos y la base de datos en "batches" y mejorar el 
        #? rendimiento de la aplicación en general...
        
        #¡ variables de inventario
        self._inv_model_data_acc:ndarray[Any] = None # acumulador temporal de 
            # datos para modelo de Inventario.
        
        #¡ variables de ventas
        self._sales_model_data_acc:ndarray[Any] = None # acumulador temp. de 
            # datos para modelo de Ventas.
        
        self.SALES_ITEM_NUM:int = 0 # contador para crear nombres de items en 
                                    # 'input_sales_data'.
        self.DICT_ITEMS_VALUES:dict[str, dict] = {} # tiene los valores de 
            # cada 'ListItemWidget'.
        self.VALID_PAID_FIELD:bool = None # True si lineEdit_paid es válido, 
            # sino False.
        self.TOTAL_COST:float = None # guarda el costo total de 'label_total' 
            # como float, para no tener que buscarlo con regex.

        #¡ variables de deudas
        self._debts_model_data_acc:ndarray[Any] = None # acumulador temp. de 
            # datos para modelo de Deudas.
        
        #¡ variables de workers
        self.worker_manager:WorkerManager = WorkerManager()
        self.select_worker:WorkerSelect = None
        self.delete_worker:WorkerDelete = None
        
        return None


    #¡ === SEÑALES ================================================================================
    def setup_inventory_signals(self) -> None:
        #* abrir/cerrar side bars
        self.ui.btn_side_barToggle.clicked.connect(lambda: self.toggleSideBar(
            TypeSideBar.CATEGORIES_SIDEBAR))
        
        self.ui.btn_inventory_sideBarToggle.clicked.connect(lambda: self.toggleSideBar(
            TypeSideBar.PERCENTAGES_SIDEBAR))
        
        #* (READ) cargar con productos 'tv_inventory_data'
        self.ui.tables_ListWidget.itemDoubleClicked.connect(lambda item: self.fillTableView(
            table_viewID=TableViewId.INVEN_TABLE_VIEW,
            ACCESSED_BY_LIST=True,
            SHOW_ALL=True if item.text() == CommonCategories.SHOW_ALL.value else False
            )
        )

        #* (CREATE) añadir nuevo producto a tabla 'tv_inventory_data'
        self.ui.btn_add_product_inventory.clicked.connect(
            lambda: self.handleTableCreateRow(TableViewId.INVEN_TABLE_VIEW)
        )
        
        #* (DELETE) eliminar un producto de 'tv_inventory_data'
        # cambios en la selección
        self.ui.tv_inventory_data.selectionModel().selectionChanged.connect(
            lambda: self.toggleDeleteButton(table_viewID=TableViewId.INVEN_TABLE_VIEW)
        )
        
        self.ui.btn_delete_product_inventory.clicked.connect(
            lambda: self.__removeInventoryModelRows()
        )
        
        self.inventory_proxy_model.baseModelRowsSelected.connect(
            self.confirmedInventoryRowsDeletion
        )
        
        #* (UPDATE) modificar celdas de 'tv_inventory_data' (sin porcentajes)
        self.inventory_data_model.dataToUpdate.connect(
            lambda params: self.onInventoryModelDataToUpdate(
                column=params[0], new_values=params[1:]
            )
        )
        
        #* delegado de inventario
        self.inventory_delegate.fieldIsValid.connect(self.__onDelegateValidationSucceded)
        self.inventory_delegate.fieldIsInvalid.connect(self.__onDelegateValidationFailed)
        
        #* inventory_sideBar
        self.ui.inventory_checkbuttons_buttonGroup.buttonPressed.connect(self.handlePressedCheckbox)
        self.ui.inventory_checkbuttons_buttonGroup.buttonClicked.connect(self.handleClickedCheckbox)
        
        self.ui.checkbox_unit_prices.stateChanged.connect(self.handleCheckboxStateChange)
        
        self.ui.checkbox_comercial_prices.stateChanged.connect(self.handleCheckboxStateChange)
        
        #* lineedit de porcentajes
        self.ui.lineEdit_percentage_change.returnPressed.connect(self.onLePercentageEditingFinished)
        self.ui.lineEdit_percentage_change.validator().validationSucceeded.connect(
            self.__onPercentageValidatorSucceded)
        self.ui.lineEdit_percentage_change.validator().validationFailed.connect(
            self.__onPercentageValidatorFailed)
        
        #* search bar
        self.ui.inventory_searchBar.returnPressed.connect(
            lambda: self.filterTableView(
                text=self.ui.inventory_searchBar.text(),
                tableViewID=TableViewId.INVEN_TABLE_VIEW
            )
        )
        self.ui.cb_inventory_colsFilter.currentIndexChanged.connect(
            lambda index: self.changeFilterColumn(
                column=index,
                tableViewID=TableViewId.INVEN_TABLE_VIEW
            )
        )
        
        #* sidebar de categorías
        self.ui.btn_sidebar_list_add_item.clicked.connect(self.addNewCategory)
        
        self.ui.tables_ListWidget.selectionModel().selectionChanged.connect(
            lambda: self.toggleCategoryDeleteButton(
                selected_items=self.ui.tables_ListWidget.selectedItems()
            )
        )
        self.ui.btn_sidebar_list_delete_item.clicked.connect(
            lambda: self.deleteCategory(
                selected_items=self.ui.tables_ListWidget.selectedItems()
            )
        )
        
        self.category_list_event_filter.nameAboutToChange.connect(self.setEditableCategoryName)
        self.category_list_event_filter.descAboutToChange.connect(self.showCategoryEditDialog)
        return None
    
    
    def setup_sales_signals(self) -> None:
        #* cambio de pestaña
        self.ui.tab2_toolBox.currentChanged.connect(
            lambda curr_index: self.setInitialDateRange() if curr_index == 1 else None
        )
        
        #* deteedits (rango de fechas)
        self.ui.dateEdit_from_date.dateChanged.connect(
            lambda date: self.validateDateRange(
                dateedit=self.ui.dateEdit_from_date,
                date=date
            )
        )
        self.ui.dateEdit_to_date.dateChanged.connect(
            lambda date: self.validateDateRange(
                dateedit=self.ui.dateEdit_to_date,
                date=date
            )
        )
        
        #* (otra vez) cambio de pestaña
        self.ui.tab2_toolBox.currentChanged.connect(
            lambda curr_index: self.ui.dateEdit_from_date.dateChanged.emit(
                self.ui.dateEdit_from_date.date()
            ) if curr_index == 1 else None
        )
        
        #* (READ) cargar con ventas 'tv_sales_data'
        self.ui.dateEdit_from_date.dateChanged.connect(
            lambda: self.fillTableView(table_viewID=TableViewId.SALES_TABLE_VIEW)
        )
        self.ui.dateEdit_to_date.dateChanged.connect(
            lambda: self.fillTableView(table_viewID=TableViewId.SALES_TABLE_VIEW)
        )
        
        
        self.ui.tabWidget.currentChanged.connect(lambda index: self.ui.tab2_toolBox.setCurrentIndex(0) if index == 1 else None)
        
        #* (CREATE) añadir una venta a 'tv_sales_data'
        self.ui.btn_add_product_sales.clicked.connect(
            lambda: self.handleTableCreateRow(TableViewId.SALES_TABLE_VIEW)
        )
        
        #* (DELETE) eliminar ventas de 'tv_sales_data'
        # cambios en la selección
        self.ui.tv_sales_data.selectionModel().selectionChanged.connect(
            lambda: self.toggleDeleteButton(table_viewID=TableViewId.SALES_TABLE_VIEW)
        )
        
        self.ui.btn_delete_product_sales.clicked.connect(
            lambda: self.__removeSalesModelRows()
        )
        
        self.sales_proxy_model.baseModelRowsSelected.connect(
            self.confirmedSalesRowsDeletion
        )
        
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
        
        #* search bar
        self.ui.sales_searchBar.returnPressed.connect(
            lambda: self.filterTableView(
                text=self.ui.sales_searchBar.text(),
                tableViewID=TableViewId.SALES_TABLE_VIEW
            )
        )
        self.ui.cb_sales_colsFilter.currentIndexChanged.connect(
            lambda index: self.changeFilterColumn(
                column=index,
                tableViewID=TableViewId.SALES_TABLE_VIEW
            )
        )

        #* dateedit (mostrar ganancias por día)
        self.ui.dateEdit_show_collected_by_day.dateChanged.connect(
            self.showCollectedInDay
        )
        
        #* formulario de ventas
        self.ui.btn_add_product.clicked.connect(self.addSalesInputListItem)
        
        self.ui.lineEdit_paid.editingFinished.connect(self.onSalePaidEditingFinished)
        
        self.ui.btn_end_sale.clicked.connect(self.onFinishedSale)
        return None
    
    
    def setup_debts_signals(self) -> None:
        #* (READ) cargar con deudas 'tv_debts_data'
        self.ui.tabWidget.currentChanged.connect(lambda curr_index: self.fillTableView(
            table_viewID=TableViewId.DEBTS_TABLE_VIEW, SHOW_ALL=True) if curr_index == 2 else None)
        
        #* (CREATE) añadir una venta a 'tv_sales_data'
        self.ui.btn_add_debtor.clicked.connect(
            lambda: self.handleTableCreateRow(
                table_viewID=TableViewId.DEBTS_TABLE_VIEW
            )
        )
        
        #* (DELETE) eliminar ventas de 'tv_sales_data'
        # cambios en la selección
        self.ui.tv_debts_data.selectionModel().selectionChanged.connect(
            lambda: self.toggleDeleteButton(table_viewID=TableViewId.DEBTS_TABLE_VIEW)
        )
        
        self.ui.btn_delete_debtor.clicked.connect(
            lambda: self.__removeDebtsModelRows()
        )
        
        self.debts_proxy_model.baseModelRowsSelected.connect(
            self.confirmedDebtsRowsDeletion
        )
        
        #* (UPDATE) modificar celdas de 'tv_sales_data'
        self.debts_data_model.dataToUpdate.connect(
            lambda params: self.__onDebtsModelDataToUpdate(
                column=params['column'],
                ID_debtor=params['IDdebtor'],
                new_val=params['new_value']
            )
        )
        
        self.debts_delegate.balanceDialogFinished.connect(self.__updateViewOnDebtsBalanceChanged)
        
        #* delegado de deudas
        self.debts_delegate.fieldIsValid.connect(self.__onDelegateValidationSucceded)
        self.debts_delegate.fieldIsInvalid.connect(self.__onDelegateValidationFailed)
        
        #* search bar
        self.ui.debts_searchBar.returnPressed.connect(
            lambda: self.filterTableView(
                text=self.ui.debts_searchBar.text(),
                tableViewID=TableViewId.DEBTS_TABLE_VIEW
            )
        )
        self.ui.cb_debts_colsFilter.currentIndexChanged.connect(
            lambda index: self.changeFilterColumn(
                column=index,
                tableViewID=TableViewId.DEBTS_TABLE_VIEW
            )
        )
        return None
    
    
    #¡ === FIN SEÑALES ============================================================================
    
    def __setTablesListWidgetItems(self) -> None:
        '''
        Coloca las categorías de productos en el QListWidget del sidebar y le 
        asigna a cada item un tooltip con su descripción.
        '''
        categories:list[tuple[str, str]] # list[tuple(categoría, descripción)]
        
        # obtiene las categorías y descripciones
        with self._db_repo as db_repo:
            categories = db_repo.selectRegisters(
                data_sql='''SELECT nombre_categoria,
                                   descripcion 
                            FROM Categorias;'''
            )
        
        if not categories:
            return None
        
        # ordena las categorías
        categories = sorted(categories, key=lambda x: x[0])
        
        # coloca las categorías y sus descripciones en la lista
        for count, cat_desc in enumerate(categories):
            self.ui.tables_ListWidget.addItem(f"{cat_desc[0]}")
            self.ui.tables_ListWidget.item(count).setToolTip(
                f'''<html>
                        <head/>
                        <body>
                            <p>
                                <span style=\" font-size:11pt; color: #111;\">{cat_desc[1]}</span>
                            </p>
                        </body>
                    </html>'''
            )
        
        # por último, agrega un item para mostrar todos
        self.ui.tables_ListWidget.addItem(CommonCategories.SHOW_ALL.value)
        self.ui.tables_ListWidget.item(self.ui.tables_ListWidget.count() - 1).setToolTip(
            ''' <html>
                    <head/>
                    <body>
                        <p>
                            <span style=\" font-size:11pt; color: #111;\">Muestra todos los productos disponibles</span>
                        </p>
                    </body>
                </html>'''
        )
        
        return None
    
    
    def __setInitialIconsToWidgets(self) -> None:
        '''
        Coloca los íconos por defecto que le corresponde a cada Widget. Éste 
        método aplica los íconos instanciando objetos.
        
        Retorna
        -------
        None
        '''
        self.main_window_icon = QIcon() # ventana principal
        self.sidebar_toggle_icon = QIcon() # sidebar de categorías
        self.inv_sidebar_toggle_icon = QIcon() # sidebar de porcentajes
        self.percent_icon = QIcon() # lineedit de porcentajes
        self.search_bars_icon = QIcon() # searchbars
        self.add_register_icon = QIcon() # añadir registros
        self.add_debtor_icon = QIcon() # añadir deudores
        self.delete_register_icon = QIcon() # eliminar registros
        self.delete_register_dark_icon = QIcon() # eliminar registros (color alternativo oscuro)
        self.end_sale_icon = QIcon() # terminar venta (formulario)
        
        # ícono de la ventana principal
        self.main_window_icon.addFile(":/icons/program-icon.ico")
        self.setWindowIcon(self.main_window_icon)
        
        # sidebar de categorías
        self.sidebar_toggle_icon.addFile(":/icons/list-normal.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.sidebar_toggle_icon.addFile(":/icons/list-focus.svg", QSize(), QIcon.Mode.Active, QIcon.State.On)
        self.ui.btn_side_barToggle.setIcon(self.sidebar_toggle_icon)
        
        # sidebar de porcentajes
        self.inv_sidebar_toggle_icon.addFile(":/icons/menu-normal.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.inv_sidebar_toggle_icon.addFile(":/icons/menu-focus.svg", QSize(), QIcon.Mode.Active, QIcon.State.On)
        self.ui.btn_inventory_sideBarToggle.setIcon(self.inv_sidebar_toggle_icon)
        
        # lineedit de porcentajes
        self.percent_icon.addFile(":/icons/percent.svg", QSize())
        self.ui.lineEdit_percentage_change.addAction(self.percent_icon, QLineEdit.ActionPosition.LeadingPosition)
        
        # search-bars
        self.search_bars_icon.addFile(":/icons/search.svg")
        self.ui.inventory_searchBar.addAction(self.search_bars_icon, QLineEdit.ActionPosition.LeadingPosition)
        self.ui.sales_searchBar.addAction(self.search_bars_icon, QLineEdit.ActionPosition.LeadingPosition)
        self.ui.debts_searchBar.addAction(self.search_bars_icon, QLineEdit.ActionPosition.LeadingPosition)
        
        # botones para añadir registros
        self.add_register_icon.addFile(":/icons/plus.svg", QSize())
        self.ui.btn_add_product_inventory.setIcon(self.add_register_icon)
        self.ui.btn_add_product.setIcon(self.add_register_icon)
        self.ui.btn_add_product_sales.setIcon(self.add_register_icon)
        self.ui.btn_sidebar_list_add_item.setIcon(self.add_register_icon)
        
        # botón para añadir deudores
        self.add_debtor_icon.addFile(":/icons/add-debtor.svg", QSize())
        self.ui.btn_add_debtor.setIcon(self.add_debtor_icon)
        
        # botones para eliminar registros
        self.delete_register_icon.addFile(":/icons/minus-circle.svg", QSize())
        self.ui.btn_delete_product_inventory.setIcon(self.delete_register_icon)
        self.ui.btn_delete_product_sales.setIcon(self.delete_register_icon)
        self.ui.btn_delete_debtor.setIcon(self.delete_register_icon)
        
        # botones para eliminar registros (color oscuro)
        self.delete_register_dark_icon.addFile(":/icons/minus-circle-alt.svg", QSize())
        self.ui.btn_sidebar_list_delete_item.setIcon(self.delete_register_dark_icon)

        # botón para terminar venta
        self.end_sale_icon.addFile(":/icons/check-circle.svg")
        self.ui.btn_end_sale.setIcon(self.end_sale_icon)
        
        return None


    def __setInitialStylesheets(self) -> None:
        '''
        Coloca las QSS por defecto que le corresponde a cada widget. Éste 
        método asigna íconos y estilos usando stylesheets, no instancia ningún 
        objeto.
        
        Retorna
        -------
        None
        '''
        # comboboxes
        self.ui.cb_inventory_colsFilter.setStyleSheet(WidgetStyle.DEF_COMBOBOX_FILTER_ICON.value)
        self.ui.cb_sales_colsFilter.setStyleSheet(WidgetStyle.DEF_COMBOBOX_FILTER_ICON.value)
        self.ui.cb_debts_colsFilter.setStyleSheet(WidgetStyle.DEF_COMBOBOX_FILTER_ICON.value)
        
        # dateedits
        self.ui.dateEdit_from_date.setStyleSheet(WidgetStyle.DEF_DATEEDIT_ARROW_ICON.value)
        self.ui.dateEdit_to_date.setStyleSheet(WidgetStyle.DEF_DATEEDIT_ARROW_ICON.value)
        self.ui.dateEdit_show_collected_by_day.setStyleSheet(WidgetStyle.DEF_DATEEDIT_ARROW_ICON.value)
        
        return None
    

    def __setInitDateWidgets(self, widget:type[QDateTimeEdit], date:QDate) -> None:
        '''
        Reemplaza el calendario interactivo del *widget* por uno personalizado 
        y le coloca la fecha especificada.
        
        Parámetros
        ----------
        widget : type[QDateTimeEdit]
            subclase de **QDateTimeEdit** que configurar
        date : QDate
            la fecha que colocarle al *widget*
        '''
        with QSignalBlocker(widget):
            widget.setCalendarWidget(CustomCalendar(widget))
            widget.setDate(date)
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


    #¡ método de search-bars
    @Slot(str, object)
    def filterTableView(self, text:str, tableViewID:TableViewId) -> None:
        '''
        Filtra la tabla especificada de acuerdo al texto introducido.
        
        Parámetros
        ----------
        text : str
            el texto introducido en la search-bar
        
        Retorna
        -------
        None
        '''
        match tableViewID:
            case TableViewId.INVEN_TABLE_VIEW:
                self.inventory_proxy_model.setFilterRegularExpression(text)
            
            case TableViewId.SALES_TABLE_VIEW:
                self.sales_proxy_model.setFilterRegularExpression(text)
            
            case TableViewId.DEBTS_TABLE_VIEW:
                self.debts_proxy_model.setFilterRegularExpression(text)
        
        return None
    
    
    @Slot(int, object)
    def changeFilterColumn(self, column:int, tableViewID:TableViewId) -> None:
        '''
        Cambia la columna filtrada en el PROXY MODEL.

        Parámetros
        ----------
        column : int
            índice actual del QComboBox que representa la columna a filtrar en 
            el PROXY MODEL
        tableViewID : TableViewId
            QTableView al que se referencia

        Retorna
        -------
        None
        '''
        _mapped_column:int = column - 1 # la columna elegida en el combobox 
            # convertida a la columna que representa en la tabla.
        
        match tableViewID:
            case TableViewId.INVEN_TABLE_VIEW:
                self.inventory_proxy_model.setFilterColumn(column=_mapped_column)
            
            case TableViewId.SALES_TABLE_VIEW:
                self.sales_proxy_model.setFilterColumn(column=_mapped_column)
            
            case TableViewId.DEBTS_TABLE_VIEW:
                self.debts_proxy_model.setFilterColumn(column=_mapped_column)
            
        return None


    #¡ métodos de sidebars
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
    
    
    @Slot()
    def addNewCategory(self) -> None:
        '''
        Agrega un item editable a la lista de categorías para que el usuario 
        pueda crear una nueva categoría.
        '''
        item = QListWidgetItem()
        self.ui.tables_ListWidget.addItem(item)
        
        # crea editor y validador para poder ingresar el nombre de la categoría
        editor:QLineEdit = self.__createCategoryNameEditor(item=item)
        
        self.ui.tables_ListWidget.setItemWidget(item, editor)
        editor.setFocus()
                
        # conecta señal 'editingFinished' del editor
        editor.editingFinished.connect(
            lambda: self.__categoryEditorOnConfirmedName(item, editor.text())
        )
        return None
    
    
    def __createCategoryNameEditor(self, item:QListWidgetItem, edit_mode:bool=False) -> QLineEdit:
        '''
        Crea un editor con su validador y un filtro de eventos para editar los 
        items de *tables_listWidget* y lo retorna.
        
        **NOTA:** éste método conecta la señal *editingFinished* a una función 
        que formatea el campo, pero lo ideal es extender su comportamiento 
        conectando nuevamente la señal a otra función.

        Parámetros
        ----------
        item : QListWidgetItem
            el item al cual colocarle un editor
        edit_mode : bool, por defecto False
            flag que determina si el editor está en modo edición o no; si es 
            True el validador compara el nuevo nombre con el anterior, sino no 
            lo hace
        
        Retorna
        -------
        QLineEdit
            editor para los items del QListWidget
        '''
        # crea editor y validador para poder ingresar el nombre de la categoría
        editor = QLineEdit()
        validator = CategoryNameValidator(
            parent=editor,
            prev_name=item.text() if edit_mode else None
        )
        
        editor.setValidator(validator)
        editor.setPlaceholderText("Escribir el nombre de la categoría")
        
        # coloca en el editor un event-filter
        filter_event:CategoryItemEventFilter = CategoryItemEventFilter(
            lineedit=editor,
            item=item,
            edit_mode=edit_mode
        )
        editor.installEventFilter(filter_event)
        
        # conecta señales
        editor.editingFinished.connect(
            lambda: editor.setText(
                editor.text().strip()
            )
        )
        
        validator.validationSucceeded.connect(
            lambda: filter_event.setValidity(validity=True)
        )
        validator.validationSucceeded.connect(
            lambda: editor.setStyleSheet(WidgetStyle.FIELD_VALID_VAL.value)
        )
        validator.validationFailed.connect(
            lambda: filter_event.setValidity(validity=False)
        )
        validator.validationFailed.connect(
            lambda: editor.setStyleSheet(WidgetStyle.FIELD_INVALID_VAL.value)
        )
        validator.isEmpty.connect(
            lambda: filter_event.setValidity(validity=None)
        )
        validator.isEmpty.connect(
            lambda: editor.setStyleSheet("")
        )
        
        filter_event.itemToDelete.connect( # si está en modo edición nunca se ejecuta este Slot...
            lambda item: self.ui.tables_ListWidget.takeItem(
                self.ui.tables_ListWidget.row(item)
            )
        )
        filter_event.itemToReset.connect( # ... alternativamente, si NO está en modo edición 
            lambda item: self.ui.tables_ListWidget.setItemWidget( # no se ejecuta este otro Slot.
                item, None
            )
        )
        
        return editor
    
    
    def __categoryEditorOnConfirmedName(self, item:QListWidgetItem, name:str) -> None:
        '''
        Agrega la categoría a la base de datos si el usuario ingresó una y 
        actualiza el contenido del QListWidgetItem.

        Parámetros
        ----------
        item : QListWidgetItem
            el item de la lista
        name : str
            el nombre de la categoría
        '''
        if name:
            with self._db_repo as db_repo:
                db_repo.insertRegister(
                    ins_sql= '''INSERT INTO Categorias (nombre_categoria, descripcion)
                                VALUES (?, ?);''',
                    ins_params=(name, "",)
                )
            
            item.setText(name)
            self.ui.tables_ListWidget.setItemWidget(item, None) # quita el editor del widget
            
            self.__makeCategoryListLastsConfigs()
        
        else:
            # si está vacío borra el item
            self.ui.tables_ListWidget.takeItem(self.ui.tables_ListWidget.row(item))
        return None
    
    
    def __makeCategoryListLastsConfigs(self) -> None:
        '''
        Ordena la lista *tables_listWidget* y coloca como último item el de 
        **MOSTRAR TODOS**.
        '''
        _item_show_all:list[QListWidgetItem] | QListWidgetItem # var. auxiliar, sirve 
            # para colocar "MOSTRAR TODOS" al final luego de ordenar la lista.
        
        self.ui.tables_ListWidget.sortItems(Qt.SortOrder.AscendingOrder)
        
        _item_show_all = self.ui.tables_ListWidget.findItems(
            CommonCategories.SHOW_ALL.value,
            Qt.MatchFlag.MatchExactly
        )
        
        if _item_show_all:
            _item_show_all = _item_show_all[0]
            self.ui.tables_ListWidget.takeItem(
                self.ui.tables_ListWidget.row(_item_show_all)
            )
            self.ui.tables_ListWidget.addItem(_item_show_all)
        return None
    
    
    @Slot(object)
    def toggleCategoryDeleteButton(self, selected_items:list[QListWidgetItem]) -> None:
        '''
        Habilita/inhabilita el botón para eliminar categorías dependiendo de 
        la selección de items del QListWidget de categorías. Si el item 
        seleccionado es el de **"MOSTRAR TODOS"** entonces desactiva el botón 
        de borrar categorías.
        
        Parámetros
        ----------
        selected_items : list[QListWidgetItem]
            los items seleccionados, debido a que 'tables_listWidget' permite 
            la selección simple la lista siempre tendrá ninguno o un solo item
        '''
        _selected_item:QListWidgetItem
        
        if not selected_items:
            return None
        
        # si hay selección, la lista siempre tendrá 1 item, porque 'tables_listWidget' 
        # sólo admite la selección de un solo item (es 'single-selection')
        _selected_item = selected_items[0]
        
        if _selected_item.text().strip().upper() not in (CommonCategories.MISC.value.upper(), CommonCategories.SHOW_ALL.value):
            self.ui.btn_sidebar_list_delete_item.setEnabled(
                self.ui.tables_ListWidget.selectionModel().hasSelection()
            )
        
        else:
            self.ui.btn_sidebar_list_delete_item.setEnabled(False)
            
        
        return None
    
    
    @Slot(object)
    def deleteCategory(self, selected_items:list[QListWidgetItem]) -> None:
        '''
        Elimina la categoría seleccionada. Los productos pertenecientes a 
        categorías que son eliminadas pasan a ser considerados de categoría 
        **"Varios"** para evitar conflictos de referencia.
        Al finalizar, quita el item del QListView y desactiva el botón de 
        borrar categorías.

        Parámetros
        ----------
        selected_items : list[QListWidgetItem]
            los items seleccionados, debido a que 'tables_listWidget' permite 
            la selección simple la lista siempre tendrá ninguno o un solo item
        '''
        _selected_item:QListWidgetItem
        
        if not selected_items:
            return None
        
        _selected_item = selected_items[0]
        
        with self._db_repo as db_repo:
            # antes de eliminar la categoría, relaciona todos los productos 
            # de la categoría a borrar con la categoría "Varios"
            db_repo.updateRegisters(
                upd_sql= '''UPDATE Productos
                            SET IDcategoria = (
                                SELECT IDcategoria 
                                FROM Categorias 
                                WHERE nombre_categoria = 'Varios'
                            )
                            WHERE IDcategoria = (
                                SELECT IDcategoria 
                                FROM Categorias 
                                WHERE nombre_categoria = ?
                            );''',
                upd_params=(_selected_item.text(),)
            )
            
            db_repo.deleteRegisters(
                del_sql= '''DELETE FROM Categorias
                            WHERE IDcategoria = (
                                SELECT IDcategoria 
                                FROM Categorias 
                                WHERE nombre_categoria = ?
                            );''',
                del_params=(_selected_item.text(),)
            )
        
        # quita el item de la lista
        self.ui.tables_ListWidget.takeItem(
            self.ui.tables_ListWidget.row(_selected_item)
        )
        
        # desactiva el botón de borrar categorías
        self.ui.btn_sidebar_list_delete_item.setEnabled(False)
        return None
    
    
    @Slot(QListWidgetItem)
    def setEditableCategoryName(self, item:QListWidgetItem) -> None:
        '''
        Coloca un QLineEdit en el item seleccionado para editar el nombre de 
        la categoría.

        Parámetros
        ----------
        item : QListWidgetItem
            el item al cual hacer editable
        '''
        # crea editor
        editor:QLineEdit = self.__createCategoryNameEditor(
            item=item,
            edit_mode=True
        )
        
        self.ui.tables_ListWidget.setItemWidget(item, editor)
        editor.setFocus()
        
        # conecta señal 'editingFinished' del editor
        editor.editingFinished.connect(
            lambda: self.__onCategoryNameUpdate(item=item, new_name=editor.text())
        )
        return None
    
    
    @Slot(str, str)
    def __onCategoryNameUpdate(self, item:QListWidgetItem, new_name:str) -> None:
        '''
        Modifica el nombre de categoría en la base de datos y actualiza el 
        contenido del QListWidgetItem.
        **NOTA:** en caso que el nuevo nombre sea igual al anterior o que el 
        campo esté vacío, el campo conservará el nombre anterior

        Parámetros
        ----------
        item : QListWidgetItem
            el item de la lista
        new_name : str
            el nombre nuevo de la categoría
        '''
        prev_name:str = item.text()
        
        if not new_name:
            new_name = prev_name
        
        else:
            with self._db_repo as db_repo:
                db_repo.updateRegisters(
                    upd_sql= '''UPDATE Categorias 
                                SET nombre_categoria = ? 
                                WHERE IDcategoria = (
                                    SELECT IDcategoria 
                                    FROM Categorias 
                                    WHERE nombre_categoria = ?
                                )''',
                    upd_params=(new_name, prev_name,)
                )
        
        item.setText(new_name)
        self.__makeCategoryListLastsConfigs()
        
        # quita el editor del widget
        self.ui.tables_ListWidget.setItemWidget(item, None)
        return None
    
    
    @Slot(QListWidgetItem)
    def showCategoryEditDialog(self, item:QListWidgetItem) -> None:
        '''
        Crea y muestra un *QDialog* para editar la descripción de la categoría 
        seleccionada.

        Parámetros
        ----------
        item : QListWidgetItem
            el item al cual referencia el *QDialog*
        '''
        # crea dialog
        category_dialog = CategoryDescDialog(
            list_item=item)
        
        category_dialog.categ_desc_dialog.te_category_desc.setFocus()
        
        # si se escribe una descripción del item la coloca como tooltip, sino 
        # deja el tooltip del item vacío
        category_dialog.descriptionChanged.connect(
            lambda desc: item.setToolTip(
                f''' <html>
                        <head/>
                        <body>
                            <p>
                                <span style=" font-size:12pt;">{desc}</span>
                            </p>
                        </body>
                    </html>'''
            if desc else None)
        )
        
        category_dialog.exec()
        return None
    
    
    #¡ métodos de acumulador de datos
    def __setNpDataAccumulator(self, table_viewID:TableViewId,
                            model_shape:tuple[int, int]) -> None:
        '''
        Dependiendo de la VISTA usada, crea un **numpy.ndarray** vacío con 
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
                    dtype=object
                )
            
            case "SALES_TABLE_VIEW": # Ventas
                self._sales_model_data_acc = empty(
                    shape=model_shape,
                    dtype=object
                )
            
            case "DEBTS_TABLE_VIEW": # Ctas. Ctes.
                self._debts_model_data_acc = empty(
                    shape=model_shape,
                    dtype=object
                )
        return None


    #¡ tablas (READ)
    @Slot(QTableView, bool, bool)
    def fillTableView(self, table_viewID:TableViewId, ACCESSED_BY_LIST:bool=False, SHOW_ALL:bool=False) -> None:
        '''
        Este método hace lo siguiente:
        - Limpia las variables de IDs asociadas con el QTableView y su selección.
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
        count_params:tuple[Any] = None
        
        data_sql:str = "" # consulta que pide los registros
        data_params:tuple[Any] = None
        
        _from_datetime:str # variables usadas cuando se llena la tabla de Ventas, 
        _to_datetime:str # sirven para marcar las fechas iniciales y finales
                
        # crea las consultas para obtener el COUNT de filas y los registros 
        # para llenar la tabla
        match table_viewID.name:
            case "INVEN_TABLE_VIEW":
                self.ui.tv_inventory_data.selectionModel().clearSelection()
                
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
                _from_datetime = self.ui.dateEdit_from_date.date().toString(
                    DateAndTimeFormat.LOCAL_DATE_FORMAT.value
                )
                _to_datetime = self.ui.dateEdit_to_date.date().toString(
                    DateAndTimeFormat.LOCAL_DATE_FORMAT.value
                )
                
                _from_datetime = f"{_from_datetime} 00:00:00"
                _to_datetime = f"{_to_datetime} 23:59:59"
                
                _from_datetime = local_to_ISO8601(_from_datetime)
                _to_datetime = local_to_ISO8601(_to_datetime)
                
                self.ui.tv_sales_data.selectionModel().clearSelection()
                
                count_sql, data_sql = getTableViewsSqlQueries(
                    table_viewID=TableViewId.SALES_TABLE_VIEW
                )
                count_params = (_from_datetime, _to_datetime)
                data_params = (_from_datetime, _to_datetime)
                self.ui.label_feedbackSales.hide()

            case "DEBTS_TABLE_VIEW":
                self.ui.tv_debts_data.selectionModel().clearSelection()
                
                count_sql, data_sql = getTableViewsSqlQueries(
                    table_viewID=TableViewId.DEBTS_TABLE_VIEW
                )
                self.ui.label_feedbackDebts.hide()
        
        self.__initSelectWorker(
            table_viewID=table_viewID,
            data_sql=data_sql,
            data_params=data_params,
            count_sql=count_sql,
            count_params=count_params
        )
        return None
    
    
    def __initSelectWorker(self, table_viewID:TableViewId, data_sql:str, 
                           data_params:tuple, count_sql:str, 
                           count_params:tuple) -> None:
        '''
        Instancia un **Worker** para realizar las consultas de tipo **SELECT** 
        a la base de datos de forma asíncrona; conecta sus señales y slots.

        Parámetros
        ----------
        table_viewID : TableViewId
            **QTableView** al que se referencia
        data_sql : str
            Consulta de tipo **SELECT**
        data_params : tuple
            Parámetros de la consulta **SELECT**
        count_sql : str
            Consulta de tipo **SELECT COUNT()** para obtener la cantidad de 
            registros coincidentes
        count_params : tuple
            Parámetros de la consulta **SELECT COUNT()**
        '''
        self.select_worker = WorkerSelect(
            data_sql=data_sql,
            data_params=data_params,
            count_sql=count_sql,
            count_params=count_params
        )
        
        self.select_worker.countFinished.connect(
            lambda model_shape: self.__workerSelectOnCountFinished(
                table_viewID=table_viewID,
                model_shape=model_shape
            )
        )
        self.select_worker.registerProgress.connect(
            lambda register: self.__workerSelectOnRegisterProgress(
                register=register,
                table_viewID=table_viewID
            )
        )
        self.select_worker.finished.connect(
            lambda: self.__workerSelectOnFinished(
                table_viewID=table_viewID
            )
        )
        
        self.worker_manager.addTask(
            worker=self.select_worker,
            priority=WorkerPriority.MEDIUM
        )
        
        return None
    
    
    @Slot(object, tuple)
    def __workerSelectOnCountFinished(self, table_viewID:TableViewId, 
                                model_shape:tuple[int, int]=None) -> None:
        '''
        Instancia un acumulador **numpy.array** para los datos del modelo, y 
        actualiza el estado del **QProgressBar** asociado al **QTableView**.

        Parámetros
        ----------
        table_viewID : TableViewID
            QTableView que se referencia
        model_shape : tuple[int, int]
            Dimensiones del modelo de datos, se usa para instanciar el 
            acumulador
        '''
        self.__setNpDataAccumulator(
            table_viewID=table_viewID,
            model_shape=model_shape
        )
        
        self.startProgressBar(
            table_viewID=table_viewID,
            max_val=model_shape[0]
        )
        return None
    
    
    @Slot(tuple, object)
    def __workerSelectOnRegisterProgress(self, register:tuple[Any], 
                                   table_viewID:TableViewId) -> None:
        '''
        Guarda los IDs necesarios de cada registro, acumula los registros en 
        una variable y actualiza la **QProgressBar** asociada a esa tabla.

        Parámetros
        ----------
        register : tuple[Any]
            El registro obtenido de la consulta SELECT, la posición [0] 
            contiene el progreso de lectura de registros
        table_viewID : TableViewID
            **QTableView** al que se referencia
        '''
        match table_viewID.name:
            case "INVEN_TABLE_VIEW":
                # actualiza la barra de progeso
                self.updateProgressBar(
                    table_viewID=table_viewID,
                    value=register[0]
                )

                # guarda en la posición actual el registro completo
                self._inv_model_data_acc[register[0]] = register[1]
            
            case "SALES_TABLE_VIEW":
                # actualiza la barra de progeso
                self.updateProgressBar(
                    table_viewID=table_viewID,
                    value=register[0]
                )
                
                # intenta convertir la fecha y hora a objeto 'datetime'
                _id, _date_time = register
                try:
                    dt = datetime.strptime(_date_time[-1], DateAndTimeFormat.DIR_DATETIME_ISO_8601.value)
                    _date_time = list(_date_time)
                    _date_time[-1] = dt.strftime(DateAndTimeFormat.DIR_LOCAL_DATETIME_FORMAT.value)
                
                except (ValueError, TypeError) as err:
                    logging.error(f"Error al convertir fecha y hora a objeto 'datetime': {err}")
                    _date_time = register[1]
                
                finally:
                    register = (_id, _date_time)
                
                # guarda en la posición actual el registro completo
                self._sales_model_data_acc[register[0]] = register[1]
            
            case "DEBTS_TABLE_VIEW":
                self.updateProgressBar(
                    table_viewID=table_viewID,
                    value=register[0]
                )
                
                self._debts_model_data_acc[register[0]] = register[1]
        
        return None
    
    
    @Slot(object, int)
    def startProgressBar(self, table_viewID:TableViewId, max_val:int) -> None:
        '''
        Inicia la **QProgressBar** correspondiente a la tabla especificada.

        Parámetros
        ----------
        table_viewID : TableViewID
            tabla a la que corresponde la barra de progreso
        max_val : int
            Valor máximo de la barra de progreso
        '''
        _progess_bar:QProgressBar
        
        match table_viewID:
            case TableViewId.INVEN_TABLE_VIEW:
                _progess_bar = self.ui.inventory_progressbar
            
            case TableViewId.SALES_TABLE_VIEW:
                _progess_bar = self.ui.sales_progressbar
                
            case TableViewId.DEBTS_TABLE_VIEW:
                _progess_bar = self.ui.debts_progressbar
        
        _progess_bar.show() if _progess_bar.isHidden() else None
        _progess_bar.setMaximum(max_val)
        return None
    
    
    @Slot(object, int)
    def updateProgressBar(self, table_viewID:TableViewId, 
                          value:int=None) -> None:
        '''
        Actualiza el valor del **QProgressBar** correspondiente a la tabla 
        especificada.

        Parámetros
        ----------
        table_viewID : TableViewID
            tabla a la que corresponde la barra de progreso
        value : int
            Valor actual de la barra de progreso
        '''
        _progress_bar:QProgressBar
        
        match table_viewID:
            case TableViewId.INVEN_TABLE_VIEW:
                _progress_bar = self.ui.inventory_progressbar
            
            case TableViewId.SALES_TABLE_VIEW:
                _progress_bar = self.ui.sales_progressbar
            
            case TableViewId.DEBTS_TABLE_VIEW:
                _progress_bar = self.ui.debts_progressbar
        
        _progress_bar.setValue(value + 1) if value < _progress_bar.maximum() else None
        return None
    
    
    @Slot(str)
    def __workerSelectOnFinished(self, table_viewID:TableViewId, 
                           READ_OPERATION:bool=True) -> None:
        '''
        Esconde la **QProgressBar** relacionada con la tabla, reinicia el 
        valor del *QSS* de dicha **QProgressBar** y carga los datos en la 
        tabla, finalmente reinicia los acumuladores temporales.
        
        Parámetros
        ----------
        table_viewID : TableViewId
            **QTableView** al que se referencia
        READ_OPERATION : bool, opcional
            determina si la operación a base de datos es de lectura, si no 
            es de lectura no reinicia el contenido de la tabla
        '''
        self.hideProgressBar(table_viewID)
        
        match table_viewID.name:
            case "INVEN_TABLE_VIEW":
                if READ_OPERATION:
                    self.inventory_data_model.setModelData(
                        data=self._inv_model_data_acc,
                        headers=ModelHeaders.INVENTORY_HEADERS.value
                    )
            
                # borra el acumulador temporal de datos
                self._inv_model_data_acc = None
            
            case "SALES_TABLE_VIEW":
                if READ_OPERATION:
                    self.sales_data_model.setModelData(
                        data=self._sales_model_data_acc,
                        headers=ModelHeaders.SALES_HEADERS.value
                    )
                
                # borra el acumulador temp. de datos
                self._sales_model_data_acc = None
            
            case "DEBTS_TABLE_VIEW":
                if READ_OPERATION:
                    self.debts_data_model.setModelData(
                        data=self._debts_model_data_acc,
                        headers=ModelHeaders.DEBTS_HEADERS.value
                    )
                
                self._debts_model_data_acc = None
        
        logging.debug(LoggingMessage.WORKER_SUCCESS)
        return None


    def hideProgressBar(self, table_viewID:TableViewId):
        '''
        Quita el estilo de la barra de progresos asociada a la tabla y la 
        esconde.

        Parámetros
        ----------
        table_viewID : TableViewId
            tabla a la que se referencia
        '''
        match table_viewID:
            case TableViewId.INVEN_TABLE_VIEW:
                self.ui.inventory_progressbar.setStyleSheet("")
                self.ui.inventory_progressbar.hide()
            
            case TableViewId.SALES_TABLE_VIEW:
                self.ui.sales_progressbar.setStyleSheet("")
                self.ui.sales_progressbar.hide()
            
            case TableViewId.DEBTS_TABLE_VIEW:
                self.ui.debts_progressbar.setStyleSheet("")
                self.ui.debts_progressbar.hide()
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
                debtorDialog = DebtorDataDialog(return_model_data=True)
                debtorDialog.setAttribute(Qt.WA_DeleteOnClose, True)
                
                debtorDialog.dataToInsert.connect(
                    lambda data_to_insert: self.insertDataIntoModel(
                        table_viewID=TableViewId.DEBTS_TABLE_VIEW,
                        data_to_insert=data_to_insert
                    )
                )

                debtorDialog.exec()
        
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
        '''
        match table_viewID.name:
            case 'INVEN_TABLE_VIEW':
                if self.inventory_data_model.modelHasData():
                    self.inventory_proxy_model.insertRows(
                        row=self.inventory_data_model.rowCount(),
                        count=1,
                        data_to_insert=data_to_insert
                    )
            
            case 'SALES_TABLE_VIEW':
                self.__updateStockOnSaleCreation(data_to_insert=data_to_insert)
                
                if self.sales_data_model.modelHasData():
                    self.sales_proxy_model.insertRows(
                        row=self.sales_data_model.rowCount(),
                        count=1,
                        data_to_insert=data_to_insert
                    )
            
            case 'DEBTS_TABLE_VIEW':
                if self.debts_data_model.modelHasData():
                    self.debts_proxy_model.insertRows(
                        row=self.debts_data_model.rowCount(),
                        count=1,
                        data_to_insert=data_to_insert
                    )
        
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
                self.inventory_data_model.index(0, InvViewCols.INV_PRODUCT_NAME.value), # busca desde la 1ra fila, 2da columna (de nombre).
                Qt.ItemDataRole.DisplayRole.value,          # devuelve la coincidencia como texto.
                data_to_insert['product_name'],             # el dato a buscar.
                1,                                          # cantidad de coincidencias para que deje de buscar.
                Qt.MatchFlag.MatchExactly                   # determina el criterio de búsqueda (debe ser exacto el string).
            )[0].row()                                      # obtengo del elemento [0] sólo el valor de la fila.
            
            if found_index_row is not None:
                # obtiene el stock en esa fila
                target_index = self.inventory_data_model.index(
                    found_index_row,
                    InvViewCols.INV_STOCK.value
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
    @Slot(object)
    def toggleDeleteButton(self, table_viewID:TableViewId) -> None:
        '''
        Verifica si hay elementos seleccionados en el MODELO DE SELECCIÓN de 
        la tabla especificada y habilita/deshabilita el botón de eliminar 
        registros asociado.

        Parámetros
        ----------
        table_viewID : TableViewId
            QTableView al que se referencia
        '''
        match table_viewID:
            case TableViewId.INVEN_TABLE_VIEW:
                self.ui.btn_delete_product_inventory.setEnabled(
                    self.ui.tv_inventory_data.selectionModel().hasSelection()
                )
            
            case TableViewId.SALES_TABLE_VIEW:
                self.ui.btn_delete_product_sales.setEnabled(
                    self.ui.tv_sales_data.selectionModel().hasSelection()
                )
            
            case TableViewId.DEBTS_TABLE_VIEW:
                self.ui.btn_delete_debtor.setEnabled(
                    self.ui.tv_debts_data.selectionModel().hasSelection()
                )
        return None
    
    
    # productos
    @Slot()
    def __removeInventoryModelRows(self) -> None:
        '''
        Elimina los productos seleccionados en el MODELO de inventario y 
        actualiza la VISTA, además actualiza la progress-bar asociada.
        '''
        selected_rows:tuple[int] = getSelectedTableRows(
            self.ui.tv_inventory_data
        )
        if not selected_rows:
            return None
        
        # preguntar antes de borrar
        ask_dialog = AskBeforeDeletion(
            parent=self,
            table_viewID=TableViewId.INVEN_TABLE_VIEW,
            reg_count=len(selected_rows)
        )
        
        if ask_dialog.exec() == ask_dialog.StandardButton.Yes:
            # cambia la progress-bar para representar las eliminaciones
            self.ui.inventory_progressbar.setMaximum(len(selected_rows))
            self.ui.inventory_progressbar.setStyleSheet(
                ProgressBarStyle.DELETION.value
            )
            
            # actualiza el MODELO de datos
            self.inventory_proxy_model.removeSelectedRows(selected_rows)
        return None
    
    
    @Slot(object)
    def confirmedInventoryRowsDeletion(self, base_model_rows_selected:tuple[int]) -> None:
        '''
        Instancia un **Worker** y un **QThread** para actualizar la base de 
        datos con los productos eliminados.
        
        **NOTA:** ÉSTE MÉTODO NO ELIMINA LOS REGISTROS DE LAS TABLAS 
        "*Productos*"  PARA EVITAR ERRORES EN LA BASE DE DATOS Y SÓLO LOS 
        MARCA COMO "*ELIMINADOS*".

        Parámetros
        ----------
        base_model_rows_selected : tuple[int]
            las filas mapeadas del MODELO BASE seleccionadas para eliminar en 
            la base de datos
        '''
        # instancia y ejecuta WORKER y THREAD
        self.deleteRowsFromDatabase(
            table_viewID=TableViewId.INVEN_TABLE_VIEW,
            ids=self.__getDeleteData(
                table_viewID=TableViewId.INVEN_TABLE_VIEW,
                selected_rows=base_model_rows_selected
            ),
            row_count=len(base_model_rows_selected)
        )
        return None


    # ventas
    @Slot()
    def __removeSalesModelRows(self) -> None:
        '''
        Elimina los productos seleccionados en el MODELO de ventas y actualiza 
        la VISTA, además actualiza la progress-bar asociada.
        '''
        # obtiene las filas seleccionadas
        selected_rows = getSelectedTableRows(self.ui.tv_sales_data)
        
        if not selected_rows:
            return None
        
        # preguntar antes de borrar
        ask_dialog = AskBeforeDeletion(
            parent=self,
            table_viewID=TableViewId.SALES_TABLE_VIEW,
            reg_count=len(selected_rows)
        )
        
        if ask_dialog.exec() == ask_dialog.StandardButton.Yes:
            # cambia la progress-bar para representar las eliminaciones
            self.ui.sales_progressbar.setMaximum(len(selected_rows))
            self.ui.sales_progressbar.setStyleSheet(
                ProgressBarStyle.DELETION.value
            )
            
            self.sales_proxy_model.removeSelectedRows(
                selected_rows=selected_rows
            )
        return None


    @Slot(object)
    def confirmedSalesRowsDeletion(self, base_model_rows_selected:tuple[int]) -> None:
        '''
        Instancia un **Worker** y un **QThread** para actualizar la base de 
        datos con los productos eliminados.
        NOTA: Este método NO ELIMINA LOS REGISTROS DE "Ventas", "Deudas" NI 
        "Detalle_Ventas" SINO QUE LOS MARCA COMO "ELIMINADOS" EN LA BASE DE 
        DATOS.

        Parámetros
        ----------
        base_model_rows_selected : tuple[int]
            las filas mapeadas del MODELO BASE seleccionadas para eliminar en 
            la base de datos
        '''
        self.deleteRowsFromDatabase(
            table_viewID=TableViewId.SALES_TABLE_VIEW, 
            ids=self.__getDeleteData(
                table_viewID=TableViewId.SALES_TABLE_VIEW,
                selected_rows=base_model_rows_selected
            ),
            row_count=len(base_model_rows_selected)
        )
        return None


    # deudas
    @Slot()
    def __removeDebtsModelRows(self) -> None:
        '''
        Elimina los deudores seleccionados en el MODELO de deudas y actualiza 
        la VISTA, además actualiza la progress-bar asociada. 
        Antes de eliminar registros advierte al usuario si se seleccionaron 
        cuentas corrientes con saldo acreedor/deudor.
        '''
        # obtiene las filas seleccionadas
        selected_rows = getSelectedTableRows(self.ui.tv_debts_data)
        _accounts_with_balance:list[list[str, str]]
        
        if not selected_rows:
            return None
        
        # preguntar antes de borrar
        ask_dialog = AskBeforeDeletion(
            parent=self,
            table_viewID=TableViewId.DEBTS_TABLE_VIEW,
            reg_count=len(selected_rows)
        )
        
        if ask_dialog.exec() != ask_dialog.StandardButton.Yes:
            return None
        
        # verifica si hay cuentas seleccionadas con balance no nulo
        _accounts_with_balance = self.__accountsThatHaveBalance(
            selected_accounts=selected_rows
        )
        if _accounts_with_balance:
            # advierte al usuario
            warn_dialog = WarnAccountHasBalance(
                selected_accounts=_accounts_with_balance
            )
            
            if warn_dialog.exec() != warn_dialog.DialogCode.Accepted:
                return None
        
        # cambia la progress-bar para representar las eliminaciones
        self.ui.debts_progressbar.setMaximum(len(selected_rows))
        self.ui.debts_progressbar.setStyleSheet(ProgressBarStyle.DELETION.value)
        
        self.debts_proxy_model.removeSelectedRows(selected_rows=selected_rows)
        return None
    
    
    def __accountsThatHaveBalance(self, selected_accounts:tuple[int]) -> list[list[str, str]]:
        '''
        Devuelve una lista con los nombres y apellidos de las cuentas 
        corrientes seleccionadas que tengan un saldo no nulo.
        
        Parámetros
        ----------
        selected_accounts : tuple[int]
            tupla con las filas seleccionadas
        
        Retorna
        -------
        list[list[str, str]]
            lista con los nombres y apellidos de las cuentas con saldo no 
            nulo
        '''
        _data:list[list[str, str]] = []
        _name:QModelIndex
        _surname:QModelIndex
        _balance:QModelIndex
        
        for acc_row in selected_accounts:
            _name = self.debts_proxy_model.index(
                acc_row, DebtorViewCols.DEBTS_NAME.value
            )
            _surname = self.debts_proxy_model.index(
                acc_row, DebtorViewCols.DEBTS_SURNAME.value
            )
            _balance = self.debts_proxy_model.index(
                acc_row, DebtorViewCols.DEBTS_BALANCE.value
            )
            
            if str(_balance.data(Qt.ItemDataRole.DisplayRole)).strip("$ ") not in ("0", "0.0"):
                _data.append(
                    [
                        _name.data(Qt.ItemDataRole.DisplayRole),
                        _surname.data(Qt.ItemDataRole.DisplayRole)
                    ]
                )
        
        return _data
    
    
    @Slot(object)
    def confirmedDebtsRowsDeletion(self, base_model_rows_selected:tuple[int]) -> None:
        '''
        Instancia un **Worker** y un **QThread** para actualizar la base de 
        datos con los deudores eliminados.
        NOTA: Este método NO ELIMINA LOS REGISTROS DE "Deudores", SINO QUE LOS 
        ANONIMIZA.

        Parámetros
        ----------
        base_model_rows_selected : tuple[int]
            las filas mapeadas del MODELO BASE seleccionadas para eliminar en 
            la base de datos
        '''
        self.deleteRowsFromDatabase(
            table_viewID=TableViewId.DEBTS_TABLE_VIEW, 
            ids=self.__getDeleteData(
                table_viewID=TableViewId.DEBTS_TABLE_VIEW,
                selected_rows=base_model_rows_selected
            ),
            row_count=len(base_model_rows_selected)
        )
        return None
    
    
    # generales
    def __getDeleteData(self, table_viewID:TableViewId, 
                        selected_rows:Iterable) -> Iterable[tuple | dict]:
        '''
        Obtiene los datos necesarios desde el MODELO de datos de la VISTA 
        específica para poder realizar las consultas.

        Parámetros
        ----------
        table_viewID : TableViewId
            QTableView al que se refencia
        selected_rows : Iterable
            las filas seleccionadas en la vista

        Retorna
        -------
        Iterable[tuple | dict]
            iterable con los datos necesarios para las consultas.
            Dependiendo de la tabla será:
            - INVENTARIO: una lista con tuplas(id_producto,)
            - VENTAS: un dict con {ids_detalle_ventas:[ids] , id_ventas:[ids] , id_deudas:[ids]}
            - CUENTAS CORRIENTES: una lista con tuplas (id_deudas,)
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
                    data.append( self.sales_data_model._data[row][0] )
                
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
                # obtiene los IDs de los Deudores y los convierte en tuple[ID]
                for row in selected_rows:
                    data.append( (self.debts_data_model._data[row][0],) )
                data = tuple(data)
        
        return data


    def deleteRowsFromDatabase(self, table_viewID:TableViewId,
                               ids:Iterable, row_count:int) -> None:
        '''
        Éste método maneja tanto las las consultas **DELETE** como las 
        consultas **UPDATE** que se usen para marcar como *"eliminado"* un 
        registro en alguna tabla de la base de datos.
        
        Este método hace lo siguiente:
        - Dependiendo de la tabla, declara las consultas **UPDATE** o 
        **DELETE**
        - Instancia e inicializa un **QThread** y un **Worker** para realizar 
        las operaciones
        - Limpia las variables de IDs asociadas con la tabla y su selección

        Parámetros
        ----------
        table_viewID : TableViewId
            QTableView que se referencia
        ids : Iterable
            IDs necesarios para las consultas; si la tabla es de Inventario 
            recibe un **tuple[ids]**, sino recibe un 
            **dict['id_tabla':tuple[id1,id2...]]**
        row_count : int
            cantidad de filas a eliminar del modelo; éste parámetro es usado 
            para inicializar la barra de progreso
        '''
        sql:str | tuple[str]
        params:tuple[Any] = None
        
        # crea las consultas para las operaciones UPDATE o DELETE
        match table_viewID:
            case TableViewId.INVEN_TABLE_VIEW:
                sql = '''UPDATE Productos 
                         SET eliminado = 1 
                         WHERE IDproducto = ?;'''
                params = ids
                
                self.ui.tv_inventory_data.selectionModel().clearSelection()
                self.ui.label_feedbackInventory.hide()

            case TableViewId.SALES_TABLE_VIEW:
                sql = (
                    '''UPDATE Detalle_Ventas 
                       SET eliminado = 1 
                       WHERE ID_detalle_venta = ?;''',
                    '''UPDATE Ventas 
                       SET eliminado = 1 
                       WHERE IDventa = ?;''',
                    '''UPDATE Deudas 
                       SET eliminado = 1 
                       WHERE IDdeuda = ?;'''
                    )
                params = ids
                
                self.ui.tv_sales_data.selectionModel().clearSelection()
                self.ui.label_feedbackSales.hide()

            case TableViewId.DEBTS_TABLE_VIEW:
                sql = (
                    ''' UPDATE Deudores 
                        SET nombre = '[ELIMINADO]',
                            apellido = '[ELIMINADO]',
                            num_telefono = NULL,
                            direccion = NULL,
                            codigo_postal = NULL
                        WHERE IDdeudor = ?;''',
                    ''' UPDATE Deudas
                        SET total_adeudado = 0,
                            eliminado = 1
                        WHERE IDdeudor = ?;'''
                    )
                params = ids
                        
                self.ui.tv_debts_data.selectionModel().clearSelection()
                self.ui.label_feedbackDebts.hide()
        
        # inicializa el worker
        self.__initDeleteWorker(
            table_viewID=table_viewID,
            del_sql=sql,
            del_params=params,
            row_count=row_count
        )
        return None
    
    
    def __initDeleteWorker(self, table_viewID:TableViewId,
                           del_sql:str | tuple[str],
                           del_params:Iterable[tuple],
                           row_count:int) -> None:
        '''
        Instancia un *Worker* para realizar las consultas de tipo **DELETE | 
        UPDATE** a la base de datos de forma asíncrona; conecta sus señales y 
        slots.
        Las operaciones **UPDATE** mencionadas son aquellas en las que se 
        marquen como *eliminados* algunos registros.

        Parámetros
        ----------
        table_viewID : TableViewId
            tabla a la que se refencia
        del_sql : str | tuple[str]
            consulta de tipo **DELETE | UPDATE**; será un **tuple[str]** cuando 
            se eliminen filas de la sección de Ventas o Deudas, ya que en esos 
            casos se tienen que borrar filas de más de una tabla
        del_params: Iterable[tuple]
            parámetros de la consulta **DELETE | UPDATE**
        row_count : int
            cantidad de filas a eliminar del modelo; éste parámetro es usado 
            para inicializar la barra de progreso
        '''
        self.delete_worker:WorkerDelete
        
        match table_viewID:
            case TableViewId.INVEN_TABLE_VIEW:
                self.delete_worker = WorkerDelete(
                    table_viewID=table_viewID,
                    del_sql=del_sql,
                    del_params=del_params
                )
            
            case _:
                self.delete_worker = WorkerDelete(
                    table_viewID=table_viewID,
                    mult_sql=del_sql,
                    del_params=del_params
                )
        
        self.delete_worker.thread().started.connect(
            self.startProgressBar(
                table_viewID=table_viewID,
                max_val=row_count
            )
        )
        self.delete_worker.progress.connect(
            lambda n: self.updateProgressBar(
                table_viewID=table_viewID,
                value=n
            )
        )
        self.delete_worker.finished.connect(
            lambda: self.hideProgressBar(table_viewID)
        )
        
        self.worker_manager.addTask(
            worker=self.delete_worker,
            priority=WorkerPriority.HIGH
        )
        return None


    #¡ tablas (UPDATE)
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
                self.ui.label_feedbackInventory.setStyleSheet(WidgetStyle.FIELD_INVALID_VAL.value)
                self.ui.label_feedbackInventory.setText(feedback[1])
                
            case "SALES_TABLE_VIEW":
                self.ui.label_feedbackSales.show()
                self.ui.label_feedbackSales.setStyleSheet(WidgetStyle.FIELD_INVALID_VAL.value)
                self.ui.label_feedbackSales.setText(feedback[1])
                
            case "DEBTS_TABLE_VIEW":
                self.ui.label_feedbackDebts.show()
                self.ui.label_feedbackDebts.setStyleSheet(WidgetStyle.FIELD_INVALID_VAL.value)
                self.ui.label_feedbackDebts.setText(feedback[1])
        return None
    
    
    #¡¡ ....... inventario ........................................................................
    @Slot(int, object)
    def onInventoryModelDataToUpdate(self, column:int,
                          new_values:tuple[int, Any]) -> None:
        '''
        Actualiza la base de datos con el valor nuevo de Productos. En caso de 
        que las columnas sean de precio unitario o precio comercial también 
        actualiza el total adeudado en la tabla Deudas.
        
        Parámetros
        ----------
        column : int
            columna del item modificado
        new_values : tuple[int, Any]
            tupla con los valores nuevos de los items seleccionados, sigue el 
            formato *[IDproducto, valor]*; en caso que la columna sea la de 
            stock el *valor* será una tupla con *[stock, unidad de medida]*
        '''
        IDproduct:int = new_values[0]
        new_val:Any
        
        match column:
            case InvViewCols.INV_CATEGORY.value:
                new_val:str = new_values[1]
                
                with self._db_repo as db_repo:
                    db_repo.updateRegisters(
                        upd_sql='''UPDATE Productos 
                                SET IDcategoria = (
                                    SELECT IDcategoria FROM Categorias 
                                    WHERE nombre_categoria = ?) 
                                WHERE IDproducto = ?;''',
                        upd_params=(new_val, IDproduct,)
                        )
            
            case InvViewCols.INV_PRODUCT_NAME.value:
                new_val:str = new_values[1]
                
                with self._db_repo as db_repo:
                    db_repo.updateRegisters(
                        upd_sql='''UPDATE Productos 
                                SET nombre = ? 
                                WHERE IDproducto = ?;''',
                        upd_params=(new_val, IDproduct,)
                        )
            
            case InvViewCols.INV_DESCRIPTION.value:
                new_val:str = new_values[1]
                
                with self._db_repo as db_repo:
                    db_repo.updateRegisters(
                        upd_sql='''UPDATE Productos 
                                SET descripcion = ? 
                                WHERE IDproducto = ?;''',
                        upd_params=(new_val, IDproduct,)
                        )
            
            case InvViewCols.INV_STOCK.value:
                new_val:tuple[float, str] = new_values[1] # (stock, unidad de medida)
                
                with self._db_repo as db_repo:
                    db_repo.updateRegisters(
                        upd_sql='''UPDATE Productos 
                                   SET stock = ?,
                                       unidad_medida = ? 
                                   WHERE IDproducto = ?;''',
                        upd_params=(new_val[0], new_val[1], IDproduct,)
                        )
            
            case InvViewCols.INV_NORMAL_PRICE.value:
                new_val:float = new_values[1]
                
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
            
            case InvViewCols.INV_COMERCIAL_PRICE.value:
                new_val:float = new_values[1]
                
                # actualiza en Productos
                with self._db_repo as db_repo:
                    db_repo.updateRegisters(
                        upd_sql= '''UPDATE Productos
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
    
    
    def __updateDebtsOnPriceChange(self, price_type:InventoryPriceType, 
                                   params:tuple[int]=None) -> None:
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
        '''
        match price_type:
            case InventoryPriceType.NORMAL:
                # actualiza en Deudas
                with self._db_repo as db_repo:
                    db_repo.updateRegisters(
                        upd_sql= '''UPDATE Deudas 
                                    SET total_adeudado = CASE 
                                        WHEN deudas.eliminado = 0 AND Detalle_Ventas.abonado = 0 THEN Productos.precio_unit * Detalle_Ventas.cantidad 
                                        WHEN deudas.eliminado = 1 THEN deudas.total_adeudado 
                                        ELSE ROUND(Productos.precio_unit * Detalle_Ventas.cantidad - Detalle_Ventas.abonado, 2) 
                                    END 
                                    FROM Detalle_Ventas, Productos, Ventas 
                                    WHERE 
                                        Deudas.IDdeuda = Detalle_Ventas.IDdeuda AND 
                                        Productos.IDproducto = ? AND 
                                        Detalle_Ventas.IDproducto = Productos.IDproducto AND 
                                        Detalle_Ventas.IDventa = Ventas.IDventa AND 
                                        Ventas.detalles_venta LIKE "%(P. PÚBLICO)%";''',
                        upd_params=params
                    )
        
            case InventoryPriceType.COMERCIAL:
                # actualiza en Deudas
                with self._db_repo as db_repo:
                    db_repo.updateRegisters(
                        upd_sql= '''UPDATE Deudas 
                                    SET total_adeudado = CASE 
                                        WHEN deudas.eliminado = 0 AND Detalle_Ventas.abonado = 0 THEN Productos.precio_comerc * Detalle_Ventas.cantidad 
                                        WHEN deudas.eliminado = 1 THEN deudas.total_adeudado 
                                        ELSE ROUND(Productos.precio_comerc * Detalle_Ventas.cantidad - Detalle_Ventas.abonado, 2) 
                                    END 
                                    FROM Detalle_Ventas, Productos, Ventas 
                                    WHERE 
                                        Deudas.IDdeuda = Detalle_Ventas.IDdeuda AND 
                                        Productos.IDproducto = ? AND 
                                        Detalle_Ventas.IDproducto = Productos.IDproducto AND 
                                        Detalle_Ventas.IDventa = Ventas.IDventa AND 
                                        Ventas.detalles_venta LIKE "%(P. COMERCIAL)%";''',
                        upd_params=params
                    )
        return None
    
    
    #¡¡ ....... ventas ............................................................................
    @Slot(int, int, object, object)
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
            ID_detalle_venta en la base de datos del item modificado
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
        _datetime_to_iso:str
        
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
                            data_sql='''SELECT COALESCE(unidad_medida, '') 
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
                # intenta convertir a formato ISO 8601...
                _datetime_to_iso = local_to_ISO8601(new_val)
                _datetime_to_iso = new_val if not _datetime_to_iso else _datetime_to_iso
                
                with self._db_repo as db_repo:
                    db_repo.updateRegisters(
                        upd_sql='''UPDATE Ventas 
                                   SET fecha_hora = ? 
                                   WHERE IDventa = (
                                       SELECT IDventa 
                                       FROM Detalle_Ventas 
                                       WHERE ID_detalle_venta = ?);''',
                        upd_params=(_datetime_to_iso, IDsales_detail)
                    )
                    
                    db_repo.updateRegisters(
                        upd_sql='''UPDATE Deudas 
                                   SET fecha_hora = ? 
                                   WHERE IDdeuda = (
                                       SELECT IDdeuda 
                                       FROM Detalle_Ventas 
                                       WHERE ID_detalle_venta = ?);''',
                        upd_params=(_datetime_to_iso, IDsales_detail)
                    )
        
        return None


    #¡¡ ....... deudas ............................................................................
    @Slot(object)
    def __updateViewOnDebtsBalanceChanged(self, data:tuple[QModelIndex, float]) -> None:
        '''
        Actualiza el MODELO DE DATOS de Deudas con el nuevo balance de la 
        cuenta corriente.

        Parámetros
        ----------
        data : tuple[QModelIndex, float]
            tupla con el índice del elemento seleccionado y el nuevo balance 
            de la cuenta corriente
        '''
        self.debts_data_model.setData(
            index=data[0], value=data[1], role=Qt.ItemDataRole.EditRole
        )
        return None
    
    
    @Slot(int, int, object)
    def __onDebtsModelDataToUpdate(self, column:int, ID_debtor:int,
                                       new_val:Any) -> None:
        '''
        Actualiza la base de datos con el valor nuevo de la sección de Cuentas 
        Corrientes. 
        Además, si la columna modifica es la de "fecha y hora" actualiza 
        el nuevo horario tanto en la tabla "Ventas" como en "Deudas".
        NOTA: ÉSTE MÉTODO NO ACTUALIZA LA COLUMNA DE BALANCE, ESO ES HECHO 
        DESDE EL DIALOG DE LOS DETALLES DE LOS BALANCES.
        
        Parámetros
        ----------
        column : int
            Columna del item modificado
        ID_debtor : int
            IDdeudor en la base de datos del item modificado
        new_val : Any
            Valor nuevo del item
        '''
        match column:
            case DebtorViewCols.DEBTS_NAME.value:
                with self._db_repo as db_repo:
                    db_repo.updateRegisters(
                        upd_sql='''UPDATE Deudores 
                                   SET nombre = ? 
                                   WHERE IDdeudor = ?;''',
                        upd_params=(new_val, ID_debtor,)
                        )
            
            case DebtorViewCols.DEBTS_SURNAME.value:
                with self._db_repo as db_repo:
                    db_repo.updateRegisters(
                        upd_sql='''UPDATE Deudores 
                                   SET apellido = ? 
                                   WHERE IDdeudor = ?;''',
                        upd_params=(new_val, ID_debtor,)
                        )
            
            case DebtorViewCols.DEBTS_PHONE_NUMBER.value:
                with self._db_repo as db_repo:
                    db_repo.updateRegisters(
                        upd_sql='''UPDATE Deudores 
                                   SET num_telefono = ? 
                                   WHERE IDdeudor = ?;''',
                        upd_params=(new_val, ID_debtor,)
                        )
            
            case DebtorViewCols.DEBTS_DIRECTION.value:
                with self._db_repo as db_repo:
                    db_repo.updateRegisters(
                        upd_sql='''UPDATE Deudores 
                                   SET direccion = ? 
                                   WHERE IDdeudor = ?;''',
                        upd_params=(new_val, ID_debtor,)
                        )
            
            case DebtorViewCols.DEBTS_POSTAL_CODE.value:
                with self._db_repo as db_repo:
                    db_repo.updateRegisters(
                        upd_sql='''UPDATE Deudores 
                                   SET codigo_postal = ? 
                                   WHERE IDdeudor = ?;''',
                        upd_params=(new_val, ID_debtor,)
                        )
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
        actualiza el modelo de datos.
        Emite la señal *self.*
        '''
        percentage:float
        selected_indexes:list[QModelIndex]
        
        # obtiene el valor del lineedit
        try:
            percentage = float(
                self.ui.lineEdit_percentage_change.text().replace(",",".")
            )
            if not percentage:
                return None
        
        except ValueError:
            return None
        
        if self.ui.checkbox_unit_prices.isChecked():
            selected_indexes = self.__getInventoryMappedIndexes(
                column=InvViewCols.INV_NORMAL_PRICE
            )
        else:
            selected_indexes = self.__getInventoryMappedIndexes(
                column=InvViewCols.INV_COMERCIAL_PRICE
            )
        
        if not selected_indexes:
            return None
        
        # calcula y asigna al MODELO los precios nuevos
        self.__calculateNewPrices(
            percentage=percentage,
            selected_indexes=selected_indexes
        )
        return None


    def __getInventoryMappedIndexes(self, column:int) -> list[QModelIndex]:
        '''
        Obtiene los índices ya mapeados seleccionados en la VISTA para usarse 
        en el MODELO DE DATOS de Inventario.
        
        Parámetros
        ----------
        column : int
            la columna de la cual obtener los índices mapeados, sólo admite 
            las columnas de "precio normal" y "precio comercial"

        Retorna
        -------
        list[QModelIndex]
            lista con todos los índices meapeados del MODELO DE DATOS BASE
        '''
        selected_rows:tuple[int] # filas seleccionadas
        table_view = self.ui.tv_inventory_data
        proxy_model = self.inventory_proxy_model
        
        # obtengo las filas seleccionadas
        selected_rows = getSelectedTableRows(tableView=table_view)
        
        # mapea los índices
        return [proxy_model.mapToSource(proxy_model.index(row, column)) for row in selected_rows]

    
    def __calculateNewPrices(self, percentage:float, 
                             selected_indexes:list[QModelIndex]) -> None:
        '''
        Calcula los aumentos/decrementos en los precios unitarios o 
        comerciales y actualiza el MODELO DE DATOS.
        
        Parámetros
        ----------
        percentage : float
            Porcentaje de incremento/decremento
        selected_indexes : list[QModelIndex]
            Índices seleccionados en la vista
        '''
        _idx_value:float
        _new_val:float
        
        # si está activada la checkbox de precios unitarios...
        if self.ui.checkbox_unit_prices.isChecked():
            for idx in selected_indexes:
                _idx_value = float(
                    idx.data(Qt.ItemDataRole.DisplayRole).replace(",",".")
                )
                
                # asigna el valor nuevo al modelo
                _new_val = round(_idx_value + (_idx_value * percentage / 100), 2)
                self.inventory_data_model.setData(
                    index=idx,
                    value=_new_val
                )
        
        # sino, si está activada la checkbox de precios comerciales...
        else:
            for idx in selected_indexes:
                _idx_value = idx.data(Qt.ItemDataRole.DisplayRole).replace(",",".")
                
                if _idx_value:
                    _idx_value = float(_idx_value)
                    _new_val = round(_idx_value + (_idx_value * percentage / 100), 2)
                
                else:
                    _new_val = 0.0
                
                self.inventory_data_model.setData(
                    index=idx,
                    value=_new_val
                )
        return None


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
        'MainWindow', la hora en el QDateTimeEdit del formulario y valida que 
        todos los demás sean válidos para poder mostrar el total de la venta.

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
        
        self.ui.dateTimeEdit_sale.setDateTime(QDateTime.currentDateTime())
        
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
                and all([item[SaleFields.IS_ALL_VALID.name] for item in self.DICT_ITEMS_VALUES.values()]) ):
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
        subtotals = [subtotal[SaleFields.SUBTOTAL.name] for subtotal in self.DICT_ITEMS_VALUES.values()]
        
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
    
    
    #* finalizando venta
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
        total_paid:float
        
        # fecha y hora en formato ISO8601
        _dt:datetime = local_to_ISO8601(self.ui.dateTimeEdit_sale.text())
        _dt = self.ui.dateTimeEdit_sale.text() if not _dt else _dt
        
        # obtengo el total pagado
        total_paid = self.ui.lineEdit_paid.text().replace(",",".")
        total_paid = float(total_paid if total_paid else 0.0)
        
        # si lo abonado es menor al total muestra el Dialog para manejar deudores
        if total_paid < self.TOTAL_COST:
            dialog = DebtorDataDialog()
            dialog.setAttribute(Qt.WA_DeleteOnClose, True)
            
            dialog.debtorChosen.connect(lambda debtor_id: self.finishedSaleOnDebtorChosen(
                    debtor_id=debtor_id,
                    total_paid=total_paid,
                    dt_iso8601=_dt
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
                        ins_params=(_dt,
                                    item[SaleFields.SALE_DETAILS.name],)
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
                            ins_params=(item[SaleFields.QUANTITY.name],
                                        item[SaleFields.SUBTOTAL.name],
                                        item[SaleFields.PRODUCT_NAME.name],
                                        _dt,
                                        item[SaleFields.SALE_DETAILS.name],
                                        item[SaleFields.SUBTOTAL.name],)
                    )
                        
                    # actualiza en Productos
                    db_repo.updateRegisters(
                        upd_sql= '''UPDATE Productos 
                                    SET stock = stock - ? 
                                    WHERE nombre = ?;''',
                        upd_params= (item[SaleFields.QUANTITY.name],
                                    item[SaleFields.PRODUCT_NAME.name],)
                    )
            
            # hace los reinicios necesarios para otras ventas
            self.__resetFieldsOnFinishedSale()
        
        return None


    @Slot(tuple)
    def finishedSaleOnDebtorChosen(self, debtor_id:int, total_paid:float, dt_iso8601:datetime) -> None:
        '''
        Cuando se termina una venta y hay deuda se invoca este método.
        
        Este método hace lo siguiente:
            - Obtiene los datos de los campos de los items y hace las consultas 
            INSERT a Ventas, Detalle_Ventas y Deudas y la consulta UPDATE a 
            Productos con el nuevo stock.
            
            NOTA: ESTE MÉTODO NO HACE CONSULTA ALGUNA A LA TABLA "Deudores", ESAS 
            CONSULTAS SON HECHAS EN EL DIALOG 'DebtorDataDialog'.
            
            - Al finalizar realiza los reinicios necesarios.
        
        Parámetros
        ----------
        debtor_id : int
            el 'IDdeudor' del deudor
        total_paid : float
            el total abonado al finalizar la venta
        dt_iso8601 : datetime
            fecha y hora del momento de la venta en formato ISO8601
        
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
        
        with self._db_repo as db_repo:        
            # recorre cada producto y hace las consultas INSERT y UPDATE (a Productos)
            for product in self.DICT_ITEMS_VALUES.values():
                db_repo.insertRegister(
                    ins_sql= '''INSERT INTO Ventas(
                                    fecha_hora,
                                    detalles_venta) 
                                VALUES(?,?);''',
                    ins_params=(dt_iso8601,
                                product["SALE_DETAILS"],)
                )
                
                # actualiza el total debido
                total_due -= product["SUBTOTAL"] # deuda = total abonado - subtotal
                total_due = round(total_due, 2)
                
                # Deudas y Detalle_Ventas (con IDdeuda)
                if total_due < 0: # el producto es deuda
                    db_repo.insertRegister(
                        ins_sql= '''INSERT INTO Deudas(
                                        fecha_hora,
                                        total_adeudado,
                                        IDdeudor,
                                        eliminado) 
                                    VALUES(?, ?, ?, 0);''',
                        ins_params=(dt_iso8601,
                                    abs(total_due),
                                    debtor_id)
                    )
                    
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
                                            AND IDdeudor = ? 
                                         ORDER BY IDdeuda DESC LIMIT 1)
                                    );''',
                        ins_params=(product["QUANTITY"],
                                    product["SUBTOTAL"],
                                    product["PRODUCT_NAME"],
                                    dt_iso8601,
                                    product["SALE_DETAILS"],
                                    round(product["SUBTOTAL"] - abs(total_due), 2),
                                    dt_iso8601,
                                    debtor_id,)
                    )
                    
                    total_due = 0
                
                else: # el producto NO es deuda
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
                                        NULL
                                    );''',
                        ins_params=(product["QUANTITY"],
                                    product["SUBTOTAL"],
                                    product["PRODUCT_NAME"],
                                    dt_iso8601,
                                    product["SALE_DETAILS"],
                                    product["SUBTOTAL"],)
                    )
                    
                # como última consulta de cada producto, actualiza el stock
                db_repo.updateRegisters(
                    upd_sql= '''UPDATE Productos 
                                SET stock = stock - ? 
                                WHERE nombre = ?;''',
                    upd_params=(product["QUANTITY"],
                                product["PRODUCT_NAME"],)
                )
        
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
        return None
    
    
    #* dateedit para mostrar recaudado por día
    @Slot()
    def setInitialDateRange(self) -> None:
        '''
        Al cambiar a la pestaña de la tabla de Ventas coloca el rango de 
        fechas de los **QDateEdits** desde el inicio de semana hasta el día 
        actual.
        '''
        with QSignalBlocker(self.ui.dateEdit_from_date):
            #? le cambio el máximo temporalmente porque sino no deja colocar 
            #? correctamente la fecha a veces (luego, en 'validateDateRange' 
            #? se corrige este cambio...
            self.ui.dateEdit_from_date.setMaximumDate(
                QDate.currentDate()
            )
            self.ui.dateEdit_from_date.setDate(
                getWeekStartDate(
                    QDate.currentDate()
                )
            )
        
        with QSignalBlocker(self.ui.dateEdit_to_date):
            # ? ... y acá cambio temporalmente la fecha mínima por la mismo
            self.ui.dateEdit_to_date.setMinimumDate(
                QDate.currentDate()
            )
            self.ui.dateEdit_to_date.setDate(
                QDate().currentDate()
            )
        
        # vuelve a validar los rangos
        self.validateDateRange(
            dateedit=self.ui.dateEdit_from_date,
            date=self.ui.dateEdit_from_date.date()
        )
        self.validateDateRange(
            dateedit=self.ui.dateEdit_to_date,
            date=self.ui.dateEdit_to_date.date()
        )
        return None
    
    
    @Slot(QDate)
    def showCollectedInDay(self, date:QDate) -> None:
        '''
        Muestra lo recaudado en el día seleccionado.

        Parámetros
        ----------
        date : QDate
            la fecha seleccionada
        '''
        collected:float
        _datetime_to_iso:str
        
        with self._db_repo as db_repo:
            _datetime_to_iso = date.toString(DateAndTimeFormat.DATE_ISO_8601.value)
            
            collected = db_repo.selectRegisters(
                data_sql='''SELECT COALESCE(ROUND(SUM(dv.costo_total), 2), 0)
                            FROM Detalle_Ventas AS dv
                            INNER JOIN Ventas AS v ON dv.IDventa = v.IDventa 
                            WHERE v.fecha_hora LIKE ? AND v.eliminado <> 1;''',
                data_params=(str(_datetime_to_iso) + "%",)
            )[0][0]
        
        self.ui.label_show_collected_by_day.setText(
            f'''<html>
                    <head/>
                    <body>
                        <p>
                            <span style='{WidgetStyle.LABEL_RICHTEXT_NEUTRAL.value}'> TOTAL=</span>
                            <span style='{WidgetStyle.LABEL_RICHTEXT_CONTENT.value}'>{str(collected).replace(".",",")}</span>
                        </p>
                    </body>
                </html>'''
            )
        return None
    
    
    #* dateedits de rango de fechas
    @Slot(QDateEdit, QDate)
    def validateDateRange(self, dateedit:QDateEdit, date:QDate) -> None:
        '''
        Actualiza el rango de fechas seleccionable entre los **QDateEdits** de 
        Ventas.

        Parámetros
        ----------
        dateedit : QDateEdit
            el *dateedit* modificado a partir del cual se actualiza el rango 
            de valores seleccionables del otro **QDateEdit** (si se modifica 
            la fecha inicial entonces se actualiza el rango de fechas para la 
            fecha final, y viceversa)
        date : QDate
            la fecha actual seleccionada
        '''
        match dateedit.objectName():
            case "dateEdit_from_date":
                self.ui.dateEdit_to_date.setMinimumDate(date)
                self.ui.dateEdit_to_date.setMaximumDate(
                    QDate(date).addDays(DateTimeRanges.MAX_DAYS_DIFF.value)
                )
            
            case "dateEdit_to_date":
                self.ui.dateEdit_from_date.setMaximumDate(date)
                self.ui.dateEdit_from_date.setMinimumDate(
                    QDate(date).addDays(-DateTimeRanges.MAX_DAYS_DIFF.value)
                )
        return None


    #¡### EVENTOS #####################################################
    def closeEvent(self, event):
        # guarda la geometría de la ventana
        self.config.saveMainWindowGeometry(self.size(), self.pos())
        
        # guarda el estado
        self.config.saveMainWindowState(self.saveGeometry(), self.saveState())
        
        return super().closeEvent(event)





def main():
    # logging
    with open("program.log", "w"): # borra los logs
        pass
    
    logging.basicConfig(
        format='%(asctime)s - (%(levelname)s) - %(module)s.%(funcName)s - %(message)s',
        level=logging.DEBUG,
        datefmt='%A %d/%m/%Y %H:%M:%S',
        handlers=[
            logging.FileHandler("program.log"),
            logging.StreamHandler()
        ]
    )
    
    # configuraciones
    settings = QSettings(
        ProgramValues.APP_NAME.value,
        ProgramValues.APP_AUTHOR.value
    )
    
    # base de datos
    createTables()
    ensureDateTimeISOformat()
    
    # app
    app = QApplication(sys.argv)
    
    # traducción al español
    translator = QTranslator()
    path = QLibraryInfo.path(QLibraryInfo.LibraryPath.TranslationsPath)
    translator.load("qtbase_es", path)
    app.installTranslator(translator)
    
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())



# MAIN #########################################################################################################
if __name__=='__main__':
    main()