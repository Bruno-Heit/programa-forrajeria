# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'warnAccountHasBalanceDialog.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QAbstractItemView, QApplication, QCheckBox,
    QDialog, QDialogButtonBox, QFrame, QLabel,
    QListView, QListWidget, QListWidgetItem, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_AccountHasBalDialog(object):
    def setupUi(self, AccountHasBalDialog):
        if not AccountHasBalDialog.objectName():
            AccountHasBalDialog.setObjectName(u"AccountHasBalDialog")
        AccountHasBalDialog.resize(400, 355)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(AccountHasBalDialog.sizePolicy().hasHeightForWidth())
        AccountHasBalDialog.setSizePolicy(sizePolicy)
        AccountHasBalDialog.setMinimumSize(QSize(400, 0))
        AccountHasBalDialog.setMaximumSize(QSize(400, 355))
        AccountHasBalDialog.setStyleSheet(u"* {\n"
"	color: #111;\n"
"	font-family: \"Futura\", \"Verdana\", \"Sans-Serif\";\n"
"	font-size: 14px;\n"
"}\n"
"\n"
"\n"
"QMenu {\n"
"	background-color: #fff;\n"
"	color: #111;\n"
"	font-size: 13px;\n"
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
"#body {\n"
"	padding: 0px 3px;\n"
"	border-radius: 10px;\n"
"}\n"
"\n"
"\n"
"/* labels */\n"
"QLabel {\n"
"	padding-right: 2px;\n"
"	padding-left: 2px;\n"
"}\n"
"\n"
"#label_askDelete {\n"
"	font-weight: bold;\n"
"}\n"
"#label_balanceWarning {\n"
"	margin-top: 10px;\n"
"	color: #F65755;\n"
"}\n"
"\n"
"\n"
"/* checkbox */\n"
"QCheckBox {\n"
"	margin-top: 5px;\n"
"	padding: 0 3px;\n"
"	spacing: 5px;\n"
"    border: none;\n"
"	border-radius: 3px;\n"
"}\n"
"QCheckBox:hover,\n"
"QCheckBox:focus {\n"
"	background-color: #3b66ab;\n"
"}\n"
"QCheckBox:checked {\n"
"	background-color: #3b66a"
                        "b;\n"
"    border: 1px inset #778da9;\n"
"}\n"
"QCheckBox:disabled {\n"
"	background-color: rgb(103, 115, 122);\n"
"    color: #999;\n"
"}\n"
"\n"
"\n"
"/* listtable y header */\n"
"QListWidget {\n"
"	color: #0d1b2a;\n"
"	background-color: #fff;\n"
"	border: None;\n"
"	border-radius: 10px;\n"
"}\n"
"QListWidget::item:hover {\n"
"	background-color: #778da9;\n"
"}\n"
"QListWidget::item:selected {\n"
"	background-color: #778da9;\n"
"	border: 1px solid #fff;\n"
"}\n"
"/* QHeaderView */\n"
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
"	background-color: "
                        "#3b465b;\n"
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
"}")
        AccountHasBalDialog.setSizeGripEnabled(False)
        self.verticalLayout = QVBoxLayout(AccountHasBalDialog)
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 3)
        self.body = QFrame(AccountHasBalDialog)
        self.body.setObjectName(u"body")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.body.sizePolicy().hasHeightForWidth())
        self.body.setSizePolicy(sizePolicy1)
        self.body.setMinimumSize(QSize(0, 0))
        self.verticalLayout_2 = QVBoxLayout(self.body)
        self.verticalLayout_2.setSpacing(10)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(5, 5, 5, 5)
        self.frame_labels = QFrame(self.body)
        self.frame_labels.setObjectName(u"frame_labels")
        self.frame_labels.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_labels.setFrameShadow(QFrame.Shadow.Plain)
        self.verticalLayout_3 = QVBoxLayout(self.frame_labels)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label_askDelete = QLabel(self.frame_labels)
        self.label_askDelete.setObjectName(u"label_askDelete")
        self.label_askDelete.setMinimumSize(QSize(0, 40))
        self.label_askDelete.setTextFormat(Qt.TextFormat.PlainText)
        self.label_askDelete.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_askDelete.setWordWrap(True)

        self.verticalLayout_3.addWidget(self.label_askDelete)

        self.label_accountsWithoutZeroBal = QLabel(self.frame_labels)
        self.label_accountsWithoutZeroBal.setObjectName(u"label_accountsWithoutZeroBal")
        self.label_accountsWithoutZeroBal.setMinimumSize(QSize(0, 40))
        self.label_accountsWithoutZeroBal.setTextFormat(Qt.TextFormat.PlainText)
        self.label_accountsWithoutZeroBal.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_accountsWithoutZeroBal.setWordWrap(True)

        self.verticalLayout_3.addWidget(self.label_accountsWithoutZeroBal)

        self.label_balanceWarning = QLabel(self.frame_labels)
        self.label_balanceWarning.setObjectName(u"label_balanceWarning")
        self.label_balanceWarning.setTextFormat(Qt.TextFormat.PlainText)
        self.label_balanceWarning.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_balanceWarning.setWordWrap(True)

        self.verticalLayout_3.addWidget(self.label_balanceWarning)


        self.verticalLayout_2.addWidget(self.frame_labels)

        self.checkb_toggleAccountsList = QCheckBox(self.body)
        self.checkb_toggleAccountsList.setObjectName(u"checkb_toggleAccountsList")
        self.checkb_toggleAccountsList.setMinimumSize(QSize(0, 20))

        self.verticalLayout_2.addWidget(self.checkb_toggleAccountsList, 0, Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)

        self.lw_accountsWithBal = QListWidget(self.body)
        self.lw_accountsWithBal.setObjectName(u"lw_accountsWithBal")
        self.lw_accountsWithBal.setEnabled(False)
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.lw_accountsWithBal.sizePolicy().hasHeightForWidth())
        self.lw_accountsWithBal.setSizePolicy(sizePolicy2)
        self.lw_accountsWithBal.setMinimumSize(QSize(380, 200))
        self.lw_accountsWithBal.setMaximumSize(QSize(380, 200))
        self.lw_accountsWithBal.setFrameShape(QFrame.Shape.NoFrame)
        self.lw_accountsWithBal.setFrameShadow(QFrame.Shadow.Plain)
        self.lw_accountsWithBal.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.lw_accountsWithBal.setProperty("showDropIndicator", False)
        self.lw_accountsWithBal.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.lw_accountsWithBal.setHorizontalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.lw_accountsWithBal.setProperty("isWrapping", False)
        self.lw_accountsWithBal.setResizeMode(QListView.ResizeMode.Adjust)
        self.lw_accountsWithBal.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.lw_accountsWithBal, 0, Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignTop)


        self.verticalLayout.addWidget(self.body, 0, Qt.AlignmentFlag.AlignTop)

        self.buttonBox = QDialogButtonBox(AccountHasBalDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.No|QDialogButtonBox.StandardButton.Yes)
        self.buttonBox.setCenterButtons(True)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(AccountHasBalDialog)
        self.buttonBox.accepted.connect(AccountHasBalDialog.accept)
        self.buttonBox.rejected.connect(AccountHasBalDialog.reject)

        QMetaObject.connectSlotsByName(AccountHasBalDialog)
    # setupUi

    def retranslateUi(self, AccountHasBalDialog):
        AccountHasBalDialog.setWindowTitle(QCoreApplication.translate("AccountHasBalDialog", u"Dialog", None))
