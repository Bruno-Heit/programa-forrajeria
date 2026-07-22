
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
    QEvent,
)

from common.enumclasses import (
    TableViewId,
    DebtorViewCols,
)
from common.customvalidators import (
    DebtorNameValidator,
    DebtorSurnameValidator,
    DebtorPhoneNumberValidator,
    DebtorDirectionValidator,
    DebtorPostalCodeValidator,
)
from utils.classes import ProductsBalanceDialog
from current_account.proxy_model import DebtsProxyModel


class DebtsDelegate(QStyledItemDelegate):
    """Clase DELEGADO que se encarga de personalizar/editar celdas del QTableView de deudas,
    además, normalmente, el método 'setModelData' se encarga de validar datos, pero en este
    caso no es necesario ya que cada editor (dependiendo de la columna) tiene un validador."""

    fieldIsValid: Signal = Signal(
        object
    )  # extensión de 'validator.validationSucceeded',
    # emite hacia MainWindow un TableViewId.
    fieldIsInvalid: Signal = Signal(
        object
    )  # extensión de 'validator.validationFailed',
    # emite hacia MainWindow tuple(TableViewId,
    # feedback como str).
    balanceDialogFinished: Signal = Signal(
        object
    )  # extensión de 'ProductsBalanceDialog.balanceChanged',
    # emite hacia MainWindow tuple(index, nuevo balance como float).

    def createEditor(
        self,
        parent: QWidget,
        option: QStyleOptionViewItem,
        index: QModelIndex | QPersistentModelIndex,
    ) -> QWidget:
        editor: QWidget
        validator = None
        match index.column():
            case DebtorViewCols.DEBTS_NAME.value:
                editor = QLineEdit(parent)
                validator = DebtorNameValidator(editor)
                validator.validationSucceeded.connect(self.__onValidField)
                validator.validationFailed.connect(self.__onInvalidField)
                editor.setValidator(validator)

            case DebtorViewCols.DEBTS_SURNAME.value:
                editor = QLineEdit(parent)
                validator = DebtorSurnameValidator(editor)
                validator.validationSucceeded.connect(self.__onValidField)
                validator.validationFailed.connect(self.__onInvalidField)
                editor.setValidator(validator)

            case DebtorViewCols.DEBTS_PHONE_NUMBER.value:
                editor = QLineEdit(parent)
                validator = DebtorPhoneNumberValidator(editor)
                validator.validationSucceeded.connect(self.__onValidField)
                validator.validationFailed.connect(self.__onInvalidField)
                editor.setValidator(validator)

            case DebtorViewCols.DEBTS_DIRECTION.value:
                editor = QLineEdit(parent)
                validator = DebtorDirectionValidator(editor)
                validator.validationSucceeded.connect(self.__onValidField)
                validator.validationFailed.connect(self.__onInvalidField)
                editor.setValidator(validator)

            case DebtorViewCols.DEBTS_POSTAL_CODE.value:
                editor = QLineEdit(parent)
                validator = DebtorPostalCodeValidator(editor)
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
        self.fieldIsValid.emit(TableViewId.DEBTS_TABLE_VIEW)
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
        self.fieldIsInvalid.emit((TableViewId.DEBTS_TABLE_VIEW, feedback_text))
        return None

    def setEditorData(
        self, editor: QLineEdit, index: QModelIndex | QPersistentModelIndex
    ) -> None:
        editor.setText(index.model().data(index, Qt.ItemDataRole.DisplayRole))
        return None

    def setModelData(
        self,
        editor: QLineEdit,
        model: QAbstractItemModel,
        index: QModelIndex | QPersistentModelIndex,
    ) -> None:
        # * formateo de datos
        match index.column():
            case DebtorViewCols.DEBTS_POSTAL_CODE.value:
                value = editor.text().replace(",", "").replace(".", "").strip()

            case _:
                value: str = editor.text().strip()

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

    def editorEvent(
        self,
        event: QEvent,
        model: DebtsProxyModel,
        option: QStyleOptionViewItem,
        index: QModelIndex,
    ):
        """
        Capta los eventos cuando se crea un editor en alguna columna. Se usa
        acá para inicializar el Dialog personalizado que creé para mostrar
        los productos con sus saldos.
        """
        balance_dialog: ProductsBalanceDialog

        if index.column() == DebtorViewCols.DEBTS_BALANCE.value:
            if event.type() == QEvent.Type.MouseButtonDblClick:
                balance_dialog = ProductsBalanceDialog(
                    debtor_id=model.getDebtorID(index),
                    curr_balance=model.data(index, Qt.ItemDataRole.DisplayRole),
                    table_view=self.parent(),  # le paso el table view para poder redimensionar
                )  # el dialog cuando se crea y no se salga del
                # rectángulo del table view.

                # emite la señal "finished" hacia MainWindow, se usa para obtener el nuevo balance
                balance_dialog.balanceChanged.connect(
                    lambda new_balance: self.balanceDialogFinished.emit(
                        (model.mapToSource(index), new_balance)
                    )
                )

                balance_dialog.show()
                balance_dialog.raise_()
                return True

        return False

