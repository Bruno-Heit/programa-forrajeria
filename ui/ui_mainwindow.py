# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QAbstractScrollArea, QAbstractSpinBox, QApplication,
    QButtonGroup, QCheckBox, QComboBox, QDateTimeEdit,
    QFrame, QGridLayout, QHBoxLayout, QHeaderView,
    QLabel, QLineEdit, QListView, QListWidget,
    QListWidgetItem, QMainWindow, QProgressBar, QPushButton,
    QSizePolicy, QSpacerItem, QTabWidget, QTableView,
    QToolBox, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setMinimumSize(QSize(750, 500))
#if QT_CONFIG(tooltip)
        MainWindow.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        MainWindow.setStyleSheet(u"* {\n"
"	color: #111;\n"
"	font-family: \"Verdana\", \"Sans-Serif\";\n"
"	font-size: 16px;\n"
"}\n"
"\n"
"\n"
"QToolTip {\n"
"	background-color: #fff;\n"
"}\n"
"\n"
"\n"
"#centralwidget,\n"
"#main_body,\n"
"#debts_info {\n"
"	background-color: #20ae7c;\n"
"}\n"
"\n"
"\n"
"QFrame, QWidget {\n"
"	border: none;\n"
"}")
        self.actionNuevo = QAction(MainWindow)
        self.actionNuevo.setObjectName(u"actionNuevo")
        self.actionAbrir = QAction(MainWindow)
        self.actionAbrir.setObjectName(u"actionAbrir")
        self.actionGuardar = QAction(MainWindow)
        self.actionGuardar.setObjectName(u"actionGuardar")
        self.actionGuardar_como = QAction(MainWindow)
        self.actionGuardar_como.setObjectName(u"actionGuardar_como")
        self.actionConfiguraci_n = QAction(MainWindow)
        self.actionConfiguraci_n.setObjectName(u"actionConfiguraci_n")
        self.actionSobre_el_programa = QAction(MainWindow)
        self.actionSobre_el_programa.setObjectName(u"actionSobre_el_programa")
        self.actionLicencia = QAction(MainWindow)
        self.actionLicencia.setObjectName(u"actionLicencia")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        font = QFont()
        font.setFamilies([u"Verdana"])
        self.centralwidget.setFont(font)
        self.centralwidget.setStyleSheet(u"QScrollBar {\n"
"	background-color: #fff;\n"
"	border: 1px solid transparent;\n"
"	border-radius: 5px;\n"
"}\n"
"QScrollBar:groove {\n"
"	border-radius: 5px;\n"
"}\n"
"QScrollBar::handle {\n"
"	background-color: #0b7e7f;\n"
"	border-radius: 5px;\n"
"}\n"
"QScrollBar::handle:pressed {\n"
"	background-color: #35bc88;\n"
"}\n"
"QScrollBar::sub-line {\n"
"	width: 0;\n"
"	height: 0;\n"
"	background: none;\n"
"}\n"
"QScrollBar::add-line {\n"
"	width: 0;\n"
"	height: 0;\n"
"	background: none;\n"
"}\n"
"\n"
"\n"
"/*vertical scrollbars*/\n"
"QScrollBar:vertical {\n"
"	width: 13px;\n"
"}\n"
"QScrollBar::handle:vertical {\n"
"	min-height: 15px;\n"
"}\n"
"QScrollBar::sub-page:vertical {\n"
"	background: none;\n"
"}\n"
"QScrollBar::add-page:vertical {\n"
"	background: none;\n"
"}\n"
"\n"
"/*horizontal scrollbars*/\n"
"QScrollBar:horizontal {\n"
"	height: 13px;\n"
"}\n"
"QScrollBar::handle:horizontal {\n"
"	min-width: 15px;\n"
"}\n"
"")
        self.centralwidget_HLayout = QHBoxLayout(self.centralwidget)
        self.centralwidget_HLayout.setSpacing(4)
        self.centralwidget_HLayout.setObjectName(u"centralwidget_HLayout")
        self.centralwidget_HLayout.setContentsMargins(0, 0, 0, 0)
        self.side_bar = QFrame(self.centralwidget)
        self.side_bar.setObjectName(u"side_bar")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.side_bar.sizePolicy().hasHeightForWidth())
        self.side_bar.setSizePolicy(sizePolicy)
        self.side_bar.setMinimumSize(QSize(40, 0))
        self.side_bar.setMaximumSize(QSize(40, 16777215))
        self.side_bar.setBaseSize(QSize(0, 0))
        self.side_bar.setStyleSheet(u"* {\n"
"	background-color: #22577a;\n"
"	color: #c7f9cc;\n"
"}\n"
"\n"
"#side_bar {\n"
"	border-bottom-right-radius: 20px;\n"
"}\n"
"\n"
"\n"
"QScrollBar {\n"
"	background-color: white;\n"
"}\n"
"\n"
"\n"
"QListWidget {\n"
"	margin-bottom: 15px;\n"
"}\n"
"\n"
"\n"
"QLabel {\n"
"	font-size: 16px;\n"
"	margin-top: 5px;\n"
"	border-bottom: 1px solid #c7f9cc;\n"
"}")
        self.side_bar.setFrameShape(QFrame.Shape.NoFrame)
        self.side_bar.setFrameShadow(QFrame.Shadow.Plain)
        self.side_bar_VLayout = QVBoxLayout(self.side_bar)
        self.side_bar_VLayout.setSpacing(8)
        self.side_bar_VLayout.setObjectName(u"side_bar_VLayout")
        self.side_bar_VLayout.setContentsMargins(0, 0, 0, 18)
        self.btn_side_barToggle = QPushButton(self.side_bar)
        self.btn_side_barToggle.setObjectName(u"btn_side_barToggle")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.btn_side_barToggle.sizePolicy().hasHeightForWidth())
        self.btn_side_barToggle.setSizePolicy(sizePolicy1)
        self.btn_side_barToggle.setMinimumSize(QSize(40, 40))
        self.btn_side_barToggle.setStyleSheet(u"QPushButton {\n"
"	border: none;\n"
"}\n"
"QPushButton:hover {\n"
"	border: 2px solid #38a3a5;\n"
"	border-radius: 3px;\n"
"	border-bottom-right-radius: 10px;\n"
"	padding-right: 2px;\n"
"	padding-bottom: 3px;\n"
"}")
        self.btn_side_barToggle.setIconSize(QSize(32, 32))

        self.side_bar_VLayout.addWidget(self.btn_side_barToggle, 0, Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)

        self.side_bar_body = QFrame(self.side_bar)
        self.side_bar_body.setObjectName(u"side_bar_body")
        sizePolicy.setHeightForWidth(self.side_bar_body.sizePolicy().hasHeightForWidth())
        self.side_bar_body.setSizePolicy(sizePolicy)
        self.side_bar_body.setFrameShape(QFrame.Shape.NoFrame)
        self.side_bar_body.setFrameShadow(QFrame.Shadow.Raised)
        self.side_bar_body_Vlayout = QVBoxLayout(self.side_bar_body)
        self.side_bar_body_Vlayout.setSpacing(4)
        self.side_bar_body_Vlayout.setObjectName(u"side_bar_body_Vlayout")
        self.side_bar_body_Vlayout.setContentsMargins(0, 0, 0, 0)
        self.label_categories = QLabel(self.side_bar_body)
        self.label_categories.setObjectName(u"label_categories")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_categories.sizePolicy().hasHeightForWidth())
        self.label_categories.setSizePolicy(sizePolicy2)
#if QT_CONFIG(tooltip)
        self.label_categories.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.label_categories.setStatusTip(u"")
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(whatsthis)
        self.label_categories.setWhatsThis(u"")
