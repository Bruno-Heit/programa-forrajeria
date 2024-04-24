import sys

from PySide6.QtWidgets import (QApplication, QMainWindow, QLineEdit, 
                               QCheckBox, QAbstractItemView, QDateTimeEdit, 
                               QListWidgetItem)
from PySide6.QtCore import (QModelIndex, Qt, QSize, QThread, Slot)
from PySide6.QtGui import (QIntValidator, QRegularExpressionValidator, QIcon)

from ui.ui_mainwindow import (Ui_MainWindow)
from utils.functionutils import *
from utils.classes import (ProductDialog, SaleDialog, ListItem, DebtorDataDialog, DebtsTablePersonData)
from utils.workerclasses import *
from utils.dboperations import *

from resources import (rc_icons)

from typing import (Any)
import logging


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("herramienta de gestión - Forrajería Torres")
        # ocultar widgets
        self.ui.side_bar_body.hide()
        self.ui.inventory_side_bar_body.hide()
        self.ui.label_feedbackInventory.hide()
        self.ui.label_feedbackChangePercentage.hide()
        self.ui.label_feedbackSales.hide()
        self.ui.inventory_progressbar.hide()
        self.ui.sales_progressbar.hide()
        self.ui.debts_progressbar.hide()

        # políticas de QTableWidgets
        setTableWidthPolitics(self.ui.displayTable)
        setTableWidthPolitics(self.ui.table_sales_data)
        setTableWidthPolitics(self.ui.table_debts)

        set_tables_ListWidgetItemsTooltip(self.ui.tables_ListWidget, getCategoriesDescription())

        # validators
        setSearchBarValidator(self.ui.inventory_searchBar)
        setSearchBarValidator(self.ui.sales_searchBar)
        setSearchBarValidator(self.ui.debts_searchBar)

        self.ui.lineEdit_percentage_change.setValidator(QIntValidator(-9_999_999, 99_999_999, self.ui.lineEdit_percentage_change))
        paid_validator = QRegularExpressionValidator("[0-9]{0,9}(\.|,)?[0-9]{0,2}", parent=self.ui.lineEdit_paid)
        self.ui.lineEdit_paid.setValidator(paid_validator)

        # añade íconos a los widgets
        self.addIconsToWidgets()

        # variables de inventario
        self.IDs_products:list = [] # var. de 'displayTable' que tiene los IDs de los productos
        self.cb_categories:list[str] = getProductsCategories()
        

        # variables de ventas
        self.ui.dateTimeEdit_sale.setDateTime(QDateTime.currentDateTime())
        
        self.IDs_saleDetails:list = [] # var. de 'table_sales_data' que tiene los IDs de las ventas en Detalle_Ventas
        self.items_objectNames:int = 0 # "ID" en los 'objectName', al crearse un item el nombre se da a partir del contador
        self.VALID_ITEMS:dict[str:bool] = {} # se usa para verificar si todos los ListItems son válidos para habilitar/deshabilitar 'btn_end_sale'
        self.ITEMS_VALUES:dict[str:tuple[str,str,bool,str,str,str,float]] = {} # tiene los valores de cada ListItem
        self.debtor_chosen:tuple[int,str,str] = None # tiene el ID, nombre y apellido del deudor elegido en DebtorDataDialog


        # variables de deudas
        
        # TODO: mostrar deudas
        # TODO: permitir agregar deuda
        # TODO: permitir eliminar deuda
        # TODO: permitir modificar deuda
        
        
        #?### VARIABLES DE MULTITHREADING ################################
        # self.READ_THREAD:QThread = QThread()
        

        #*## SEÑALES #####################################################
        #--- INVENTARIO --------------------------------------------------
        self.ui.btn_side_barToggle.clicked.connect(lambda: toggleSideBar(self.ui.side_bar, self.ui.centralwidget, self.ui.side_bar_body))
        
        self.ui.btn_inventory_sideBarToggle.clicked.connect(lambda: toggleSideBar(self.ui.inventory_sideBar, self.ui.main_inventory_frame, self.ui.inventory_side_bar_body, 200))
        
        # (READ) cargar con productos 'displayTable'
        self.ui.tables_ListWidget.itemClicked.connect(lambda: self.handleTableToFill(self.ui.displayTable, ACCESSED_BY_LIST=True))
        self.ui.tables_ListWidget.itemActivated.connect(lambda: self.handleTableToFill(self.ui.displayTable, ACCESSED_BY_LIST=True))

        self.ui.inventory_searchBar.returnPressed.connect(lambda: self.handleTableToFill(self.ui.displayTable, self.ui.inventory_searchBar))

        # (CREATE) añadir nuevo producto a tabla 'displayTable'
        self.ui.btn_add_product_inventory.clicked.connect(lambda: self.handleTableCreateRow(self.ui.displayTable))
        
        # (DELETE) eliminar un producto de 'displayTable'
        self.ui.btn_delete_product_inventory.clicked.connect(lambda: self.handleTableDeleteRows(self.ui.displayTable))
        
        # (UPDATE) modificar celdas de 'displayTable'
        self.ui.displayTable.doubleClicked.connect(lambda: self.handleTableUpdateItem(self.ui.displayTable, self.ui.displayTable.currentIndex()) )
        
        # cambio de selección
        self.ui.displayTable.itemSelectionChanged.connect(lambda: self.handleSelectionChange(self.ui.displayTable))
        
        # inventory_sideBar
        self.ui.inventory_checkbuttons_buttonGroup.buttonPressed.connect(self.handlePressedCheckbutton)
        self.ui.inventory_checkbuttons_buttonGroup.buttonClicked.connect(self.handleClickedCheckbutton)
        
        self.ui.checkbox_unit_prices.stateChanged.connect(self.handleCheckboxStateChange)
        
        self.ui.checkbox_comercial_prices.stateChanged.connect(self.handleCheckboxStateChange)
        
        self.ui.lineEdit_percentage_change.editingFinished.connect(self.handleLineeditPercentageEditingFinished)

        #--- VENTAS ------------------------------------------------------
        # (READ) cargar con ventas 'table_sales_data'
        self.ui.tab2_toolBox.currentChanged.connect(lambda curr_index: self.handleTableToFill(self.ui.table_sales_data, SHOW_ALL=True) if curr_index == 1 else None)
        
        self.ui.sales_searchBar.returnPressed.connect(lambda: self.handleTableToFill(self.ui.table_sales_data, self.ui.sales_searchBar))
        
        self.ui.tabWidget.currentChanged.connect(lambda index: self.ui.tab2_toolBox.setCurrentIndex(0) if index == 1 else None)
        
        # TODO: en classes.py, seguir colocando validators, luego seguir refactorizando el código a partir de acá
        # (CREATE) añadir una venta a 'table_sales_data'
        self.ui.btn_add_product_sales.clicked.connect(lambda: self.handleTableCreateRow(self.ui.table_sales_data))
        # (DELETE) eliminar ventas de 'table_sales_data'
        self.ui.btn_delete_product_sales.clicked.connect(lambda: self.handleTableDeleteRows(self.ui.table_sales_data))
        # (UPDATE) modificar celdas de 'table_sales_data'
        self.ui.table_sales_data.doubleClicked.connect(lambda: self.handleTableUpdateItem(self.ui.table_sales_data, self.ui.table_sales_data.currentIndex()) )
        self.ui.table_sales_data.itemSelectionChanged.connect(lambda: self.handleSelectionChange(self.ui.table_sales_data))
        
        # formulario de ventas
        self.ui.btn_add_product.clicked.connect(self.addSalesInputListItem)
        
        self.ui.btn_end_sale.clicked.connect(self.handleFinishedSale)

        self.ui.lineEdit_paid.editingFinished.connect(lambda: self.validateSalesFields(None))

        #--- DEUDAS ------------------------------------------------------
        self.ui.tabWidget.currentChanged.connect(lambda curr_index: self.handleTableToFill(self.ui.table_debts, SHOW_ALL=True) if curr_index == 2 else None)




    #*## MÉTODOS #####################################################
    # método que coloca íconos a los widgets
    def addIconsToWidgets(self) -> None:
        '''Simplemente le coloca los íconos que le corresponde a cada Widget. Retorna 'None'.'''
        icon:QIcon = QIcon()
        icon.addFile(":/icons/menu-white.svg")
        self.ui.btn_side_barToggle.setIcon(icon)
        self.ui.btn_inventory_sideBarToggle.setIcon(icon)

        icon.addFile(":/icons/plus-white.svg")
        self.ui.btn_add_product_inventory.setIcon(icon)

        icon.addFile(":/icons/minus-circle-white.svg")
        self.ui.btn_delete_product_inventory.setIcon(icon)

        icon.addFile(":/icons/plus-white.svg")
        self.ui.btn_add_product.setIcon(icon)

        icon.addFile(":/icons/check-white.svg")
        self.ui.btn_end_sale.setIcon(icon)

        icon.addFile(":/icons/plus-white.svg")
        self.ui.btn_add_product_sales.setIcon(icon)

        icon.addFile(":/icons/minus-circle-white.svg")
        self.ui.btn_delete_product_sales.setIcon(icon)

        icon.addFile(":/icons/plus-white.svg")
        self.ui.btn_add_debt.setIcon(icon)

        icon.addFile(":/icons/minus-circle-white.svg")
        self.ui.btn_delete_debt.setIcon(icon)

        return None


    #?================ MULTITHREADING ================
    #¡ tablas (READ)
    @Slot(QTableWidget,QLineEdit,bool)
    def handleTableToFill(self, table_widget:QTableWidget, search_bar:QLineEdit=None, ACCESSED_BY_LIST:bool=False, SHOW_ALL:bool=False) -> None:
        '''
        Este método hace lo siguiente:
        - Limpia el 'table_widget'.
        - Limpia las variables de IDs asociadas con 'table_widget'.
        - Dependiendo del 'table_widget' que se tenga que llenar, se encarga de declarar las consultas sql y los 
        parámetros necesarios para luego hacer las consultas en la clase 'workerclasses.DbReadWorker'.
        - Crea una instancia de WORKER y QThread y conecta sus señales/slots.
        
        NO LLAMA A NINGÚN OTRO MÉTODO.

        PARAMS:
        - table_widget: el QTableWidget que se referencia.
        - search_bar: determina si se usó una barra de búsqueda, y cuál fue.
        - ACCESSED_BY_LIST: flag que será True si se seleccionó un item desde 'tables_ListWidget', sino False. 
        Por defecto es False.
        - SHOW_ALL: flag que determina si mostrar todos los elementos de un 'table_widget'. Por defecto es False.

        Retorna 'None'.
        '''
        
        count_sql:str = "" # consulta de tipo COUNT()
        count_params:tuple[Any] = None # params de la consulta COUNT()
        
        sql:str = "" # consulta que pide los registros
        params:tuple[Any] = None # params de la consulta de registros
        
        text:str = None # var. auxiliar; se usa esta variable si se llena la tabla usando un search_bar
        
        # limpia la tabla
        table_widget.clearContents()
        table_widget.setRowCount(0)
        
        # crea las consultas para obtener el COUNT() de filas y los registros para llenar la tabla
        match table_widget.objectName():
            case "displayTable":
                self.IDs_products.clear() # limpia los IDs
                
                # si se seleccionó una categoría desde 'tables_ListWidget', cambia hacia la pestaña de inventario...
                if ACCESSED_BY_LIST:
                    self.ui.tabWidget.setCurrentWidget(self.ui.tabWidget.findChild(QWidget, "tab1_inventory"))

                # si NO se usa una barra de búsqueda...
                if not search_bar:
                    if SHOW_ALL or self.ui.tables_ListWidget.currentItem().text() == "MOSTRAR TODOS":
                        count_sql:str = "SELECT COUNT(*) FROM Productos WHERE eliminado = 0;"
                        sql = "SELECT IDproducto,nombre_categoria,nombre,p.descripcion,stock,unidad_medida,precio_unit,precio_comerc FROM Productos AS p INNER JOIN Categorias AS c WHERE p.IDcategoria=c.IDcategoria AND p.eliminado = 0;"
                    elif not SHOW_ALL and ACCESSED_BY_LIST:
                        # cols.: detalle venta, cantidad, producto, costo total, abonado, fecha y hora
                        count_sql = "SELECT COUNT(*) FROM Productos WHERE IDcategoria = (SELECT IDcategoria FROM Categorias WHERE nombre_categoria = ? ) AND eliminado = 0;"
                        count_params = (self.ui.tables_ListWidget.currentItem().text(),)
                        sql = "SELECT IDproducto,nombre_categoria,nombre,p.descripcion,stock,unidad_medida,precio_unit,precio_comerc FROM Productos AS p INNER JOIN Categorias AS c WHERE p.IDcategoria=c.IDcategoria AND c.nombre_categoria=? AND eliminado = 0;"
                        params = (self.ui.tables_ListWidget.currentItem().text(),)
                    
                # TODO: al usar search_bar, cambiar %{text}% por ?, para evitar sql injections.
                
                # si SÍ se usa una barra de búsqueda...
                elif search_bar:
                    text:str = self.ui.inventory_searchBar.text()
                    count_sql = f"SELECT COUNT(*) FROM Productos AS p LEFT JOIN Categorias AS c WHERE p.eliminado = 0 AND p.IDcategoria=c.IDcategoria AND (nombre_categoria LIKE '%{text}%' OR nombre LIKE '%{text}%' OR p.descripcion LIKE '%{text}%' OR stock LIKE '%{text}%' OR unidad_medida LIKE '%{text}%' OR precio_unit LIKE '%{text}%' OR precio_comerc LIKE '%{text}%');"
                    sql = f"SELECT IDproducto,nombre_categoria,nombre,p.descripcion,stock,unidad_medida,precio_unit,precio_comerc FROM Productos AS p LEFT JOIN Categorias AS c WHERE p.eliminado = 0 AND p.IDcategoria=c.IDcategoria AND (nombre_categoria LIKE '%{text}%' OR  nombre LIKE '%{text}%' OR  p.descripcion LIKE '%{text}%' OR  stock LIKE '%{text}%' OR unidad_medida LIKE '%{text}%' OR precio_unit LIKE '%{text}%' OR precio_comerc LIKE '%{text}%');"
                self.ui.label_feedbackInventory.hide()


            case "table_sales_data":
                self.IDs_saleDetails.clear() # limpia los IDs
                
                # si no se usa la 'search bar'...
                if not search_bar and SHOW_ALL:
                    count_sql = "SELECT COUNT(*) FROM Detalle_Ventas as dv LEFT JOIN Productos AS p ON dv.IDproducto = p.IDproducto LEFT JOIN Ventas AS v ON dv.IDventa = v.IDventa;"
                    sql = "SELECT dv.ID_detalle_venta, v.detalles_venta, p.nombre, dv.cantidad, p.unidad_medida, dv.costo_total, dv.abonado, v.fecha_hora FROM Detalle_Ventas as dv LEFT JOIN Productos AS p ON dv.IDproducto = p.IDproducto LEFT JOIN Ventas AS v ON dv.IDventa = v.IDventa;"
                # en cambio, si SÍ se usa...
                else:
                    text:str = self.ui.sales_searchBar.text()
                    count_sql = f'SELECT COUNT(*) FROM Detalle_Ventas AS dv, Productos AS p, Ventas AS v WHERE (dv.IDproducto = p.IDproducto AND dv.IDventa = v.IDventa) AND (v.Detalles_venta LIKE "%{text}%" OR p.nombre LIKE "%{text}%" OR cantidad LIKE "%{text}%" OR p.unidad_medida LIKE "%{text}%" OR costo_total LIKE "%{text}%" OR abonado LIKE "%{text}%" OR fecha_hora LIKE "%{text}%") ;'
                    sql = f'SELECT dv.ID_detalle_venta, v.detalles_venta, p.nombre, dv.cantidad, p.unidad_medida, dv.costo_total, dv.abonado, v.fecha_hora FROM Detalle_Ventas AS dv, Productos AS p, Ventas AS v WHERE (dv.IDproducto = p.IDproducto AND dv.IDventa = v.IDventa) AND (v.Detalles_venta LIKE "%{text}%" OR p.nombre LIKE "%{text}%" OR cantidad LIKE "%{text}%" OR p.unidad_medida LIKE "%{text}%" OR costo_total LIKE "%{text}%" OR abonado LIKE "%{text}%" OR fecha_hora LIKE "%{text}%") ;'
                self.ui.label_feedbackSales.hide()


            case "table_debts":
                # TODO: declarar consultas sql para también traer los datos necesarios
                if not search_bar and SHOW_ALL:
                    count_sql = "SELECT COUNT(DISTINCT IDdeudor) FROM Deudas;"
                    sql = 'SELECT Detalle_Ventas.*, Deudores.* \
                        FROM Detalle_Ventas \
                        JOIN Deudas ON Detalle_Ventas.IDdeuda = Deudas.IDdeuda \
                        JOIN Deudores ON Deudas.IDdeudor = Deudores.IDdeudor;'

                else:
                    pass
        
        #? declaro WORKER, THREAD y sus señales/slots
        self.READ_THREAD = QThread()
        self.read_worker = DbReadWorker()
        
        self.read_worker.moveToThread(self.READ_THREAD)
        
        self.READ_THREAD.started.connect(lambda: self.read_worker.executeReadQuery(
            data_sql=sql,
            data_params=params if params else None,
            count_sql=count_sql,
            count_params=count_params if count_params else None))
        self.read_worker.countFinished.connect(lambda row_count: self.DbReadWorker_onCountFinished(
            row_count=row_count,
            table_widget=table_widget))
        self.read_worker.registerProgress.connect(lambda register: self.DbReadWorker_onRegisterProgress(
            register=register,
            table_widget=table_widget))
        self.read_worker.finished.connect(lambda: self.workerOnFinished(
            table_name=table_widget.objectName()))
        self.read_worker.finished.connect(self.READ_THREAD.quit)
        self.READ_THREAD.finished.connect(self.read_worker.deleteLater)
        
        self.READ_THREAD.start()
        return None
    
    
    @Slot(int,QTableWidget,str,tuple)
    def DbReadWorker_onCountFinished(self, row_count:int, table_widget:QTableWidget) -> None:
        '''
        Es llamada cuando el WORKER termina con la consulta COUNT().
        
        Este método llama al método 'self.__updateProgressBar' sólo para indicar el valor máximo del QProgressBar 
        relacionado con el 'table_widget' y asigna la cantidad de filas al 'table_widget'.
        
        - row_count: cantidad de filas para el 'table_widget'.
        - table_widget: QTableWidget al que se referencia.
        
        Retorna None.
        '''
        self.__updateProgressBar(table_name=table_widget.objectName(),
                                 max_val=row_count)
        table_widget.setRowCount(row_count)
        return None
    
    
    @Slot(tuple,QTableWidget)
    def DbReadWorker_onRegisterProgress(self, register:tuple[Any], table_widget:QTableWidget=None) -> None:
        '''
        Es llamado a medida que el WORKER encuentra registros.
        
        Si 'FILL_TABLE == True' y 'table_widget != None' éste método llama a:
        - self.__saveTableWidgetIDs -> para guardar en una variable global los IDs del 'table_widget'.
        - self.__setTableWidgetContent -> para colocar los datos en el 'table_widget' correspondiente.
        - self.__updateProgressBar -> para actualizar el valor del QProgressBar relacionado con el 'table_widget'.
        
        - register: registro obtenido de la consulta READ.
        - table_widget: el QTableWidget al que se referencia. Por defecto es None.
        '''
        self.__saveTableWidgetIDs(table_name=table_widget.objectName(),
                                    register_id=register[1][0])
        self.__setTableWidgetContent(table_widget=table_widget,
                                        curr_row=register[0],
                                        row_data=register[1])
        self.__updateProgressBar(table_name=table_widget.objectName(),max_val=None,
                                    value=register[0])
    
    
    def __updateProgressBar(self, table_name:str, max_val:int=None, value:int=None) -> None:
        '''
        Actualiza el QProgressBar correspondiente dependiendo del nombre de la tabla 'table_name'.
        
        Recibe un 'max_val' si se llama desde 'self.DbReadWorker_onCountFinished' que determina el valor máximo del 
        QProgressBar, ó recibe un 'value' si se llama desde las otros métodos/señales que representa el valor actual 
        de progreso del QProgressBar.
        
        Es llamada desde:
        - self.DbReadWorker_onCountFinished: se llama una vez para determinar el valor máximo del QProgressBar 
        asociado al QTableWidget con nombre 'table_name', y luego desde la señal 'self.DbReadWorker_onRegisterProgress' 
        a medida que se encuentran registros para actualizar el 'value' del QProgressBar.
        - self.DbDeleteWorker_onFinished: se llama a medida que se borran registros para actualizar el 'value' del 
        QProgressBar.
        
        Retorna None.
        '''
        match table_name:
            case "displayTable":
                self.ui.inventory_progressbar.show() if self.ui.inventory_progressbar.isHidden() else None
                self.ui.inventory_progressbar.setMaximum(max_val) if max_val is not None and self.ui.inventory_progressbar.maximum() != max_val else None
                self.ui.inventory_progressbar.setValue(value + 1) if value else None
            
            case "table_sales_data":
                self.ui.sales_progressbar.show() if self.ui.sales_progressbar.isHidden() else None
                self.ui.sales_progressbar.setMaximum(max_val) if max_val is not None and self.ui.sales_progressbar.maximum() != max_val else None
                self.ui.sales_progressbar.setValue(value + 1) if value else None
                
            case "table_debts":
                self.ui.debts_progressbar.show() if self.ui.debts_progressbar.isHidden() else None
                self.ui.debts_progressbar.setMaximum(max_val) if max_val is not None and self.ui.debts_progressbar.maximum() != max_val else None
                self.ui.debts_progressbar.setValue(value + 1) if value else None
        return None
    
    
    def __saveTableWidgetIDs(self, table_name:str, register_id:int) -> None:
        '''
        Es llamada desde 'self.DbReadWorker_onRegisterProgress' a medida que el WORKER encuentra registros.
        
        Se encarga de guardar los 'register_id' de los registros coincidentes en una variable global asociada a cada 
        QTableWidget con nombre 'table_name'.
        
        Retorna None.
        '''
        match table_name:
            case "displayTable":
                self.IDs_products.append(register_id)
                
            case "table_sales_data":
                self.IDs_saleDetails.append(register_id)
            
            case "table_debts":
                pass
        return None
    
    
    def __setTableWidgetContent(self, table_widget:QTableWidget, curr_row:int, row_data:list[Any]) -> None:
        '''
        Es llamada desde 'self.DbReadWorker_onRegisterProgress' a medida que el WORKER encuentra registros.
        
        Se encarga de ir poblando el 'table_widget' con los datos correspondientes.
        
        - table_widget: el QTableWidget que se referencia.
        - curr_row: la fila actual de 'table_widget' a poblar con datos.
        - row_data: los datos para poblar la fila 'curr_row' de 'table_widget'.
        
        Retorna None.
        '''
        aux_text:str # var. aux. placeholder para formatear texto de celdas
        
        match table_widget.objectName():
            case "displayTable":
                table_widget.setItem(curr_row, 0, QTableWidgetItem(str(row_data[1])) ) # col.0 tiene categoría
                table_widget.setItem(curr_row, 1, QTableWidgetItem(str(row_data[2])) ) # col.1 tiene nombre
                table_widget.setItem(curr_row, 2, QTableWidgetItem(str(row_data[3]) if str(row_data[3]) != None else "") ) # col.2 tiene descripción
                aux_text = str(row_data[4]).replace(".",",")
                table_widget.setItem(curr_row, 3, QTableWidgetItem(str(f"{aux_text} {row_data[5]}")) ) # col.3 tiene stock y unidad_medida
                table_widget.setItem(curr_row, 4, QTableWidgetItem(str(row_data[6]).replace(".",",")) ) # col.4 tiene precio_unit
                table_widget.setItem(curr_row, 5, QTableWidgetItem(str(row_data[7]).replace(".",",") if row_data[7] != None else "") ) # col.5 tiene precio_comerc
            
            case "table_sales_data":
                table_widget.setItem(curr_row, 0, QTableWidgetItem(str(row_data[1]) if row_data[1] != None else "") ) # columna 0 tiene detalles_venta
                aux_text = str(row_data[3]).replace(".",",")
                table_widget.setItem(curr_row, 1, QTableWidgetItem(str(f"{aux_text} {str(row_data[4]) if row_data[4] != None else ''}")) ) # col.1 tiene cantidad y unidad_medida
                table_widget.setItem(curr_row, 2, QTableWidgetItem(str(row_data[2])) ) # col.2 tiene nombre
                table_widget.setItem(curr_row, 3, QTableWidgetItem(str(row_data[5]).replace(".",",")) ) # col.3 tiene costo_total
                table_widget.setItem(curr_row, 4, QTableWidgetItem(str(row_data[6]).replace(".",",")) ) # col.4 tiene abonado
                table_widget.setItem(curr_row, 5, QTableWidgetItem(str(row_data[7]) if str(row_data[7]) != None else "") ) # col.5 tiene fecha_hora
                
            case "table_debts":
                pass
                # TODO: seguir poniendo funcionalidad acá (antes necesito declarar las consultas sql)
        return None


    @Slot(str)
    def workerOnFinished(self, table_name:str, READ_OPERATION:bool=True) -> None:
        '''
        Esconde la QProgressBar relacionada con el QTableWidget con nombre 'table_name', reinicia el valor del 
        QSS de dicha QProgressBar y recarga el QTableWidget.
        
        Este método llama a:
        - self.handleTableToFill: para recargar el QTableWdiget con nombre 'table_name'.
        
        PARAMS:
        - table_name: nombre del QTableWidget al que se referencia.
        - READ_OPERATION: flag que determina si la operación que se hizo fue de llenado (READ) a un QTableWidget.
        Por defecto es True.

        Si 'READ_OPERATION' es False es porque se realizaron otras consultas a la base de datos (DELETE ó INSERT), y 
        sólo en esos casos se debe llamar a 'self.handleTableToFill'.
        
        Retorna None.
        '''
        match table_name:
            case "displayTable":
                self.ui.inventory_progressbar.setStyleSheet("")
                self.ui.inventory_progressbar.hide()
                if not READ_OPERATION:
                    # recarga la tabla
                    try:
                        self.handleTableToFill(table_widget=self.ui.displayTable, SHOW_ALL=True)
                    except AttributeError: # salta porque se intenta recargar la tabla pero nunca se llenó anteriormente
                        pass
                else:
                    self.ui.displayTable.resizeRowsToContents()
                
            case "table_sales_data":
                self.ui.sales_progressbar.setStyleSheet("")
                self.ui.sales_progressbar.hide()
                if not READ_OPERATION:
                    # recarga la tabla
                    self.handleTableToFill(table_widget=self.ui.table_sales_data, SHOW_ALL=True)
                else:
                    self.ui.table_sales_data.resizeRowsToContents()
                
            case "table_debts":
                self.ui.debts_progressbar.setStyleSheet("")
                self.ui.debts_progressbar.hide()
                if not READ_OPERATION:
                    # recarga la tabla
                    self.handleTableToFill(table_widget=self.ui.table_debts, SHOW_ALL=True)
                else:
                    self.ui.table_debts.resizeRowsToContents()
            
        logging.debug(f">> WORKER terminó de ejecutarse.")
        return None



    #¡ tablas (CREATE)
    @Slot(str)
    def handleTableCreateRow(self, table_widget:QTableWidget) -> None:
        '''
        Dependiendo del QTableWidget al que se agregue una fila, se encarga de crear una instancia del QDialog 
        correspondiente que pide los datos necesarios para la nueva fila.
        
        Al final, recarga la tabla correspondiente llamando a 'self.handleTableToFill'.
        \nRetorna 'None'.'''
        match table_widget.objectName():
            case "displayTable":
                productDialog = ProductDialog() # QDialog para añadir un producto nuevo a 'displayTable'
                productDialog.setAttribute(Qt.WA_DeleteOnClose, True) # destruye el dialog cuando se cierra
                productDialog.exec()

            case "table_sales_data":
                saleDialog = SaleDialog() # QDialog para añadir una venta nueva a 'table_sales_data' (y posiblemente, una
                                          # deuda a 'table_debts')
                saleDialog.setAttribute(Qt.WA_DeleteOnClose, True)
                saleDialog.exec()
        
        return None



    #¡ tablas (DELETE)
    def __getTableElementsToDelete(self, table_widget:QTableWidget, selected_rows:list) -> tuple | None:
        '''
        Dependiendo de cuál sea 'table_widget', obtiene los nombres de los productos de 'displayTable' ó la fecha 
        y hora de 'table_sales_data'. 
        
        - table_widget: QTableWidget al que se referencia.
        - selected_rows: lista con las filas seleccionadas del 'table_widget'.
        
        Retorna una tupla con los registros a eliminar, o None si no hay elementos seleccionados.
        '''
        if not selected_rows:
            return None
        
        registers_to_delete:list = [None]*len(selected_rows)
        
        match table_widget.objectName():
            # obtiene los nombres de los productos a borrar
            case "displayTable":
                for pos,row in enumerate(selected_rows):
                    registers_to_delete[pos] = table_widget.item(row, 1).text()
            
            # obtiene la fecha y hora de las ventas a borrar
            case "table_sales_data":
                for pos,row in enumerate(selected_rows):
                    registers_to_delete[pos] = table_widget.item(row, 5).text()
            
        return tuple(registers_to_delete)


    @Slot(QTableWidget)
    def handleTableDeleteRows(self, table_widget:QTableWidget) -> None:
        '''
        NOTA: Este método NO ELIMINA LOS REGISTROS DE "Productos" NI "Deudas", LOS MARCA COMO "ELIMINADOS" EN LA 
        BASE DE DATOS. EN CAMBIO SÍ ELIMINA LOS REGISTROS DE "Ventas" Y "Detalle_Ventas".
        
        Este método hace lo siguiente:
        - Dependiendo del 'table_widget' del que se tengan que borrar registros, se encarga de declarar las 
        consultas sql y los parámetros necesarios para luego hacer las consultas UPDATE que marcan como "eliminado" 
        los registros en la clase 'workerclasses.DbDeleteWorker'.
        - Cambia el QSS del QProgressBar asociado a 'table_widget'.
        - Especifica el valor máximo del QProgressBar asociado a 'table_widget'.
        - Crea una instancia de WORKER y QThread y conecta sus señales/slots.
        
        Este método llama a:
        - functionutils.getSelectedTableRows: para obtener las filas seleccionas del 'table_widget'.
        - self.__getTableElementsToDelete: para obtener datos sobre los registros a marcar como eliminados.
        - self.__updateProgressBar: para especificar el valor máximo de la QProgressBar asociada a 'table_widget'.
        
        Retorna None.
        '''
        selected_rows:tuple # las posiciones de self.IDs_products/self.IDs_saleDetails donde están los registros seleccionados
        ids_to_delete:list # los IDs de los registros a eliminar (necesario para consulta)
        productnames_to_delete:list|None # los nombres de los registros a eliminar de "Productos"
        dateTime_to_delete:list|None # las fechas y horas de los registros a eliminar de "Ventas" y "Detalle_Ventas"

        mark_sql:str = None # consulta UPDATE para marcar "eliminado" los registros (Productos y Deudas)
        mult_sql:tuple[str] = None # se usa para borrar de Detalle_Ventas y Ventas.
        params:list[tuple] = None # lista[(id, nombre)] si es Productos; ó lista[(id,fecha_hora)] si es Detalle_Ventas
        
        selected_rows = getSelectedTableRows(table_widget)
        
        if not selected_rows:
            return None
        
        
        match table_widget.objectName():
            case "displayTable":
                productnames_to_delete = self.__getTableElementsToDelete(table_widget, selected_rows)
                
                # a partir de las filas seleccionadas, obtiene de self.IDs_products los ids para la consulta
                ids_to_delete = [self.IDs_products[n_id] for n_id in selected_rows]
                
                mark_sql = "UPDATE Productos SET eliminado = 1 WHERE IDproducto = ? AND nombre = ?;"
                
                # une 'ids_to_delete' y 'productnames_to_delete' en una lista[(id, nombre)]
                params = [(id, name) for id,name in zip(ids_to_delete, productnames_to_delete)]
                
                self.ui.inventory_progressbar.setMaximum(len(params))
                self.ui.inventory_progressbar.setStyleSheet("QProgressBar::chunk {background-color: qlineargradient(spread:reflect, x1:0.119, y1:0.426, x2:0.712045, y2:0.926, stop:0.0451977 rgba(255, 84, 87, 255), stop:0.59887 rgba(255, 161, 71, 255));}")
            
            
            case "table_sales_data":
                dateTime_to_delete = self.__getTableElementsToDelete(table_widget, selected_rows)
                
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


            case "table_debts":
                pass
        
        #? inicializa WORKER y THREAD, y conecta señales/slots
        self.DELETE_THREAD = QThread()
        # si mark_sql != None es porque se deben MARCAR "eliminados" los registros, sino se deben ELIMINAR        
        if mark_sql:
            self.update_worker = DbUpdateWorker()
            self.update_worker.moveToThread(self.DELETE_THREAD)
            self.DELETE_THREAD.started.connect(lambda: self.update_worker.executeUpdateQuery(
                sql=mark_sql,
                params=params))
            self.update_worker.progress.connect(lambda value: self.__updateProgressBar(
                table_name=table_widget.objectName(),
                value=value))
            self.update_worker.finished.connect(lambda: self.workerOnFinished(
                table_name=table_widget.objectName(),
                READ_OPERATION=False) )
            self.update_worker.finished.connect(self.DELETE_THREAD.quit)
            self.DELETE_THREAD.finished.connect(self.update_worker.deleteLater)
            
        # sino, se deben borrar completamente (no marcar como "eliminados")
        else:
            self.delete_worker = DbDeleteWorker()
            self.delete_worker.moveToThread(self.DELETE_THREAD)
            self.DELETE_THREAD.started.connect(lambda: self.delete_worker.executeDeleteQuery(
                params=params,
                mult_sql=mult_sql))
            self.delete_worker.progress.connect(lambda value: self.__updateProgressBar(
                table_name=table_widget.objectName(),
                value=value))
            self.delete_worker.finished.connect(lambda: self.workerOnFinished(
                table_name=table_widget.objectName(),
                READ_OPERATION=False) )
            self.delete_worker.finished.connect(self.DELETE_THREAD.quit)
            self.DELETE_THREAD.finished.connect(self.delete_worker.deleteLater)
            
        self.DELETE_THREAD.start()
        return None


    #¡ tablas (UPDATE)
    def __tableComboBoxOnCurrentTextChanged(self, table_widget:QTableWidget, curr_index:QModelIndex, combobox:QComboBox) -> None:
        '''
        Declara la consulta sql y los parámetros y luego hace la consulta UPDATE a la base de datos con el nuevo 
        dato seleccionado a partir del nuevo texto de 'combobox'. Reemplaza el valor anterior de la celda por el
        nuevo. Al finalizar, elimina todos los QComboBox de 'table_widget'.
        
        PARAMS:
        - table_widget: QTableWidget al que se referencia.
        - curr_index: representa las coordenadas del item en 'table_widget'.
        - combobox: representa al QComboBox afectado.
        
        Retorna None.
        '''
        new_unit:str | None # y el valor de la unidad ya seleccionado.
        quantity:float | int # cantidad seleccionada.

        match table_widget.objectName():
            case "displayTable":
                makeUpdateQuery(sql="UPDATE Productos SET IDcategoria = (SELECT IDcategoria FROM Categorias WHERE nombre_categoria = ?) WHERE IDproducto = ?;",
                                params=(combobox.currentText(), str(self.IDs_products[curr_index.row()]),) )
                table_widget.item(curr_index.row(), curr_index.column()).setText(combobox.currentText())


            case "table_sales_data":
                # actualiza el producto en Detalle_Ventas
                makeUpdateQuery(sql="UPDATE Detalle_Ventas SET IDproducto = (SELECT IDproducto FROM Productos WHERE nombre = ?) WHERE ID_detalle_venta = ?;",
                                params=(combobox.currentText(), str(self.IDs_saleDetails[curr_index.row()]),) )
                table_widget.item(curr_index.row(), curr_index.column()).setText(f"{combobox.currentText()}")

                # obtengo la cantidad de la columna "cantidad" para luego unirlo a la unidad de medida
                quantity = table_widget.item(curr_index.row(), 1).text().split(" ")[0].strip()

                # obtengo la unidad de medida del producto actual para colocarlo en la columna "cantidad"
                new_unit = makeReadQuery(sql="SELECT unidad_medida FROM Productos WHERE nombre = ?;",
                                         params=(combobox.currentText(),) )[0][0]
                table_widget.item(curr_index.row(), 1).setText(f"{quantity} {new_unit}")

        combobox.deleteLater()
        # remueve los widgets de las celdas (para que se puedan modificar sólo una vez al mismo tiempo las comboboxes)
        removeTableCellsWidgets(table_widget)
        # vuelve a activar el ordenamiento de la tabla
        # table_widget.setSortingEnabled(True)
        return None


    @Slot(QTableWidget, QModelIndex, QLineEdit, str)
    def __tableLineEditOnReturnPressed(self, table_widget:QTableWidget, curr_index:QModelIndex, lineedit:QLineEdit, prev_text:str) -> None:
        '''
        Este método es llamado desde la señal 'self.lineedit.returnPressed' y sólo se ejecutará cuando el input 
        sea válido ('validador.State.Acceptable').
        
        Declara la consulta sql y los parámetros y luego hace la consulta UPDATE a la base de datos con el nuevo 
        dato ingresado a partir del nuevo texto introducido en 'lineedit'. Luego sustituye el valor actual de 
        la celda por el nuevo.
        Al finalizar, remueve 'lineedit' de la celda de 'table_widget'.
        
        Este método llama a:
        - makeUpdateQuery: para realizar las consultas UPDATE.
        - removeTableCellsWidgets: para quitar los QLineEdit de 'table_widget'.
        
        PARAMS:
        - table_widget: el QTableWidget al que se referencia.
        - curr_index: índice de la celda seleccionada de 'table_widget'.
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


        match table_widget.objectName():
            case "displayTable":                
                match curr_index.column():
                    case 1: # nombre
                        makeUpdateQuery(sql="UPDATE Productos SET nombre = ? WHERE IDproducto = ?;",
                                        params=( lineedit.text(), str(self.IDs_products[curr_index.row()]), ))
                        # reemplaza el valor anterior con el nuevo
                        table_widget.item(curr_index.row(), curr_index.column()).setText(lineedit.text().strip())
                    
                    case 2: # descripción
                        makeUpdateQuery(sql="UPDATE Productos SET descripcion = ? WHERE IDproducto = ?;",
                                        params=( lineedit.text(), str(self.IDs_products[curr_index.row()]), ))
                        # reemplaza el valor anterior con el nuevo
                        table_widget.item(curr_index.row(), curr_index.column()).setText(lineedit.text().strip())
                    
                    case 3: # stock
                        # obtiene la cantidad de stock y la unidad de medida (si tiene)
                        full_stock = lineedit.text().replace(",",".").split(" ") # pos. 0 tiene cantidad de stock y pos. 1 tiene unidad de medida
                        full_stock.append("") if len(full_stock) == 1 else None
                        
                        makeUpdateQuery(sql="UPDATE Productos SET stock = ?, unidad_medida = ? WHERE IDproducto = ?;",
                                        params=(full_stock[0], full_stock[1], str(self.IDs_products[curr_index.row()]), ))
                        # reemplaza el valor anterior con el nuevo
                        full_stock[0] = full_stock[0].replace(".",",")
                        table_widget.item(curr_index.row(), curr_index.column()).setText(f"{full_stock[0]} {full_stock[1].strip()}")
                    
                    case 4: # si es precio unitario, modifica también en Deudas precios normales
                        # actualiza en Productos
                        makeUpdateQuery(sql="UPDATE Productos SET precio_unit = ? WHERE IDproducto = ?;",
                                        params=(lineedit.text().replace(",","."), str(self.IDs_products[curr_index.row()]), ))
                        
                        # obtiene la expresión para calcular en Deudas el nuevo total_adeudado
                        prev_text = prev_text.replace(",",".")
                        try:
                            percentage_diff = (float(lineedit.text().replace(",",".")) - float(prev_text)) * 100 / float(prev_text)
                            
                        except ZeroDivisionError: # en caso de fallar porque el valor anterior es 0, hago que sea 0.00001
                            percentage_diff = (float(lineedit.text().replace(",",".")) - float(prev_text)) * 100 / (float(prev_text) + 0.00001)
                            
                        new_debt_term = 1 + percentage_diff / 100
                        sql = "UPDATE Deudas SET total_adeudado = ROUND(total_adeudado * ?, 2) WHERE IDdeuda IN (SELECT Detalle_Ventas.IDdeuda FROM Detalle_Ventas JOIN Ventas ON Detalle_Ventas.IDventa = Ventas.IDventa WHERE Detalle_Ventas.IDproducto = (SELECT IDproducto FROM Productos WHERE nombre = ?) AND Ventas.detalles_venta LIKE '%(P. NORMAL)%');"
                        
                        # actualiza total_adeudado en Deudas en precios normales
                        makeUpdateQuery(sql, (new_debt_term, table_widget.item(curr_index.row(), 1).text(),) )
                        # reemplaza el valor anterior con el nuevo
                        lineedit_text = lineedit.text().replace(".",",")
                        table_widget.item(curr_index.row(), curr_index.column()).setText(lineedit_text.strip())
                        
                    case 5: # si es precio comercial, modifica en Deudas precios comerciales
                        lineedit_text = lineedit.text().replace(",",".") if lineedit.text() else 0.0
                            
                        # actualiza en Productos
                        makeUpdateQuery(sql="UPDATE Productos SET precio_comerc = ? WHERE IDproducto = ?;",
                                        params=(str(lineedit_text), str(self.IDs_products[curr_index.row()]), ))
                        
                        prev_text = prev_text.replace(",",".") if prev_text else 0.0
                        try:
                            percentage_diff = (float(lineedit_text) - float(prev_text)) * 100 / float(prev_text)
                            
                        except ZeroDivisionError: # en caso de fallar porque el valor anterior es 0, hago que sea 0.00001
                            percentage_diff = (float(lineedit_text) - float(prev_text)) * 100 / (float(prev_text) + 0.00001)
                        
                        new_debt_term = 1 + percentage_diff / 100
                        sql = sql = "UPDATE Deudas SET total_adeudado = ROUND(total_adeudado * ?, 2) WHERE IDdeuda IN (SELECT Detalle_Ventas.IDdeuda FROM Detalle_Ventas JOIN Ventas ON Detalle_Ventas.IDventa = Ventas.IDventa WHERE Detalle_Ventas.IDproducto = (SELECT IDproducto FROM Productos WHERE nombre = ?) AND Ventas.detalles_venta LIKE '%(P. COMERCIAL)%');"
                        
                        # actualiza total_adeudado en Deudas en precios comerciales
                        makeUpdateQuery(sql, (new_debt_term, table_widget.item(curr_index.row(), 1).text(),) )
                        
                        # reemplaza el valor anterior con el nuevo
                        lineedit_text = lineedit.text().replace(".",",")
                        table_widget.item(curr_index.row(), curr_index.column()).setText(lineedit_text.strip())


            case "table_sales_data":
                match curr_index.column():
                    case 0: # detalle de venta
                        pattern = compile("(\([\s]*P\.[\s]*NORMAL[\s]*\)|\([\s]*P\.[\s]*COMERCIAL[\s]*\))$", IGNORECASE)
                        
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
                        
                        makeUpdateQuery(sql="UPDATE Ventas SET detalles_venta = ? WHERE IDventa = (SELECT IDventa FROM Detalle_Ventas WHERE ID_detalle_venta = ?);",
                                        params=(lineedit_text, str(self.IDs_saleDetails[curr_index.row()]), ))
                        table_widget.item(curr_index.row(), curr_index.column()).setText(f"{lineedit_text}")
                    
                    case 1: # cantidad
                        makeUpdateQuery(sql="UPDATE Detalle_Ventas SET cantidad = ? WHERE ID_detalle_venta = ?;",
                                        params=(lineedit.text().replace(",","."), str(self.IDs_saleDetails[curr_index.row()]), ))
                        # toma la unidad de medida (si tiene) y la concatena con la nueva cantidad
                        new_prev_text = prev_text.split(" ")[1] if len(prev_text.split(" ")) > 1 else ""
                        lineedit_text = lineedit.text().replace(".",",")
                        table_widget.item(curr_index.row(), curr_index.column()).setText(f"{lineedit_text} {new_prev_text}")
                    
                    case 3: # costo total
                        makeUpdateQuery(sql="UPDATE Detalle_Ventas SET costo_total = ? WHERE ID_detalle_venta = ?;",
                                        params=(lineedit.text().replace(",","."), str(self.IDs_saleDetails[curr_index.row()]), ))
                        lineedit_text = lineedit.text().replace(".",",")
                        table_widget.item(curr_index.row(), curr_index.column()).setText(f"{lineedit_text.strip()}")
                    
                    case 4: # abonado
                        makeUpdateQuery(sql="UPDATE Detalle_Ventas SET abonado = ? WHERE ID_detalle_venta = ?;",
                                        params=(lineedit.text().replace(",","."), str(self.IDs_saleDetails[curr_index.row()]), ))
                        lineedit_text = lineedit.text().replace(".",",")
                        table_widget.item(curr_index.row(), curr_index.column()).setText(f"{lineedit_text.strip()}")
        
        # borra el lineedit
        if table_widget.cellWidget(curr_index.row(), curr_index.column()): #! veo si existe porque, por alguna razón, al
            lineedit.deleteLater()                                         #! lineedit en 'table_sales_data' no lo encuentra.
        # remueve todos los widgets                                        #! Igualmente 'removeTableCellWidgets' le da 
        removeTableCellsWidgets(table_widget)                              #! permiso al 'garbage collector' de borrarlos...
        
        # vuelvo a activar el ordenamiento de la tabla
        # table_widget.setSortingEnabled(True)
        return None


    @Slot(QTableWidget, QModelIndex, QDateTimeEdit)
    def __tableDateTimeOnEditingFinished(self, table_widget:QTableWidget, curr_index:QModelIndex, datetimeedit:QDateTimeEdit) -> None:
        '''
        Este método es llamado desde la señal 'self.datetimeedit.editingFinished'.
        
        Declara la consulta UPDATE y sus parámetros y luego hace la consulta a la base de datos para actualizar 
        el valor de 'datetimeedit', luego sustituye el valor actual de la celda por el nuevo.
        Al finalizar, remueve 'datetimeedit' de la celda de 'table_widget'.
        
        Este método llama a:
        - makeUpdateQuery: para realizar las consultas UPDATE.
        - removeTableCellsWidgets: para quitar los QDateTimeEdit de 'table_widget'.
        
        PARAMS:
        - table_widget: el QTableWidget al que se referencia.
        - curr_index: índice de la celda seleccionada de 'table_widget'.
        - datetimeedit: el QDateTimeEdit que envía la señal.
        
        Retorna None.
        '''
        match table_widget.objectName():
            case "table_sales_data":
                makeUpdateQuery(sql="UPDATE Ventas SET fecha_hora = ? WHERE IDventa = (SELECT IDventa FROM Detalle_Ventas WHERE ID_detalle_venta = ?);",
                                params=(datetimeedit.text(), self.IDs_saleDetails[curr_index.row()], ))
                table_widget.item(curr_index.row(), curr_index.column()).setText(f"{str(datetimeedit.text()).strip()}")
            
            case _:
                pass
        
        #? verifico si el calendar tiene el foco puesto porque cuando se muestra el popup cambia el foco y envía 
        #? la señal 'editingFinished' a éste método, lo que hace que se cierre instantáneamente. La comparación 
        #? de abajo hace que no se cierre el calendar y permita editar la fecha.
        if not datetimeedit.calendarWidget().hasFocus():
            datetimeedit.deleteLater()
            removeTableCellsWidgets(table_widget)
        return None


    @Slot(QTableWidget, QModelIndex)
    def handleTableUpdateItem(self, table_widget:QTableWidget, curr_index:QModelIndex) -> None:
        '''
        Dependiendo del 'table_widget' del cual se quiera modificar una celda y dependiendo de la columna seleccionada 
        en 'curr_index' crea un QLineEdit|QComboBox|QDateTimeEdit para permitir una modificación más adecuada en esa celda.
        Además conecta las señales/slots de los widgets y sus 'validators'.

        Este método llama a:
        - functionutils.createTableColumnComboBox: para crear QComboBox.
        - functionutils.createTableColumnLineEdit: para crear QLineEdit.
        - functionutils.createTableColumnDateTimeEdit: para crear QDateTimeEdit.
        
        PARAMS:
        - table_widget: el QTableWidget al que se referencia.
        - curr_index: índice seleccionado en 'table_widget'.
        
        Retorna None.
        '''
        cell_old_text:str # texto actual de la celda.
        self.combobox:QComboBox
        self.lineedit:QLineEdit
        self.datetimeedit:QDateTimeEdit
        validator:ProductNameValidator
        
        # desactivo el ordenamiento de la tabla
        # table_widget.setSortingEnabled(False)

        if table_widget.editTriggers() != QAbstractItemView.EditTrigger.NoEditTriggers:
            cell_old_text = table_widget.item(curr_index.row(), curr_index.column()).text()
            
            match table_widget.objectName():
                case "displayTable":
                    self.ui.label_feedbackInventory.hide()
                    
                    match curr_index.column():
                        case 0: # categoría (QComboBox)
                            self.combobox = createTableColumnComboBox(table_widget, curr_index, cell_old_text)
                            self.combobox.textActivated.connect(lambda: self.__tableComboBoxOnCurrentTextChanged(
                                table_widget=table_widget,
                                curr_index=curr_index,
                                combobox=self.combobox))
                            
                        case _: # nombre | descripción | stock | precio unitario | precio comercial (QLineEdit)
                            self.lineedit = createTableColumnLineEdit(table_widget, curr_index)
                        
                            self.lineedit.returnPressed.connect(lambda: self.__tableLineEditOnReturnPressed(
                                table_widget=self.ui.displayTable,
                                curr_index=curr_index,
                                lineedit=self.lineedit,
                                prev_text=cell_old_text))
                            
                            if curr_index.column() != 2: # diferente de descripción (no tiene validador)
                                # señal del validador
                                validator = self.lineedit.validator()
                                validator.validationSucceded.connect(self.ui.label_feedbackInventory.hide)
                                validator.validationFailed.connect(lambda text: self.__validatorOnValidationFailed(
                                    feedback_text=text,
                                    feedback_label=self.ui.label_feedbackInventory,
                                    curr_text=self.lineedit.text(),
                                    prev_text=cell_old_text))
                
                
                case "table_sales_data":
                    self.ui.label_feedbackSales.hide()
                    
                    match curr_index.column():
                        case 2: # producto (QComboBox)
                            self.combobox  = createTableColumnComboBox(table_widget, curr_index, cell_old_text)
                            
                            self.combobox.textActivated.connect(lambda: self.__tableComboBoxOnCurrentTextChanged(
                                table_widget=table_widget,
                                curr_index=curr_index,
                                combobox=self.combobox))
                        
                        case 5: # fecha y hora (QDateTimeEdit)
                            self.datetimeedit = createTableColumnDateTimeEdit(table_widget, curr_index)
                            
                            self.datetimeedit.editingFinished.connect(lambda: self.__tableDateTimeOnEditingFinished(
                                table_widget=table_widget,
                                curr_index=curr_index,
                                datetimeedit=self.datetimeedit))
                        
                        case _: # detalle de venta | cantidad | costo total | abonado (QLineEdit)
                            
                            self.lineedit = createTableColumnLineEdit(table_widget, curr_index)
                            
                            self.lineedit.returnPressed.connect(lambda: self.__tableLineEditOnReturnPressed(
                                table_widget=self.ui.table_sales_data,
                                curr_index=curr_index,
                                lineedit=self.lineedit,
                                prev_text=cell_old_text))
                            
                            # señal del validador
                            validator = self.lineedit.validator()
                            validator.validationSucceded.connect(self.ui.label_feedbackSales.hide)
                            validator.validationFailed.connect(lambda text: self.__validatorOnValidationFailed(
                                feedback_text=text,
                                feedback_label=self.ui.label_feedbackSales,
                                curr_text=self.lineedit.text(),
                                prev_text=cell_old_text))
                
                            
                case "table_debts":
                    self.ui.label_feedbackDebts.hide()
                    
        return None


    @Slot(str)
    def __validatorOnValidationFailed(self, feedback_text:str, feedback_label:QLabel, curr_text:str, prev_text:str) -> None:
        '''
        Es llamado desde la señal 'validationFailed' perteneciente a los validadores declarados en el método 
        'self.handleTableUpdateItem'.
        
        Muestra el 'feedback_label' con el texto 'feedback_text' en él sólo si 'prev_text' es diferente al 
        texto actual (sino significa que hubo un falso 'Validator.State.Intermediate' dado que el nombre introducido 
        es el mismo que el anterior), además cambia la hoja de estilos del QLabel.
        
        Retorna None.
        '''
        if prev_text != curr_text:
            feedback_label.show()
            feedback_label.setStyleSheet("font-family: 'Verdana'; font-size: 16px; letter-spacing: 0px; word-spacing: 0px; color: #f00; border: 1px solid #f00; background-color: rgb(255, 185, 185);")
            feedback_label.setText(feedback_text)
        return None


    #¡ método de cambios en la selección
    @Slot(QTableWidget)
    def handleSelectionChange(self, table_widget:QTableWidget) -> None:
        '''
        Esta función es llamada ni bien se detecta que la selección de los items en 'table_widget' cambia. 
        Verifica si hay celdas seleccionadas. Si no hay, llama a 'functionutils.removeTableCellsWidgets'.
        
        Retorna None.'''
        # obtengo los items seleccionados actualmente de las tablas
        curr_selection = table_widget.selectedItems()
        if len(curr_selection) <= 1: # por alguna razón 'curr_selection' siempre tiene 1 item, nunca llega a estar vacía...
            removeTableCellsWidgets(table_widget)
        return None



    #### INVENTARIO ##################################################
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
                        value = float(self.ui.displayTable.item(selected_rows[row], 4).text())
                        unit_price = value + (value * percentage / 100)
                        # asigna el valor nuevo
                        params.append({'id': self.IDs_products[selected_rows[row]],
                                        'unit_pr': f"{unit_price:.2f}"})
                        self.ui.displayTable.item(selected_rows[row], 4).setText(f"{unit_price:.2f}")
                        sql:str = "UPDATE Productos SET precio_unit = :unit_pr WHERE IDproducto = :id;"
                        makeUpdateQuery(sql, params, inv_prices=True)
                    except:
                        pass

        # sino, si está activada la checkbox de precios comerciales...
        else:
            for row in range(len(selected_rows)):
                if self.IDs_products[selected_rows[row]] not in params and self.ui.displayTable.item(selected_rows[row], 5).text() != "":
                    try:
                        # calcula el valor nuevo
                        percentage = int(self.ui.lineEdit_percentage_change.text().replace(".","").replace(",",""))
                        value = float(self.ui.displayTable.item(selected_rows[row], 5).text())
                        comerc_price = value + (value * percentage / 100)
                        # asigna el valor nuevo
                        params.append({'id': self.IDs_products[selected_rows[row]],
                                       'comerc_pr': f"{comerc_price:.2f}"})
                        self.ui.displayTable.item(selected_rows[row], 5).setText(f"{comerc_price:.2f}")
                        sql:str = "UPDATE Productos SET precio_comerc = :comerc_pr WHERE IDproducto = :id;"
                        makeUpdateQuery(sql, params, inv_prices=True)
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
            selected_rows = getSelectedTableRows(self.ui.displayTable)
            self.__calculateNewPrices(selected_rows)
        return None


    @Slot()
    def handleCheckboxStateChange(self) -> None:
        '''Dependiendo de cuál se haya checkeado, permite al usuario seleccionar las filas de los productos cuyos 
        precios (unitarios o comerciales) de la tabla 'displayTable' desee incrementar/decrementar de forma porcentual. Además 
        al checkear cualquier checkbox se habilita el 'lineEdit_percentage_change', sino lo deshabilita. Retorna 'None'.'''
        if self.ui.checkbox_unit_prices.isChecked() or self.ui.checkbox_comercial_prices.isChecked():
            # cambia el modo de selección de 'displayTable', habilita el lineedit
            self.ui.displayTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.ui.displayTable.setSelectionBehavior(QAbstractItemView.SelectRows)
            self.ui.displayTable.setSelectionMode(QAbstractItemView.MultiSelection)
            self.ui.lineEdit_percentage_change.setEnabled(True)
        else: # vuelve a poner el modo de selección de 'displayTable' al que tiene por defecto, deshabilita el lineedit
            self.ui.displayTable.setEditTriggers(QAbstractItemView.DoubleClicked)
            self.ui.displayTable.setSelectionBehavior(QAbstractItemView.SelectItems)
            self.ui.displayTable.setSelectionMode(QAbstractItemView.ExtendedSelection)
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



    #### VENTAS ######################################################
    def __update_self_ValidItems(self, item_action:dict[str:bool] | str) -> None:
        '''Actualiza el diccionario 'self.VALID_ITEMS' dependiendo de si se modificó, se agregó o se eliminó 
        un item (si se modificó o agregó, 'item_action' será un dict, sinó será str). Retorna 'None'.'''
        # si recibe un 'dict' (item_action se recibe por la señal 'allFieldsValid') es porque se agregó un item o se modificó...
        if isinstance(item_action, dict):
            self.VALID_ITEMS.update(item_action)
        # si recibe un 'str' es porque se borró un item...
        else:
            if item_action in self.VALID_ITEMS.keys():
                self.VALID_ITEMS.pop(item_action, 0)
                self.ITEMS_VALUES.pop(item_action, 1)

            if self.ui.sales_input_list.count() == 0:
                self.VALID_ITEMS.clear()
                self.ITEMS_VALUES.clear()
                self.items_objectNames = 0
        return None


    def __update_self_ItemsValues(self) -> float:
        '''
        Actualiza con los valores de los items la tupla 'self.ITEMS_VALUES', y de paso calcula el costo total de la 
        venta.
        
        Retorna un float.
        '''
        object_name:str
        name_combobox:QComboBox
        product_price:str
        re_price:Match | None | str | float # intenta dejarlo como float, sino queda como str o None.
        total_paid:str | float = self.ui.lineEdit_paid.text()
        total_cost:float = 0.0

        # obtengo la cantidad abonada y la formateo
        try:
            if total_paid:
                total_paid = total_paid.replace(",",".")
                if total_paid.endswith("."):
                    total_paid = total_paid.replace(".","")
                total_paid = round(float(total_paid), 2)
            else:
                total_paid = 0.0
        except:
            pass
        # recorre los items y accede a los datos
        for i in range(self.ui.sales_input_list.count()):
            object_name = self.ui.sales_input_list.itemWidget(self.ui.sales_input_list.item(i)).objectName()

            name_combobox = self.ui.sales_input_list.itemWidget(self.ui.sales_input_list.item(i)).findChild(QComboBox, "comboBox_productName")
            product_price = self.ui.sales_input_list.itemWidget(self.ui.sales_input_list.item(i)).findChild(QLabel, "label_subtotal").text()
            self.ui.lineEdit_paid.setText(str(total_paid))
            # busco el precio del producto
            re_price = search(">[0-9]+[.]?[0-9]{1,2}<", product_price)
            try:
                re_price = float(re_price.group().strip("><")) if re_price else None
            except:
                pass

            # coloco en self.ITEMS_VALUES los valores
            self.ITEMS_VALUES[object_name] = (name_combobox.itemText(name_combobox.currentIndex()),
                    self.ui.sales_input_list.itemWidget(self.ui.sales_input_list.item(i)).findChild(QLineEdit, "lineEdit_productQuantity").text(),
                    self.ui.sales_input_list.itemWidget(self.ui.sales_input_list.item(i)).findChild(QCheckBox, "checkBox_comercialPrice").isChecked(),
                    self.ui.sales_input_list.itemWidget(self.ui.sales_input_list.item(i)).findChild(QLineEdit, "lineEdit_saleDetail").text(),
                    re_price,
                    self.ui.dateTimeEdit_sale.text(),
                    total_paid)
            
            # calculo el costo total
            total_cost += re_price
        return round(total_cost, 2)


    def __validateSalesInputListItems(self, item_action:dict[str:bool] | str) -> None:
        '''Si un campo dentro de un item fue modificado, 'item_action' será un diccionario con el 'objectName' del \
        item. Si los campos son válidos habilita el botón 'btn_end_sale', si alguno no es válido lo deshabilita. \
        Además cambia el contenido de 'dateTimeEdit_sale' para mostrar la hora precisa de la venta, agrega los valores \
        a 'self.ITEM_VALUES', coloca el precio total en 'self.label_total' y finalmente crea un QCompleter para \
        'self.lineEdit_paid' con el precio total.
        \nRetorna 'None'.'''
        total_cost:float
        completer:QCompleter

        # actualiza self.VALID_ITEMS
        self.__update_self_ValidItems(item_action)
        
        # habilita o deshalibita el botón 'btn_end_sale', actualiza self.ITEM_VALUES 
        if( len(self.VALID_ITEMS) == self.ui.sales_input_list.count() and all(self.VALID_ITEMS.values()) ) and self.ui.sales_input_list.count() > 0:
            self.ui.btn_end_sale.setEnabled(True)
            total_cost = self.__update_self_ItemsValues()
            # pone el precio total
            self.ui.label_total.setText(f"<html><head/><body><p>TOTAL <span style=\" color: #22577a;\">{total_cost}</span></p></body></html>")
            # crea el completer
            completer = QCompleter([str(total_cost)], parent=self.ui.lineEdit_paid)
            completer.setCompletionMode(completer.CompletionMode.InlineCompletion)
            completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
            self.ui.lineEdit_paid.setCompleter(completer)

            self.ui.lineEdit_paid.textChanged.connect(completer.setCompletionPrefix)

        else:
            self.ui.btn_end_sale.setEnabled(False)
            self.ui.label_total.setText("TOTAL")

        # cambia la hora de la venta
        self.ui.dateTimeEdit_sale.setDateTime(QDateTime.currentDateTime())
        return None
    

    def validateSalesFields(self, item_action:dict[str:bool] | str | None) -> None:
        '''Llama a 'self.__validateSalesInputListItems' para validar los items de 'sales_input_list', valida también \
        el campo de cantidad abonada 'self.lineEdit_paid' y muestra el cambio a devolver.
        \n\tSi lo abonado es mayor al total se muestra el cambio que se debe dar en 'label_total_change'.
        \nRetorna 'None'.'''
        total_paid:float
        re_total_cost:Match | float | None

        # si item_action no es None es porque se llamó al método desde una señal de un item, y valido los items...
        if item_action is not None:
            self.__validateSalesInputListItems(item_action)

        # sino, se llamó al método desde la señal de 'self.lineEdit_paid'
        elif self.ui.label_total.text() != "TOTAL":
            # si no hay un valor en lineEdit_paid, le pone 0
            if not self.ui.lineEdit_paid.text():
                self.ui.lineEdit_paid.setText(str(0.0))
            # formatea el texto de 'self.lineEdit_paid'
            self.ui.lineEdit_paid.setText(self.ui.lineEdit_paid.text().replace(",","."))
            if self.ui.lineEdit_paid.text().endswith("."):
                self.ui.lineEdit_paid.setText(self.ui.lineEdit_paid.text().strip("."))

            # convierte a float el precio total y lo abonado
            try:
                re_total_cost = search(">[0-9]+[.]?[0-9]{1,2}<", self.ui.label_total.text())
                re_total_cost = round(float(re_total_cost.group().strip("><")), 2) if re_total_cost else None
                total_paid = round(float(self.ui.lineEdit_paid.text()), 2) if self.ui.lineEdit_paid.text() else 0.0
            except:
                pass

            # verifica si 'self.lineEdit_paid' tiene un valor mayor al total
            if total_paid > re_total_cost: # si lo abonado es mayor al total se muestra el cambio
                self.ui.label_total_change.setText(f"{round(total_paid - re_total_cost, 2)}")

            elif total_paid == re_total_cost:
                self.ui.label_total_change.setText("")
        return None


    @Slot()
    def addSalesInputListItem(self) -> None:
        '''Crea un item que se colocará dentro de 'sales_input_list', y que representa la venta de un producto.
        \nRetorna 'None'.'''
        listWidgetItem:QListWidgetItem = QListWidgetItem()
        name:str = f"item_{self.items_objectNames}"
        item:ListItem = ListItem(self.ui.sales_input_list, listWidgetItem, name)

        # incremento el contador
        self.items_objectNames += 1
        
        # conecta la señal 'SignalToParent.allFieldsValid'
        item.signalToParent.allFieldsValid.connect(lambda dict_item: self.validateSalesFields(dict_item))
        # conecta la señal 'SignalToParent.deletedItem'
        item.signalToParent.deletedItem.connect(lambda deleted_item: self.validateSalesFields(deleted_item))

        # coloca el widget dentro del item
        listWidgetItem.setSizeHint(item.size())
        self.ui.sales_input_list.addItem(listWidgetItem)
        self.ui.sales_input_list.setItemWidget(listWidgetItem, item)

        # pone el foco en el item nuevo
        self.ui.sales_input_list.setFocus()
        self.ui.sales_input_list.setCurrentItem(listWidgetItem)
        item.findChild(QComboBox, "comboBox_productName").setFocus()

        # desactiva btn_end_sale cuando se agrega un producto
        self.ui.btn_end_sale.setEnabled(False)
        return None


    def __resetListAndFields(self) -> None:
        '''Limpia la lista 'sales_input_list' y los campos, reinicia las variables e inhabilita el botón de finalizar 
        venta. Retorna 'None'.'''
        self.ui.sales_input_list.clear()
        self.VALID_ITEMS.clear()
        self.ITEMS_VALUES.clear()
        self.items_objectNames = 0
        self.ui.label_total.setText("TOTAL")
        self.ui.label_total_change.setText("")
        self.ui.lineEdit_paid.setText("")
        self.ui.btn_end_sale.setEnabled(False)
        self.debtor_chosen = None
        return None
    

    def __assignDebtorChosenOption(self, value:int) -> None:
        '''Simplemente asigna el valor recibido por la señal 'debtorChosen' en 'self.debtor_chosen'. Retorna 'None'.'''
        self.debtor_chosen = value
        return None


    @Slot()
    def handleFinishedSale(self) -> None:
        '''Obtiene los datos de los campos de los items y hace las consultas necesarias a la base de datos.
        \nSi la cantidad abonada es menor al precio total se crea un Dialog que pide datos del deudor.
        \nPor cada producto que se vende, hace un INSERT a Detalle_Ventas y Ventas, y si hay una deuda también a Deudas; actualiza el \
        stock en Productos.
        \nFinalmente limpia los campos y desactiva el botón 'btn_end_sale'.
        \nRetorna 'None'.'''
        item:tuple[str,tuple]
        total_paid:float
        re_total_price:Match | float | None
        total_due:float # contador para verificar qué productos van o no en Deudas, y cuánto resta por pagar de ese producto

        '''
            Decidí que cuando se hacen ventas (sin importar la cantidad de productos diferentes) y el comprador paga 
            menos del total, esa cantidad sea distribuída entre los primeros productos. 
            ejemplo: una persona lleva 3 productos -> 1 de $3.000, 1 de $2.000 y otro de $4.000, pero paga $4.000.
                esos $4.000 se descuentan, primero, del primer producto:
                    $4.000 - $3.000 = $1.000
                    $1.000 - $2.000 = $-1.000 <-- -1.000 es lo que queda del 2do producto, más el 3er producto.
                luego se agrega a Deudas los $1.000 que quedaron del 2do producto y también el 3er producto, pero 
                no el 1ro que quedó pago.
        '''

        # si no hay un valor en lineEdit_paid, le pone 0
        if not self.ui.lineEdit_paid.text():
            self.ui.lineEdit_paid.setText(str(0.0))
        
        # verifico si lo abonado es menor al total para mostrar el Dialog con los datos del deudor
        try:
            # obtengo el precio total
            re_total_price = search(">[0-9]+(\.|,)[0-9]{0,2}<", self.ui.label_total.text())
            re_total_price = float(re_total_price.group().strip("><")) if re_total_price else None
            # obtengo el total pagado
            total_paid = float(self.ui.lineEdit_paid.text())
            # si lo abonado es menor al total muestra el Dialog para agregar al deudor (si no existe en "Deudores" se crea)
            if re_total_price and total_paid < re_total_price:
                dialog = DebtorDataDialog()
                dialog.setAttribute(Qt.WA_DeleteOnClose, True)
                dialog.signalToParent.debtorChosen.connect(lambda option: self.__assignDebtorChosenOption(option))
                dialog.exec()
        except:
            pass

        if total_paid < re_total_price and self.debtor_chosen:
            total_due = total_paid
            # recorre cada item y hace las consultas INSERT y UPDATE (a Productos)
            for item in self.ITEMS_VALUES.items():
                makeInsertQuery("INSERT INTO Ventas(fecha_hora, detalles_venta) VALUES(?,?);", (item[1][5], item[1][3],))
                # Deudas y Detalle_Ventas (con IDdeuda)
                total_due -= item[1][4] # deuda = total abonado - subtotal
                if total_due < 0: # el producto es deuda
                    makeInsertQuery("INSERT INTO Deudas(fecha_hora, total_adeudado, IDdeudor) VALUES(?,?,?);", (item[1][5], abs(total_due), self.debtor_chosen[0]))
                    
                    # ? ya probé la consulta de abajo y al parecer funciona bien. Los registros de Detalle_Ventas 
                    # ? apuntan a donde deben... pero igualmente prefiero estar atento a esto...
                    makeInsertQuery("INSERT INTO Detalle_Ventas(cantidad, costo_total, IDproducto, IDventa, abonado, IDdeuda) VALUES(?, ?, (SELECT IDproducto FROM Productos WHERE nombre = ?), (SELECT IDventa FROM Ventas WHERE fecha_hora = ? AND detalles_venta = ?), ?, (SELECT IDdeuda FROM Deudas WHERE fecha_hora = ? AND IDdeudor = ? ORDER BY IDdeuda DESC LIMIT 1));", 
                                    (item[1][1], item[1][4], item[1][0], item[1][5], item[1][3], item[1][4] - abs(total_due), item[1][5], self.debtor_chosen[0], ))
                    total_due = 0
                else: # el producto NO es deuda
                    makeInsertQuery("INSERT INTO Detalle_Ventas(cantidad, costo_total, IDproducto, IDventa, abonado, IDdeuda) VALUES(?, ?, (SELECT IDproducto FROM Productos WHERE nombre = ?), (SELECT IDventa FROM Ventas WHERE fecha_hora = ? AND detalles_venta = ?), ?, NULL);", (item[1][1], item[1][4], item[1][0], item[1][5], item[1][3], item[1][4],))
                # actualiza el stock
                makeUpdateQuery("UPDATE Productos SET stock = stock - ? WHERE nombre = ?;", (item[1][1], item[1][0],))
            self.__resetListAndFields()

        elif total_paid >= re_total_price:
            for item in self.ITEMS_VALUES.items():
                makeInsertQuery("INSERT INTO Ventas(fecha_hora, detalles_venta) VALUES(?,?);", (item[1][5], item[1][3],))
                makeInsertQuery("INSERT INTO Detalle_Ventas(cantidad, costo_total, IDproducto, IDventa, abonado, IDdeuda) VALUES(?, ?, (SELECT IDproducto FROM Productos WHERE nombre = ?), (SELECT IDventa FROM Ventas WHERE fecha_hora = ? AND detalles_venta = ?), ?, NULL);", (item[1][1], item[1][4], item[1][0], item[1][5], item[1][3], item[1][4],))
                makeUpdateQuery("UPDATE Productos SET stock = stock - ? WHERE nombre = ?;", (item[1][1], item[1][0],))
            self.__resetListAndFields()
        return None


    
    #### DEUDAS ######################################################
    def __fillDebtsTable(self) -> None:
        '''Es llamada desde 'handleTableToFill'. Recorre cada item y, dependiendo de la columna en la que esté, crea instancias \
        de las siguientes clases:\n
        - columna 0 (nombre completo): instancia de 'DebtsTablePersonData'.
        - columna 1 (productos): ...
        \nSi la columna es la 2 (total adeudado) coloca el total que se adeuda.
        \nRetorna 'None'.'''
        for row in range(self.ui.table_debts.rowCount()):
            widget = DebtsTablePersonData(tableWidget=self.ui.table_debts, full_name="nombre completo")
            self.ui.table_debts.setCellWidget(row, 0, widget)
        
            





def main():
    logging.basicConfig(level=logging.DEBUG)
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())


# MAIN #########################################################################################################
if __name__=='__main__':
    main()