
'''
En este archivo están las clases de PROXY MODELS, que son subclaseadas 
principalmente para que las señales del MODELO DE DATOS y la VISTA sean 
pasadas correctamente entre ellos sin errores.
'''

from PySide6.QtCore import (QSortFilterProxyModel, Qt, QModelIndex, Signal, QDateTime)

from utils.model_classes import (InventoryTableModel, SalesTableModel, DebtsTableModel)
from utils.enumclasses import (ModelDataCols, TableViewColumns)
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
        self._filter_column:int = -1 # columna a ordenar por defecto
    
    
    # inserción de filas
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
    
    
    # eliminación de filas
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
    
    
    # ordenamiento
    def lessThan(self, source_left:QModelIndex, source_right:QModelIndex) -> bool:
        _source_model:InventoryTableModel = self.sourceModel()
        _left_value:float | str # intenta comparar primero los valores como float, 
        _right_value:float | str # sino funciona los compara como str.
        
        # antes de obtener datos del modelo, verifica qué columna se está ordenando
        match source_left.column():
            case TableViewColumns.INV_CATEGORY.value: # cantidad
                _left_value = _source_model._data[source_left.row(), ModelDataCols.INV_CATEGORY_NAME.value]
                _right_value = _source_model._data[source_right.row(), ModelDataCols.INV_CATEGORY_NAME.value]
            
            case TableViewColumns.INV_PRODUCT_NAME.value: # nombre de producto
                _left_value = _source_model._data[source_left.row(), ModelDataCols.INV_NAME.value]
                _right_value = _source_model._data[source_right.row(), ModelDataCols.INV_NAME.value]
            
            case TableViewColumns.INV_DECRIPTION.value: # descripción (¿tiene sentido ordenar por descripción?)
                _left_value = _source_model._data[source_left.row(), ModelDataCols.INV_DESCRIPTION.value]
                _right_value = _source_model._data[source_right.row(), ModelDataCols.INV_DESCRIPTION.value]
            
            case TableViewColumns.INV_STOCK.value: # stock
                _left_value = _source_model._data[source_left.row(), ModelDataCols.INV_STOCK.value]
                _right_value = _source_model._data[source_right.row(), ModelDataCols.INV_STOCK.value]
                
                # hace la comparación como float
                try:
                    return float(_left_value) < float(_right_value)
                
                # si hay algún error, compara los valores como str
                except (ValueError, IndexError):
                    pass
            
            case TableViewColumns.INV_NORMAL_PRICE.value: # precio normal
                _left_value = _source_model._data[source_left.row(), ModelDataCols.INV_NORMAL_PRICE.value]
                _right_value = _source_model._data[source_right.row(), ModelDataCols.INV_NORMAL_PRICE.value]
                
                try:
                    return float(_left_value) < float(_right_value)
                
                except (ValueError, IndexError):
                    pass
            
            case TableViewColumns.INV_COMERCIAL_PRICE.value: # precio comercial
                _left_value = _source_model._data[source_left.row(), ModelDataCols.INV_COMERCIAL_PRICE.value]
                _right_value = _source_model._data[source_right.row(), ModelDataCols.INV_COMERCIAL_PRICE.value]
                
                # antes de comparar, verifica si hay valores nulos/ceros, si hay, los considera 
                # como los valores más pequeños
                if not _left_value and _right_value: # coloca valores nulos después de los datos
                    return True
                if _left_value and not _right_value: # coloca valores con datos antes de nulos
                    return False
                if not _left_value and not _right_value: # mantiene el orden si ambos son nulos
                    return False
                
                try:
                    return float(_left_value) < float(_right_value)
                
                except (ValueError, IndexError):
                    pass
        
        return str(_left_value) < str(_right_value)


    # filtrado avanzado
    def setFilterColumn(self, column:int) -> None:
        '''
        Al alternar el ordenamiento entre columnas, éste método se encarga de 
        establecer la nueva columna que se debe ordenar en el PROXY MODEL.

        Parámetros
        ----------
        column : int
            columna a ordenar

        Retorna
        -------
        None
        '''
        self._filter_column = column
        self.invalidateFilter() # invalida el filtro existente, esto se hace para 
            # implementar una lógica personalizada de ordenamiento sobre alguna 
            # columna específica...
        return None
    
    
    def filterAcceptsRow(self, source_row:int, source_parent:QModelIndex) -> bool:
        regex = self.filterRegularExpression()
        
        # si el patrón (o sea, el texto de la search bar) está vacío no filtra nada
        if not regex.pattern():
            return True
        
        _source_model:InventoryTableModel = self.sourceModel()
        index_data:Any
        
        # si la columna de filtrado es -1 busca en todas
        if self._filter_column == -1:
            for col in range(_source_model.columnCount()):
                index_data = _source_model.index(
                    source_row,
                    col,
                    source_parent).data(Qt.ItemDataRole.DisplayRole)
                
                if index_data and regex.match(index_data).hasMatch():
                    return True
            return False
        
        # sino, busca en la columna especificada
        else:
            # obtengo el dato de índice en la columna a filtrar
            index_data = _source_model.index(
                source_row,
                self._filter_column,
                source_parent).data(Qt.ItemDataRole.DisplayRole)
        
        # devuelve True si hay coincidencia en el dato en el index actual, sino False
        return regex.match(index_data).hasMatch() if index_data else False