#endif // QT_CONFIG(whatsthis)
        self.label_categories.setAutoFillBackground(False)
        self.label_categories.setText(u"CATEGOR\u00cdAS")
        self.label_categories.setTextFormat(Qt.TextFormat.PlainText)
        self.label_categories.setAlignment(Qt.AlignmentFlag.AlignBottom|Qt.AlignmentFlag.AlignHCenter)
        self.label_categories.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        self.side_bar_body_Vlayout.addWidget(self.label_categories)

        self.tables_ListWidget = QListWidget(self.side_bar_body)
        __qlistwidgetitem = QListWidgetItem(self.tables_ListWidget)
        __qlistwidgetitem.setText(u"Alimentos dom\u00e9sticos");
        __qlistwidgetitem1 = QListWidgetItem(self.tables_ListWidget)
        __qlistwidgetitem1.setText(u"Alimentos de granja");
        __qlistwidgetitem2 = QListWidgetItem(self.tables_ListWidget)
        __qlistwidgetitem2.setText(u"Cereales/arroz");
        __qlistwidgetitem3 = QListWidgetItem(self.tables_ListWidget)
        __qlistwidgetitem3.setText(u"Limpieza/qu\u00edmica");
        __qlistwidgetitem4 = QListWidgetItem(self.tables_ListWidget)
        __qlistwidgetitem4.setText(u"Accesorios de pesca");
        __qlistwidgetitem5 = QListWidgetItem(self.tables_ListWidget)
        __qlistwidgetitem5.setText(u"Accesorios para mascotas");
        __qlistwidgetitem6 = QListWidgetItem(self.tables_ListWidget)
        __qlistwidgetitem6.setText(u"Accesorios para boyeros");
        __qlistwidgetitem7 = QListWidgetItem(self.tables_ListWidget)
        __qlistwidgetitem7.setText(u"Accesorios para jardiner\u00eda");
        __qlistwidgetitem8 = QListWidgetItem(self.tables_ListWidget)
        __qlistwidgetitem8.setText(u"Accesorios para piletas");
        __qlistwidgetitem9 = QListWidgetItem(self.tables_ListWidget)
        __qlistwidgetitem9.setText(u"Electrodom\u00e9sticos");
        __qlistwidgetitem10 = QListWidgetItem(self.tables_ListWidget)
        __qlistwidgetitem10.setText(u"Electr\u00f3nicos");
        __qlistwidgetitem11 = QListWidgetItem(self.tables_ListWidget)
        __qlistwidgetitem11.setText(u"Herramientas");
        __qlistwidgetitem12 = QListWidgetItem(self.tables_ListWidget)
        __qlistwidgetitem12.setText(u"Indumentaria");
        __qlistwidgetitem13 = QListWidgetItem(self.tables_ListWidget)
        __qlistwidgetitem13.setText(u"Arenas");
        __qlistwidgetitem14 = QListWidgetItem(self.tables_ListWidget)
        __qlistwidgetitem14.setText(u"Gas");
        __qlistwidgetitem15 = QListWidgetItem(self.tables_ListWidget)
        __qlistwidgetitem15.setText(u"Venenos");
        __qlistwidgetitem15.setFlags(Qt.ItemIsSelectable|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled);
        __qlistwidgetitem16 = QListWidgetItem(self.tables_ListWidget)
        __qlistwidgetitem16.setText(u"Varios");
        font1 = QFont()
        font1.setBold(True)
        font1.setUnderline(False)
        __qlistwidgetitem17 = QListWidgetItem(self.tables_ListWidget)
        __qlistwidgetitem17.setText(u"MOSTRAR TODOS");
        __qlistwidgetitem17.setFont(font1);
        self.tables_ListWidget.setObjectName(u"tables_ListWidget")
        self.tables_ListWidget.setStyleSheet(u"QListWidget {\n"
"	border: none;\n"
"}\n"
"QListWidget::item {\n"
"	font: 14pt \"Tahoma\";\n"
"}\n"
"QListWidget::item:selected {\n"
"	font-size: 15pt;\n"
"	background-color: rgb(71, 184, 255);\n"
"	border-radius: 3px;\n"
"}")
        self.tables_ListWidget.setFrameShape(QFrame.Shape.NoFrame)
        self.tables_ListWidget.setFrameShadow(QFrame.Shadow.Plain)
        self.tables_ListWidget.setLineWidth(1)
        self.tables_ListWidget.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.tables_ListWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.tables_ListWidget.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.tables_ListWidget.setEditTriggers(QAbstractItemView.EditTrigger.DoubleClicked)
        self.tables_ListWidget.setTabKeyNavigation(True)
        self.tables_ListWidget.setDragEnabled(False)
        self.tables_ListWidget.setTextElideMode(Qt.TextElideMode.ElideLeft)
        self.tables_ListWidget.setSpacing(5)
        self.tables_ListWidget.setSortingEnabled(False)

        self.side_bar_body_Vlayout.addWidget(self.tables_ListWidget)


        self.side_bar_VLayout.addWidget(self.side_bar_body)


        self.centralwidget_HLayout.addWidget(self.side_bar)

        self.main_body = QFrame(self.centralwidget)
        self.main_body.setObjectName(u"main_body")
        self.main_body.setFont(font)
        self.main_body.setFrameShape(QFrame.Shape.StyledPanel)
        self.main_body.setFrameShadow(QFrame.Shadow.Raised)
        self.main_body_VLayout = QVBoxLayout(self.main_body)
        self.main_body_VLayout.setSpacing(4)
        self.main_body_VLayout.setObjectName(u"main_body_VLayout")
        self.main_body_VLayout.setContentsMargins(0, 5, 0, 0)
        self.tabWidget = QTabWidget(self.main_body)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setFont(font)
#if QT_CONFIG(tooltip)
        self.tabWidget.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.tabWidget.setStyleSheet(u"#inventory_searchBar,\n"
"#sales_searchBar,\n"
"#debts_searchBar,\n"
"#lineEdit_paid {\n"
"	background-color: #fff;\n"
"	border: none;\n"
"	border-top: 1px solid;\n"
"	border-bottom: 1px solid;\n"
"	border-color: #0b7e7f;\n"
"	width: 400px;\n"
"}\n"
"#inventory_searchBar:focus,\n"
"#sales_searchBar:focus,\n"
"#debts_searchBar:focus,\n"
"#lineEdit_paid:focus {\n"
"	background-color: rgb(197, 255, 252);\n"
"	border: 1px solid;\n"
"	border-color: #0b7e7f;\n"
"}\n"
"\n"
"\n"
"QPushButton {\n"
"	color: #fff;\n"
"	background-color: #22577a;\n"
"	border: 1px solid #12476a;\n"
"	border-radius: 2px;\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: #38a3a5;\n"
"	border: 1px inset #289395;\n"
"}\n"
"QPushButton:pressed {\n"
"	background-color: #58c3c5;\n"
"	border: 1px inset #48b3b5;\n"
"}\n"
"QPushButton:disabled {\n"
"	background-color: rgb(103, 115, 122);\n"
"	color: #999;\n"
"}\n"
"\n"
"\n"
"QTabWidget::pane { /* selecciona la ventana, sin las pesta\u00f1as */\n"
"	border-top: 2px solid #0b7e7f;\n"
"	margin-top: "
                        "-1px;\n"
"}\n"
"QTabWidget::tab-bar {\n"
"	left: 5px;\n"
"}\n"
"\n"
"QTabBar::tab { /* selecciona la barra de las pesta\u00f1as */\n"
"	background-color: #0b7e7f;\n"
"	border: 1px solid #0b7e7f;\n"
"	margin: 0 1px;\n"
"	color: #fff;\n"
"	padding: 2px;\n"
"	width: 150px;\n"
"	height: 20px;\n"
"	font-size: 18px;\n"
"}\n"
"QTabBar::tab:hover {\n"
"	background-color: #35bc88;\n"
"	border: 1px solid #20ae7c;\n"
"}\n"
"QTabBar::tab:selected {\n"
"	margin-bottom: -1px;\n"
"	background-color: qlineargradient(spread:pad, x1:0.658, y1:1, x2:0.289, y2:0, stop:0 rgba(11, 126, 127, 255), stop:1 rgba(84, 137, 172, 255));\n"
"	border-top-color:  rgba(84, 137, 172, 255);\n"
"}\n"
"QTabBar::tab:!selected {\n"
"	margin-top: 3px;\n"
"	height: 17px;\n"
"}\n"
"\n"
"\n"
"QTableView {\n"
"	background-color: #58dfab;\n"
"	alternate-background-color: #98ffcb;\n"
"	border: 1px solid #111;\n"
"}\n"
"QTableView::item:hover {\n"
"	background-color: rgb(197, 255, 252);\n"
"}\n"
"QTableView::item:selected {\n"
"	background-color: #38a3a5;\n"
""
                        "}\n"
"QHeaderView:section {\n"
"	background-color: #fff;\n"
"	border: none;\n"
"	border-right: 1px solid;\n"
"	border-bottom: 1px solid;\n"
"	border-color: #111;\n"
"}\n"
"\n"
"\n"
"QToolBox::tab {\n"
"	background-color: #13947d;\n"
"	color: #fff;\n"
"	height: 18px;\n"
"}\n"
"QToolBox::tab:hover {\n"
"	background-color: rgb(197, 255, 252);\n"
"	color: #111;\n"
"}\n"
"QToolBox::tab:selected {\n"
"	font: italic;\n"
"	font-size: 16px;\n"
"	background-color: qlineargradient(spread:pad, x1:0.658, y1:1, x2:0.289, y2:0, stop:0 rgba(11, 126, 127, 255), stop:1 rgba(84, 137, 172, 255));\n"
"	border-top-color:  rgba(84, 137, 172, 255);\n"
"}\n"
"\n"
"\n"
"QComboBox {\n"
"	background-color: #fff;\n"
"	color: #111;\n"
"	border: none;\n"
"	border-top: 1px solid;\n"
"	border-bottom: 1px solid;\n"
"	border-color: #111;\n"
"}\n"
"QComboBox:on {\n"
"	background-color: rgb(197, 255, 252);\n"
"	border: 1px solid;\n"
"	border-color: rgb(11, 126, 127);\n"
"	padding-top: 2px;\n"
"	padding-left: 4px;\n"
"}\n"
"QComboBox QAbstractItem"
                        "View {\n"
"	background-color: #fff;\n"
"	selection-background-color: #38a3a5;\n"
"}\n"
"\n"
"\n"
"/* estilos del QDateTimeEdit y del QCalendarWidget */\n"
"QDateTimeEdit {\n"
"	background-color: #fff;\n"
"}\n"
"\n"
"\n"
"QCalendarWidget QAbstractItemView {\n"
"	background-color: #fff;\n"
"	selection-background-color: #38a3a5;\n"
"}\n"
"QCalendarWidget QToolButton {\n"
"	background-color: #22577a;\n"
"	color: #fff;\n"
"}\n"
"QCalendarWidget QToolButton:hover,\n"
"QCalendarWidget QToolButton:pressed {\n"
"	background-color: #38a3a5;\n"
"	color: #111;\n"
"}\n"
"\n"
"\n"
"/* estilos de QProgressBar */\n"
"QProgressBar {\n"
"	margin: 0 10px 0 10px;\n"
"	background-color: rgba(255, 255, 255, 0.6);\n"
"	border: None;\n"
"	border-radius: 5px;\n"
"}\n"
"QProgressBar::chunk {\n"
"	background-color: qlineargradient(spread:reflect, x1:0.119, y1:0.426, x2:0.712045, y2:0.926, stop:0.0451977 rgba(84, 137, 172, 255), stop:0.59887 rgba(71, 184, 255, 255));\n"
"	border-radius: 5px;\n"
"}")
        self.tabWidget.setTabPosition(QTabWidget.TabPosition.North)
        self.tabWidget.setTabShape(QTabWidget.TabShape.Rounded)
        self.tabWidget.setElideMode(Qt.TextElideMode.ElideMiddle)
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setMovable(True)
        self.tabWidget.setTabBarAutoHide(False)
        self.tab1_inventory = QWidget()
        self.tab1_inventory.setObjectName(u"tab1_inventory")
        self.tab1_inventory.setFont(font)
        self.tab1_inventory.setStyleSheet(u"#main_inventory_frame {\n"
"	background-color: #35bc88;\n"
"	border-color: #0b7e7f;\n"
"}")
        self.verticalLayout = QVBoxLayout(self.tab1_inventory)
        self.verticalLayout.setSpacing(4)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 5)
        self.main_inventory_frame = QFrame(self.tab1_inventory)
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
        self.inventory_display_Vlayout.setSpacing(4)
        self.inventory_display_Vlayout.setObjectName(u"inventory_display_Vlayout")
        self.inventory_display_Vlayout.setContentsMargins(0, 8, 0, 0)
        self.inventory_header = QFrame(self.inventory_display)
        self.inventory_header.setObjectName(u"inventory_header")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.inventory_header.sizePolicy().hasHeightForWidth())
        self.inventory_header.setSizePolicy(sizePolicy3)
        self.inventory_header.setFrameShape(QFrame.Shape.NoFrame)
        self.inventory_header.setFrameShadow(QFrame.Shadow.Raised)
        self.inventory_header_Hlayout = QHBoxLayout(self.inventory_header)
        self.inventory_header_Hlayout.setSpacing(4)
        self.inventory_header_Hlayout.setObjectName(u"inventory_header_Hlayout")
        self.inventory_header_Hlayout.setContentsMargins(5, 0, 5, 0)
        self.inventory_searchBar = QLineEdit(self.inventory_header)
        self.inventory_searchBar.setObjectName(u"inventory_searchBar")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.inventory_searchBar.sizePolicy().hasHeightForWidth())
        self.inventory_searchBar.setSizePolicy(sizePolicy4)
        self.inventory_searchBar.setMinimumSize(QSize(150, 25))
        self.inventory_searchBar.setMaximumSize(QSize(16777215, 25))
        self.inventory_searchBar.setBaseSize(QSize(0, 0))
        self.inventory_searchBar.setAcceptDrops(False)
