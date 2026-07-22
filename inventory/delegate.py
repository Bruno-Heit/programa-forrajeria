
from PySide6.QtWidgets import (
    QWidget,
    QStyledItemDelegate,
    QStyleOptionViewItem,
    QComboBox,
    QLineEdit,
)
from PySide6.QtCore import (
    Qt,
    QModelIndex,
    QSize,
    QPersistentModelIndex,
    QAbstractItemModel,
    Signal,
    Slot,
)

from common.enumclasses import (
    TableViewId,
    InvViewCols,
    WidgetStyle,
)
from common.functionutils import getProductsCategories, createCompleter
from common.customvalidators import (
    ProductNameValidator,
    ProductStockValidator,
    ProductUnitPriceValidator,
    ProductComercPriceValidator,
)


class InventoryDelegate(QStyledItemDelegate):
    """Clase DELEGADO que se encarga de personalizar/editar celdas del QTableView de inventario,
    además, normalmente, el método 'setModelData' se encarga de validar datos, pero en este caso
    no es necesario ya que cada editor (dependiendo de la columna) tiene un validador."""

    fieldIsValid: Signal = Signal(
        object
    )  # extensión de 'validator.validationSucceeded',
    # emite hacia MainWindow un TableViewId.
    fieldIsInvalid: Signal = Signal(
        object
    )  # extensión de 'validator.validationFailed',
    # emite hacia MainWindow tuple(TableViewId,
    # feedback como str).

    def createEditor(
        self,
        parent: QWidget,
        option: QStyleOptionViewItem,
        index: QModelIndex | QPersistentModelIndex,
    ) -> QWidget:
        editor: QWidget
        validator = None

        match index.column():
            case InvViewCols.INV_CATEGORY.value:  # categoría
                editor = QComboBox(parent)
                editor.setEditable(False)
                editor.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
                editor.setFrame(False)
                editor.addItems(getProductsCategories())
                editor.setStyleSheet(WidgetStyle.DEF_COMBOBOX_ARROW_ICON.value)
                editor.setPlaceholderText("Seleccionar una categoría")

            case InvViewCols.INV_PRODUCT_NAME.value:  # nombre
                editor = QLineEdit(parent)
                editor.setCompleter(createCompleter(type=3))
                editor.setMaxLength(50)
                validator = ProductNameValidator(
                    prev_name=index.data(Qt.ItemDataRole.DisplayRole)
                )
                validator.validationSucceeded.connect(self.__onValidField)
                validator.validationFailed.connect(self.__onInvalidField)
                editor.setValidator(validator)

            case InvViewCols.INV_DESCRIPTION.value:  # descripción
                editor = QLineEdit(parent)
                editor.setMaxLength(200)

            case InvViewCols.INV_STOCK.value:  # stock
                editor = QLineEdit(parent)
                editor.setMaxLength(31)
                validator = ProductStockValidator(parent=editor)
                validator.validationSucceeded.connect(self.__onValidField)
                validator.validationFailed.connect(self.__onInvalidField)
                editor.setValidator(validator)

            case InvViewCols.INV_NORMAL_PRICE.value:  # precio unitario
                editor = QLineEdit(parent)
                editor.setMaxLength(10)
                validator = ProductUnitPriceValidator(editor)
                validator.validationSucceeded.connect(self.__onValidField)
                validator.validationFailed.connect(self.__onInvalidField)
                editor.setValidator(validator)

            case InvViewCols.INV_COMERCIAL_PRICE.value:  # precio comercial
                editor = QLineEdit(parent)
                editor.setMaxLength(10)
                validator = ProductComercPriceValidator(editor)
                validator.validationSucceeded.connect(self.__onValidField)
                validator.validationFailed.connect(self.__onInvalidField)
                editor.setValidator(validator)
        return editor

    @Slot()
    def __onValidField(self):
        """
        Emite la señal 'fieldIsValid' hacia MainWindow. Funciona principalmente
        como una extensión de la señal 'validator.validationSucceeded'.


        """
        self.fieldIsValid.emit(TableViewId.INVEN_TABLE_VIEW)
        return None

    @Slot(str)
    def __onInvalidField(self, feedback_text: str):
        """
        Emite la señal 'fieldIsValid' hacia MainWindow. Funciona principalmente
        como una extensión de la señal 'validator.validationSucceeded'.

        Parámetros
        ----------
        feedback_text: str
            Texto con feedback para mostrar al usuario


        """
        self.fieldIsInvalid.emit((TableViewId.INVEN_TABLE_VIEW, feedback_text))
        return None

    def setEditorData(
        self, editor: QComboBox | QLineEdit, index: QModelIndex | QPersistentModelIndex
    ) -> None:
        if isinstance(editor, QComboBox):
            editor.setCurrentText(index.data(Qt.ItemDataRole.DisplayRole))

        else:
            editor.setText(index.data(Qt.ItemDataRole.DisplayRole))

        return None

    def setModelData(
        self,
        editor: QComboBox | QLineEdit,
        model: QAbstractItemModel,
        index: QModelIndex | QPersistentModelIndex,
    ) -> None:
        col: int = index.column()

        # * formateo de datos
        if isinstance(editor, QComboBox):
            value = editor.currentText()

        else:
            value = editor.text().strip()
            # col 3 es stock
            if (col == 3) and (value.split(" ")[0].endswith((",", "."))):
                full_value = value.split(" ")
                try:
                    value = " ".join([full_value[0].rstrip(",."), full_value[1]])
                except (
                    IndexError
                ):  # devuelve IndexError cuando no se escribe la unidad de medida
                    value = full_value[0].rstrip(",.")

            # col 4 es precio normal, col 5 es precio comercial
            elif (col == 4 or col == 5) and (value.endswith((",", "."))):
                value = value.rstrip(",.")

            editor.setText(value)

        model.setData(index, value, Qt.ItemDataRole.EditRole)
        return None

    def updateEditorGeometry(
        self,
        editor: QComboBox | QLineEdit,
        option: QStyleOptionViewItem,
        index: QModelIndex | QPersistentModelIndex,
    ) -> None:
        editor.setGeometry(option.rect)
        return None

    def sizeHint(self, option: QStyleOptionViewItem, index: QModelIndex) -> QSize:
        return super().sizeHint(option, index)


