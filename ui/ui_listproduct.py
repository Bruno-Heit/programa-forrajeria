# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'listproduct.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFrame,
    QGridLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QWidget)

class Ui_listProduct(object):
    def setupUi(self, listProduct):
        if not listProduct.objectName():
            listProduct.setObjectName(u"listProduct")
        listProduct.resize(768, 110)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(listProduct.sizePolicy().hasHeightForWidth())
        listProduct.setSizePolicy(sizePolicy)
        listProduct.setMinimumSize(QSize(580, 110))
        listProduct.setStyleSheet(u"* {\n"
"	color: #111;\n"
"	border-color: #0b7e7f;\n"
"	font-family: \"Tahoma\", \"Verdana\", \"Sans-Serif\";\n"
"	font-size: 17px;\n"
"}\n"
"\n"
"\n"
"QFrame, QWidget {\n"
"	border: none;\n"
"}\n"
"\n"
"\n"
"#label_nameFeedback, \n"
"#label_quantityFeedback {\n"
"	font-size: 15px;\n"
"	color: #dc2627;\n"
"	border: 1px solid #dc2627;\n"
"	background-color: rgba(224,164,164,0.7);\n"
"}\n"
"\n"
"\n"
"QLineEdit {\n"
"	border: none;\n"
"	border-top: 1px solid;\n"
"	border-bottom: 1px solid;\n"
"	border-color: #0b7e7f;\n"
"}\n"
"QLineEdit:focus,\n"
"QComboBox:focus,\n"
"QCheckBox:focus {\n"
"	background-color: rgba(197, 255, 252, 150);\n"
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
"QPushButton {\n"
"	background-color: #ff4949;\n"
"	margin-left: 5px;\n"
"	border: 1px solid #12476a;\n"
"	border-radius: 2px;\n"
"}\n"
"QPushButton:hover,\n"
"QPushButton:pressed {\n"
"	background-color: #faa;\n"
"	"
                        "color: #111;\n"
"	border: 1px inset;\n"
"	border-color: rgb(231, 66, 66);\n"
"}\n"
"\n"
"\n"
"QComboBox {\n"
"	background-color: rgb(255,255,255);\n"
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
"	background-color: rgba(170, 255, 127, 100);\n"
"	selection-background-color: #38a3a5;\n"
"}")
        self.gridLayout = QGridLayout(listProduct)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(9, 4, 4, 4)
        self.comboBox_productName = QComboBox(listProduct)
        self.comboBox_productName.setObjectName(u"comboBox_productName")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.comboBox_productName.sizePolicy().hasHeightForWidth())
        self.comboBox_productName.setSizePolicy(sizePolicy1)
        self.comboBox_productName.setMinimumSize(QSize(70, 25))
        self.comboBox_productName.setMaximumSize(QSize(350, 25))
#if QT_CONFIG(tooltip)
        self.comboBox_productName.setToolTip(u"<html><head/><body><p><span style=\" font-size:12pt;\">El nombre del producto vendido.</span></p></body></html>")
#endif // QT_CONFIG(tooltip)
        self.comboBox_productName.setEditable(True)
        self.comboBox_productName.setCurrentText(u"")
        self.comboBox_productName.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        self.comboBox_productName.setFrame(False)

        self.gridLayout.addWidget(self.comboBox_productName, 0, 0, 1, 1)

        self.frame_productQuantity = QFrame(listProduct)
        self.frame_productQuantity.setObjectName(u"frame_productQuantity")
        sizePolicy.setHeightForWidth(self.frame_productQuantity.sizePolicy().hasHeightForWidth())
        self.frame_productQuantity.setSizePolicy(sizePolicy)
        self.frame_productQuantity.setMinimumSize(QSize(0, 0))
        self.frame_productQuantity.setMaximumSize(QSize(450, 16777215))
        self.frame_productQuantity.setFrameShape(QFrame.NoFrame)
        self.frame_productQuantity.setFrameShadow(QFrame.Raised)
        self.frame_productQuantity_Hlayout = QHBoxLayout(self.frame_productQuantity)
        self.frame_productQuantity_Hlayout.setSpacing(4)
        self.frame_productQuantity_Hlayout.setObjectName(u"frame_productQuantity_Hlayout")
        self.frame_productQuantity_Hlayout.setContentsMargins(0, 0, 0, 0)
        self.lineEdit_productQuantity = QLineEdit(self.frame_productQuantity)
        self.lineEdit_productQuantity.setObjectName(u"lineEdit_productQuantity")
        sizePolicy1.setHeightForWidth(self.lineEdit_productQuantity.sizePolicy().hasHeightForWidth())
        self.lineEdit_productQuantity.setSizePolicy(sizePolicy1)
        self.lineEdit_productQuantity.setMinimumSize(QSize(75, 25))
        self.lineEdit_productQuantity.setMaximumSize(QSize(120, 16777215))
#if QT_CONFIG(tooltip)
        self.lineEdit_productQuantity.setToolTip(u"<html><head/><body><p><span style=\" font-size:12pt;\">La cantidad vendida del producto.</span></p></body></html>")
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
        self.label_productMeasurementUnit.setTextFormat(Qt.PlainText)
        self.label_productMeasurementUnit.setWordWrap(False)
        self.label_productMeasurementUnit.setTextInteractionFlags(Qt.NoTextInteraction)

        self.frame_productQuantity_Hlayout.addWidget(self.label_productMeasurementUnit)

        self.frame_productQuantity_Hlayout.setStretch(0, 3)
        self.frame_productQuantity_Hlayout.setStretch(1, 5)

        self.gridLayout.addWidget(self.frame_productQuantity, 0, 1, 1, 1)

        self.checkBox_comercialPrice = QCheckBox(listProduct)
        self.checkBox_comercialPrice.setObjectName(u"checkBox_comercialPrice")
        sizePolicy1.setHeightForWidth(self.checkBox_comercialPrice.sizePolicy().hasHeightForWidth())
        self.checkBox_comercialPrice.setSizePolicy(sizePolicy1)
        self.checkBox_comercialPrice.setMinimumSize(QSize(80, 25))
        self.checkBox_comercialPrice.setMaximumSize(QSize(140, 25))
