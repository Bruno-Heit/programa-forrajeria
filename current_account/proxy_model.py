
from PySide6.QtCore import QSortFilterProxyModel, Qt, QModelIndex, Signal, QDateTime

from current_account.data_model import (
    DebtsTableModel,
    ProductsBalanceModel,
)
from common.enumclasses import (
    DebtsModelCols,
    DebtorModelCols,
    DebtorViewCols,
    DebtsViewCols,
    DateAndTimeFormat,
)
from typing import Any

class DebtsProxyModel(QSortFilterProxyModel):
    """
    PROXY MODEL editable de Deudas.
    """

    baseModelRowsSelected: Signal = Signal(
        object
    )  # emite una tupla[int] con las filas seleccionadas
    # mapeadas del MODELO BASE a MainWindow para
    # actualizar la base de datos.

    def __init__(self, parent=None):
        super(DebtsProxyModel, self).__init__()
        self._filter_column: int = -1  # columna qué filtrar por defecto

    # inserción de filas
    def insertRows(
        self,
        row: int,
        count: int,
        data_to_insert: dict[str, Any],
        parent: QModelIndex = QModelIndex(),
    ) -> bool:
        source_model: DebtsTableModel = self.sourceModel()

        source_parent = self.mapToSource(parent)

        # notifica a la VISTA que se insertarán filas
        if not source_model.insertRows(row, count, data_to_insert, source_parent):
            return False

        # emite señales para confirmar cambios
        self.beginInsertRows(parent, row, row + count - 1)
        self.endInsertRows()
        return True

    # eliminación de filas
    def removeSelectedRows(self, selected_rows: tuple[int]) -> None:
        source_model: DebtsTableModel = self.sourceModel()

        selected_source_rows: tuple[int] = tuple(
            self.mapToSource(self.index(proxy_row, 0)).row()
            for proxy_row in selected_rows
        )

        if selected_source_rows:
            # emite señal a MainWindow con las filas seleccionadas en el MODELO BASE
            self.baseModelRowsSelected.emit(selected_source_rows)

            source_model.removeSelectedModelRows(selected_rows=selected_source_rows)
        return None

    # ordenamiento
    def lessThan(self, source_left: QModelIndex, source_right: QModelIndex) -> bool:
        _source_model: DebtsTableModel = self.sourceModel()
        _left_value: (
            int | float | str
        )  # intenta comparar primero los valores como sus tipos de
        _right_value: (
            int | float | str
        )  # datos correspondientes, sino puede lo hace como str.

        # antes de obtener datos del modelo, verifica qué columna se está ordenando
        match source_left.column():
            case DebtorViewCols.DEBTS_POSTAL_CODE.value:  # código postal
                _left_value = _source_model._data[
                    source_left.row(), DebtorModelCols.DEBTS_POSTAL_CODE.value
                ]
                _right_value = _source_model._data[
                    source_right.row(), DebtorModelCols.DEBTS_POSTAL_CODE.value
                ]
                try:
                    return int(_left_value) < int(_right_value)
                except (ValueError, IndexError):
                    pass

            case DebtorViewCols.DEBTS_BALANCE.value:  # balance total
                _left_value = _source_model.data(
                    source_left, Qt.ItemDataRole.DisplayRole
                )
                _right_value = _source_model.data(
                    source_right, Qt.ItemDataRole.DisplayRole
                )

                _left_value = _left_value.lstrip("$ ")
                _right_value = _right_value.lstrip("$ ")
                try:
                    return float(_left_value) < float(_right_value)
                except (ValueError, IndexError):
                    pass

            case _:  # nombre | apellido | número de teléfono | dirección
                _left_value = _source_model.data(
                    source_left, Qt.ItemDataRole.DisplayRole
                )
                _right_value = _source_model.data(
                    source_right, Qt.ItemDataRole.DisplayRole
                )

        return str(_left_value) < str(_right_value)

    # filtrado avanzado
    def setFilterColumn(self, column: int) -> None:
        """
        Al alternar el ordenamiento entre columnas, éste método se encarga de
        establecer la nueva columna que se debe ordenar en el PROXY MODEL.

        Parámetros
        ----------
        column : int
            columna a ordenar


        """
        self._filter_column = column
        self.invalidateFilter()
        return None

    def filterAcceptsRow(self, source_row: int, source_parent: QModelIndex) -> bool:
        regex = self.filterRegularExpression()

        if not regex.pattern():
            return True

        _source_model: DebtsTableModel = self.sourceModel()
        index_data: Any

        # si la columna de filtrado es -1 busca en todas
        if self._filter_column == -1:
            for col in range(_source_model.columnCount()):
                index_data = _source_model.index(source_row, col, source_parent).data(
                    Qt.ItemDataRole.DisplayRole
                )

                if index_data and regex.match(index_data).hasMatch():
                    return True
            return False

        # sino, busca en la columna especificada
        else:
            index_data = _source_model.index(
                source_row, self._filter_column, source_parent
            ).data(Qt.ItemDataRole.DisplayRole)

        return regex.match(index_data).hasMatch() if index_data else False

    # data
    def getDebtorID(self, index: QModelIndex) -> int:
        """
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
        """
        model: DebtsTableModel = self.sourceModel()

        debtor_id: int = model.data(
            index=self.mapToSource(index),
            role=Qt.ItemDataRole.DisplayRole,
            return_debtor_id=True,
        )

        return int(debtor_id)


