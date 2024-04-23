# SQLITE3

from PySide6.QtWidgets import (QTableWidget, QComboBox, QHeaderView, QTableWidgetItem, QListWidget,
                               QLineEdit, QLabel, QCompleter, QFrame, QWidget, QDateTimeEdit)
from PySide6.QtCore import (QRegularExpression, QModelIndex, Qt, QPropertyAnimation, 
                            QEasingCurve, QDateTime, QDate, QTime)
from PySide6.QtGui import (QRegularExpressionValidator)

from re import (Match, match, search, sub, IGNORECASE)

from resources import (rc_icons)
from utils.dboperations import *
from utils.customvalidators import *


# side bars
def toggleSideBar(side_bar:QFrame, parent:QWidget|QFrame, body:QFrame, max_width:int=250) -> None:
    '''Anima la apertura o cierre de los menús laterales. Retorna None.'''
    # OBTENER el width actual
    start_value = side_bar.width()
    if start_value == 40:
        end_value = max_width
        signal = 1 # señal para mostrar los widgets
    else:
        end_value = 40
        signal = 0 # señal para ocultar los widgets
    # funciones de animación
    anim = QPropertyAnimation(side_bar, b"minimumWidth", parent) # NOTE: hay que agregarle el 'parent'.
    anim.setDuration(140)
    anim.setStartValue(start_value)
    anim.setEndValue(end_value)
    anim.setEasingCurve(QEasingCurve.Type.InOutCubic)
    anim.start()
    # una vez terminada la animación, llama a la función de abajo, que muestra o esconde los widgets
    anim.finished.connect(lambda: __toggleSideBarWidgetsVisibility(body, signal))
    return None


def __toggleSideBarWidgetsVisibility(body:QFrame, signal:int):
    '''Muestra o esconde los widgets dentro del menú lateral al terminar la animación de apertura o cierre del 
    menú lateral. Retorna None.'''
    match signal:
        case 0:
            body.hide()
        case 1:
            body.show()
    return None
