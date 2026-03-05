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

        # Combo outside the main stack
        self.combo = QComboBox()
        layout.addWidget(self.combo)

        # Main stack (platform pages)
        self.mainStack = QStackedWidget()
        layout.addWidget(self.mainStack)

        # Shared inner stack
        self.innerStack = QStackedWidget()
        self.innerStack.addWidget(QLabel("Inner Page 1"))  # index 0
        self.innerStack.addWidget(QLabel("Inner Page 2"))  # index 1
        self.innerStack.addWidget(QLabel("Inner Page 3"))  # index 2

        # Platform pages
        self.pageWin = QWidget()
        self.pageMac = QWidget()
        self.pageWinLayout = QVBoxLayout(self.pageWin)
        self.pageMacLayout = QVBoxLayout(self.pageMac)

        self.mainStack.addWidget(self.pageWin)
        self.mainStack.addWidget(self.pageMac)

        # Platform-specific combo items
        platform = sys.platform.lower()

        if platform.startswith("darwin"):
            self.combo.addItems(["zero", "one", "two"])
            self.pageMacLayout.addWidget(self.innerStack)
            self.mainStack.setCurrentWidget(self.pageMac)

        elif platform.startswith("win"):
            self.combo.addItems(["three", "four", "five"])
            self.pageWinLayout.addWidget(self.innerStack)
            self.mainStack.setCurrentWidget(self.pageWin)

        # Connect combo to custom handler
        self.combo.currentIndexChanged.connect(self.handle_combo)

    def handle_combo(self, index):
        # Map two combo items to the same inner page
        if index in (0, 1):          # first two items → page 2
            self.innerStack.setCurrentIndex(2)
        elif index == 2:             # last item → page 1
            self.innerStack.setCurrentIndex(1)


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()

