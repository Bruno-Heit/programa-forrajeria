# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'saleDialog.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QAbstractSpinBox, QApplication, QCheckBox,
    QComboBox, QDateTimeEdit, QDialog, QDialogButtonBox,
    QFrame, QGridLayout, QHBoxLayout, QLabel,
    QLineEdit, QSizePolicy, QVBoxLayout, QWidget)

class Ui_saleDialog(object):
    def setupUi(self, saleDialog):
        if not saleDialog.objectName():
            saleDialog.setObjectName(u"saleDialog")
        saleDialog.resize(555, 428)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(saleDialog.sizePolicy().hasHeightForWidth())
        saleDialog.setSizePolicy(sizePolicy)
        saleDialog.setMinimumSize(QSize(555, 428))
        saleDialog.setMaximumSize(QSize(555, 428))
        saleDialog.setStyleSheet(u"* {\n"
"	color: #111;\n"
"	border-color: #0b7e7f;\n"
"	font-family: \"Futura\", \"Verdana\", \"Sans-Serif\";\n"
"	font-size: 16px;\n"
"}\n"
"\n"
"\n"
"QToolTip {\n"
"	background-color: #fff;\n"
"	color: #0d1b2a;\n"
"}\n"
"\n"
"\n"
"QDialog {\n"
"	background-color: #e0e1dd;\n"
"}\n"
"\n"
"\n"
"#sale_data,\n"
"#debtor_data {\n"
"	background-color: #fff;\n"
"	padding: 5px 3px;\n"
"	border-radius: 10px;\n"
"}\n"
"\n"
"\n"
"#sale_data {\n"
"	margin-bottom: 10px;\n"
"}\n"
"\n"
"\n"
"/* labels */\n"
"QLabel {\n"
"	padding-right: 2px;\n"
"	padding-left: 2px;\n"
"}\n"
"\n"
"\n"
"#label_productTotalCost {\n"
"	font-size: 19px;\n"
"	font-weight: 900;\n"
"	background-color: #0d1b2a;\n"
"	color: #e0e1dd;\n"
"}\n"
"\n"
"\n"
"#label_productName_feedback,\n"
"#label_productQuantity_feedback,\n"
"#label_totalPaid_feedback,\n"
"#label_debtorName_feedback,\n"
"#label_debtorSurname_feedback,\n"
"#label_phoneNumber_feedback,\n"
"#label_postalCode_feedback {\n"
"	background-color: #F65755;\n"
"	color: #fff;\n"
"	border-radius: 5px;"
                        "\n"
"}\n"
"\n"
"\n"
"#label_debtor_header {\n"
"	font-family: \"Arial\", \"Calibri\", \"Sans-Serif\";\n"
"	font-size: 18px;\n"
"	font-weight: 600px;\n"
"}\n"
"\n"
"\n"
"/* lineedits */\n"
"#lineEdit_direction:disabled,\n"
"#lineEdit_phoneNumber:disabled,\n"
"#lineEdit_postalCode:disabled {\n"
"	background-color: #e0e1dd;\n"
"	color: #0d1b2a;\n"
"}\n"
"\n"
"\n"
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
"/* pushbuttons */\n"
"QPushButton {\n"
"	background-color: #415a77;\n"
"	color: #fff;\n"
"	border: none;\n"
"	border-radius: 4px;\n"
"	width: 220px;\n"
"	height: 30px;\n"
"}\n"
"QPushButton:hover,\n"
"QPushButton:focus {\n"
"	background-color: #3b66ab;\n"
"}\n"
"QPushButton:pressed {\n"
"	background-color: #3b66ab;\n"
"	border: 1px inset #778da9;\n"
"}\n"
"QPushButton:disabled {\n"
"	background-color:"
                        " rgb(103, 115, 122);\n"
"	color: #999;\n"
"}\n"
"\n"
"\n"
"/* combobox */\n"
"QComboBox {\n"
"	background-color: #e0e1dd;\n"
"	color: #0d1b2a;\n"
"	border: 1px solid #3b66ab;\n"
"	border-radius: 5px;\n"
"	padding-left: 2px 0;\n"
"}\n"
"QComboBox:on {\n"
"	background-color: #3b66ab;\n"
"	color: #fff;\n"
"	border: none;\n"
"	padding-top: 3px;\n"
"	padding-left: 4px;\n"
"}\n"
"QComboBox::drop-down {\n"
"	subcontrol-origin: padding;\n"
"	subcontrol-position: top right;\n"
"	width: 20px;\n"
"	padding-right: 3px;\n"
"	border-left: none;\n"
"	border-top-right-radius: 5px;\n"
"	border-bottom-right-radius: 5px;\n"
"}\n"
"QComboBox::down-arrow:on {\n"
"    top: 1px;\n"
"    left: 1px;\n"
"}\n"
"QComboBox QAbstractItemView{\n"
"	background-color: #778da9;\n"
"	color: #fff;\n"
"	selection-background-color: #3b66ab;\n"
"}\n"
"QComboBox:disabled {\n"
"	background-color: rgb(103, 115, 122);\n"
"	color: #999;\n"
"}\n"
"\n"
"\n"
"/* datetimeedit y calendar */\n"
"QDateTimeEdit {\n"
"	background-color: #fff;\n"
"}\n"
"QCalendar"
                        "Widget QAbstractItemView {\n"
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
"QSc"
                        "rollBar::sub-page:vertical {\n"
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
        self.verticalLayout = QVBoxLayout(saleDialog)
        self.verticalLayout.setSpacing(4)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)
        self.sale_data = QFrame(saleDialog)
        self.sale_data.setObjectName(u"sale_data")
        self.sale_data.setMinimumSize(QSize(545, 277))
        self.sale_data.setMaximumSize(QSize(16777215, 277))
        self.sale_data.setFrameShape(QFrame.Shape.NoFrame)
        self.sale_data.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.sale_data)
        self.verticalLayout_2.setSpacing(8)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.frame_saleDetail = QFrame(self.sale_data)
        self.frame_saleDetail.setObjectName(u"frame_saleDetail")
        self.frame_saleDetail.setMinimumSize(QSize(0, 21))
        self.frame_saleDetail.setMaximumSize(QSize(16777215, 21))
        self.frame_saleDetail.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_saleDetail.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame_saleDetail)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.label_saleDetail = QLabel(self.frame_saleDetail)
        self.label_saleDetail.setObjectName(u"label_saleDetail")
        self.label_saleDetail.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout.addWidget(self.label_saleDetail)

        self.lineEdit_saleDetail = QLineEdit(self.frame_saleDetail)
        self.lineEdit_saleDetail.setObjectName(u"lineEdit_saleDetail")
        self.lineEdit_saleDetail.setPlaceholderText(u"(Opcional) descripci\u00f3n de la venta")

        self.horizontalLayout.addWidget(self.lineEdit_saleDetail)

        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 2)

        self.verticalLayout_2.addWidget(self.frame_saleDetail)

        self.product_data = QFrame(self.sale_data)
        self.product_data.setObjectName(u"product_data")
        self.product_data.setMinimumSize(QSize(0, 145))
        self.product_data.setMaximumSize(QSize(16777215, 145))
        self.product_data.setFrameShape(QFrame.Shape.NoFrame)
        self.product_data.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout = QGridLayout(self.product_data)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.label_productQuantity = QLabel(self.product_data)
        self.label_productQuantity.setObjectName(u"label_productQuantity")
        self.label_productQuantity.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_productQuantity, 2, 0, 1, 1)

        self.comboBox_productName = QComboBox(self.product_data)
        self.comboBox_productName.setObjectName(u"comboBox_productName")
