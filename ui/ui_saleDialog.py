# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'saleDialog.ui'
##
## Created by: Qt User Interface Compiler version 6.5.3
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
        saleDialog.resize(615, 295)
        saleDialog.setMinimumSize(QSize(615, 295))
        saleDialog.setStyleSheet(u"* {\n"
"	color: #111;\n"
"	border-color: #0b7e7f;\n"
"	font-family: \"Tahoma\", \"Verdana\", \"Sans-Serif\";\n"
"	font-size: 16px;\n"
"}\n"
"\n"
"\n"
"QDialog {\n"
"	background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(255, 178, 102, 255), stop:0.378531 rgba(230, 177, 61, 255), stop:0.745763 rgba(232, 105, 57, 255), stop:0.982955 rgba(255, 180, 128, 255));\n"
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
"	color: #dc2627;\n"
"	border: 1px solid #dc2627;\n"
"	background-color: rgba(224,164,164,0.7)\n"
"}\n"
"\n"
"\n"
"#lineEdit_direction:disabled,\n"
"#lineEdit_phoneNumber:disabled,\n"
"#lineEdit_postalCode:disabled {\n"
"	background-color: rgba(204, 204, 204, 0.6);\n"
"	color: #888;\n"
"}\n"
"\n"
"\n"
"QLineEdit {\n"
"	background-color: #fff;\n"
"	border: none;\n"
"	border-top: 1px"
                        " solid;\n"
"	border-bottom: 1px solid;\n"
"	border-color: #0b7e7f;\n"
"	height: 24px;\n"
"}\n"
"QLineEdit:focus {\n"
"	background-color: rgb(197, 255, 252);\n"
"	border: 1px solid;\n"
"	border-color: #0b7e7f;\n"
"	font-size: 18px;\n"
"}\n"
"\n"
"\n"
"QPushButton {\n"
"	font-size: 16px;\n"
"	background-color: #22577a;\n"
"	color: #fff;\n"
"	border: 1px solid #12476a;\n"
"	border-radius: 2px;\n"
"	min-width: 200px;\n"
"	min-height: 23px;\n"
"}\n"
"QPushButton:hover,\n"
"QPushButton:pressed {\n"
"	background-color: #38a3a5;\n"
"	color: #111;\n"
"	border: 1px inset #289395;\n"
"}\n"
"QPushButton:disabled {\n"
"	background-color: rgb(103, 115, 122);\n"
"	color: #999;\n"
"}\n"
"\n"
"\n"
"/*cambia el estilo del combobox*/\n"
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
""
                        "	padding-top: 2px;\n"
"	padding-left: 4px;\n"
"}\n"
"QComboBox QAbstractItemView {\n"
"	background-color: #fff;\n"
"	selection-background-color: #38a3a5;\n"
"}")
        self.verticalLayout = QVBoxLayout(saleDialog)
        self.verticalLayout.setSpacing(4)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)
        self.sale_data = QFrame(saleDialog)
        self.sale_data.setObjectName(u"sale_data")
        self.sale_data.setStyleSheet(u"QScrollBar {\n"
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
"}")
        self.sale_data.setFrameShape(QFrame.NoFrame)
        self.sale_data.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.sale_data)
        self.verticalLayout_2.setSpacing(4)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.frame_saleDetail = QFrame(self.sale_data)
        self.frame_saleDetail.setObjectName(u"frame_saleDetail")
        self.frame_saleDetail.setFrameShape(QFrame.NoFrame)
        self.frame_saleDetail.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame_saleDetail)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.label_saleDetail = QLabel(self.frame_saleDetail)
        self.label_saleDetail.setObjectName(u"label_saleDetail")

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
        self.product_data.setFrameShape(QFrame.NoFrame)
        self.product_data.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.product_data)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.label_productQuantity = QLabel(self.product_data)
        self.label_productQuantity.setObjectName(u"label_productQuantity")

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
        self.label_productQuantity_feedback.setTextFormat(Qt.PlainText)
        self.label_productQuantity_feedback.setAlignment(Qt.AlignCenter)
        self.label_productQuantity_feedback.setTextInteractionFlags(Qt.NoTextInteraction)

        self.gridLayout.addWidget(self.label_productQuantity_feedback, 4, 0, 1, 2, Qt.AlignHCenter|Qt.AlignTop)

        self.label_productName_feedback = QLabel(self.product_data)
        self.label_productName_feedback.setObjectName(u"label_productName_feedback")
        self.label_productName_feedback.setMaximumSize(QSize(16777215, 20))
        self.label_productName_feedback.setText(u"")
        self.label_productName_feedback.setTextFormat(Qt.PlainText)
        self.label_productName_feedback.setAlignment(Qt.AlignCenter)
        self.label_productName_feedback.setTextInteractionFlags(Qt.NoTextInteraction)

        self.gridLayout.addWidget(self.label_productName_feedback, 1, 0, 1, 2, Qt.AlignHCenter|Qt.AlignTop)

        self.label_productName = QLabel(self.product_data)
        self.label_productName.setObjectName(u"label_productName")

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
        self.checkBox_comercialPrice.setToolTip(u"<html><head/><body><p><span style=\" font-size:11pt;\">Si la casilla est\u00e1 </span><span style=\" font-size:11pt; text-decoration: underline;\">desmarcada</span><span style=\" font-size:11pt;\"> el precio calculado del producto es en base al </span><span style=\" font-size:11pt; font-weight:600; text-decoration: underline;\">precio unitario</span><span style=\" font-size:11pt;\">.</span></p><p><span style=\" font-size:11pt;\">Si la casilla est\u00e1 </span><span style=\" font-size:11pt; text-decoration: underline;\">marcada</span><span style=\" font-size:11pt;\"> el precio total calculado se basa en el </span><span style=\" font-size:11pt; font-weight:600; text-decoration: underline;\">precio comercial</span><span style=\" font-size:11pt;\">.</span></p></body></html>")
