from PySide6.QtWidgets import (
    QWidget, QGridLayout, QComboBox, 
    QLabel, QPushButton
)
import sys


class PageA(QWidget):
    def __init__(self):
        super().__init__()
        layout = QGridLayout(self)
        layout.addWidget(QLabel("This is Page A"), 0, 0)
        layout.addWidget(QPushButton("Action A"), 1, 0)


