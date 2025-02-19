# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'productDialog.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QComboBox, QDialog,
    QDialogButtonBox, QFrame, QGridLayout, QHBoxLayout,
    QLabel, QLineEdit, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(556, 470)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QSize(556, 470))
        Dialog.setMaximumSize(QSize(556, 470))
        Dialog.setStyleSheet(u"* {\n"
"	color: #111;\n"
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
"/* frames */\n"
"QFrame, QWidget {\n"
"	border: none;\n"
"}\n"
"\n"
"\n"
"#frame_upper,\n"
"#frame_middle,\n"
"#frame_lower {\n"
"	background-color: #fff;\n"
"	padding: 5px 3px;\n"
"	border-radius: 10px;\n"
"}\n"
"\n"
"\n"
"#frame_productDescription,\n"
"#frame_measurementUnit {\n"
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
"#label_nameWarning,\n"
"#label_stockWarning,\n"
"#label_categoryWarning,\n"
"#label_unitPriceWarning,\n"
"#label_comercialPriceWarning {\n"
"	background-color: #F65755;\n"
"	color: #fff;\n"
"	border-radius: 5px;\n"
"}\n"
"\n"
"\n"
"/* lineedits */\n"
"QLineEdit {\n"
"	background-color: #e0e1dd;\n"
"	color: #0d1b2a;\n"
"	border: none;\n"
""
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
"/* botones */\n"
"QPushButton {\n"
"	background-color: #415a77;\n"
"	color: #fff;\n"
"	border: none;\n"
"	border-radius: 4px;\n"
"	width: 220px;\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: #3b66ab;\n"
"}\n"
"QPushButton:pressed {\n"
"	background-color: #3b66ab;\n"
"	border: 1px inset #778da9;\n"
"}\n"
"QPushButton:disabled {\n"
"	background-color: rgb(103, 115, 122);\n"
"	color: #999;\n"
"}\n"
"\n"
"\n"
"/* QComboBoxes */\n"
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
"	pa"
                        "dding-right: 3px;\n"
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
"QScrollB"
                        "ar::sub-page:vertical {\n"
"	background: none;\n"
"}\n"
"QScrollBar::add-page:vertical {\n"
"	background: none;\n"
"}")
        Dialog.setSizeGripEnabled(False)
        self.dialog_Vlayout = QVBoxLayout(Dialog)
        self.dialog_Vlayout.setSpacing(5)
        self.dialog_Vlayout.setObjectName(u"dialog_Vlayout")
        self.dialog_Vlayout.setContentsMargins(0, 0, 0, 0)
        self.mainForm = QFrame(Dialog)
        self.mainForm.setObjectName(u"mainForm")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.mainForm.sizePolicy().hasHeightForWidth())
        self.mainForm.setSizePolicy(sizePolicy1)
        self.mainForm.setMinimumSize(QSize(0, 425))
        self.mainForm.setFrameShape(QFrame.Shape.NoFrame)
        self.mainForm.setFrameShadow(QFrame.Shadow.Raised)
        self.mainForm_Vlayout = QVBoxLayout(self.mainForm)
        self.mainForm_Vlayout.setSpacing(15)
        self.mainForm_Vlayout.setObjectName(u"mainForm_Vlayout")
        self.mainForm_Vlayout.setContentsMargins(5, 5, 5, 5)
        self.frame_upper = QFrame(self.mainForm)
        self.frame_upper.setObjectName(u"frame_upper")
        sizePolicy1.setHeightForWidth(self.frame_upper.sizePolicy().hasHeightForWidth())
        self.frame_upper.setSizePolicy(sizePolicy1)
        self.frame_upper.setMinimumSize(QSize(0, 160))
        self.frame_upper.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_upper.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout = QVBoxLayout(self.frame_upper)
        self.verticalLayout.setSpacing(4)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)
        self.frame_productName = QFrame(self.frame_upper)
        self.frame_productName.setObjectName(u"frame_productName")
        sizePolicy1.setHeightForWidth(self.frame_productName.sizePolicy().hasHeightForWidth())
        self.frame_productName.setSizePolicy(sizePolicy1)
        self.frame_productName.setMaximumSize(QSize(16777215, 16777215))
