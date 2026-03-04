from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QComboBox, QLabel, QPushButton
)
import sys

class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)

        self.combo = QComboBox()
        self.combo.addItems(["Select...", "Widget A", "Widget B", "Widget C"])
        self.combo.currentIndexChanged.connect(self.on_select)

        self.back_btn = QPushButton("Back")
        self.back_btn.clicked.connect(self.go_back)
        self.back_btn.setEnabled(False)

        self.layout.addWidget(self.combo)
        self.layout.addWidget(self.back_btn)

        self.widget_stack = []
        self.ignore_combo_change = False

    def on_select(self, index):
        if self.ignore_combo_change:
            return

        if index == 0:
            return

        if self.widget_stack:
            self.widget_stack[-1]["widget"].hide()

        if index == 1:
            widget = QLabel("This is Widget A")
        elif index == 2:
            widget = QLabel("This is Widget B")
        elif index == 3:
            widget = QLabel("This is Widget C")

        self.layout.addWidget(widget)
        widget.show()

        self.widget_stack.append({"widget": widget, "index": index})
        self.back_btn.setEnabled(len(self.widget_stack) > 1)

    def go_back(self):
        if len(self.widget_stack) <= 1:
            return

        current = self.widget_stack.pop()
        current["widget"].hide()
        current["widget"].deleteLater()

        previous = self.widget_stack[-1]
        previous["widget"].show()

        self.ignore_combo_change = True
        self.combo.setCurrentIndex(previous["index"])
        self.ignore_combo_change = False

        self.back_btn.setEnabled(len(self.widget_stack) > 1)


app = QApplication(sys.argv)
w = Window()
w.show()
app.exec()

