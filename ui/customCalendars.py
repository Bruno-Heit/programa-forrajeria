"""
Éste archivo contiene las declaraciones de subclases de QCalendar usadas
en el programa.

La principal razón por la que crear calendarios personalizados es que, por
defecto, PySide no permite modificar algunas cosas de los calendarios, por
ejemplo los botones que permiten cambiar entre meses, de ahí la existencia
de este archivo.
"""

from PySide6.QtWidgets import QCalendarWidget
from PySide6.QtCore import Qt, QObject, QRect, QDate
from PySide6.QtGui import QPainter, QColor, QTextCharFormat, QBrush

from resources import rc_icons


class CustomCalendar(QCalendarWidget):
    """
    Subclase de **QCalendarWidget** creado específicamente para personalizar
    el calendario mostrado en **QDateTimeEdits** y subclases.
    """

    def __init__(self, parent: QObject = None) -> None:
        super(CustomCalendar, self).__init__()
        self.setParent(parent)

        self.setup_ui()
        return None

    def setup_ui(self) -> None:
        self.setHorizontalHeaderFormat(self.HorizontalHeaderFormat.ShortDayNames)
        self.setVerticalHeaderFormat(self.VerticalHeaderFormat.ISOWeekNumbers)

        self.setFirstDayOfWeek(Qt.DayOfWeek.Monday)

        # formato de texto del header de los días
        _header_format = QTextCharFormat()
        _header_format.setBackground(QColor(65, 90, 119))
        _header_format.setForeground(QColor(255, 255, 255))
        self.setHeaderTextFormat(_header_format)

        # estilos de botones
        self.setStyleSheet(
            """
            /* barra de navegación superior */
            QCalendarWidget QWidget#qt_calendar_navigationbar {
                background-color: #fff;
            }
            
            
            /* menú del botón de meses */
            QCalendarWidget QWidget#qt_calendar_navigationbar QMenu {
                background-color: #fff;
                color: #111;
                selection-background-color: #3b66ab;
                selection-color: #fff;
            }
            
            
            /* botones de mes anterior y posterior */
            QCalendarWidget QToolButton#qt_calendar_prevmonth,
            QCalendarWidget QToolButton#qt_calendar_nextmonth {
                width: 20px;
                height: 20px;
            }
            QCalendarWidget QToolButton#qt_calendar_prevmonth {
                qproperty-icon: url(":/icons/prev-month.svg");
            }
            QCalendarWidget QToolButton#qt_calendar_nextmonth {
                qproperty-icon: url(":/icons/next-month.svg");
            }
            
            
            /* toolbutton de mes */
            QCalendarWidget QToolButton#qt_calendar_monthbutton {
                min-width: 200px;
            }
            QCalendarWidget QToolButton#qt_calendar_monthbutton::menu-indicator {
                image: url(":icons/chevron-down.svg");
                subcontrol-origin: padding;
                subcontrol-position: bottom right;
            }
            QCalendarWidget QToolButton#qt_calendar_monthbutton::menu-indicator:pressed, 
            QCalendarWidget QToolButton#qt_calendar_monthbutton::menu-indicator:open {
                position: relative;
                top: 2px;
                left: 2px;
            }
            
            
            /* toolbutton de año */
            QCalendarWidget QToolButton#qt_calendar_yearbutton,
            QCalendarWidget QWidget#qt_calendar_navigationbar QSpinBox {
                min-width: 100px;
            }
            
            
            /* spinbox de año */
            QCalendarWidget QSpinBox#qt_calendar_yearedit {
                padding-left: 15px;
                border-width: 3px;
                background-color: #fff;
                color: #111;
            }
            QCalendarWidget QSpinBox#qt_calendar_yearedit::up-button {
                subcontrol-origin: border;
                subcontrol-position: top right;
                width: 16px;
                border-image: url(":icons/chevron-up.svg");
                border-width: 1px;
            }
            QCalendarWidget QSpinBox#qt_calendar_yearedit::down-button {
                subcontrol-origin: border;
                subcontrol-position: bottom right;
                width: 16px;
                border-image: url(":icons/chevron-down.svg");
                border-width: 1px;
                border-top-width: 0;
            }
            """
        )
        return None

    def dateIsValid(self, date: QDate) -> bool:
        """
        Determina si la fecha está dentro del rango permitido.

        Parámetros
        ----------
        date : QDate
            la fecha actual

        Retorna
        -------
        bool
            flag que determina la validez de la fecha
        """
        return self.minimumDate() <= date <= self.maximumDate()

    def paintCell(self, painter: QPainter, rect: QRect, date: QDate):
        _text_color: QColor = QColor(246, 87, 85)

        if not self.dateIsValid(date):
            painter.save()

            # pinta el background
            painter.fillRect(rect, QBrush(QColor(200, 200, 200)))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRect(rect)

            # pinta el texto
            painter.setPen(_text_color)
            painter.drawText(
                rect,
                Qt.TextFlag.TextSingleLine | Qt.AlignmentFlag.AlignCenter,
                f"{date.day()}",
            )

            painter.restore()

        else:
            match date.dayOfWeek():
                case 7:  # domingo
                    painter.save()
                    painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
                    painter.setRenderHint(QPainter.RenderHint.TextAntialiasing, True)

                    # pinta el background
                    painter.setBrush(QColor(224, 225, 221))
                    painter.setPen(Qt.PenStyle.NoPen)  # sin borde
                    painter.drawRect(rect)

                    # pinta el texto
                    painter.setPen(_text_color)
                    painter.drawText(
                        rect,
                        Qt.TextFlag.TextSingleLine | Qt.AlignmentFlag.AlignCenter,
                        f"{date.day()}",
                    )

                    painter.restore()

                case _:
                    return super().paintCell(painter, rect, date)
