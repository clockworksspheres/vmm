from PySide6.QtWidgets import (
    QWidget, QGridLayout, QComboBox, 
    QLabel, QPushButton
)
import sys


class PageB(QWidget):
    def __init__(self):
        super().__init__()
        layout = QGridLayout(self)
        layout.addWidget(QLabel("This is Page B"), 0, 0)
        layout.addWidget(QPushButton("Action B"), 1, 0)


