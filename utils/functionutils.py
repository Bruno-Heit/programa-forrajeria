# SQLITE3
import sys
import os
from sqlite3 import Connection

from PySide6.QtWidgets import (QTableWidget, QComboBox, QHeaderView, QTableWidgetItem, QListWidget,
                               QLineEdit, QLabel, QCompleter, QFrame, QWidget, QDateTimeEdit)
from PySide6.QtCore import (QRegularExpression, QModelIndex, Qt, QPropertyAnimation, 
                            QEasingCurve, QDateTime, QDate, QTime)
from PySide6.QtGui import (QRegularExpressionValidator)

from re import (Match, match, search, sub, IGNORECASE)


'''
La siguiente función sirve para ayudar a pyinstaller a completar el path completo a un archivo, 
y se tiene que hacer esto porque tiene un error y a veces no puede hacerlo.
'''
def pyinstallerCompleteResourcePath(relative_path:str) -> str:
    '''Obtiene el path completo para el archivo especificado y lo devuelve. Retorna un 'str'.'''
    base_path:str
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)



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
#------------------------------------------------
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



#------------------------------------------------
def createConnection(db_name:str) -> Connection | None:
    '''Crea una conexión a la base de datos y devuelve la conexión, si no se pudo devuelve None.'''
    from sqlite3 import connect
    from sqlite3 import Error
    try:
        connection = connect(pyinstallerCompleteResourcePath(db_name))
    except Error as e:
        return None
    return connection


def getProductsCategories() -> list[str] | None:
    '''Hace una consulta SELECT a la base de datos y toma las categorías que hay. Devuelve una lista con las categorías. 
    Si hubo un error conectándose a la base  de datos devuelve 'None'.'''
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
    '''Hace una consulta SELECT a la base de datos y obtiene todos los nombres de productos que hay. Retorna una 
    lista con los nombres.'''
    conn = createConnection("database/inventario.db")
    if not conn:
        return None
    cursor = conn.cursor()
    sql = "SELECT nombre FROM Productos;"
    query = cursor.execute(sql).fetchall()
    # convierto la lista de tuplas en una lista de strings...
    query:list[str] = [q[0] for q in query]
    conn.close()
    return query


def getCategoriesDescription() -> tuple[str] | None:
    '''Hace una consulta SELECT a la base de datos y toma las descripciones de las categorías que hay. Devuelve una tupla 
    con las categorías. Si hubo un error conectándose a la base  de datos devuelve 'None'.'''
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
    '''Recibe un 'QTableWidget' y especifica las políticas de ancho de las columnas. Retorna un 'QHeaderView'.'''
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


def getTableWidgetRowCount(count_sql:str=None, count_params:tuple=None) -> int:
    '''
    Hace una consulta SELECT a la base de datos y obtiene la cantidad de filas que debe tener la tabla. 
    
    Retorna la cantidad como 'int'.
    '''
    row_count:int
    conn = createConnection("database/inventario.db")
    if not conn:
        return
    cursor = conn.cursor()
    # si no se pasó un sql y count_params hago de cuenta que la tabla es 'displayTable' y se seleccionó "MOSTRAR TODOS"...
    if not count_sql and not count_params:
        count_sql:str = "SELECT COUNT(*) FROM Productos;"
        row_count = cursor.execute(count_sql).fetchone()[0]
    elif count_sql and not count_params:
        row_count = cursor.execute(count_sql).fetchone()[0]
    else:
        row_count = cursor.execute(count_sql, count_params).fetchone()[0]
    conn.close()
    return row_count


def getIDsFromTable() -> tuple:
    '''Hace una consulta SELECT y obtiene los IDs de "Ventas" y de "Deudas". Retorna una tupla con los IDs.'''
    sql:str
    sql = "SELECT v.IDventa, d.IDdeuda FROM Detalle_Ventas as dv \
        INNER JOIN Productos AS p ON dv.IDproducto = p.IDproducto \
        INNER JOIN Ventas AS v ON dv.IDventa = v.IDventa;"
    ids = [q[0] for q in makeReadQuery(sql)]
    return tuple(ids)


# READ QUERY
def makeReadQuery(sql:str, params:tuple = None) -> list:
    '''Hace la consulta SELECT a la base de datos y devuelve los valores de las filas seleccionadas. Retorna una 'list' 
    con los valores.'''
    conn = createConnection("database/inventario.db")
    if not conn:
        return
    cursor = conn.cursor()
    if not params:
        query = cursor.execute(sql).fetchall()
    else:
        query = cursor.execute(sql, params).fetchall()
    conn.close()
    return query


