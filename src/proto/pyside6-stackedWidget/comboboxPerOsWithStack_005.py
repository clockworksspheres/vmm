import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QStackedWidget, QComboBox, QLabel,
    QRadioButton, QTextEdit, QSlider
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

        # --- Page 2: QTextEdit + vertical slider ---
        page2 = QWidget()
        p2_layout = QHBoxLayout(page2)

        self.textbox = QTextEdit()
        self.textbox.setPlainText("This is a QTextEdit.\nScroll using the slider.")
        p2_layout.addWidget(self.textbox)

        self.slider = QSlider(Qt.Vertical)
        self.slider.setRange(0, 100)
        p2_layout.addWidget(self.slider)

        # Connect slider to scroll the text box
        self.slider.valueChanged.connect(self.sync_scroll)

        self.stack.addWidget(page2)

        # Platform-specific combo items
        platform = sys.platform.lower()

        if platform.startswith("darwin"):
            self.combo.addItems(["zero", "one", "two"])
        elif platform.startswith("win"):
            self.combo.addItems(["three", "four", "five"])

        # Connect combo to stack
        self.combo.currentIndexChanged.connect(self.stack.setCurrentIndex)

    def sync_scroll(self, value):
        # Map slider value to QTextEdit vertical scroll
        bar = self.textbox.verticalScrollBar()
        bar.setValue(int(value / 100 * bar.maximum()))


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()