#========================================================================================================================
# tooltips
def set_tables_ListWidgetItemsTooltip(listWidget:QListWidget, categories_descriptions:tuple[str]) -> None:
    '''Recibe una tupla con las descripciones de las categorías y crea los tooltips para cada item de 'tables_ListWidget'.
    Retorna 'None'.'''
    # NOTE: LA RAZÓN POR LA QUE TUVE QUE USAR UN 'MATCH' ES PORQUE EL ORDEN DE LAS CATEGORÍAS EN LA LISTA NO ES 
    # EL MISMO ORDEN DE LAS CATEGORÍAS EN LA BASE DE DATOS; IGUALMENTE NO HAY EFECTOS NEGATIVOS EN EL RENDIMIENTO 
    # DEL PROGRAMA AL USAR UN 'MATCH' PORQUE TIENE UNA COMPLEJIDAD DE TIEMPO DE O(1).
    for row in range(listWidget.count()-1):
        match listWidget.item(row).text():
            case "Alimentos domésticos":
                listWidget.item(row).setToolTip(f"<html><head/><body><p><span style=\" font-size:11pt; color: #111;\">{categories_descriptions[0]}</span></p></body></html>")
            case "Alimentos de granja":
                listWidget.item(row).setToolTip(f"<html><head/><body><p><span style=\" font-size:11pt; color: #111;\">{categories_descriptions[1]}</span></p></body></html>")
            case "Cereales/arroz":
                listWidget.item(row).setToolTip(f"<html><head/><body><p><span style=\" font-size:11pt; color: #111;\">{categories_descriptions[2]}</span></p></body></html>")
            case "Accesorios de pesca":
                listWidget.item(row).setToolTip(f"<html><head/><body><p><span style=\" font-size:11pt; color: #111;\">{categories_descriptions[3]}</span></p></body></html>")
            case "Limpieza/química":
                listWidget.item(row).setToolTip(f"<html><head/><body><p><span style=\" font-size:11pt; color: #111;\">{categories_descriptions[4]}</span></p></body></html>")
            case "Gas":
                listWidget.item(row).setToolTip(f"<html><head/><body><p><span style=\" font-size:11pt; color: #111;\">{categories_descriptions[5]}</span></p></body></html>")
            case "Electrodomésticos":
                listWidget.item(row).setToolTip(f"<html><head/><body><p><span style=\" font-size:11pt; color: #111;\">{categories_descriptions[6]}</span></p></body></html>")
            case "Electrónicos":
                listWidget.item(row).setToolTip(f"<html><head/><body><p><span style=\" font-size:11pt; color: #111;\">{categories_descriptions[7]}</span></p></body></html>")
            case "Indumentaria":
                listWidget.item(row).setToolTip(f"<html><head/><body><p><span style=\" font-size:11pt; color: #111;\">{categories_descriptions[8]}</span></p></body></html>")
            case "Herramientas":
                listWidget.item(row).setToolTip(f"<html><head/><body><p><span style=\" font-size:11pt; color: #111;\">{categories_descriptions[9]}</span></p></body></html>")
            case "Accesorios para piletas":
                listWidget.item(row).setToolTip(f"<html><head/><body><p><span style=\" font-size:11pt; color: #111;\">{categories_descriptions[10]}</span></p></body></html>")
            case "Accesorios para mascotas":
                listWidget.item(row).setToolTip(f"<html><head/><body><p><span style=\" font-size:11pt; color: #111;\">{categories_descriptions[11]}</span></p></body></html>")
            case "Arenas":
                listWidget.item(row).setToolTip(f"<html><head/><body><p><span style=\" font-size:11pt; color: #111;\">{categories_descriptions[12]}</span></p></body></html>")
            case "Accesorios para boyeros":
                listWidget.item(row).setToolTip(f"<html><head/><body><p><span style=\" font-size:11pt; color: #111;\">{categories_descriptions[13]}</span></p></body></html>")
            case "Venenos":
                listWidget.item(row).setToolTip(f"<html><head/><body><p><span style=\" font-size:11pt; color: #111;\">{categories_descriptions[14]}</span></p></body></html>")
            case "Accesorios para jardinería":
                listWidget.item(row).setToolTip(f"<html><head/><body><p><span style=\" font-size:11pt; color: #111;\">{categories_descriptions[15]}</span></p></body></html>")
            case "Varios":
                listWidget.item(row).setToolTip(f"<html><head/><body><p><span style=\" font-size:11pt; color: #111;\">{categories_descriptions[16]}</span></p></body></html>")
    return None



#========================================================================================================================
def getProductsCategories() -> list[str] | None:
    '''
    Hace una consulta SELECT a la base de datos y toma las categorías que hay. Devuelve una lista con las 
    categorías. 
    '''
    connection = createConnection("database/inventario.db")
    if not connection:
        return None
    cursor = connection.cursor()
    query:list[tuple] = cursor.execute("SELECT nombre_categoria FROM Categorias;").fetchall()
    # convierto la lista de tuplas en una lista de strings...
    query:list[str] = [q[0] for q in query]
    connection.close()
    return query


def getProductNames() -> list[str]:
    '''
    Hace una consulta SELECT a la base de datos y obtiene todos los nombres de productos que hay.
    
    Retorna una lista con los nombres.
    '''
    conn = createConnection("database/inventario.db")
    if not conn:
        return None
    cursor = conn.cursor()
    
    query = cursor.execute("SELECT nombre FROM Productos;").fetchall()
    
    # convierto la lista de tuplas en una lista de strings...
    query:list[str] = [q[0] for q in query]
    
    conn.close()
    return query


def getCategoriesDescription() -> tuple[str] | None:
    '''
    Hace una consulta SELECT a la base de datos y toma las descripciones de las categorías que hay. Devuelve una tupla 
    con las categorías.
    '''
    connection = createConnection("database/inventario.db")
    if not connection:
        return None
    cursor = connection.cursor()
    query:list[tuple] = cursor.execute("SELECT descripcion FROM Categorias;").fetchall()
    query_tuple = list()
    connection.close()
    for tupl in query:
        query_tuple.append(tupl[0])
    return tuple(query_tuple)


