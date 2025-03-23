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
from PySide6.QtWidgets import (QAbstractItemView, QAbstractScrollArea, QApplication, QCheckBox,
    QDialog, QFrame, QHBoxLayout, QHeaderView,
    QLineEdit, QPushButton, QSizePolicy, QTableView,
    QVBoxLayout, QWidget)

class Ui_ProductsBalance(object):
    def setupUi(self, ProductsBalance):
        if not ProductsBalance.objectName():
            ProductsBalance.setObjectName(u"ProductsBalance")
        ProductsBalance.resize(400, 160)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ProductsBalance.sizePolicy().hasHeightForWidth())
        ProductsBalance.setSizePolicy(sizePolicy)
        ProductsBalance.setMinimumSize(QSize(400, 160))
        ProductsBalance.setMaximumSize(QSize(400, 16777215))
        ProductsBalance.setWindowOpacity(1.000000000000000)
        ProductsBalance.setStyleSheet(u"* {\n"
"	color: #111;\n"
"	border-color: #0b7e7f;\n"
"	font-family: \"Futura\", \"Verdana\", \"Sans-Serif\";\n"
"	font-size: 14px;\n"
"}\n"
"\n"
"\n"
"#central_widget {\n"
"	background-color: #415a77;\n"
"	border-radius: 5px;\n"
"}\n"
"\n"
"\n"
"QToolTip {\n"
"	background-color: #fff;\n"
"	color: #0d1b2a;\n"
"}\n"
"\n"
"\n"
"/* checkbox */\n"
"QCheckBox {\n"
"	color: #fff;\n"
"	spacing: 5px;\n"
"}\n"
"\n"
"\n"
"/* pushbutton */\n"
"QPushButton {\n"
"	color: #fff;\n"
"	background-color: #415a77;\n"
"	border: None;\n"
"	border-radius: 4px;\n"
"}\n"
"QPushButton:hover,\n"
"QPushButton:pressed {\n"
"	background-color: #faa;\n"
"}\n"
"QPushButton:pressed {\n"
"	border: 1px inset #778da9;\n"
"}\n"
"QPushButton:disabled {\n"
"	color: #999;\n"
"}\n"
"\n"
"\n"
"/* tableview y headers */\n"
"QTableView {\n"
"	color: #0d1b2a;\n"
"	background-color: #fff;\n"
"	border: None;\n"
"	border-radius: 10px;\n"
"}\n"
"QTableView::item:hover {\n"
"	background-color: #778da9;\n"
"}\n"
"QTableView::item:selected {\n"
"	background-col"
                        "or: #778da9;\n"
"	border: 1px solid #fff;\n"
"}\n"
"/* QHeaderViews */\n"
"QHeaderView::section {\n"
"	background-color: #778da9;\n"
"	color: #fff;\n"
"	border: none;\n"
"	border-right: 1px solid;\n"
"	border-bottom: 1px solid;\n"
"	border-color: #e0e1dd;\n"
"}\n"
"\n"
"\n"
"/* lineedits */\n"
"QLineEdit {\n"
"	background-color: #e0e1dd;\n"
"	color: #0d1b2a;\n"
"	border: none;\n"
"	border-radius: 10px;\n"
"	padding-left: 3px;\n"
"	padding-right: 3px;\n"
"}\n"
"QLineEdit:focus {\n"
"	background-color: #3b66ab;\n"
"	color: #fff;\n"
"}\n"
"\n"
"\n"
"/* QDateTimeEdit y del QCalendarWidget */\n"
"QDateTimeEdit {\n"
"	background-color: #fff;\n"
"}\n"
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
"/* scrollbars */\n"
""
                        "QScrollBar {\n"
"	background-color: #e0e1dd;\n"
"	border: 1px solid transparent;\n"
"	border-radius: 5px;\n"
"}\n"
"QScrollBar:groove {\n"
"	border-radius: 5px;\n"
"}\n"
"QScrollBar::handle {\n"
"	background-color:  #1b263b;\n"
"	border-radius: 5px;\n"
"}\n"
"QScrollBar::handle:pressed {\n"
"	background-color: #3b465b;\n"
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
"}")
        self.horizontalLayout_4 = QHBoxLayout(ProductsBalance)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.central_widget = QWidget(ProductsBalance)
        self.central_widget.setObjectName(u"central_widget")
        self.central_widget.setMinimumSize(QSize(0, 160))
        self.verticalLayout_2 = QVBoxLayout(self.central_widget)
        self.verticalLayout_2.setSpacing(8)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(5, 5, 5, 5)
        self.header = QWidget(self.central_widget)
        self.header.setObjectName(u"header")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.header.sizePolicy().hasHeightForWidth())
        self.header.setSizePolicy(sizePolicy1)
        self.header.setMinimumSize(QSize(0, 24))
        self.header.setMaximumSize(QSize(16777215, 24))
        self.horizontalLayout = QHBoxLayout(self.header)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(30, 0, 30, 0)
        self.search_bar = QLineEdit(self.header)
        self.search_bar.setObjectName(u"search_bar")
        sizePolicy1.setHeightForWidth(self.search_bar.sizePolicy().hasHeightForWidth())
        self.search_bar.setSizePolicy(sizePolicy1)
        self.search_bar.setMinimumSize(QSize(0, 24))
        self.search_bar.setMaximumSize(QSize(16777215, 24))
        self.search_bar.setFrame(False)
        self.search_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.search_bar.setClearButtonEnabled(True)

        self.horizontalLayout.addWidget(self.search_bar)


        self.verticalLayout_2.addWidget(self.header)

        self.body = QWidget(self.central_widget)
        self.body.setObjectName(u"body")
        self.body.setMinimumSize(QSize(0, 86))
        self.verticalLayout_3 = QVBoxLayout(self.body)
        self.verticalLayout_3.setSpacing(5)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 10)
        self.tv_balance_products = QTableView(self.body)
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

        self.verticalLayout_3.addWidget(self.tv_balance_products)

        self.lower_body = QWidget(self.body)
        self.lower_body.setObjectName(u"lower_body")
        sizePolicy1.setHeightForWidth(self.lower_body.sizePolicy().hasHeightForWidth())
        self.lower_body.setSizePolicy(sizePolicy1)
        self.lower_body.setMinimumSize(QSize(0, 24))
        self.lower_body.setMaximumSize(QSize(16777215, 24))
        self.horizontalLayout_3 = QHBoxLayout(self.lower_body)
        self.horizontalLayout_3.setSpacing(4)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.checkbox_show_all_products = QCheckBox(self.lower_body)
        self.checkbox_show_all_products.setObjectName(u"checkbox_show_all_products")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.checkbox_show_all_products.sizePolicy().hasHeightForWidth())
        self.checkbox_show_all_products.setSizePolicy(sizePolicy3)
        self.checkbox_show_all_products.setMinimumSize(QSize(0, 24))
        self.checkbox_show_all_products.setMaximumSize(QSize(16777215, 24))
