# SQLITE3

from typing import (Any)

from PySide6.QtWidgets import (QTableWidget, QComboBox, QHeaderView, QListWidget, QLineEdit, 
                               QCompleter, QFrame, QWidget, QDateTimeEdit, QTableView, 
                               QCheckBox, QButtonGroup)
from PySide6.QtCore import (QModelIndex, Qt, QPropertyAnimation, QEasingCurve, QDateTime, 
                            QDate, QTime)

from resources import (rc_icons)
from utils.dboperations import *
from utils.customvalidators import *
from re import (Match, sub, match, findall)


# consultas sql
def getTableViewsSqlQueries(tv_name:str, ACCESSED_BY_LIST:bool=False, SHOW_ALL:bool=False) -> tuple[str, str]:
    '''
    Dependiendo de cada caso específico, devuelve la consulta sql en formato str.
    
    PARAMS:
    - tv_name: el nombre del QTableView al que se hace referencia.
    - ACCESSED_BY_LIST: flag que será True si se seleccionó un item desde 'tables_ListWidget', sino False.
    - SHOW_ALL: flag que determina si se muestran todos los elementos del QTableView 'tv_name'.
    
    Retorna un tuple[count_sql, data_sql], siendo 'count_sql' la consulta tipo COUNT y 'data_sql' la 
    consulta para traer los registros.
    '''
    match tv_name:
        case "tv_inventory_data":
            if SHOW_ALL:
                return (
                    str("SELECT COUNT(*) FROM Productos WHERE eliminado = 0;"),
                    str('''SELECT IDproducto,nombre_categoria,nombre,p.descripcion,
                        stock,unidad_medida,precio_unit,precio_comerc 
                        FROM Productos AS p INNER JOIN Categorias AS c 
                            WHERE (p.IDcategoria=c.IDcategoria AND p.eliminado = 0);'''))
            
            elif not SHOW_ALL and ACCESSED_BY_LIST:
                # cols.: detalle venta, cantidad, producto, costo total, abonado, fecha y hora
                return (
                    str('''SELECT COUNT(*) 
                        FROM Productos 
                            WHERE IDcategoria = (SELECT IDcategoria FROM Categorias 
                                WHERE nombre_categoria = ?) AND eliminado = 0;'''),
                    str('''SELECT IDproducto,nombre_categoria,nombre,p.descripcion,
                        stock,unidad_medida,precio_unit,precio_comerc 
                        FROM Productos AS p INNER JOIN Categorias AS c 
                            ON p.IDcategoria=c.IDcategoria 
                                WHERE c.nombre_categoria=? AND eliminado = 0;''')
                    )
                    
        case "tv_sales_data":
            return (
                str('''SELECT COUNT(*) 
                    FROM Detalle_Ventas as dv 
                        LEFT JOIN Productos AS p ON dv.IDproducto = p.IDproducto 
                        LEFT JOIN Ventas AS v ON dv.IDventa = v.IDventa;'''),
                str('''SELECT dv.ID_detalle_venta, v.detalles_venta, p.nombre, dv.cantidad, 
                    p.unidad_medida, dv.costo_total, dv.abonado, v.fecha_hora 
                    FROM Detalle_Ventas as dv 
                        LEFT JOIN Productos AS p ON dv.IDproducto = p.IDproducto 
                        LEFT JOIN Ventas AS v ON dv.IDventa = v.IDventa;''')
                )

        case "tv_debts_data":
            # TODO: declarar consultas sql para también traer los datos necesarios
            if SHOW_ALL:
                count_sql = "SELECT COUNT(DISTINCT IDdeudor) FROM Deudas;"
                sql = 'SELECT Detalle_Ventas.*, Deudores.* F'


# side bars
def toggleSideBar(side_bar:QFrame, parent:QWidget|QFrame, body:QFrame, max_width:int=250) -> bool:
    '''
    Anima la apertura o cierre de los menús laterales y esconde o muestra los 
    widgets internos.
    
    Parámetros
    ----------
    side_bar: QFrame
        El sidebar al que se referencia
    parent: QWidget|QFrame
        El widget padre al que pertenece el sidebar, es necesario porque la 
        animación requiere especificar el widget padre
    body: QFrame
        El widget con los widgets hijos que deben esconderse o mostrarse
    max_width: int, opcional
        El ancho máximo al que animar la apertura del sidebar
    
    Retorna
    -------
    bool
        Determina si se abrió o si se cerró el sidebar, si es False se cerró, si es True 
        se abrió
    '''
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
    return bool(signal)


def __toggleSideBarWidgetsVisibility(body:QFrame, signal:int):
    '''
    Muestra o esconde los widgets dentro del menú lateral al terminar la animación 
    de apertura o cierre del menú lateral
    
    Parámetros
    ----------
    body: QFrame
        El cuerpo del sidebar que hay que esconder/mostrar
    signal: int
        Flag que determina si esconder/mostrar el cuerpo del sidebar
    
    Retorna
    -------
    None
    '''
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
    
    query = cursor.execute("SELECT nombre FROM Productos WHERE eliminado != 1;").fetchall()
    
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


def setTableViewPolitics(tableView:QTableView) -> None:
    '''
    Declara las políticas del QTableView.
    
    Parámetros
    ----------
    tableView : QTableView
        El QTableView que se referencia

    Retorna
    -------
    None
    '''
    tableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
    tableView.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
    return None


