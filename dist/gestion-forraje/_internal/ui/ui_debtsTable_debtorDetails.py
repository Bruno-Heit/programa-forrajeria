# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'debtsTable_debtorDetails.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QPushButton,
    QSizePolicy, QWidget)

class Ui_debtorDetails(object):
    def setupUi(self, debtorDetails):
        if not debtorDetails.objectName():
            debtorDetails.setObjectName(u"debtorDetails")
        debtorDetails.resize(150, 42)
        debtorDetails.setMinimumSize(QSize(150, 25))
        self.horizontalLayout = QHBoxLayout(debtorDetails)
        self.horizontalLayout.setSpacing(4)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(2, 0, 2, 0)
        self.label_full_name = QLabel(debtorDetails)
        self.label_full_name.setObjectName(u"label_full_name")
        self.label_full_name.setMinimumSize(QSize(100, 24))
        self.label_full_name.setAlignment(Qt.AlignCenter)
        self.label_full_name.setWordWrap(True)
        self.label_full_name.setTextInteractionFlags(Qt.TextEditable|Qt.TextSelectableByMouse)

        self.horizontalLayout.addWidget(self.label_full_name)

        self.btn_expand_info = QPushButton(debtorDetails)
        self.btn_expand_info.setObjectName(u"btn_expand_info")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_expand_info.sizePolicy().hasHeightForWidth())
        self.btn_expand_info.setSizePolicy(sizePolicy)
        self.btn_expand_info.setMinimumSize(QSize(24, 24))
        self.btn_expand_info.setMaximumSize(QSize(24, 24))
        self.btn_expand_info.setText(u"")
#if QT_CONFIG(shortcut)
        self.btn_expand_info.setShortcut(u"")
#endif // QT_CONFIG(shortcut)

        self.horizontalLayout.addWidget(self.btn_expand_info)


        self.retranslateUi(debtorDetails)

        QMetaObject.connectSlotsByName(debtorDetails)
    # setupUi

    def retranslateUi(self, debtorDetails):
        debtorDetails.setWindowTitle(QCoreApplication.translate("debtorDetails", u"Form", None))
        self.label_full_name.setText(QCoreApplication.translate("debtorDetails", u"nombre completo", None))
    # retranslateUi

