from PyQt5.QtCore import QDateTime, Qt, QTimer
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QGraphicsScene, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit, 
        QMainWindow, QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
        QVBoxLayout, QWidget)

from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
import math

import config

class TabManager(QWidget):
    def __init__(self, Wself):
        # super(QWidget, self).__init__(parent)
        super().__init__()
        self.Wself = Wself
        self.layout = QVBoxLayout()
        self.index = 0

        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget { 
                font-size: 30 pt;
            }
        """)
        self.tabs.setTabsClosable(True)
        self.tabs.setMovable(True)
        
        self.tabs.tabCloseRequested.connect(self.closeTabHandler)
        self.tablist = []
        self.tablist.append( self.addTab(self.index) )
        

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

        self.setMouseTracking(True) 
      

    def addTab(self, index):
        self.tbtmp = QWidget()
        self.tbtmp.setStyleSheet("""
            QWidget {
                font-size: 20 pt;
                color: black;
            }
        """)
        self.tabs.addTab(self.tbtmp, f"Tab {self.index}")
        self.index = self.index + 1

        self.tbtmp.layout = QVBoxLayout()
        self.drawing = False
        self.brushSize = 2
        self.brushColor = Qt.white
        # self.image = QImage(5,5, QImage.Format_RGB32)
        # self.image.fill(Qt.black)

        self.scene = QGraphicsSceneEdit(self)

        # self.pixmap = QPixmap("Images/brush.png")
        # self.scene.addPixmap(self.pixmap)

        self.scene.setSceneRect(0,0,10,10)
        # self.text1 = self.scene.addText("Hello, World").setPos(250,250)
  
        pen = QPen(Qt.transparent, 0, Qt.DotLine, Qt.SquareCap, Qt.BevelJoin)
        side = 1
        
        x = Qt.darkGray
        y = Qt.lightGray
        flag = 0
        for i in range(10):
            for j in range(10):
                r = QRectF(QPointF(j*side, i*side), QSizeF(side, side))
                if flag == 1:
                    self.scene.addRect(r, pen).setBrush(QBrush(x))
                    flag = 0
                else:
                    self.scene.addRect(r, pen).setBrush(QBrush(y))
                    flag = 1
            if flag == 0:
                flag = 1
            else:
                flag = 0
        pen = QPen(Qt.black, 0.1, Qt.DotLine, Qt.SquareCap, Qt.BevelJoin)
        side = 1 
        for i in range(11):
            self.scene.addLine(i*side, 0, i*side, 10, pen).setZValue(1) #Vertical Lines
            self.scene.addLine(0, i*side, 10, i*side, pen).setZValue(1) #Horizontal Lines
        

        self.view = QGraphicsView(self)
        self.view.setBackgroundBrush(QBrush(QColor(40, 40, 50, 230), Qt.SolidPattern))
        self.view.setScene(self.scene)
        self.zoom_num = 50
        self.view.scale(self.zoom_num,self.zoom_num)
        self.tbtmp.layout.addWidget(self.view)        
        self.tbtmp.setLayout(self.tbtmp.layout)
        
        # self.rect = self.view.sceneRect().toRect()    #viewport().rect()
        # print(self.rect)
        # self.tmp_pixmap = QPixmap(self.rect.size())

        self.scene.clearSelection
        # self.scene.setSceneRect(self.scene.itemsBoundingRect())
        self.scene.setSceneRect(0, 0, 10, 10) #self.scene.sceneRect().size().toSize()
        self.image = QImage(10, 10, QImage.Format_ARGB32)
        # print(self.scene.sceneRect().size().toSize())
        self.image.fill(Qt.transparent)

        self.painter = QPainter(self.image)
        self.scene.render(self.painter)
        self.painter.end()
      
      
        # self.image.save("asdfas.png")

        # self.tmp_pixmap = self.view.grab(self.view.sceneRect().toRect() );        
        # self.tmp_pixmap.save("tmppix.png")

        # self.label = QLabel()
        # self.pixmap = QPixmap("Images/brush.png")
        # self.label.setPixmap(self.pixmap)
        # self.tbtmp.layout.addWidget(self.label)
        # self.tbtmp.setLayout(self.tbtmp.layout)

    def paintEvent(self, event):
        # canvasPainter = QPainter(self)
        # canvasPainter.drawImage(self.rect(), self.image, self.rect())
        # print(self.rect())
        # print("CanEvent")
        pass



    def closeTabHandler(self, index): 
        print (f"close_handler called, index = {index}")
        self.tabs.removeTab(index)
        self.index = self.index - 1
        print(self.index)

    @pyqtSlot()
    def on_click(self):
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())


class QGraphicsSceneEdit(QGraphicsScene):
    def __init__(self, Tabself):
        super().__init__()
        self.Tabself = Tabself
        self.position = QPointF(0, 0)
        self.zoom_var = 10
        self.drawing = False
        self.last_point = QPoint()

    def mousePressEvent(self, event):
        self.scene_POS = event.scenePos()
        if event.buttons() == Qt.LeftButton and self.Tabself.Wself.zoomout.isChecked() == True:
            self.Tabself.zoom_num = 0.5
            self.Tabself.view.scale(self.Tabself.zoom_num,self.Tabself.zoom_num)
            # print("zoom out")
        elif event.buttons() == Qt.LeftButton and self.Tabself.Wself.zoomin.isChecked() == True:
            self.Tabself.zoom_num = 2
            self.Tabself.view.scale(self.Tabself.zoom_num,self.Tabself.zoom_num)
        # print(event.scenePos())

        if event.buttons() == Qt.LeftButton and self.Tabself.Wself.brush.isChecked(): #and self.drawing:
            
            self.label = QLabel()
            self.label.setStyleSheet("""
                QLabel {
                    padding: 0px;
                }
            """)
            self.label.setAttribute(Qt.WA_TranslucentBackground)
            canvas = QPixmap(10, 10)
            canvas.fill(Qt.transparent)
            
            
            # painter = QPainter(self.label.pixmap())
            painter = QPainter(canvas)
            pen = QPen()
            pen.setWidth(1)
            # print(config.red)
            ctmp = QColor(config.red, config.green, config.blue)
            # ctmp = ctmp.darker()
            pen.setColor(ctmp)
            painter.setPen(pen)
            painter.drawPoint(event.scenePos().x(), event.scenePos().y())
            # print(event.scenePos().x())
            painter.end()
            self.label.setPixmap(canvas)
            self.Tabself.scene.addWidget(self.label)
            self.Tabself.view.setScene(self.Tabself.scene)
            self.last_point = event.scenePos()
            # print(event.scenePos())
            self.update()
        self.last_point = event.scenePos()
        
        
    def mouseMoveEvent(self, event):
        # print(event.scenePos())
         
        if event.buttons() == Qt.LeftButton and self.Tabself.Wself.brush.isChecked(): #and self.drawing:
            
            self.label = QLabel()
            self.label.setStyleSheet("""
                QLabel {
                    padding: 0px;
                }
            """)
            self.label.setAttribute(Qt.WA_TranslucentBackground)
            canvas = QPixmap(10, 10)
            canvas.fill(Qt.transparent)
            
            
            # painter = QPainter(self.label.pixmap())
            painter = QPainter(canvas)
            pen = QPen()
            pen.setWidth(1)
            pen.setColor(QColor(config.red, config.green, config.blue))
            painter.setPen(pen)
            painter.drawLine(self.last_point, event.scenePos())
            painter.end()
            self.label.setPixmap(canvas)
            self.Tabself.scene.addWidget(self.label)
            self.Tabself.view.setScene(self.Tabself.scene)
            self.last_point = event.scenePos()
            # print(event.scenePos())
            self.update()
        self.last_point = event.scenePos()