#endif // QT_CONFIG(tooltip)
        self.checkBox_comercialPrice.setText(u"Aplicar precio comercial")
#if QT_CONFIG(shortcut)
        self.checkBox_comercialPrice.setShortcut(u"")
#endif // QT_CONFIG(shortcut)
        self.checkBox_comercialPrice.setChecked(False)

        self.gridLayout.addWidget(self.checkBox_comercialPrice, 3, 1, 1, 1)

        self.label_productTotalCost = QLabel(self.product_data)
        self.label_productTotalCost.setObjectName(u"label_productTotalCost")
        self.label_productTotalCost.setStyleSheet(u"font-size: 19px;\n"
"font-weight: 500;\n"
"background-color: #bbb;\n"
"border-top: 1px solid #111;\n"
"border-right: 1px solid #111;")
        self.label_productTotalCost.setText(u"COSTO TOTAL")
        self.label_productTotalCost.setTextFormat(Qt.AutoText)
        self.label_productTotalCost.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.label_productTotalCost.setTextInteractionFlags(Qt.TextSelectableByMouse)

        self.gridLayout.addWidget(self.label_productTotalCost, 5, 1, 1, 1)

        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 2)

        self.verticalLayout_2.addWidget(self.product_data)

        self.frame_totalPaid = QFrame(self.sale_data)
        self.frame_totalPaid.setObjectName(u"frame_totalPaid")
        self.frame_totalPaid.setFrameShape(QFrame.NoFrame)
        self.frame_totalPaid.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frame_totalPaid)
        self.gridLayout_2.setSpacing(4)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label_totalPaid = QLabel(self.frame_totalPaid)
        self.label_totalPaid.setObjectName(u"label_totalPaid")

        self.gridLayout_2.addWidget(self.label_totalPaid, 0, 0, 1, 1)

        self.lineEdit_totalPaid = QLineEdit(self.frame_totalPaid)
        self.lineEdit_totalPaid.setObjectName(u"lineEdit_totalPaid")