#if QT_CONFIG(tooltip)
        self.inventory_searchBar.setToolTip(u"<html><head/><body><p><span style=\" font-size:12pt;\">Buscar un producto en la tabla seg\u00fan su nombre, caracter\u00edsticas, palabras claves, etc.</span></p></body></html>")
#endif // QT_CONFIG(tooltip)
        self.inventory_searchBar.setText(u"")
        self.inventory_searchBar.setMaxLength(100)
        self.inventory_searchBar.setFrame(False)
        self.inventory_searchBar.setEchoMode(QLineEdit.EchoMode.Normal)
        self.inventory_searchBar.setPlaceholderText(u"Ingresar detalles de productos a buscar...")
        self.inventory_searchBar.setCursorMoveStyle(Qt.CursorMoveStyle.LogicalMoveStyle)
        self.inventory_searchBar.setClearButtonEnabled(True)

        self.inventory_header_Hlayout.addWidget(self.inventory_searchBar, 0, Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.cb_inventory_colsFilter = QComboBox(self.inventory_header)
        self.cb_inventory_colsFilter.addItem(u"Todas")
        self.cb_inventory_colsFilter.addItem(u"Categor\u00eda")
        self.cb_inventory_colsFilter.addItem(u"Nombre de producto")
        self.cb_inventory_colsFilter.addItem(u"Descripci\u00f3n")
        self.cb_inventory_colsFilter.addItem(u"Stock")
        self.cb_inventory_colsFilter.addItem(u"Precio normal")
        self.cb_inventory_colsFilter.addItem(u"Precio comercial")
        self.cb_inventory_colsFilter.setObjectName(u"cb_inventory_colsFilter")
        sizePolicy4.setHeightForWidth(self.cb_inventory_colsFilter.sizePolicy().hasHeightForWidth())
        self.cb_inventory_colsFilter.setSizePolicy(sizePolicy4)
        self.cb_inventory_colsFilter.setMinimumSize(QSize(60, 26))
        self.cb_inventory_colsFilter.setMaximumSize(QSize(16777215, 26))
#if QT_CONFIG(tooltip)
        self.cb_inventory_colsFilter.setToolTip(u"<html><head/><body><p><span style=\" font-size:12pt;\">Permite seleccionar qu\u00e9 columna filtrar.</span></p></body></html>")
#endif // QT_CONFIG(tooltip)
        self.cb_inventory_colsFilter.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
        self.cb_inventory_colsFilter.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)
        self.cb_inventory_colsFilter.setIconSize(QSize(24, 24))
        self.cb_inventory_colsFilter.setFrame(False)

        self.inventory_header_Hlayout.addWidget(self.cb_inventory_colsFilter)


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
        self.label_feedbackInventory.setStyleSheet(u"font-family: \"Verdana\";\n"
"font-size: 16px;\n"
"letter-spacing: 0px;\n"
"word-spacing: 0px;\n"
"background-color: rgb(88, 223, 171);\n"
"color: #111;")
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

        self.tab1_buttons_Hlayout.addWidget(self.btn_add_product_inventory)

        self.btn_delete_product_inventory = QPushButton(self.tab1_buttons_2)
        self.btn_delete_product_inventory.setObjectName(u"btn_delete_product_inventory")
        self.btn_delete_product_inventory.setMinimumSize(QSize(180, 23))
        self.btn_delete_product_inventory.setMaximumSize(QSize(250, 23))
#if QT_CONFIG(tooltip)
        self.btn_delete_product_inventory.setToolTip(u"<html><head/><body><p><span style=\" font-size:12pt;\">Borra el producto actualmente seleccionado (</span><span style=\" font-size:12pt; font-style:italic;\">supr</span><span style=\" font-size:12pt;\">).</span></p><p><span style=\" font-size:12pt; font-weight:600; text-decoration: underline;\">IMPORTANTE</span><span style=\" font-size:12pt; font-weight:600;\">: esta acci\u00f3n no se puede deshacer, debe estar seguro de querer eliminar un producto.</span></p></body></html>")
#endif // QT_CONFIG(tooltip)
        self.btn_delete_product_inventory.setStyleSheet(u"QPushButton {\n"
"	background-color: #ff4949;\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: #faa;\n"
"}\n"
"")
        self.btn_delete_product_inventory.setText(u"Eliminar producto")
        self.btn_delete_product_inventory.setIconSize(QSize(24, 24))
#if QT_CONFIG(shortcut)
        self.btn_delete_product_inventory.setShortcut(u"Del")
#endif // QT_CONFIG(shortcut)

        self.tab1_buttons_Hlayout.addWidget(self.btn_delete_product_inventory)


        self.inventory_display_Vlayout.addWidget(self.tab1_buttons_2)


        self.main_inventory_frame_Hlayout.addWidget(self.inventory_display)

        self.inventory_sideBar = QFrame(self.main_inventory_frame)
        self.inventory_sideBar.setObjectName(u"inventory_sideBar")
        self.inventory_sideBar.setEnabled(True)
        sizePolicy.setHeightForWidth(self.inventory_sideBar.sizePolicy().hasHeightForWidth())
        self.inventory_sideBar.setSizePolicy(sizePolicy)
        self.inventory_sideBar.setMinimumSize(QSize(40, 0))
        self.inventory_sideBar.setMaximumSize(QSize(40, 16777215))
