
# importing modules 
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
import sys 


class NewFileWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("New File Setup")
        layout.addWidget(self.label)
        self.setLayout(layout)