#if QT_CONFIG(tooltip)
        self.frame_productName.setToolTip(u"<html><head/><body><p><span style=\" font-size:12pt;\">El nombre del producto.</span></p><p><span style=\" font-size:12pt; font-weight:600;\">CONSEJO:</span><span style=\" font-size:12pt;\"> mantener el nombre simple, usando marcas de los productos y el tipo como nombre (ejemplo: Dog-Chow razas peque\u00f1as).</span></p></body></html>")
#endif // QT_CONFIG(tooltip)
        self.frame_productName.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_productName.setFrameShadow(QFrame.Shadow.Raised)
        self.frame_productName_GridLayout = QGridLayout(self.frame_productName)
        self.frame_productName_GridLayout.setSpacing(4)
        self.frame_productName_GridLayout.setObjectName(u"frame_productName_GridLayout")
        self.frame_productName_GridLayout.setContentsMargins(0, 0, 0, 0)
        self.label_productName = QLabel(self.frame_productName)
        self.label_productName.setObjectName(u"label_productName")
#if QT_CONFIG(tooltip)
        self.label_productName.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.label_productName.setText(u"<html><head/><body><p>Nombre del producto  <span style=\" color:#ff0000;\">*</span></p></body></html>")
        self.label_productName.setTextFormat(Qt.TextFormat.RichText)
        self.label_productName.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        self.frame_productName_GridLayout.addWidget(self.label_productName, 0, 0, 1, 1)

        self.label_nameWarning = QLabel(self.frame_productName)
        self.label_nameWarning.setObjectName(u"label_nameWarning")
        self.label_nameWarning.setMinimumSize(QSize(0, 18))
#if QT_CONFIG(tooltip)
        self.label_nameWarning.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.label_nameWarning.setText(u"")
        self.label_nameWarning.setTextFormat(Qt.TextFormat.PlainText)
        self.label_nameWarning.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTop|Qt.AlignmentFlag.AlignTrailing)
        self.label_nameWarning.setWordWrap(False)
        self.label_nameWarning.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        self.frame_productName_GridLayout.addWidget(self.label_nameWarning, 1, 0, 1, 2, Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTop)

        self.lineedit_productName = QLineEdit(self.frame_productName)
        self.lineedit_productName.setObjectName(u"lineedit_productName")
        self.lineedit_productName.setMinimumSize(QSize(0, 24))
        self.lineedit_productName.setMaximumSize(QSize(16777215, 24))
        self.lineedit_productName.setText(u"")
        self.lineedit_productName.setMaxLength(50)
        self.lineedit_productName.setPlaceholderText(u"Escribir el nombre del producto")
        self.lineedit_productName.setClearButtonEnabled(True)

        self.frame_productName_GridLayout.addWidget(self.lineedit_productName, 0, 1, 1, 1)

        self.frame_productName_GridLayout.setColumnStretch(0, 2)
        self.frame_productName_GridLayout.setColumnStretch(1, 3)

        self.verticalLayout.addWidget(self.frame_productName)

        self.frame_productCategory = QFrame(self.frame_upper)
        self.frame_productCategory.setObjectName(u"frame_productCategory")
        sizePolicy1.setHeightForWidth(self.frame_productCategory.sizePolicy().hasHeightForWidth())
        self.frame_productCategory.setSizePolicy(sizePolicy1)
        self.frame_productCategory.setMinimumSize(QSize(0, 0))
        self.frame_productCategory.setMaximumSize(QSize(16777215, 16777215))