#if QT_CONFIG(tooltip)
        self.inventory_sideBar.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.inventory_sideBar.setStyleSheet(u"* {\n"
"	background-color: #22577a;\n"
"	color: #c7f9cc;\n"
"}\n"
"\n"
"#inventory_sideBar {\n"
"	border-bottom-left-radius: 20px;\n"
"}\n"
"\n"
"QScrollBar {\n"
"	background-color: white;\n"
"}\n"
"\n"
"QLabel {\n"
"	font-size: 16px;\n"
"}\n"
"\n"
"\n"
"QLineEdit {\n"
"	background-color: #fff;\n"
"	color: #111;\n"
"	border: none;\n"
"	border-top: 1px solid;\n"
"	border-bottom: 1px solid;\n"
"	border-color: #0b7e7f;\n"
"	height: 24px;\n"
"}\n"
"QLineEdit:focus {\n"
"	background-color: rgb(197, 255, 252);\n"
"	border: 1px solid;\n"
"	border-color: #0b7e7f;\n"
"	font-size: 18px;\n"
"}")
        self.inventory_sideBar.setFrameShape(QFrame.Shape.NoFrame)
        self.inventory_sideBar.setFrameShadow(QFrame.Shadow.Raised)
        self.inventory_sideBar_Vlayout = QVBoxLayout(self.inventory_sideBar)
        self.inventory_sideBar_Vlayout.setSpacing(10)
        self.inventory_sideBar_Vlayout.setObjectName(u"inventory_sideBar_Vlayout")
        self.inventory_sideBar_Vlayout.setContentsMargins(0, 0, 0, 10)
        self.btn_inventory_sideBarToggle = QPushButton(self.inventory_sideBar)
        self.btn_inventory_sideBarToggle.setObjectName(u"btn_inventory_sideBarToggle")
        sizePolicy1.setHeightForWidth(self.btn_inventory_sideBarToggle.sizePolicy().hasHeightForWidth())
        self.btn_inventory_sideBarToggle.setSizePolicy(sizePolicy1)
        self.btn_inventory_sideBarToggle.setMinimumSize(QSize(0, 0))
        self.btn_inventory_sideBarToggle.setMaximumSize(QSize(16777215, 16777215))
        self.btn_inventory_sideBarToggle.setStyleSheet(u"QPushButton {\n"
"	border: none;\n"
"}\n"
"QPushButton:hover {\n"
"	border: 2px solid #38a3a5;\n"
"	border-radius: 3px;\n"
"	border-bottom-left-radius: 10px;\n"
"	padding-left: 2px;\n"
"	padding-bottom: 3px;\n"
"}")
        self.btn_inventory_sideBarToggle.setIconSize(QSize(32, 32))

        self.inventory_sideBar_Vlayout.addWidget(self.btn_inventory_sideBarToggle, 0, Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTop)

        self.inventory_side_bar_body = QFrame(self.inventory_sideBar)
        self.inventory_side_bar_body.setObjectName(u"inventory_side_bar_body")
        self.inventory_side_bar_body.setMinimumSize(QSize(0, 0))
        self.inventory_side_bar_body.setFrameShape(QFrame.Shape.NoFrame)
        self.inventory_side_bar_body.setFrameShadow(QFrame.Shadow.Plain)
        self.inventory_side_bar_body_Vlayout = QVBoxLayout(self.inventory_side_bar_body)
        self.inventory_side_bar_body_Vlayout.setSpacing(14)
        self.inventory_side_bar_body_Vlayout.setObjectName(u"inventory_side_bar_body_Vlayout")
        self.inventory_side_bar_body_Vlayout.setContentsMargins(5, 10, 5, 5)
        self.inventory_sideBar_label_changePrices = QLabel(self.inventory_side_bar_body)
        self.inventory_sideBar_label_changePrices.setObjectName(u"inventory_sideBar_label_changePrices")
        self.inventory_sideBar_label_changePrices.setStyleSheet(u"border-bottom: 1px solid #fff;\n"
"margin-bottom: 5px;")
        self.inventory_sideBar_label_changePrices.setText(u"CAMBIAR PRECIOS USANDO PORCENTAJES")
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
        self.change_percentage_frame_Vlayout.setSpacing(8)
        self.change_percentage_frame_Vlayout.setObjectName(u"change_percentage_frame_Vlayout")
        self.change_percentage_frame_Vlayout.setContentsMargins(0, 15, 0, 0)
        self.checkbox_unit_prices = QCheckBox(self.change_percentage_frame)
        self.inventory_checkbuttons_buttonGroup = QButtonGroup(MainWindow)
        self.inventory_checkbuttons_buttonGroup.setObjectName(u"inventory_checkbuttons_buttonGroup")
        self.inventory_checkbuttons_buttonGroup.setExclusive(True)
        self.inventory_checkbuttons_buttonGroup.addButton(self.checkbox_unit_prices)
        self.checkbox_unit_prices.setObjectName(u"checkbox_unit_prices")
#if QT_CONFIG(tooltip)
        self.checkbox_unit_prices.setToolTip(u"<html><head/><body><p><span style=\" font-size:12pt; color:#000000;\">Cambia el </span><span style=\" font-size:12pt; text-decoration: underline; color:#000000;\">precio normal</span><span style=\" font-size:12pt; color:#000000;\"> de los productos seleccionados.</span></p></body></html>")
#endif // QT_CONFIG(tooltip)
        self.checkbox_unit_prices.setText(u"Precios unitarios")
        self.checkbox_unit_prices.setIconSize(QSize(24, 24))

        self.change_percentage_frame_Vlayout.addWidget(self.checkbox_unit_prices)

        self.checkbox_comercial_prices = QCheckBox(self.change_percentage_frame)
        self.inventory_checkbuttons_buttonGroup.addButton(self.checkbox_comercial_prices)
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
        self.percentage_label.setStyleSheet(u"margin-top: 20px;\n"
"margin-bottom: 0;")
        self.percentage_label.setText(u"Porcentaje de cambio")
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
        self.lineEdit_percentage_change.setToolTip(u"<html><head/><body><p><span style=\" font-size:12pt; color:#000000;\">Aumenta o disminuye un cierto porcentaje los precios normales/comerciales seleccionados.</span></p><p><span style=\" font-size:12pt; font-weight:600; color:#000000;\">NOTA:</span><span style=\" font-size:12pt; color:#000000;\"> No es necesario escribir el s\u00edmbolo de porcentaje &quot;%&quot;, simplemente escribir el porcentaje nuevo.</span></p><p><span style=\" font-size:12pt; font-weight:600; color:#000000;\">EJ.: </span><span style=\" font-size:12pt; color:#000000;\">Para aumentar un 25% un valor, introducir &quot;25&quot;; en cambio, para disminuir el precio un 25%, introducir &quot;-25&quot;.</span></p></body></html>")
#endif // QT_CONFIG(tooltip)
        self.lineEdit_percentage_change.setStyleSheet(u"QLineEdit {\n"
"	height: 24px;\n"
"}\n"
"QLineEdit:disabled {\n"
"	background-color: #bbb;\n"
"	color: #555;\n"
"}")
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

        self.verticalLayout.addWidget(self.main_inventory_frame)

        self.tabWidget.addTab(self.tab1_inventory, "")
#if QT_CONFIG(tooltip)
        self.tabWidget.setTabToolTip(self.tabWidget.indexOf(self.tab1_inventory), u"<html><head/><body><p>Muestra el inventario de una tabla que haya sido seleccionada desde el men\u00fa lateral de la izquierda.</p></body></html>")
#endif // QT_CONFIG(tooltip)
        self.tab2_sales = QWidget()
        self.tab2_sales.setObjectName(u"tab2_sales")
        self.tab2_sales.setStyleSheet(u"#tab2_sales,\n"
"#sales_buttons,\n"
"#box2_sales_table,\n"
"#box1_sales_form {\n"
"	background-color: #35bc88;\n"
"	border-color: #0b7e7f;\n"
"}")
        self.tab2_sales_Vlayout = QVBoxLayout(self.tab2_sales)
        self.tab2_sales_Vlayout.setSpacing(4)
        self.tab2_sales_Vlayout.setObjectName(u"tab2_sales_Vlayout")
        self.tab2_sales_Vlayout.setContentsMargins(0, 5, 0, 5)
        self.tab2_toolBox = QToolBox(self.tab2_sales)
        self.tab2_toolBox.setObjectName(u"tab2_toolBox")
        self.tab2_toolBox.setStyleSheet(u"QLabel {\n"
"	font-size:14px;\n"
"	font-weight: 100;\n"
"	letter-spacing: 1px;\n"
"	word-spacing: 1px;\n"
"}")
        self.box1_sales_form = QWidget()
        self.box1_sales_form.setObjectName(u"box1_sales_form")
        self.box1_sales_form.setGeometry(QRect(0, 0, 756, 496))
        self.box1_sales_form_Vlayout = QVBoxLayout(self.box1_sales_form)
        self.box1_sales_form_Vlayout.setSpacing(4)
        self.box1_sales_form_Vlayout.setObjectName(u"box1_sales_form_Vlayout")
        self.box1_sales_form_Vlayout.setContentsMargins(0, 6, 0, 0)
        self.main_form = QFrame(self.box1_sales_form)
        self.main_form.setObjectName(u"main_form")
        self.main_form.setFrameShape(QFrame.Shape.StyledPanel)
        self.main_form.setFrameShadow(QFrame.Shadow.Raised)
        self.box1_main_form_Vlayout = QVBoxLayout(self.main_form)
        self.box1_main_form_Vlayout.setSpacing(4)
        self.box1_main_form_Vlayout.setObjectName(u"box1_main_form_Vlayout")
        self.box1_main_form_Vlayout.setContentsMargins(0, 0, 0, 0)
        self.frame_list = QFrame(self.main_form)
        self.frame_list.setObjectName(u"frame_list")
        self.frame_list.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_list.setFrameShadow(QFrame.Shadow.Raised)
        self.box1_frame_list_Vlayout = QVBoxLayout(self.frame_list)
        self.box1_frame_list_Vlayout.setSpacing(4)
        self.box1_frame_list_Vlayout.setObjectName(u"box1_frame_list_Vlayout")
        self.box1_frame_list_Vlayout.setContentsMargins(0, 0, 0, 0)
        self.add_products = QFrame(self.frame_list)
        self.add_products.setObjectName(u"add_products")
        self.add_products.setFrameShape(QFrame.Shape.StyledPanel)
        self.add_products.setFrameShadow(QFrame.Shadow.Raised)
        self.box1_add_products_Hlayout = QHBoxLayout(self.add_products)
        self.box1_add_products_Hlayout.setSpacing(4)
        self.box1_add_products_Hlayout.setObjectName(u"box1_add_products_Hlayout")
        self.box1_add_products_Hlayout.setContentsMargins(0, 0, 0, 0)
        self.btn_add_product = QPushButton(self.add_products)
        self.btn_add_product.setObjectName(u"btn_add_product")
        self.btn_add_product.setMinimumSize(QSize(180, 25))
        self.btn_add_product.setMaximumSize(QSize(250, 25))
