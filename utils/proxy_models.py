
'''
En este archivo están las clases de PROXY MODELS, que son subclaseadas 
principalmente para que las señales del MODELO DE DATOS y la VISTA sean 
pasadas correctamente entre ellos sin errores.
'''

from PySide6.QtCore import (QSortFilterProxyModel, Qt, QModelIndex, Signal)

from utils.model_classes import (InventoryTableModel)
from typing import (Any, Sequence)



class InventoryProxyModel(QSortFilterProxyModel):
    '''
    PROXY MODEL editable de Inventario.
    '''
    baseModelRowsSelected:Signal = Signal(object) # emite una tupla[int] con las filas seleccionadas 
                                        # mapeadas del MODELO BASE a MainWindow para 
                                        # actualizar la base de datos.
    
    
    def __init__(self, parent=None) -> None:
        super(InventoryProxyModel, self).__init__()
    
    
    def insertRows(self, row:int, count:int, data_to_insert:dict[str, Any], 
                   parent:QModelIndex=QModelIndex()) -> bool:
        '''
        Inserta nuevas filas en el MODELO DE DATOS. Éste método sirve para 
        extender la comunicación de la VISTA al MODELO.
        '''
        # obtiene el MODELO BASE
        source_model:InventoryTableModel = self.sourceModel()
        
        # convierte el modelIndex del PROXY MODEL al modelIndex del MODELO DE DATOS
        source_parent = self.mapToSource(parent)
        
        # notifica a la VISTA que se insertarán filas
        if not source_model.insertRows(row, count, data_to_insert, source_parent):
            return False
        
        # emite señales para confirmar cambios
        self.beginInsertRows(parent, row, row + count - 1)
        self.endInsertRows()
        return True
    
    
    def removeSelectedRows(self, selected_rows:tuple[int]) -> None:
        '''
        Elimina en el MODELO DE DATOS las filas seleccionadas en la VISTA.
        
        NOTA: la base de datos no es actualizada desde acá, eso se hace en 
        MainWindow, éste método emite la señal 'baseModelRowsSelected' con los IDs de 
        los productos para poder actualizarla.

        Parámetros
        ----------
        selected_rows : tuple[int]
            tupla con las filas seleccionadas

        Retorna
        -------
        None
        '''
        # obtiene el MODELO BASE (simplemente para type-hinting)
        source_model:InventoryTableModel = self.sourceModel()
        
        # mapea las filas seleccionadas para obtener las del MODELO BASE
        selected_source_rows:tuple[int] = tuple(
            self.mapToSource(self.index(proxy_row, 0)).row() for proxy_row in selected_rows
        )
        
        # elimina las filas seleccionadas en el MODELO BASE
        if selected_source_rows:
            # emite señal a MainWindow con las filas seleccionadas en el MODELO BASE
            self.baseModelRowsSelected.emit(selected_source_rows)
            
            source_model.removeSelectedModelRows(selected_rows=selected_source_rows)
        return None
    