#if QT_CONFIG(tooltip)
        self.lineEdit_totalPaid.setToolTip(u"<html><head/><body><p><span style=\" font-size:11pt;\">El valor total que es abonado en esta compra.</span></p><p><span style=\" font-size:11pt; font-weight:600; text-decoration: underline;\">NOTA:</span><span style=\" font-size:11pt;\"> si es diferente al costo se pedir\u00e1n los datos del comprador y la diferencia se agregar\u00e1 a la base de datos como saldo a favor/en contra.</span></p></body></html>")
#endif // QT_CONFIG(tooltip)
        self.lineEdit_totalPaid.setPlaceholderText(u"Total abonado. Ej.: 15000")
        self.lineEdit_totalPaid.setClearButtonEnabled(True)

        self.gridLayout_2.addWidget(self.lineEdit_totalPaid, 0, 1, 1, 1)

        self.label_totalPaid_feedback = QLabel(self.frame_totalPaid)
        self.label_totalPaid_feedback.setObjectName(u"label_totalPaid_feedback")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_totalPaid_feedback.sizePolicy().hasHeightForWidth())
        self.label_totalPaid_feedback.setSizePolicy(sizePolicy)
        self.label_totalPaid_feedback.setMaximumSize(QSize(16777215, 20))
        self.label_totalPaid_feedback.setText(u"")
        self.label_totalPaid_feedback.setTextFormat(Qt.PlainText)
        self.label_totalPaid_feedback.setAlignment(Qt.AlignCenter)
        self.label_totalPaid_feedback.setTextInteractionFlags(Qt.NoTextInteraction)

        self.gridLayout_2.addWidget(self.label_totalPaid_feedback, 1, 0, 1, 2, Qt.AlignHCenter|Qt.AlignTop)

        self.gridLayout_2.setColumnStretch(0, 1)
        self.gridLayout_2.setColumnStretch(1, 2)

        self.verticalLayout_2.addWidget(self.frame_totalPaid)

        self.dateTimeEdit = QDateTimeEdit(self.sale_data)
        self.dateTimeEdit.setObjectName(u"dateTimeEdit")
#if QT_CONFIG(tooltip)
        self.dateTimeEdit.setToolTip(u"<html><head/><body><p><span style=\" font-size:11pt;\">Fecha y hora de la compra.</span></p><p><span style=\" font-size:11pt; font-weight:600; text-decoration: underline;\">NOTA:</span><span style=\" font-size:11pt;\"> no es necesario que sea exacta, pero por conveniencia debe ser al menos aproximada.</span></p></body></html>")
#endif // QT_CONFIG(tooltip)
        self.dateTimeEdit.setFrame(True)
        self.dateTimeEdit.setButtonSymbols(QAbstractSpinBox.UpDownArrows)
        self.dateTimeEdit.setProperty("showGroupSeparator", False)
        self.dateTimeEdit.setDate(QDate(2023, 12, 13))
        self.dateTimeEdit.setMinimumDateTime(QDateTime(QDate(2022, 1, 1), QTime(0, 0, 0)))
        self.dateTimeEdit.setDisplayFormat(uDATETIME_FORMAT)
        self.dateTimeEdit.setCalendarPopup(True)

        self.verticalLayout_2.addWidget(self.dateTimeEdit)


        self.verticalLayout.addWidget(self.sale_data)

        self.debtor_data = QFrame(saleDialog)
        self.debtor_data.setObjectName(u"debtor_data")
        self.debtor_data.setFrameShape(QFrame.NoFrame)
        self.debtor_data.setFrameShadow(QFrame.Raised)
        self.debtor_data_GridLayout = QGridLayout(self.debtor_data)
        self.debtor_data_GridLayout.setSpacing(4)
        self.debtor_data_GridLayout.setObjectName(u"debtor_data_GridLayout")
        self.debtor_data_GridLayout.setContentsMargins(0, 0, 0, 0)
        self.lineEdit_direction = QLineEdit(self.debtor_data)
        self.lineEdit_direction.setObjectName(u"lineEdit_direction")
