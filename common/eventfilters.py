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
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtCore import QObject, QEvent, Qt, QSize, Signal, Slot, QRect, QRectF
from PySide6.QtGui import QPainter, QPixmap, QAction, QFont, QFontMetricsF

from resources import rc_icons
import logging

from common.enumclasses import TablesAndListsObjName, CommonCategories

logger = logging.getLogger(__name__)


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
    MIN_ICON_SIZE:int = 30
    MAX_ICON_SIZE:int = 160
    ICON_MAX_MARGIN_FACTOR:float = 0.7 # factor de márgen máximo usado para calcular 
        # el tamaño del ícono (máximo puede ocupar un 70% del viewport). Ésto es 
        # necesario porque el margin_factor es dinámico
    SPACING_ICON_TITLE:int = 16 # espaciado entre el ícono y el título
    SPACING_TITLE_SUBTITLE:int = 6 # espaciado entre el título y el subtítulo

    def __init__(self, svg_path:str, widget: QTableView | QListWidget,
                 title_text:str, subtitle_text:str):
        """
        Dependiendo del widget muestra un fondo determinado dependiendo de si
        el widget está mostrando datos o no.
        Si hay datos en el viewport del widget los muestra, sino muestra una
        imagen de fondo propia del widget.

        Parámetros
        ----------
        svg_path : str
            path del svg a colocar de background
        widget : QTableView | QListWidget
            la vista / widget al que pintarle el background
        title_text : str
            texto a mostrar como título debajo de la imagen
        subtitle_text : str
            texto a mostrar como subtítulo debajo del título
        """
        super().__init__()
        
        self.widget: QTableView = widget
        self._svg_renderer:QSvgRenderer = QSvgRenderer(svg_path)
        self._title_text:str = title_text
        self._subtitle_text:str = subtitle_text
        
        if not self._svg_renderer.isValid():
            logger.warning(f"No se pudo cargar el SVG en {svg_path}")
        return None

    def eventFilter(self, watched: QTableView | QListWidget, event: QEvent):
        painter:QPainter
        layout:dict[str, QRectF | QFont]
        
        if event.type() == QEvent.Type.Paint:
            if watched is self.widget.viewport() and event.type() == QEvent.Type.Paint:
                model = self.widget.model()
                
                # si el widget está vacío...
                if model is None or model.rowCount() == 0:
                    painter = QPainter(self.widget.viewport())
                    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
                    painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
                    
                    layout = self._calculate_layout(painter)
                    
                    # dibuja la imagen
                    self._svg_renderer.render(painter, layout["icon_rect"])
                    
                    # escribe el texto
                    self._draw_text(painter, layout)
                    
                    painter.end()
        
        return super().eventFilter(watched, event)
    
    def _calculate_layout(self, painter:QPainter) -> dict[str, QRectF | QFont]:
        """
        Calcula todos los layouts del ícono, título y subtítulo dinámicamente 
        a partir del espacio disponible, además (debido a que se requiere 
        trabajar con tipografías para determinar el área que ocupará el texto) 
        también devuelve las tipografías usadas.
        
        Parámetros
        ----------
        painter : QPainter
            el painter usado para determinar los layouts
        
        retorna
        -------
        dict[str, QRectF | QFont]
            diccionario{*"icon_rect"*: área del ícono, *"title_rect"*: área 
            del título, *"subtitle_rect"*: área del subtítulo, 
            *"title_font"*: font del título,
            *"subtitle_font"*: font del subtítulo}
        """
        viewport_rect:QRect = self.widget.viewport().rect()
        text_block_data:dict[str, float] # dict("altura título": ...,
                                           # "font título": ...,
                                           # "altura subtítulo": ...,
                                           # "font subtítulo": ...,
                                           # "altura texto": ...)
        available_for_icon:float
        icon_size:dict[str, float] # tamaño real del ícono: dict("ancho": ...,
                                                               # "altura": ...)
        total_block_height:float
        block_top:float
        icon_rect:QRectF
        title_top:float
        title_rect:QRectF
        subtitle_top:float
        subtitle_rect:QRectF
        
        # 1: mide la altura del texto (tamaño fijo, no depende del viewport)
        text_block_data = self._get_text_block_data(
            painter=painter,
            viewport_rect=viewport_rect
        )
        
        # 2: calcular espacio disponible para el ícono
        available_for_icon = self._calculate_icon_available_size(
            viewport_rect=viewport_rect,
            text_height=text_block_data["text_height"]
        )
        
        # 3: determinar tamaño del ícono (el menor entre lo "ideal" y lo disponible)
        icon_size = self._get_icon_size(
            viewport_rect=viewport_rect,
            h_available_for_icon=available_for_icon
        )
        
        # 4: posicionar todo el bloque (ícono + texto) centrado verticalmente
        total_block_height = (icon_size["height"] + self.SPACING_ICON_TITLE 
                              + text_block_data["text_height"])
        block_top = viewport_rect.center().y() - total_block_height / 2
        
        icon_rect = QRectF(
            viewport_rect.center().x() - icon_size["width"] / 2,
            block_top,
            icon_size["width"],
            icon_size["height"]
        )
        
        title_top = icon_rect.bottom() + self.SPACING_ICON_TITLE
        title_rect = QRectF(
            viewport_rect.left(),
            title_top,
            viewport_rect.width(),
            text_block_data["title_height"]
        )
        
        subtitle_top = title_rect.bottom() + self.SPACING_TITLE_SUBTITLE
        subtitle_rect = QRectF(
            viewport_rect.left(),
            subtitle_top,
            viewport_rect.width(),
            text_block_data["subtitle_height"]
        )
        return {
            "icon_rect": icon_rect,
            "title_rect": title_rect,
            "subtitle_rect": subtitle_rect,
            "title_font": text_block_data["title_font"],
            "subtitle_font": text_block_data["subtitle_font"]
        }

    def _get_text_block_data(self, painter:QPainter, viewport_rect:QRect) -> dict[str, float]:
        """
        Calcula la altura fija del bloque de texto (título y subtítulo) y 
        determina la tipografía del título y subtítulo.
        
        Parámetros
        ----------
        painter : QPainter
            el painter usado para dibujar el texto
        viewport_rect : QRect
            el área del viewport
        
        Retorna
        -------
        dict[str, float]
            dict{*"title_height"*: altura de título, *"title_font"*: font 
            del título, *"subtitle_height"*: altura de subtítulo, 
            *"subtitle_font"*: font del subtítulo, *"text_height"*: altura de texto}
        """
        # título
        title_font:QFont = painter.font()
        title_font.setPointSize(17)
        title_font.setBold(True)
        
        title_metrics:QFontMetricsF = QFontMetricsF(title_font)
        title_height:float = title_metrics.boundingRect(
            QRect(0, 0, viewport_rect.width(), 0),
            Qt.AlignmentFlag.AlignHCenter | Qt.TextFlag.TextWordWrap,
            self._title_text
        ).height()
        
        # subtítulo
        subtitle_font:QFont = painter.font()
        subtitle_font.setPointSize(15)
        subtitle_font.setBold(False)
        
        subtitle_metrics:QFontMetricsF = QFontMetricsF(subtitle_font)
        subtitle_height:float = subtitle_metrics.boundingRect(
            QRect(0, 0, viewport_rect.width(), 0),
            Qt.AlignmentFlag.AlignHCenter | Qt.TextFlag.TextWordWrap,
            self._subtitle_text
        ).height()
         
        return {
            "title_height": title_height,
            "title_font": title_font,
            "subtitle_height": subtitle_height,
            "subtitle_font": subtitle_font,
            "text_height": title_height + self.SPACING_TITLE_SUBTITLE + subtitle_height}
    
    def _calculate_icon_available_size(self, viewport_rect:QRect, text_height:float) -> float:
        
        """
        Calcula la altura disponible para el ícono.
        
        Parámetros
        ----------
        viewport_rect : QRect
            el área del viewport
        text_height : float
            el área ocupada por el bloque de texto
        
        Retorna
        -------
        float
            el tamaño disponible para el ícono
        """
        available_for_icon:float = (
            viewport_rect.height()
            - text_height
            - self.SPACING_ICON_TITLE)
        
        return max(available_for_icon, self.MIN_ICON_SIZE)

    def _get_icon_size(self, viewport_rect:QRect, h_available_for_icon:float) -> dict[str, float]:
        """
        Determina el tamaño real del ícono a partir del espacio disponible.
        
        Parámetros
        ----------
        viewport_rect : QRect
            el área del viewport
        h_available_for_icon : float
            la altura disponible para el ícono
        
        Retorna
        -------
        dict[str, float]
            dict("width": ..., "height": ...) con el ancho y la altura del ícono

        """
        default_size:QSize
        aspect:float
        ideal_icon_h:float
        icon_w:float
        icon_h:float
        max_icon_w:float
        
        default_size = self._svg_renderer.defaultSize()
        aspect = (default_size.width() / default_size.height()
                  if not default_size.isEmpty() else 1.0)
        
        ideal_icon_h = viewport_rect.height() * self.ICON_MAX_MARGIN_FACTOR
        
        # si el ideal no entra en el espacio disponible se reduce
        icon_h = min(ideal_icon_h, h_available_for_icon)
        icon_h = min(icon_h, self.MAX_ICON_SIZE)
        icon_h = max(icon_h, self.MIN_ICON_SIZE) # pero nunca por debajo del mínimo
        icon_w = icon_h * aspect
        
        # respetamos el ancho del viewport
        max_icon_w = viewport_rect.width() * self.ICON_MAX_MARGIN_FACTOR
        if icon_w > max_icon_w:
            icon_w = max_icon_w
            icon_h = icon_w / aspect
        return {"width": icon_w, "height": icon_h}

    def _draw_text(self, painter:QPainter, layout:dict[str, QRectF | float]) -> None:
        """
        Dibuja el texto debajo de la imagen.
        **NOTA: Éste método tiene en consideración la tipografía usada en 
        el programa para dibujar el texto.**
        
        Parámetros
        ----------
        painter : QPainter
            el painter usado para dibujar el texto
        layout : dict[str, QRectF | QFont]
            las zonas donde dibujar el texto y sus tipografías
        """
        # título
        painter.setPen(Qt.GlobalColor.gray)
        
        painter.setFont(layout["title_font"])
        painter.drawText(
            layout["title_rect"],
            Qt.AlignmentFlag.AlignHCenter,
            self._title_text
        )
        
        # subtítulo
        painter.setFont(layout["subtitle_font"])
        painter.drawText(
            layout["subtitle_rect"],
            Qt.AlignmentFlag.AlignHCenter | Qt.TextFlag.TextWordWrap,
            self._subtitle_text
        )
        return None


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
