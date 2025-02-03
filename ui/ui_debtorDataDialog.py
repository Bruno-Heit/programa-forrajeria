# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'debtorDataDialog.ui'
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
    QFrame, QGridLayout, QLabel, QLineEdit,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_debtorDataDialog(object):
    def setupUi(self, debtorDataDialog):
        if not debtorDataDialog.objectName():
            debtorDataDialog.setObjectName(u"debtorDataDialog")
        debtorDataDialog.resize(613, 263)
        debtorDataDialog.setMinimumSize(QSize(613, 263))
        debtorDataDialog.setStyleSheet(u"* {\n"
"	color: #111;\n"
"	border-color: #7f7e0b;\n"
"	font-family: \"Tahoma\", \"Verdana\", \"Sans-Serif\";\n"
"	font-size: 16px;\n"
"}\n"
"\n"
"\n"
"QToolTip {\n"
"	background-color: #fff;\n"
"}\n"
"\n"
"\n"
"QDialog {\n"
"	background-color: qlineargradient(spread:pad, x1:0, y1:0.124364, x2:1, y2:0.409182, stop:0 rgba(178, 229, 246, 255), stop:0.393082 rgba(143, 201, 220, 255), stop:0.59306 rgba(67, 118, 134, 255), stop:0.761006 rgba(152, 151, 154, 255), stop:0.795597 rgba(110, 108, 112, 255), stop:0.845912 rgba(110, 108, 112, 255), stop:0.946372 rgba(67, 118, 134, 255), stop:1 rgba(143, 201, 220, 255));\n"
"}\n"
"\n"
"\n"
"#label_debtorName_feedback,\n"
"#label_debtorSurname_feedback,\n"
"#label_phoneNumber_feedback,\n"
"#label_postalCode_feedback {\n"
"	color: #dc2627;\n"
"	border: 1px solid #dc2627;\n"
"	background-color: rgba(224,164,164,0.7);\n"
"}\n"
"\n"
"\n"
"QLineEdit {\n"
"	background-color: rgba(255, 255, 255, 0.6);\n"
"	border: none;\n"
"	border-top: 1px solid;\n"
"	border-bottom: 1px solid;\n"
""
                        "	height: 24px;\n"
"}\n"
"QLineEdit:focus {\n"
"	background-color: rgba(176, 214, 245, 0.6);\n"
"	border: 1px solid;\n"
"	border-color: #0b7e7f;\n"
"	font-size: 18px;\n"
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
"}")
        self.verticalLayout = QVBoxLayout(debtorDataDialog)
        self.verticalLayout.setSpacing(4)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(5, 10, 5, 5)
        self.debtor_data = QFrame(debtorDataDialog)
        self.debtor_data.setObjectName(u"debtor_data")
        self.debtor_data.setFrameShape(QFrame.Shape.NoFrame)
        self.debtor_data.setFrameShadow(QFrame.Shadow.Raised)
        self.debtor_data_GridLayout = QGridLayout(self.debtor_data)
        self.debtor_data_GridLayout.setSpacing(4)
        self.debtor_data_GridLayout.setObjectName(u"debtor_data_GridLayout")
        self.debtor_data_GridLayout.setContentsMargins(0, 0, 0, 0)
        self.lineEdit_direction = QLineEdit(self.debtor_data)
        self.lineEdit_direction.setObjectName(u"lineEdit_direction")
#if QT_CONFIG(tooltip)
        self.lineEdit_direction.setToolTip(u"<html><head/><body><p><span style=\" font-size:12pt;\">(Opcional) direcci\u00f3n del propietario.</span></p></body></html>")
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
        self.lineEdit_postalCode.setToolTip(u"<html><head/><body><p><span style=\" font-size:12pt;\">(Opcional) c\u00f3digo postal del propietario.</span></p><p><span style=\" font-size:12pt; font-weight:600; text-decoration: underline;\">NOTA:</span><span style=\" font-size:12pt;\"> por conveniencia s\u00f3lo admite c\u00f3digos postales de Argentina.</span></p></body></html>")
#endif // QT_CONFIG(tooltip)
        self.lineEdit_postalCode.setInputMask(u"")
        self.lineEdit_postalCode.setText(u"")
        self.lineEdit_postalCode.setPlaceholderText(u"(Opcional) Ej.: 6703")
        self.lineEdit_postalCode.setClearButtonEnabled(True)

        self.debtor_data_GridLayout.addWidget(self.lineEdit_postalCode, 7, 2, 1, 3)

        self.label_debtorSurname_feedback = QLabel(self.debtor_data)
        self.label_debtorSurname_feedback.setObjectName(u"label_debtorSurname_feedback")
        self.label_debtorSurname_feedback.setText(u"")
        self.label_debtorSurname_feedback.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_debtorSurname_feedback.setWordWrap(False)
        self.label_debtorSurname_feedback.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        self.debtor_data_GridLayout.addWidget(self.label_debtorSurname_feedback, 2, 4, 1, 1, Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTop)

        self.lineEdit_debtorName = QLineEdit(self.debtor_data)
        self.lineEdit_debtorName.setObjectName(u"lineEdit_debtorName")
#if QT_CONFIG(tooltip)
        self.lineEdit_debtorName.setToolTip(u"<html><head/><body><p><span style=\" font-size:12pt;\">El nombre del propietario.</span></p></body></html>")