#if QT_CONFIG(tooltip)
        self.comboBox_productName.setToolTip(u"<html><head/><body><p><span style=\" font-size:11pt;\">El nombre del producto vendido.</span></p><p><span style=\" font-size:11pt; font-weight:600; text-decoration: underline;\">NOTA:</span><span style=\" font-size:11pt;\"> en caso de buscar un producto que no est\u00e1 en esta lista de productos se debe agregar ese producto antes a la base de datos mediante la secci\u00f3n de </span><span style=\" font-size:11pt; font-style:italic;\">INVENTARIO.</span></p></body></html>")
#endif // QT_CONFIG(tooltip)
        self.comboBox_productName.setEditable(True)
        self.comboBox_productName.setCurrentText(u"")
        self.comboBox_productName.setFrame(False)

        self.gridLayout.addWidget(self.comboBox_productName, 0, 1, 1, 1)

        self.label_productQuantity_feedback = QLabel(self.product_data)
        self.label_productQuantity_feedback.setObjectName(u"label_productQuantity_feedback")
        self.label_productQuantity_feedback.setMaximumSize(QSize(16777215, 20))
        self.label_productQuantity_feedback.setText(u"")
        self.label_productQuantity_feedback.setTextFormat(Qt.TextFormat.PlainText)
        self.label_productQuantity_feedback.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_productQuantity_feedback.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        self.gridLayout.addWidget(self.label_productQuantity_feedback, 4, 0, 1, 2, Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignTop)

        self.label_productName_feedback = QLabel(self.product_data)
        self.label_productName_feedback.setObjectName(u"label_productName_feedback")
        self.label_productName_feedback.setMaximumSize(QSize(16777215, 20))
        self.label_productName_feedback.setText(u"")
        self.label_productName_feedback.setTextFormat(Qt.TextFormat.PlainText)
        self.label_productName_feedback.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_productName_feedback.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        self.gridLayout.addWidget(self.label_productName_feedback, 1, 0, 1, 2, Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignTop)

        self.label_productName = QLabel(self.product_data)
        self.label_productName.setObjectName(u"label_productName")
        self.label_productName.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_productName, 0, 0, 1, 1)

        self.lineEdit_productQuantity = QLineEdit(self.product_data)
        self.lineEdit_productQuantity.setObjectName(u"lineEdit_productQuantity")
