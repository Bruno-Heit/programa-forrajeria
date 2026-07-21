
from PySide6.QtCore import QSortFilterProxyModel, Qt, QModelIndex, Signal, QDateTime

from sales.data_model import SalesTableModel
from common.enumclasses import (
    SalesModelCols,
    SalesViewCols,
    DateAndTimeFormat,
)
from typing import Any

class SalesProxyModel(QSortFilterProxyModel):
    """
    PROXY MODEL editable de Ventas.
    """

    baseModelRowsSelected: Signal = Signal(
        object
    )  # emite una tupla[int] con las filas seleccionadas
    # mapeadas del MODELO BASE a MainWindow para
    # actualizar la base de datos.

    def __init__(self, parent=None):
        super(SalesProxyModel, self).__init__()
        self._filter_column: int = -1  # columna qué filtrar por defecto

    # inserción de filas
    def insertRows(
        self,
        row: int,
        count: int,
        data_to_insert: dict[str, Any],
        parent: QModelIndex = QModelIndex(),
    ) -> bool:
        source_model: SalesTableModel = self.sourceModel()

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
        source_model: SalesTableModel = self.sourceModel()

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
        _source_model: SalesTableModel = self.sourceModel()
        _left_value: (
            float | QDateTime | str
        )  # intenta comparar primero los valores como sus tipos de
        _right_value: (
            float | QDateTime | str
        )  # datos correspondientes, sino puede lo hace como str.

        # antes de obtener datos del modelo, verifica qué columna se está ordenando
        match source_left.column():
            case SalesViewCols.SALES_DETAIL.value:  # detalle de venta
                _left_value = _source_model._data[
                    source_left.row(), SalesModelCols.SALES_DETAIL.value
                ]
                _right_value = _source_model._data[
                    source_right.row(), SalesModelCols.SALES_DETAIL.value
                ]

            case SalesViewCols.SALES_QUANTITY.value:  # cantidad
                _left_value = _source_model._data[
                    source_left.row(), SalesModelCols.SALES_QUANTITY.value
                ]
                _right_value = _source_model._data[
                    source_right.row(), SalesModelCols.SALES_QUANTITY.value
                ]

                try:
                    return float(_left_value) < float(_right_value)

                except (ValueError, IndexError):
                    pass

            case SalesViewCols.SALES_PRODUCT_NAME.value:  # producto
                _left_value = _source_model._data[
                    source_left.row(), SalesModelCols.SALES_PRODUCT_NAME.value
                ]
                _right_value = _source_model._data[
                    source_right.row(), SalesModelCols.SALES_PRODUCT_NAME.value
                ]

            case SalesViewCols.SALES_TOTAL_COST.value:  # costo total
                _left_value = _source_model._data[
                    source_left.row(), SalesModelCols.SALES_TOTAL_COST.value
                ]
                _right_value = _source_model._data[
                    source_right.row(), SalesModelCols.SALES_TOTAL_COST.value
                ]

                try:
                    return float(_left_value) < float(_right_value)

                except (ValueError, IndexError):
                    pass

            case SalesViewCols.SALES_TOTAL_PAID.value:  # abonado
                _left_value = _source_model._data[
                    source_left.row(), SalesModelCols.SALES_TOTAL_PAID.value
                ]
                _right_value = _source_model._data[
                    source_right.row(), SalesModelCols.SALES_TOTAL_PAID.value
                ]

                try:
                    return float(_left_value) < float(_right_value)

                except (ValueError, IndexError):
                    pass

            case SalesViewCols.SALES_DATETIME.value:  # fecha y hora
                _left_value = str(
                    _source_model._data[
                        source_left.row(), SalesModelCols.SALES_DATETIME.value
                    ]
                )
                _right_value = str(
                    _source_model._data[
                        source_right.row(), SalesModelCols.SALES_DATETIME.value
                    ]
                )

                _left_value = QDateTime.fromString(
                    _left_value, DateAndTimeFormat.LOCAL_DATETIME_FORMAT.value
                )
                _right_value = QDateTime.fromString(
                    _right_value, DateAndTimeFormat.LOCAL_DATETIME_FORMAT.value
                )

                return _left_value < _right_value

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

        _source_model: SalesTableModel = self.sourceModel()
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