def setTableWidgetContent(tableWidget:QTableWidget, row_count:int=None, query:list=None) -> tuple | None:
    '''Recibe un QTableWidget, la cantidad de filas que tiene y una consulta SELECT ya hecha con los valores de la base 
    de datos.
    \n\tColoca todos los datos de la query en el QTableWidget. 
    Dependiendo del parámetro QTableWidget, retorna una tupla con los IDs de la tabla correspondiente o 'None'.'''
    n_row:int = 0
    id_list:list = []

    # guardo en una lista todos los IDs (no me interesan los IDs de Deudas)
    match tableWidget.objectName():
        case "table_debts":
            pass
        case _:
            for id_col in query:
                id_list.append(id_col[0])
            id_list = tuple(id_list)

    # limpia la tabla
    tableWidget.clearContents()
    # determina la cantidad de filas que tendrá la tabla
    tableWidget.setRowCount(row_count)
    
    # y dependiendo de cuál tabla se seleccionó la llena con sus respectivos valores...
    match tableWidget.objectName():
        case "displayTable":
            for row in query:
                tableWidget.setItem(n_row, 0, QTableWidgetItem(str(row[1])) ) # col.0 tiene categoría
                tableWidget.setItem(n_row, 1, QTableWidgetItem(str(row[2])) ) # col.1 tiene nombre
                tableWidget.setItem(n_row, 2, QTableWidgetItem(str(row[3]) if str(row[3]) != None else "") ) # col.2 tiene descripción
                stock:float = row[4]
                if stock.is_integer():
                    try:
                        stock = int(stock)
                    except ValueError:
                        pass
                tableWidget.setItem(n_row, 3, QTableWidgetItem(str(f"{stock} {row[5]}")) ) # col.3 tiene stock y unidad_medida
                tableWidget.setItem(n_row, 4, QTableWidgetItem(str(row[6])) ) # col.4 tiene precio_unit
                tableWidget.setItem(n_row, 5, QTableWidgetItem(str(row[7]) if row[7] != None else "") ) # col.5 tiene precio_comerc
                n_row += 1
        
        case "table_sales_data":
            for row in query:
                tableWidget.setItem(n_row, 0, QTableWidgetItem(str(row[1]) if row[1] != None else "") ) # columna 0 tiene detalles_venta
                quantity = row[3]
                if quantity.is_integer():
                    try:
                        quantity = int(quantity)
                    except ValueError:
                        pass
                measurement_unit = str(row[4]) if row[4] != None else ""
                tableWidget.setItem(n_row, 1, QTableWidgetItem(str(f"{quantity} {measurement_unit}")) ) # col.1 tiene cantidad y unidad_medida
                tableWidget.setItem(n_row, 2, QTableWidgetItem(str(row[2])) ) # col.2 tiene nombre
                tableWidget.setItem(n_row, 3, QTableWidgetItem(str(row[5])) ) # col.3 tiene costo_total
                tableWidget.setItem(n_row, 4, QTableWidgetItem(str(row[6])) ) # col.4 tiene abonado
                tableWidget.setItem(n_row, 5, QTableWidgetItem(str(row[7]) if str(row[7]) != None else "") ) # col.5 tiene fecha_hora
                n_row += 1

        case "table_debts":
            # for row in query:
            #     tableWidget.setItem(n_row, 0, QTableWidgetItem())
            # TODO: seguir poniendo funcionalidad acá (antes necesito ir a MainWindow y declarar las consultas sql)
            pass

    # al final, redimensiona las filas acorde al contenido...
    tableWidget.resizeRowsToContents()
    if id_list:
        return tuple(id_list)
    else:
        return None


def getSelectedTableRows(tableWidget:QTableWidget) -> tuple:
    '''Obtiene todas las filas seleccionadas del QTableWidget. Retorna una tupla con las filas.'''
    selected_indexes:list = []
    for index in tableWidget.selectedIndexes():
        if index.row() not in selected_indexes:
            selected_indexes.append(index.row())
    return tuple(selected_indexes)