def getSelectedTableRows(tableView:QTableView, 
                         indexes_in_col:int=-1) -> tuple[int] | dict[int, QModelIndex]:
    '''
    Obtiene todas las filas seleccionadas del QTableView. Puede retornar una 
    tupla o un diccionario, dependiendo del parámetro 'indexes_in_col'. 
    NOTA: no devuelve valores de filas repetidas.
    
    Parámetros
    ----------
    tableView : QTableView
        El QTableView al que se referencia
    indexes_in_col: int, opcional
        Especifica una columna en particular de la cual obtener los índices, de forma 
        que se ignorarán los índices seleccionados en esa fila a excepción de los 
        índices seleccionados en la columna especificada.
        NOTA: al pasar este parámetro, se devuelve un diccionario con la fila como 
        clave y el índice como valor.
    
    Retorna
    -------
    tuple[int] | dict[int, QModelIndex]
        Tupla con las filas seleccionadas ó diccionario con las filas seleccionadas 
        como 'keys' y el índice como 'value'
        '''
    selected_indexes:list[int] | dict[int, QModelIndex]
    
    match indexes_in_col:
        case -1:
            selected_indexes:list[int] = []
            
            for index in tableView.selectedIndexes():
                if index.row() not in selected_indexes:
                    selected_indexes.append(index.row())
        
            return tuple(selected_indexes)
        
        case _:
            selected_indexes:dict[int, QModelIndex] = {}
            
            for index in tableView.selectedIndexes():
                if index.column() == indexes_in_col:
                    selected_indexes[index.row()] = index
            
            return selected_indexes


def getCurrentProductStock(product_name:str) -> tuple[float,str]:
        '''
        Hace una consulta SELECT y obtiene el stock actual del producto ingresado. 
        
        Retorna una tupla con el stock como número y la unidad de medida como 'str'.
        '''
        conn:Connection | None
        stock:float
        measurement_unit:str

        conn = createConnection("database/inventario.db")
        if not conn:
            return None
        cursor = conn.cursor()
        query = cursor.execute("SELECT stock, unidad_medida FROM Productos WHERE nombre = ?;", (product_name,)).fetchone()
        if len(query) == 2:
            stock, measurement_unit = [q for q in query]
        else:
            stock = query[0]
            measurement_unit = ""
        
        try:
            stock = float(stock)
        except:
            pass
        return stock, measurement_unit


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
        case "tv_inventory_data":
            combobox.addItems(getProductsCategories())
            combobox.setPlaceholderText("Elegir categoría")
        
        case "tv_sales_data":
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
        case "tv_inventory_data":
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
        
        
        case "tv_sales_data":
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
def createCompleter(sql:str=None, params:tuple[Any]=None, type:int=None) -> QCompleter:
    '''
    Crea un QCompleter y establece sus atributos.
    El parámetro 'type' sirve para realizar una consulta genérica a la base de datos y obtener todas 
    las coincidencias del valor de 'type', en cambio los parámetros 'sql' y 'params' sirven para obtener 
    resultados más precisos al realizar consultas concretas.
    
    Parámetros
    ----------
    sql: str, opcional
        Consulta SELECT a la base de datos, requiere 'params'
    params: tuple[Any], opcional 
        Parámetros para la consulta
    type: int, opcional 
        Flag que determina los datos con los que llenar el QCompleter
        - 1: lo carga con todos los nombres de personas con cuenta corriente
        - 2: lo carga con todos los apellidos de personas con cuenta corriente
        - 3: lo carga con todos los nombres de productos
    
    Retorna
    -------
    QCompleter
        QCompleter con sus atributos especificados
    '''
    completer:QCompleter
    query:list
    
    if sql and params:
        query = makeReadQuery(sql, params)
        results = [res[0] for res in query]
        completer = QCompleter(results)
    
    else:
        if type == 1: # nombres de personas con cta. corriente
            query = makeReadQuery("SELECT DISTINCT nombre FROM Deudores;")
            names = [name[0] for name in query]
            completer = QCompleter(names)
        
        elif type == 2: # apellidos de personas con cta. corriente
            query = makeReadQuery("SELECT DISTINCT apellido FROM Deudores;")
            surnames = [surname[0] for surname in query]
            completer = QCompleter(surnames)
        
        elif type == 3: # nombres de productos
            completer = QCompleter(getProductNames())
    
    completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
    completer.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
    completer.setMaxVisibleItems(10)

    return completer


#========================================================================================================================
def getPercentageMultipFactor(new_value:float, prev_value:float) -> float:
    '''
    Obtiene el factor de multiplicación que representa el cambio porcentual entre 
    un valor nuevo y un valor anterior. Por ejemplo: si el valor anterior es 100 y el 
    valor nuevo es 200 hubo un incremento del 100%, o lo que es lo mismo, su factor de 
    multiplicación es 2.
    Si el valor anterior es 0 y el nuevo valor es diferente de 0, en su lugar retorna 
    el nuevo valor, porque el cambio porcentual -matemáticamente hablando- en ese caso 
    es tendiente a infinito.

    Parámetros
    ----------
    new_value : float
        El valor nuevo de la expresión
    prev_value : float
        El valor anterior de la expresión

    Retorna
    -------
    float
        - Retorna 1 cuando el valor anterior es igual al nuevo valor.
        - Retorna 'new_value' cuando el valor anterior es 0.
        - Retorna el factor de multiplicación por el que multiplicar al valor anterior para obtener 
        el cambio porcentual.
    '''
    percentage_diff:float = 0 # cambio porcentual entre el valor anterior al valor nuevo
    
    try:
        # no tiene sentido calcular el cambio porcentual si ambos valores son iguales...
        if prev_value == new_value:
            return 1
        # ni tampoco cuando cambia de 0 a otro valor, porque tiende a infinito...
        elif prev_value == 0 and new_value != 0:
            return new_value
        
        percentage_diff = (float(new_value) - float(prev_value)) * 100 / float(prev_value)
        
    except ValueError:
        pass
        
    return 1 + percentage_diff / 100






