'''
    Este archivo contiene los modelos de datos necesarios para usar 
    en las vistas.
'''
from typing import (Any, Sequence)

from PySide6.QtCore import (QAbstractTableModel, Qt, QModelIndex, QObject)


class InventoryTableModel(QAbstractTableModel):
    '''
    Clase MODELO que contiene los datos de los productos para la VISTA 'tv_inventory_data'.
    '''
    def __init__(self, data:Sequence[Sequence[Any]]=None, headers:Sequence[str]=None, parent:QObject=None) -> None:
        super(InventoryTableModel, self).__init__()
        self._data = data
        self._headers = headers
        self._parent = parent
        
    
    def rowCount(self) -> int:
        return len(self._data)
    
    
    def columnCount(self) -> int:
        return len(self._headers)
    
    
    def data(self, index:QModelIndex, role:Qt.ItemDataRole=Qt.ItemDataRole.DisplayRole) -> Any:
        if not index.isValid():
            return None
        
        # todo: seguir reimplementando el método data() para retornar diferentes roles y datos
        
        row:int = index.row()
        col:int = index.column()
        
        if role == Qt.ItemDataRole.DisplayRole:
            return str(self._data[row][col])
        
        elif role == Qt.ItemDataRole.BackgroundRole:
            if col == 4:
                return Qt.GlobalColor.cyan
            elif col == 5:
                return Qt.GlobalColor.darkGreen
    
    
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
        # self._headers = headers
        self.endResetModel()
        return None
    
    
    # TODO: implementar la lógica para añadir/quitar filas a medida que se hace scroll en la vista
    # def insertRows(self, row:int, count:int, parent:QModelIndex=QModelIndex()) -> None:
    #     self.beginInsertRows(QModelIndex(), )