from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QGridLayout,
    QComboBox, QLabel, QPushButton, QStackedWidget
)
import sys

class PageA(QWidget):
    def __init__(self):
        super().__init__()
        layout = QGridLayout(self)
        layout.addWidget(QLabel("This is Page A"), 0, 0)
        layout.addWidget(QPushButton("Action A"), 1, 0)

class PageB(QWidget):
    def __init__(self):
        super().__init__()
        layout = QGridLayout(self)
        layout.addWidget(QLabel("This is Page B"), 0, 0)
        layout.addWidget(QPushButton("Action B"), 1, 0)

class PageC(QWidget):
    def __init__(self):
        super().__init__()
        layout = QGridLayout(self)
        layout.addWidget(QLabel("This is Page C"), 0, 0)
        layout.addWidget(QPushButton("Action C"), 1, 0)

class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        central = QWidget()
        self.setCentralWidget(central)

        self.layout = QGridLayout(central)

        self.combo = QComboBox()
        self.combo.addItems(["Page A", "Page B", "Page C"])
        self.combo.currentIndexChanged.connect(self.on_combo_change)

        self.back_btn = QPushButton("Back")
        self.back_btn.clicked.connect(self.go_back)
        self.back_btn.setEnabled(False)

        self.stack = QStackedWidget()
        self.stack.addWidget(PageA())
        self.stack.addWidget(PageB())
        self.stack.addWidget(PageC())

        # Grid positions:
        # Row 0: combo + back button
        # Row 1: stacked widget spanning full width
        self.layout.addWidget(self.combo, 0, 0)
        self.layout.addWidget(self.back_btn, 0, 1)
        self.layout.addWidget(self.stack, 1, 0, 1, 2)

        self.history = []
        self.ignore_combo = False

        self.set_page(0)

    def set_page(self, index):
        self.stack.setCurrentIndex(index)
        self.ignore_combo = True
        self.combo.setCurrentIndex(index)
        self.ignore_combo = False

    def on_combo_change(self, index):
        if self.ignore_combo:
            return

        current = self.stack.currentIndex()
        if current != index:
            self.history.append(current)

        self.set_page(index)
        self.back_btn.setEnabled(len(self.history) > 0)

    def go_back(self):
        if not self.history:
            return

        previous = self.history.pop()
        self.set_page(previous)
        self.back_btn.setEnabled(len(self.history) > 0)


app = QApplication(sys.argv)
w = Window()
w.show()
app.exec()

