# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'debts_balanceProductsList.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QAbstractScrollArea, QApplication, QDialog,
    QFrame, QHeaderView, QLineEdit, QSizePolicy,
    QTableView, QVBoxLayout, QWidget)

class Ui_ProductsBalance(object):
    def setupUi(self, ProductsBalance):
        if not ProductsBalance.objectName():
            ProductsBalance.setObjectName(u"ProductsBalance")
        ProductsBalance.resize(400, 150)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ProductsBalance.sizePolicy().hasHeightForWidth())
        ProductsBalance.setSizePolicy(sizePolicy)
        ProductsBalance.setMinimumSize(QSize(400, 100))
        ProductsBalance.setMaximumSize(QSize(400, 16777215))
        ProductsBalance.setWindowOpacity(1.000000000000000)
        ProductsBalance.setStyleSheet(u"* {\n"
"	color: #111;\n"
"	font-family: \"Verdana\", \"Sans-Serif\";\n"
"	font-size: 14px;\n"
"}\n"
"\n"
"\n"
"#central_widget {\n"
"	background-color: rgba(34, 87, 122, 190);\n"
"	border-radius: 5px;\n"
"}\n"
"\n"
"\n"
"QToolTip {\n"
"	background-color: #fff;\n"
"}\n"
"\n"
"\n"
"QTableView {\n"
"	background-color: rgba(34, 87, 122, 240);\n"
"	color: #fff;\n"
"}\n"
"QTableView::item:hover {\n"
"	background-color: #38a3a5;\n"
"}\n"
"QTableView::item:selected {\n"
"	background-color: rgb(84,147,212);\n"
"	color: #333;\n"
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
"QLineEdit {\n"
"	color: #111;\n"
"	background-color: rgba(255, 255, 255, 255);\n"
"	border: none;\n"
"	border-radius: 3px;\n"
"}\n"
"QLineEdit:focus {\n"
"	background-color: rgba(197, 255, 252, 255);\n"
"	border: 1px solid;\n"
"	border-color: #0b7e7f;\n"
"}\n"
"\n"
"\n"
"#search_bar {\n"
"	border-bottom: 1px solid;\n"
""
                        "	border-bottom-color: #555;\n"
"	border-bottom-color: #111;\n"
"	margin-left: 30px;\n"
"	margin-right: 30px;\n"
"}\n"
"\n"
"\n"
"#le_reduce_debt {\n"
"	border-top: 1px solid;\n"
"	border-bottom: 1px solid;\n"
"	border-color: #fff;\n"
"}\n"
"\n"
"\n"
"/* estilos del QDateTimeEdit y del QCalendarWidget */\n"
"QDateTimeEdit {\n"
"	color: #333;\n"
"	background-color: #fff;\n"
"}\n"
"\n"
"\n"
"QCalendarWidget QAbstractItemView {\n"
"	background-color: #fff;\n"
"	selection-background-color: #38a3a5;\n"
"	color: #444;\n"
"}\n"
"QCalendarWidget QToolButton {\n"
"	background-color: #22577a;\n"
"	color: #fff;\n"
"}\n"
"QCalendarWidget QHeaderView {\n"
"	background-color: #fff;\n"
"	color: #fff;\n"
"}\n"
"QCalendarWidget QToolButton:hover,\n"
"QCalendarWidget QToolButton:pressed {\n"
"	background-color: #38a3a5;\n"
"	color: #555;\n"
"}")
        self.verticalLayout = QVBoxLayout(ProductsBalance)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.central_widget = QWidget(ProductsBalance)
        self.central_widget.setObjectName(u"central_widget")
        self.verticalLayout_2 = QVBoxLayout(self.central_widget)
        self.verticalLayout_2.setSpacing(7)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(5, 5, 5, 5)
        self.search_bar = QLineEdit(self.central_widget)
        self.search_bar.setObjectName(u"search_bar")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.search_bar.sizePolicy().hasHeightForWidth())
        self.search_bar.setSizePolicy(sizePolicy1)
        self.search_bar.setMinimumSize(QSize(0, 24))
        self.search_bar.setMaximumSize(QSize(16777215, 24))
        self.search_bar.setFrame(False)
        self.search_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_2.addWidget(self.search_bar)

        self.tv_balance_products = QTableView(self.central_widget)
        self.tv_balance_products.setObjectName(u"tv_balance_products")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.tv_balance_products.sizePolicy().hasHeightForWidth())
        self.tv_balance_products.setSizePolicy(sizePolicy2)
        self.tv_balance_products.setFrameShape(QFrame.Shape.NoFrame)
        self.tv_balance_products.setFrameShadow(QFrame.Shadow.Plain)
        self.tv_balance_products.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.tv_balance_products.setEditTriggers(QAbstractItemView.EditTrigger.DoubleClicked)
        self.tv_balance_products.setProperty("showDropIndicator", False)
        self.tv_balance_products.setDragDropOverwriteMode(False)
        self.tv_balance_products.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.tv_balance_products.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectItems)
        self.tv_balance_products.setSortingEnabled(False)
        self.tv_balance_products.setCornerButtonEnabled(False)
        self.tv_balance_products.horizontalHeader().setMinimumSectionSize(40)
        self.tv_balance_products.horizontalHeader().setHighlightSections(True)
        self.tv_balance_products.verticalHeader().setVisible(False)

        self.verticalLayout_2.addWidget(self.tv_balance_products)

        self.le_reduce_debt = QLineEdit(self.central_widget)
        self.le_reduce_debt.setObjectName(u"le_reduce_debt")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.le_reduce_debt.sizePolicy().hasHeightForWidth())
        self.le_reduce_debt.setSizePolicy(sizePolicy3)
        self.le_reduce_debt.setMinimumSize(QSize(0, 24))
        self.le_reduce_debt.setMaximumSize(QSize(16777215, 24))
#if QT_CONFIG(tooltip)
        self.le_reduce_debt.setToolTip(u"<html><head/><body><p>Descuenta la cantidad especificada de los productos seleccionados en <span style=\" font-weight:700;\">orden de selecci\u00f3n</span>. Si no hay productos seleccionados, descuenta desde el primero al \u00faltimo en <span style=\" font-weight:700;\">orden de aparici\u00f3n</span>.</p></body></html>")
#endif // QT_CONFIG(tooltip)
        self.le_reduce_debt.setFrame(False)
        self.le_reduce_debt.setClearButtonEnabled(True)

        self.verticalLayout_2.addWidget(self.le_reduce_debt)


        self.verticalLayout.addWidget(self.central_widget)


        self.retranslateUi(ProductsBalance)

        QMetaObject.connectSlotsByName(ProductsBalance)
    # setupUi

    def retranslateUi(self, ProductsBalance):
        ProductsBalance.setWindowTitle(QCoreApplication.translate("ProductsBalance", u"Dialog", None))
#if QT_CONFIG(tooltip)
        ProductsBalance.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.search_bar.setPlaceholderText(QCoreApplication.translate("ProductsBalance", u"Escribir t\u00e9rminos a buscar...", None))
        self.le_reduce_debt.setPlaceholderText(QCoreApplication.translate("ProductsBalance", u"Descontar del saldo de productos seleccionados...", None))
    # retranslateUi