#if QT_CONFIG(tooltip)
        self.lineEdit_direction.setToolTip(u"<html><head/><body><p><span style=\" font-size:11pt;\">(Opcional) direcci\u00f3n del deudor.</span></p><p><span style=\" font-size:11pt; font-weight:600; text-decoration: underline;\">NOTA:</span><span style=\" font-size:11pt;\"> si el deudor ya existe en la base de datos es recomendable </span><span style=\" font-size:11pt; text-decoration: underline;\">no llenar este campo</span><span style=\" font-size:11pt;\">, porque crear\u00e1 un registro diferente del mismo deudor.</span></p></body></html>")
#endif // QT_CONFIG(tooltip)
        self.lineEdit_direction.setInputMask(u"")
        self.lineEdit_direction.setText(u"")
        self.lineEdit_direction.setPlaceholderText(u"(Opcional) Ej.: Padre J.M. Criado Alonso 200")
        self.lineEdit_direction.setClearButtonEnabled(True)

        self.debtor_data_GridLayout.addWidget(self.lineEdit_direction, 6, 2, 1, 3)

        self.label_phoneNumber = QLabel(self.debtor_data)
        self.label_phoneNumber.setObjectName(u"label_phoneNumber")

        self.debtor_data_GridLayout.addWidget(self.label_phoneNumber, 3, 0, 1, 2)

        self.lineEdit_postalCode = QLineEdit(self.debtor_data)
        self.lineEdit_postalCode.setObjectName(u"lineEdit_postalCode")
#if QT_CONFIG(tooltip)
        self.lineEdit_postalCode.setToolTip(u"<html><head/><body><p><span style=\" font-size:11pt;\">(Opcional) c\u00f3digo postal del deudor.</span></p><p><span style=\" font-size:11pt; font-weight:600; text-decoration: underline;\">NOTA:</span><span style=\" font-size:11pt;\"> si el deudor ya existe en la base de datos es recomendable </span><span style=\" font-size:11pt; text-decoration: underline;\">no llenar este campo</span><span style=\" font-size:11pt;\">, porque crear\u00e1 un registro diferente del mismo deudor.</span></p><p><span style=\" font-size:11pt; font-weight:600; text-decoration: underline;\">NOTA:</span><span style=\" font-size:11pt;\"> por conveniencia s\u00f3lo admite c\u00f3digos postales de Argentina.</span></p></body></html>")
#endif // QT_CONFIG(tooltip)
        self.lineEdit_postalCode.setInputMask(u"")
        self.lineEdit_postalCode.setText(u"")
        self.lineEdit_postalCode.setPlaceholderText(u"(Opcional) Ej.: 6703")
        self.lineEdit_postalCode.setClearButtonEnabled(True)

        self.debtor_data_GridLayout.addWidget(self.lineEdit_postalCode, 7, 2, 1, 3)

        self.label_debtorSurname_feedback = QLabel(self.debtor_data)
        self.label_debtorSurname_feedback.setObjectName(u"label_debtorSurname_feedback")
        self.label_debtorSurname_feedback.setMaximumSize(QSize(16777215, 20))
        self.label_debtorSurname_feedback.setText(u"")
        self.label_debtorSurname_feedback.setTextFormat(Qt.PlainText)
        self.label_debtorSurname_feedback.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.label_debtorSurname_feedback.setTextInteractionFlags(Qt.NoTextInteraction)

        self.debtor_data_GridLayout.addWidget(self.label_debtorSurname_feedback, 2, 4, 1, 1, Qt.AlignRight|Qt.AlignTop)

        self.lineEdit_debtorName = QLineEdit(self.debtor_data)
        self.lineEdit_debtorName.setObjectName(u"lineEdit_debtorName")
