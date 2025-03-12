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
        debtorDataDialog.resize(555, 346)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(debtorDataDialog.sizePolicy().hasHeightForWidth())
        debtorDataDialog.setSizePolicy(sizePolicy)
        debtorDataDialog.setMinimumSize(QSize(555, 320))
        debtorDataDialog.setMaximumSize(QSize(556, 10000))
        debtorDataDialog.setStyleSheet(u"* {\n"
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
"#mandatory_data,\n"
"#additional_data {\n"
"	background-color: #fff;\n"
"	border-radius: 10px;\n"
"}\n"
"\n"
"\n"
"#mandatory_data {\n"
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
"#label_debtorName_feedback,\n"
"#label_debtorSurname_feedback,\n"
"#label_phoneNumber_feedback,\n"
"#label_postalCode_feedback {\n"
"	background-color: #F65755;\n"
"	color: #fff;\n"
"	border-radius: 5px;\n"
"	margin: 0px 10px;\n"
"}\n"
"\n"
"#label_debtor_header {\n"
"	font-family: \"Arial\", \"Calibri\", \"Sans-Serif\";\n"
"	font-size: 18px;\n"
"	font-weight: 600px;\n"
"}\n"
"\n"
"\n"
"/* lineedits */\n"
"QLineEdit {\n"
"	background-color: #e0e1dd;\n"
"	col"
                        "or: #0d1b2a;\n"
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
"#lineEdit_direction:disabled,\n"
"#lineEdit_phoneNumber:disabled,\n"
"#lineEdit_postalCode:disabled {\n"
"	background-color: #e0e1dd;\n"
"	color: #0d1b2a;\n"
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
"	background-color: rgb(103, 115, 122);\n"
"	color: #999;\n"
"}")
        self.verticalLayout = QVBoxLayout(debtorDataDialog)
        self.verticalLayout.setSpacing(4)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(5, 0, 5, 5)
        self.debtor_data = QFrame(debtorDataDialog)
        self.debtor_data.setObjectName(u"debtor_data")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.debtor_data.sizePolicy().hasHeightForWidth())
        self.debtor_data.setSizePolicy(sizePolicy1)
        self.debtor_data.setMinimumSize(QSize(0, 281))
        self.debtor_data.setMaximumSize(QSize(16777215, 300))
        self.debtor_data.setFrameShape(QFrame.Shape.NoFrame)
        self.debtor_data.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.debtor_data)
        self.verticalLayout_2.setSpacing(8)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 5, 0, 5)
        self.label_debtor_header = QLabel(self.debtor_data)
        self.label_debtor_header.setObjectName(u"label_debtor_header")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_debtor_header.sizePolicy().hasHeightForWidth())
        self.label_debtor_header.setSizePolicy(sizePolicy2)
        self.label_debtor_header.setStyleSheet(u"")
        self.label_debtor_header.setText(u"Informaci\u00f3n del propietario de la cuenta")
        self.label_debtor_header.setTextFormat(Qt.TextFormat.PlainText)
        self.label_debtor_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_debtor_header.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        self.verticalLayout_2.addWidget(self.label_debtor_header)

        self.mandatory_data = QWidget(self.debtor_data)
        self.mandatory_data.setObjectName(u"mandatory_data")
        sizePolicy1.setHeightForWidth(self.mandatory_data.sizePolicy().hasHeightForWidth())
        self.mandatory_data.setSizePolicy(sizePolicy1)
        self.mandatory_data.setMinimumSize(QSize(0, 80))
        self.mandatory_data.setMaximumSize(QSize(10000, 104))
        self.gridLayout = QGridLayout(self.mandatory_data)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(3, 5, 3, 5)
        self.lineEdit_debtorName = QLineEdit(self.mandatory_data)
        self.lineEdit_debtorName.setObjectName(u"lineEdit_debtorName")
#if QT_CONFIG(tooltip)
        self.lineEdit_debtorName.setToolTip(u"<html><head/><body><p><span style=\" font-size:12pt;\">El nombre del propietario.</span></p></body></html>")
#endif // QT_CONFIG(tooltip)
        self.lineEdit_debtorName.setText(u"")
        self.lineEdit_debtorName.setFrame(False)
        self.lineEdit_debtorName.setPlaceholderText(u"Nombre")
        self.lineEdit_debtorName.setClearButtonEnabled(True)

        self.gridLayout.addWidget(self.lineEdit_debtorName, 0, 1, 1, 1)

        self.lineEdit_debtorSurname = QLineEdit(self.mandatory_data)
        self.lineEdit_debtorSurname.setObjectName(u"lineEdit_debtorSurname")