# DELETE QUERY
def makeDeleteQuery(tableWidget:QTableWidget, rows_to_delete:tuple, ids:tuple, items_to_delete:tuple = None) -> None:
    '''Declara las consultas sql y los parámetros para hacer la consulta DELETE a la base de datos con las filas 
    seleccionadas. El parámetro 'items_to_delete' no es necesario, funciona como una "medida de seguridad", es otro 
    valor a tener en cuenta -además del ID del registro- para borrar un registro. Retorna 'None'.'''
    pos:int = 0
    connection = createConnection("database/inventario.db")
    if not connection:
        return None
    cursor = connection.cursor()
    # NOTE: sql no admite múltiples DELETE, así que se deben hacer 1 por 1
    match tableWidget.objectName():
        case "displayTable":
            while pos < len(rows_to_delete):
                cursor.execute("DELETE FROM Productos WHERE IDproducto = ? AND nombre = ?", (ids[rows_to_delete[pos]], items_to_delete[pos], ) )
                pos += 1
        
        case "table_sales_data":
            while pos < len(rows_to_delete):
                cursor.execute("DELETE FROM Detalle_Ventas WHERE ID_detalle_venta = ?;", (ids[rows_to_delete[pos]], ) )
                # obtengo el IDventa desde Detalle_Ventas
                IDventa = makeReadQuery("SELECT IDventa FROM Detalle_Ventas WHERE ID_detalle_venta = ?", (ids[rows_to_delete[pos]], ))[0][0]
                IDdeuda = makeReadQuery("SELECT IDdeuda FROM Detalle_Ventas WHERE ID_detalle_venta = ?", (ids[rows_to_delete[pos]], ))[0][0]
                # hago los DELETE a Ventas y Deudas
                cursor.execute("DELETE FROM Ventas WHERE IDventa = ? AND fecha_hora = ?;", (IDventa, items_to_delete[pos]) )
                cursor.execute("DELETE FROM Deudas WHERE IDdeuda = ? AND fecha_hora = ?;", (IDdeuda, items_to_delete[pos]) )
                pos += 1
            
    connection.commit()
    connection.close()
    return None


def removeTableCellsWidgets(tableWidget:QTableWidget) -> None:
    '''Recorre la tabla y borra todos los widgets creados en las celdas. Retorna 'None'.'''
    # si cell_widget es un QComboBox o un QLineEdit lo elimina...
    for row in range(tableWidget.rowCount()):
        for col in range(tableWidget.columnCount()):
            cell_widget = tableWidget.cellWidget(row, col)
            if isinstance(cell_widget, (QComboBox, QLineEdit, QDateTimeEdit)):
                tableWidget.removeCellWidget(row, col)
    return None


def createTableColumnComboBox(tableWidget:QTableWidget, curr_index:QModelIndex, curr_text:str) -> QComboBox:
    '''Crea el combobox que se encontrará dentro de la celda de la columna especificada por 'curr_index' en la tabla 
    'tableWidget'.\n
    'curr_text' representa al elemento que está seleccionado inicialmente en la combobox.
    \nRetorna un 'QComboBox'.'''
    combobox = QComboBox(tableWidget)
    combobox.setEditable(False)
    combobox.setFrame(False)

    match tableWidget.objectName():
        case "displayTable":
            combobox.addItems(getProductsCategories())
            combobox.setPlaceholderText("Elegir categoría")
        
        case "table_sales_data":
            combobox.addItems(getProductNames())
            combobox.setPlaceholderText("Elegir producto")
        
    # coloca como índice actual el que tenga el string 'curr_text', sino hay el índice actual es -1
    combobox.setCurrentIndex(combobox.findText(curr_text))
    tableWidget.setCellWidget(curr_index.row(), curr_index.column(), combobox)
    return combobox