#if QT_CONFIG(tooltip)
        self.checkbox_show_all_products.setToolTip(u"<html><head/><body><p>Muestra <span style=\" font-weight:700;\">todos los productos</span> que el cliente haya tenido en su cuenta corriente.</p><p><br/>\u00c9sto es \u00fatil para, por ejemplo, realizar correcciones sobre cambios hechos en detalles de alg\u00fan producto que no se debieron haber realizado, como eliminar una deuda incorrecta o ingresar mal una fecha.</p></body></html>")
#endif // QT_CONFIG(tooltip)
        self.checkbox_show_all_products.setIconSize(QSize(24, 24))

        self.horizontalLayout_3.addWidget(self.checkbox_show_all_products)

        self.btn_delete_debt = QPushButton(self.lower_body)
        self.btn_delete_debt.setObjectName(u"btn_delete_debt")
        self.btn_delete_debt.setEnabled(False)
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.btn_delete_debt.sizePolicy().hasHeightForWidth())
        self.btn_delete_debt.setSizePolicy(sizePolicy4)
        self.btn_delete_debt.setMinimumSize(QSize(24, 24))
        self.btn_delete_debt.setMaximumSize(QSize(24, 24))
        self.btn_delete_debt.setIconSize(QSize(24, 24))
        self.btn_delete_debt.setFlat(False)

        self.horizontalLayout_3.addWidget(self.btn_delete_debt, 0, Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignVCenter)


        self.verticalLayout_3.addWidget(self.lower_body)


        self.verticalLayout_2.addWidget(self.body)

        self.footer = QWidget(self.central_widget)
        self.footer.setObjectName(u"footer")
        sizePolicy1.setHeightForWidth(self.footer.sizePolicy().hasHeightForWidth())
        self.footer.setSizePolicy(sizePolicy1)
        self.footer.setMinimumSize(QSize(0, 24))
        self.footer.setMaximumSize(QSize(16777215, 24))
        self.horizontalLayout_2 = QHBoxLayout(self.footer)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(15, 0, 15, 0)
        self.le_reduce_debt = QLineEdit(self.footer)
        self.le_reduce_debt.setObjectName(u"le_reduce_debt")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.le_reduce_debt.sizePolicy().hasHeightForWidth())
        self.le_reduce_debt.setSizePolicy(sizePolicy5)
        self.le_reduce_debt.setMinimumSize(QSize(0, 24))
        self.le_reduce_debt.setMaximumSize(QSize(16777215, 24))