#if QT_CONFIG(tooltip)
        self.lineEdit_debtorSurname.setToolTip(u"<html><head/><body><p><span style=\" font-size:12pt;\">El apellido del propietario.</span></p></body></html>")
#endif // QT_CONFIG(tooltip)
        self.lineEdit_debtorSurname.setText(u"")
        self.lineEdit_debtorSurname.setFrame(False)
        self.lineEdit_debtorSurname.setPlaceholderText(u"Apellido")
        self.lineEdit_debtorSurname.setClearButtonEnabled(True)

        self.gridLayout.addWidget(self.lineEdit_debtorSurname, 0, 3, 1, 1)

        self.label_nameMark = QLabel(self.mandatory_data)
        self.label_nameMark.setObjectName(u"label_nameMark")
#if QT_CONFIG(tooltip)
        self.label_nameMark.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.label_nameMark.setText(u"<html><head/><body><p><span style=\" color:#ff0000;\">*</span></p></body></html>")

        self.gridLayout.addWidget(self.label_nameMark, 0, 0, 1, 1)

        self.label_surnameMark = QLabel(self.mandatory_data)
        self.label_surnameMark.setObjectName(u"label_surnameMark")
#if QT_CONFIG(tooltip)
        self.label_surnameMark.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.label_surnameMark.setText(u"<html><head/><body><p><span style=\" color:#ff0000;\">*</span></p></body></html>")

        self.gridLayout.addWidget(self.label_surnameMark, 0, 2, 1, 1)

        self.label_debtorSurname_feedback = QLabel(self.mandatory_data)
        self.label_debtorSurname_feedback.setObjectName(u"label_debtorSurname_feedback")
        self.label_debtorSurname_feedback.setEnabled(True)
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.label_debtorSurname_feedback.sizePolicy().hasHeightForWidth())
        self.label_debtorSurname_feedback.setSizePolicy(sizePolicy3)
        self.label_debtorSurname_feedback.setMinimumSize(QSize(0, 20))
        self.label_debtorSurname_feedback.setMaximumSize(QSize(16777215, 40))
        self.label_debtorSurname_feedback.setText(u"")
        self.label_debtorSurname_feedback.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_debtorSurname_feedback.setWordWrap(True)
        self.label_debtorSurname_feedback.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        self.gridLayout.addWidget(self.label_debtorSurname_feedback, 1, 3, 1, 1)

        self.label_debtorName_feedback = QLabel(self.mandatory_data)
        self.label_debtorName_feedback.setObjectName(u"label_debtorName_feedback")
        self.label_debtorName_feedback.setEnabled(True)
        sizePolicy3.setHeightForWidth(self.label_debtorName_feedback.sizePolicy().hasHeightForWidth())
        self.label_debtorName_feedback.setSizePolicy(sizePolicy3)
        self.label_debtorName_feedback.setMinimumSize(QSize(0, 20))
        self.label_debtorName_feedback.setMaximumSize(QSize(16777215, 40))
        self.label_debtorName_feedback.setText(u"")
        self.label_debtorName_feedback.setTextFormat(Qt.TextFormat.PlainText)
        self.label_debtorName_feedback.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_debtorName_feedback.setWordWrap(True)
        self.label_debtorName_feedback.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        self.gridLayout.addWidget(self.label_debtorName_feedback, 1, 1, 1, 1)

        self.gridLayout.setColumnStretch(1, 1)
        self.gridLayout.setColumnStretch(3, 1)

        self.verticalLayout_2.addWidget(self.mandatory_data)

        self.additional_data = QWidget(self.debtor_data)
        self.additional_data.setObjectName(u"additional_data")
        sizePolicy2.setHeightForWidth(self.additional_data.sizePolicy().hasHeightForWidth())
        self.additional_data.setSizePolicy(sizePolicy2)
        self.additional_data.setMinimumSize(QSize(0, 150))
        self.additional_data.setMaximumSize(QSize(16777215, 150))
        self.gridLayout_2 = QGridLayout(self.additional_data)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setHorizontalSpacing(6)
        self.gridLayout_2.setVerticalSpacing(8)
        self.gridLayout_2.setContentsMargins(3, 5, 3, 5)
        self.label_phoneNumber = QLabel(self.additional_data)
        self.label_phoneNumber.setObjectName(u"label_phoneNumber")

        self.gridLayout_2.addWidget(self.label_phoneNumber, 0, 0, 1, 1)

        self.lineEdit_phoneNumber = QLineEdit(self.additional_data)
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

        self.gridLayout_2.addWidget(self.lineEdit_phoneNumber, 0, 1, 1, 1)

        self.label_direction = QLabel(self.additional_data)
        self.label_direction.setObjectName(u"label_direction")

        self.gridLayout_2.addWidget(self.label_direction, 2, 0, 1, 1)

        self.lineEdit_direction = QLineEdit(self.additional_data)
        self.lineEdit_direction.setObjectName(u"lineEdit_direction")
