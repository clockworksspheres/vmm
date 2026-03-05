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
    QGridLayout, QLabel, QLineEdit, QMainWindow,
    QMenu, QMenuBar, QRadioButton, QScrollBar,
    QSizePolicy, QStackedWidget, QStatusBar, QTextEdit,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(564, 478)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.layoutWidget = QWidget(self.centralwidget)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(40, 30, 471, 341))
        self.gridLayout = QGridLayout(self.layoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.buttonBox = QDialogButtonBox(self.layoutWidget)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Apply|QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.gridLayout.addWidget(self.buttonBox, 4, 2, 1, 1)

        self.label_3 = QLabel(self.layoutWidget)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 0, 2, 1, 1)

        self.stackedWidget_2 = QStackedWidget(self.layoutWidget)
        self.stackedWidget_2.setObjectName(u"stackedWidget_2")
        self.page_4 = QWidget()
        self.page_4.setObjectName(u"page_4")
        self.comboBox_2 = QComboBox(self.page_4)
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.setObjectName(u"comboBox_2")
        self.comboBox_2.setGeometry(QRect(10, 0, 181, 21))
        self.stackedWidget_2.addWidget(self.page_4)
        self.page_6 = QWidget()
        self.page_6.setObjectName(u"page_6")
        self.comboBox_3 = QComboBox(self.page_6)
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.setObjectName(u"comboBox_3")
        self.comboBox_3.setGeometry(QRect(10, 0, 171, 32))
        self.stackedWidget = QStackedWidget(self.page_6)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setGeometry(QRect(-10, 30, 467, 181))
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.radioButton = QRadioButton(self.page)
        self.radioButton.setObjectName(u"radioButton")
        self.radioButton.setGeometry(QRect(20, 30, 99, 20))
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.radioButton_2 = QRadioButton(self.page_2)
        self.radioButton_2.setObjectName(u"radioButton_2")
        self.radioButton_2.setGeometry(QRect(20, 30, 99, 20))
        self.stackedWidget.addWidget(self.page_2)
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.textEdit = QTextEdit(self.page_3)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setGeometry(QRect(10, 10, 351, 161))
        self.verticalScrollBar = QScrollBar(self.page_3)
        self.verticalScrollBar.setObjectName(u"verticalScrollBar")
        self.verticalScrollBar.setGeometry(QRect(340, 20, 16, 141))
        self.verticalScrollBar.setOrientation(Qt.Orientation.Vertical)
        self.stackedWidget.addWidget(self.page_3)
        self.stackedWidget_2.addWidget(self.page_6)

        self.gridLayout.addWidget(self.stackedWidget_2, 3, 0, 1, 3)

        self.lineEdit_2 = QLineEdit(self.layoutWidget)
        self.lineEdit_2.setObjectName(u"lineEdit_2")

        self.gridLayout.addWidget(self.lineEdit_2, 1, 2, 1, 1)

        self.label_2 = QLabel(self.layoutWidget)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 2)

        self.comboBox = QComboBox(self.layoutWidget)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")

        self.gridLayout.addWidget(self.comboBox, 1, 0, 1, 2)

        self.label = QLabel(self.layoutWidget)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 564, 39))
        self.menuvmctl = QMenu(self.menubar)
        self.menuvmctl.setObjectName(u"menuvmctl")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuvmctl.menuAction())

        self.retranslateUi(MainWindow)

        self.stackedWidget_2.setCurrentIndex(1)
        self.stackedWidget.setCurrentIndex(2)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Virtual Machine", None))
        self.comboBox_2.setItemText(0, QCoreApplication.translate("MainWindow", u"Vmware Fusion", None))
        self.comboBox_2.setItemText(1, QCoreApplication.translate("MainWindow", u"UTM", None))
        self.comboBox_2.setItemText(2, QCoreApplication.translate("MainWindow", u"Virtualbox", None))

        self.comboBox_3.setItemText(0, QCoreApplication.translate("MainWindow", u"VMware Workstation", None))
        self.comboBox_3.setItemText(1, QCoreApplication.translate("MainWindow", u"HyperV", None))
        self.comboBox_3.setItemText(2, QCoreApplication.translate("MainWindow", u"VirtualBox", None))

        self.radioButton.setText(QCoreApplication.translate("MainWindow", u"Headless", None))
        self.radioButton_2.setText(QCoreApplication.translate("MainWindow", u"Hard", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Hypervisor", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"Start", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"Stop", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"Reset", None))
        self.comboBox.setItemText(3, QCoreApplication.translate("MainWindow", u"pause", None))
        self.comboBox.setItemText(4, QCoreApplication.translate("MainWindow", u"unpause", None))
        self.comboBox.setItemText(5, QCoreApplication.translate("MainWindow", u"IP", None))
        self.comboBox.setItemText(6, QCoreApplication.translate("MainWindow", u"Status", None))

        self.label.setText(QCoreApplication.translate("MainWindow", u"Action", None))
        self.menuvmctl.setTitle(QCoreApplication.translate("MainWindow", u"vmctl", None))
    # retranslateUi

