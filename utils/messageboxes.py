# message-box dialog para preguntar antes de eliminar registros
"""
Éste archivo contiene las subclases de **QMessageBoxes** y **QDialogs**
que tienen como principal objetivo informar o advertir al usuario sobre
diversas acciones.
"""

from PySide6.QtWidgets import QMessageBox, QWidget, QDialog
from PySide6.QtCore import Qt, Slot

from utils.enumclasses import TableViewId
from ui.ui_warnAccountHasBalanceDialog import Ui_AccountHasBalDialog


class AskBeforeDeletion(QMessageBox):
    """
    **QMessageBox** usado para preguntar al usuario si de verdad quiere borrar
    un registro antes de hacerlo.
    """

    def __init__(
        self, parent: QWidget, table_viewID: TableViewId, reg_count: int
    ) -> None:
        """
        Inicializa un objeto de tipo **QMessageBox** usado para preguntar si
        se quiere eliminar un registro con mensajes personalizados dependiendo
        de la tabla a la que estará asociado.

        Parámetros
        ----------
        parent : QWidget
            *widget* padre del **QMessageBox**
        table_viewID : TableViewId
            ID de la tabla asociada
        reg_count : int
            cantidad de registros seleccionados
        """
        super(AskBeforeDeletion, self).__init__()
        self.setParent = parent
        self.table_viewID = table_viewID

        # textos
        self.setText(f"¿Está seguro de borrar los registros seleccionados?")
        self.setInformativeText(
            f"Se borrarán {reg_count} registros"
            if reg_count > 1
            else f"Se borrará {reg_count} registro"
        )
        self.setDetailedText(
            "Los registros borrados no se eliminarán de la base de datos "
            + "para evitar conflictos, simplemente no serán mostrados al "
            + "ver datos en las tablas"
        ) if self.table_viewID != TableViewId.DEBTS_TABLE_VIEW else None

        match self.table_viewID:
            case TableViewId.INVEN_TABLE_VIEW:
                self.setWindowTitle("¿Eliminar registros de inventario?")

            case TableViewId.SALES_TABLE_VIEW:
                self.setWindowTitle("¿Eliminar registros de ventas?")

            case TableViewId.DEBTS_TABLE_VIEW:
                self.setWindowTitle("¿Eliminar registros de cuentas corrientes?")
                self.setDetailedText(
                    "Los registros borrados no se eliminarán de la base de "
                    + "datos para evitar conflictos, pero sí serán "
                    + "anonimizados para así cumplir con la Ley de Protección "
                    + "de los Datos Personales 25.326 de la República Argentina"
                )

        # botones
        self.setStandardButtons(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        self.setDefaultButton(QMessageBox.StandardButton.No)

        self.setup_ui()
        return None

    def setup_ui(self) -> None:
        self.setIcon(QMessageBox.Icon.Question)

        self.setStyleSheet(
            """
            QMessageBox {
                background-color: #fff;
            }
            
            QDialogButtonBox > QPushButton {
                background-color: #415a77;
                color: #fff;
                border: none;
                border-radius: 3px;
                min-width: 80px;
                height: 30px;
            }
            QDialogButtonBox > QPushButton:hover,
            QDialogButtonBox > QPushButton:focus {
                background-color: #3b66ab;
            }
            QDialogButtonBox > QPushButton:pressed {
                background-color: #3b66ab;
                border: 1px inset #778da9;
            }
            QDialogButtonBox > QPushButton:disabled {
                background-color: rgb(103, 115, 122);
                color: #999;
            }
            
            QDialogButtonBox > QPushButton[text="&Sí"] {
                background-color: #ff4949;
            }
            QDialogButtonBox > QPushButton[text="&Sí"]:hover,
            QDialogButtonBox > QPushButton[text="&Sí"]:focus {
                background-color: #faa;
            }
            QDialogButtonBox > QPushButton[text="&Sí"]:pressed {
                background-color: #3b66ab;
                border: 1px inset #778da9;
            }
            
            QDialogButtonBox > QPushButton[text="&No"] {
                background-color: #fff;
                color: #111;
                border: 1px solid #aaa;
            }
            QDialogButtonBox > QPushButton[text="&No"]:hover,
            QDialogButtonBox > QPushButton[text="&No"]:pressed,
            QDialogButtonBox > QPushButton[text="&No"]:focus {
                background-color: #ccc;
            }
            
            
            QLabel {
                font-size: 13px;
                color: #111;
            }
            
            QLabel#qt_msgbox_label {
                font-weight: bold;
            }
            """
        )
        return None


class WarnAccountHasBalance(QDialog):
    """
    **QMessageBox** usado para advertir al usuario que hay cuentas corrientes
    seleccionadas que tienen una deuda/saldo a favor.
    """

    def __init__(self, selected_accounts: list[list[str, str]]) -> None:
        """
        Inicializa un objeto de tipo **QDialog** usado para advertir que hay
        cuentas corrientes seleccionadas con saldo no nulo.

        Parámetros
        ----------
        selected_accounts : list[list[str, str]]
            lista con los nombres y apellidos de las cuentas seleccionadas
        """
        super(WarnAccountHasBalance, self).__init__()
        self.ui_warn_dialog = Ui_AccountHasBalDialog()
        self.ui_warn_dialog.setupUi(self)

        self.selected_accounts: list[list[str, str]] = selected_accounts

        self.setup_ui()
        self.setup_signals()

    def setup_ui(self) -> None:
        # coloca el texto informativo
        text: str
        count_accounts: int = len(self.selected_accounts)

        if count_accounts > 1:
            text = (
                f"Hay {count_accounts} cuentas corrientes seleccionadas con "
                + "saldo no nulo"
            )
        else:
            text = "Hay 1 cuenta corriente seleccionada con saldo no nulo"
        self.ui_warn_dialog.label_accountsWithoutZeroBal.setText(text)

        self.ui_warn_dialog.lw_accountsWithBal.hide()

        self.ui_warn_dialog.body.adjustSize()
        self.adjustSize()

        self.ui_warn_dialog.buttonBox.setStyleSheet(
            """
            QDialogButtonBox > QPushButton {
                background-color: #415a77;
                color: #fff;
                border: none;
                border-radius: 3px;
                min-width: 80px;
                height: 30px;
            }
            QDialogButtonBox > QPushButton:hover,
            QDialogButtonBox > QPushButton:focus {
                background-color: #3b66ab;
            }
            QDialogButtonBox > QPushButton:pressed {
                background-color: #3b66ab;
                border: 1px inset #778da9;
            }
            QDialogButtonBox > QPushButton:disabled {
                background-color: rgb(103, 115, 122);
                color: #999;
            }
            
            QDialogButtonBox > QPushButton[text="&Sí"] {
                background-color: #ff4949;
            }
            QDialogButtonBox > QPushButton[text="&Sí"]:hover,
            QDialogButtonBox > QPushButton[text="&Sí"]:focus {
                background-color: #faa;
            }
            QDialogButtonBox > QPushButton[text="&Sí"]:pressed {
                background-color: #3b66ab;
                border: 1px inset #778da9;
            }
            
            QDialogButtonBox > QPushButton[text="&No"] {
                background-color: #fff;
                color: #111;
                border: 1px solid #aaa;
            }
            QDialogButtonBox > QPushButton[text="&No"]:hover,
            QDialogButtonBox > QPushButton[text="&No"]:pressed,
            QDialogButtonBox > QPushButton[text="&No"]:focus {
                background-color: #ccc;
            }
            """
        )
        return None

    def setup_signals(self) -> None:
        self.ui_warn_dialog.checkb_toggleAccountsList.checkStateChanged.connect(
            self.toggleAccountsList
        )
        return None

    @Slot(Qt.CheckState)
    def toggleAccountsList(self, state: Qt.CheckState) -> None:
        """
        Muestra/esconde la lista de cuentas corrientes con saldo no nulo
        dependiendo del estado del *checkbox*.

        Parámetros
        ----------
        state : Qt.CheckState
            estado actual del *checkbox*
        """
        match state:
            case Qt.CheckState.Checked:
                self.ui_warn_dialog.lw_accountsWithBal.show()
                self.ui_warn_dialog.lw_accountsWithBal.clearSelection()
                self.ui_warn_dialog.lw_accountsWithBal.clear()
                self.ui_warn_dialog.lw_accountsWithBal.addItems(
                    [self.__getAccountOwner(acc) for acc in self.selected_accounts]
                )

            case Qt.CheckState.Unchecked:
                self.ui_warn_dialog.lw_accountsWithBal.hide()

        self.ui_warn_dialog.body.adjustSize()
        self.adjustSize()
        return None

    def __getAccountOwner(self, account: list[str, str]) -> str:
        """
        Devuelve el nombre del propietario de la cuenta corriente como un
        **str**.

        Parámetros
        ----------
        account : list[str, str]
            lista con el nombre y el apellido del propietario de la cuenta

        Retorna
        -------
        str
            cadena con el nombre y apellido del propietario de la cuenta
        """
        return f"{account[0]} {account[1]}"