#if QT_CONFIG(tooltip)
        self.lineEdit_debtorName.setToolTip(u"<html><head/><body><p><span style=\" font-size:11pt;\">Nombre del deudor.</span></p></body></html>")
#endif // QT_CONFIG(tooltip)
        self.lineEdit_debtorName.setText(u"")
        self.lineEdit_debtorName.setFrame(False)
        self.lineEdit_debtorName.setPlaceholderText(u"Nombre del deudor")
        self.lineEdit_debtorName.setClearButtonEnabled(True)

        self.debtor_data_GridLayout.addWidget(self.lineEdit_debtorName, 1, 1, 1, 2)

        self.label_phoneNumber_feedback = QLabel(self.debtor_data)
        self.label_phoneNumber_feedback.setObjectName(u"label_phoneNumber_feedback")
        self.label_phoneNumber_feedback.setMaximumSize(QSize(16777215, 20))
        self.label_phoneNumber_feedback.setText(u"")
        self.label_phoneNumber_feedback.setTextFormat(Qt.PlainText)
        self.label_phoneNumber_feedback.setAlignment(Qt.AlignCenter)
        self.label_phoneNumber_feedback.setTextInteractionFlags(Qt.NoTextInteraction)

        self.debtor_data_GridLayout.addWidget(self.label_phoneNumber_feedback, 4, 0, 1, 5, Qt.AlignHCenter|Qt.AlignTop)

        self.label_surnameMark = QLabel(self.debtor_data)
        self.label_surnameMark.setObjectName(u"label_surnameMark")
#if QT_CONFIG(tooltip)
        self.label_surnameMark.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.label_surnameMark.setText(u"<html><head/><body><p><span style=\" color:#ff0000;\">*</span></p></body></html>")

        self.debtor_data_GridLayout.addWidget(self.label_surnameMark, 1, 3, 1, 1)

        self.label_postalCode = QLabel(self.debtor_data)
        self.label_postalCode.setObjectName(u"label_postalCode")

        self.debtor_data_GridLayout.addWidget(self.label_postalCode, 7, 0, 1, 2)

        self.label_debtorInfo = QLabel(self.debtor_data)
        self.label_debtorInfo.setObjectName(u"label_debtorInfo")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_debtorInfo.sizePolicy().hasHeightForWidth())
        self.label_debtorInfo.setSizePolicy(sizePolicy1)
        self.label_debtorInfo.setStyleSheet(u"color: rgb(8, 68, 68);\n"
"margin-top: 15px;\n"
"margin-left: 30px;\n"
"margin-right: 30px;\n"
"border-bottom: 1px solid;\n"
"border-color: rgb(11, 126, 127);")
        self.label_debtorInfo.setText(u"INFORMACI\u00d3N SOBRE EL DEUDOR")
        self.label_debtorInfo.setTextFormat(Qt.PlainText)
        self.label_debtorInfo.setAlignment(Qt.AlignCenter)
        self.label_debtorInfo.setTextInteractionFlags(Qt.NoTextInteraction)

        self.debtor_data_GridLayout.addWidget(self.label_debtorInfo, 0, 0, 1, 5)

        self.label_nameMark = QLabel(self.debtor_data)
        self.label_nameMark.setObjectName(u"label_nameMark")
#if QT_CONFIG(tooltip)
        self.label_nameMark.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.label_nameMark.setText(u"<html><head/><body><p><span style=\" color:#ff0000;\">*</span></p></body></html>")

        self.debtor_data_GridLayout.addWidget(self.label_nameMark, 1, 0, 1, 1)

        self.lineEdit_debtorSurname = QLineEdit(self.debtor_data)
        self.lineEdit_debtorSurname.setObjectName(u"lineEdit_debtorSurname")