#if QT_CONFIG(tooltip)
        self.lineEdit_productQuantity.setToolTip(u"<html><head/><body><p><span style=\" font-size:11pt;\">La cantidad del producto vendido.</span></p><p><span style=\" font-size:11pt;\">Admite valores decimales.</span></p></body></html>")
#endif // QT_CONFIG(tooltip)
        self.lineEdit_productQuantity.setPlaceholderText(u"Cantidad vendida. Ej.: 5")
        self.lineEdit_productQuantity.setClearButtonEnabled(True)

        self.gridLayout.addWidget(self.lineEdit_productQuantity, 2, 1, 1, 1)

        self.checkBox_comercialPrice = QCheckBox(self.product_data)
        self.checkBox_comercialPrice.setObjectName(u"checkBox_comercialPrice")
#if QT_CONFIG(tooltip)
        self.checkBox_comercialPrice.setToolTip(u"<html><head/><body><p><span style=\" font-size:11pt;\">Si la casilla est\u00e1 </span><span style=\" font-size:11pt; font-weight:700;\">marcada</span><span style=\" font-size:11pt;\"> el precio calculado del producto es en base al </span><span style=\" font-size:11pt; font-weight:700;\">precio comercial</span><span style=\" font-size:11pt;\">.</span></p></body></html>")
#endif // QT_CONFIG(tooltip)
        self.checkBox_comercialPrice.setText(u"precio comercial")
#if QT_CONFIG(shortcut)
        self.checkBox_comercialPrice.setShortcut(u"")
