# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'productDialog.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QComboBox, QDialog,
    QDialogButtonBox, QFrame, QGridLayout, QHBoxLayout,
    QLabel, QLineEdit, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(651, 359)
        Dialog.setMinimumSize(QSize(650, 0))
        Dialog.setStyleSheet(u"* {\n"
"	color: #111;\n"
"	border-color: #0b7e7f;\n"
"	font-family: \"Tahoma\", \"Verdana\", \"Sans-Serif\";\n"
"	font-size: 16px;\n"
"}\n"
"\n"
"\n"
"QDialog {\n"
"	background-color: qlineargradient(spread:pad, x1:0.149, y1:0.892, x2:0.774, y2:0.0860909, stop:0 rgba(30, 168, 59, 255), stop:1 rgba(153, 228, 184, 255));\n"
"}\n"
"\n"
"\n"
"#frame_productDescription,\n"
"#frame_measurementUnit {\n"
"	border: none;\n"
"	border-bottom: 1px solid;\n"
"	border-color: #0b7e7f;\n"
"}\n"
"\n"
"\n"
"#label_nameWarning,\n"
"#label_stockWarning,\n"
"#label_categoryWarning,\n"
"#label_unitPriceWarning,\n"
"#label_comercialPriceWarning {\n"
"	color: #dc2627;\n"
"	border: 1px solid #dc2627;\n"
"	background-color: rgba(224, 164, 164, 0.7);\n"
"}\n"
"\n"
"\n"
"#frame_productStock {\n"
"	margin-bottom: 5px;\n"
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
"	backg"
                        "round-color: rgb(197, 255, 252);\n"
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
"	padding-top: 2px;\n"
"	padding-left: 4px;\n"
"}\n"
"QComboBox QAbstractItemView {\n"
"	background-color: #fff;\n"
"	selecti"
                        "on-background-color: #38a3a5;\n"
"}\n"
"")
        Dialog.setSizeGripEnabled(True)
        self.dialog_Vlayout = QVBoxLayout(Dialog)
        self.dialog_Vlayout.setSpacing(4)
        self.dialog_Vlayout.setObjectName(u"dialog_Vlayout")
        self.dialog_Vlayout.setContentsMargins(5, 5, 5, 5)
        self.mainForm = QFrame(Dialog)
        self.mainForm.setObjectName(u"mainForm")
        self.mainForm.setStyleSheet(u"* {\n"
"	color: #111;\n"
"	border-color: #0b7e7f;\n"
"	font-family: \"Tahoma\", \"Verdana\", \"Sans-Serif\";\n"
"	font-size: 16px;\n"
"}\n"
"\n"
"\n"
"QDialog {\n"
"	background-color: qlineargradient(spread:pad, x1:0.149, y1:0.892, x2:0.774, y2:0.0860909, stop:0 rgba(30, 168, 59, 255), stop:1 rgba(153, 228, 184, 255));\n"
"}\n"
"\n"
"\n"
"#frame_productDescription,\n"
"#frame_measurementUnit {\n"
"	border: none;\n"
"	border-bottom: 1px solid;\n"
"	border-color: #0b7e7f;\n"
"}\n"
"\n"
"\n"
"#label_nameWarning,\n"
"#label_stockWarning,\n"
"#label_categoryWarning,\n"
"#label_unitPriceWarning,\n"
"#label_comercialPriceWarning {\n"
"	color: #dc2627;\n"
"	border: 1px solid #dc2627;\n"
"	background-color: #e0a4a4;\n"
"}\n"
"\n"
"\n"
"#frame_productStock {\n"
"	margin-bottom: 5px;\n"
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
"	background-color: rgb("
                        "197, 255, 252);\n"
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
"	padding-top: 2px;\n"
"	padding-left: 4px;\n"
"}\n"
"QComboBox QAbstractItemView {\n"
"	background-color: #fff;\n"
"	selection-background-col"
                        "or: #38a3a5;\n"
"}\n"
"")
        self.mainForm.setFrameShape(QFrame.NoFrame)
        self.mainForm.setFrameShadow(QFrame.Raised)
        self.mainForm_Vlayout = QVBoxLayout(self.mainForm)
        self.mainForm_Vlayout.setSpacing(4)
        self.mainForm_Vlayout.setObjectName(u"mainForm_Vlayout")
        self.mainForm_Vlayout.setContentsMargins(0, 0, 0, 0)
        self.frame_productName = QFrame(self.mainForm)
        self.frame_productName.setObjectName(u"frame_productName")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_productName.sizePolicy().hasHeightForWidth())
        self.frame_productName.setSizePolicy(sizePolicy)
        self.frame_productName.setMaximumSize(QSize(16777215, 16777215))