#if QT_CONFIG(tooltip)
        self.checkBox_comercialPrice.setToolTip(u"<html><head/><body><p><span style=\" font-size:12pt;\">Aplica el costo comercial al producto.</span></p></body></html>")
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
        self.label_subtotal.setMaximumSize(QSize(350, 30))
        self.label_subtotal.setStyleSheet(u"background-color: #b6b6b6;\n"
"color: #555;\n"
"border-top: 1px solid #111;\n"
"border-right: 1px solid #111;")
        self.label_subtotal.setText(u"SUBTOTAL")
        self.label_subtotal.setAlignment(Qt.AlignCenter)
        self.label_subtotal.setTextInteractionFlags(Qt.TextSelectableByMouse)

        self.gridLayout.addWidget(self.label_subtotal, 0, 3, 1, 1)

        self.btn_deleteCurrentProduct = QPushButton(listProduct)
        self.btn_deleteCurrentProduct.setObjectName(u"btn_deleteCurrentProduct")
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.btn_deleteCurrentProduct.sizePolicy().hasHeightForWidth())
        self.btn_deleteCurrentProduct.setSizePolicy(sizePolicy2)
        self.btn_deleteCurrentProduct.setMinimumSize(QSize(30, 30))
        self.btn_deleteCurrentProduct.setMaximumSize(QSize(30, 30))
#if QT_CONFIG(tooltip)
        self.btn_deleteCurrentProduct.setToolTip(u"<html><head/><body><p><span style=\" font-size:12pt;\">Borra el producto de la venta actual (</span><span style=\" font-size:12pt; font-style:italic;\">Supr.</span><span style=\" font-size:12pt;\">)</span></p></body></html>")
#endif // QT_CONFIG(tooltip)
        self.btn_deleteCurrentProduct.setText(u"")
        self.btn_deleteCurrentProduct.setIconSize(QSize(28, 28))
#if QT_CONFIG(shortcut)
        self.btn_deleteCurrentProduct.setShortcut(u"Del")
#endif // QT_CONFIG(shortcut)

        self.gridLayout.addWidget(self.btn_deleteCurrentProduct, 0, 4, 1, 1)

        self.label_nameFeedback = QLabel(listProduct)
        self.label_nameFeedback.setObjectName(u"label_nameFeedback")
        sizePolicy.setHeightForWidth(self.label_nameFeedback.sizePolicy().hasHeightForWidth())
        self.label_nameFeedback.setSizePolicy(sizePolicy)
        self.label_nameFeedback.setMinimumSize(QSize(100, 20))
        self.label_nameFeedback.setMaximumSize(QSize(350, 16777215))
        self.label_nameFeedback.setText(u"")
        self.label_nameFeedback.setTextFormat(Qt.PlainText)
        self.label_nameFeedback.setAlignment(Qt.AlignCenter)
        self.label_nameFeedback.setWordWrap(True)
        self.label_nameFeedback.setTextInteractionFlags(Qt.NoTextInteraction)

        self.gridLayout.addWidget(self.label_nameFeedback, 1, 0, 1, 1)

        self.label_quantityFeedback = QLabel(listProduct)
        self.label_quantityFeedback.setObjectName(u"label_quantityFeedback")
        sizePolicy.setHeightForWidth(self.label_quantityFeedback.sizePolicy().hasHeightForWidth())
        self.label_quantityFeedback.setSizePolicy(sizePolicy)
        self.label_quantityFeedback.setMinimumSize(QSize(100, 20))
        self.label_quantityFeedback.setMaximumSize(QSize(450, 16777215))
        self.label_quantityFeedback.setText(u"")
        self.label_quantityFeedback.setTextFormat(Qt.PlainText)
        self.label_quantityFeedback.setAlignment(Qt.AlignCenter)
        self.label_quantityFeedback.setWordWrap(True)
        self.label_quantityFeedback.setTextInteractionFlags(Qt.NoTextInteraction)

        self.gridLayout.addWidget(self.label_quantityFeedback, 1, 1, 1, 1)

        self.lineEdit_saleDetail = QLineEdit(listProduct)
        self.lineEdit_saleDetail.setObjectName(u"lineEdit_saleDetail")
        sizePolicy1.setHeightForWidth(self.lineEdit_saleDetail.sizePolicy().hasHeightForWidth())
        self.lineEdit_saleDetail.setSizePolicy(sizePolicy1)
        self.lineEdit_saleDetail.setMinimumSize(QSize(300, 25))
#if QT_CONFIG(tooltip)
        self.lineEdit_saleDetail.setToolTip(u"<html><head/><body><p><span style=\" font-size:12pt;\">Descripci\u00f3n adicional de la venta (opcional).</span></p><p><span style=\" font-size:12pt;\">Si este campo se deja vac\u00edo se llenar\u00e1 con el producto vendido, la cantidad vendida, la unidad de medida usada para el producto y el tipo de precio que se pag\u00f3 (comercial o normal).</span></p></body></html>")
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
        self.frame_productQuantity.setToolTip(QCoreApplication.translate("listProduct", u"<html><head/><body><p><span style=\" font-size:12pt;\">La cantidad vendida del producto.</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        pass
    # retranslateUi

