import sys
from PySide6.QtWidgets import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        central = QWidget()
        layout = QVBoxLayout(central)
        self.setCentralWidget(central)

        # Main stack
        self.mainStack = QStackedWidget()
        layout.addWidget(self.mainStack)

        # Shared inner stack
        self.innerStack = QStackedWidget()
        self.innerStack.addWidget(QLabel("Inner Page 1"))
        self.innerStack.addWidget(QLabel("Inner Page 2"))

        # Platform pages
        self.pageWin = QWidget()
        self.pageMac = QWidget()

        self.pageWinLayout = QVBoxLayout(self.pageWin)
        self.pageMacLayout = QVBoxLayout(self.pageMac)

        self.mainStack.addWidget(self.pageWin)
        self.mainStack.addWidget(self.pageMac)

        # Decide platform
        if sys.platform.lower().startswith("win"):
            self.pageWinLayout.addWidget(self.innerStack)
            self.mainStack.setCurrentWidget(self.pageWin)
        elif sys.platform.lower().startswith("darwin"):
            self.pageMacLayout.addWidget(self.innerStack)
            self.mainStack.setCurrentWidget(self.pageMac)

app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()

