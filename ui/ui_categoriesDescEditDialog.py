# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'categoriesDescEditDialog.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QFrame, QLabel, QSizePolicy, QTextEdit,
    QVBoxLayout, QWidget)

class Ui_CategoryDescEditDialog(object):
    def setupUi(self, CategoryDescEditDialog):
        if not CategoryDescEditDialog.objectName():
            CategoryDescEditDialog.setObjectName(u"CategoryDescEditDialog")
        CategoryDescEditDialog.setWindowModality(Qt.WindowModality.ApplicationModal)
        CategoryDescEditDialog.setEnabled(True)
        CategoryDescEditDialog.resize(400, 300)
        CategoryDescEditDialog.setMinimumSize(QSize(250, 250))
        CategoryDescEditDialog.setStyleSheet(u"* {\n"
"	color: #111;\n"
"	font-family: \"Futura\", \"Verdana\", \"Sans-Serif\";\n"
"	font-size: 14px;\n"
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
"QDialog {\n"
"	background-color: #e0e1dd;\n"
"}\n"
"\n"
"\n"
"#central_widget {\n"
"	background-color: #fff;\n"
"	padding: 5px 3px;\n"
"	border-radius: 10px;\n"
"	margin-bottom: 5px;\n"
"}\n"
"\n"
"\n"
"QToolTip {\n"
"	background-color: #fff;\n"
"	color: #0d1b2a;\n"
"}\n"
"\n"
"\n"
"/* textedit */\n"
"QTextEdit {\n"
"	background-color: #e0e1dd;\n"
"	selection-background-color: #3b66ab;\n"
"	selection-color: #fff;\n"
"	border-radius: 10px;\n"
"	padding-left: 3px;\n"
"	padding-right: 3px;\n"
"}\n"
"\n"
"\n"
"/* label */\n"
"QLabel {\n"
"	background-color: #fff;\n"
"}\n"
"\n"
"\n"
"/* pushbuttons */\n"
"QPushButton[text='Guardar'] {\n"
"	background-color: #415a77;\n"
"	color: #fff;\n"
"	border: none;\n"
"}\n"
"\n"
"QPushButton[text='Descartar'] {\n"
"	background-color: #fff;\n"
"	color: #111;\n"
""
                        "	border: 1px solid #111;\n"
"}\n"
"\n"
"QPushButton {\n"
"	border-radius: 4px;\n"
"	width: 150px;\n"
"	height: 25px;\n"
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
"	background-color: rgb(103, 115, 122);\n"
"	color: #999;\n"
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
""
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
        CategoryDescEditDialog.setSizeGripEnabled(True)
        CategoryDescEditDialog.setModal(True)
        self.verticalLayout = QVBoxLayout(CategoryDescEditDialog)
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 3)
        self.central_widget = QWidget(CategoryDescEditDialog)
        self.central_widget.setObjectName(u"central_widget")
        self.verticalLayout_2 = QVBoxLayout(self.central_widget)
        self.verticalLayout_2.setSpacing(5)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(4, 4, 4, 5)
        self.te_category_desc = QTextEdit(self.central_widget)
        self.te_category_desc.setObjectName(u"te_category_desc")
        self.te_category_desc.setFrameShape(QFrame.Shape.NoFrame)
        self.te_category_desc.setFrameShadow(QFrame.Shadow.Plain)
        self.te_category_desc.setLineWidth(0)
        self.te_category_desc.setAutoFormatting(QTextEdit.AutoFormattingFlag.AutoAll)
        self.te_category_desc.setTabChangesFocus(False)
        self.te_category_desc.setUndoRedoEnabled(True)
        self.te_category_desc.setOverwriteMode(False)
        self.te_category_desc.setTabStopDistance(20.000000000000000)
        self.te_category_desc.setAcceptRichText(False)
        self.te_category_desc.setTextInteractionFlags(Qt.TextInteractionFlag.TextEditorInteraction)

        self.verticalLayout_2.addWidget(self.te_category_desc)

        self.label_show_character_count = QLabel(self.central_widget)
        self.label_show_character_count.setObjectName(u"label_show_character_count")
        self.label_show_character_count.setTextFormat(Qt.TextFormat.PlainText)
        self.label_show_character_count.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        self.verticalLayout_2.addWidget(self.label_show_character_count)


        self.verticalLayout.addWidget(self.central_widget)

        self.buttonBox = QDialogButtonBox(CategoryDescEditDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setEnabled(True)
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Discard|QDialogButtonBox.StandardButton.Save)
        self.buttonBox.setCenterButtons(True)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(CategoryDescEditDialog)
        self.buttonBox.accepted.connect(CategoryDescEditDialog.accept)
        self.buttonBox.rejected.connect(CategoryDescEditDialog.reject)

        QMetaObject.connectSlotsByName(CategoryDescEditDialog)
    # setupUi

    def retranslateUi(self, CategoryDescEditDialog):
        CategoryDescEditDialog.setWindowTitle(QCoreApplication.translate("CategoryDescEditDialog", u"Nueva descripci\u00f3n de categor\u00eda", None))
#if QT_CONFIG(tooltip)
        self.te_category_desc.setToolTip(QCoreApplication.translate("CategoryDescEditDialog", u"<html><head/><body><p><span style=\" font-size:11pt;\">Permite colocarle una descripci\u00f3n a la categor\u00eda seleccionada.</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.te_category_desc.setPlaceholderText(QCoreApplication.translate("CategoryDescEditDialog", u"Escribir una descripci\u00f3n para la categor\u00eda...", None))
        self.label_show_character_count.setText(QCoreApplication.translate("CategoryDescEditDialog", u"cantidad de caracteres: x/256", None))
    # retranslateUi