#if QT_CONFIG(tooltip)
        self.btn_add_product.setToolTip(u"<html><head/><body><p><span style=\" font-size:12pt;\">Agrega un producto m\u00e1s a la venta actual (</span><span style=\" font-size:12pt; font-style:italic;\">+</span><span style=\" font-size:12pt;\">).</span></p></body></html>")
#endif // QT_CONFIG(tooltip)
        self.btn_add_product.setIconSize(QSize(24, 24))
#if QT_CONFIG(shortcut)
        self.btn_add_product.setShortcut(u"+")
#endif // QT_CONFIG(shortcut)

        self.box1_add_products_Hlayout.addWidget(self.btn_add_product)

        self.btn_add_product_Hspacer = QSpacerItem(379, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.box1_add_products_Hlayout.addItem(self.btn_add_product_Hspacer)

        self.box1_add_products_Hlayout.setStretch(1, 10)

        self.box1_frame_list_Vlayout.addWidget(self.add_products)

        self.sales_input_list = QListWidget(self.frame_list)
        self.sales_input_list.setObjectName(u"sales_input_list")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.sales_input_list.sizePolicy().hasHeightForWidth())
        self.sales_input_list.setSizePolicy(sizePolicy5)
        self.sales_input_list.setStyleSheet(u"QListWidget {\n"
"	background-color: rgb(194, 255, 237);\n"
"}\n"
"QListWidget::item {\n"
"	background-color: qlineargradient(spread:pad, x1:0, y1:0.273, x2:1, y2:0.835, stop:0 rgba(144, 205, 171, 255), stop:1 rgba(187, 255, 154, 255));\n"
"	margin-left: 7px;\n"
"	margin-right: 7px;\n"
"	padding: 2px;\n"
"	border-bottom: 1px solid;\n"
"	border-color: rgb(65, 117, 75);\n"
"}\n"
"QListWidget::item:selected {\n"
"	border-left: 7px solid rgb(34, 87, 122);\n"
"}")
        self.sales_input_list.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.sales_input_list.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.sales_input_list.setTabKeyNavigation(True)
        self.sales_input_list.setAlternatingRowColors(False)
        self.sales_input_list.setResizeMode(QListView.ResizeMode.Adjust)
        self.sales_input_list.setSpacing(5)
        self.sales_input_list.setUniformItemSizes(True)
        self.sales_input_list.setWordWrap(True)

        self.box1_frame_list_Vlayout.addWidget(self.sales_input_list)

        self.box1_frame_list_Vlayout.setStretch(1, 10)

        self.box1_main_form_Vlayout.addWidget(self.frame_list)

        self.sale_info = QFrame(self.main_form)
        self.sale_info.setObjectName(u"sale_info")
        self.sale_info.setStyleSheet(u"QLabel,\n"
"#lineEdit_paid {\n"
"	font-size: 21px;\n"
"}\n"
"\n"
"\n"
"#label_total_change {\n"
"	color: #dc2627;\n"
"}\n"
"\n"
"\n"
"#dateTimeEdit_sale {\n"
"	font-size: 18px;\n"
"}")
        self.sale_info.setFrameShape(QFrame.Shape.NoFrame)
        self.sale_info.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout = QGridLayout(self.sale_info)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(5)
        self.gridLayout.setVerticalSpacing(4)
        self.gridLayout.setContentsMargins(10, 0, 10, 0)
        self.label_total_change = QLabel(self.sale_info)
        self.label_total_change.setObjectName(u"label_total_change")
        self.label_total_change.setMaximumSize(QSize(400, 16777215))
        self.label_total_change.setText(u"")
        self.label_total_change.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.label_total_change.setWordWrap(False)

        self.gridLayout.addWidget(self.label_total_change, 2, 2, 2, 1)

        self.lineEdit_paid = QLineEdit(self.sale_info)
        self.lineEdit_paid.setObjectName(u"lineEdit_paid")
        self.lineEdit_paid.setMaximumSize(QSize(400, 16777215))
#if QT_CONFIG(tooltip)
        self.lineEdit_paid.setToolTip(u"<html><head/><body><p><span style=\" font-size:12pt;\">La cantidad de dinero pagado en esta venta. Si es </span><span style=\" font-size:12pt; text-decoration: underline;\">menor al total</span><span style=\" font-size:12pt;\">, la diferencia se considera </span><span style=\" font-size:12pt; text-decoration: underline;\">deuda</span><span style=\" font-size:12pt;\">. Si es </span><span style=\" font-size:12pt; text-decoration: underline;\">mayor que el total</span><span style=\" font-size:12pt;\">, se calcula el </span><span style=\" font-size:12pt; text-decoration: underline;\">vuelto</span><span style=\" font-size:12pt;\">.</span></p></body></html>")
#endif // QT_CONFIG(tooltip)
        self.lineEdit_paid.setInputMask(u"")
        self.lineEdit_paid.setText(u"")
        self.lineEdit_paid.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.lineEdit_paid.setPlaceholderText(u"Total abonado ($)")

        self.gridLayout.addWidget(self.lineEdit_paid, 1, 2, 1, 1)

        self.label_total = QLabel(self.sale_info)
        self.label_total.setObjectName(u"label_total")
        sizePolicy4.setHeightForWidth(self.label_total.sizePolicy().hasHeightForWidth())
        self.label_total.setSizePolicy(sizePolicy4)
        self.label_total.setMaximumSize(QSize(400, 16777215))
        self.label_total.setStyleSheet(u"font-weight: 500;\n"
"background-color: #bbb;\n"
"border-top: 1px solid #111;\n"
"border-right: 1px solid #111;")
        self.label_total.setText(u"TOTAL")
        self.label_total.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.label_total.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

        self.gridLayout.addWidget(self.label_total, 0, 2, 1, 1)

        self.label_paid = QLabel(self.sale_info)
        self.label_paid.setObjectName(u"label_paid")
        self.label_paid.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        self.gridLayout.addWidget(self.label_paid, 1, 1, 1, 1, Qt.AlignmentFlag.AlignRight)

        self.label_change = QLabel(self.sale_info)
        self.label_change.setObjectName(u"label_change")

        self.gridLayout.addWidget(self.label_change, 2, 1, 1, 1, Qt.AlignmentFlag.AlignRight)

        self.dateTimeEdit_sale = QDateTimeEdit(self.sale_info)
        self.dateTimeEdit_sale.setObjectName(u"dateTimeEdit_sale")
        self.dateTimeEdit_sale.setWrapping(True)
        self.dateTimeEdit_sale.setFrame(False)
        self.dateTimeEdit_sale.setReadOnly(True)
        self.dateTimeEdit_sale.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.dateTimeEdit_sale.setAccelerated(False)
        self.dateTimeEdit_sale.setCorrectionMode(QAbstractSpinBox.CorrectionMode.CorrectToPreviousValue)
        self.dateTimeEdit_sale.setKeyboardTracking(False)
        self.dateTimeEdit_sale.setProperty("showGroupSeparator", True)

        self.gridLayout.addWidget(self.dateTimeEdit_sale, 0, 0, 1, 1)


        self.box1_main_form_Vlayout.addWidget(self.sale_info)

        self.end_sale = QFrame(self.main_form)
        self.end_sale.setObjectName(u"end_sale")
        self.end_sale.setFrameShape(QFrame.Shape.StyledPanel)
        self.end_sale.setFrameShadow(QFrame.Shadow.Raised)
        self.end_sale_Hlayout = QHBoxLayout(self.end_sale)
        self.end_sale_Hlayout.setSpacing(0)
        self.end_sale_Hlayout.setObjectName(u"end_sale_Hlayout")
        self.end_sale_Hlayout.setContentsMargins(0, 3, 15, 10)
        self.horizontalSpacer_2 = QSpacerItem(412, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.end_sale_Hlayout.addItem(self.horizontalSpacer_2)

        self.btn_end_sale = QPushButton(self.end_sale)
        self.btn_end_sale.setObjectName(u"btn_end_sale")
        self.btn_end_sale.setEnabled(False)
#if QT_CONFIG(tooltip)
        self.btn_end_sale.setToolTip(u"<html><head/><body><p><span style=\" font-size:12pt;\">Guarda los datos de la venta actual y da por terminada la venta (</span><span style=\" font-size:12pt; font-style:italic;\">may\u00fasculas </span><span style=\" font-size:12pt;\">+</span><span style=\" font-size:12pt; font-style:italic;\"> enter</span><span style=\" font-size:12pt;\">).</span></p></body></html>")
#endif // QT_CONFIG(tooltip)
        self.btn_end_sale.setIconSize(QSize(24, 24))
#if QT_CONFIG(shortcut)
        self.btn_end_sale.setShortcut(u"Shift+Return")
#endif // QT_CONFIG(shortcut)

        self.end_sale_Hlayout.addWidget(self.btn_end_sale)

        self.end_sale_Hlayout.setStretch(0, 3)
        self.end_sale_Hlayout.setStretch(1, 1)

        self.box1_main_form_Vlayout.addWidget(self.end_sale)

        self.box1_main_form_Vlayout.setStretch(0, 10)

        self.box1_sales_form_Vlayout.addWidget(self.main_form)

        self.tab2_toolBox.addItem(self.box1_sales_form, u"Formulario de venta")
        self.box2_sales_table = QWidget()
        self.box2_sales_table.setObjectName(u"box2_sales_table")
        self.box2_sales_table.setGeometry(QRect(0, 0, 756, 496))
        self.box2_sales_Vlayout = QVBoxLayout(self.box2_sales_table)
        self.box2_sales_Vlayout.setSpacing(4)
        self.box2_sales_Vlayout.setObjectName(u"box2_sales_Vlayout")
        self.box2_sales_Vlayout.setContentsMargins(0, 6, 0, 0)
        self.sales_table_header = QFrame(self.box2_sales_table)
        self.sales_table_header.setObjectName(u"sales_table_header")
        sizePolicy3.setHeightForWidth(self.sales_table_header.sizePolicy().hasHeightForWidth())
        self.sales_table_header.setSizePolicy(sizePolicy3)
        self.sales_table_header.setFrameShape(QFrame.Shape.NoFrame)
        self.sales_table_header.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.sales_table_header)
        self.horizontalLayout_2.setSpacing(4)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(5, 0, 5, 0)
        self.sales_searchBar = QLineEdit(self.sales_table_header)
        self.sales_searchBar.setObjectName(u"sales_searchBar")
        sizePolicy4.setHeightForWidth(self.sales_searchBar.sizePolicy().hasHeightForWidth())
        self.sales_searchBar.setSizePolicy(sizePolicy4)
        self.sales_searchBar.setMinimumSize(QSize(150, 25))
        self.sales_searchBar.setMaximumSize(QSize(16777215, 25))
        self.sales_searchBar.setAcceptDrops(False)
