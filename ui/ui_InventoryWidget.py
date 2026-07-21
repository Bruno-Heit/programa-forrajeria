# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'InventoryWidget.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QAbstractScrollArea, QApplication, QCheckBox,
    QComboBox, QFrame, QHBoxLayout, QHeaderView,
    QLabel, QLineEdit, QProgressBar, QPushButton,
    QSizePolicy, QTableView, QVBoxLayout, QWidget)

class Ui_InventoryWidget(object):
    def setupUi(self, InventoryWidget):
        if not InventoryWidget.objectName():
            InventoryWidget.setObjectName(u"InventoryWidget")
        InventoryWidget.resize(979, 530)
        InventoryWidget.setWindowTitle(u"InventoryWidget")
#if QT_CONFIG(tooltip)
        InventoryWidget.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.horizontalLayout = QHBoxLayout(InventoryWidget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.main_inventory_frame = QFrame(InventoryWidget)
        self.main_inventory_frame.setObjectName(u"main_inventory_frame")
        self.main_inventory_frame.setFrameShape(QFrame.Shape.NoFrame)
        self.main_inventory_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.main_inventory_frame_Hlayout = QHBoxLayout(self.main_inventory_frame)
        self.main_inventory_frame_Hlayout.setSpacing(0)
        self.main_inventory_frame_Hlayout.setObjectName(u"main_inventory_frame_Hlayout")
        self.main_inventory_frame_Hlayout.setContentsMargins(0, 0, 0, 0)
        self.inventory_display = QFrame(self.main_inventory_frame)
        self.inventory_display.setObjectName(u"inventory_display")
        self.inventory_display.setFrameShape(QFrame.Shape.StyledPanel)
        self.inventory_display.setFrameShadow(QFrame.Shadow.Raised)
        self.inventory_display_Vlayout = QVBoxLayout(self.inventory_display)
        self.inventory_display_Vlayout.setSpacing(6)
        self.inventory_display_Vlayout.setObjectName(u"inventory_display_Vlayout")
        self.inventory_display_Vlayout.setContentsMargins(0, 6, 10, 0)
        self.inventory_header = QFrame(self.inventory_display)
        self.inventory_header.setObjectName(u"inventory_header")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.inventory_header.sizePolicy().hasHeightForWidth())
        self.inventory_header.setSizePolicy(sizePolicy)
        self.inventory_header.setMaximumSize(QSize(16777215, 16777215))
        self.inventory_header.setFrameShape(QFrame.Shape.NoFrame)
        self.inventory_header.setFrameShadow(QFrame.Shadow.Plain)
        self.inventory_header_Hlayout = QHBoxLayout(self.inventory_header)
        self.inventory_header_Hlayout.setSpacing(7)
        self.inventory_header_Hlayout.setObjectName(u"inventory_header_Hlayout")
        self.inventory_header_Hlayout.setContentsMargins(10, 5, 10, 20)
        self.inventory_searchBar = QLineEdit(self.inventory_header)
        self.inventory_searchBar.setObjectName(u"inventory_searchBar")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.inventory_searchBar.sizePolicy().hasHeightForWidth())
        self.inventory_searchBar.setSizePolicy(sizePolicy1)
        self.inventory_searchBar.setMinimumSize(QSize(150, 25))
        self.inventory_searchBar.setMaximumSize(QSize(1000, 25))
        self.inventory_searchBar.setBaseSize(QSize(0, 0))
        self.inventory_searchBar.setAcceptDrops(False)
#if QT_CONFIG(tooltip)
        self.inventory_searchBar.setToolTip(u"<html><head/><body><p><span style=\" font-size:12pt;\">Buscar un producto en la tabla seg\u00fan su nombre, caracter\u00edsticas, palabras claves, etc.</span></p></body></html>")
