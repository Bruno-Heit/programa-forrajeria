'''
    Este archivo contiene los modelos de datos necesarios para usar 
    en las vistas.
'''
from typing import (Any, Sequence)
from numpy import (ndarray, delete, s_, vstack, array)

from PySide6.QtCore import (QAbstractTableModel, Qt, QModelIndex, QPersistentModelIndex, 
                            QObject, Signal)
from PySide6.QtGui import (QBrush, QColor)

from utils.enumclasses import (TableBgColors, TableFontColor)
from utils.dboperations import (DatabaseRepository)


#¡ == MODELO DE PRODUCTOS =========================================================================


class InventoryTableModel(QAbstractTableModel):
    '''
    Clase MODELO que contiene los datos de los productos para la VISTA 'tv_inventory_data'.
    Esta clase no maneja operaciones a bases de datos.
    Los datos son guardados en la variable 'self._data'.
    
    datos en self._data:
        (posición ┇ dato de base de datos)
        0 ┇ IDproducto
        1 ┇ c.nombre_categoria
        2 ┇ p.nombre
        3 ┇ p.descripcion
        4 ┇ p.stock
        5 ┇ p.unidad_medida
        6 ┇ p.precio_unit
        7 ┇ p.precio_comerc
    '''
    # señal para actualizar datos en MainWindow
    dataToUpdate:Signal = Signal(object) #? emite tuple(col:int, id:int, nuevo_valor:str).
                                         #? NOTA: si la columna es la de stock (3) el nuevo_valor
                                         #? será una lista[stock:float, unidad_medida:str]
    
    def __init__(self, data:ndarray=None, headers:Sequence[str]=None, 
                 parent:QObject=None) -> None:
        super(InventoryTableModel, self).__init__()
        self._data = data
        self._headers = headers
        self._parent = parent
        self._db_repo = DatabaseRepository()
        
    
    #¡ dimensiones
    def rowCount(self, parent:QModelIndex | QPersistentModelIndex=QModelIndex()) -> int:
        if self._data is not None:
            return len(self._data)
        return 0
    
    
    def columnCount(self, parent:QModelIndex | QPersistentModelIndex=QModelIndex()) -> int:
        if self._headers is not None:
            return len(self._headers)
        return 0
    
    
    #¡ flags
    def flags(self, index: QModelIndex | QPersistentModelIndex) -> Qt.ItemFlag:
        return Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsEditable
    
    
    def modelHasData(self) -> bool:
        '''
        Devuelve un flag que determina si el modelo de datos tiene datos 
        o si está vacío.

        Retorna
        -------
        bool
            flag que determina la existencia de datos en el modelo
        '''
        try:
            if self._data.shape:
                return True
        
        except NameError:
            return False
        
        except AttributeError:
            return False
        
        return True
    
    
    #¡ datos
    def setData(self, index: QModelIndex | QPersistentModelIndex, 
                value: Any, role: int = Qt.ItemDataRole.EditRole) -> bool:
        '''
        Realiza la actualización de datos dentro del modelo y además emite la 
        señal 'dataToUpdate' con el índice, el IDproducto y el valor nuevo, para 
        poder actualizar la base de datos a partir de esos datos.
        '''
        
        if role == Qt.ItemDataRole.EditRole:
            match index.column():
                case 0 | 1 | 2: # categoría, nombre, descripción
                    #? no modifica el modelo si el nuevo dato es igual al anterior
                    if str(value) == str(self._data[index.row()][index.column() + 1]):
                        return False
                    
                    self._data[index.row()][index.column() + 1] = value
                    
                    # actualiza los datos en MainWindow
                    self.dataToUpdate.emit(
                        (index.column(), self._data[index.row()][0], value)
                        )
                    
                    self.dataChanged.emit(index, index, [Qt.ItemDataRole.EditRole])
                    return True
                    
                case 3: # stock (con unidad de medida)
                    # [0] tiene cantidad de stock y [1] tiene unidad de medida
                    full_stock = str(value).replace(",",".").split(" ")
                    full_stock.append("") if len(full_stock) == 1 else None
                    
                    #? no modifica el modelo si el nuevo stock es igual al anterior
                    if (self._data[index.row()][4] == full_stock[0] and 
                        self._data[index.row()][5] == full_stock[1]):
                        return False
                    
                    self._data[index.row()][4] = full_stock[0] # stock
                    self._data[index.row()][5] = full_stock[1] # unidad de medida
                    
                    self.dataToUpdate.emit(
                        (index.column(), self._data[index.row()][0], full_stock)
                        )
                    
                    self.dataChanged.emit(index, index, [Qt.ItemDataRole.EditRole])
                    return True
                
                case 4: # precio unitario
                    value = str(value).replace(",",".")
                    
                    self._data[index.row()][6] = value
                    
                    self.dataToUpdate.emit(
                        (index.column(), self._data[index.row()][0], self._data[index.row()][6])
                        )
                    
                    self.dataChanged.emit(index, index, [Qt.ItemDataRole.EditRole])
                    return True
                    
                case 5: # precio comercial
                    value = str(value).replace(",",".")
                    
                    self._data[index.row()][7] = str(value).replace(",",".")
                    
                    self.dataToUpdate.emit(
                        (index.column(), self._data[index.row()][0], self._data[index.row()][7])
                        )
                    
                    self.dataChanged.emit(index, index, [Qt.ItemDataRole.EditRole])
                    return True
        return False
    
    
    def data(self, index:QModelIndex | QPersistentModelIndex, role:Qt.ItemDataRole=Qt.ItemDataRole.DisplayRole) -> Any:
        if not index.isValid():
            return None
        
        #* columnas: 0 c.nombre_categoria, 1 p.nombre, 2 p.descripcion, 3 p.stock, 
        #* 4 p.unidad_medida, 5 p.precio_unit, 6 p.precio_comerc
        
        row:int = index.row()
        col:int = index.column()
        
        match role:
            case Qt.ItemDataRole.DisplayRole:
                match col:
                    case 0: # categoría
                        return str(self._data[row][1])
                    case 1: # nombre del producto
                        return str(self._data[row][2])
                    case 2: # descripción
                        return str(self._data[row][3])
                    case 3: # stock
                        return str(f"{self._data[row][4]} {self._data[row][5]}").replace(".",",")
                    case 4: # precio normal
                        return str(self._data[row][6]).replace(".",",")
                    case 5: # precio comercial
                        if self._data[row][7]:
                            return str(self._data[row][7]).replace(".",",")
                        else:
                            return ""
        
            case Qt.ItemDataRole.BackgroundRole:
                match col:
                    case 3: # stock
                        try:
                            if float(self._data[row][4]) <= 5.0:
                                return TableBgColors.LOW_STOCK_ROW.value
                        except ValueError:
                            pass
                    
                    case 4: # precio normal
                        return TableBgColors.UNIT_PRICE_ROW.value
                    
                    case 5: # precio comerc.
                        return TableBgColors.COMERC_PRICE_ROW.value
        
            case Qt.ItemDataRole.ForegroundRole:
                if col == 3: # stock
                    try:
                        if float(self._data[row][4]) <= 5.0:
                            return QBrush(TableFontColor.CONTRAST_RED.value)
                        
                    except ValueError:
                        pass
        
            case Qt.ItemDataRole.TextAlignmentRole:
                match col:
                    case 3 | 4 | 5: # stock, precio normal, precio comerc.
                        return Qt.AlignmentFlag.AlignCenter
                    
                    case _:
                        return Qt.AlignmentFlag.AlignLeft
        return None
    
    
    def headerData(self, section:int, orientation:Qt.Orientation, 
                   role:Qt.ItemDataRole=Qt.ItemDataRole.DisplayRole) -> str|None:
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return str(self._headers[section])
        return None
    

    #¡ actualización del modelo    
    def setModelData(self, data:Sequence[Sequence[Any]], headers:Sequence[str]) -> None:
        '''
        Guarda los datos recibidos en la variable 'self._data' y coloca los headers.
        Juntos, conforman el set de datos del MODELO.

        Parámetros
        ----------
        data : Sequence[Sequence[Any]]
            Datos para almacenar en el modelo
        headers : Sequence[str]
            Headers del modelo
        
        Retorna
        -------
        None
        '''
        self.beginResetModel()
        self._data = data
        self._headers = headers
        self.endResetModel()
        return None


    def removeSelectedModelRows(self, selected_rows:Sequence) -> None:
        '''
        Actualiza el MODELO de datos eliminando los datos de las filas seleccionadas 
        en bloques de filas, ya que es más eficiente que hacerlo de a una.

        Parámetros
        ----------
        selected_rows : Sequence
            secuencia con las filas seleccionadas
        
        Retorna
        -------
        None
        '''
        blocks:list[tuple[int, int]] = []
        start_block:int = selected_rows[0] # puntero al primer elemento del bloque
        end_block:int = start_block # puntero al último elemento del bloque
        
        # ordeno las filas para trabajar con bloques de filas continuas
        selected_rows = sorted(selected_rows)
        
        # agrupo filas continuas
        for row in selected_rows[1:]:
            # verifica si el elemento actual es 1 mayor al anterior, básicamente
            if row == end_block + 1:
                end_block = row
        
            # sino, es porque las filas no son continuas, así que guardamos el bloque 
            # anterior y empezamos con otro nuevo
            else:
                blocks.append( (start_block, end_block) )
                start_block = row
                end_block = row
        
        # guardo el último bloque
        blocks.append( (start_block, end_block) )
        
        # elimina los datos en orden inverso para evitar problemas de índices
        for start, end in reversed(blocks):
            self.removeRows(start, end - start + 1)
        
        return None


    def removeRows(self, row:int, count:int, parent:QModelIndex=QModelIndex()) -> bool:
        # verifica que las filas estén dentro del rango válido
        if row < 0 or (row + count) > self.rowCount():
            return False

        # elimina las filas seleccionadas del modelo        
        self.beginRemoveRows(parent, row, row + count - 1)
        # s_[inicio:final] es la forma simple que tiene numpy de hacer 'slicing'
        self._data = delete(self._data, s_[row:row + count], axis=0)
        self.endRemoveRows()
        
        return True


    def insertRows(self, row:int, count:int, data_to_insert:dict[str, Any], 
                   parent:QModelIndex = QModelIndex()) -> bool:
        '''
        Actualiza el MODELO de datos agregando los datos introducidos en el QDialog 
        de MainWindow a una fila nueva al final de la tabla.

        Parámetros
        ----------
        data_to_insert: dict[Any]
            datos con los que actualizar el MODELO
        
        Retorna
        -------
        None
        '''
        if row < 0 or row > self.rowCount():
            return False
        
        self.beginInsertRows(parent, row, row + count - 1)
        # actualiza el atributo '_data'
        dict_to_ndarray:ndarray = array( # convierte el dict a un array de Numpy
            object=[data_to_insert["product_ID"], 
                    data_to_insert["product_category"],
                    data_to_insert["product_name"],
                    data_to_insert["product_description"],
                    data_to_insert["product_stock"],
                    data_to_insert["product_measurement_unit"],
                    data_to_insert["product_unit_price"],
                    data_to_insert["product_comercial_price"]]
            )
        # 'numpy.vstack' concatena ambos arrays de forma vertical, es decir, por filas
        self._data = vstack((self._data, dict_to_ndarray))
        self.endInsertRows()
                
        return True