#if QT_CONFIG(tooltip)
        self.sales_searchBar.setToolTip(u"<html><head/><body><p><span style=\" font-size:12pt;\">Buscar una venta en la tabla seg\u00fan nombres, caracter\u00edsticas, palabras claves, etc.</span></p></body></html>")
#endif // QT_CONFIG(tooltip)
        self.sales_searchBar.setText(u"")
        self.sales_searchBar.setMaxLength(100)
        self.sales_searchBar.setFrame(False)
        self.sales_searchBar.setEchoMode(QLineEdit.EchoMode.Normal)
        self.sales_searchBar.setPlaceholderText(u"Ingresar detalles de ventas a buscar...")
        self.sales_searchBar.setCursorMoveStyle(Qt.CursorMoveStyle.LogicalMoveStyle)
        self.sales_searchBar.setClearButtonEnabled(True)

        self.horizontalLayout_2.addWidget(self.sales_searchBar)

        self.cb_sales_colsFilter = QComboBox(self.sales_table_header)
        self.cb_sales_colsFilter.addItem("")
        self.cb_sales_colsFilter.addItem("")
        self.cb_sales_colsFilter.addItem("")
        self.cb_sales_colsFilter.addItem("")
        self.cb_sales_colsFilter.addItem("")
        self.cb_sales_colsFilter.addItem("")
        self.cb_sales_colsFilter.addItem("")
        self.cb_sales_colsFilter.setObjectName(u"cb_sales_colsFilter")
        self.cb_sales_colsFilter.setMinimumSize(QSize(60, 26))
        self.cb_sales_colsFilter.setMaximumSize(QSize(16777215, 26))
#if QT_CONFIG(tooltip)
        self.cb_sales_colsFilter.setToolTip(u"<html><head/><body><p><span style=\" font-size:12pt;\">Permite seleccionar qu\u00e9 columna filtrar.</span></p></body></html>")
#endif // QT_CONFIG(tooltip)
        self.cb_sales_colsFilter.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
        self.cb_sales_colsFilter.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)
        self.cb_sales_colsFilter.setIconSize(QSize(24, 24))
        self.cb_sales_colsFilter.setFrame(False)

        self.horizontalLayout_2.addWidget(self.cb_sales_colsFilter)


        self.box2_sales_Vlayout.addWidget(self.sales_table_header)

        self.sales_progressbar = QProgressBar(self.box2_sales_table)
        self.sales_progressbar.setObjectName(u"sales_progressbar")
        self.sales_progressbar.setMinimumSize(QSize(0, 12))
        self.sales_progressbar.setMaximumSize(QSize(16777215, 12))
        self.sales_progressbar.setValue(24)
        self.sales_progressbar.setTextVisible(False)
        self.sales_progressbar.setFormat(u"%p%")

        self.box2_sales_Vlayout.addWidget(self.sales_progressbar)

        self.tv_sales_data = QTableView(self.box2_sales_table)
        self.tv_sales_data.setObjectName(u"tv_sales_data")
#if QT_CONFIG(tooltip)
        self.tv_sales_data.setToolTip(u"<html><head/><body><p><span style=\" font-size:12pt;\">Para </span><span style=\" font-size:12pt; text-decoration: underline;\">modificar</span><span style=\" font-size:12pt;\"> un dato de alguna venta hacer </span><span style=\" font-size:12pt; font-style:italic;\">doble click</span><span style=\" font-size:12pt;\"> sobre una celda e ingresar el nuevo valor.</span></p><p><span style=\" font-size:12pt; font-weight:600; text-decoration: underline;\">NOTA:</span><span style=\" font-size:12pt;\"> si se cambia el </span><span style=\" font-size:12pt; font-style:italic;\">producto vendido</span><span style=\" font-size:12pt;\"> o la </span><span style=\" font-size:12pt; font-style:italic;\">cantidad vendida</span><span style=\" font-size:12pt;\"> de un producto NO se ver\u00e1 afectado el stock de ese producto directamente, para eso es necesario cambiar el stock de ese producto manualmente mediante la pesta\u00f1a de </span><span style=\" font-size:12pt; font-style:italic;\">inventario</span><span style=\" font-siz"
                        "e:12pt;\">.</span></p></body></html>")
#endif // QT_CONFIG(tooltip)
        self.tv_sales_data.setStyleSheet(u"")
        self.tv_sales_data.setFrameShape(QFrame.Shape.NoFrame)
        self.tv_sales_data.setFrameShadow(QFrame.Shadow.Plain)
        self.tv_sales_data.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.tv_sales_data.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.tv_sales_data.setEditTriggers(QAbstractItemView.EditTrigger.DoubleClicked)
        self.tv_sales_data.setProperty("showDropIndicator", False)
        self.tv_sales_data.setDragDropOverwriteMode(False)
        self.tv_sales_data.setAlternatingRowColors(True)
        self.tv_sales_data.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.tv_sales_data.setTextElideMode(Qt.TextElideMode.ElideMiddle)
        self.tv_sales_data.setGridStyle(Qt.PenStyle.SolidLine)
        self.tv_sales_data.setSortingEnabled(False)
        self.tv_sales_data.setCornerButtonEnabled(False)
        self.tv_sales_data.horizontalHeader().setMinimumSectionSize(41)
        self.tv_sales_data.verticalHeader().setVisible(False)

        self.box2_sales_Vlayout.addWidget(self.tv_sales_data)

        self.label_feedbackSales = QLabel(self.box2_sales_table)
        self.label_feedbackSales.setObjectName(u"label_feedbackSales")
        self.label_feedbackSales.setStyleSheet(u"font-family: \"Verdana\";\n"
"font-size: 16px;\n"
"letter-spacing: 0px;\n"
"word-spacing: 0px;\n"
"background-color: rgb(88, 223, 171);\n"
"color: #111;")
        self.label_feedbackSales.setText(u"")
        self.label_feedbackSales.setTextFormat(Qt.TextFormat.PlainText)
        self.label_feedbackSales.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_feedbackSales.setWordWrap(True)
        self.label_feedbackSales.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        self.box2_sales_Vlayout.addWidget(self.label_feedbackSales)

        self.sales_buttons = QFrame(self.box2_sales_table)
        self.sales_buttons.setObjectName(u"sales_buttons")
        self.sales_buttons.setFrameShape(QFrame.Shape.StyledPanel)
        self.sales_buttons.setFrameShadow(QFrame.Shadow.Raised)
        self.box2_sales_buttons_Hlayout = QHBoxLayout(self.sales_buttons)
        self.box2_sales_buttons_Hlayout.setSpacing(4)
        self.box2_sales_buttons_Hlayout.setObjectName(u"box2_sales_buttons_Hlayout")
        self.box2_sales_buttons_Hlayout.setContentsMargins(0, 0, 0, 0)
        self.btn_add_product_sales = QPushButton(self.sales_buttons)
        self.btn_add_product_sales.setObjectName(u"btn_add_product_sales")
        self.btn_add_product_sales.setMinimumSize(QSize(180, 25))
        self.btn_add_product_sales.setMaximumSize(QSize(250, 25))
#if QT_CONFIG(tooltip)
        self.btn_add_product_sales.setToolTip(u"<html><head/><body><p><span style=\" font-size:12pt;\">A\u00f1adir un producto nuevo vendido a la lista de ventas actual (</span><span style=\" font-size:12pt; font-style:italic;\">+</span><span style=\" font-size:12pt;\">).</span></p></body></html>")
#endif // QT_CONFIG(tooltip)
        self.btn_add_product_sales.setText(u"Nueva venta")
        self.btn_add_product_sales.setIconSize(QSize(24, 24))
#if QT_CONFIG(shortcut)
        self.btn_add_product_sales.setShortcut(u"+")
#endif // QT_CONFIG(shortcut)

        self.box2_sales_buttons_Hlayout.addWidget(self.btn_add_product_sales)

        self.btn_delete_product_sales = QPushButton(self.sales_buttons)
        self.btn_delete_product_sales.setObjectName(u"btn_delete_product_sales")
        self.btn_delete_product_sales.setMinimumSize(QSize(180, 25))
        self.btn_delete_product_sales.setMaximumSize(QSize(250, 25))