#if QT_CONFIG(tooltip)
        self.frame_productName.setToolTip(u"<html><head/><body><p>El nombre del producto.</p><p><span style=\" font-weight:600; text-decoration: underline;\">CONSEJO:</span> mantener el nombre simple, usando marcas de los productos y el tipo como nombre (ejemplo: Dog-Chow razas peque\u00f1as).</p></body></html>")
#endif // QT_CONFIG(tooltip)
        self.frame_productName.setFrameShape(QFrame.NoFrame)
        self.frame_productName.setFrameShadow(QFrame.Raised)
        self.frame_productName_GridLayout = QGridLayout(self.frame_productName)
        self.frame_productName_GridLayout.setSpacing(4)
        self.frame_productName_GridLayout.setObjectName(u"frame_productName_GridLayout")
        self.frame_productName_GridLayout.setContentsMargins(0, 0, 0, 0)
        self.lineedit_productName = QLineEdit(self.frame_productName)
        self.lineedit_productName.setObjectName(u"lineedit_productName")
        self.lineedit_productName.setText(u"")
        self.lineedit_productName.setMaxLength(50)
        self.lineedit_productName.setPlaceholderText(u"Escribir el nombre del producto")
        self.lineedit_productName.setClearButtonEnabled(True)

        self.frame_productName_GridLayout.addWidget(self.lineedit_productName, 0, 1, 1, 1)

        self.label_productName = QLabel(self.frame_productName)
        self.label_productName.setObjectName(u"label_productName")
#if QT_CONFIG(tooltip)
        self.label_productName.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.label_productName.setText(u"<html><head/><body><p>Nombre del producto  <span style=\" color:#ff0000;\">*</span></p></body></html>")
        self.label_productName.setTextFormat(Qt.RichText)
        self.label_productName.setTextInteractionFlags(Qt.NoTextInteraction)

        self.frame_productName_GridLayout.addWidget(self.label_productName, 0, 0, 1, 1)

        self.label_nameWarning = QLabel(self.frame_productName)
        self.label_nameWarning.setObjectName(u"label_nameWarning")
        self.label_nameWarning.setMinimumSize(QSize(0, 18))
#if QT_CONFIG(tooltip)
        self.label_nameWarning.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.label_nameWarning.setText(u"")
        self.label_nameWarning.setTextFormat(Qt.PlainText)
        self.label_nameWarning.setAlignment(Qt.AlignRight|Qt.AlignTop|Qt.AlignTrailing)
        self.label_nameWarning.setWordWrap(False)
        self.label_nameWarning.setTextInteractionFlags(Qt.NoTextInteraction)

        self.frame_productName_GridLayout.addWidget(self.label_nameWarning, 1, 0, 1, 2, Qt.AlignRight|Qt.AlignTop)

        self.frame_productName_GridLayout.setColumnStretch(0, 2)
        self.frame_productName_GridLayout.setColumnStretch(1, 3)

        self.mainForm_Vlayout.addWidget(self.frame_productName)

        self.frame_productCategory = QFrame(self.mainForm)
        self.frame_productCategory.setObjectName(u"frame_productCategory")
        sizePolicy.setHeightForWidth(self.frame_productCategory.sizePolicy().hasHeightForWidth())
        self.frame_productCategory.setSizePolicy(sizePolicy)
        self.frame_productCategory.setMinimumSize(QSize(0, 0))
        self.frame_productCategory.setMaximumSize(QSize(16777215, 16777215))
