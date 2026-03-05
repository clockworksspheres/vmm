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

        # Combo box OUTSIDE the stack
        self.combo = QComboBox()
        layout.addWidget(self.combo)

        # One stack controlled by the combo
        self.stack = QStackedWidget()
        layout.addWidget(self.stack)

        # Stack pages
        self.stack.addWidget(QLabel("Page 0"))
        self.stack.addWidget(QLabel("Page 1"))
        self.stack.addWidget(QLabel("Page 2"))

        # Platform-specific combo items
        platform = sys.platform.lower()

        if platform.startswith("darwin"):
            self.combo.addItems(["zero", "one", "two"])
        elif platform.startswith("win"):
            self.combo.addItems(["three", "four", "five"])

        # Connect combo to handler
        self.combo.currentIndexChanged.connect(self.handle_combo)

    def handle_combo(self, index):
        # Example mapping:
        # - first two combo items → page 2
        # - last combo item → page 1
        if index in (0, 1):
            self.stack.setCurrentIndex(2)
        elif index == 2:
            self.stack.setCurrentIndex(1)


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()

