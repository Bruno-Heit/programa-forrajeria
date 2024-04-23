# SQLITE3

from PySide6.QtWidgets import (QTableWidget, QComboBox, QHeaderView, QTableWidgetItem, QListWidget,
                               QLineEdit, QLabel, QCompleter, QFrame, QWidget, QDateTimeEdit)
from PySide6.QtCore import (QRegularExpression, QModelIndex, Qt, QPropertyAnimation, 
                            QEasingCurve, QDateTime, QDate, QTime)
from PySide6.QtGui import (QRegularExpressionValidator)

from re import (Match, match, search, sub, IGNORECASE)

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


# def getUpdateSqlAndParameters(tableWidget:QTableWidget, lineEdit:QLineEdit, curr_index:QModelIndex, ids:tuple) -> tuple[str, tuple[str]]:
#     '''Recibe el 'QTableWidget', el item que fue modificado, el 'QLineEdit' y los IDs de los elementos. Retorna una 
#     tupla con la consulta Sql y una tupla con los parámetros que recibe la consulta.'''
#     sql:str
#     params:tuple
#     re_stock:Match | None
#     re_unit:Match | None
    
#     match tableWidget.objectName():
#         # case "displayTable":
#             # params = (lineEdit.text(), str(ids[curr_index.row()]))
#             # match curr_index.column():
#                 # case 1: # columna de nombre
#                 #     sql = "UPDATE Productos SET nombre = ? WHERE IDproducto = ?;"
#                 # case 2: # columna de descripción
#                 #     sql = "UPDATE Productos SET descripcion = ? WHERE IDproducto = ?;"
#                 # case 3: # columna de stock
#                     # re_stock = match("[0-9]+(\.)?[0-9]{0,2}", lineEdit.text())
#                     # re_stock = re_stock.group() if re_stock is not None else None
#                     # re_unit = search("[a-zA-Z]*$", lineEdit.text(), IGNORECASE)
#                     # re_unit = re_unit.group() if re_unit is not None else None
#                     # if re_stock:
#                     #     params = (re_stock, re_unit, str(ids[curr_index.row()]))
#                     #     sql = "UPDATE Productos SET stock = ?, unidad_medida = ? WHERE IDproducto = ?;"
#                 # case 4: # precio unitario
#                 #     sql = "UPDATE Productos SET precio_unit = ? WHERE IDproducto = ?;"
#                 # case 5: # precio comercial
#                 #     sql = "UPDATE Productos SET precio_comerc = ? WHERE IDproducto = ?;"
        
#         # case "table_sales_data":
#         #     # params = (lineEdit.text(), str(ids[curr_index.row()]))
#         #     match curr_index.column():
#         #         case 0: # detalle de venta
#         #             sql = "UPDATE Ventas SET detalles_venta = ? WHERE IDventa = (SELECT IDventa FROM Detalle_Ventas WHERE ID_detalle_venta = ?);"
#         #         case 1: # cantidad
#         #             sql = "UPDATE Detalle_Ventas SET cantidad = ? WHERE ID_detalle_venta = ?;"
#         #         case 3: # costo total
#         #             sql = "UPDATE Detalle_Ventas SET costo_total = ? WHERE ID_detalle_venta = ?;"
#         #         case 4: # abonado
#         #             sql = "UPDATE Detalle_Ventas SET abonado = ? WHERE ID_detalle_venta = ?;"
            
#     return sql, params


def createTableColumnLineEdit(table_widget:QTableWidget, curr_index:QModelIndex) -> QLineEdit:
    '''
    Crea un QLineEdit para ser colocado en la celda seleccionada con índice 'curr_index', y dependiendo de la columna 
    donde esté la celda le aplica un validador al QLineEdit. Si el QTableWidget es "inventario" y la columna es "nombre" 
    también le asigna un QCompleter con los nombres de los productos.
    
    Retorna un QLineEdit.
    '''
    float_re:QRegularExpression = QRegularExpression("[0-9]{0,7}(\.|,)?[0-9]{0,2}")
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
                    lineedit.setValidator(SalePaidValidator(lineedit))

    table_widget.setCellWidget(curr_index.row(), curr_index.column(), lineedit)
    
    return lineedit


# def overwriteTableCellOldValue(table_widget:QTableWidget, curr_index:QModelIndex, params:tuple = None, cb_curr_text:str = None) -> None:
#     '''
#     Reemplaza el valor anterior de la celda en la posición 'curr_index' en 'table_widget' con el nuevo valor.
    
#     PARAMS:
#     - params: si la celda tiene un QLineEdit:
#         - la 1ra posición es a la que hay que acceder para obtener el contenido
#         - la 2da posición es sólo por si el contenido está compuesto por 2 tipos de valores (ej.: stock en 'displayTable').
#     - cb_curr_text es por si la celda tiene un QComboBox: representa al texto del QComboBox.
    
#     Retorna None.
#     '''
#     # coloca el valor nuevo en la celda
#     match table_widget.objectName():
#         # case "displayTable":
#         #     if curr_index.column() == 0: # categoría
#         #         table_widget.item(curr_index.row(), curr_index.column()).setText(cb_curr_text)
#         #     elif curr_index.column() == (1 or 2 or 4 or 5): # nombre/descripción/precio unitario/precio comercial
#         #         table_widget.item(curr_index.row(), curr_index.column()).setText(str(params[0]).strip())
#         #     elif curr_index.column() == 3: # stock
#         #         table_widget.item(curr_index.row(), curr_index.column()).setText(f"{params[0]} {str(params[1]).strip()}")
        
#         case "table_sales_data":
#             # if curr_index.column() == 1: # cantidad (int|float + str)
#                 # table_widget.item(curr_index.row(), curr_index.column()).setText(f"{params[0]} {params[1]}")
#             # elif curr_index.column() == 2: # producto
#             #     table_widget.item(curr_index.row(), curr_index.column()).setText(f"{cb_curr_text}")
#             # else: # detalle de venta/costo total/abonado/fecha y hora
#             #     table_widget.item(curr_index.row(), curr_index.column()).setText(f"{str(params[0]).strip()}")

#         case "":
#             pass
#     return None

def createTableColumnDateTimeEdit(tableWidget:QTableWidget, curr_index:QModelIndex) -> QDateTimeEdit:
    '''Crea un 'QDateTimeEdit' en el 'tableWidget' indicado y en la celda indicada por 'curr_index'. Retorna un 
    'QDateTimeEdit'.'''
    dateTimeEdit = QDateTimeEdit(parent=tableWidget)
    curr_datetime:QDateTime = QDateTime()
    date:QDate
    time:QTime

    dateTimeEdit.setMinimumDateTime(QDateTime().fromString("1/1/2022 00:00", "d/M/yyyy HH:mm"))
    dateTimeEdit.setCalendarPopup(True)
    # por alguna razón, QDateTime().fromString() no me funcionó, así que obtengo la fecha y la hora separadas...
    cell_datetime = tableWidget.item(curr_index.row(), curr_index.column()).text()
    date = QDate().fromString(cell_datetime.split(" ")[0].strip(), "d/M/yyyy") # bien
    time = QTime().fromString(cell_datetime.split(" ")[1].strip(), "HH:mm") # bien
    # y las junto en el curr_datetime...
    curr_datetime.setDate(date)
    curr_datetime.setTime(time)
    # al final asigno la fecha y la hora al dateTimeEdit
    dateTimeEdit.setDateTime(curr_datetime)
    tableWidget.setCellWidget(curr_index.row(), curr_index.column(), dateTimeEdit)

    return dateTimeEdit


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