#endif // QT_CONFIG(shortcut)
        self.checkBox_comercialPrice.setChecked(False)

        self.gridLayout.addWidget(self.checkBox_comercialPrice, 3, 1, 1, 1)

        self.label_productTotalCost = QLabel(self.product_data)
        self.label_productTotalCost.setObjectName(u"label_productTotalCost")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_productTotalCost.sizePolicy().hasHeightForWidth())
        self.label_productTotalCost.setSizePolicy(sizePolicy1)
        self.label_productTotalCost.setMinimumSize(QSize(0, 23))
        self.label_productTotalCost.setMaximumSize(QSize(16777215, 23))
        self.label_productTotalCost.setText(u"COSTO TOTAL")
        self.label_productTotalCost.setTextFormat(Qt.TextFormat.AutoText)
        self.label_productTotalCost.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.label_productTotalCost.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

        self.gridLayout.addWidget(self.label_productTotalCost, 5, 1, 1, 1)

        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 2)

        self.verticalLayout_2.addWidget(self.product_data)

        self.frame_totalPaid = QFrame(self.sale_data)
        self.frame_totalPaid.setObjectName(u"frame_totalPaid")
        self.frame_totalPaid.setMinimumSize(QSize(0, 44))
        self.frame_totalPaid.setMaximumSize(QSize(16777215, 44))
        self.frame_totalPaid.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_totalPaid.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_2 = QGridLayout(self.frame_totalPaid)
        self.gridLayout_2.setSpacing(4)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label_totalPaid = QLabel(self.frame_totalPaid)
        self.label_totalPaid.setObjectName(u"label_totalPaid")
        self.label_totalPaid.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.label_totalPaid, 0, 0, 1, 1)

        self.lineEdit_totalPaid = QLineEdit(self.frame_totalPaid)
        self.lineEdit_totalPaid.setObjectName(u"lineEdit_totalPaid")
#if QT_CONFIG(tooltip)
        self.lineEdit_totalPaid.setToolTip(u"<html><head/><body><p><span style=\" font-size:11pt;\">El valor total abonado en esta venta.</span></p><p><span style=\" font-size:11pt; font-weight:600; text-decoration: underline;\">NOTA:</span><span style=\" font-size:11pt;\"> si es diferente al costo se pedir\u00e1n los datos del comprador y la diferencia se agregar\u00e1 a la base de datos como saldo a favor/adeudado.</span></p></body></html>")
#endif // QT_CONFIG(tooltip)
        self.lineEdit_totalPaid.setPlaceholderText(u"Total abonado. Ej.: 15000")
        self.lineEdit_totalPaid.setClearButtonEnabled(True)

        self.gridLayout_2.addWidget(self.lineEdit_totalPaid, 0, 1, 1, 1)

        self.label_totalPaid_feedback = QLabel(self.frame_totalPaid)
        self.label_totalPaid_feedback.setObjectName(u"label_totalPaid_feedback")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_totalPaid_feedback.sizePolicy().hasHeightForWidth())
        self.label_totalPaid_feedback.setSizePolicy(sizePolicy2)
        self.label_totalPaid_feedback.setMaximumSize(QSize(16777215, 20))
        self.label_totalPaid_feedback.setText(u"")
        self.label_totalPaid_feedback.setTextFormat(Qt.TextFormat.PlainText)
        self.label_totalPaid_feedback.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_totalPaid_feedback.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        self.gridLayout_2.addWidget(self.label_totalPaid_feedback, 1, 0, 1, 2, Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignTop)

        self.gridLayout_2.setColumnStretch(0, 1)
        self.gridLayout_2.setColumnStretch(1, 2)

        self.verticalLayout_2.addWidget(self.frame_totalPaid)

        self.dateTimeEdit = QDateTimeEdit(self.sale_data)
        self.dateTimeEdit.setObjectName(u"dateTimeEdit")
        self.dateTimeEdit.setMinimumSize(QSize(0, 23))
        self.dateTimeEdit.setMaximumSize(QSize(16777215, 23))
#if QT_CONFIG(tooltip)
        self.dateTimeEdit.setToolTip(u"<html><head/><body><p><span style=\" font-size:11pt;\">Fecha y hora de la venta.</span></p></body></html>")