#if QT_CONFIG(tooltip)
        self.frame_productCategory.setToolTip(u"<html><head/><body><p>Elegir a qu\u00e9 categor\u00eda pertenece el producto.</p><p><span style=\" font-weight:600; text-decoration: underline;\">CONSEJO:</span> si se considera que un producto no pertenece a ninguna categor\u00eda de la lista, introducirla en &quot;Varios&quot;.</p></body></html>")
#endif // QT_CONFIG(tooltip)
        self.frame_productCategory.setFrameShape(QFrame.NoFrame)
        self.frame_productCategory.setFrameShadow(QFrame.Raised)
        self.frame_productCategory_GridLayout = QGridLayout(self.frame_productCategory)
        self.frame_productCategory_GridLayout.setSpacing(4)
        self.frame_productCategory_GridLayout.setObjectName(u"frame_productCategory_GridLayout")
        self.frame_productCategory_GridLayout.setContentsMargins(0, 0, 0, 0)
        self.label_productCategory = QLabel(self.frame_productCategory)
        self.label_productCategory.setObjectName(u"label_productCategory")
        self.label_productCategory.setText(u"<html><head/><body><p>Categor\u00eda a la que pertenece  <span style=\" color:#ff0000;\">*</span></p></body></html>")
        self.label_productCategory.setTextFormat(Qt.RichText)
        self.label_productCategory.setTextInteractionFlags(Qt.NoTextInteraction)

        self.frame_productCategory_GridLayout.addWidget(self.label_productCategory, 0, 0, 1, 1)

        self.cb_productCategory = QComboBox(self.frame_productCategory)
        self.cb_productCategory.setObjectName(u"cb_productCategory")
#if QT_CONFIG(tooltip)
        self.cb_productCategory.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.cb_productCategory.setEditable(True)
        self.cb_productCategory.setCurrentText(u"")
        self.cb_productCategory.setSizeAdjustPolicy(QComboBox.AdjustToContentsOnFirstShow)
        self.cb_productCategory.setPlaceholderText(u"Seleccionar categor\u00eda")
        self.cb_productCategory.setFrame(False)

        self.frame_productCategory_GridLayout.addWidget(self.cb_productCategory, 0, 1, 1, 1)

        self.label_categoryWarning = QLabel(self.frame_productCategory)
        self.label_categoryWarning.setObjectName(u"label_categoryWarning")
        self.label_categoryWarning.setMinimumSize(QSize(0, 18))
        self.label_categoryWarning.setMaximumSize(QSize(16777215, 16777215))
        self.label_categoryWarning.setText(u"")
        self.label_categoryWarning.setTextFormat(Qt.PlainText)
        self.label_categoryWarning.setAlignment(Qt.AlignRight|Qt.AlignTop|Qt.AlignTrailing)
        self.label_categoryWarning.setWordWrap(False)
        self.label_categoryWarning.setTextInteractionFlags(Qt.NoTextInteraction)

        self.frame_productCategory_GridLayout.addWidget(self.label_categoryWarning, 1, 0, 1, 2, Qt.AlignRight|Qt.AlignTop)

        self.frame_productCategory_GridLayout.setColumnStretch(0, 2)
        self.frame_productCategory_GridLayout.setColumnStretch(1, 3)

        self.mainForm_Vlayout.addWidget(self.frame_productCategory)

        self.frame_productDescription = QFrame(self.mainForm)
        self.frame_productDescription.setObjectName(u"frame_productDescription")
        sizePolicy.setHeightForWidth(self.frame_productDescription.sizePolicy().hasHeightForWidth())
        self.frame_productDescription.setSizePolicy(sizePolicy)
        self.frame_productDescription.setMinimumSize(QSize(0, 0))
        self.frame_productDescription.setMaximumSize(QSize(16777215, 16777215))
