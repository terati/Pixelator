import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QGridLayout, QWidget
from PyQt5.QtGui import QPixmap

# importing libraries 
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
import sys 
  
# window class 
class TClass():
    def __init__(self):
        self.num = 5
        print(self.num)
        self.cl = INclass(self)
        # self.incr()
        self.cl.read()
        print(self.num)
    def incr(self):
        self.num = self.num + 1

class INclass():
    def __init__(self, TCself):
        self.TCself = TCself
        self.TCself.num = 8
        # print(self.TCself.num)
    def read(self):
        print(self.TCself.num)


TClass()