#if QT_CONFIG(tooltip)
        self.le_reduce_debt.setToolTip(u"<html><head/><body><p>Descuenta la cantidad especificada de los productos seleccionados en <span style=\" font-weight:700;\">orden de selecci\u00f3n</span>. Si no hay productos seleccionados, descuenta desde el primero al \u00faltimo en <span style=\" font-weight:700;\">orden de aparici\u00f3n</span>.</p></body></html>")
#endif // QT_CONFIG(tooltip)
        self.le_reduce_debt.setFrame(False)
        self.le_reduce_debt.setClearButtonEnabled(True)

        self.horizontalLayout_2.addWidget(self.le_reduce_debt)


        self.verticalLayout_2.addWidget(self.footer)


        self.horizontalLayout_4.addWidget(self.central_widget)


        self.retranslateUi(ProductsBalance)

        QMetaObject.connectSlotsByName(ProductsBalance)
    # setupUi

    def retranslateUi(self, ProductsBalance):
        ProductsBalance.setWindowTitle(QCoreApplication.translate("ProductsBalance", u"Dialog", None))
#if QT_CONFIG(tooltip)
        ProductsBalance.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.search_bar.setToolTip(QCoreApplication.translate("ProductsBalance", u"<html><head/><body><p>Realiza b\u00fasquedas en la tabla de productos en cuenta corriente.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.search_bar.setPlaceholderText(QCoreApplication.translate("ProductsBalance", u"Buscar ventas por fecha, cantidad, etc...", None))
        self.checkbox_show_all_products.setText(QCoreApplication.translate("ProductsBalance", u"Mostrar historial de productos", None))
#if QT_CONFIG(tooltip)
        self.btn_delete_debt.setToolTip(QCoreApplication.translate("ProductsBalance", u"<html><head/><body><p><span style=\" font-size:11pt;\">Elimina la cantidad adeudada/a favor del producto actualmente seleccionado en la tabla.</span></p><p><span style=\" font-size:11pt;\">\u00c9ste m\u00e9todo no elimina para siempre los productos, sino que considera la cantidad como saldada.</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.btn_delete_debt.setText("")
        self.le_reduce_debt.setPlaceholderText(QCoreApplication.translate("ProductsBalance", u"Descontar del saldo de productos seleccionados...", None))
    # retranslateUi

