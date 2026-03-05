from PySide6.QtWidgets import (
    QWidget, QGridLayout, QComboBox, 
    QLabel, QPushButton
)
import sys


class PageC(QWidget):
    def __init__(self):
        super().__init__()
        layout = QGridLayout(self)
        layout.addWidget(QLabel("This is Page C"), 0, 0)
        layout.addWidget(QPushButton("Action C"), 1, 0)