#endif // QT_CONFIG(tooltip)
        self.inventory_searchBar.setText(u"")
        self.inventory_searchBar.setMaxLength(255)
        self.inventory_searchBar.setFrame(False)
        self.inventory_searchBar.setEchoMode(QLineEdit.EchoMode.Normal)
        self.inventory_searchBar.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.inventory_searchBar.setPlaceholderText(u"Buscar productos por nombre, precio, stock...")
        self.inventory_searchBar.setCursorMoveStyle(Qt.CursorMoveStyle.LogicalMoveStyle)
        self.inventory_searchBar.setClearButtonEnabled(True)

        self.inventory_header_Hlayout.addWidget(self.inventory_searchBar)

        self.cb_inventory_colsFilter = QComboBox(self.inventory_header)
        self.cb_inventory_colsFilter.addItem(u"Todas")
        self.cb_inventory_colsFilter.addItem(u"Categor\u00eda")
        self.cb_inventory_colsFilter.addItem(u"Nombre de producto")
        self.cb_inventory_colsFilter.addItem(u"Descripci\u00f3n")
        self.cb_inventory_colsFilter.addItem(u"Stock")
        self.cb_inventory_colsFilter.addItem(u"Precio normal")
        self.cb_inventory_colsFilter.addItem(u"Precio comercial")
        self.cb_inventory_colsFilter.setObjectName(u"cb_inventory_colsFilter")
        sizePolicy1.setHeightForWidth(self.cb_inventory_colsFilter.sizePolicy().hasHeightForWidth())
        self.cb_inventory_colsFilter.setSizePolicy(sizePolicy1)
        self.cb_inventory_colsFilter.setMinimumSize(QSize(60, 26))
        self.cb_inventory_colsFilter.setMaximumSize(QSize(350, 26))
#if QT_CONFIG(tooltip)
        self.cb_inventory_colsFilter.setToolTip(u"<html><head/><body><p><span style=\" font-size:12pt;\">Permite seleccionar qu\u00e9 columna filtrar.</span></p></body></html>")
#endif // QT_CONFIG(tooltip)
        self.cb_inventory_colsFilter.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
        self.cb_inventory_colsFilter.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)
        self.cb_inventory_colsFilter.setIconSize(QSize(24, 24))
        self.cb_inventory_colsFilter.setFrame(False)

        self.inventory_header_Hlayout.addWidget(self.cb_inventory_colsFilter, 0, Qt.AlignmentFlag.AlignLeft)

        self.inventory_header_Hlayout.setStretch(0, 3)
        self.inventory_header_Hlayout.setStretch(1, 1)

        self.inventory_display_Vlayout.addWidget(self.inventory_header)

        self.inventory_progressbar = QProgressBar(self.inventory_display)
        self.inventory_progressbar.setObjectName(u"inventory_progressbar")
        self.inventory_progressbar.setMinimumSize(QSize(0, 12))
        self.inventory_progressbar.setMaximumSize(QSize(16777215, 12))
        self.inventory_progressbar.setValue(24)
        self.inventory_progressbar.setTextVisible(False)
        self.inventory_progressbar.setFormat(u"%p%")

        self.inventory_display_Vlayout.addWidget(self.inventory_progressbar)

        self.tv_inventory_data = QTableView(self.inventory_display)
        self.tv_inventory_data.setObjectName(u"tv_inventory_data")
#if QT_CONFIG(tooltip)
        self.tv_inventory_data.setToolTip(u"<html><head/><body><p><span style=\" font-size:12pt;\">Para </span><span style=\" font-size:12pt; text-decoration: underline;\">modificar</span><span style=\" font-size:12pt;\"> las </span><span style=\" font-size:12pt; text-decoration: underline;\">caracter\u00edsticas</span><span style=\" font-size:12pt;\"> de un producto, simplemente hacer </span><span style=\" font-size:12pt; font-style:italic;\">doble click</span><span style=\" font-size:12pt;\"> sobre la celda que se quiere modificar e ingresar el nuevo valor.</span></p></body></html>")