#if QT_CONFIG(tooltip)
        self.frame_productCategory.setToolTip(u"<html><head/><body><p><span style=\" font-size:12pt;\">Elegir a qu\u00e9 categor\u00eda pertenece el producto.</span></p><p><span style=\" font-size:12pt; font-weight:600;\">CONSEJO:</span><span style=\" font-size:12pt;\"> si se considera que un producto no pertenece a ninguna categor\u00eda de la lista, introducirla en &quot;Varios&quot;.</span></p></body></html>")
#endif // QT_CONFIG(tooltip)
        self.frame_productCategory.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_productCategory.setFrameShadow(QFrame.Shadow.Raised)
        self.frame_productCategory_GridLayout = QGridLayout(self.frame_productCategory)
        self.frame_productCategory_GridLayout.setSpacing(4)
        self.frame_productCategory_GridLayout.setObjectName(u"frame_productCategory_GridLayout")
        self.frame_productCategory_GridLayout.setContentsMargins(0, 0, 0, 0)
        self.label_productCategory = QLabel(self.frame_productCategory)
        self.label_productCategory.setObjectName(u"label_productCategory")
        self.label_productCategory.setText(u"<html><head/><body><p>Categor\u00eda <span style=\" color:#ff0000;\">*</span></p></body></html>")
        self.label_productCategory.setTextFormat(Qt.TextFormat.RichText)
        self.label_productCategory.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        self.frame_productCategory_GridLayout.addWidget(self.label_productCategory, 0, 0, 1, 1)

        self.cb_productCategory = QComboBox(self.frame_productCategory)
        self.cb_productCategory.setObjectName(u"cb_productCategory")
#if QT_CONFIG(tooltip)
        self.cb_productCategory.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.cb_productCategory.setEditable(True)
        self.cb_productCategory.setCurrentText(u"")
        self.cb_productCategory.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContentsOnFirstShow)
        self.cb_productCategory.setPlaceholderText(u"Seleccionar categor\u00eda")
        self.cb_productCategory.setFrame(False)

        self.frame_productCategory_GridLayout.addWidget(self.cb_productCategory, 0, 1, 1, 1)

        self.label_categoryWarning = QLabel(self.frame_productCategory)
        self.label_categoryWarning.setObjectName(u"label_categoryWarning")
        self.label_categoryWarning.setMinimumSize(QSize(0, 18))
        self.label_categoryWarning.setMaximumSize(QSize(16777215, 16777215))
        self.label_categoryWarning.setText(u"")
        self.label_categoryWarning.setTextFormat(Qt.TextFormat.PlainText)
        self.label_categoryWarning.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTop|Qt.AlignmentFlag.AlignTrailing)
        self.label_categoryWarning.setWordWrap(False)
        self.label_categoryWarning.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        self.frame_productCategory_GridLayout.addWidget(self.label_categoryWarning, 1, 0, 1, 2, Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTop)

        self.frame_productCategory_GridLayout.setColumnStretch(0, 2)
        self.frame_productCategory_GridLayout.setColumnStretch(1, 3)

        self.verticalLayout.addWidget(self.frame_productCategory)

        self.frame_productDescription = QFrame(self.frame_upper)
        self.frame_productDescription.setObjectName(u"frame_productDescription")
        sizePolicy1.setHeightForWidth(self.frame_productDescription.sizePolicy().hasHeightForWidth())
        self.frame_productDescription.setSizePolicy(sizePolicy1)
        self.frame_productDescription.setMinimumSize(QSize(0, 0))
        self.frame_productDescription.setMaximumSize(QSize(16777215, 16777215))
#if QT_CONFIG(tooltip)
        self.frame_productDescription.setToolTip(u"<html><head/><body><p><span style=\" font-size:12pt;\">Admite una descripci\u00f3n m\u00e1s extensa si se desea del producto.</span></p><p><span style=\" font-size:12pt; font-weight:600;\">CONSEJO: </span><span style=\" font-size:12pt;\">usar palabras clave en la descripci\u00f3n que permitan posteriormente la b\u00fasqueda del producto mediante esas palabras (algunos ejemplos de palabras clave: perro; adulto; cachorro; urinary; gato; granja; ca\u00f1a; veneno; insecto; hormiga; etc.)</span></p></body></html>")
