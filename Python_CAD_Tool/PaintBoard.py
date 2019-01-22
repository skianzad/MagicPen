'''
Created on 2019-01-02

@author: Yuxiang Huang
'''
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.Qt import QPixmap, QPainter, QPoint, QPaintEvent, QMouseEvent, QPen,\
    QColor, QSize
from PyQt5.QtCore import Qt, QTimer
import threading
import socket
import sys

coordinates = [0, 0]
penDrawing = False

'''
	The PaintBoard class handles the drawing events, including CAD drawings and free drawing
'''
class PaintBoard(QWidget):


    def __init__(self, Parent=None):
        '''
        Constructor
        '''
        super().__init__(Parent)

        self.__InitData() #Initialize Data first, then interface/view
        self.__InitView()
        print("Init PaintBoard")
        
    def __InitView(self):
        
        self.setFixedSize(self.__size)

        
    def __InitData(self):
        
        self.__size = QSize(480,460)
        
        self.__board = QPixmap(self.__size) #Make a new QPixmap as paint board，480px * 460px
        self.__board.fill(Qt.white) #Fill the paint board with white
        
        self.__IsEmpty = True #board is empty by default 
        self.EraserMode = False #eraser mode is disabled by default
        
        self.__lastPos = QPoint(0,0)
        self.__currentPos = QPoint(0,0)
        
        self.__painter = QPainter()
        
        self.__thickness = 2                    #default pen thickness is 2
        self.__penColor = QColor("black")       #default color is black
        self.__colorList = QColor.colorNames()  #get the list of colors
        
    def Clear(self):
        #Clear the board
        self.__board.fill(Qt.white)
        self.update()
        self.__IsEmpty = True
        
    def ChangePenColor(self, color="black"):
		#Change the color of the pen
        self.__penColor = QColor(color)
        
    def ChangePenThickness(self, thickness=10):
		#Change the thickness of the pen
        self.__thickness = thickness
        
    def IsEmpty(self):
        #Is the board empty
        return self.__IsEmpty
    
    def GetContentAsQImage(self):
        #return the content of the board (return QImage)
        image = self.__board.toImage()
        return image
        
    def paintEvent(self, paintEvent):

        global coordinates, penDrawing

        self.__painter.begin(self)
        self.__painter.drawPixmap(0,0,self.__board)
        self.__painter.end()

        print("inside paintEvent")

        if penDrawing is True:
            self.penMoveEvent(coordinates)
            

    def penPressEvent(self, pos):
        
        self.__currentPos =  QPoint(pos[0],pos[1])
        self.__lastPos = self.__currentPos
        
       
    def penMoveEvent(self, pos):

        global coordinates, penDrawing

        self.__currentPos =  QPoint(pos[0],pos[1])
        self.__painter.begin(self.__board)

        #print("inside penMoveEvent")
        
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

'''
    The following classes and methods are to be used exclusively in the WiFi scenario
'''
class WiFi:

    __TCP_IP = ''
    __TCP_PORT = 8080
    __BUFFER_SIZE = 1024

    def __init__(self, TCP_IP = '', TCP_PORT = 8080, BUFFER_SIZE = 1024):
        self.__TCP_IP = TCP_IP
        self.__TCP_PORT = TCP_PORT
        self.__BUFFER_SIZE = BUFFER_SIZE

    def WiFiComms(self):

        global coordinates, penDrawing
        
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.__TCP_IP, self.__TCP_PORT))
        s.listen(1)
        conn, addr = s.accept()

        while(addr is None and conn is None):
                conn, addr = s.accept()
                #print "waiting for connection..."

        print("Connection address:", addr)
               
        while(addr is not None and conn is not None):
            penDrawing = True
            conn.sendall((str(coordinates[0])+str(",")+str(coordinates[1])\
                          +str(",////////")).encode("utf-8"))  # echo
            data = conn.recv(self.__BUFFER_SIZE)
            decodedData = data.decode("utf-8")
            #print ("received data: " + decodedData)
            coordinates = decodedData.split(",")
            #covert coordinates elements to int
            #print(coordinates)
            coordinates[0] = int(coordinates[0])
            coordinates[1] = int(coordinates[1])


class paintThread (threading.Thread):
    
    def __init__(self, threadID, name, counter):
       
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):

        global coordinates, penDrawing
        
        print("Starting " + self.name)

        app = QApplication(sys.argv)
        paintBoard = PaintBoard()
        paintBoard.show()
        exit(app.exec_())
            
        print("Exiting " + self.name)


class wifiThread (threading.Thread):
    
    def __init__(self, threadID, name, counter):
       
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):

        print("Starting " + self.name)
        
        wifi = WiFi()
        wifi.WiFiComms()

        print("Exiting " + self.name)

'''
# Create new threads
paintThread = paintThread(1, "Paint_Thread", 1)
wifiThread = wifiThread(2, "Wifi_Thread", 2)

# Start new Threads
paintThread.start()
wifiThread.start()

print("Exiting Main Thread")
'''