#if QT_CONFIG(tooltip)
        self.frame_productDescription.setToolTip(u"<html><head/><body><p>Es un campo opcional. Admite una descripci\u00f3n m\u00e1s extensa si se desea del producto.</p><p><span style=\" font-weight:600; text-decoration: underline;\">CONSEJO: </span>usar palabras clave en la descripci\u00f3n que permitan posteriormente la b\u00fasqueda del producto mediante esas palabras (algunos ejemplos de palabras clave: perro; adulto; cachorro; urinary; gato; granja; ca\u00f1a; veneno; insecto; hormiga; etc.)</p></body></html>")
#endif // QT_CONFIG(tooltip)
        self.frame_productDescription.setFrameShape(QFrame.NoFrame)
        self.frame_productDescription.setFrameShadow(QFrame.Raised)
        self.frame_productDescription_Hlayout = QHBoxLayout(self.frame_productDescription)
        self.frame_productDescription_Hlayout.setSpacing(4)
        self.frame_productDescription_Hlayout.setObjectName(u"frame_productDescription_Hlayout")
        self.frame_productDescription_Hlayout.setContentsMargins(0, 0, 0, 0)
        self.label_productDescription = QLabel(self.frame_productDescription)
        self.label_productDescription.setObjectName(u"label_productDescription")
        self.label_productDescription.setText(u"Descripci\u00f3n del producto")
        self.label_productDescription.setTextFormat(Qt.PlainText)
        self.label_productDescription.setTextInteractionFlags(Qt.NoTextInteraction)

        self.frame_productDescription_Hlayout.addWidget(self.label_productDescription)

        self.lineedit_productDescription = QLineEdit(self.frame_productDescription)
        self.lineedit_productDescription.setObjectName(u"lineedit_productDescription")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.lineedit_productDescription.sizePolicy().hasHeightForWidth())
        self.lineedit_productDescription.setSizePolicy(sizePolicy1)
        self.lineedit_productDescription.setText(u"")
        self.lineedit_productDescription.setMaxLength(255)
        self.lineedit_productDescription.setFrame(True)
        self.lineedit_productDescription.setPlaceholderText(u"(opcional) Ej.: alimento para gatos adultos")
        self.lineedit_productDescription.setClearButtonEnabled(True)

        self.frame_productDescription_Hlayout.addWidget(self.lineedit_productDescription)

        self.frame_productDescription_Hlayout.setStretch(0, 2)
        self.frame_productDescription_Hlayout.setStretch(1, 3)

        self.mainForm_Vlayout.addWidget(self.frame_productDescription)

        self.frame_productStock = QFrame(self.mainForm)
        self.frame_productStock.setObjectName(u"frame_productStock")
        sizePolicy.setHeightForWidth(self.frame_productStock.sizePolicy().hasHeightForWidth())
        self.frame_productStock.setSizePolicy(sizePolicy)
        self.frame_productStock.setMinimumSize(QSize(0, 0))
        self.frame_productStock.setMaximumSize(QSize(16777215, 16777215))
#if QT_CONFIG(tooltip)
        self.frame_productStock.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.frame_productStock.setFrameShape(QFrame.NoFrame)
        self.frame_productStock.setFrameShadow(QFrame.Raised)
        self.frame_productStock_GridLayout = QGridLayout(self.frame_productStock)
        self.frame_productStock_GridLayout.setSpacing(4)
        self.frame_productStock_GridLayout.setObjectName(u"frame_productStock_GridLayout")
        self.frame_productStock_GridLayout.setContentsMargins(0, 0, 0, 0)
        self.label_productStock = QLabel(self.frame_productStock)
        self.label_productStock.setObjectName(u"label_productStock")