class SalesProxyModel(QSortFilterProxyModel):
    '''
    PROXY MODEL editable de Ventas.
    '''
    baseModelRowsSelected:Signal = Signal(object) # emite una tupla[int] con las filas seleccionadas 
                                        # mapeadas del MODELO BASE a MainWindow para 
                                        # actualizar la base de datos.
    
    def __init__(self, parent=None):
        super(SalesProxyModel, self).__init__()
        self._filter_column:int = -1 # columna qué filtrar por defecto
    
    # inserción de filas
    def insertRows(self, row:int, count:int, data_to_insert:dict[str, Any], 
                   parent:QModelIndex=QModelIndex()) -> bool:
        source_model:SalesTableModel = self.sourceModel()
        
        source_parent = self.mapToSource(parent)
        
        # notifica a la VISTA que se insertarán filas
        if not source_model.insertRows(row, count, data_to_insert, source_parent):
            return False
        
        # emite señales para confirmar cambios
        self.beginInsertRows(parent, row, row + count - 1)
        self.endInsertRows()
        return True
    
    
    # eliminación de filas
    def removeSelectedRows(self, selected_rows:tuple[int]) -> None:
        source_model:SalesTableModel = self.sourceModel()
        
        selected_source_rows:tuple[int] = tuple(
            self.mapToSource(self.index(proxy_row, 0)).row() for proxy_row in selected_rows
        )
        
        if selected_source_rows:
            # emite señal a MainWindow con las filas seleccionadas en el MODELO BASE
            self.baseModelRowsSelected.emit(selected_source_rows)
            
            source_model.removeSelectedModelRows(selected_rows=selected_source_rows)
        return None
    
    
    # ordenamiento
    def lessThan(self, source_left:QModelIndex, source_right:QModelIndex) -> bool:
        _source_model:SalesTableModel = self.sourceModel()
        _left_value:float | QDateTime | str # intenta comparar primero los valores como sus tipos de 
        _right_value:float | QDateTime | str # datos correspondientes, sino puede lo hace como str.
        
        # antes de obtener datos del modelo, verifica qué columna se está ordenando
        match source_left.column():
            case TableViewColumns.SALES_DETAIL.value: # detalle de venta
                _left_value = _source_model._data[source_left.row(), ModelDataCols.SALES_DETAIL.value]
                _right_value = _source_model._data[source_right.row(), ModelDataCols.SALES_DETAIL.value]
            
            case TableViewColumns.SALES_QUANTITY.value: # cantidad
                _left_value = _source_model._data[source_left.row(), ModelDataCols.SALES_QUANTITY.value]
                _right_value = _source_model._data[source_right.row(), ModelDataCols.SALES_QUANTITY.value]
                
                try:
                    return float(_left_value) < float(_right_value)
                
                except (ValueError, IndexError):
                    pass
                
            case TableViewColumns.SALES_PRODUCT_NAME.value: # producto
                _left_value = _source_model._data[source_left.row(), ModelDataCols.SALES_PRODUCT_NAME.value]
                _right_value = _source_model._data[source_right.row(), ModelDataCols.SALES_PRODUCT_NAME.value]
            
            case TableViewColumns.SALES_TOTAL_COST.value: # costo total
                _left_value = _source_model._data[source_left.row(), ModelDataCols.SALES_TOTAL_COST.value]
                _right_value = _source_model._data[source_right.row(), ModelDataCols.SALES_TOTAL_COST.value]
                
                try:
                    return float(_left_value) < float(_right_value)
                
                except (ValueError, IndexError):
                    pass
            
            case TableViewColumns.SALES_TOTAL_PAID.value: # abonado
                _left_value = _source_model._data[source_left.row(), ModelDataCols.SALES_TOTAL_PAID.value]
                _right_value = _source_model._data[source_right.row(), ModelDataCols.SALES_TOTAL_PAID.value]
                
                try:
                    return float(_left_value) < float(_right_value)
                
                except (ValueError, IndexError):
                    pass
            
            case TableViewColumns.SALES_DATETIME.value: # fecha y hora
                _left_value = str(_source_model._data[source_left.row(), ModelDataCols.SALES_DATETIME.value])
                _right_value = str(_source_model._data[source_right.row(), ModelDataCols.SALES_DATETIME.value])
                
                _left_value = QDateTime.fromString(_left_value, "d/M/yyyy HH:mm:ss")
                _right_value = QDateTime.fromString(_right_value, "d/M/yyyy HH:mm:ss")
                
                return _left_value < _right_value

        return str(_left_value) < str(_right_value)


    # filtrado avanzado
    def setFilterColumn(self, column:int) -> None:
        '''
        Al alternar el ordenamiento entre columnas, éste método se encarga de 
        establecer la nueva columna que se debe ordenar en el PROXY MODEL.

        Parámetros
        ----------
        column : int
            columna a ordenar

        Retorna
        -------
        None
        '''
        self._filter_column = column
        self.invalidateFilter()
        return None
    
    
    def filterAcceptsRow(self, source_row:int, source_parent:QModelIndex) -> bool:
        regex = self.filterRegularExpression()
        
        if not regex.pattern():
            return True
        
        _source_model:SalesTableModel = self.sourceModel()
        index_data:Any
        
        # si la columna de filtrado es -1 busca en todas
        if self._filter_column == -1:
            for col in range(_source_model.columnCount()):
                index_data = _source_model.index(
                    source_row,
                    col,
                    source_parent).data(Qt.ItemDataRole.DisplayRole)
                
                if index_data and regex.match(index_data).hasMatch():
                    return True
            return False
        
        # sino, busca en la columna especificada
        else:
            index_data = _source_model.index(
                source_row,
                self._filter_column,
                source_parent).data(Qt.ItemDataRole.DisplayRole)
        
        return regex.match(index_data).hasMatch() if index_data else False





