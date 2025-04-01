'''
    Éste archivo contiene las declaraciones de los filtros de eventos 
    personalizados usados en el programa.
    El principal uso de esos eventos es para recibir los eventos tipo 
    "Paint" y pintar sobre las tablas o listas dependiendo de si están 
    vacías o no.
'''

from PySide6.QtWidgets import (QTableView, QListWidget)
from PySide6.QtCore import (QObject, QEvent, Qt, QSize)
from PySide6.QtGui import (QPainter, QPixmap)

from resources import (rc_icons)

from utils.enumclasses import (TablesAndListsObjName)


class BackgroundEventFilter(QObject):
    '''
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
    '''
    def __init__(self, widget:QTableView | QListWidget):
        '''
        Dependiendo del widget muestra un fondo determinado dependiendo de si 
        el widget está mostrando datos o no.
        Si hay datos en el viewport del widget los muestra, sino muestra una 
        imagen de fondo propia del widget.

        Parámetros
        ----------
        widget : QTableView | QListWidget
            la vista / widget al que pintarle el background
        '''
        super().__init__()
        self.widget:QTableView = widget
        
        self.pixmap:QPixmap
        self.__max_pixmap_size:QSize
        
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


    def eventFilter(self, watched:QTableView | QListWidget, event:QEvent):
        painter:QPainter
        target_size:QSize
        
        if event.type() == QEvent.Type.Paint:
            # Deja que se pinte la tabla normalmente
            result = super().eventFilter(watched, event)
            
            # Si el modelo está vacío, dibuja la imagen de fondo
            if self.widget.model() is None or self.widget.model().rowCount() == 0:
                painter = QPainter(watched)
                
                # calcula el tamaño objetivo
                target_size = QSize(
                    min(watched.size().width(), self.__max_pixmap_size.width()),
                    min(watched.size().height(), self.__max_pixmap_size.height())
                )
                
                # escala la imagen
                scaled = self.pixmap.scaled(
                    target_size,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                x = (watched.width() - scaled.width()) // 2
                y = (watched.height() - scaled.height()) // 2
                
                painter.drawPixmap(x, y, scaled)
            return result
        return super().eventFilter(watched, event)