#endif // QT_CONFIG(tooltip)
        self.frame_productDescription.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_productDescription.setFrameShadow(QFrame.Shadow.Raised)
        self.frame_productDescription_Hlayout = QHBoxLayout(self.frame_productDescription)
        self.frame_productDescription_Hlayout.setSpacing(4)
        self.frame_productDescription_Hlayout.setObjectName(u"frame_productDescription_Hlayout")
        self.frame_productDescription_Hlayout.setContentsMargins(0, 0, 0, 0)
        self.label_productDescription = QLabel(self.frame_productDescription)
        self.label_productDescription.setObjectName(u"label_productDescription")
        self.label_productDescription.setText(u"Descripci\u00f3n del producto")
        self.label_productDescription.setTextFormat(Qt.TextFormat.PlainText)
        self.label_productDescription.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        self.frame_productDescription_Hlayout.addWidget(self.label_productDescription)

        self.lineedit_productDescription = QLineEdit(self.frame_productDescription)
        self.lineedit_productDescription.setObjectName(u"lineedit_productDescription")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.lineedit_productDescription.sizePolicy().hasHeightForWidth())
        self.lineedit_productDescription.setSizePolicy(sizePolicy2)
        self.lineedit_productDescription.setMinimumSize(QSize(0, 24))
        self.lineedit_productDescription.setMaximumSize(QSize(16777215, 24))
        self.lineedit_productDescription.setText(u"")
        self.lineedit_productDescription.setMaxLength(255)
        self.lineedit_productDescription.setFrame(True)
        self.lineedit_productDescription.setPlaceholderText(u"(opcional) Ej.: alimento para gatos adultos")
        self.lineedit_productDescription.setClearButtonEnabled(True)

        self.frame_productDescription_Hlayout.addWidget(self.lineedit_productDescription)

        self.frame_productDescription_Hlayout.setStretch(0, 2)
        self.frame_productDescription_Hlayout.setStretch(1, 3)

        self.verticalLayout.addWidget(self.frame_productDescription)


        self.mainForm_Vlayout.addWidget(self.frame_upper)

        self.frame_middle = QFrame(self.mainForm)
        self.frame_middle.setObjectName(u"frame_middle")
        sizePolicy1.setHeightForWidth(self.frame_middle.sizePolicy().hasHeightForWidth())
        self.frame_middle.setSizePolicy(sizePolicy1)
        self.frame_middle.setMinimumSize(QSize(0, 110))
        self.frame_middle.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_middle.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame_middle)
        self.verticalLayout_2.setSpacing(4)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(5, 5, 5, 5)
        self.frame_productStock = QFrame(self.frame_middle)
        self.frame_productStock.setObjectName(u"frame_productStock")
        sizePolicy1.setHeightForWidth(self.frame_productStock.sizePolicy().hasHeightForWidth())
        self.frame_productStock.setSizePolicy(sizePolicy1)
        self.frame_productStock.setMinimumSize(QSize(0, 0))
        self.frame_productStock.setMaximumSize(QSize(16777215, 16777215))