#if QT_CONFIG(tooltip)
        self.label_productStock.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.label_productStock.setText(u"<html><head/><body><p>Stock  <span style=\" color:#ff0000;\">*</span></p></body></html>")
        self.label_productStock.setTextFormat(Qt.RichText)
        self.label_productStock.setTextInteractionFlags(Qt.NoTextInteraction)

        self.frame_productStock_GridLayout.addWidget(self.label_productStock, 0, 0, 1, 1)

        self.lineedit_productStock = QLineEdit(self.frame_productStock)
        self.lineedit_productStock.setObjectName(u"lineedit_productStock")
        self.lineedit_productStock.setText(u"")
        self.lineedit_productStock.setMaxLength(10)
        self.lineedit_productStock.setPlaceholderText(u"Cantidad del producto en stock")
        self.lineedit_productStock.setClearButtonEnabled(True)

        self.frame_productStock_GridLayout.addWidget(self.lineedit_productStock, 0, 1, 1, 1)

        self.label_stockWarning = QLabel(self.frame_productStock)
        self.label_stockWarning.setObjectName(u"label_stockWarning")
        self.label_stockWarning.setEnabled(True)
        sizePolicy.setHeightForWidth(self.label_stockWarning.sizePolicy().hasHeightForWidth())
        self.label_stockWarning.setSizePolicy(sizePolicy)
        self.label_stockWarning.setMinimumSize(QSize(0, 18))
        self.label_stockWarning.setMaximumSize(QSize(16777215, 16777215))
        self.label_stockWarning.setText(u"")
        self.label_stockWarning.setTextFormat(Qt.PlainText)
        self.label_stockWarning.setAlignment(Qt.AlignRight|Qt.AlignTop|Qt.AlignTrailing)
        self.label_stockWarning.setWordWrap(False)
        self.label_stockWarning.setTextInteractionFlags(Qt.NoTextInteraction)

        self.frame_productStock_GridLayout.addWidget(self.label_stockWarning, 1, 0, 1, 2, Qt.AlignRight|Qt.AlignTop)

        self.frame_productStock_GridLayout.setColumnStretch(0, 2)
        self.frame_productStock_GridLayout.setColumnStretch(1, 3)

        self.mainForm_Vlayout.addWidget(self.frame_productStock)

        self.frame_measurementUnit = QFrame(self.mainForm)
        self.frame_measurementUnit.setObjectName(u"frame_measurementUnit")
        sizePolicy.setHeightForWidth(self.frame_measurementUnit.sizePolicy().hasHeightForWidth())
        self.frame_measurementUnit.setSizePolicy(sizePolicy)
        self.frame_measurementUnit.setMinimumSize(QSize(0, 0))
        self.frame_measurementUnit.setMaximumSize(QSize(16777215, 16777215))
#if QT_CONFIG(tooltip)
        self.frame_measurementUnit.setToolTip(u"<html><head/><body><p>Campo opcional. De qu\u00e9 forma se mide el producto en stock. La existencia de este campo es puramente de ayuda al navegar por los productos.</p><p><span style=\" font-weight:600; text-decoration: underline;\">CONSEJO:</span> usar unidades de medida sencillas, tales como kilogramos, litros, bolsas, cajas, unidades, etc.</p></body></html>")
#endif // QT_CONFIG(tooltip)
        self.frame_measurementUnit.setFrameShape(QFrame.NoFrame)
        self.frame_measurementUnit.setFrameShadow(QFrame.Raised)
        self.frame_measurementUnit_Hlayout = QHBoxLayout(self.frame_measurementUnit)
        self.frame_measurementUnit_Hlayout.setSpacing(4)
        self.frame_measurementUnit_Hlayout.setObjectName(u"frame_measurementUnit_Hlayout")
        self.frame_measurementUnit_Hlayout.setContentsMargins(0, 0, 0, 0)
        self.label_measurementUnit = QLabel(self.frame_measurementUnit)
        self.label_measurementUnit.setObjectName(u"label_measurementUnit")