#endif // QT_CONFIG(tooltip)
        self.tv_inventory_data.setFrameShape(QFrame.Shape.NoFrame)
        self.tv_inventory_data.setFrameShadow(QFrame.Shadow.Plain)
        self.tv_inventory_data.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.tv_inventory_data.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.tv_inventory_data.setEditTriggers(QAbstractItemView.EditTrigger.DoubleClicked)
        self.tv_inventory_data.setProperty("showDropIndicator", False)
        self.tv_inventory_data.setDragDropOverwriteMode(False)
        self.tv_inventory_data.setAlternatingRowColors(True)
        self.tv_inventory_data.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.tv_inventory_data.setTextElideMode(Qt.TextElideMode.ElideMiddle)
        self.tv_inventory_data.setGridStyle(Qt.PenStyle.SolidLine)
        self.tv_inventory_data.setSortingEnabled(False)
        self.tv_inventory_data.setWordWrap(True)
        self.tv_inventory_data.setCornerButtonEnabled(False)
        self.tv_inventory_data.horizontalHeader().setMinimumSectionSize(50)
        self.tv_inventory_data.verticalHeader().setVisible(False)

        self.inventory_display_Vlayout.addWidget(self.tv_inventory_data)

        self.label_feedbackInventory = QLabel(self.inventory_display)
        self.label_feedbackInventory.setObjectName(u"label_feedbackInventory")
        self.label_feedbackInventory.setText(u"")
        self.label_feedbackInventory.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_feedbackInventory.setWordWrap(True)
        self.label_feedbackInventory.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        self.inventory_display_Vlayout.addWidget(self.label_feedbackInventory)

        self.tab1_buttons_2 = QFrame(self.inventory_display)
        self.tab1_buttons_2.setObjectName(u"tab1_buttons_2")
        self.tab1_buttons_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.tab1_buttons_2.setFrameShadow(QFrame.Shadow.Raised)
        self.tab1_buttons_Hlayout = QHBoxLayout(self.tab1_buttons_2)
        self.tab1_buttons_Hlayout.setObjectName(u"tab1_buttons_Hlayout")
        self.tab1_buttons_Hlayout.setContentsMargins(0, 0, 0, 0)
        self.btn_add_product_inventory = QPushButton(self.tab1_buttons_2)
        self.btn_add_product_inventory.setObjectName(u"btn_add_product_inventory")
        self.btn_add_product_inventory.setMinimumSize(QSize(180, 25))
        self.btn_add_product_inventory.setMaximumSize(QSize(250, 25))
#if QT_CONFIG(tooltip)
        self.btn_add_product_inventory.setToolTip(u"<html><head/><body><p><span style=\" font-size:12pt;\">A\u00f1adir un producto nuevo a la lista de productos actual (</span><span style=\" font-size:12pt; font-style:italic;\">+</span><span style=\" font-size:12pt;\">). </span></p></body></html>")
#endif // QT_CONFIG(tooltip)
        self.btn_add_product_inventory.setText(u"Nuevo producto")
        self.btn_add_product_inventory.setIconSize(QSize(24, 24))
#if QT_CONFIG(shortcut)
        self.btn_add_product_inventory.setShortcut(u"+")
#endif // QT_CONFIG(shortcut)
        self.btn_add_product_inventory.setCheckable(True)

        self.tab1_buttons_Hlayout.addWidget(self.btn_add_product_inventory)

        self.btn_delete_product_inventory = QPushButton(self.tab1_buttons_2)
        self.btn_delete_product_inventory.setObjectName(u"btn_delete_product_inventory")
        self.btn_delete_product_inventory.setEnabled(False)
        self.btn_delete_product_inventory.setMinimumSize(QSize(180, 23))
        self.btn_delete_product_inventory.setMaximumSize(QSize(250, 23))
#if QT_CONFIG(tooltip)
        self.btn_delete_product_inventory.setToolTip(u"<html><head/><body><p><span style=\" font-size:12pt;\">Borra el producto actualmente seleccionado (</span><span style=\" font-size:12pt; font-style:italic;\">supr</span><span style=\" font-size:12pt;\">).</span></p><p><span style=\" font-size:12pt;\">\u00c9sta acci\u00f3n elimina la </span><span style=\" font-size:12pt; text-decoration: underline;\">referencia al producto</span><span style=\" font-size:12pt;\">, no el producto como tal.</span></p><p><span style=\" font-size:12pt; font-weight:600; text-decoration: underline;\">IMPORTANTE</span><span style=\" font-size:12pt; font-weight:600;\">: esta acci\u00f3n no se puede deshacer, debe estar seguro de querer eliminar un producto.</span></p></body></html>")
#endif // QT_CONFIG(tooltip)
        self.btn_delete_product_inventory.setStyleSheet(u"")
        self.btn_delete_product_inventory.setText(u"Eliminar producto")
        self.btn_delete_product_inventory.setIconSize(QSize(24, 24))
#if QT_CONFIG(shortcut)
        self.btn_delete_product_inventory.setShortcut(u"Del")
#endif // QT_CONFIG(shortcut)
        self.btn_delete_product_inventory.setCheckable(True)

        self.tab1_buttons_Hlayout.addWidget(self.btn_delete_product_inventory)


        self.inventory_display_Vlayout.addWidget(self.tab1_buttons_2)


        self.main_inventory_frame_Hlayout.addWidget(self.inventory_display)

        self.inventory_sideBar = QFrame(self.main_inventory_frame)
        self.inventory_sideBar.setObjectName(u"inventory_sideBar")
        self.inventory_sideBar.setEnabled(True)
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.inventory_sideBar.sizePolicy().hasHeightForWidth())
        self.inventory_sideBar.setSizePolicy(sizePolicy2)
        self.inventory_sideBar.setMinimumSize(QSize(40, 0))
        self.inventory_sideBar.setMaximumSize(QSize(40, 16777215))