#if QT_CONFIG(tooltip)
        self.lineEdit_debtorSurname.setToolTip(u"<html><head/><body><p><span style=\" font-size:11pt;\">Apellido del deudor.</span></p></body></html>")
#endif // QT_CONFIG(tooltip)
        self.lineEdit_debtorSurname.setText(u"")
        self.lineEdit_debtorSurname.setFrame(False)
        self.lineEdit_debtorSurname.setPlaceholderText(u"Apellido del deudor")
        self.lineEdit_debtorSurname.setClearButtonEnabled(True)

        self.debtor_data_GridLayout.addWidget(self.lineEdit_debtorSurname, 1, 4, 1, 1)

        self.label_direction = QLabel(self.debtor_data)
        self.label_direction.setObjectName(u"label_direction")

        self.debtor_data_GridLayout.addWidget(self.label_direction, 6, 0, 1, 2)

        self.label_debtorName_feedback = QLabel(self.debtor_data)
        self.label_debtorName_feedback.setObjectName(u"label_debtorName_feedback")
        self.label_debtorName_feedback.setMaximumSize(QSize(16777215, 20))
        self.label_debtorName_feedback.setText(u"")
        self.label_debtorName_feedback.setTextFormat(Qt.PlainText)
        self.label_debtorName_feedback.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.label_debtorName_feedback.setTextInteractionFlags(Qt.NoTextInteraction)

        self.debtor_data_GridLayout.addWidget(self.label_debtorName_feedback, 2, 1, 1, 2, Qt.AlignLeft|Qt.AlignTop)

        self.lineEdit_phoneNumber = QLineEdit(self.debtor_data)
        self.lineEdit_phoneNumber.setObjectName(u"lineEdit_phoneNumber")
#if QT_CONFIG(tooltip)
        self.lineEdit_phoneNumber.setToolTip(u"<html><head/><body><p><span style=\" font-size:11pt;\">(Opcional) n\u00famero de tel\u00e9fono del deudor.</span></p><p><span style=\" font-size:11pt; font-weight:600; text-decoration: underline;\">NOTA:</span><span style=\" font-size:11pt;\"> si el deudor ya existe en la base de datos es recomendable </span><span style=\" font-size:11pt; text-decoration: underline;\">no llenar este campo</span><span style=\" font-size:11pt;\">, porque crear\u00e1 un registro diferente del mismo deudor.</span></p><p><span style=\" font-size:11pt; font-weight:600; text-decoration: underline;\">NOTA:</span><span style=\" font-size:11pt;\"> no lleva ni 0 ni 15, pero s\u00ed requiere el c\u00f3digo de pa\u00eds (el de Argentina es +54).</span></p></body></html>")
