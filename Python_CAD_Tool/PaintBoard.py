'''
Created on 2019-01-01

@author: Yuxiang
'''
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.Qt import QPixmap, QPainter, QPoint, QPaintEvent, QMouseEvent, QPen,\
    QColor, QSize
from PyQt5.QtCore import Qt, QTimer
import threading
import socket
import sys

penDrawing = False
#356, 470

class PaintBoard(QWidget):

    # Define virtual panel coordinates for different shapes/regions
    VPCoord_Start   =   [316, 332]           #LeftTopX, Y
    VPCoord_Circle  =   [316, 332, 336, 363] #LeftTopX, Y, RightBotX, Y 
    VPCoord_Rect    =   [336, 332, 356, 363] #LeftTopX, Y, RightBotX, Y    
    VPCoord_Tri     =   [316, 363, 336, 395] #LeftTopX, Y, RightBotX, Y 
    VPCoord_Line    =   [336, 363, 356, 395] #LeftTopX, Y, RightBotX, Y

    # A flag to check if the user is currently using the virtual panel
    usingVP = False

    def __init__(self, sizeX, sizeY, Parent=None):
        '''
        Constructor
        '''
        super().__init__(Parent)

        self.__InitData(sizeX, sizeY) #Initialize Data first, then interface/view
        self.__InitView()
        print("Init PaintBoard")
        
    def __InitView(self):
        
        self.setFixedSize(self.__size)

        
    def __InitData(self, sizeX, sizeY):
        self.__size = QSize(sizeX, sizeY)
        
        self.__board = QPixmap(self.__size) #Make a new QPixmap as paint board，350px * 250px
        self.__board.fill(Qt.white) #Fill the paint board with white
        
        self.__IsEmpty = True #board is empty by default 
        self.EraserMode = False #eraser mode is disabled by default
        
        self.__lastPos = None
        self.__currentPos = QPoint(0,0)
        
        self.__painter = QPainter()
        
        self.__thickness = 1                    #default pen thickness is 1
        self.__penColor = QColor("black")       #default color is black
        self.__colorList = QColor.colorNames()  #get the list of colors
        
    def Clear(self):
        #Clear the board
        self.__board.fill(Qt.white)
        self.update()
        self.__IsEmpty = True
        
    def ChangePenColor(self, color="black"):
        self.__penColor = QColor(color)
        
    def ChangePenThickness(self, thickness=1):
        self.__thickness = thickness
        
    def IsEmpty(self):
        #Is the board empty
        return self.__IsEmpty
    
    def GetContentAsQImage(self):
        #return the content of the board (return QImage)
        image = self.__board.toImage()
        return image
        
    def paintEvent(self, paintEvent):


        self.__painter.begin(self)
        self.__painter.drawPixmap(0,0,self.__board)
        self.__painter.end()

        # print("inside paintEvent")
            

    def penPressEvent(self, pos):
        
        self.__currentPos =  QPoint(pos[0],pos[1])
        self.__lastPos = self.__currentPos
        
       
    def penMoveEvent(self, pos, pressure):
        pen_x = pos[0]
        pen_y = pos[1]
        pen_pressure = pressure

        if self.__lastPos is None:
            self.__lastPos = QPoint(pen_x,pen_y)
        elif (abs(pen_x-self.__lastPos.x()) > 21 or abs(pen_y-self.__lastPos.y()) > 21):
            self.__lastPos = QPoint(pen_x,pen_y)       

        self.__currentPos =  QPoint(pen_x,pen_y)
        self.__painter.begin(self.__board)
        
        if self.EraserMode == False:
            #Non-Eraser mode
            self.__painter.setPen(QPen(self.__penColor,self.__thickness)) #Set pen color, thickness
        else:
            #Eraser mode: pen color is white, thickness is 6
            self.__painter.setPen(QPen(Qt.white,6))
            
        self.__painter.drawLine(self.__lastPos, self.__currentPos)
        self.__painter.end()
        self.__lastPos = self.__currentPos

        self.update() #Show updates

    
    def penVPEvent(self, pos, pressure):
        pass
    '''    
        # Check if the pressure is over 500
        if(pen_pressure > 400):
            # Check which region the pen is in and prepare to draw shape accordingly
            if(pen_x < self.VPCoord_Circle[2] and pen_y < self.VPCoord_Circle[3]):
                print("A")        
            elif(pen_x < self.VPCoord_Rect[2] and pen_y < self.VPCoord_Rect[3]):
                print("B")
            elif(pen_x < self.VPCoord_Tri[2] and pen_y < self.VPCoord_Tri[3]):
                print("C")
            elif(pen_x < self.VPCoord_Line[2] and pen_y < self.VPCoord_Line[3]):
                print("D")
    '''
            
    def penReleaseEvent(self, pos):
        self.__IsEmpty = False #board is not empty

    def paintEllipse(self, center_x, center_y, radias1, radias2):
        self.__painter.begin(self.__board)

        self.__painter.setPen(QPen(self.__penColor,self.__thickness))  
        self.__painter.drawEllipse(QPoint(center_x, center_y), radias1, radias2)

        self.__painter.end()
                
        self.update() #Show updates

    def paintRect(self, center_x, center_y, upper_left_x, upper_left_y):
        width = abs(2*(center_x - upper_left_x))
        height = abs(2*(center_y - upper_left_y))
        
        self.__painter.begin(self.__board)
        
        self.__painter.setPen(QPen(self.__penColor,self.__thickness))    
        self.__painter.drawRect(upper_left_x, upper_left_y, width, height)

        self.__painter.end()
                
        self.update() #Show updates

    def paintTriangle(self, points):
        self.__painter.begin(self.__board)
        
        self.__painter.setPen(QPen(self.__penColor,self.__thickness)) 
        self.__painter.drawPolygon(points)
        
        self.__painter.end()
                
        self.update() #Show updates

    def paintLine(self, P1_x, P1_y, P2_x, P2_y):
        P1 = QPoint(P1_x, P1_y)
        P2 = QPoint(P2_x, P2_y)
        
        self.__painter.begin(self.__board)
        self.__painter.drawLine(P1, P2)
        self.__painter.end()
                
        self.update() #Show updates