#if QT_CONFIG(tooltip)
        self.btn_delete_product_sales.setToolTip(u"<html><head/><body><p><span style=\" font-size:12pt;\">Borra el producto vendido actualmente seleccionado (</span><span style=\" font-size:12pt; font-style:italic;\">supr</span><span style=\" font-size:12pt;\">).</span></p><p><span style=\" font-size:12pt; font-weight:600; text-decoration: underline;\">IMPORTANTE</span><span style=\" font-size:12pt; font-weight:600;\">: esta acci\u00f3n no se puede deshacer, debe estar seguro de querer eliminar un producto.</span></p></body></html>")
#endif // QT_CONFIG(tooltip)
        self.btn_delete_product_sales.setStyleSheet(u"QPushButton {\n"
"	background-color: #ff4949;\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: #faa;\n"
"}\n"
"")
        self.btn_delete_product_sales.setIconSize(QSize(24, 24))
#if QT_CONFIG(shortcut)
        self.btn_delete_product_sales.setShortcut(u"Del")
#endif // QT_CONFIG(shortcut)

        self.box2_sales_buttons_Hlayout.addWidget(self.btn_delete_product_sales)


        self.box2_sales_Vlayout.addWidget(self.sales_buttons)

        self.tab2_toolBox.addItem(self.box2_sales_table, u"Tabla de ventas")

        self.tab2_sales_Vlayout.addWidget(self.tab2_toolBox)

        self.tabWidget.addTab(self.tab2_sales, "")
#if QT_CONFIG(tooltip)
        self.tabWidget.setTabToolTip(self.tabWidget.indexOf(self.tab2_sales), u"<html><head/><body><p>Muestra informaci\u00f3n sobre las ventas realizadas y permite ingresar nuevas ventas.</p></body></html>")
#endif // QT_CONFIG(tooltip)
        self.tab3_debts = QWidget()
        self.tab3_debts.setObjectName(u"tab3_debts")
        self.tab3_debts_Vlayout = QVBoxLayout(self.tab3_debts)
        self.tab3_debts_Vlayout.setSpacing(4)
        self.tab3_debts_Vlayout.setObjectName(u"tab3_debts_Vlayout")
        self.tab3_debts_Vlayout.setContentsMargins(0, 0, 0, 5)
        self.debts_info = QFrame(self.tab3_debts)
        self.debts_info.setObjectName(u"debts_info")
        self.debts_info.setFrameShape(QFrame.Shape.StyledPanel)
        self.debts_info.setFrameShadow(QFrame.Shadow.Raised)
        self.debts_info_Vlayout = QVBoxLayout(self.debts_info)
        self.debts_info_Vlayout.setSpacing(4)
        self.debts_info_Vlayout.setObjectName(u"debts_info_Vlayout")
        self.debts_info_Vlayout.setContentsMargins(0, 8, 0, 0)
        self.debts_header = QFrame(self.debts_info)
        self.debts_header.setObjectName(u"debts_header")
        sizePolicy3.setHeightForWidth(self.debts_header.sizePolicy().hasHeightForWidth())
        self.debts_header.setSizePolicy(sizePolicy3)
        self.debts_header.setFrameShape(QFrame.Shape.NoFrame)
        self.debts_header.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.debts_header)
        self.horizontalLayout_4.setSpacing(4)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(5, 0, 5, 0)
        self.debts_searchBar = QLineEdit(self.debts_header)
        self.debts_searchBar.setObjectName(u"debts_searchBar")
        sizePolicy4.setHeightForWidth(self.debts_searchBar.sizePolicy().hasHeightForWidth())
        self.debts_searchBar.setSizePolicy(sizePolicy4)
        self.debts_searchBar.setMinimumSize(QSize(150, 25))
        self.debts_searchBar.setMaximumSize(QSize(16777215, 25))
        font2 = QFont()
        font2.setFamilies([u"Verdana"])
        font2.setStyleStrategy(QFont.PreferDefault)
        self.debts_searchBar.setFont(font2)
        self.debts_searchBar.setAcceptDrops(False)
#if QT_CONFIG(tooltip)
        self.debts_searchBar.setToolTip(u"<html><head/><body><p><span style=\" font-size:12pt;\">Buscar una deuda en la tabla seg\u00fan nombres, caracter\u00edsticas, palabras claves, etc.</span></p></body></html>")
#endif // QT_CONFIG(tooltip)
        self.debts_searchBar.setText(u"")
        self.debts_searchBar.setMaxLength(100)
        self.debts_searchBar.setFrame(False)
        self.debts_searchBar.setEchoMode(QLineEdit.EchoMode.Normal)
        self.debts_searchBar.setPlaceholderText(u"Ingresar detalles de cuenta corriente a buscar...")
        self.debts_searchBar.setCursorMoveStyle(Qt.CursorMoveStyle.LogicalMoveStyle)
        self.debts_searchBar.setClearButtonEnabled(True)

        self.horizontalLayout_4.addWidget(self.debts_searchBar)

        self.cb_debts_colsFilter = QComboBox(self.debts_header)
        self.cb_debts_colsFilter.setObjectName(u"cb_debts_colsFilter")
        self.cb_debts_colsFilter.setMinimumSize(QSize(60, 26))
        self.cb_debts_colsFilter.setMaximumSize(QSize(16777215, 26))
#if QT_CONFIG(tooltip)
        self.cb_debts_colsFilter.setToolTip(u"<html><head/><body><p><span style=\" font-size:12pt;\">Permite seleccionar qu\u00e9 columna filtrar.</span></p></body></html>")
#endif // QT_CONFIG(tooltip)
        self.cb_debts_colsFilter.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
        self.cb_debts_colsFilter.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)
        self.cb_debts_colsFilter.setIconSize(QSize(24, 24))
        self.cb_debts_colsFilter.setFrame(False)

        self.horizontalLayout_4.addWidget(self.cb_debts_colsFilter)


        self.debts_info_Vlayout.addWidget(self.debts_header)

        self.debts_progressbar = QProgressBar(self.debts_info)
        self.debts_progressbar.setObjectName(u"debts_progressbar")
        self.debts_progressbar.setMinimumSize(QSize(0, 12))
        self.debts_progressbar.setMaximumSize(QSize(16777215, 12))
        self.debts_progressbar.setValue(24)
        self.debts_progressbar.setTextVisible(False)
        self.debts_progressbar.setFormat(u"%p%")

        self.debts_info_Vlayout.addWidget(self.debts_progressbar)

        self.tv_debts_data = QTableView(self.debts_info)
        self.tv_debts_data.setObjectName(u"tv_debts_data")
#if QT_CONFIG(tooltip)
        self.tv_debts_data.setToolTip(u"<html><head/><body><p><span style=\" font-size:12pt;\">Para </span><span style=\" font-size:12pt; text-decoration: underline;\">modificar</span><span style=\" font-size:12pt;\"> las </span><span style=\" font-size:12pt; text-decoration: underline;\">caracter\u00edsticas</span><span style=\" font-size:12pt;\"> de una deuda simplemente hacer </span><span style=\" font-size:12pt; font-style:italic;\">doble click</span><span style=\" font-size:12pt;\"> sobre la celda que se quiere modificar e ingresar el nuevo valor.</span></p></body></html>")
#endif // QT_CONFIG(tooltip)
        self.tv_debts_data.setStyleSheet(u"#tv_debts_data QLabel {\n"
"	font-size: 16px;\n"
"}\n"
"\n"
"\n"
"#tv_debts_data QPushButton {\n"
"	max-width: 24px;\n"
"	max-height: 24px;\n"
"	border-radius: 1px;\n"
"	background-color: rgb(71, 184, 255);\n"
"}")
        self.tv_debts_data.setFrameShape(QFrame.Shape.NoFrame)
        self.tv_debts_data.setFrameShadow(QFrame.Shadow.Plain)
        self.tv_debts_data.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.tv_debts_data.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.tv_debts_data.setEditTriggers(QAbstractItemView.EditTrigger.DoubleClicked)
        self.tv_debts_data.setProperty("showDropIndicator", False)
        self.tv_debts_data.setDragDropOverwriteMode(False)
        self.tv_debts_data.setDefaultDropAction(Qt.DropAction.IgnoreAction)
        self.tv_debts_data.setAlternatingRowColors(True)
        self.tv_debts_data.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.tv_debts_data.setSortingEnabled(False)
        self.tv_debts_data.setCornerButtonEnabled(False)
        self.tv_debts_data.horizontalHeader().setMinimumSectionSize(50)
        self.tv_debts_data.verticalHeader().setVisible(False)

        self.debts_info_Vlayout.addWidget(self.tv_debts_data)

        self.label_feedbackDebts = QLabel(self.debts_info)
        self.label_feedbackDebts.setObjectName(u"label_feedbackDebts")
        self.label_feedbackDebts.setStyleSheet(u"font-family: \"Verdana\";\n"
"font-size: 16px;\n"
"letter-spacing: 0px;\n"
"word-spacing: 0px;\n"
"background-color: rgb(88, 223, 171);\n"
"color: #111;")
        self.label_feedbackDebts.setText(u"")
        self.label_feedbackDebts.setTextFormat(Qt.TextFormat.PlainText)
        self.label_feedbackDebts.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_feedbackDebts.setWordWrap(True)
        self.label_feedbackDebts.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        self.debts_info_Vlayout.addWidget(self.label_feedbackDebts)

        self.debts_buttons = QFrame(self.debts_info)
        self.debts_buttons.setObjectName(u"debts_buttons")
        self.debts_buttons.setFrameShape(QFrame.Shape.NoFrame)
        self.debts_buttons.setFrameShadow(QFrame.Shadow.Raised)
        self.debts_buttons_Hlayout = QHBoxLayout(self.debts_buttons)
        self.debts_buttons_Hlayout.setSpacing(4)
        self.debts_buttons_Hlayout.setObjectName(u"debts_buttons_Hlayout")
        self.debts_buttons_Hlayout.setContentsMargins(0, 0, 0, 0)
        self.btn_add_debt = QPushButton(self.debts_buttons)
        self.btn_add_debt.setObjectName(u"btn_add_debt")
        self.btn_add_debt.setMinimumSize(QSize(180, 25))
        self.btn_add_debt.setMaximumSize(QSize(250, 25))