#if QT_CONFIG(tooltip)
        self.frame_productStock.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.frame_productStock.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_productStock.setFrameShadow(QFrame.Shadow.Raised)
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
        self.label_productStock.setTextFormat(Qt.TextFormat.RichText)
        self.label_productStock.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        self.frame_productStock_GridLayout.addWidget(self.label_productStock, 0, 0, 1, 1)

        self.lineedit_productStock = QLineEdit(self.frame_productStock)
        self.lineedit_productStock.setObjectName(u"lineedit_productStock")
        self.lineedit_productStock.setMinimumSize(QSize(0, 24))
        self.lineedit_productStock.setMaximumSize(QSize(16777215, 24))
        self.lineedit_productStock.setText(u"")
        self.lineedit_productStock.setMaxLength(10)
        self.lineedit_productStock.setPlaceholderText(u"Cantidad del producto en stock")
        self.lineedit_productStock.setClearButtonEnabled(True)

        self.frame_productStock_GridLayout.addWidget(self.lineedit_productStock, 0, 1, 1, 1)

        self.label_stockWarning = QLabel(self.frame_productStock)
        self.label_stockWarning.setObjectName(u"label_stockWarning")
        self.label_stockWarning.setEnabled(True)
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.label_stockWarning.sizePolicy().hasHeightForWidth())
        self.label_stockWarning.setSizePolicy(sizePolicy3)
        self.label_stockWarning.setMinimumSize(QSize(0, 18))
        self.label_stockWarning.setMaximumSize(QSize(16777215, 16777215))
        self.label_stockWarning.setText(u"")
        self.label_stockWarning.setTextFormat(Qt.TextFormat.PlainText)
        self.label_stockWarning.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTop|Qt.AlignmentFlag.AlignTrailing)
        self.label_stockWarning.setWordWrap(False)
        self.label_stockWarning.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        self.frame_productStock_GridLayout.addWidget(self.label_stockWarning, 1, 0, 1, 2, Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTop)

        self.frame_productStock_GridLayout.setColumnStretch(0, 2)
        self.frame_productStock_GridLayout.setColumnStretch(1, 3)

        self.verticalLayout_2.addWidget(self.frame_productStock)

        self.frame_measurementUnit = QFrame(self.frame_middle)
        self.frame_measurementUnit.setObjectName(u"frame_measurementUnit")
        sizePolicy1.setHeightForWidth(self.frame_measurementUnit.sizePolicy().hasHeightForWidth())
        self.frame_measurementUnit.setSizePolicy(sizePolicy1)
        self.frame_measurementUnit.setMinimumSize(QSize(0, 0))
        self.frame_measurementUnit.setMaximumSize(QSize(16777215, 16777215))
#if QT_CONFIG(tooltip)
        self.frame_measurementUnit.setToolTip(u"<html><head/><body><p><span style=\" font-size:12pt;\">Forma en que se mide el producto en stock. La existencia de este campo es puramente de ayuda al navegar por los productos.</span></p><p><span style=\" font-size:12pt; font-weight:700;\">CONSEJO:</span><span style=\" font-size:12pt;\"> usar unidades de medida sencillas, tales como kilogramos, litros, bolsas, cajas, unidades, etc.</span></p></body></html>")