class DebtsProxyModel(QSortFilterProxyModel):
    '''
    PROXY MODEL editable de Deudas.
    '''
    baseModelRowsSelected:Signal = Signal(object) # emite una tupla[int] con las filas seleccionadas 
                                        # mapeadas del MODELO BASE a MainWindow para 
                                        # actualizar la base de datos.
    
    def __init__(self, parent=None):
        super(DebtsProxyModel, self).__init__()
        self._filter_column:int = -1 # columna qué filtrar por defecto
    
    # inserción de filas
    def insertRows(self, row:int, count:int, data_to_insert:dict[str, Any], 
                   parent:QModelIndex=QModelIndex()) -> bool:
        source_model:DebtsTableModel = self.sourceModel()
        
        source_parent = self.mapToSource(parent)
        
        # notifica a la VISTA que se insertarán filas
        if not source_model.insertRows(row, count, data_to_insert, source_parent):
            return False
        
        # emite señales para confirmar cambios
        self.beginInsertRows(parent, row, row + count - 1)
        self.endInsertRows()
        return True
    
    
    # eliminación de filas
    def removeSelectedRows(self, selected_rows:tuple[int]) -> None:
        source_model:SalesTableModel = self.sourceModel()
        
        selected_source_rows:tuple[int] = tuple(
            self.mapToSource(self.index(proxy_row, 0)).row() for proxy_row in selected_rows
        )
        
        if selected_source_rows:
            # emite señal a MainWindow con las filas seleccionadas en el MODELO BASE
            self.baseModelRowsSelected.emit(selected_source_rows)
            
            source_model.removeSelectedModelRows(selected_rows=selected_source_rows)
        return None
    
    
    # ordenamiento
    def lessThan(self, source_left:QModelIndex, source_right:QModelIndex) -> bool:
        _source_model:DebtsTableModel = self.sourceModel()
        _left_value:int | float | str # intenta comparar primero los valores como sus tipos de 
        _right_value:int | float | str # datos correspondientes, sino puede lo hace como str.
        
        # antes de obtener datos del modelo, verifica qué columna se está ordenando
        match source_left.column():
            case TableViewColumns.DEBTS_POSTAL_CODE.value: # código postal
                _left_value = _source_model._data[source_left.row(), ModelDataCols.DEBTS_POSTAL_CODE.value]
                _right_value = _source_model._data[source_right.row(), ModelDataCols.DEBTS_POSTAL_CODE.value]
                try:
                    return int(_left_value) < int(_right_value)
                except (ValueError, IndexError):
                    pass
            
            case TableViewColumns.DEBTS_BALANCE.value: # balance total
                _left_value = _source_model.data(source_left, Qt.ItemDataRole.DisplayRole)
                _right_value = _source_model.data(source_right, Qt.ItemDataRole.DisplayRole)
                
                _left_value = _left_value.lstrip("$ ")
                _right_value = _right_value.lstrip("$ ")
                try:
                    return float(_left_value) < float(_right_value)
                except (ValueError, IndexError):
                    pass
            
            case _: # nombre | apellido | número de teléfono | dirección
                _left_value = _source_model.data(source_left, Qt.ItemDataRole.DisplayRole)
                _right_value = _source_model.data(source_right, Qt.ItemDataRole.DisplayRole)
            
        return str(_left_value) < str(_right_value)


    # filtrado avanzado
    def setFilterColumn(self, column:int) -> None:
        '''
        Al alternar el ordenamiento entre columnas, éste método se encarga de 
        establecer la nueva columna que se debe ordenar en el PROXY MODEL.

        Parámetros
        ----------
        column : int
            columna a ordenar

        Retorna
        -------
        None
        '''
        self._filter_column = column
        self.invalidateFilter()
        return None
    
    
    def filterAcceptsRow(self, source_row:int, source_parent:QModelIndex) -> bool:
        regex = self.filterRegularExpression()
        
        if not regex.pattern():
            return True
        
        _source_model:DebtsTableModel = self.sourceModel()
        index_data:Any
        
        # si la columna de filtrado es -1 busca en todas
        if self._filter_column == -1:
            for col in range(_source_model.columnCount()):
                index_data = _source_model.index(
                    source_row,
                    col,
                    source_parent).data(Qt.ItemDataRole.DisplayRole)
                
                if index_data and regex.match(index_data).hasMatch():
                    return True
            return False
        
        # sino, busca en la columna especificada
        else:
            index_data = _source_model.index(
                source_row,
                self._filter_column,
                source_parent).data(Qt.ItemDataRole.DisplayRole)
        
        return regex.match(index_data).hasMatch() if index_data else False


    # data
    def getDebtorID(self, index:QModelIndex) -> int:
        '''
        Obtiene y devuelve el IDdeudor desde el MODELO DE DATOS base.
        Éste método es usado desde el DELEGADO de la VISTA de Deudas para poder 
        acceder al IDdeudor del MODELO.

        Parámetros
        ----------
        index : QModelIndex
            el índice actual

        Retorna
        -------
        int
            el IDdeudor del índice actual
        '''
        model:DebtsTableModel = self.sourceModel()
        
        debtor_id:int = model.data(
            index=self.mapToSource(index),
            role=Qt.ItemDataRole.DisplayRole,
            return_debtor_id=True
        )
        
        return int(debtor_id)