#if QT_CONFIG(tooltip)
        self.btn_add_debt.setToolTip(u"<html><head/><body><p><span style=\" font-size:12pt;\">Agrega una deuda nueva a la tabla (</span><span style=\" font-size:12pt; font-style:italic;\">+</span><span style=\" font-size:12pt;\">).</span></p></body></html>")
#endif // QT_CONFIG(tooltip)
        self.btn_add_debt.setText(u"Nueva deuda")
        self.btn_add_debt.setIconSize(QSize(24, 24))
#if QT_CONFIG(shortcut)
        self.btn_add_debt.setShortcut(u"+")
#endif // QT_CONFIG(shortcut)

        self.debts_buttons_Hlayout.addWidget(self.btn_add_debt)

        self.btn_delete_debt = QPushButton(self.debts_buttons)
        self.btn_delete_debt.setObjectName(u"btn_delete_debt")
        self.btn_delete_debt.setMinimumSize(QSize(180, 25))
        self.btn_delete_debt.setMaximumSize(QSize(250, 25))
#if QT_CONFIG(tooltip)
        self.btn_delete_debt.setToolTip(u"<html><head/><body><p><span style=\" font-size:12pt;\">Elimina la deuda actualmente seleccionada en la tabla (</span><span style=\" font-size:12pt; font-style:italic;\">supr</span><span style=\" font-size:12pt;\">).</span></p><p><span style=\" font-size:12pt; font-weight:600; text-decoration: underline;\">IMPORTANTE</span><span style=\" font-size:12pt; font-weight:600;\">: esta acci\u00f3n no se puede deshacer, debe estar seguro de querer borrar una deuda.</span></p></body></html>")
#endif // QT_CONFIG(tooltip)
        self.btn_delete_debt.setStyleSheet(u"QPushButton {\n"
"	background-color: #ff4949;\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: #faa;\n"
"}\n"
"")
        self.btn_delete_debt.setText(u"Eliminar deuda")
        self.btn_delete_debt.setIconSize(QSize(24, 24))
#if QT_CONFIG(shortcut)
        self.btn_delete_debt.setShortcut(u"Del")
#endif // QT_CONFIG(shortcut)

        self.debts_buttons_Hlayout.addWidget(self.btn_delete_debt)


        self.debts_info_Vlayout.addWidget(self.debts_buttons)


        self.tab3_debts_Vlayout.addWidget(self.debts_info)

        self.tabWidget.addTab(self.tab3_debts, "")
#if QT_CONFIG(tooltip)
        self.tabWidget.setTabToolTip(self.tabWidget.indexOf(self.tab3_debts), u"<html><head/><body><p>Muestra las cuentas corrientes y datos personales de quienes posean una.</p></body></html>")
#endif // QT_CONFIG(tooltip)

        self.main_body_VLayout.addWidget(self.tabWidget)


        self.centralwidget_HLayout.addWidget(self.main_body)

        MainWindow.setCentralWidget(self.centralwidget)
        QWidget.setTabOrder(self.tabWidget, self.inventory_searchBar)
        QWidget.setTabOrder(self.inventory_searchBar, self.cb_inventory_colsFilter)
        QWidget.setTabOrder(self.cb_inventory_colsFilter, self.tv_inventory_data)
        QWidget.setTabOrder(self.tv_inventory_data, self.btn_add_product_inventory)
        QWidget.setTabOrder(self.btn_add_product_inventory, self.btn_delete_product_inventory)
        QWidget.setTabOrder(self.btn_delete_product_inventory, self.btn_side_barToggle)
        QWidget.setTabOrder(self.btn_side_barToggle, self.tables_ListWidget)
        QWidget.setTabOrder(self.tables_ListWidget, self.btn_inventory_sideBarToggle)
        QWidget.setTabOrder(self.btn_inventory_sideBarToggle, self.checkbox_unit_prices)
        QWidget.setTabOrder(self.checkbox_unit_prices, self.checkbox_comercial_prices)
        QWidget.setTabOrder(self.checkbox_comercial_prices, self.lineEdit_percentage_change)
        QWidget.setTabOrder(self.lineEdit_percentage_change, self.btn_add_product)
        QWidget.setTabOrder(self.btn_add_product, self.sales_input_list)
        QWidget.setTabOrder(self.sales_input_list, self.dateTimeEdit_sale)
        QWidget.setTabOrder(self.dateTimeEdit_sale, self.lineEdit_paid)
        QWidget.setTabOrder(self.lineEdit_paid, self.btn_end_sale)
        QWidget.setTabOrder(self.btn_end_sale, self.sales_searchBar)
        QWidget.setTabOrder(self.sales_searchBar, self.cb_sales_colsFilter)
        QWidget.setTabOrder(self.cb_sales_colsFilter, self.tv_sales_data)
        QWidget.setTabOrder(self.tv_sales_data, self.btn_add_product_sales)
        QWidget.setTabOrder(self.btn_add_product_sales, self.btn_delete_product_sales)
        QWidget.setTabOrder(self.btn_delete_product_sales, self.debts_searchBar)
        QWidget.setTabOrder(self.debts_searchBar, self.cb_debts_colsFilter)
        QWidget.setTabOrder(self.cb_debts_colsFilter, self.tv_debts_data)
        QWidget.setTabOrder(self.tv_debts_data, self.btn_add_debt)
        QWidget.setTabOrder(self.btn_add_debt, self.btn_delete_debt)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(1)
        self.tab2_toolBox.setCurrentIndex(0)
        self.tab2_toolBox.layout().setSpacing(4)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionNuevo.setText(QCoreApplication.translate("MainWindow", u"Nuevo...", None))
        self.actionAbrir.setText(QCoreApplication.translate("MainWindow", u"Abrir...", None))
        self.actionGuardar.setText(QCoreApplication.translate("MainWindow", u"Guardar", None))
        self.actionGuardar_como.setText(QCoreApplication.translate("MainWindow", u"Guardar como...", None))
        self.actionConfiguraci_n.setText(QCoreApplication.translate("MainWindow", u"Configuraci\u00f3n...", None))
        self.actionSobre_el_programa.setText(QCoreApplication.translate("MainWindow", u"Sobre el programa...", None))
        self.actionLicencia.setText(QCoreApplication.translate("MainWindow", u"Licencia", None))
        self.btn_side_barToggle.setText("")

        __sortingEnabled = self.tables_ListWidget.isSortingEnabled()
        self.tables_ListWidget.setSortingEnabled(False)
        self.tables_ListWidget.setSortingEnabled(__sortingEnabled)


        self.btn_inventory_sideBarToggle.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab1_inventory), QCoreApplication.translate("MainWindow", u"INVENTARIO", None))
        self.btn_add_product.setText(QCoreApplication.translate("MainWindow", u"Agregar producto", None))
        self.label_paid.setText(QCoreApplication.translate("MainWindow", u"ABONA", None))
        self.label_change.setText(QCoreApplication.translate("MainWindow", u"CAMBIO", None))
        self.dateTimeEdit_sale.setDisplayFormat(QCoreApplication.translate("MainWindow", u"d/M/yyyy HH:mm:ss", None))
        self.btn_end_sale.setText(QCoreApplication.translate("MainWindow", u"Finalizar venta", None))
        self.tab2_toolBox.setItemText(self.tab2_toolBox.indexOf(self.box1_sales_form), QCoreApplication.translate("MainWindow", u"Formulario de venta", None))
        self.cb_sales_colsFilter.setItemText(0, QCoreApplication.translate("MainWindow", u"Todas", None))
        self.cb_sales_colsFilter.setItemText(1, QCoreApplication.translate("MainWindow", u"Detalles de venta", None))
        self.cb_sales_colsFilter.setItemText(2, QCoreApplication.translate("MainWindow", u"Cantidad", None))
        self.cb_sales_colsFilter.setItemText(3, QCoreApplication.translate("MainWindow", u"Producto", None))
        self.cb_sales_colsFilter.setItemText(4, QCoreApplication.translate("MainWindow", u"Costo total", None))
        self.cb_sales_colsFilter.setItemText(5, QCoreApplication.translate("MainWindow", u"Abonado", None))
        self.cb_sales_colsFilter.setItemText(6, QCoreApplication.translate("MainWindow", u"Fecha y hora", None))

        self.btn_delete_product_sales.setText(QCoreApplication.translate("MainWindow", u"Eliminar venta", None))
        self.tab2_toolBox.setItemText(self.tab2_toolBox.indexOf(self.box2_sales_table), QCoreApplication.translate("MainWindow", u"Tabla de ventas", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab2_sales), QCoreApplication.translate("MainWindow", u"VENTAS", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab3_debts), QCoreApplication.translate("MainWindow", u"CUENTAS CORRIENTES", None))
    # retranslateUi