#¡ == MODELO DE VENTAS ============================================================================


class SalesTableModel(QAbstractTableModel):
    '''
    Clase MODELO que contiene los datos de los productos para la VISTA 'tv_sales_data'.
    Esta clase no maneja operaciones a bases de datos.
    Los datos son guardados en la variable 'self._data'.
    
    ### datos en self._data:
        (posición ┇ dato de base de datos)
        0 ┇ dv.ID_detalle_venta
        1 ┇ v.detalles_venta
        2 ┇ dv.cantidad
        3 ┇ p.unidad_medida
        4 ┇ p.nombre
        5 ┇ dv.costo_total
        6 ┇ dv.abonado
        7 ┇ v.fecha_hora
    
    ### columnas:
        0 detalle de venta
        1: cantidad (+ unidad de medida)
        2: producto
        3: costo total
        4: abonado
        5: fecha y hora
    '''
    # señal para actualizar datos en MainWindow
    dataToUpdate:Signal = Signal(object) # emite dict[columna, IDdetalle_venta, nuevo valor], 
                                         # excepto si se elige otro producto, entonces emite 
                                         # dict[columna, IDdetalle_venta, nuevo valor, índice 
                                         # de columna "cantidad"]

    def __init__(self, data:ndarray=None, headers:Sequence[str]=None, 
                 parent:QObject = ...) -> None:
        super(SalesTableModel, self).__init__()
        
        self._data = data
        self._headers = headers
        self._parent = parent
        self._db_repo = DatabaseRepository()
    
    
    #¡ dimensiones
    def rowCount(self, parent:QObject = ...) -> int:
        if self._data is not None:
            return self._data.shape[0]
    
    
    def columnCount(self, parent:QObject = ...):
        if self._headers is not None:
            return len(self._headers)
    
    
    #¡ flags
    def flags(self, index:QModelIndex | QPersistentModelIndex) -> Qt.ItemFlag:
        return Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsEditable
    
    
    def modelHasData(self) -> bool:
        '''
        Devuelve un flag que determina si el modelo de datos tiene datos 
        o si está vacío.

        Retorna
        -------
        bool
            flag que determina la existencia de datos en el modelo
        '''
        try:
            if self._data.shape:
                return True
        
        except NameError:
            return False
        
        except AttributeError:
            return False
        
        return True
    
    
    #¡ datos    
    def setData(self, index:QModelIndex | QPersistentModelIndex, value:Any, 
                role:Qt.ItemDataRole = Qt.ItemDataRole.EditRole) -> bool:
        '''
        Realiza la actualización de datos dentro del modelo y además emite la 
        señal 'dataToUpdate' con el índice, el ID_detalle_venta y el valor nuevo 
        (en caso de modificarse el producto, emite también el índice de la columna 
        "cantidad"), para poder actualizar la base de datos a partir de esos datos.
        '''
        if role == Qt.ItemDataRole.EditRole:
            match index.column():
                case 0: # detalle de venta
                    #? no modifica el modelo si el nuevo dato es igual al anterior
                    if str(value) == str(self._data[index.row()][index.column() + 1]):
                        return False
                    
                    self._data[index.row()][index.column() + 1] = value
                    
                    # actualiza detalles de venta en MainWindow
                    self.dataToUpdate.emit(
                        {'column': index.column(),
                         'IDsales_detail': self._data[index.row()][0],
                         'new_value': value}
                        )
                    
                    self.dataChanged.emit(index, index, [Qt.ItemDataRole.EditRole])
                    return True
        
                case 1: # cantidad
                    value = str(value).replace(",", ".").strip()
                    if value == str(self._data[index.row()][index.column() + 1]):
                        return False
                    
                    self._data[index.row()][index.column() + 1] = float(value)
                    
                    # actualiza cantidad en MainWindow
                    self.dataToUpdate.emit(
                        {'column': index.column(),
                         'IDsales_detail': self._data[index.row()][0],
                         'new_value': value}
                    )
                    
                    self.dataChanged.emit(index, index, [Qt.ItemDataRole.EditRole])
                    return True
                    
                case 2: # producto
                    if value == str(self._data[index.row()][index.column() + 2]):
                        return False
                    
                    self._data[index.row()][index.column() + 2] = value

                    # actualiza producto en MainWindow
                    self.dataToUpdate.emit(
                        {'row': index.row(),
                         'column': index.column(),
                         'IDsales_detail': self._data[index.row()][0],
                         'new_value': value,
                         'quantity_index': self.index(index.row(), 1)
                         }
                    )
                    
                    self.dataChanged.emit(index, index, [Qt.ItemDataRole.EditRole])
                    return True
                
                case 3 | 4: # costo total | abonado
                    value = str(value).replace(",", ".")
                    if str(value) == str(self._data[index.row()][index.column() + 2]):
                        return False
                    
                    self._data[index.row()][index.column() + 2] = value
                    
                    # actualiza costo total | abonado en MainWindow
                    self.dataToUpdate.emit(
                        {'column': index.column(),
                         'IDsales_detail': self._data[index.row()][0],
                         'new_value': value}
                        )
                    
                    self.dataChanged.emit(index, index, [Qt.ItemDataRole.EditRole])
                    return True
                
                case 5: # fecha y hora
                    if str(value) == str(self._data[index.row()][index.column() + 2]):
                        return False
                    
                    self._data[index.row()][index.column() + 2] = value
                    
                    # actualiza fecha y hora en MainWindow
                    self.dataToUpdate.emit(
                        {'column': index.column(),
                         'IDsales_detail': self._data[index.row()][0],
                         'new_value': value}
                        )
                    
                    self.dataChanged.emit(index, index, [Qt.ItemDataRole.EditRole])
                    return True
        return False
    
    
    def data(self, index:QModelIndex | QPersistentModelIndex, role:Qt.ItemDataRole = Qt.ItemDataRole.DisplayRole) -> Any:
        if not index.isValid():
            return None
        
        row:int = index.row()
        col:int = index.column()
        
        match role:
            case Qt.ItemDataRole.DisplayRole:
                match col:
                    case 0: # detalle de venta
                        return self._data[row, 1]
                    
                    case 1: # cantidad (+ unidad de medida)
                        return f"{self._data[row, 2]} {self._data[row, 3]}".replace(".", ",")
                    
                    case 2: # producto
                        return self._data[row, 4]
                    
                    case 3: # costo total
                        return str(self._data[row, 5]).replace(".", ",")
                    
                    case 4: # abonado
                        return str(self._data[row, 6]).replace(".", ",")
                    
                    case 5: # fecha y hora
                        return self._data[row, 7]
            
            case Qt.ItemDataRole.BackgroundRole:
                match col:
                    case 3 | 4: # costo total | abonado
                        # si lo abonado es menor al costo total, le da un fondo rojizo
                        if float(self._data[row, 5]) > float(self._data[row, 6]):
                            return TableBgColors.SALES_LOWER_PAID.value
                    
            case Qt.ItemDataRole.ForegroundRole:
                match col:
                    case 3 | 4: # costo total | abonado
                        # si lo abonado es menor al costo total, le da un fondo rojizo
                        if float(self._data[row, 5]) > float(self._data[row, 6]):
                            return TableFontColor.CONTRAST_RED.value
                    
            case Qt.ItemDataRole.TextAlignmentRole:
                match col:
                    case 1 | 3 | 4: # cantidad | costo total | abonado
                        return Qt.AlignmentFlag.AlignCenter
                    
                    case 5: # fecha y hora
                        return Qt.AlignmentFlag.AlignRight
                    
                    case _:
                        return Qt.AlignmentFlag.AlignLeft
                    
        return None
    
    
    def headerData(self, section:int, orientation:Qt.Orientation, 
                   role:Qt.ItemDataRole=Qt.ItemDataRole.DisplayRole) -> str|None:
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return str(self._headers[section])
        return None
    
    
    #¡ actualización del modelo
    def setModelData(self, data:Sequence[Sequence[Any]], headers:Sequence[str]) -> None:
        '''
        Guarda los datos recibidos en la variable 'self._data' y coloca los headers.
        Juntos, conforman el set de datos del MODELO.

        Parámetros
        ----------
        data : Sequence[Sequence[Any]]
            Datos para almacenar en el modelo
        headers : Sequence[str]
            Headers del modelo
        
        Retorna
        -------
        None
        '''
        self.beginResetModel()
        self._data = data
        self._headers = headers
        self.endResetModel()
        return None


    def updateMeasurementUnit(self, quantity_index:QModelIndex, new_value:str) -> None:
        '''
        Actualiza el valor de la unidad de medida en el atributo '_data'. 
        NOTA: se llama a éste método desde 'MainWindow' cuando se cambia el 
        producto elegido.

        Parámetros
        ----------
        quantity_index : QModelIndex
            índice del registro modificado
        new_value : str
            la nueva unidad de medida correspondiente al producto
        
        Retorna
        -------
        None
        '''
        self._data[quantity_index.row(), quantity_index.column() + 2] = new_value
        
        self.dataChanged.emit(quantity_index, quantity_index, [Qt.ItemDataRole.EditRole])
        return None
    

    # TODO: implementar eliminar filas
    def insertRows(self, row, count, data_to_insert:dict[str, Any], 
                   parent:QModelIndex = QModelIndex()):
        if row < 0 or row > self.rowCount():
            return False
        
        self.beginInsertRows(parent, row, row + count - 1)
        # actualiza el atributo '_data'
        dict_to_ndarray:ndarray = array( # convierte el dict a un array de Numpy
            object=[data_to_insert["IDsale_detail"],
                    data_to_insert["sale_detail"],
                    data_to_insert["product_quantity"],
                    data_to_insert["product_measurement_unit"],
                    data_to_insert["product_name"],
                    data_to_insert["total_cost"],
                    data_to_insert["total_paid"],
                    data_to_insert["datetime"]]
            )
        # 'numpy.vstack' concatena ambos arrays de forma vertical, es decir, por filas
        self._data = vstack((self._data, dict_to_ndarray))
        self.endInsertRows()
                
        return True