#endif // QT_CONFIG(tooltip)
        self.frame_measurementUnit.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_measurementUnit.setFrameShadow(QFrame.Shadow.Raised)
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
        self.label_measurementUnit.setTextFormat(Qt.TextFormat.PlainText)
        self.label_measurementUnit.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        self.frame_measurementUnit_Hlayout.addWidget(self.label_measurementUnit)

        self.lineedit_measurementUnit = QLineEdit(self.frame_measurementUnit)
        self.lineedit_measurementUnit.setObjectName(u"lineedit_measurementUnit")
        self.lineedit_measurementUnit.setMinimumSize(QSize(0, 24))
        self.lineedit_measurementUnit.setMaximumSize(QSize(16777215, 24))
        self.lineedit_measurementUnit.setText(u"")
        self.lineedit_measurementUnit.setMaxLength(20)
        self.lineedit_measurementUnit.setPlaceholderText(u"(opcional) Ejs.: bolsas; litros; kgs.")
        self.lineedit_measurementUnit.setClearButtonEnabled(True)

        self.frame_measurementUnit_Hlayout.addWidget(self.lineedit_measurementUnit)

        self.frame_measurementUnit_Hlayout.setStretch(0, 2)
        self.frame_measurementUnit_Hlayout.setStretch(1, 3)

        self.verticalLayout_2.addWidget(self.frame_measurementUnit)


        self.mainForm_Vlayout.addWidget(self.frame_middle)

        self.frame_lower = QFrame(self.mainForm)
        self.frame_lower.setObjectName(u"frame_lower")
        sizePolicy1.setHeightForWidth(self.frame_lower.sizePolicy().hasHeightForWidth())
        self.frame_lower.setSizePolicy(sizePolicy1)
        self.frame_lower.setMinimumSize(QSize(0, 125))
        self.frame_lower.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_lower.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame_lower)
        self.verticalLayout_3.setSpacing(4)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(5, 5, 5, 5)
        self.frame_unitPrice = QFrame(self.frame_lower)
        self.frame_unitPrice.setObjectName(u"frame_unitPrice")
        sizePolicy1.setHeightForWidth(self.frame_unitPrice.sizePolicy().hasHeightForWidth())
        self.frame_unitPrice.setSizePolicy(sizePolicy1)
        self.frame_unitPrice.setMinimumSize(QSize(0, 0))
        self.frame_unitPrice.setMaximumSize(QSize(16777215, 16777215))
        self.frame_unitPrice.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_unitPrice.setFrameShadow(QFrame.Shadow.Raised)
        self.frame_unitPrice_GridLayout = QGridLayout(self.frame_unitPrice)
        self.frame_unitPrice_GridLayout.setSpacing(4)
        self.frame_unitPrice_GridLayout.setObjectName(u"frame_unitPrice_GridLayout")
        self.frame_unitPrice_GridLayout.setContentsMargins(0, 0, 0, 0)
        self.label_unitPriceWarning = QLabel(self.frame_unitPrice)
        self.label_unitPriceWarning.setObjectName(u"label_unitPriceWarning")
        self.label_unitPriceWarning.setMinimumSize(QSize(0, 18))
        self.label_unitPriceWarning.setText(u"")
        self.label_unitPriceWarning.setTextFormat(Qt.TextFormat.PlainText)
        self.label_unitPriceWarning.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTop|Qt.AlignmentFlag.AlignTrailing)
        self.label_unitPriceWarning.setWordWrap(False)
        self.label_unitPriceWarning.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        self.frame_unitPrice_GridLayout.addWidget(self.label_unitPriceWarning, 1, 0, 1, 4, Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTop)

        self.label_productUnitPrice = QLabel(self.frame_unitPrice)
        self.label_productUnitPrice.setObjectName(u"label_productUnitPrice")
        self.label_productUnitPrice.setText(u"<html><head/><body><p>Precio p\u00fablico <span style=\" color:#ff0000;\">*</span></p></body></html>")
        self.label_productUnitPrice.setTextFormat(Qt.TextFormat.RichText)
        self.label_productUnitPrice.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        self.frame_unitPrice_GridLayout.addWidget(self.label_productUnitPrice, 0, 0, 1, 2)

        self.lineedit_productUnitPrice = QLineEdit(self.frame_unitPrice)
        self.lineedit_productUnitPrice.setObjectName(u"lineedit_productUnitPrice")
        self.lineedit_productUnitPrice.setMinimumSize(QSize(0, 24))
        self.lineedit_productUnitPrice.setMaximumSize(QSize(16777215, 24))
        self.lineedit_productUnitPrice.setInputMask(u"")
        self.lineedit_productUnitPrice.setText(u"")
        self.lineedit_productUnitPrice.setPlaceholderText(u"Precio al p\u00fablico")
        self.lineedit_productUnitPrice.setClearButtonEnabled(True)

        self.frame_unitPrice_GridLayout.addWidget(self.lineedit_productUnitPrice, 0, 2, 1, 2)

        self.frame_unitPrice_GridLayout.setColumnStretch(0, 2)
        self.frame_unitPrice_GridLayout.setColumnStretch(1, 2)
        self.frame_unitPrice_GridLayout.setColumnStretch(2, 3)
        self.frame_unitPrice_GridLayout.setColumnStretch(3, 3)

        self.verticalLayout_3.addWidget(self.frame_unitPrice)

        self.frame_comercialPrice = QFrame(self.frame_lower)
        self.frame_comercialPrice.setObjectName(u"frame_comercialPrice")
        sizePolicy1.setHeightForWidth(self.frame_comercialPrice.sizePolicy().hasHeightForWidth())
        self.frame_comercialPrice.setSizePolicy(sizePolicy1)
        self.frame_comercialPrice.setMaximumSize(QSize(16777215, 16777215))
