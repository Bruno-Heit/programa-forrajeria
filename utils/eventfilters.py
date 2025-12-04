"""
Éste archivo contiene las declaraciones de los filtros de eventos
personalizados usados en el programa.
"""

from PySide6.QtWidgets import (
    QTableView,
    QListWidget,
    QListWidgetItem,
    QLineEdit,
    QMenu,
    QTextEdit,
)
from PySide6.QtCore import QObject, QEvent, Qt, QSize, Signal, Slot
from PySide6.QtGui import QPainter, QPixmap, QAction

from resources import rc_icons

from utils.enumclasses import TablesAndListsObjName, CommonCategories


class BackgroundEventFilter(QObject):
    """
    Filtro de eventos que sobreescribe el funcionamiento del evento Paint de
    Qt y dibuja los datos de una tabla/widget si hay ó una imagen de fondo
    sino.
    Está diseñado para ser usado específicamente con QTableViews/QListWidgets.
    La razón de que acepte simplemente esos dos tipos de widgets es que sólo
    se necesita mostrar imágenes dentro de los viewports de los siguientes
    widgets:
    - tv_inventory_data (QTableView)
    - sales_input_list (QListWidget)
    - tv_sales_data (QTableView)
    - tv_debts_data (QTableView)
    - tv_balance_products (QTableView)
    """

    def __init__(self, widget: QTableView | QListWidget):
        """
        Dependiendo del widget muestra un fondo determinado dependiendo de si
        el widget está mostrando datos o no.
        Si hay datos en el viewport del widget los muestra, sino muestra una
        imagen de fondo propia del widget.

        Parámetros
        ----------
        widget : QTableView | QListWidget
            la vista / widget al que pintarle el background
        """
        super().__init__()
        self.widget: QTableView = widget

        self.pixmap: QPixmap
        self.__max_pixmap_size: QSize

        match widget.objectName():
            case TablesAndListsObjName.INVEN_TABLE_VIEW.value:
                self.pixmap = QPixmap(":/icons/products-table-empty-bg.png")

            case TablesAndListsObjName.SALES_INPUT_LIST.value:
                self.pixmap = QPixmap(":/icons/sales-empty-input-list-bg.png")

            case TablesAndListsObjName.SALES_TABLE_VIEW.value:
                self.pixmap = QPixmap(":/icons/sales-table-empty-bg.png")

            case TablesAndListsObjName.DEBTS_TABLE_VIEW.value:
                self.pixmap = QPixmap(":/icons/debts-table-empty-bg.png")

            case TablesAndListsObjName.BAL_PRODS_TABLE_VIEW.value:
                self.pixmap = QPixmap(":/icons/debts-empty-prods-balance-table-bg.png")

        self.__max_pixmap_size = QPixmap.size(self.pixmap)
        return None

    def eventFilter(self, watched: QTableView | QListWidget, event: QEvent):
        painter: QPainter
        target_size: QSize

        if event.type() == QEvent.Type.Paint:
            # Deja que se pinte la tabla normalmente
            result = super().eventFilter(watched, event)

            # Si el modelo está vacío, dibuja la imagen de fondo
            if self.widget.model() is None or self.widget.model().rowCount() == 0:
                painter = QPainter(watched)

                # calcula el tamaño objetivo
                target_size = QSize(
                    min(watched.size().width(), self.__max_pixmap_size.width()),
                    min(watched.size().height(), self.__max_pixmap_size.height()),
                )

                # escala la imagen
                scaled = self.pixmap.scaled(
                    target_size,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
                x = (watched.width() - scaled.width()) // 2
                y = (watched.height() - scaled.height()) // 2

                painter.drawPixmap(x, y, scaled)
            return result
        return super().eventFilter(watched, event)


class CategoryItemEventFilter(QObject):
    """
    Filtro de eventos que sobreescribe el funcionamiento del evento FocusOut
    del QLineEdit creado cuando se añade un item nuevo al QListWidget de
    categorías.
    """

    itemToDelete: Signal = Signal(QListWidgetItem)
    itemToReset: Signal = Signal(QListWidgetItem)

    def __init__(
        self, lineedit: QLineEdit, item: QListWidgetItem, edit_mode: bool = False
    ):
        """
        Capta el evento FocusOut y verifica si el campo es inválido. Emite la
        señal *itemToDelete* en caso de que el campo sea inválido y se deba
        quitar del QListWidget, si el item se está editando emite *itemToReset*.

        Parámetros
        ----------
        lineedit : QLineEdit
            el QLineEdit al que modificar su evento FocusOut
        item : QListWidgetItem
            el item que borrar en caso de que el campo sea inválido
        edit_mode : bool, por defecto False
            flag que determina si el item se está modificando en lugar de ser
            creado desde cero, si es True emite la señal *itemToReset* en
            lugar de *itemToDelete* cuando el campo está vacío o es inválido
        """
        super().__init__()
        self.lineedit: QLineEdit = lineedit
        self.item: QListWidgetItem = item
        self.validity: bool = None
        self.edit_mode: bool = edit_mode
        return None

    @Slot(bool)
    def setValidity(self, validity: bool | None) -> None:
        """
        Determina la validez del campo de acuerdo a los validadores.

        Parámetros
        ----------
        validity : bool | None
            validez del campo, el valor es triestado: **True**, **False** o
            **None**.
            - si es **True**: el campo es válido, el comportamiento del evento
            es el por defecto
            - si es **False**: el campo es inválido, se sobreescribe el evento
            - si es **None**: el campo es inválido y está vacío, se
            sobreescribe el evento
        """
        self.validity = validity
        return None

    def fieldIsValid(self) -> bool:
        """
        Devuelve la validez del campo.

        Retorna
        -------
        bool
            la validez del campo, **True** si el campo es válido o **False**
            si el campo es inválido (es decir, si es **False** o **None**)
        """
        return True if self.validity else False

    def eventFilter(self, watched: QLineEdit, event: QEvent):
        if event.type() == QEvent.Type.FocusOut and not self.fieldIsValid():
            match self.edit_mode:
                case True:
                    self.itemToReset.emit(self.item)

                case False:
                    self.itemToDelete.emit(self.item)

        return super().eventFilter(watched, event)


class CategoryListEventFilter(QObject):
    """
    Filtro de eventos usado para mostrar un menú contextual personalizado que
    permite al usuario cambiar el nombre de la categoría o su descripción.
    """

    nameAboutToChange: Signal = Signal(QListWidgetItem)
    descAboutToChange: Signal = Signal(QListWidgetItem)

    def eventFilter(self, watched: QListWidget, event: QEvent):
        if event.type() == QEvent.Type.ContextMenu:
            menu: QMenu = QMenu()

            change_name: QAction = menu.addAction("cambiar nombre...")
            change_desc: QAction = menu.addAction("cambiar descripción...")

            curr_item: QListWidgetItem = watched.itemAt(event.pos())

            change_name.triggered.connect(
                lambda: self.nameAboutToChange.emit(curr_item)
            )
            change_desc.triggered.connect(
                lambda: self.descAboutToChange.emit(curr_item)
            )

            if watched.indexAt(event.pos()).isValid() and curr_item.text() not in (
                CommonCategories.SHOW_ALL.value,
                CommonCategories.MISC.value,
            ):
                change_name.setEnabled(True)
                change_desc.setEnabled(True)

            else:
                change_name.setEnabled(False)
                change_desc.setEnabled(False)

            menu.exec(event.globalPos())

        return super().eventFilter(watched, event)


class CategoryDescTextEditEventFilter(QObject):
    """
    Filtro de eventos usado para capturar los cambios de foco en el
    **QTextEdit** del **QDialog** que permite al usuario cambiar la
    descripción de la categoría.
    Al salir del foco emite la señal *focusedOut*.
    """

    focusedOut: Signal = Signal()

    def eventFilter(self, watched: QTextEdit, event: QEvent):
        if event.type() == QEvent.Type.FocusOut:
            self.focusedOut.emit()

        return super().eventFilter(watched, event)
