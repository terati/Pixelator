from PyQt5.QtCore import QDateTime, Qt, QTimer
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QGraphicsScene, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit, 
        QMainWindow, QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
        QVBoxLayout, QWidget)

from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 

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

        self.pixmap = QPixmap("Images/brush.png")
        self.scene.addPixmap(self.pixmap)
        self.scene.setSceneRect(0,0,300,300)
        self.text1 = self.scene.addText("Hello, World").setPos(250,250)
  
        pen = QPen(Qt.white)
        side = 20
        for i in range(16):
            for j in range(16):
                r = QRectF(QPointF(i*side, j*side), QSizeF(side, side))
                self.scene.addRect(r, pen)
        self.view = QGraphicsView(self)
        self.view.setBackgroundBrush(QBrush(QColor(40, 40, 50, 230), Qt.SolidPattern))
        self.view.setScene(self.scene)
        self.zoom_num = 1
        self.view.scale(self.zoom_num,self.zoom_num)
        self.tbtmp.layout.addWidget(self.view)
        self.tbtmp.setLayout(self.tbtmp.layout)

        # self.rect = self.view.sceneRect().toRect()    #viewport().rect()
        # print(self.rect)
        # self.tmp_pixmap = QPixmap(self.rect.size())

        self.scene.clearSelection
        self.scene.setSceneRect(self.scene.itemsBoundingRect())
        self.image = QImage(self.scene.sceneRect().size().toSize(), QImage.Format_ARGB32)
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
        self.position = QPointF(2, 2)
        self.zoom_var = 10
        self.drawing = False

    def mousePressEvent(self, event):
        self.scene_POS = event.scenePos()
        if event.buttons() == Qt.LeftButton and self.Tabself.Wself.zoomout.isChecked() == True:
            self.Tabself.zoom_num = 0.5
            self.Tabself.view.scale(self.Tabself.zoom_num,self.Tabself.zoom_num)
            # print("zoom out")
        elif event.buttons() == Qt.LeftButton and self.Tabself.Wself.zoomin.isChecked() == True:
            self.Tabself.zoom_num = 2
            self.Tabself.view.scale(self.Tabself.zoom_num,self.Tabself.zoom_num)


        self.label = QLabel()
        self.label.setAttribute(Qt.WA_TranslucentBackground)
        canvas = QPixmap(400, 300)
        canvas.fill(Qt.transparent)
        self.label.setPixmap(canvas)
        painter = QPainter(self.label.pixmap())
        pen = QPen()
        pen.setWidth(40)
        pen.setColor(QColor('red'))
        painter.setPen(pen)
        painter.drawPoint(200, 150)
        painter.end()
        self.Tabself.scene.addWidget(self.label)
        self.Tabself.view.setScene(self.Tabself.scene)


        # self.Tabself.view.update()
        # self.drawing = True
        # self.Tabself.tbtmp.update()

        # self.last_point = event.scenePos()
            # print("zoom in")
        # self.Tabself.view.scale(self.Tabself.zoom_num,self.Tabself.zoom_num)

        # self.Tabself.tbtmp.layout.addWidget(self.Tabself.view)
        # self.Tabself.tbtmp.setLayout(self.Tabself.tbtmp.layout)

        # print( self.Tabself.Wself.zoomin.isChecked() )
        # print( self.Tabself.Wself.zoomout.isChecked() )
        # print( self.Tabself.zoom_num )
        
        
    # def mouseMoveEvent(self, event):
    #     if event.buttons() == Qt.LeftButton and self.Tabself.Wself.brush.isChecked() and self.drawing:
    #         self.image = QPixmap(QSize(100,100))
    #         painter = QPainter(self.image)
    #         self.bcolor = Qt.black
    #         self.bsize = 2
    #         painter.setPen(QPen(self.bcolor, self.bsize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
    #         painter.drawLine(self.last_point, self.event.scenePos())
    #         self.last_point = self.event.scenePos()
    #         self.update()

    # def paintEvent(self, event):
    #     self.scene.addPixmap(self.pixmap)
    #     self.view.setScene(self.scene)

    # def mouseReleaseEvent(self, event):
    #     if event.button == Qt.LeftButton:
    #         self.drawing = False