#if QT_CONFIG(tooltip)
        self.label_measurementUnit.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.label_measurementUnit.setText(u"Unidad de medida")
        self.label_measurementUnit.setTextFormat(Qt.PlainText)
        self.label_measurementUnit.setTextInteractionFlags(Qt.NoTextInteraction)

        self.frame_measurementUnit_Hlayout.addWidget(self.label_measurementUnit)

        self.lineedit_measurementUnit = QLineEdit(self.frame_measurementUnit)
        self.lineedit_measurementUnit.setObjectName(u"lineedit_measurementUnit")
        self.lineedit_measurementUnit.setText(u"")
        self.lineedit_measurementUnit.setMaxLength(40)
        self.lineedit_measurementUnit.setPlaceholderText(u"(opcional) Ejs.: bolsas; litros; kgs.")
        self.lineedit_measurementUnit.setClearButtonEnabled(True)

        self.frame_measurementUnit_Hlayout.addWidget(self.lineedit_measurementUnit)

        self.frame_measurementUnit_Hlayout.setStretch(0, 2)
        self.frame_measurementUnit_Hlayout.setStretch(1, 3)

        self.mainForm_Vlayout.addWidget(self.frame_measurementUnit)

        self.frame_unitPrice = QFrame(self.mainForm)
        self.frame_unitPrice.setObjectName(u"frame_unitPrice")
        sizePolicy.setHeightForWidth(self.frame_unitPrice.sizePolicy().hasHeightForWidth())
        self.frame_unitPrice.setSizePolicy(sizePolicy)
        self.frame_unitPrice.setMinimumSize(QSize(0, 0))
        self.frame_unitPrice.setMaximumSize(QSize(16777215, 16777215))
        self.frame_unitPrice.setFrameShape(QFrame.NoFrame)
        self.frame_unitPrice.setFrameShadow(QFrame.Raised)
        self.frame_unitPrice_GridLayout = QGridLayout(self.frame_unitPrice)
        self.frame_unitPrice_GridLayout.setSpacing(4)
        self.frame_unitPrice_GridLayout.setObjectName(u"frame_unitPrice_GridLayout")
        self.frame_unitPrice_GridLayout.setContentsMargins(0, 0, 0, 0)
        self.label_unitPriceWarning = QLabel(self.frame_unitPrice)
        self.label_unitPriceWarning.setObjectName(u"label_unitPriceWarning")
        self.label_unitPriceWarning.setMinimumSize(QSize(0, 18))
        self.label_unitPriceWarning.setText(u"")
        self.label_unitPriceWarning.setTextFormat(Qt.PlainText)
        self.label_unitPriceWarning.setAlignment(Qt.AlignRight|Qt.AlignTop|Qt.AlignTrailing)
        self.label_unitPriceWarning.setWordWrap(False)
        self.label_unitPriceWarning.setTextInteractionFlags(Qt.NoTextInteraction)

        self.frame_unitPrice_GridLayout.addWidget(self.label_unitPriceWarning, 1, 0, 1, 4, Qt.AlignRight|Qt.AlignTop)

        self.label_productUnitPrice = QLabel(self.frame_unitPrice)
        self.label_productUnitPrice.setObjectName(u"label_productUnitPrice")
        self.label_productUnitPrice.setText(u"<html><head/><body><p>Precio unitario  <span style=\" color:#ff0000;\">*</span></p></body></html>")
        self.label_productUnitPrice.setTextFormat(Qt.RichText)
        self.label_productUnitPrice.setTextInteractionFlags(Qt.NoTextInteraction)

        self.frame_unitPrice_GridLayout.addWidget(self.label_productUnitPrice, 0, 0, 1, 2)

        self.lineedit_productUnitPrice = QLineEdit(self.frame_unitPrice)
        self.lineedit_productUnitPrice.setObjectName(u"lineedit_productUnitPrice")
        self.lineedit_productUnitPrice.setInputMask(u"")
        self.lineedit_productUnitPrice.setText(u"")
        self.lineedit_productUnitPrice.setPlaceholderText(u"Precio por unidad del producto")
        self.lineedit_productUnitPrice.setClearButtonEnabled(True)

        self.frame_unitPrice_GridLayout.addWidget(self.lineedit_productUnitPrice, 0, 2, 1, 2)

        self.frame_unitPrice_GridLayout.setColumnStretch(0, 2)
        self.frame_unitPrice_GridLayout.setColumnStretch(1, 2)
        self.frame_unitPrice_GridLayout.setColumnStretch(2, 3)
        self.frame_unitPrice_GridLayout.setColumnStretch(3, 3)

        self.mainForm_Vlayout.addWidget(self.frame_unitPrice)

        self.frame_comercialPrice = QFrame(self.mainForm)
        self.frame_comercialPrice.setObjectName(u"frame_comercialPrice")
        sizePolicy.setHeightForWidth(self.frame_comercialPrice.sizePolicy().hasHeightForWidth())
        self.frame_comercialPrice.setSizePolicy(sizePolicy)
        self.frame_comercialPrice.setMaximumSize(QSize(16777215, 16777215))