def getUpdateSqlAndParameters(tableWidget:QTableWidget, lineEdit:QLineEdit, curr_index:QModelIndex, ids:tuple) -> tuple[str, tuple[str]]:
    '''Recibe el 'QTableWidget', el item que fue modificado, el 'QLineEdit' y los IDs de los elementos. Retorna una 
    tupla con la consulta Sql y una tupla con los parámetros que recibe la consulta.'''
    sql:str
    params:tuple
    re_stock:Match | None
    re_unit:Match | None
    
    match tableWidget.objectName():
        case "displayTable":
            params = (lineEdit.text(), str(ids[curr_index.row()]))
            match curr_index.column():
                case 1: # columna de nombre
                    sql = "UPDATE Productos SET nombre = ? WHERE IDproducto = ?;"
                case 2: # columna de descripción
                    sql = "UPDATE Productos SET descripcion = ? WHERE IDproducto = ?;"
                case 3: # columna de stock
                    re_stock = match("[0-9]+(\.)?[0-9]{0,2}", lineEdit.text())
                    re_stock = re_stock.group() if re_stock is not None else None
                    re_unit = search("[a-zA-Z]*$", lineEdit.text(), IGNORECASE)
                    re_unit = re_unit.group() if re_unit is not None else None
                    if re_stock:
                        params = (re_stock, re_unit, str(ids[curr_index.row()]))
                        sql = "UPDATE Productos SET stock = ?, unidad_medida = ? WHERE IDproducto = ?;"
                case 4: # precio unitario
                    sql = "UPDATE Productos SET precio_unit = ? WHERE IDproducto = ?;"
                case 5: # precio comercial
                    sql = "UPDATE Productos SET precio_comerc = ? WHERE IDproducto = ?;"
        
        case "table_sales_data":
            params = (lineEdit.text(), str(ids[curr_index.row()]))
            match curr_index.column():
                case 0: # detalle de venta
                    sql = "UPDATE Ventas SET detalles_venta = ? WHERE IDventa = (SELECT IDventa FROM Detalle_Ventas WHERE ID_detalle_venta = ?);"
                case 1: # cantidad
                    sql = "UPDATE Detalle_Ventas SET cantidad = ? WHERE ID_detalle_venta = ?;"
                case 3: # costo total
                    sql = "UPDATE Detalle_Ventas SET costo_total = ? WHERE ID_detalle_venta = ?;"
                case 4: # abonado
                    sql = "UPDATE Detalle_Ventas SET abonado = ? WHERE ID_detalle_venta = ?;"
            
    return sql, params


def validateColumnUpdatedValue(tableWidget:QTableWidget, curr_index:QModelIndex, lineEdit:QLineEdit, prev_text:str, labelFeedback:QLabel) -> None:
    '''Valida el valor ingresado para el 'QLineEdit' en la celda ubicada en la columna de la tabla actual; \
    modifica el texto de 'labelFeedback' dependiendo del error si hubo alguno.\n
    'prev_text' es la cadena de texto que había antes en la celda.\n
    \nRetorna 'None'.'''
    valid:bool = True
    text_stock:str # guarda el texto completo del stock.
    aux_stock:str # variable auxiliar. Contiene la cantidad de la celda en "stock" de 'displayTable'.

    match tableWidget.objectName():
        case "displayTable":
            # verifica si el campo está vacío...
            if lineEdit.text().strip() == "" and (curr_index.column() != 2 and curr_index.column() != 5): # col.2 (descripción) y 5 (precio comer.) son opcionales...
                valid = False
                # pone como contenido en la celda lo que estaba antes...
                tableWidget.item(curr_index.row(), curr_index.column()).setText(prev_text)
                labelFeedback.show()
                labelFeedback.setStyleSheet("font-family: 'Verdana'; font-size: 16px; letter-spacing: 0px; word-spacing: 0px;color: #f00; border: 1px solid #f00; background-color: rgb(255, 185, 185);")
                # y dependiendo de la columa seleccionada muestra un mensaje diferente...
                match curr_index.column():
                    case 1: # columna de nombre del producto
                        labelFeedback.setText("El campo del nombre del producto no puede estar vacío")
                    case 3: # columna de stock
                        labelFeedback.setText("El campo de stock no puede estar vacío")
                    case 4: # columna de precio unitario
                        labelFeedback.setText("El campo de precio unitario no puede estar vacío")

            # si es 'float' lo formatea...
            if curr_index.column() == 3: # stock
                text_stock = lineEdit.text()
                aux_stock = lineEdit.text().split(" ")[0]
                aux_stock = aux_stock.replace(",",".")
                if aux_stock.endswith("."):
                    aux_stock = aux_stock.strip(".")
                text_stock = sub("[0-9]{1,8}(\.|,)?[0-9]{0,2}", aux_stock, text_stock, count=1)
                lineEdit.setText(text_stock)

            elif (curr_index.column() == 4 or curr_index.column() == 5): # precio unitario/precio comercial
                lineEdit.setText(lineEdit.text().replace(",", "."))
                # y si termina con "," ó "."...
                if lineEdit.text().endswith("."):
                    lineEdit.setText(lineEdit.text().rstrip("."))

            if valid:
                tableWidget.item(curr_index.row(), curr_index.column()).setText(lineEdit.text())
                labelFeedback.hide()
        
        case "table_sales_data":
            # si es 'float' lo formatea...
            if (curr_index.column() == 3 or curr_index.column() == 4):
                lineEdit.setText(lineEdit.text().replace(",", "."))
                # y si termina con "," ó "."...
                if lineEdit.text().replace(",", ".").endswith("."):
                    lineEdit.setText(lineEdit.text().rstrip(",."))
            
            # si el campo está vacío...
            if curr_index.column() != 0 and lineEdit.text().strip() == "": # col.0 (detalle de venta) es opcional...
                valid = False

                tableWidget.item(curr_index.row(), curr_index.column()).setText(prev_text)
                labelFeedback.show()
                labelFeedback.setStyleSheet("font-family: 'Verdana'; font-size: 16px; letter-spacing: 0px; word-spacing: 0px; color: #f00; border: 1px solid #f00; background-color: rgb(255, 185, 185);")
                # diferente mensaje de error dependiendo de la columna...
                match curr_index.column():
                    case 1: # cantidad
                        labelFeedback.setText("El campo de cantidad no puede estar vacío")
                    case 2: # producto
                        labelFeedback.setText("El campo de producto no puede estar vacío")
                    case 3: # costo total
                        labelFeedback.setText("El campo de costo total no puede estar vacío")
                    case 4: # abonado
                        labelFeedback.setText("El campo del total abonado no puede estar vacío")
                    case 5: # fecha y hora
                        labelFeedback.setText("El campo de fecha y hora no puede estar vacío")

            if valid:
                tableWidget.item(curr_index.row(), curr_index.column()).setText(lineEdit.text())
                labelFeedback.hide()


        case "":
            pass
    
    return None


