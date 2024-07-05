'''
    Este archivo contiene los modelos de datos necesarios para usar 
    en las vistas.
'''
from typing import (Any, Sequence)

from PySide6.QtCore import (QAbstractTableModel, Qt, QModelIndex, QPersistentModelIndex, 
                            QObject, Signal)
from PySide6.QtGui import (QBrush, QColor)

from utils.enumclasses import (TableBgColors, TableFontColor)


class InventoryTableModel(QAbstractTableModel):
    '''
    Clase MODELO que contiene los datos de los productos para la VISTA 'tv_inventory_data'.
    Esta clase no maneja operaciones a bases de datos.
    '''
    def __init__(self, data:Sequence[Sequence[Any]]=None, headers:Sequence[str]=None, 
                 parent:QObject=None) -> None:
        super(InventoryTableModel, self).__init__()
        '''
        datos en self._data:
        (pos->dato) 0-> ID | 1-> c.nombre_categoria | 2-> p.nombre |3-> p.descripcion |
                    4-> p.stock | 5-> p.unidad_medida | 6-> p.precio_unit | 
                    7-> p.precio_comerc
        '''
        self._data = data
        self._headers = headers
        self._parent = parent
        
    
    def rowCount(self, parent:QModelIndex | QPersistentModelIndex=QModelIndex()) -> int:
        if self._data is not None:
            return len(self._data)
        return 0
    
    
    def columnCount(self, parent:QModelIndex | QPersistentModelIndex=QModelIndex()) -> int:
        if self._headers is not None:
            return len(self._headers)
        return 0
    
    
    # hace el modelo editable
    def flags(self, index: QModelIndex | QPersistentModelIndex) -> Qt.ItemFlag:
        return Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsEditable
    
    
    def setData(self, index: QModelIndex | QPersistentModelIndex, 
                value: Any, role: int = Qt.ItemDataRole.EditRole) -> bool:
        #* realizar la actualización de datos en base de datos desde este método
        
        if role == Qt.ItemDataRole.EditRole:
            match index.column():
                case 0 | 1 | 2: # categoría, nombre, descripción
                    self._data[index.row()][index.column() + 1] = value
                    
                    self.dataChanged.emit(index, index, [Qt.ItemDataRole.EditRole])
                    return True
                    
                case 3: # stock (con unidad de medida)
                    # [0] tiene cantidad de stock y [1] tiene unidad de medida
                    full_stock = str(value).replace(",",".").split(" ")
                    full_stock.append("") if len(full_stock) == 1 else None
                    
                    self._data[index.row()][4] = full_stock[0] # stock
                    self._data[index.row()][5] = full_stock[1] # unidad de medida
                    
                    self.dataChanged.emit(index, index, [Qt.ItemDataRole.EditRole])
                    return True
                
                case 4: # precio unitario
                    self._data[index.row()][6] = value
                    self.dataChanged.emit(index, index, [Qt.ItemDataRole.EditRole])
                    return True
                    
                case 5: # precio comercial
                    self._data[index.row()][7] = value
                    self.dataChanged.emit(index, index, [Qt.ItemDataRole.EditRole])
                    return True
        return False
    
    
    def data(self, index:QModelIndex | QPersistentModelIndex, role:Qt.ItemDataRole=Qt.ItemDataRole.DisplayRole) -> Any:
        if not index.isValid():
            return None
        
        #* datos: 0 c.nombre_categoria, 1 p.nombre, 2 p.descripcion, 3 p.stock, 
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
                            if float(self._data[row][4]) <= 15.0:
                                return TableBgColors.LOW_STOCK_ROW
                        except ValueError:
                            pass
                    
                    case 4: # precio normal
                        return TableBgColors.UNIT_PRICE_ROW.value
                    
                    case 5: # precio comerc.
                        return TableBgColors.COMERC_PRICE_ROW.value
        
            case Qt.ItemDataRole.ForegroundRole:
                if col == 3: # stock
                    try:
                        if float(self._data[row][4]) <= 15.0:
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
    
    
    # TODO: implementar la lógica para añadir/quitar filas a medida que se hace scroll en la vista
    # def insertRows(self, row:int, count:int, parent:QModelIndex=QModelIndex()) -> None:
    #     self.beginInsertRows(QModelIndex(), )