class ProductsBalanceProxyModel(QSortFilterProxyModel):
    """
    PROXY MODEL editable de Deudas, es usado cuando se crea el QDialog con los
    productos adeudados en la columna "balance".
    """

    baseModelRowsSelected: Signal = Signal(
        object
    )  # emite una tupla[int] con las filas seleccionadas
    # mapeadas del MODELO BASE para actualizar los datos.

    def __init__(self, parent=None):
        super(ProductsBalanceProxyModel, self).__init__()
        self.invalidateFilter()

    # eliminación de filas
    def removeSelectedRows(self, selected_rows: tuple[int]) -> None:
        source_model: ProductsBalanceModel = self.sourceModel()

        selected_source_rows: tuple[int] = tuple(
            self.mapToSource(self.index(proxy_row, 0)).row()
            for proxy_row in selected_rows
        )

        if selected_source_rows:
            # emite señal a MainWindow con las filas seleccionadas en el MODELO BASE
            self.baseModelRowsSelected.emit(selected_source_rows)

            source_model.removeSelectedModelRows(selected_rows=selected_source_rows)
        return None

    # ordenamiento
    def lessThan(self, source_left: QModelIndex, source_right: QModelIndex) -> bool:
        _source_model: ProductsBalanceModel = self.sourceModel()
        _left_value: (
            float | QDateTime | str
        )  # intenta comparar primero los valores como sus tipos de
        _right_value: (
            float | QDateTime | str
        )  # datos correspondientes, sino puede lo hace como str.

        # antes de obtener datos del modelo, verifica qué columna se está ordenando
        match source_left.column():
            case DebtsViewCols.PRODS_BAL_DATETIME.value:
                _left_value = _source_model._data[
                    source_left.row(), DebtsModelCols.PRODS_BAL_DATETIME.value
                ]
                _right_value = _source_model._data[
                    source_right.row(), DebtsModelCols.PRODS_BAL_DATETIME.value
                ]

                _left_value = QDateTime.fromString(
                    _left_value, DateAndTimeFormat.LOCAL_DATETIME_FORMAT.value
                )
                _right_value = QDateTime.fromString(
                    _right_value, DateAndTimeFormat.LOCAL_DATETIME_FORMAT.value
                )

                return _left_value < _right_value

            case DebtsViewCols.PRODS_BAL_DESCRIPTION.value:
                _left_value = _source_model._data[
                    source_left.row(), DebtsModelCols.PRODS_BAL_DESCRIPTION.value
                ]
                _right_value = _source_model._data[
                    source_right.row(), DebtsModelCols.PRODS_BAL_DESCRIPTION.value
                ]

                _left_value = _left_value.lstrip("$ ")
                _right_value = _right_value.lstrip("$ ")

            case DebtsViewCols.PRODS_BAL_BALANCE.value:
                _left_value = _source_model._data[
                    source_left.row(), DebtsModelCols.PRODS_BAL_BALANCE.value
                ]
                _right_value = _source_model._data[
                    source_right.row(), DebtsModelCols.PRODS_BAL_BALANCE.value
                ]

                try:
                    return float(_left_value) < float(_right_value)
                except:
                    pass

        return str(_left_value) < str(_right_value)

    # filtrado avanzado
    def filterAcceptsRow(self, source_row: int, source_parent: QModelIndex) -> bool:
        regex = self.filterRegularExpression()

        if not regex.pattern():
            return True

        _source_model: ProductsBalanceModel = self.sourceModel()
        index_data: Any

        for col in range(_source_model.columnCount()):
            index_data = str(
                _source_model.index(source_row, col, source_parent).data(
                    Qt.ItemDataRole.DisplayRole
                )
            )

            if index_data and regex.match(index_data).hasMatch():
                return True
        return False

    # data
    def getSaleDetailID(self, row: int) -> int:
        """
        Obtiene y devuelve el ID_detalle_venta desde el MODELO DE DATOS base.

        Parámetros
        ----------
        index : int
            la fila seleccionada

        Retorna
        -------
        int
            el ID_detalle_venta de la fila actual
        """
        model: ProductsBalanceModel = self.sourceModel()

        debtor_id: int = model.getSaleDetailID(row)

        return int(debtor_id)