# UPDATE QUERY
def makeUpdateQuery(sql:str, params:tuple, inv_prices:bool=None) -> None:
    '''Hace la consulta UPDATE a la base de datos.\n
    'inv_prices' determina si hacer un UPDATE normal ó si es para actualizar los precios que fueron modificados de \n
    la tabla 'displayTable' usando porcentajes, en cuyo caso se usa la instrucción 'executemany()'.
    \nRetorna 'None'.'''
    conn = createConnection("database/inventario.db")
    if not conn:
        return None
    cursor = conn.cursor()
    if not inv_prices:
        cursor.execute(sql, params)
    else:
        cursor.executemany(sql, params)
    conn.commit()
    conn.close()
    return None


def overwriteTableCellOldValue(tableWidget:QTableWidget, curr_index:QModelIndex, params:tuple = None, cb_curr_text:str = None) -> None:
    '''Reemplaza el valor anterior de la celda en la posición 'curr_index' en 'tableWidget' con el nuevo valor.\n
    'params' es por si la celda tiene un QLineEdit: la 1ra posición es a la que hay que acceder para obtener el 
    contenido, y la 2da posición es sólo por si el contenido está compuesto por 2 tipos de valores (ej.: el stock en 
    'displayTable').\n
    'cb_curr_text' es por si la celda tiene un QComboBox: representa al texto del combobox.
    \nRetorna 'None'.'''
    # coloca el valor nuevo en la celda
    match tableWidget.objectName():
        case "displayTable":
            if curr_index.column() == 0: # categoría
                tableWidget.item(curr_index.row(), curr_index.column()).setText(cb_curr_text)
            elif curr_index.column() == (1 or 2 or 4 or 5): # nombre/descripción/precio unitario/precio comercial
                tableWidget.item(curr_index.row(), curr_index.column()).setText(str(params[0]).strip())
            elif curr_index.column() == 3: # stock
                tableWidget.item(curr_index.row(), curr_index.column()).setText(f"{params[0]} {str(params[1]).strip()}")
        
        case "table_sales_data":
            if curr_index.column() == 1: # cantidad (int|float + str)
                tableWidget.item(curr_index.row(), curr_index.column()).setText(f"{params[0]} {params[1]}")
            elif curr_index.column() == 2: # producto
                tableWidget.item(curr_index.row(), curr_index.column()).setText(f"{cb_curr_text}")
            else: # detalle de venta/costo total/abonado/fecha y hora
                tableWidget.item(curr_index.row(), curr_index.column()).setText(f"{str(params[0]).strip()}")

        case "":
            pass
    return None