#if QT_CONFIG(tooltip)
        self.frame_comercialPrice.setToolTip(u"<html><head/><body><p>Campo opcional. El precio especial que se les cobra a los comercios.</p><p><span style=\" font-weight:600; text-decoration: underline;\">NOTA:</span> no es necesario escribir el signo de &quot;$&quot;.</p></body></html>")
#endif // QT_CONFIG(tooltip)
        self.frame_comercialPrice.setFrameShape(QFrame.NoFrame)
        self.frame_comercialPrice.setFrameShadow(QFrame.Raised)
        self.frame_comercialPrice_GridLayout = QGridLayout(self.frame_comercialPrice)
        self.frame_comercialPrice_GridLayout.setSpacing(4)
        self.frame_comercialPrice_GridLayout.setObjectName(u"frame_comercialPrice_GridLayout")
        self.frame_comercialPrice_GridLayout.setContentsMargins(0, 0, 0, 0)
        self.label_productComercialPrice = QLabel(self.frame_comercialPrice)
        self.label_productComercialPrice.setObjectName(u"label_productComercialPrice")
        self.label_productComercialPrice.setText(u"Precio comercial")
        self.label_productComercialPrice.setTextFormat(Qt.PlainText)
        self.label_productComercialPrice.setTextInteractionFlags(Qt.NoTextInteraction)

        self.frame_comercialPrice_GridLayout.addWidget(self.label_productComercialPrice, 0, 0, 1, 1)

        self.lineedit_productComercialPrice = QLineEdit(self.frame_comercialPrice)
        self.lineedit_productComercialPrice.setObjectName(u"lineedit_productComercialPrice")
        self.lineedit_productComercialPrice.setText(u"")
        self.lineedit_productComercialPrice.setPlaceholderText(u"(opcional) precio para comercios")
        self.lineedit_productComercialPrice.setClearButtonEnabled(True)

        self.frame_comercialPrice_GridLayout.addWidget(self.lineedit_productComercialPrice, 0, 1, 1, 1)

        self.label_comercialPriceWarning = QLabel(self.frame_comercialPrice)
        self.label_comercialPriceWarning.setObjectName(u"label_comercialPriceWarning")
        self.label_comercialPriceWarning.setMinimumSize(QSize(0, 18))
        font = QFont()
        font.setFamilies([u"Tahoma"])
        font.setBold(False)
        font.setItalic(False)
        self.label_comercialPriceWarning.setFont(font)
        self.label_comercialPriceWarning.setText(u"")
        self.label_comercialPriceWarning.setTextFormat(Qt.PlainText)
        self.label_comercialPriceWarning.setAlignment(Qt.AlignRight|Qt.AlignTop|Qt.AlignTrailing)
        self.label_comercialPriceWarning.setWordWrap(False)
        self.label_comercialPriceWarning.setTextInteractionFlags(Qt.NoTextInteraction)

        self.frame_comercialPrice_GridLayout.addWidget(self.label_comercialPriceWarning, 1, 0, 1, 2, Qt.AlignRight|Qt.AlignTop)

        self.frame_comercialPrice_GridLayout.setColumnStretch(0, 2)
        self.frame_comercialPrice_GridLayout.setColumnStretch(1, 3)

        self.mainForm_Vlayout.addWidget(self.frame_comercialPrice)


        self.dialog_Vlayout.addWidget(self.mainForm)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)

        self.dialog_Vlayout.addWidget(self.buttonBox)


        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Nuevo producto", None))
#if QT_CONFIG(tooltip)
        self.frame_unitPrice.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p>El precio que tiene una sola unidad del producto.</p><p><span style=\" font-weight:600; text-decoration: underline;\">NOTA: </span>no es necesario escribir el signo de &quot;$&quot;.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
    # retranslateUi

