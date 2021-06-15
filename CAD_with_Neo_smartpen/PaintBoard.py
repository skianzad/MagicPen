# -*- coding: utf-8 -*-
'''
Created on 2019-01-01

@author: Yuxiang, Guanxiong
'''
from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget
from PyQt5.Qt import QPixmap, QPainter, QPoint, QPaintEvent, QMouseEvent, QPen,\
    QColor, QSize
from PyQt5.QtCore import Qt, QTimer, QRectF
import threading
import socket
import sys
import math
pi=math.pi

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
        super(PaintBoard, self).__init__(Parent)

        self.__InitData(sizeX, sizeY) #Initialize Data first, then interface/view
        self.__InitView()
        print("Init PaintBoard")
        
    def __InitView(self):
        
        self.setFixedSize(self.__size)

        
    def __InitData(self, sizeX, sizeY):
        self.__size = QSize(sizeX, sizeY)
        
        self.__board = QPixmap(self.__size) # Make a new QPixmap as paint board，350px * 250px
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
        
       
    def penMoveEvent(self, pos, pressure, liftedDeque):
        pen_x = pos[0]
        pen_y = pos[1]
        pen_pressure = pressure
        
        # print(liftedDeque)
        # print(self.__lastPos)

        if self.__lastPos is None:
            self.__lastPos = QPoint(pen_x,pen_y)

        self.__currentPos =  QPoint(pen_x,pen_y)
        self.__painter.begin(self.__board)
        
        if self.EraserMode == False:
            #Non-Eraser mode
            self.__penColor=QColor("blue")
            self.__painter.setPen(QPen(self.__penColor,self.__thickness)) #Set pen color, thickness
        else:
            #Eraser mode: pen color is white, thickness is 6
            self.__painter.setPen(QPen(Qt.white,6))
            
        self.__painter.drawLine(self.__lastPos, self.__currentPos)
        self.__painter.end()
        self.__lastPos = self.__currentPos

        self.update() #Show updates
        
        # If ever detected the pen is lifted, reset the __lastPos variable in order to reposition the pen 
        if (True in liftedDeque):
            self.__lastPos = None 
    
    # Virtual Panel event
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
        self.__penColor=QColor("black")
        self.__painter.setPen(QPen(self.__penColor,self.__thickness))  
        self.__painter.drawEllipse(QPoint(center_x, center_y), radias1, radias2)

        self.__painter.end()
                
        self.update() #Show updates

    def paintRect(self, center_x, center_y, upper_left_x, upper_left_y):
        width = abs(2*(center_x - upper_left_x))
        height = abs(2*(center_y - upper_left_y))
        
        self.__painter.begin(self.__board)
        self.__penColor=QColor("black")
        self.__painter.setPen(QPen(self.__penColor,self.__thickness))    
        self.__painter.drawRect(upper_left_x, upper_left_y, width, height)

        self.__painter.end()
                
        self.update() #Show updates

    def paintTriangle(self, points):
        self.__painter.begin(self.__board)
        self.__penColor=QColor("black")
        self.__painter.setPen(QPen(self.__penColor,self.__thickness)) 
        self.__painter.drawPolygon(points)
        
        self.__painter.end()
                
        self.update() #Show updates
    def paintPolyg(self, x1,y1,x2,y2,x3,y3,x4,y4):
        self.__painter.begin(self.__board)
        self.__penColor=QColor("black")
        self.__painter.setPen(QPen(self.__penColor,self.__thickness)) 
        self.__painter.drawPolygon(QPoint(x1,y1),QPoint(x2,y2),QPoint(x3,y3),QPoint(x4,y4))        
        self.__painter.end()
                
        self.update() #Show updates

    def paintLine(self, P1_x, P1_y, P2_x, P2_y):
        P1 = QPoint(P1_x, P1_y)
        P2 = QPoint(P2_x, P2_y)
        
        self.__painter.begin(self.__board)
        self.__penColor=QColor("black")
        self.__painter.setPen(QPen(self.__penColor,self.__thickness)) 
        self.__painter.drawLine(P1, P2)
        self.__painter.end()
                
        self.update() #Show updates
    
    def paintAuxLine(self, P1_x, P1_y, P2_x, P2_y):
        P1 = QPoint(P1_x, P1_y)
        P2 = QPoint(P2_x, P2_y)
        
        self.__painter.begin(self.__board)
        self.__penColor=QColor("red")
        self.__painter.setPen(QPen(self.__penColor,self.__thickness)) 
        self.__painter.drawLine(P1, P2)
        self.__painter.end()
                
        self.update() #Show updates

    def PointsInCircum(self,r,n,phi):
        return [(math.cos(2*pi/n*x+phi)*r,math.sin(2*pi/n*x+phi)*r) for x in range(0,n+1)]  # defining the points on the Circum of a circle
        
    def paintPCircle(self,center_x,center_y,start_x,start_y,pers_x,pers_y):
        point=[start_x,start_y]
        center=[center_x,center_y]
        distance=[(point[0]-center[0]),(point[1]-center[1])]
        phi=math.atan2(distance[1],distance[0])
        r=math.sqrt(distance[0]*distance[0]+distance[1]*distance[1])
        points=self.PointsInCircum(r,300,phi)
        #Drawing the circle in perspective
        dist_x=center_x-pers_x
        print("dist_x", dist_x,pers_x,pers_y,center_x,center_y)
        points=[(j[0],(j[1]+center_x-pers_y) *((j[0]+center_x)/dist_x)+pers_y-center_y) for j in points]    
        
        self.__painter.begin(self.__board)
        self.__penColor=QColor("blue")
        self.__painter.setPen(QPen(self.__penColor,self.__thickness)) 
        for x in points:
            self.__painter.drawPoint(round(x[0]+center[0],3),round(x[1]/1.00+center[1],3))    
        
        self.__painter.end()
    
    # returns true if given angle is in the second quadrant;
    # requires angle in degree and in range -180 to 180
    def _isAngleInSecondQuadrant(self, angle):
        if angle>90 and angle<180:
            return True
        else:
            return False
    
    # returns true if given angle is in the third quadrant;
    # requires angle in degree and in range -180 to 180
    def _isAngleInThirdQuadrant(self, angle):
        if angle<-90 and angle>-180:
            return True
        else:
            return False

    
    def paintArc(self, center_x, center_y, start_x, start_y, end_x, end_y):
        radius = math.sqrt(math.pow(center_x-start_x, 2) + math.pow(center_y-start_y, 2))
        rect = QRectF(center_x - radius, center_y - radius, radius*2, radius*2)
        # start angle calculation
        startAngle = math.degrees(math.atan2(center_y - start_y, start_x - center_x))
        # end angle calculation
        endAngle = math.degrees(math.atan2(center_y - end_y, end_x - center_x))
        
        # span angle calculation
        spanAngle = endAngle - startAngle
        # assume user always wants to draw clock-wise
        if spanAngle > 0:
            spanAngle = -1 * (360 - spanAngle)
        #print("start angle is " + str(startAngle))
        #print("span angle is " + str(spanAngle))

        self.__painter.begin(self.__board)
        self.__penColor=QColor("black")
        self.__painter.setPen(QPen(self.__penColor,self.__thickness)) 
        self.__painter.drawArc(rect, 16*startAngle, 16*spanAngle)
        self.__painter.end()

        self.update() #Show updates
    
    def paintAuxArc(self, center_x, center_y, start_x, start_y, end_x, end_y):
        radius = math.sqrt(math.pow(center_x-start_x, 2) + math.pow(center_y-start_y, 2))
        rect = QRectF(center_x - radius, center_y - radius, radius*2, radius*2)
        # start angle calculation
        startAngle = math.degrees(math.atan2(center_y - start_y, start_x - center_x))
        # end angle calculation
        endAngle = math.degrees(math.atan2(center_y - end_y, end_x - center_x))

        # span angle calculation
        spanAngle = 0
        if (self._isAngleInThirdQuadrant(startAngle) and self._isAngleInSecondQuadrant(endAngle)) or (self._isAngleInThirdQuadrant(endAngle) and self._isAngleInSecondQuadrant(startAngle)) or (startAngle==180 and self._isAngleInThirdQuadrant(endAngle)) or (startAngle==-180 and self._isAngleInSecondQuadrant(endAngle)) or (endAngle==180 and self._isAngleInThirdQuadrant(startAngle)) or (endAngle==-180 and self._isAngleInSecondQuadrant(startAngle)):
            if startAngle==180 or self._isAngleInThirdQuadrant(startAngle):
                spanAngle = endAngle - (startAngle + 360)
            else:
                spanAngle = (endAngle + 360) - startAngle
        else:
            spanAngle = endAngle - startAngle
        #print("start angle is " + str(startAngle))
        #print("span angle is " + str(spanAngle))

        self.__painter.begin(self.__board)
        self.__penColor=QColor("red")
        self.__painter.setPen(QPen(self.__penColor,self.__thickness)) 
        self.__painter.drawArc(rect, 16*startAngle, 16*spanAngle)
        self.__painter.end()

        self.update() #Show updates
        

    def paintBezierSpline(self, pointListX, pointListY):
        P1 = QPoint(int(pointListX[0]), int(pointListY[0]))
        path = QtGui.QPainterPath()
        path.moveTo(P1)
            
        self.__painter.begin(self.__board)
        self.__penColor=QColor("black")
        self.__painter.setPen(QPen(self.__penColor,self.__thickness))

        i = 0
        while i < len(pointListX)-3:
            P2 = QPoint(int(pointListX[i+1]), int(pointListY[i+1]))
            P3 = QPoint(int(pointListX[i+2]), int(pointListY[i+2]))
            P4 = QPoint(int(pointListX[i+3]), int(pointListY[i+3]))
            path.cubicTo(P2, P3, P4)
            self.__painter.drawPath(path)
            i += 3
        
        self.__painter.end()
        
        self.update() #Show updates