#endif // QT_CONFIG(tooltip)
        self.lineEdit_debtorName.setText(u"")
        self.lineEdit_debtorName.setFrame(False)
        self.lineEdit_debtorName.setPlaceholderText(u"Nombre")
        self.lineEdit_debtorName.setClearButtonEnabled(True)

        self.debtor_data_GridLayout.addWidget(self.lineEdit_debtorName, 1, 1, 1, 2)

        self.label_phoneNumber_feedback = QLabel(self.debtor_data)
        self.label_phoneNumber_feedback.setObjectName(u"label_phoneNumber_feedback")
        self.label_phoneNumber_feedback.setText(u"")
        self.label_phoneNumber_feedback.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_phoneNumber_feedback.setWordWrap(False)
        self.label_phoneNumber_feedback.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        self.debtor_data_GridLayout.addWidget(self.label_phoneNumber_feedback, 4, 0, 1, 5, Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignTop)

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
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_debtorInfo.sizePolicy().hasHeightForWidth())
        self.label_debtorInfo.setSizePolicy(sizePolicy)
        self.label_debtorInfo.setStyleSheet(u"font-size: 18px;\n"
"color: rgb(8, 68, 68);\n"
"margin-left: 30px;\n"
"margin-right: 30px;\n"
"margin-bottom: 7px;\n"
"border-bottom: 1px solid;\n"
"border-color: rgb(11, 126, 127);")
        self.label_debtorInfo.setText(u"DATOS DEL PROPIETARIO DE LA CUENTA")
        self.label_debtorInfo.setTextFormat(Qt.TextFormat.PlainText)
        self.label_debtorInfo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_debtorInfo.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

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
        self.lineEdit_debtorSurname.setToolTip(u"<html><head/><body><p><span style=\" font-size:12pt;\">El apellido del propietario.</span></p></body></html>")
#endif // QT_CONFIG(tooltip)
        self.lineEdit_debtorSurname.setText(u"")
        self.lineEdit_debtorSurname.setFrame(False)
        self.lineEdit_debtorSurname.setPlaceholderText(u"Apellido")
        self.lineEdit_debtorSurname.setClearButtonEnabled(True)

        self.debtor_data_GridLayout.addWidget(self.lineEdit_debtorSurname, 1, 4, 1, 1)

        self.label_direction = QLabel(self.debtor_data)
        self.label_direction.setObjectName(u"label_direction")

        self.debtor_data_GridLayout.addWidget(self.label_direction, 6, 0, 1, 2)

        self.label_debtorName_feedback = QLabel(self.debtor_data)
        self.label_debtorName_feedback.setObjectName(u"label_debtorName_feedback")
        self.label_debtorName_feedback.setText(u"")
        self.label_debtorName_feedback.setTextFormat(Qt.TextFormat.PlainText)
        self.label_debtorName_feedback.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_debtorName_feedback.setWordWrap(False)
        self.label_debtorName_feedback.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        self.debtor_data_GridLayout.addWidget(self.label_debtorName_feedback, 2, 1, 1, 2, Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)

        self.lineEdit_phoneNumber = QLineEdit(self.debtor_data)
        self.lineEdit_phoneNumber.setObjectName(u"lineEdit_phoneNumber")
#if QT_CONFIG(tooltip)
        self.lineEdit_phoneNumber.setToolTip(u"<html><head/><body><p><span style=\" font-size:12pt;\">(Opcional) n\u00famero de tel\u00e9fono del propietario.</span></p></body></html>")
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
        self.label_postalCode_feedback.setText(u"")
        self.label_postalCode_feedback.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_postalCode_feedback.setWordWrap(False)
        self.label_postalCode_feedback.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        self.debtor_data_GridLayout.addWidget(self.label_postalCode_feedback, 8, 0, 1, 5, Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignTop)

        self.debtor_data_GridLayout.setColumnStretch(1, 1)
        self.debtor_data_GridLayout.setColumnStretch(2, 1)
        self.debtor_data_GridLayout.setColumnStretch(4, 2)

        self.verticalLayout.addWidget(self.debtor_data)

        self.buttonBox = QDialogButtonBox(debtorDataDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setCenterButtons(True)

        self.verticalLayout.addWidget(self.buttonBox)

        QWidget.setTabOrder(self.lineEdit_debtorName, self.lineEdit_debtorSurname)
        QWidget.setTabOrder(self.lineEdit_debtorSurname, self.lineEdit_phoneNumber)
        QWidget.setTabOrder(self.lineEdit_phoneNumber, self.lineEdit_direction)
        QWidget.setTabOrder(self.lineEdit_direction, self.lineEdit_postalCode)

        self.retranslateUi(debtorDataDialog)
        self.buttonBox.accepted.connect(debtorDataDialog.accept)
        self.buttonBox.rejected.connect(debtorDataDialog.reject)

        QMetaObject.connectSlotsByName(debtorDataDialog)
    # setupUi

    def retranslateUi(self, debtorDataDialog):
        debtorDataDialog.setWindowTitle(QCoreApplication.translate("debtorDataDialog", u"Dialog", None))
        self.label_phoneNumber.setText(QCoreApplication.translate("debtorDataDialog", u"N\u00fam. de tel\u00e9fono", None))
        self.label_postalCode.setText(QCoreApplication.translate("debtorDataDialog", u"C\u00f3digo postal", None))
        self.label_direction.setText(QCoreApplication.translate("debtorDataDialog", u"Direcci\u00f3n", None))
    # retranslateUi