def setSearchBarValidator(searchBar:QLineEdit) -> None:
    '''Coloca un 'Validator' en el 'searchBar' de entrada. Retorna 'None'.'''
    re = QRegularExpression("[^;,.?¿\'\'\"\"\t\r]*")
    validator = QRegularExpressionValidator(re, searchBar)
    searchBar.setValidator(validator)
    return None


def createTableColumnLineEdit(tableWidget:QTableWidget, curr_index:QModelIndex) -> QLineEdit:
    '''crea un 'QLineEdit' para ser colocado en la celda seleccionada, y dependiendo de la columna donde esté la celda 
    le aplica un 'Validator' al lineedit; además, si la celda seleccionada es de un nombre de un producto se le aplica un 
    'QCompleter' al LineEdit. Retorna un 'QLineEdit'.'''
    float_re:QRegularExpression = QRegularExpression("[0-9]{0,7}(\.|,)?[0-9]{0,2}")
    completer:QCompleter
    lineedit:QLineEdit = QLineEdit(tableWidget)

    lineedit.setText(tableWidget.item(curr_index.row(), curr_index.column()).text())
    match tableWidget.objectName():
        case "displayTable":
            match curr_index.column():
                case 1: # nombre
                    completer = createCompleter(lineedit, 3)
                    lineedit.setCompleter(completer)
                case 3: # stock
                    lineedit.setValidator(QRegularExpressionValidator("[0-9]{0,8}(\.|,)?[0-9]{0,2} ?[a-zA-Z]{0,20}", lineedit))
                case 4: # precio unitario
                    lineedit.setValidator(QRegularExpressionValidator(float_re, lineedit))
                case 5: # precio comercial
                    lineedit.setValidator(QRegularExpressionValidator(float_re, lineedit))
        
        case "table_sales_data":
            match curr_index.column():
                case 1: # cantidad
                    lineedit.setValidator(QRegularExpressionValidator("[0-9]{0,8}(\.|,)?[0-9]{0,2}", lineedit))
                    lineedit.setText(tableWidget.item(curr_index.row(), curr_index.column()).text().split(" ")[0].strip())
                case 3: # costo total
                    lineedit.setValidator(QRegularExpressionValidator(float_re, lineedit))
                case 4: # abonado
                    lineedit.setValidator(QRegularExpressionValidator(float_re, lineedit))

    tableWidget.setCellWidget(curr_index.row(), curr_index.column(), lineedit)
    return lineedit


# INSERT QUERY
def makeInsertQuery(sql:str, params:tuple = None) -> None:
    '''Hace la consulta INSERT a la base de datos. Retorna 'None'.'''
    conn = createConnection("database/inventario.db")
    if not conn:
        return None
    cursor = conn.cursor()
    if sql and params:
        cursor.execute(sql, params)
    else:
        cursor.execute(sql)
    conn.commit()
    conn.close()
    return None


def getDebtorNamesOrSurnames(type:int = 1 | 2) -> list[str]:
    '''Hace una consulta SELECT a la base de datos y obtiene los nombres ó apellidos de los deudores. Si 'type' es 1 
    trae los nombres, si es 2 trae los apellidos. Retorna una lista de strings.'''
    column:str = "nombre" if type == 1 else "apellido"
    sql = f"SELECT {column} FROM Deudores;"
    query = makeReadQuery(sql)
    return query


def createCompleter(widget:QLineEdit, type:int = 1 | 2 | 3) -> None:
    '''Recibe un 'QLineEdit'; crea un 'QCompleter', establece sus atributos y lo coloca dentro del widget. 
    \nSi 'type' es 1 carga el 'QCompleter' con nombres de deudores, si es 2 lo carga con los apellidos, si \
    es 3 lo carga con nombres de productos.
    \nRetorna 'None'.'''
    completer:QCompleter
    if type == 1 or type == 2: # nombres o apellidos de deudores
        names_or_surnames = [q[0] for q in getDebtorNamesOrSurnames(type)]
        completer = QCompleter(names_or_surnames, parent=widget)
    elif type == 3: # nombres de productos
        completer = QCompleter(getProductNames(), parent=widget)
    completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
    completer.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
    completer.setMaxVisibleItems(10)

    widget.setCompleter(completer)
    return None


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