#if QT_CONFIG(tooltip)
        self.inventory_sideBar.setToolTip(u"<html><head/><body><p><span style=\" font-size:12pt;\">\u00c9ste men\u00fa lateral permite cambiar precios usando porcentajes, para eso se sigue el siguiente procedimiento (es necesario mantener el men\u00fa lateral abierta durante el proceso):</span></p><p><span style=\" font-size:12pt; font-weight:700;\">1)</span><span style=\" font-size:12pt;\"> Seleccionar el </span><span style=\" font-size:12pt; font-weight:700;\">tipo de precio</span><span style=\" font-size:12pt;\"> que se desea modificar dentro del men\u00fa</span></p><p><span style=\" font-size:12pt; font-weight:700;\">2)</span><span style=\" font-size:12pt;\"> Seleccionar los </span><span style=\" font-size:12pt; font-weight:700;\">productos</span><span style=\" font-size:12pt;\"> a modificar en la tabla</span></p><p><span style=\" font-size:12pt; font-weight:700;\">3)</span><span style=\" font-size:12pt;\"> Escribir el </span><span style=\" font-size:12pt; font-weight:700;\">porcentaje de cambio</span><span style=\" font-size:12pt;\"> en la barra in"
                        "ferior del men\u00fa y presionar </span><span style=\" font-size:12pt; font-style:italic;\">Enter</span></p><p><br/></p><p><span style=\" font-size:12pt;\">De esa forma se cambia el precio elegido de todos los </span><span style=\" font-size:12pt; font-weight:700;\">productos seleccionados </span><span style=\" font-size:12pt;\">y tambi\u00e9n se actualizan las </span><span style=\" font-size:12pt; font-weight:700;\">cuentas corrientes</span><span style=\" font-size:12pt;\"> con los nuevos valores.</span></p></body></html>")