#endif // QT_CONFIG(tooltip)
        self.dateTimeEdit.setFrame(True)
        self.dateTimeEdit.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.UpDownArrows)
        self.dateTimeEdit.setProperty("showGroupSeparator", False)
        self.dateTimeEdit.setDate(QDate(2023, 12, 13))
        self.dateTimeEdit.setMinimumDateTime(QDateTime(QDate(2022, 1, 1), QTime(0, 0, 0)))
        self.dateTimeEdit.setDisplayFormat(u"d/M/yyyy HH:mm:ss")
        self.dateTimeEdit.setCalendarPopup(True)

        self.verticalLayout_2.addWidget(self.dateTimeEdit)


        self.verticalLayout.addWidget(self.sale_data)

        self.debtor_data = QFrame(saleDialog)
        self.debtor_data.setObjectName(u"debtor_data")
        self.debtor_data.setEnabled(False)
        self.debtor_data.setMinimumSize(QSize(0, 97))
        self.debtor_data.setMaximumSize(QSize(16777215, 97))
        self.debtor_data.setFrameShape(QFrame.Shape.NoFrame)
        self.debtor_data.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.debtor_data)
        self.verticalLayout_3.setSpacing(8)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 5, 0, 5)
        self.label_debtor_header = QLabel(self.debtor_data)
        self.label_debtor_header.setObjectName(u"label_debtor_header")
        sizePolicy1.setHeightForWidth(self.label_debtor_header.sizePolicy().hasHeightForWidth())
        self.label_debtor_header.setSizePolicy(sizePolicy1)
        self.label_debtor_header.setMinimumSize(QSize(0, 25))
        self.label_debtor_header.setMaximumSize(QSize(16777215, 25))
