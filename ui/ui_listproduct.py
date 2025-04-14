# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'listproduct.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFrame,
    QGridLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QWidget)

class Ui_listProduct(object):
    def setupUi(self, listProduct):
        if not listProduct.objectName():
            listProduct.setObjectName(u"listProduct")
        listProduct.resize(595, 110)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(listProduct.sizePolicy().hasHeightForWidth())
        listProduct.setSizePolicy(sizePolicy)
        listProduct.setMinimumSize(QSize(595, 110))
        listProduct.setStyleSheet(u"* {\n"
"	color: #111;\n"
"	border-color: #0b7e7f;\n"
"	font-family: \"Verdana\", \"Sans-Serif\";\n"
"	font-size: 16px;\n"
"}\n"
"\n"
"\n"
"QMenu {\n"
"	background-color: #fff;\n"
"	color: #111;\n"
"	font-size: 14px;\n"
"}\n"
"\n"
"\n"
"#listProduct {\n"
"	background-color: #fff;\n"
"}\n"
"\n"
"\n"
"QToolTip {\n"
"	background-color: #fff;\n"
"	color: #0d1b2a;\n"
"}\n"
"\n"
"\n"
"/* labels */\n"
"QLabel {\n"
"	padding-right: 2px;\n"
"	padding-left: 2px;\n"
"}\n"
"\n"
"#label_nameFeedback, \n"
"#label_quantityFeedback {\n"
"	background-color: #F65755;\n"
"	color: #fff;\n"
"	border-radius: 5px;\n"
"}\n"
"\n"
"#label_subtotal {\n"
"	font-size: 19px;\n"
"	font-weight: 900;\n"
"	background-color: #0d1b2a;\n"
"	color: #e0e1dd;\n"
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
"QLineEdit"
                        ":disabled {\n"
"	background-color: #e0e1dd;\n"
"	color: #0d1b2a;\n"
"}\n"
"\n"
"\n"
"/* pushbuttons */\n"
"QPushButton {\n"
"	background-color: #fff;\n"
"	border-radius: 4px;\n"
"}\n"
"QPushButton:hover,\n"
"QPushButton:focus {\n"
"	background-color: #F68785;\n"
"}\n"
"QPushButton:pressed {\n"
"	background-color: #F68785;\n"
"	border: 1px inset #A65755;\n"
"}\n"
"\n"
"/* comboboxes */\n"
"QComboBox {\n"
"	background-color: #e0e1dd;\n"
"	color: #0d1b2a;\n"
"	border: 1px solid #3b66ab;\n"
"	border-radius: 10px;\n"
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
"QComboBox::down-"
                        "arrow {\n"
"	image: url(':/icons/chevron-down.svg');\n"
"}\n"
"QComboBox QAbstractItemView{\n"
"	background-color: #778da9;\n"
"	color: #fff;\n"
"	selection-background-color: #3b66ab;\n"
"}\n"
"QComboBox:disabled {\n"
"	background-color: rgb(103, 115, 122);\n"
"	color: #999;\n"
"}")
        self.gridLayout = QGridLayout(listProduct)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(9, 4, 4, 4)
        self.comboBox_productName = QComboBox(listProduct)
        self.comboBox_productName.setObjectName(u"comboBox_productName")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.comboBox_productName.sizePolicy().hasHeightForWidth())
        self.comboBox_productName.setSizePolicy(sizePolicy1)
        self.comboBox_productName.setMinimumSize(QSize(70, 25))
        self.comboBox_productName.setMaximumSize(QSize(16777215, 25))
#if QT_CONFIG(tooltip)
        self.comboBox_productName.setToolTip(u"<html><head/><body><p><span style=\" font-size:11pt;\">El nombre del producto vendido.</span></p></body></html>")
#endif // QT_CONFIG(tooltip)
        self.comboBox_productName.setEditable(True)
        self.comboBox_productName.setCurrentText(u"")
        self.comboBox_productName.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)
        self.comboBox_productName.setFrame(False)

        self.gridLayout.addWidget(self.comboBox_productName, 0, 0, 1, 1)

        self.frame_productQuantity = QFrame(listProduct)
        self.frame_productQuantity.setObjectName(u"frame_productQuantity")
        sizePolicy.setHeightForWidth(self.frame_productQuantity.sizePolicy().hasHeightForWidth())
        self.frame_productQuantity.setSizePolicy(sizePolicy)
        self.frame_productQuantity.setMinimumSize(QSize(0, 0))
        self.frame_productQuantity.setMaximumSize(QSize(16777215, 16777215))
        self.frame_productQuantity.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_productQuantity.setFrameShadow(QFrame.Shadow.Raised)
        self.frame_productQuantity_Hlayout = QHBoxLayout(self.frame_productQuantity)
        self.frame_productQuantity_Hlayout.setSpacing(4)
        self.frame_productQuantity_Hlayout.setObjectName(u"frame_productQuantity_Hlayout")
        self.frame_productQuantity_Hlayout.setContentsMargins(0, 0, 0, 0)
        self.lineEdit_productQuantity = QLineEdit(self.frame_productQuantity)
        self.lineEdit_productQuantity.setObjectName(u"lineEdit_productQuantity")
        sizePolicy1.setHeightForWidth(self.lineEdit_productQuantity.sizePolicy().hasHeightForWidth())
        self.lineEdit_productQuantity.setSizePolicy(sizePolicy1)
        self.lineEdit_productQuantity.setMinimumSize(QSize(75, 25))
        self.lineEdit_productQuantity.setMaximumSize(QSize(16777215, 16777215))
