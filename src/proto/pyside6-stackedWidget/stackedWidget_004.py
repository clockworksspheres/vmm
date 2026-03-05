from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QComboBox, QLabel, QPushButton, QStackedWidget
)
import sys

class PageA(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("This is Page A"))
        layout.addWidget(QPushButton("Action A"))

class PageB(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("This is Page B"))
        layout.addWidget(QPushButton("Action B"))

class PageC(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("This is Page C"))
        layout.addWidget(QPushButton("Action C"))

class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create a central widget for the QMainWindow
        central = QWidget()
        self.setCentralWidget(central)

        self.layout = QVBoxLayout(central)

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

        self.layout.addWidget(self.combo)
        self.layout.addWidget(self.back_btn)
        self.layout.addWidget(self.stack)

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