#endif // QT_CONFIG(tooltip)
        self.inventory_sideBar.setStyleSheet(u"* {\n"
"	background-color: #0d1b2a;\n"
"	color: #e0e1dd;\n"
"}\n"
"\n"
"\n"
"QToolTip {\n"
"	background-color: #fff;\n"
"	color: #0d1b2a;\n"
"}\n"
"\n"
"\n"
"#inventory_sideBar {\n"
"	border-bottom-left-radius: 20px;\n"
"}\n"
"\n"
"QScrollBar {\n"
"	background-color: white;\n"
"}\n"
"\n"
"\n"
"/* botones */\n"
"QPushButton {\n"
"	border: none;\n"
"}\n"
"QPushButton:hover {\n"
"	border: 2px solid #38a3a5;\n"
"	border-radius: 3px;\n"
"	border-bottom-right-radius: 10px;\n"
"	padding-right: 2px;\n"
"	padding-bottom: 3px;\n"
"}\n"
"\n"
"\n"
"/* labels */\n"
"QLabel {\n"
"	font-family: \"Arial\", \"Calibri\", \"Sans-Serif\";\n"
"	font-size: 18px;\n"
"	font-weight: 600px;\n"
"	margin-bottom: 5px;\n"
"}\n"
"\n"
"\n"
"#percentage_label {\n"
"	margin-top: 25px;\n"
"	margin-bottom: 0;\n"
"}\n"
"\n"
"\n"
"/* lineedit */\n"
"QLineEdit {\n"
"	background-color: #e0e1dd;\n"
"	color: #0d1b2a;\n"
"	border: none;\n"
"	border-top: 1px solid;\n"
"	border-bottom: 1px solid;\n"
"	border-color: #0b7e7f;\n"
"	border-radius: 10px;\n"
""
                        "	height: 24px;\n"
"}\n"
"QLineEdit:focus {\n"
"	background-color: #3b66ab;\n"
"	color: #fff;\n"
"	border: 1px solid;\n"
"	border-color: #0b7e7f;\n"
"	font-size: 18px;\n"
"}\n"
"QLineEdit:disabled {\n"
"	background-color: #bbb;\n"
"	color: #555;\n"
"}\n"
"\n"
"\n"
"/* checkbuttons */\n"
"")
        self.inventory_sideBar.setFrameShape(QFrame.Shape.NoFrame)
        self.inventory_sideBar.setFrameShadow(QFrame.Shadow.Raised)
        self.inventory_sideBar_Vlayout = QVBoxLayout(self.inventory_sideBar)
        self.inventory_sideBar_Vlayout.setSpacing(15)
        self.inventory_sideBar_Vlayout.setObjectName(u"inventory_sideBar_Vlayout")
        self.inventory_sideBar_Vlayout.setContentsMargins(0, 5, 0, 18)
        self.btn_inventory_sideBarToggle = QPushButton(self.inventory_sideBar)
        self.btn_inventory_sideBarToggle.setObjectName(u"btn_inventory_sideBarToggle")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.btn_inventory_sideBarToggle.sizePolicy().hasHeightForWidth())
        self.btn_inventory_sideBarToggle.setSizePolicy(sizePolicy3)
        self.btn_inventory_sideBarToggle.setMinimumSize(QSize(0, 0))
        self.btn_inventory_sideBarToggle.setMaximumSize(QSize(16777215, 16777215))
        self.btn_inventory_sideBarToggle.setIconSize(QSize(32, 32))
        self.btn_inventory_sideBarToggle.setCheckable(True)

        self.inventory_sideBar_Vlayout.addWidget(self.btn_inventory_sideBarToggle, 0, Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)

        self.inventory_side_bar_body = QFrame(self.inventory_sideBar)
        self.inventory_side_bar_body.setObjectName(u"inventory_side_bar_body")
        self.inventory_side_bar_body.setMinimumSize(QSize(0, 0))
        self.inventory_side_bar_body.setFrameShape(QFrame.Shape.NoFrame)
        self.inventory_side_bar_body.setFrameShadow(QFrame.Shadow.Plain)
        self.inventory_side_bar_body_Vlayout = QVBoxLayout(self.inventory_side_bar_body)
        self.inventory_side_bar_body_Vlayout.setSpacing(35)
        self.inventory_side_bar_body_Vlayout.setObjectName(u"inventory_side_bar_body_Vlayout")
        self.inventory_side_bar_body_Vlayout.setContentsMargins(8, 5, 8, 0)
        self.inventory_sideBar_label_changePrices = QLabel(self.inventory_side_bar_body)
        self.inventory_sideBar_label_changePrices.setObjectName(u"inventory_sideBar_label_changePrices")
        self.inventory_sideBar_label_changePrices.setText(u"Cambios porcentuales de precios")
        self.inventory_sideBar_label_changePrices.setTextFormat(Qt.TextFormat.PlainText)
        self.inventory_sideBar_label_changePrices.setScaledContents(False)
        self.inventory_sideBar_label_changePrices.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.inventory_sideBar_label_changePrices.setWordWrap(True)
        self.inventory_sideBar_label_changePrices.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        self.inventory_side_bar_body_Vlayout.addWidget(self.inventory_sideBar_label_changePrices)

        self.change_percentage_frame = QFrame(self.inventory_side_bar_body)
        self.change_percentage_frame.setObjectName(u"change_percentage_frame")
        self.change_percentage_frame.setFrameShape(QFrame.Shape.NoFrame)
        self.change_percentage_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.change_percentage_frame_Vlayout = QVBoxLayout(self.change_percentage_frame)
        self.change_percentage_frame_Vlayout.setSpacing(25)
        self.change_percentage_frame_Vlayout.setObjectName(u"change_percentage_frame_Vlayout")
        self.change_percentage_frame_Vlayout.setContentsMargins(0, 5, 0, 5)
        self.checkbox_unit_prices = QCheckBox(self.change_percentage_frame)
        self.checkbox_unit_prices.setObjectName(u"checkbox_unit_prices")
#if QT_CONFIG(tooltip)
        self.checkbox_unit_prices.setToolTip(u"<html><head/><body><p><span style=\" font-size:12pt; color:#000000;\">Cambia el </span><span style=\" font-size:12pt; text-decoration: underline; color:#000000;\">precio normal</span><span style=\" font-size:12pt; color:#000000;\"> de los productos seleccionados.</span></p></body></html>")
#endif // QT_CONFIG(tooltip)
        self.checkbox_unit_prices.setText(u"Precios normales")
        self.checkbox_unit_prices.setIconSize(QSize(24, 24))

        self.change_percentage_frame_Vlayout.addWidget(self.checkbox_unit_prices)

        self.checkbox_comercial_prices = QCheckBox(self.change_percentage_frame)
        self.checkbox_comercial_prices.setObjectName(u"checkbox_comercial_prices")
