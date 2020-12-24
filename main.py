from Signal_Gen import *
from Tab import *
from External_Windows import *
import config
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
  
Red = 255
Green = 255
Blue = 255
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
        self.PDock = QDockWidget("", self)
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
        self.PDock.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.addDockWidget(Qt.RightDockWidgetArea, self.PDock)


        self.PDtabs = QTabWidget()
        self.tab1 = QWidget()
        self.PDtabs.addTab(self.tab1,"Pallete")
        self.tab2 = QWidget()
        self.PDtabs.addTab(self.tab2,"TMP")
        self.PDock.setLayout(QVBoxLayout())
        self.PDock.layout().addWidget(self.PDtabs)
        
        self.tab1.layout = QVBoxLayout()
        self.tab1.setLayout(self.tab1.layout)
        self.tab1.layout.setAlignment(Qt.AlignTop)

        # self.p_scene = PGraphicsSceneEdit()


        # self.p_label = QLabel()
        # p_canvas = QPixmap(250,200)
        # self.p_label.setPixmap(p_canvas)
        # p = QPainter(self.p_label.pixmap())
        # # p = QPainter(self)
        # self.radius = 100.
        # for i in range(self.width()):
        #     for j in range(self.height()):
        #         color = QColor(255, 255, 255, 255)
        #         h = (np.arctan2(i-self.radius, j-self.radius)+np.pi)/(2.*np.pi)
        #         s = np.sqrt(np.power(i-self.radius, 2)+np.power(j-self.radius, 2))/self.radius
        #         v = 1.0
        #         if s < 1.0 and s > 0.5:
        #             var = round(1**(s))
        #             color.setHsvF(h, s, v, 1)
        #         else:
        #             color.setHsv(210, 44.4, 17.6, 0)
        #         p.setPen(color)
        #         p.drawPoint(i, j)
        # p.setBrush(QColor(255, 255, 255, 255))
        # p.drawRect(70, 70, 60, 60)
        # p.drawRect(190, 0, 30, 30)
        # self.p_scene.addWidget(self.p_label)

        # self.p_view = QGraphicsView(self)
        # self.p_view.setScene(self.p_scene)
        # self.tab1.layout.addWidget(self.p_view)
        
        self.cc = ColorCircle()
        self.tab1.layout.addWidget(self.cc)

        self.slide = QSlider(Qt.Horizontal)
        self.slide.setValue(50)
        self.slide.valueChanged.connect(self.slider_callback)
        
        self.slide.setStyleSheet("""
            QSlider {
                height: 40px;
                min-width: 100px;
                max-width: 220px;
            }
            QSlider::groove:horizontal{
                height: 5px;
                background: qlineargradient(x1:0, x2:1, stop:0 white, stop:1 black);
            }
            QSlider::sub-page:horizontal {
                background: transparent
            }
            QSlider::handle:horizontal {
                background: blue;
                width: 10px;
                border: 10px;
                margin-top: -5px;
                margin-bottom: -5px;
                border-radius: 10px;
            }
        """)
        self.tab1.layout.addWidget(self.slide)
        
        self.slide2 = QSlider(Qt.Horizontal)
        self.tab1.layout.addWidget(self.slide2)

    def slider_callback(self, val):
        config.slider1 = val # ranges from 0-100
        if config.slider1 > 50:    
            config.factor = (config.slider1 - 50)*40 + 100
        if config.slider1 < 50:
            config.factor = (50 - config.slider1)*40 + 100

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
            
        
import numpy as np
class ColorCircle(QWidget):

    def __init__(self):
        super().__init__()
        self.radius = 100.
        self.setFixedSize(250, 250)
        self.tmp = QColor(255, 255, 255, 255)
        self.flag = 0 
        self.p = QPainter(self)
        self.pixmap = QPixmap('palette.png')
        self.r = 255
        self.g = 255
        self.b = 255
        self.old_r = 255
        self.old_g = 255
        self.old_b = 255
        self.m_r = 255
        self.m_g = 255
        self.m_b = 255
        self.m_x = 255
        self.m_y = 255

        self.r1 = 255
        self.g1 = 0
        self.b1 = 0
        self.r2 = 0
        self.g2 = 255
        self.b2 = 0
        self.r3 = 0
        self.g3 = 0
        self.b3 = 255

        self.tmpp_r = 0
        self.tmpp_g = 0
        self.tmpp_b = 0
    def paintEvent(self, ev):
        super().paintEvent(ev)

        # self.p_label = QLabel()
        # p_canvas = QPixmap(250,200)
        # self.p_label.setPixmap(p_canvas)

        # p = QPainter(self.p_label.pixmap())
        self.p.begin(self)
        self.p.drawPixmap(QPoint(0,0), self.pixmap, QRect(0,0,250,200))

        # if self.flag == 0:
        #     for i in range(self.width()):
        #         for j in range(self.height()):
        #             color = QColor(255, 255, 255, 255)
        #             h = (np.arctan2(i-self.radius, j-self.radius)+np.pi)/(2.*np.pi)
        #             s = np.sqrt(np.power(i-self.radius, 2)+np.power(j-self.radius, 2))/self.radius
        #             v = 1.0
        #             if s < 1.0 and s > 0.5:
        #                 var = round(1**(s))
        #                 color.setHsvF(h, s, v, 1)
        #             else:
        #                 color.setHsv(210, 44.4, 17.6, 0)
        #             self.p.setPen(color)
        #             self.p.drawPoint(i, j)
        #     # self.p.save()
        #     self.flag = 1
            
      
      
        

        self.tp = QColor(self.r, self.g, self.b, 255)
        if config.slider1 > 50:
            self.tp = self.tp.darker(config.factor)
        if config.slider1 < 50:
            self.tp = self.tp.lighter(config.factor)
        self.p.setBrush(self.tp)
        self.p.drawRect(70, 70, 60, 60) #Center square
        self.tp = QColor(self.old_r, self.old_g, self.old_b, 255)
        self.p.setBrush(self.tp)
        self.p.drawEllipse(190, 0, 30, 30) #Right corner square


        self.tp = QColor(self.r1, self.g1, self.b1, 255)
        self.p.setBrush(self.tp)
        self.p.drawEllipse(5, 180, 30, 30) #Swatch1
        self.tp = QColor(self.r2, self.g2, self.b2, 255)
        self.p.setBrush(self.tp)
        self.p.drawEllipse(42, 205, 30, 30) #Swatch2
        self.tp = QColor(self.r3, self.g3, self.b3, 255)
        self.p.setBrush(self.tp)
        self.p.drawEllipse(90, 210, 30, 30) #Swatch3


        self.tp = QColor(255, 255, 255, 255)
        self.p.setBrush(self.tp)
        self.p.drawEllipse(self.m_x-23, self.m_y-2, 25, 25)
        self.tp = QColor(self.m_r, self.m_g, self.m_b, 255)
        self.p.setBrush(self.tp)
        self.p.drawEllipse(self.m_x-20, self.m_y, 20, 20)
        self.p.end()
        
        # p.setBrush(QColor(255, 255, 255, 255))
    def mousePressEvent(self, event):
        self.pr_x = event.x()
        self.pr_y = event.y()
        if ( (self.pr_x - 190 - 15)**2 + (self.pr_y - 15)**2 <= 15**2 ): #Top-right
            # print("signal")
            self.tmpp_r = self.r
            self.tmpp_g = self.g
            self.tmpp_b = self.b
            self.r = self.old_r
            self.g = self.old_g
            self.b = self.old_b
            self.old_r = self.tmpp_r
            self.old_g = self.tmpp_g
            self.old_b = self.tmpp_b
        if event.buttons() == Qt.LeftButton and ( (self.pr_x - 5 - 15)**2 + (self.pr_y - 180 - 15)**2 <= 15**2 ): #Swatch 1
            self.r1 = self.r
            self.g1 = self.g
            self.b1 = self.b
        if event.buttons() == Qt.RightButton and ( (self.pr_x - 5 - 15)**2 + (self.pr_y - 180 - 15)**2 <= 15**2 ): 
            self.r = self.r1 
            self.g = self.g1
            self.b = self.b1
        if event.buttons() == Qt.LeftButton and ( (self.pr_x - 42 - 15)**2 + (self.pr_y - 205 - 15)**2 <= 15**2 ): #Swatch 2
            self.r2 = self.r
            self.g2 = self.g
            self.b2 = self.b
        if event.buttons() == Qt.RightButton and ( (self.pr_x - 42 - 15)**2 + (self.pr_y - 205 - 15)**2 <= 15**2 ):
            self.r = self.r2
            self.g = self.g2
            self.b = self.b2
        if event.buttons() == Qt.LeftButton and ( (self.pr_x - 90 - 15)**2 + (self.pr_y - 210 - 15)**2 <= 15**2 ): #Swatch 3
            self.r3 = self.r
            self.g3 = self.g
            self.b3 = self.b
        if event.buttons() == Qt.RightButton and ( (self.pr_x - 90 - 15)**2 + (self.pr_y - 210 - 15)**2 <= 15**2 ): 
            self.r = self.r3 
            self.g = self.g3
            self.b = self.b3
        
        config.red = self.r
        config.green = self.g
        config.blue = self.b
        self.update()
        
    
    def mouseReleaseEvent(self, event):
        self.setCursor(Qt.ArrowCursor)
        self.p_x = event.x()
        self.p_y = event.y()
        self.old_r = self.r
        self.old_g = self.g
        self.old_b = self.b
        p_h = (np.arctan2(self.p_x-self.radius, self.p_y-self.radius)+np.pi)/(2.*np.pi)
        p_s = np.sqrt(np.power(self.p_x-self.radius, 2)+np.power(self.p_y-self.radius, 2))/self.radius
        p_v = 1.0
        self.tmp = QColor(255, 255, 255, 255)
        if p_s < 1.0 and p_s > 0.5:
            var = round(1**(p_s))
            self.tmp.setHsvF(p_h, p_s, p_v, 1)
            self.tmp = self.tmp.getRgb()
            self.r = self.tmp[0]
            self.g = self.tmp[1]
            self.b = self.tmp[2]
        config.red = self.r
        config.green = self.g
        config.blue = self.b
        self.update()
        
    def mouseMoveEvent(self, event):
        self.setCursor(Qt.BlankCursor)
        self.old_mx = self.m_x
        self.old_my = self.m_y
        self.m_x = event.x()
        self.m_y = event.y()
        m_h = (np.arctan2(self.m_x-self.radius, self.m_y-self.radius)+np.pi)/(2.*np.pi)
        m_s = np.sqrt(np.power(self.m_x-self.radius, 2)+np.power(self.m_y-self.radius, 2))/self.radius
        m_v = 1.0
        self.tpp = QColor(255, 255, 255, 255)
        if m_s < 1.0 and m_s > 0.5:
            # var = round(1**(m_s))
            self.tpp.setHsvF(m_h, m_s, m_v, 1)
            self.tpp = self.tpp.getRgb()
            self.m_r = self.tpp[0]
            self.m_g = self.tpp[1]
            self.m_b = self.tpp[2]
        else:
            self.m_x = self.old_mx
            self.m_y = self.old_my
        config.red = self.r
        config.green = self.g
        config.blue = self.b
        
        self.update()
        



class PGraphicsSceneEdit(QGraphicsScene):
    def __init__(self):
        super().__init__()
        # self.PTabself = PTabself
        # self.cc = ColorCircle()

    def mousePressEvent(self, event):
        self.scene_POS = event.scenePos()
        print(self.scene_POS)

    def mouseMoveEvent(self, event):
        pass
        # print(event.scenePos())


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