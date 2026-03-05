import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QStackedWidget, QComboBox, QLabel
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        central = QWidget()
        layout = QVBoxLayout(central)
        self.setCentralWidget(central)

        # Combo box OUTSIDE the main stack
        self.combo = QComboBox()
        layout.addWidget(self.combo)

        # Main stack (platform pages)
        self.mainStack = QStackedWidget()
        layout.addWidget(self.mainStack)

        # Shared inner stack
        self.innerStack = QStackedWidget()
        self.innerStack.addWidget(QLabel("Inner Page 1"))
        self.innerStack.addWidget(QLabel("Inner Page 2"))
        self.innerStack.addWidget(QLabel("Inner Page 3"))

        # Platform pages
        self.pageWin = QWidget()
        self.pageMac = QWidget()
        self.pageWinLayout = QVBoxLayout(self.pageWin)
        self.pageMacLayout = QVBoxLayout(self.pageMac)

        self.mainStack.addWidget(self.pageWin)
        self.mainStack.addWidget(self.pageMac)

        # Platform-specific combo items and placement of inner stack
        platform = sys.platform.lower()

        if platform.startswith("darwin"):
            self.combo.addItems(["zero", "one", "two"])
            self.pageMacLayout.addWidget(self.innerStack)
            self.mainStack.setCurrentWidget(self.pageMac)

        elif platform.startswith("win"):
            self.combo.addItems(["three", "four", "five"])
            self.pageWinLayout.addWidget(self.innerStack)
            self.mainStack.setCurrentWidget(self.pageWin)

        # Connect combo to inner stack
        self.combo.currentIndexChanged.connect(self.innerStack.setCurrentIndex)


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()