#if QT_CONFIG(tooltip)
        self.checkbox_comercial_prices.setToolTip(u"<html><head/><body><p><span style=\" font-size:12pt; color:#000000;\">Cambia el </span><span style=\" font-size:12pt; text-decoration: underline; color:#000000;\">precio comercial</span><span style=\" font-size:12pt; color:#000000;\"> de los productos seleccionados.</span></p></body></html>")
#endif // QT_CONFIG(tooltip)
        self.checkbox_comercial_prices.setText(u"Precios comerciales")
        self.checkbox_comercial_prices.setIconSize(QSize(24, 24))

        self.change_percentage_frame_Vlayout.addWidget(self.checkbox_comercial_prices)

        self.percentage_label = QLabel(self.change_percentage_frame)
        self.percentage_label.setObjectName(u"percentage_label")
#if QT_CONFIG(tooltip)
        self.percentage_label.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.percentage_label.setText(u"Porcentaje")
        self.percentage_label.setTextFormat(Qt.TextFormat.PlainText)
        self.percentage_label.setAlignment(Qt.AlignmentFlag.AlignBottom|Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft)
        self.percentage_label.setWordWrap(True)
        self.percentage_label.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        self.change_percentage_frame_Vlayout.addWidget(self.percentage_label)

        self.lineEdit_percentage_change = QLineEdit(self.change_percentage_frame)
        self.lineEdit_percentage_change.setObjectName(u"lineEdit_percentage_change")
        self.lineEdit_percentage_change.setEnabled(False)
        self.lineEdit_percentage_change.setAcceptDrops(False)
#if QT_CONFIG(tooltip)
        self.lineEdit_percentage_change.setToolTip(u"<html><head/><body><p><span style=\" font-size:12pt; color:#000000;\">Aumenta o disminuye un cierto porcentaje los precios normales/comerciales seleccionados.</span></p><p><span style=\" font-size:12pt; font-weight:600; color:#000000;\">EJ.: </span><span style=\" font-size:12pt; color:#000000;\">Para aumentar un 25% un valor introducir &quot;25&quot;, para disminuir el precio un 25% introducir &quot;-25&quot;.</span></p></body></html>")
#endif // QT_CONFIG(tooltip)
        self.lineEdit_percentage_change.setStyleSheet(u"")
        self.lineEdit_percentage_change.setText(u"")
        self.lineEdit_percentage_change.setMaxLength(12)
        self.lineEdit_percentage_change.setFrame(False)
        self.lineEdit_percentage_change.setPlaceholderText(u"Ejemplo: 25")
        self.lineEdit_percentage_change.setClearButtonEnabled(True)

        self.change_percentage_frame_Vlayout.addWidget(self.lineEdit_percentage_change)

        self.change_percentage_frame_Vlayout.setStretch(2, 1)
        self.change_percentage_frame_Vlayout.setStretch(3, 1)

        self.inventory_side_bar_body_Vlayout.addWidget(self.change_percentage_frame)

        self.label_feedbackChangePercentage = QLabel(self.inventory_side_bar_body)
        self.label_feedbackChangePercentage.setObjectName(u"label_feedbackChangePercentage")
        self.label_feedbackChangePercentage.setStyleSheet(u"font-family: \"Verdana\";\n"
"font-size: 16px;\n"
"letter-spacing: 0px;\n"
"word-spacing: 0px;\n"
"color: #111;")
        self.label_feedbackChangePercentage.setText(u"")
        self.label_feedbackChangePercentage.setTextFormat(Qt.TextFormat.PlainText)
        self.label_feedbackChangePercentage.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_feedbackChangePercentage.setWordWrap(True)

        self.inventory_side_bar_body_Vlayout.addWidget(self.label_feedbackChangePercentage)


        self.inventory_sideBar_Vlayout.addWidget(self.inventory_side_bar_body, 0, Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTop)

        self.inventory_sideBar_Vlayout.setStretch(1, 10)

        self.main_inventory_frame_Hlayout.addWidget(self.inventory_sideBar)

        self.main_inventory_frame_Hlayout.setStretch(0, 10)

        self.horizontalLayout.addWidget(self.main_inventory_frame)


        self.retranslateUi(InventoryWidget)

        QMetaObject.connectSlotsByName(InventoryWidget)
    # setupUi

    def retranslateUi(self, InventoryWidget):

        self.btn_inventory_sideBarToggle.setText("")
        pass
    # retranslateUi