def setTableWidthPolitics(tableWidget:QTableWidget) -> None:
    '''
    Recibe un 'QTableWidget' y especifica las políticas de ancho de las columnas. 
    
    Retorna None.
    '''
    match tableWidget.objectName():
        case "displayTable":
            header = tableWidget.horizontalHeader()
            header.setSectionResizeMode(QHeaderView.ResizeToContents)
            header.setSectionResizeMode(0, QHeaderView.Stretch)
            header.setSectionResizeMode(2, QHeaderView.Stretch)
            header.setMaximumSectionSize(200)
        case "table_sales_data":
            header = tableWidget.horizontalHeader()
            header.setSectionResizeMode(QHeaderView.ResizeToContents)
            header.setSectionResizeMode(0, QHeaderView.Stretch)
            header.setSectionResizeMode(2, QHeaderView.Stretch)
            header.setMaximumSectionSize(200)
        case "table_debts":
            header = tableWidget.horizontalHeader()
            header.setSectionResizeMode(QHeaderView.ResizeToContents)
            header.setSectionResizeMode(0, QHeaderView.Stretch)
            header.setSectionResizeMode(1, QHeaderView.Stretch)
            header.setMaximumSectionSize(200)
    return None


def getSelectedTableRows(tableWidget:QTableWidget) -> tuple:
    '''Obtiene todas las filas seleccionadas del QTableWidget. Retorna una tupla con las filas.'''
    selected_indexes:list = []
    for index in tableWidget.selectedIndexes():
        if index.row() not in selected_indexes:
            selected_indexes.append(index.row())
    return tuple(selected_indexes)


#========================================================================================================================
def removeTableCellsWidgets(table_widget:QTableWidget) -> None:
    '''
    Recorre 'table_widget' y borra todos los widgets creados en las celdas. 
    
    Retorna None.
    '''
    # si cell_widget es un QComboBox|QLineEdit|QDateTimeEdit lo elimina...
    for row in range(table_widget.rowCount()):
        for col in range(table_widget.columnCount()):
            if isinstance(table_widget.cellWidget(row, col), (QComboBox, QLineEdit, QDateTimeEdit)):
                table_widget.removeCellWidget(row, col)
    return None


def createTableColumnComboBox(table_widget:QTableWidget, curr_index:QModelIndex, curr_text:str) -> QComboBox:
    '''
    Crea el combobox que se encontrará dentro de la celda de la columna especificada por 'curr_index' en la tabla 
    'table_widget'.
    
    PARAMS:
    - table_widget: el QTableWidget donde se colocará el QComboBox.
    - curr_index: índice seleccionado de la celda de 'table_widget'.
    - curr_text: el elemento que está seleccionado inicialmente en el QComboBox.
    
    Retorna un QComboBox.
    '''
    combobox = QComboBox(table_widget)
    combobox.setEditable(False)
    combobox.setFrame(False)

    match table_widget.objectName():
        case "displayTable":
            combobox.addItems(getProductsCategories())
            combobox.setPlaceholderText("Elegir categoría")
        
        case "table_sales_data":
            combobox.addItems(getProductNames())
            combobox.setPlaceholderText("Elegir producto")
        
    # coloca como índice actual el que tenga el string 'curr_text', sino hay el índice actual es -1
    combobox.setCurrentIndex(combobox.findText(curr_text))
    table_widget.setCellWidget(curr_index.row(), curr_index.column(), combobox)
    return combobox