#if QT_CONFIG(tooltip)
        self.body.setToolTip(QCoreApplication.translate("AccountHasBalDialog", u"<html><head/><body><p><span style=\" font-size:11pt;\">Se considera que una cuenta tiene saldo nulo o cero cuando el balance es igual a cero, por lo que no tiene saldo a favor (acreedor) ni en contra (deudor).</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_askDelete.setText(QCoreApplication.translate("AccountHasBalDialog", u"\u00bfEst\u00e1 seguro de dar de baja las cuentas corrientes seleccionadas?", None))
        self.label_accountsWithoutZeroBal.setText(QCoreApplication.translate("AccountHasBalDialog", u"Hay _ cuentas corrientes seleccionadas con saldo no nulo", None))
#if QT_CONFIG(tooltip)
        self.label_balanceWarning.setToolTip(QCoreApplication.translate("AccountHasBalDialog", u"<html><head/><body><p><span style=\" font-size:11pt;\">El saldo deudor/a favor de cada cuenta asociada ser\u00e1 considerado 0.</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_balanceWarning.setText(QCoreApplication.translate("AccountHasBalDialog", u"Nota: el balance de las cuentas ser\u00e1 considerado saldado", None))
        self.checkb_toggleAccountsList.setText(QCoreApplication.translate("AccountHasBalDialog", u"Mostrar cuentas con saldo", None))
    # retranslateUi

