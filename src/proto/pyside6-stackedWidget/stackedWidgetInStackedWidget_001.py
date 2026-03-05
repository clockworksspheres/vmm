from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QComboBox, QLineEdit, QStackedWidget, QLabel
)
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # --- Main container ---
        central = QWidget()
        layout = QVBoxLayout(central)
        self.setCentralWidget(central)

        # --- Top-level ComboBox controlling mainStack ---
        self.mainCombo = QComboBox()
        self.mainCombo.addItems(["Main Page A", "Main Page B"])
        layout.addWidget(self.mainCombo)

        # --- Main stacked widget ---
        self.mainStack = QStackedWidget()
        layout.addWidget(self.mainStack)

        # --- Page A (contains another stacked widget) ---
        pageA = QWidget()
        pageA_layout = QVBoxLayout(pageA)

        self.innerCombo = QComboBox()
        self.innerCombo.addItems(["Inner Page 1", "Inner Page 2"])
        pageA_layout.addWidget(self.innerCombo)

        self.innerStack = QStackedWidget()
        pageA_layout.addWidget(self.innerStack)

        # Inner pages
        inner1 = QLabel("This is inner page 1")
        inner2 = QLabel("This is inner page 2")
        self.innerStack.addWidget(inner1)
        self.innerStack.addWidget(inner2)

        # --- Page B ---
        pageB = QLabel("This is Main Page B")

        # Add pages to main stack
        self.mainStack.addWidget(pageA)
        self.mainStack.addWidget(pageB)

        # --- Optional LineEdit controlling something ---
        self.lineEdit = QLineEdit()
        self.lineEdit.setPlaceholderText("Type '1' or '2' to switch inner pages")
        layout.addWidget(self.lineEdit)

        # --- Connections ---
        self.mainCombo.currentIndexChanged.connect(self.mainStack.setCurrentIndex)
        self.innerCombo.currentIndexChanged.connect(self.innerStack.setCurrentIndex)
        self.lineEdit.textChanged.connect(self.handle_text_change)

    def handle_text_change(self, text):
        if text == "1":
            self.innerStack.setCurrentIndex(0)
        elif text == "2":
            self.innerStack.setCurrentIndex(1)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())


