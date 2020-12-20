from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 

class Sig(QMainWindow):
    def __init__(self):
        self.tmp  = 0

    # paintEvent for creating blank canvas 
    def paintEvent(self, event): 
        canvasPainter = QPainter(self) 
        canvasPainter.drawImage(self.rect(), self.image, 
                                      self.image.rect())
        print("Event") 