#if QT_CONFIG(tooltip)
        self.lineEdit_productQuantity.setToolTip(u"<html><head/><body><p><span style=\" font-size:11pt;\">La cantidad vendida del producto.</span></p></body></html>")
#endif // QT_CONFIG(tooltip)
        self.lineEdit_productQuantity.setFrame(False)
        self.lineEdit_productQuantity.setPlaceholderText(u"Cantidad")

        self.frame_productQuantity_Hlayout.addWidget(self.lineEdit_productQuantity)

        self.label_productMeasurementUnit = QLabel(self.frame_productQuantity)
        self.label_productMeasurementUnit.setObjectName(u"label_productMeasurementUnit")
        sizePolicy1.setHeightForWidth(self.label_productMeasurementUnit.sizePolicy().hasHeightForWidth())
        self.label_productMeasurementUnit.setSizePolicy(sizePolicy1)
        self.label_productMeasurementUnit.setMinimumSize(QSize(0, 0))
        self.label_productMeasurementUnit.setMaximumSize(QSize(16777215, 16777215))
        self.label_productMeasurementUnit.setText(u"")
        self.label_productMeasurementUnit.setTextFormat(Qt.TextFormat.PlainText)
        self.label_productMeasurementUnit.setWordWrap(True)
        self.label_productMeasurementUnit.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        self.frame_productQuantity_Hlayout.addWidget(self.label_productMeasurementUnit)

        self.frame_productQuantity_Hlayout.setStretch(0, 3)
        self.frame_productQuantity_Hlayout.setStretch(1, 5)

        self.gridLayout.addWidget(self.frame_productQuantity, 0, 1, 1, 1)

        self.checkBox_comercialPrice = QCheckBox(listProduct)
        self.checkBox_comercialPrice.setObjectName(u"checkBox_comercialPrice")
        sizePolicy1.setHeightForWidth(self.checkBox_comercialPrice.sizePolicy().hasHeightForWidth())
        self.checkBox_comercialPrice.setSizePolicy(sizePolicy1)
        self.checkBox_comercialPrice.setMinimumSize(QSize(160, 25))
        self.checkBox_comercialPrice.setMaximumSize(QSize(16777215, 25))
#if QT_CONFIG(tooltip)
        self.checkBox_comercialPrice.setToolTip(u"<html><head/><body><p><span style=\" font-size:11pt;\">Aplica el costo comercial al producto.</span></p></body></html>")
#endif // QT_CONFIG(tooltip)
        self.checkBox_comercialPrice.setText(u"precio comercial")
#if QT_CONFIG(shortcut)
        self.checkBox_comercialPrice.setShortcut(u"")
#endif // QT_CONFIG(shortcut)

        self.gridLayout.addWidget(self.checkBox_comercialPrice, 0, 2, 1, 1)

        self.label_subtotal = QLabel(listProduct)
        self.label_subtotal.setObjectName(u"label_subtotal")
        sizePolicy1.setHeightForWidth(self.label_subtotal.sizePolicy().hasHeightForWidth())
        self.label_subtotal.setSizePolicy(sizePolicy1)
        self.label_subtotal.setMinimumSize(QSize(120, 30))
        self.label_subtotal.setMaximumSize(QSize(16777215, 30))
        self.label_subtotal.setText(u"SUBTOTAL")
        self.label_subtotal.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_subtotal.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

        self.gridLayout.addWidget(self.label_subtotal, 0, 3, 1, 1)

        self.btn_deleteCurrentProduct = QPushButton(listProduct)
        self.btn_deleteCurrentProduct.setObjectName(u"btn_deleteCurrentProduct")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.btn_deleteCurrentProduct.sizePolicy().hasHeightForWidth())
        self.btn_deleteCurrentProduct.setSizePolicy(sizePolicy2)
        self.btn_deleteCurrentProduct.setMinimumSize(QSize(32, 32))
        self.btn_deleteCurrentProduct.setMaximumSize(QSize(32, 32))
#if QT_CONFIG(tooltip)
        self.btn_deleteCurrentProduct.setToolTip(u"<html><head/><body><p><span style=\" font-size:11pt;\">Borra el producto de la venta actual (</span><span style=\" font-size:11pt; font-style:italic;\">Supr.</span><span style=\" font-size:11pt;\">)</span></p></body></html>")
