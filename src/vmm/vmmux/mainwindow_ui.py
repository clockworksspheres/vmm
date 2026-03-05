# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.10.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QComboBox, QDialogButtonBox,
    QGridLayout, QLabel, QLayout, QLineEdit,
    QMainWindow, QMenu, QMenuBar, QRadioButton,
    QSizePolicy, QStackedWidget, QStatusBar, QTextEdit,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(489, 308)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.layoutWidget = QWidget(self.centralwidget)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(30, 20, 421, 216))
        self.gridLayout = QGridLayout(self.layoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.hypervisorLabel = QLabel(self.layoutWidget)
        self.hypervisorLabel.setObjectName(u"hypervisorLabel")

        self.gridLayout.addWidget(self.hypervisorLabel, 0, 0, 1, 1)

        self.vmNameLineEdit = QLineEdit(self.layoutWidget)
        self.vmNameLineEdit.setObjectName(u"vmNameLineEdit")

        self.gridLayout.addWidget(self.vmNameLineEdit, 5, 0, 1, 1)

        self.stackedWidget = QStackedWidget(self.layoutWidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.stackedWidget.sizePolicy().hasHeightForWidth())
        self.stackedWidget.setSizePolicy(sizePolicy1)
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.headlessRadioButton = QRadioButton(self.page)
        self.headlessRadioButton.setObjectName(u"headlessRadioButton")
        self.headlessRadioButton.setGeometry(QRect(20, 20, 99, 20))
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.hardRadioButton = QRadioButton(self.page_2)
        self.hardRadioButton.setObjectName(u"hardRadioButton")
        self.hardRadioButton.setGeometry(QRect(20, 20, 99, 20))
        self.stackedWidget.addWidget(self.page_2)
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.textEdit = QTextEdit(self.page_3)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setGeometry(QRect(0, 10, 171, 121))
        sizePolicy1.setHeightForWidth(self.textEdit.sizePolicy().hasHeightForWidth())
        self.textEdit.setSizePolicy(sizePolicy1)
        self.stackedWidget.addWidget(self.page_3)

        self.gridLayout.addWidget(self.stackedWidget, 2, 1, 4, 1)

        self.actionLabel = QLabel(self.layoutWidget)
        self.actionLabel.setObjectName(u"actionLabel")

        self.gridLayout.addWidget(self.actionLabel, 2, 0, 1, 1)

        self.actionComboBox = QComboBox(self.layoutWidget)
        self.actionComboBox.setObjectName(u"actionComboBox")

        self.gridLayout.addWidget(self.actionComboBox, 3, 0, 1, 1)

        self.vmNameLabel = QLabel(self.layoutWidget)
        self.vmNameLabel.setObjectName(u"vmNameLabel")

        self.gridLayout.addWidget(self.vmNameLabel, 4, 0, 1, 1)

        self.buttonBox = QDialogButtonBox(self.layoutWidget)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Apply|QDialogButtonBox.StandardButton.Ok)

        self.gridLayout.addWidget(self.buttonBox, 6, 1, 1, 1)

        self.hypervisorComboBox = QComboBox(self.layoutWidget)
        self.hypervisorComboBox.setObjectName(u"hypervisorComboBox")

        self.gridLayout.addWidget(self.hypervisorComboBox, 1, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 489, 39))
        self.menuvmctl = QMenu(self.menubar)
        self.menuvmctl.setObjectName(u"menuvmctl")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuvmctl.menuAction())

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.hypervisorLabel.setText(QCoreApplication.translate("MainWindow", u"Hypervisor", None))
        self.headlessRadioButton.setText(QCoreApplication.translate("MainWindow", u"Headless", None))
        self.hardRadioButton.setText(QCoreApplication.translate("MainWindow", u"Hard", None))
        self.actionLabel.setText(QCoreApplication.translate("MainWindow", u"Action", None))
        self.vmNameLabel.setText(QCoreApplication.translate("MainWindow", u"virtual machine name", None))
        self.menuvmctl.setTitle(QCoreApplication.translate("MainWindow", u"vmctl", None))
    # retranslateUi