#endif // QT_CONFIG(tooltip)
        self.lineEdit_phoneNumber.setInputMask(u"")
        self.lineEdit_phoneNumber.setText(u"")
        self.lineEdit_phoneNumber.setFrame(False)
        self.lineEdit_phoneNumber.setCursorPosition(0)
        self.lineEdit_phoneNumber.setPlaceholderText(u"(Opcional) Ej.: 2323-123456")
        self.lineEdit_phoneNumber.setClearButtonEnabled(True)

        self.debtor_data_GridLayout.addWidget(self.lineEdit_phoneNumber, 3, 2, 1, 3)

        self.label_postalCode_feedback = QLabel(self.debtor_data)
        self.label_postalCode_feedback.setObjectName(u"label_postalCode_feedback")
        self.label_postalCode_feedback.setMaximumSize(QSize(16777215, 20))
        self.label_postalCode_feedback.setText(u"")
        self.label_postalCode_feedback.setTextFormat(Qt.PlainText)
        self.label_postalCode_feedback.setAlignment(Qt.AlignCenter)
        self.label_postalCode_feedback.setTextInteractionFlags(Qt.NoTextInteraction)

        self.debtor_data_GridLayout.addWidget(self.label_postalCode_feedback, 8, 0, 1, 5, Qt.AlignHCenter|Qt.AlignTop)

        self.debtor_data_GridLayout.setColumnStretch(1, 1)
        self.debtor_data_GridLayout.setColumnStretch(2, 1)
        self.debtor_data_GridLayout.setColumnStretch(4, 2)

        self.verticalLayout.addWidget(self.debtor_data)

        self.buttonBox = QDialogButtonBox(saleDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)

        self.verticalLayout.addWidget(self.buttonBox)

        QWidget.setTabOrder(self.lineEdit_saleDetail, self.comboBox_productName)
        QWidget.setTabOrder(self.comboBox_productName, self.lineEdit_productQuantity)
        QWidget.setTabOrder(self.lineEdit_productQuantity, self.checkBox_comercialPrice)
        QWidget.setTabOrder(self.checkBox_comercialPrice, self.lineEdit_totalPaid)
        QWidget.setTabOrder(self.lineEdit_totalPaid, self.dateTimeEdit)
        QWidget.setTabOrder(self.dateTimeEdit, self.lineEdit_debtorName)
        QWidget.setTabOrder(self.lineEdit_debtorName, self.lineEdit_debtorSurname)
        QWidget.setTabOrder(self.lineEdit_debtorSurname, self.lineEdit_phoneNumber)
        QWidget.setTabOrder(self.lineEdit_phoneNumber, self.lineEdit_direction)
        QWidget.setTabOrder(self.lineEdit_direction, self.lineEdit_postalCode)

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
        self.label_productName.setText(QCoreApplication.translate("saleDialog", u"<html><head/><body><p>Nombre del producto  <span style=\" color:#ff0000;\">*</span></p></body></html>", None))
        self.label_totalPaid.setText(QCoreApplication.translate("saleDialog", u"<html><head/><body><p>Total abonado  <span style=\" color:#ff0000;\">*</span></p></body></html>", None))
        self.lineEdit_totalPaid.setStyleSheet(QCoreApplication.translate("saleDialog", u"* {\n"
"	background-color: #35bc88;\n"
"	color: #111;\n"
"	border-color: #0b7e7f;\n"
"	font-family: \"Verdana\", \"Sans-Serif\";\n"
"	font-size: 16px;\n"
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
"	color: #dc2627;\n"
"	border: 1px solid #dc2627;\n"
"	background-color: #e0a4a4;\n"
"}\n"
"\n"
"\n"
"*[mandatoryField=\"True\"] {\n"
"	background-color: rgb(255, 251, 142);\n"
"}\n"
"\n"
"\n"
"QLineEdit {\n"
"	background-color: #fff;\n"
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
"}\n"
"\n"
"\n"
"QPushButton {\n"
"	font-size: 16px;\n"
"	background-color: #22577a;\n"
"	color: #fff;\n"
"	borde"
                        "r: 1px solid #12476a;\n"
"	border-radius: 2px;\n"
"	min-width: 200px;\n"
"	min-height: 23px;\n"
"}\n"
"QPushButton:hover,\n"
"QPushButton:pressed {\n"
"	background-color: #38a3a5;\n"
"	color: #111;\n"
"	border: 1px inset #289395;\n"
"}\n"
"QPushButton:disabled {\n"
"	background-color: rgb(103, 115, 122);\n"
"	color: #999;\n"
"}\n"
"\n"
"\n"
"/*cambia el estilo del combobox*/\n"
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
"QComboBox QAbstractItemView {\n"
"	background-color: #fff;\n"
"	selection-background-color: #38a3a5;\n"
"}", None))
        self.label_phoneNumber.setText(QCoreApplication.translate("saleDialog", u"N\u00fam. de tel\u00e9fono", None))
        self.label_postalCode.setText(QCoreApplication.translate("saleDialog", u"C\u00f3digo postal", None))
        self.label_direction.setText(QCoreApplication.translate("saleDialog", u"Direcci\u00f3n", None))
    # retranslateUi