#if QT_CONFIG(tooltip)
        self.label_debtor_header.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.label_debtor_header.setText(u"Cuenta corriente")
        self.label_debtor_header.setTextFormat(Qt.TextFormat.PlainText)
        self.label_debtor_header.setScaledContents(False)
        self.label_debtor_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_debtor_header.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        self.verticalLayout_3.addWidget(self.label_debtor_header)

        self.frame_debtor_name = QFrame(self.debtor_data)
        self.frame_debtor_name.setObjectName(u"frame_debtor_name")
        self.frame_debtor_name.setMinimumSize(QSize(0, 23))
        self.frame_debtor_name.setMaximumSize(QSize(16777215, 23))
        self.frame_debtor_name.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_debtor_name.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_debtor_name)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label_debtor_name = QLabel(self.frame_debtor_name)
        self.label_debtor_name.setObjectName(u"label_debtor_name")
        sizePolicy1.setHeightForWidth(self.label_debtor_name.sizePolicy().hasHeightForWidth())
        self.label_debtor_name.setSizePolicy(sizePolicy1)
        self.label_debtor_name.setTextFormat(Qt.TextFormat.RichText)
        self.label_debtor_name.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_3.addWidget(self.label_debtor_name)

        self.cb_debtor_name = QComboBox(self.frame_debtor_name)
        self.cb_debtor_name.setObjectName(u"cb_debtor_name")
        sizePolicy1.setHeightForWidth(self.cb_debtor_name.sizePolicy().hasHeightForWidth())
        self.cb_debtor_name.setSizePolicy(sizePolicy1)
        self.cb_debtor_name.setEditable(True)
        self.cb_debtor_name.setPlaceholderText(u"")

        self.horizontalLayout_3.addWidget(self.cb_debtor_name)

        self.horizontalLayout_3.setStretch(0, 1)
        self.horizontalLayout_3.setStretch(1, 2)

        self.verticalLayout_3.addWidget(self.frame_debtor_name)

        self.frame_debtor_surname = QFrame(self.debtor_data)
        self.frame_debtor_surname.setObjectName(u"frame_debtor_surname")
        self.frame_debtor_surname.setMinimumSize(QSize(0, 23))
        self.frame_debtor_surname.setMaximumSize(QSize(16777215, 23))
        self.frame_debtor_surname.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_debtor_surname.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_debtor_surname)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label_debtor_surname = QLabel(self.frame_debtor_surname)
        self.label_debtor_surname.setObjectName(u"label_debtor_surname")
        sizePolicy1.setHeightForWidth(self.label_debtor_surname.sizePolicy().hasHeightForWidth())
        self.label_debtor_surname.setSizePolicy(sizePolicy1)
        self.label_debtor_surname.setTextFormat(Qt.TextFormat.RichText)
        self.label_debtor_surname.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_2.addWidget(self.label_debtor_surname)

        self.cb_debtor_surname = QComboBox(self.frame_debtor_surname)
        self.cb_debtor_surname.setObjectName(u"cb_debtor_surname")
        sizePolicy1.setHeightForWidth(self.cb_debtor_surname.sizePolicy().hasHeightForWidth())
        self.cb_debtor_surname.setSizePolicy(sizePolicy1)
        self.cb_debtor_surname.setEditable(True)
        self.cb_debtor_surname.setPlaceholderText(u"")
        self.cb_debtor_surname.setFrame(True)

        self.horizontalLayout_2.addWidget(self.cb_debtor_surname)

        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 2)

        self.verticalLayout_3.addWidget(self.frame_debtor_surname)


        self.verticalLayout.addWidget(self.debtor_data)

        self.buttonBox = QDialogButtonBox(saleDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setMinimumSize(QSize(0, 30))
        self.buttonBox.setMaximumSize(QSize(16777215, 30))
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setCenterButtons(True)

        self.verticalLayout.addWidget(self.buttonBox)

        QWidget.setTabOrder(self.lineEdit_saleDetail, self.comboBox_productName)
        QWidget.setTabOrder(self.comboBox_productName, self.lineEdit_productQuantity)
        QWidget.setTabOrder(self.lineEdit_productQuantity, self.checkBox_comercialPrice)
        QWidget.setTabOrder(self.checkBox_comercialPrice, self.lineEdit_totalPaid)
        QWidget.setTabOrder(self.lineEdit_totalPaid, self.dateTimeEdit)

        self.retranslateUi(saleDialog)
        self.buttonBox.accepted.connect(saleDialog.accept)
        self.buttonBox.rejected.connect(saleDialog.reject)

        QMetaObject.connectSlotsByName(saleDialog)
    # setupUi

    def retranslateUi(self, saleDialog):
        saleDialog.setWindowTitle(QCoreApplication.translate("saleDialog", u"Dialog", None))
        self.label_saleDetail.setText(QCoreApplication.translate("saleDialog", u"Detalle de la venta", None))
        self.label_productQuantity.setText(QCoreApplication.translate("saleDialog", u"<html><head/><body><p>Cantidad  <span style=\" color:#ff0000;\">*</span></p></body></html>", None))
        self.comboBox_productName.setPlaceholderText(QCoreApplication.translate("saleDialog", u"Elegir el producto...", None))
        self.label_productName.setText(QCoreApplication.translate("saleDialog", u"<html><head/><body><p>Producto <span style=\" color:#ff0000;\">*</span></p></body></html>", None))
        self.label_totalPaid.setText(QCoreApplication.translate("saleDialog", u"<html><head/><body><p>Total abonado  <span style=\" color:#ff0000;\">*</span></p></body></html>", None))
#if QT_CONFIG(tooltip)
        self.frame_debtor_name.setToolTip(QCoreApplication.translate("saleDialog", u"<html><head/><body><p><span style=\" font-size:11pt;\">El nombre del propietario de la cuenta corriente.</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_debtor_name.setText(QCoreApplication.translate("saleDialog", u"<html><head/><body><p>Nombre <span style=\" color:#ff0000;\">*</span></p></body></html>", None))
#if QT_CONFIG(tooltip)
        self.frame_debtor_surname.setToolTip(QCoreApplication.translate("saleDialog", u"<html><head/><body><p><span style=\" font-size:11pt;\">El apellido del propietario de la cuenta corriente.</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_debtor_surname.setText(QCoreApplication.translate("saleDialog", u"<html><head/><body><p>Apellido <span style=\" color:#ff0000;\">*</span></p></body></html>", None))
    # retranslateUi