#if QT_CONFIG(tooltip)
        self.frame_comercialPrice.setToolTip(u"<html><head/><body><p><span style=\" font-size:12pt;\">El precio que se le cobra a los comercios.</span></p></body></html>")
#endif // QT_CONFIG(tooltip)
        self.frame_comercialPrice.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_comercialPrice.setFrameShadow(QFrame.Shadow.Raised)
        self.frame_comercialPrice_GridLayout = QGridLayout(self.frame_comercialPrice)
        self.frame_comercialPrice_GridLayout.setSpacing(4)
        self.frame_comercialPrice_GridLayout.setObjectName(u"frame_comercialPrice_GridLayout")
        self.frame_comercialPrice_GridLayout.setContentsMargins(0, 0, 0, 0)
        self.label_productComercialPrice = QLabel(self.frame_comercialPrice)
        self.label_productComercialPrice.setObjectName(u"label_productComercialPrice")
        self.label_productComercialPrice.setText(u"Precio comercial")
        self.label_productComercialPrice.setTextFormat(Qt.TextFormat.PlainText)
        self.label_productComercialPrice.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        self.frame_comercialPrice_GridLayout.addWidget(self.label_productComercialPrice, 0, 0, 1, 1)

        self.lineedit_productComercialPrice = QLineEdit(self.frame_comercialPrice)
        self.lineedit_productComercialPrice.setObjectName(u"lineedit_productComercialPrice")
        self.lineedit_productComercialPrice.setMinimumSize(QSize(0, 24))
        self.lineedit_productComercialPrice.setMaximumSize(QSize(16777215, 24))
        self.lineedit_productComercialPrice.setText(u"")
        self.lineedit_productComercialPrice.setPlaceholderText(u"(opcional) precio para comercios")
        self.lineedit_productComercialPrice.setClearButtonEnabled(True)

        self.frame_comercialPrice_GridLayout.addWidget(self.lineedit_productComercialPrice, 0, 1, 1, 1)

        self.label_comercialPriceWarning = QLabel(self.frame_comercialPrice)
        self.label_comercialPriceWarning.setObjectName(u"label_comercialPriceWarning")
        self.label_comercialPriceWarning.setMinimumSize(QSize(0, 18))
        font = QFont()
        font.setFamilies([u"Futura"])
        font.setBold(False)
        font.setItalic(False)
        self.label_comercialPriceWarning.setFont(font)
        self.label_comercialPriceWarning.setText(u"")
        self.label_comercialPriceWarning.setTextFormat(Qt.TextFormat.PlainText)
        self.label_comercialPriceWarning.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTop|Qt.AlignmentFlag.AlignTrailing)
        self.label_comercialPriceWarning.setWordWrap(False)
        self.label_comercialPriceWarning.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        self.frame_comercialPrice_GridLayout.addWidget(self.label_comercialPriceWarning, 1, 0, 1, 2, Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTop)

        self.frame_comercialPrice_GridLayout.setColumnStretch(0, 2)
        self.frame_comercialPrice_GridLayout.setColumnStretch(1, 3)

        self.verticalLayout_3.addWidget(self.frame_comercialPrice)


        self.mainForm_Vlayout.addWidget(self.frame_lower)


        self.dialog_Vlayout.addWidget(self.mainForm)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        sizePolicy.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy)
        self.buttonBox.setMinimumSize(QSize(556, 26))
        self.buttonBox.setMaximumSize(QSize(556, 26))
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)
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
        self.frame_unitPrice.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-size:12pt;\">El precio que se le cobra al p\u00fablico.</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
    # retranslateUi