#if QT_CONFIG(tooltip)
        self.lineEdit_direction.setToolTip(u"<html><head/><body><p><span style=\" font-size:12pt;\">(Opcional) direcci\u00f3n del propietario.</span></p></body></html>")
#endif // QT_CONFIG(tooltip)
        self.lineEdit_direction.setInputMask(u"")
        self.lineEdit_direction.setText(u"")
        self.lineEdit_direction.setPlaceholderText(u"(Opcional) Ej.: Padre J.M. Criado Alonso 200")
        self.lineEdit_direction.setClearButtonEnabled(True)

        self.gridLayout_2.addWidget(self.lineEdit_direction, 2, 1, 1, 1)

        self.label_postalCode = QLabel(self.additional_data)
        self.label_postalCode.setObjectName(u"label_postalCode")

        self.gridLayout_2.addWidget(self.label_postalCode, 3, 0, 1, 1)

        self.lineEdit_postalCode = QLineEdit(self.additional_data)
        self.lineEdit_postalCode.setObjectName(u"lineEdit_postalCode")
#if QT_CONFIG(tooltip)
        self.lineEdit_postalCode.setToolTip(u"<html><head/><body><p><span style=\" font-size:12pt;\">(Opcional) c\u00f3digo postal del propietario.</span></p><p><span style=\" font-size:12pt; font-weight:600; text-decoration: underline;\">NOTA:</span><span style=\" font-size:12pt;\"> por conveniencia s\u00f3lo admite c\u00f3digos postales de Argentina.</span></p></body></html>")
#endif // QT_CONFIG(tooltip)
        self.lineEdit_postalCode.setInputMask(u"")
        self.lineEdit_postalCode.setText(u"")
        self.lineEdit_postalCode.setPlaceholderText(u"(Opcional) Ej.: 6703")
        self.lineEdit_postalCode.setClearButtonEnabled(True)

        self.gridLayout_2.addWidget(self.lineEdit_postalCode, 3, 1, 1, 1)

        self.label_postalCode_feedback = QLabel(self.additional_data)
        self.label_postalCode_feedback.setObjectName(u"label_postalCode_feedback")
        self.label_postalCode_feedback.setEnabled(True)
        self.label_postalCode_feedback.setMaximumSize(QSize(16777215, 20))
        self.label_postalCode_feedback.setText(u"")
        self.label_postalCode_feedback.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_postalCode_feedback.setWordWrap(False)
        self.label_postalCode_feedback.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        self.gridLayout_2.addWidget(self.label_postalCode_feedback, 4, 0, 1, 2)

        self.label_phoneNumber_feedback = QLabel(self.additional_data)
        self.label_phoneNumber_feedback.setObjectName(u"label_phoneNumber_feedback")
        self.label_phoneNumber_feedback.setEnabled(True)
        self.label_phoneNumber_feedback.setMaximumSize(QSize(16777215, 20))
        self.label_phoneNumber_feedback.setText(u"")
        self.label_phoneNumber_feedback.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_phoneNumber_feedback.setWordWrap(False)
        self.label_phoneNumber_feedback.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        self.gridLayout_2.addWidget(self.label_phoneNumber_feedback, 1, 0, 1, 2)

        self.gridLayout_2.setColumnStretch(0, 1)
        self.gridLayout_2.setColumnStretch(1, 2)

        self.verticalLayout_2.addWidget(self.additional_data)


        self.verticalLayout.addWidget(self.debtor_data)

        self.buttonBox = QDialogButtonBox(debtorDataDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setCenterButtons(True)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(debtorDataDialog)
        self.buttonBox.accepted.connect(debtorDataDialog.accept)
        self.buttonBox.rejected.connect(debtorDataDialog.reject)

        QMetaObject.connectSlotsByName(debtorDataDialog)
    # setupUi

    def retranslateUi(self, debtorDataDialog):
        debtorDataDialog.setWindowTitle(QCoreApplication.translate("debtorDataDialog", u"Dialog", None))
        self.label_phoneNumber.setText(QCoreApplication.translate("debtorDataDialog", u"N\u00fam. de tel\u00e9fono", None))
        self.label_direction.setText(QCoreApplication.translate("debtorDataDialog", u"Direcci\u00f3n", None))
        self.label_postalCode.setText(QCoreApplication.translate("debtorDataDialog", u"C\u00f3digo postal", None))
    # retranslateUi

