from Signal_Gen import *
from Tab import *
from External_Windows import *
import qdarkstyle

from PyQt5.QtCore import QDateTime, Qt, QTimer
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QGraphicsScene, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit, 
        QMainWindow, QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
        QVBoxLayout, QWidget)


# importing modules 
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
import sys 

from PyQt5 import QtCore, QtGui, QtWidgets
import os
  

# creating class fo winow 
class Window(QMainWindow): 
    def __init__(self): 
        super().__init__() 
        title = "Pixel Art"
        top = 400
        left = 400
        width = 1200
        height = 900     
        self.setWindowTitle(title)  # window name 
        self.setGeometry(top, left, width, height) # setting geometry
        self.image = QImage(self.size(), QImage.Format_RGB32) # creating canvas 
        self.image.fill(Qt.white)  # setting canvas color to white \
        
        self.setWindowIcon(QIcon('Images/splatter.png'))  # setting icon to brush
  
        
        mainMenu = self.menuBar() # creating menu bar 
        mainMenu.setStyleSheet("""
            QMenuBar {
                spacing: 3px; 
                padding: 3px;
                color: white;
                font-size: 18pt;
                font-family: Courier;
            }
        """)

        # New Tab Method
        fileMenu = mainMenu.addMenu("File") # adding file menu in it 
        newAction = QAction("New", self)
        newAction.setShortcut("Ctrl + N")
        fileMenu.addAction(newAction)
        newAction.triggered.connect( self.newtab )
        # newAction.triggered.connect(self.inter_window)

        # fileMenu.addAction(self.openAction)
        
        # Saving Method
        saveAction = QAction("Save", self) # creating save action 
        saveAction.setShortcut("Ctrl + S") #Saving shortcut
        fileMenu.addAction(saveAction) # adding save action to filemenu
        saveAction.triggered.connect(self.save) # setting triggered method 
  
        editMenu = mainMenu.addMenu("Edit")

        transformMenu = mainMenu.addMenu("Transform")

        viewMenu = mainMenu.addMenu("View")

        self.ToolBar = self.createToolBar()


        self.RightPalleteDock = self.createRightPalleteDock()
        self.BottomPalleteDock = self.createBottomPalleteDock()

        self.TbM = TabManager(self) #TbM is short for "Tab Manager"
        self.setCentralWidget(self.TbM)
        
        self.statusBar().showMessage("Message in statusbar")

        self.signal = Sig() 
        
        self.l_press = False  #Left-click
        self.pointer = QPoint()  #Mouse Position
        

        # calling draw_something method 
        # self.draw_something() 
 

    # creates the tool bar on the left side
    def createToolBar(self):
        self.ToolBar = QToolBar()
        self.ToolBar.setStyleSheet("""
            QToolBar {
                spacing: 5px;
                padding: 5px;
            }

        """)

        self.prev = " "

        # tools = ["brush", "eraser", "selection", "fill", "colorpicker"]
        
        self.point = QAction(QIcon("Images/mouse.png"),"point",self)
        self.point.triggered.connect(lambda: self.TB_callback('point'))
        self.point.setCheckable(True)
        self.ToolBar.addAction(self.point)

        self.brush = QAction(QIcon("Images/brushtool.png"),"brush",self)
        self.brush.triggered.connect(lambda: self.TB_callback('brush'))
        self.brush.setCheckable(True)
        self.ToolBar.addAction(self.brush)

        self.eraser = QAction(QIcon("Images/eraser.png"),"eraser",self)
        self.eraser.triggered.connect(lambda: self.TB_callback('eraser'))
        self.eraser.setCheckable(True)
        self.ToolBar.addAction(self.eraser)

        self.selection = QAction(QIcon("Images/selection.png"),"selection",self)
        self.selection.triggered.connect(lambda: self.TB_callback('selection'))
        self.selection.setCheckable(True)
        self.ToolBar.addAction(self.selection)

        self.fill = QAction(QIcon("Images/fill.png"),"fill",self)
        self.fill.triggered.connect(lambda: self.TB_callback('fill'))
        self.fill.setCheckable(True)
        self.ToolBar.addAction(self.fill)

        self.zoomin = QAction(QIcon("Images/zoomin.png"),"zoom in",self)
        self.zoomin.triggered.connect(lambda: self.TB_callback('zoomin'))
        self.zoomin.setCheckable(True)
        self.ToolBar.addAction(self.zoomin)

        self.zoomout = QAction(QIcon("Images/zoomout.png"),"zoom out",self)
        self.zoomout.setCheckable(True)
        self.zoomout.triggered.connect(lambda: self.TB_callback('zoomout'))
        self.ToolBar.addAction(self.zoomout)
        

        self.ToolBar.setMovable(False)
        self.ToolBar.setOrientation(Qt.Vertical)
        self.ToolBar.setIconSize(QSize(30,30))
        self.tb = self.addToolBar(Qt.LeftToolBarArea, self.ToolBar)

        return self.tb
    
    def TB_callback(self, a):
        if self.prev == " ":
            pass
        else:
            if self.prev == "point":
                self.point.toggle()
            if self.prev == "brush":
                self.brush.toggle()
            elif self.prev == "eraser":
                self.eraser.toggle()
            elif self.prev == "selection":
                self.selection.toggle()
            elif self.prev == "fill":
                self.fill.toggle()
            elif self.prev == "zoomin":
                self.zoomin.toggle()
            elif self.prev == "zoomout":
                self.zoomout.toggle()
        self.prev = a
        
        # if(self.zoomout.isChecked() == True):
    #         if (self.zoomin.isChecked() == True):
    #             self.zoomout.trigger()
    #             print("Trigger")

    def createRightPalleteDock(self):
        self.PDock = QDockWidget("Pallete Chooser", self)
        self.PDock.setStyleSheet("""
            QDockWidget {
                color: white;
                font-size: 12pt;
                font-family: Courier;
            }
            

        """)
        self.PDock.setAllowedAreas(Qt.RightDockWidgetArea)

        self.listWidget = QListWidget()
        self.PDock.setWidget(self.listWidget)
        # self.PDock.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)

      
        self.PDock.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.addDockWidget(Qt.RightDockWidgetArea, self.PDock)

    def createBottomPalleteDock(self):
        self.BoPDock = QDockWidget("Holder", self)
        self.BoPDock.setAllowedAreas(Qt.BottomDockWidgetArea)
        self.BolistWidget = QListWidget()
        self.BoPDock.setWidget(self.BolistWidget)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.BoPDock)

    # paintEvent for creating blank canvas 
    # def paintEvent(self, event): 
    #     canvasPainter = QPainter(self) 
    #     canvasPainter.drawImage(self.rect(), self.image, 
    #                                   self.image.rect())
    #     print("Event") 
     
          
    # this method will draw a line 
    def draw_something(self):   
        painter = QPainter(self.image)   
        painter.setPen(QPen(Qt.black, 5, Qt.SolidLine,  
                            Qt.RoundCap, Qt.RoundJoin)) 
        painter.drawLine(100, 100, 300, 300)  # drawing a line 
        self.update()  # updating it to canvas 
      
    # save method 
    def save(self): 
        # selecting file path 
        filePath, _ = QFileDialog.getSaveFileName(self, "Save Image", "", 
                         "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ") 
        # if file path is blank return back 
        if filePath == "": 
            return
        # saving canvas at desired path 
        self.image.save(filePath) 
    
    def inter_window(self):
        self.w = NewFileWindow()
        self.w.show()

    def newtab(self):
        self.TbM.tablist.append(self.TbM.addTab(self.TbM.tablist.index))


    # mouse event handling methods
    # def mousePressEvent(self, event):
        
    #     if event.buttons() == Qt.LeftButton:
    #         self.l_press = True
    #         print("HerePressed")
    #     if(self.zoomout.isChecked() == True):
    #         if (self.zoomin.isChecked() == True):
    #             self.zoomout.trigger()
    #             print("Trigger")
            
        

# main method 
if __name__ == "__main__": 
    app = QApplication(sys.argv) 
    app.setStyle('Fusion')
    dark_stylesheet = qdarkstyle.load_stylesheet()
    app.setStyleSheet(dark_stylesheet)
   
    window = Window() 
    window.show() 
      
    # looping for window 
    sys.exit(app.exec()) 