#endif // QT_CONFIG(tooltip)
        self.btn_deleteCurrentProduct.setText(u"")
        self.btn_deleteCurrentProduct.setIconSize(QSize(32, 32))
#if QT_CONFIG(shortcut)
        self.btn_deleteCurrentProduct.setShortcut(u"Del")
#endif // QT_CONFIG(shortcut)

        self.gridLayout.addWidget(self.btn_deleteCurrentProduct, 0, 4, 1, 1)

        self.label_nameFeedback = QLabel(listProduct)
        self.label_nameFeedback.setObjectName(u"label_nameFeedback")
        sizePolicy.setHeightForWidth(self.label_nameFeedback.sizePolicy().hasHeightForWidth())
        self.label_nameFeedback.setSizePolicy(sizePolicy)
        self.label_nameFeedback.setMinimumSize(QSize(110, 20))
        self.label_nameFeedback.setMaximumSize(QSize(16777215, 16777215))
        self.label_nameFeedback.setText(u"")
        self.label_nameFeedback.setTextFormat(Qt.TextFormat.PlainText)
        self.label_nameFeedback.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_nameFeedback.setWordWrap(True)
        self.label_nameFeedback.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        self.gridLayout.addWidget(self.label_nameFeedback, 1, 0, 1, 1)

        self.label_quantityFeedback = QLabel(listProduct)
        self.label_quantityFeedback.setObjectName(u"label_quantityFeedback")
        sizePolicy.setHeightForWidth(self.label_quantityFeedback.sizePolicy().hasHeightForWidth())
        self.label_quantityFeedback.setSizePolicy(sizePolicy)
        self.label_quantityFeedback.setMinimumSize(QSize(110, 20))
        self.label_quantityFeedback.setMaximumSize(QSize(16777215, 16777215))
        self.label_quantityFeedback.setText(u"")
        self.label_quantityFeedback.setTextFormat(Qt.TextFormat.PlainText)
        self.label_quantityFeedback.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_quantityFeedback.setWordWrap(True)
        self.label_quantityFeedback.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        self.gridLayout.addWidget(self.label_quantityFeedback, 1, 1, 1, 1)

        self.lineEdit_saleDetail = QLineEdit(listProduct)
        self.lineEdit_saleDetail.setObjectName(u"lineEdit_saleDetail")
        sizePolicy1.setHeightForWidth(self.lineEdit_saleDetail.sizePolicy().hasHeightForWidth())
        self.lineEdit_saleDetail.setSizePolicy(sizePolicy1)
        self.lineEdit_saleDetail.setMinimumSize(QSize(300, 25))
#if QT_CONFIG(tooltip)
        self.lineEdit_saleDetail.setToolTip(u"<html><head/><body><p><span style=\" font-size:11pt;\">Descripci\u00f3n adicional de la venta (opcional).</span></p><p><span style=\" font-size:11pt;\">Si este campo se deja vac\u00edo se llenar\u00e1 con el producto vendido, la cantidad vendida, la unidad de medida usada para el producto y el tipo de precio que se pag\u00f3 (comercial o normal).</span></p></body></html>")
#endif // QT_CONFIG(tooltip)
        self.lineEdit_saleDetail.setInputMask(u"")
        self.lineEdit_saleDetail.setText(u"")
        self.lineEdit_saleDetail.setFrame(False)
        self.lineEdit_saleDetail.setPlaceholderText(u"(Opcional) detalles de la venta")

        self.gridLayout.addWidget(self.lineEdit_saleDetail, 2, 0, 1, 4)

        self.gridLayout.setColumnStretch(0, 2)
        self.gridLayout.setColumnStretch(1, 2)
        self.gridLayout.setColumnStretch(2, 2)
        self.gridLayout.setColumnStretch(3, 2)
        QWidget.setTabOrder(self.comboBox_productName, self.lineEdit_productQuantity)
        QWidget.setTabOrder(self.lineEdit_productQuantity, self.checkBox_comercialPrice)
        QWidget.setTabOrder(self.checkBox_comercialPrice, self.lineEdit_saleDetail)
        QWidget.setTabOrder(self.lineEdit_saleDetail, self.btn_deleteCurrentProduct)

        self.retranslateUi(listProduct)

        QMetaObject.connectSlotsByName(listProduct)
    # setupUi

    def retranslateUi(self, listProduct):
        self.comboBox_productName.setPlaceholderText(QCoreApplication.translate("listProduct", u"Nombre del producto", None))
#if QT_CONFIG(tooltip)
        self.frame_productQuantity.setToolTip(QCoreApplication.translate("listProduct", u"<html><head/><body><p><span style=\" font-size:11pt;\">La cantidad vendida del producto.</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        pass
    # retranslateUi