def createTableColumnLineEdit(table_widget:QTableWidget, curr_index:QModelIndex) -> QLineEdit:
    '''
    Crea un QLineEdit para ser colocado en la celda de 'table_widget' seleccionada con índice 'curr_index', y 
    dependiendo de la columna donde esté la celda le aplica un validador al QLineEdit y/o un QCompleter.
    
    Retorna un QLineEdit.
    '''
    lineedit:QLineEdit = QLineEdit(table_widget)

    lineedit.setText(table_widget.item(curr_index.row(), curr_index.column()).text())
    
    # a continuación coloca validators y completers dependiendo de la columna...
    match table_widget.objectName():
        case "displayTable":
            match curr_index.column():
                case 1: # nombre
                    lineedit.setCompleter(createCompleter(type=3))
                    lineedit.setValidator(ProductNameValidator(lineedit))
                
                case 3: # stock
                    lineedit.setValidator(ProductStockValidator(lineedit))
                
                case 4: # precio unitario
                    lineedit.setValidator(ProductUnitPriceValidator(lineedit))
                
                case 5: # precio comercial
                    lineedit.setValidator(ProductComercPriceValidator(lineedit))
        
        
        case "table_sales_data":
            match curr_index.column():
                case 0: # detalle de venta
                    lineedit.setValidator(SaleDetailsValidator(lineedit))
                
                case 1: # cantidad
                    lineedit.setValidator(SaleQuantityValidator(lineedit))
                    # sólo permite editar la cantidad, no la unidad
                    lineedit.setText(table_widget.item(curr_index.row(), curr_index.column()).text().split(" ")[0].strip())
                
                case 3: # costo total
                    lineedit.setValidator(SaleTotalCostValidator(lineedit))
                
                case 4: # abonado
                    # completer con costo total (misma fila, columna 3)
                    lineedit.setCompleter( QCompleter( [table_widget.item(curr_index.row(), 3).text()] ) )
                    lineedit.setValidator(SalePaidValidator(lineedit))

    table_widget.setCellWidget(curr_index.row(), curr_index.column(), lineedit)
    
    return lineedit


def createTableColumnDateTimeEdit(table_widget:QTableWidget, curr_index:QModelIndex) -> QDateTimeEdit:
    '''
    Crea un QDateTimeEdit en 'table_widget' y en la celda indicada por 'curr_index'. Además le asigna un estilo 
    QSS.
    
    Retorna un QDateTimeEdit.
    '''
    datetimeedit = QDateTimeEdit(parent=table_widget)
    curr_datetime:QDateTime = QDateTime()
    date:QDate
    time:QTime

    datetimeedit.setMinimumDateTime(QDateTime().fromString("1/1/2022 00:00", "d/M/yyyy HH:mm"))
    datetimeedit.setCalendarPopup(True)
    
    # por alguna razón, QDateTime().fromString() no me funcionó, así que obtengo la fecha y la hora separadas...
    cell_datetime = table_widget.item(curr_index.row(), curr_index.column()).text()
    date = QDate().fromString(cell_datetime.split(" ")[0].strip(), "d/M/yyyy")
    time = QTime().fromString(cell_datetime.split(" ")[1].strip(), "HH:mm")
    
    # y las junto en el curr_datetime...
    curr_datetime.setDate(date)
    curr_datetime.setTime(time)
    
    # al final asigno la fecha y la hora al datetimeedit
    datetimeedit.setDateTime(curr_datetime)
    
    # le asigno un estilo
    datetimeedit.setStyleSheet(
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
    
    table_widget.setCellWidget(curr_index.row(), curr_index.column(), datetimeedit)

    return datetimeedit


#========================================================================================================================
def setSearchBarValidator(searchBar:QLineEdit) -> None:
    '''Coloca un 'Validator' en el 'searchBar' de entrada. Retorna 'None'.'''
    re = QRegularExpression("[^;,.?¿\'\'\"\"\t\r]*")
    validator = QRegularExpressionValidator(re, searchBar)
    searchBar.setValidator(validator)
    return None


#========================================================================================================================
def createCompleter(type:int = 1 | 2 | 3) -> QCompleter:
    '''
    Crea un QCompleter, establece sus atributos y lo coloca dentro de 'lineedit'.
    
    PARAMS:
    - type: valor entero que determina los datos con los que llenar el QCompleter. 
        - 1: lo carga con nombres de personas con cuenta corriente.
        - 2: lo carga con apellidos de personas con cuenta corriente.
        - 3: lo carga con nombres de productos.
    
    Retorna un QCompleter.
    '''
    completer:QCompleter
    query:list
    
    if type == 1: # nombres de personas con cta. corriente
        query = makeReadQuery("SELECT nombre FROM Deudores;")
        names = [name[0] for name in query]
        completer = QCompleter(names)
        
    elif type == 2:# apellidos de personas con cta. corriente
        query = makeReadQuery("SELECT apellido FROM Deudores;")
        surnames = [surname[0] for surname in query]
        completer = QCompleter(surnames)
        
    
    elif type == 3: # nombres de productos
        completer = QCompleter(getProductNames())
    
    completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
    completer.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
    completer.setMaxVisibleItems(10)

    return completer




