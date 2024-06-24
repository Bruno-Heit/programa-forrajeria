'''
    Este archivo contiene los modelos de datos necesarios para usar 
    en las vistas.
'''
from typing import (Any, Sequence)

from PySide6.QtCore import (QAbstractTableModel, Qt, QModelIndex, QObject)
from PySide6.QtGui import (QBrush, QColor)

from utils.enumclasses import (TableBgColors, TableFontColor)


class InventoryTableModel(QAbstractTableModel):
    '''
    Clase MODELO que contiene los datos de los productos para la VISTA 'tv_inventory_data'.
    '''
    def __init__(self, data:Sequence[Sequence[Any]]=None, headers:Sequence[str]=None, 
                 parent:QObject=None) -> None:
        super(InventoryTableModel, self).__init__()
        self._data = data
        self._headers = headers
        self._parent = parent
        
    
    def rowCount(self, parent:QModelIndex=QModelIndex()) -> int:
        if self._data is not None:
            return len(self._data)
        return 0
    
    
    def columnCount(self, parent:QModelIndex=QModelIndex()) -> int:
        if self._headers is not None:
            return len(self._headers)
        return 0
    
    
    def data(self, index:QModelIndex, role:Qt.ItemDataRole=Qt.ItemDataRole.DisplayRole) -> Any:
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
                        return str(self._data[row][0])
                    case 1: # nombre del producto
                        return str(self._data[row][1])
                    case 2: # descripción
                        return str(self._data[row][2])
                    case 3: # stock
                        return str(f"{self._data[row][3]} {self._data[row][4]}")
                    case 4: # precio normal
                        return str(self._data[row][5])
                    case 5: # precio comercial
                        if self._data[row][6]:
                            return str(self._data[row][6])
                        else:
                            return ""
        
            case Qt.ItemDataRole.BackgroundRole:
                match col:
                    case 3: # stock
                        try:
                            if float(self._data[row][3]) <= 15.0:
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
                        if float(self._data[row][3]) <= 15.0:
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






