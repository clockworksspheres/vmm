from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QComboBox, QLabel, QPushButton, QStackedWidget
)
import sys

class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)

        # Combo box controls page selection
        self.combo = QComboBox()
        self.combo.addItems(["Widget A", "Widget B", "Widget C"])
        self.combo.currentIndexChanged.connect(self.on_combo_change)

        # Back button
        self.back_btn = QPushButton("Back")
        self.back_btn.clicked.connect(self.go_back)
        self.back_btn.setEnabled(False)

        # Stacked widget holds all pages
        self.stack = QStackedWidget()
        self.stack.addWidget(QLabel("This is Widget A"))
        self.stack.addWidget(QLabel("This is Widget B"))
        self.stack.addWidget(QLabel("This is Widget C"))

        self.layout.addWidget(self.combo)
        self.layout.addWidget(self.back_btn)
        self.layout.addWidget(self.stack)

        # History stack (stores page indices)
        self.history = []
        self.ignore_combo = False

        # Start on page 0
        self.set_page(0)

    def set_page(self, index):
        """Switch page without creating loops."""
        self.stack.setCurrentIndex(index)

        self.ignore_combo = True
        self.combo.setCurrentIndex(index)
        self.ignore_combo = False

    def on_combo_change(self, index):
        """User selected a new page from the combo box."""
        if self.ignore_combo:
            return

        current = self.stack.currentIndex()

        # Push current page to history before switching
        if current != index:
            self.history.append(current)

        self.set_page(index)
        self.back_btn.setEnabled(len(self.history) > 0)

    def go_back(self):
        """Go back one page in history."""
        if not self.history:
            return

        previous = self.history.pop()
        self.set_page(previous)
        self.back_btn.setEnabled(len(self.history) > 0)


app = QApplication(sys.argv)
w = Window()
w.show()
app.exec()

