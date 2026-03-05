import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QStackedWidget, QComboBox, QLabel, QRadioButton,
    QLineEdit, QSlider
)
from PySide6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        central = QWidget()
        layout = QVBoxLayout(central)
        self.setCentralWidget(central)

        # Combo box outside the stack
        self.combo = QComboBox()
        layout.addWidget(self.combo)

        # One stack controlled by the combo
        self.stack = QStackedWidget()
        layout.addWidget(self.stack)

        # --- Page 0: radio buttons ---
        page0 = QWidget()
        p0_layout = QVBoxLayout(page0)
        p0_layout.addWidget(QRadioButton("Option A"))
        p0_layout.addWidget(QRadioButton("Option B"))
        self.stack.addWidget(page0)

        # --- Page 1: radio buttons ---
        page1 = QWidget()
        p1_layout = QVBoxLayout(page1)
        p1_layout.addWidget(QRadioButton("Choice 1"))
        p1_layout.addWidget(QRadioButton("Choice 2"))
        self.stack.addWidget(page1)

        # --- Page 2: textbox + slider ---
        page2 = QWidget()
        p2_layout = QVBoxLayout(page2)
        p2_layout.addWidget(QLineEdit("Type here"))
        slider = QSlider(Qt.Horizontal)
        slider.setRange(0, 100)
        p2_layout.addWidget(slider)
        self.stack.addWidget(page2)

        # Platform‑specific combo items
        platform = sys.platform.lower()

        if platform.startswith("darwin"):
            self.combo.addItems(["zero", "one", "two"])
        elif platform.startswith("win"):
            self.combo.addItems(["three", "four", "five"])

        # Connect combo to handler
        self.combo.currentIndexChanged.connect(self.handle_combo)

    def handle_combo(self, index):
        # Direct mapping: combo index → stack page
        # Page 0 = radio buttons
        # Page 1 = radio buttons
        # Page 2 = textbox + slider
        self.stack.setCurrentIndex(index)


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()

