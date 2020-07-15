# -*- coding: utf-8 -*-
'''
Created on 2019-01-01

@author: Yuxiang, Guanxiong, Soheil
'''
import collections
from PyQt4 import QtGui
from PyQt4.Qt import *
import time
# from PyQt4.QtCore import *
from PaintBoard import PaintBoard
# from WiFi import WiFiThread
from Bluetooth import BluetoothThread
import math
from Shapes import *
from Relations import *
#from Control import ControlThread


class MainWidget(QWidget):
    # 80 * 200 pallet
    # Define virtual panel coordinates for different shapes/regions
    VPCoord_Start   =   [80, 275]            #LeftTopX, Y (originally 316, 332)
    VPCoord_Circle  =   [0,  0,   40, 50]    #LeftTopX, Y, RightBotX, Y 
    VPCoord_Rect    =   [40, 0,   80, 50] 
    VPCoord_Tri     =   [0,  50,  40, 100] 
    VPCoord_Line    =   [40, 50,  80, 100] 
    VPCoord_Arc     =   [0,  100, 40, 150] 
    VPCoord_Curve   =   [40, 100, 80, 150]
    VPCoord_Perspect    =   [0,  150, 40, 200] 
    VPCoord_Ruler   =   [40, 150, 80, 200] 
    # VPCoord_Copy    =   [0,  150, 40, 200] 
    #VPCoord_Paste   =   [40, 150, 80, 200] 
    # Define virtual ruler coordinates
    VRCoord = [80, 0, 180, 50]
    #Define virtual panel coordinates for different constraints
    VPCoord_Alignment = [0, 200, 40, 225]
    VPCoord_Distance = [40, 200, 80, 225]
    VPCoord_Concentric = [0, 225, 40, 250]
    VPCoord_Parallel = [40, 225, 80, 250]
    VPCoord_Perpendicular = [0, 250, 40, 275]

    # A flag to check if the user is currently using the virtual panel
    usingVP         = False
    usingVP_Line    = False
    usingVP_Rect    = False
    usingVP_Circle  = False
    usingVP_Arc     = False
    usingVP_Tri     = False
    usingVP_Curve   = False
    usingVP_Copy    = False
    usingVP_Paste   = False
    usingVP_Perspect= False
    usingVP_VPoint  = False
    usingVP_Ruler  = False
    
    # a flag to check if the user is using the motor to draw shapes
    usingMotor      = False
    usingMotor_Line = False
    
    vpPointCount = 0 
    vpShapePointList = []
    vpCopyPointList  = []
    vpVanishingPoint = []
    vpVpoint=[]
    
    controlLineSignal = pyqtSignal(list)
    controlRectSignal = pyqtSignal(list)
    controlRectPSignal= pyqtSignal(list)
    controlTriSignal  = pyqtSignal(list)
    gcoordinate = pyqtSignal(list)
    
    # A deque used to store the recent "lifted" variable from the pen due to asynch bluetooth transmission
    liftedDeque = collections.deque(3*[True], 3)

    # Data structures to hold parameterized objects
    circList = [] # stores previous circles and arcs
    rectList = []
    triList = []
    lineList = []
    distMeasurementList = []

    # flags representing if a constraint has been applied
    constraintAlignment_enabled = True # default enabled relation is alignment
    constraintDist_enabled = False
    constraintConcentric_enabled = False
    constraintParallel_enabled = False
    constraintPerpendicular_enabled = False

    # macros for constraints
    CONSTRAINT_ALIGNMENT = "constraint"
    CONSTRAINT_CONCENTRIC = "concentric"
    CONSTRAINT_DIST = "distance"
    CONSTRAINT_PARALLEL = "parallel"
    CONSTRAINT_PERP = "perpendicular"

    # Data structures for alignments. Always refer to the current object
    alignmentCenter = None
    alignmentUL = None

    # Data structures for distance relations. Always refer to the current object

    # Data structures for concentric relations. Always refer to the current object
    
    # the current object being drawn on paper
    currObject = None

    # the last object being drawn; used when distance constraint applied
    lastObject = None

    def __init__(self, Parent=None):
        '''
                Constructor
        ''' 
        super(MainWidget, self).__init__(Parent)

        #The NeoSmartpen custom paper is 88.3 x 114.2 in raw coordinates
        rawLimitX =100
        rawLimitY = 85
        multiplier = 8
        
        paintSizeX = rawLimitX * multiplier
        paintSizeY = rawLimitY * multiplier
        mainSizeX = paintSizeX + 30
        mainSizeY = paintSizeY + 170

        self.__InitData(paintSizeX, paintSizeY) #First initialize data, then initialize view/interface
        self.__InitView(mainSizeX, mainSizeY)
        #self.__InitWiFi()
        self.__InitBluetooth()
        #self.__InitControl()

    '''
    def __InitWiFi(self):
        
                  #initialize the tcp server
        
        self.WiFiThread = WiFiThread()
        self.WiFiThread.sigOut.connect(self.free_draw_updates)
        # self.WiFiThread.sigOut.connect(self.VP_draw_updates)
        self.WiFiThread.start()
    '''
    
    
    def __InitBluetooth(self):
        '''
                 initialize the bluetooth
        '''
        self.BluetoothThread = BluetoothThread()
        self.BluetoothThread.sigOut.connect(self.free_draw_updates)
        # self.WiFiThread.sigOut.connect(self.VP_draw_updates)
        self.BluetoothThread.start()
    
    """
    def __InitControl(self):
        '''
                 initialize the motor control
        '''
        self.ControlThread = ControlThread()
        self.controlLineSignal.connect(self.ControlThread.receiveLineData)
        self.controlRectSignal.connect(self.ControlThread.receiveRectData)
        self.controlRectPSignal.connect(self.ControlThread.receiveRectPData)
        self.controlTriSignal.connect(self.ControlThread.receiveTriData)
        self.gcoordinate.connect(self.ControlThread.gpos)
        self.ControlThread.start()
    """
    

    def __InitData(self, sizeX, sizeY):
        '''
                  initialize data
        '''
        self.__paintBoard = PaintBoard(sizeX, sizeY)
        self.__colorList = QColor.colorNames() #Get a list of color names
        self.penCoordinates = [0,0]
        self.penPressure = 0
        
    def __InitView(self, sizeX, sizeY):
        '''
                  initialize UI
        '''
        print("inside MainWidget")
        self.setFixedSize(sizeX,sizeY)
        self.setWindowTitle("PaintBoard Example PyQt5")
        
        
        main_layout = QVBoxLayout(self)     #Create a new horizontal box layout as the main UI
        main_layout.setSpacing(10)          #Set the inner border space and space between wedgets to 10px

        self.sub_layout_root = QHBoxLayout()     # Create a sub layuout to place button on top
        self.sub_layout_control = QGridLayout()   # Create a new horizontal sub layout for control buttons
        self.sub_layout_CAD = QGridLayout()      # Create a new grid sub layout for CAD buttons

        self.sub_layout_root.setSpacing(20)
        self.sub_layout_control.setSpacing(10)
        self.sub_layout_CAD.setSpacing(20)
        self.sub_layout_root.setContentsMargins(0, 0, 10, 0) # Only set the rigt margin (10) for now
        
        self.__init_control_buttons()
        self.__init_CAD_buttons()

        Separator = QFrame()
        Separator.setFrameShape(QFrame.VLine)
        Separator.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        Separator.setLineWidth(1)

        self.sub_layout_root.addLayout(self.sub_layout_CAD, 2)
        self.sub_layout_root.addWidget(Separator)
        self.sub_layout_root.addLayout(self.sub_layout_control, 2)
        

        main_layout.addLayout(self.sub_layout_root)  #Add the sub-layout to the main UI
        main_layout.addWidget(self.__paintBoard)        #put the paintboard at the left side of the main UI


    # Initialize buttons for control functionalities
    def __init_control_buttons(self):
        self.__btn_Clear = QPushButton("Clear")
        self.__btn_Clear.setParent(self) #set the parent to self (the main UI)
        self.__btn_Clear.clicked.connect(self.__paintBoard.Clear) #connect the "clear" button to the "clear paintboard" method
        self.sub_layout_control.addWidget(self.__btn_Clear, 0, 0)
        
        self.__btn_Quit = QPushButton("Quit")
        self.__btn_Quit.setParent(self) #set the parent to self (the main UI)
        self.__btn_Quit.clicked.connect(self.Quit)
        self.sub_layout_control.addWidget(self.__btn_Quit, 0, 1)
        
        self.__btn_Save = QPushButton("Save")
        self.__btn_Save.setParent(self)
        self.__btn_Save.clicked.connect(self.on_btn_Save_Clicked)
        self.sub_layout_control.addWidget(self.__btn_Save, 1, 0)
        
        self.__cbtn_Eraser = QCheckBox("Eraser")
        self.__cbtn_Eraser.setParent(self)
        self.__cbtn_Eraser.clicked.connect(self.on_cbtn_Eraser_clicked)
        self.sub_layout_control.addWidget(self.__cbtn_Eraser, 1, 1)
        
        splitter = QSplitter(self) #a splitter to add space
        self.sub_layout_control.addWidget(splitter)
        
        self.__label_penThickness = QLabel(self)
        self.__label_penThickness.setText("Thickness")
        self.__label_penThickness.setFixedHeight(20)
        self.sub_layout_control.addWidget(self.__label_penThickness, 2, 0)
        
        self.__spinBox_penThickness = QSpinBox(self)
        self.__spinBox_penThickness.setMaximum(10)
        self.__spinBox_penThickness.setMinimum(1)
        self.__spinBox_penThickness.setValue(2)     #default thickness is 2
        self.__spinBox_penThickness.setSingleStep(1) #minimum single step is 1
        self.__spinBox_penThickness.valueChanged.connect(self.on_PenThicknessChange)#Connect spinBox's value change to on_PenThicknessChange method
        self.sub_layout_control.addWidget(self.__spinBox_penThickness, 2, 1)
        
        self.__label_penColor = QLabel(self)
        self.__label_penColor.setText("Color")
        self.__label_penColor.setFixedHeight(20)
        self.sub_layout_control.addWidget(self.__label_penColor, 3, 0)
        
        self.__comboBox_penColor = QComboBox(self)
        self.__fillColorList(self.__comboBox_penColor) #Fill the color table/list with various colors
        self.__comboBox_penColor.currentIndexChanged.connect(self.on_PenColorChange) #on_PenColorChange
        self.sub_layout_control.addWidget(self.__comboBox_penColor, 3, 1)


    # Initialize buttons for CAD functionalities
    def __init_CAD_buttons(self):
        self.__cbtn_DrawCircle = QPushButton("")
        self.__cbtn_DrawCircle.setParent(self)
        self.__cbtn_DrawCircle.setIcon(QtGui.QIcon('icons/ellipse.png'))
        self.__cbtn_DrawCircle.clicked.connect(self.on_cbtn_DrawCircle_clicked)
        self.sub_layout_CAD.addWidget(self.__cbtn_DrawCircle, 1, 0)

        self.__cbtn_DrawRect = QPushButton("")
        self.__cbtn_DrawRect.setParent(self)
        self.__cbtn_DrawRect.setIcon(QtGui.QIcon('icons/rectangle.png'))
        self.__cbtn_DrawRect.clicked.connect(self.on_cbtn_DrawRect_clicked)
        self.sub_layout_CAD.addWidget(self.__cbtn_DrawRect, 1, 1)

        self.__cbtn_DrawTriangle = QPushButton("")
        self.__cbtn_DrawTriangle.setParent(self)
        self.__cbtn_DrawTriangle.setIcon(QtGui.QIcon('icons/polygon.png'))
        self.__cbtn_DrawTriangle.clicked.connect(self.on_cbtn_DrawTriangle_clicked)
        self.sub_layout_CAD.addWidget(self.__cbtn_DrawTriangle, 2, 0)

        self.__cbtn_DrawLine = QPushButton("")
        self.__cbtn_DrawLine.setParent(self)
        self.__cbtn_DrawLine.setIcon(QtGui.QIcon('icons/segment.png'))
        self.__cbtn_DrawLine.clicked.connect(self.on_cbtn_DrawLine_clicked)
        self.sub_layout_CAD.addWidget(self.__cbtn_DrawLine, 2, 1)
        
        self.__cbtn_DrawArc = QPushButton("")
        self.__cbtn_DrawArc.setParent(self)
        self.__cbtn_DrawArc.setIcon(QtGui.QIcon('icons/arc.png'))
        self.__cbtn_DrawArc.clicked.connect(self.on_cbtn_DrawArc_clicked)
        self.sub_layout_CAD.addWidget(self.__cbtn_DrawArc, 3, 0)

        self.__cbtn_DrawBezierSpline = QPushButton("")
        self.__cbtn_DrawBezierSpline.setParent(self)
        self.__cbtn_DrawBezierSpline.setIcon(QtGui.QIcon('icons/nurbs.png'))
        self.__cbtn_DrawBezierSpline.clicked.connect(self.on_cbtn_DrawBezierSpline_clicked)
        self.sub_layout_CAD.addWidget(self.__cbtn_DrawBezierSpline, 3, 1)
        

    def __fillColorList(self, comboBox):

        index_black = 0
        index = 0
        for color in self.__colorList: 
            if color == "black":
                index_black = index
            index += 1
            pix = QPixmap(70,20)
            pix.fill(QColor(color))
            comboBox.addItem(QIcon(pix),color)
            comboBox.setIconSize(QSize(70,20))
            comboBox.setSizeAdjustPolicy(QComboBox.AdjustToContents)

        comboBox.setCurrentIndex(index_black)
        
    def on_PenColorChange(self):
        color_index = self.__comboBox_penColor.currentIndex()
        color_str = self.__colorList[color_index]
        self.__paintBoard.ChangePenColor(color_str)

    def on_PenThicknessChange(self):
        penThickness = self.__spinBox_penThickness.value()
        self.__paintBoard.ChangePenThickness(penThickness)

    def on_btn_Save_Clicked(self):
        savePath = QFileDialog.getSaveFileName(self, 'Save Your Paint', '.\\', '*.png')
        print(savePath)
        if savePath[0] == "":
            print("Save cancel")
            return
        image = self.__paintBoard.GetContentAsQImage()
        image.save(savePath[0])
        
    def on_cbtn_Eraser_clicked(self):
        if self.__cbtn_Eraser.isChecked():
            self.__paintBoard.EraserMode = True #Enter Eraser Mode [Note: The eraser mode does not work yet]
        else:
            self.__paintBoard.EraserMode = False #Quit Eraser Mode

    # CAD functionalities
    def on_cbtn_DrawCircle_clicked(self):
        painter = QPainter(self)
        window = Dialog(['center', 'radias'])
        data = window.getData(['center', 'radias'])
        self.usingVP = False
        center_x = int(data[0].split(',')[0])
        center_y = int(data[0].split(',')[1])
        radias = int(data[1])
        self.__paintBoard.paintEllipse(center_x, center_y, radias, radias)
        
    def on_cbtn_DrawRect_clicked(self):
        painter = QPainter(self)
        window = Dialog(['center', 'upper left point'])     
        data = window.getData(['center', 'upper left point'])
        self.usingVP = False
        center_x = int(data[0].split(',')[0])
        center_y = int(data[0].split(',')[1])
        upper_left_x = int(data[1].split(',')[0])
        upper_left_y = int(data[1].split(',')[1]) 
        self.__paintBoard.paintRect(center_x, center_y, upper_left_x, upper_left_y)
 
    def on_cbtn_DrawTriangle_clicked(self):
        painter = QPainter(self)
        window = Dialog(['point1', 'point2', 'point3'])
        data = window.getData(['point1', 'point2', 'point3'])
        self.usingVP = False
        P1_x = int(data[0].split(',')[0])
        P1_y = int(data[0].split(',')[1])
        P2_x = int(data[1].split(',')[0])
        P2_y = int(data[1].split(',')[1])
        P3_x = int(data[2].split(',')[0])
        P3_y = int(data[2].split(',')[1])
        points = QPolygon([
            QPoint(P1_x, P1_y),
            QPoint(P2_x, P2_y),
            QPoint(P3_x, P3_y)]
        )   
        self.__paintBoard.paintTriangle(points)

    def on_cbtn_DrawLine_clicked(self):
        painter = QPainter(self)
        window = Dialog(['Point1', 'Point2'])
        data = window.getData(['Point1', 'Point2'])
        self.usingVP = False
        P1_x = int(data[0].split(',')[0])
        P1_y = int(data[0].split(',')[1])
        P2_x = int(data[1].split(',')[0])
        P2_y = int(data[1].split(',')[1])
        self.__paintBoard.paintLine(P1_x, P1_y, P2_x, P2_y)

    
    def on_cbtn_DrawArc_clicked(self):
        painter = QPainter(self)
        window = Dialog(['center', 'start point', 'end point'])
        data = window.getData(['center', 'start point', 'end point'])
        center_x = int(data[0].split(',')[0])
        center_y = int(data[0].split(',')[1])
        start_x = int(data[1].split(',')[0])
        start_y = int(data[1].split(',')[1])
        end_x = int(data[2].split(',')[0])
        end_y = int(data[2].split(',')[1])
        self.__paintBoard.paintArc(center_x, center_y, start_x, start_y, end_x, end_y)

    #10,20;20,30;90,40;60,70;90,90;130,150;100,120;130,190
    def on_cbtn_DrawBezierSpline_clicked(self):
        painter = QPainter(self)
        window = Dialog(['Points'])
        data = window.getData(['Points'])
        self.usingVP = False
        pointList = data[0].split(';')

        if(len(pointList)%4 is not 0):
            print("Invalid point list!")
            return
        else:
            pointListX = []
            pointListY = []
            for i in range(len(pointList)):
                pointListX.append(pointList[i].split(',')[0])
                pointListY.append(pointList[i].split(',')[1])
            self.__paintBoard.paintBezierSpline(pointListX, pointListY)

    # toggle the given constraint on and others off
    def turn_on_constraint(self, constraint):
        self.constraintAlignment_enabled = False
        self.constraintConcentric_enabled = False
        self.constraintDist_enabled = False
        self.constraintParallel_enabled = False
        self.constraintPerpendicular_enabled = False
        if constraint == self.CONSTRAINT_ALIGNMENT:
            self.constraintAlignment_enabled = True
        elif constraint == self.CONSTRAINT_CONCENTRIC:
            self.constraintConcentric_enabled = True
        elif constraint == self.CONSTRAINT_DIST:
            self.constraintDist_enabled = True
        elif constraint == self.CONSTRAINT_PARALLEL:
            self.constraintParallel_enabled = True
        elif constraint == self.CONSTRAINT_PERP:
            self.constraintPerpendicular_enabled = True
        return

    # Free drawing functionalities; also a state machine
    def free_draw_updates(self, penDataList):
        self.gcoordinate.emit(penDataList)
        lifted = penDataList[3]
        self.liftedDeque.append(lifted)
        # print(penDataList)
        # print("calling free_draw_updates")   
        
        if penDataList is not None:
            # print(penDataList)
            # State 1: free drawing
            if(not(penDataList[0] < self.VPCoord_Start[0] and penDataList[1] < self.VPCoord_Start[1]) and self.usingVP is False):
                self.penCoordinates[0] = penDataList[0]
                self.penCoordinates[1] = penDataList[1]
                self.penPressure = penDataList[2]
                #print("calling penMoveEvent" + str(self.liftedDeque) + str(penDataList))
                self.__paintBoard.penMoveEvent(self.penCoordinates, self.penPressure, self.liftedDeque)
                return

            # State 2: click with force within the VP boundary to begin using the VP functions
            elif(self.usingVP is False): # penDataList[2] > 10 and 
                '''
                self.penCoordinates[0] = penDataList[0]
                self.penCoordinates[1] = penDataList[1]
                self.penPressure = penDataList[2]
                '''
                #print(penDataList)
                pen_x = penDataList[0]
                pen_y = penDataList[1]
                pen_pressure = penDataList[2]
                self.usingMotor=False
                self.vpShapePointList = []
                self.vpPointCount = 0
                # lifted = True means the pen has been lifted
                # Check which region the pen is in and prepare enter different states accordingly
                if(pen_x < self.VPCoord_Circle[2] and pen_y < self.VPCoord_Circle[3] and pen_x!=0 and lifted==True):
                    print("Circle")
                    self.usingVP = True
                    self.usingVP_Circle = True
                    self.vpShapePointList = []
                    self.vpPointCount = 0
                    self.currObject = Circle(0, 0, 0)
                    self.alignmentCenter = None
                    self.alignmentUL = None
                    self.BluetoothThread.beep()
                    time.sleep(0.5)
                    self.BluetoothThread.beep()
                    return
                    # self.on_cbtn_DrawCircle_clicked()
                    
                elif(pen_x < self.VPCoord_Rect[2] and pen_y < self.VPCoord_Rect[3] and lifted==True):
                    print("Rect")
                    self.usingVP = True
                    self.usingVP_Rect = True
                    self.vpShapePointList = []
                    self.vpPointCount = 0
                    self.currObject = Rectangle(0, 0, 0, 0)
                    self.alignmentCenter = None
                    self.alignmentUL = None
                    self.BluetoothThread.beep()
                    time.sleep(0.5)
                    self.BluetoothThread.beep()
                    return

                elif(pen_x < self.VPCoord_Tri[2] and pen_y < self.VPCoord_Tri[3] and lifted==True):
                    print("Tri")
                    self.usingVP = True
                    self.usingVP_Tri = True
                    self.vpShapePointList = []
                    self.vpPointCount = 0
                    self.currObject = Triangle(0, 0, 0, 0, 0, 0)
                    self.alignmentCenter = None
                    self.alignmentUL = None
                    self.BluetoothThread.beep()
                    time.sleep(0.5)
                    self.BluetoothThread.beep()
                    return

                elif(pen_x < self.VPCoord_Line[2] and pen_y < self.VPCoord_Line[3] and lifted==True):
                    print("Line")
                    self.usingVP = True
                    self.usingVP_Line = True
                    self.vpShapePointList = []
                    self.vpPointCount = 0
                    self.currObject = Line(0, 0, 0, 0)
                    self.alignmentCenter = None
                    self.alignmentUL = None
                    self.BluetoothThread.beep()
                    time.sleep(0.5)
                    self.BluetoothThread.beep()
                    # return to prevent going further down
                    return

                elif(pen_x < self.VPCoord_Arc[2] and pen_y < self.VPCoord_Arc[3] and lifted==True):
                    print("Arc")
                    self.usingVP = True
                    self.usingVP_Arc = True
                    self.vpShapePointList = []
                    self.vpPointCount = 0
                    self.currObject = Arc(0, 0, 0, 0, 0, 0)
                    self.alignmentCenter = None
                    self.alignmentUL = None
                    self.BluetoothThread.beep()
                    time.sleep(0.5)
                    self.BluetoothThread.beep()
                    return

                elif(pen_x < self.VPCoord_Curve[2] and pen_y < self.VPCoord_Curve[3] and lifted==True):
                    print("Bezier Curve")
                    self.usingVP = True
                    self.usingVP_Curve = True
                    self.vpShapePointList = []
                    self.vpPointCount = 0
                    self.BluetoothThread.beep()
                    time.sleep(0.5)
                    self.BluetoothThread.beep()
                    return
                
                elif(pen_x < self.VPCoord_Perspect[2] and pen_y < self.VPCoord_Perspect[3] and lifted==True):
                    print("Perspective Drawing")
                    self.usingVP = True
                    self.usingVP_Perspect = True
                    self.usingVP_VPoint= True 
                    self.vpShapePointList = []
                    self.vpPointCount = 0
                    self.BluetoothThread.beep()
                    time.sleep(0.5)
                    self.BluetoothThread.beep()
                    return
                    
                elif(pen_x < self.VPCoord_Ruler[2] and pen_y < self.VPCoord_Ruler[3] and lifted==True):
                    print("Ruler Mode")
                    self.usingVP = True
                    self.vpShapePointList = []
                    self.vpPointCount = 0
                    self.lastObject = self.currObject
                    self.currObject = DistMeasurement()
                    self.usingVP_Ruler = True
                    self.BluetoothThread.beep()
                    time.sleep(0.5)
                    self.BluetoothThread.beep()
                    return
                
                elif(pen_x < self.VPCoord_Alignment[2] and pen_y < self.VPCoord_Alignment[3] and lifted==True):
                    print("Alignment enabled")
                    self.turn_on_constraint(self.CONSTRAINT_ALIGNMENT)
                    self.alignmentCenter = None
                    self.alignmentUL = None
                    self.BluetoothThread.beep()
                    time.sleep(0.5)
                    self.BluetoothThread.beep()
                    return
                
                elif(pen_x < self.VPCoord_Distance[2] and pen_y < self.VPCoord_Distance[3] and lifted==True):
                    print("Distance enabled; Please use ruler to set distance")
                    self.turn_on_constraint(self.CONSTRAINT_DIST)
                    self.dist = None
                    self.BluetoothThread.beep()
                    time.sleep(0.5)
                    self.BluetoothThread.beep()
                    return
                
                elif(pen_x < self.VPCoord_Concentric[2] and pen_y < self.VPCoord_Concentric[3] and lifted==True):
                    print("Concentric enabled")
                    self.turn_on_constraint(self.CONSTRAINT_CONCENTRIC)
                    self.concen = None
                    self.BluetoothThread.beep()
                    time.sleep(0.5)
                    self.BluetoothThread.beep()
                    return
            
                elif(pen_x < self.VPCoord_Parallel[2] and pen_y < self.VPCoord_Parallel[3] and lifted==True):
                    print("Parallel enabled")
                    self.turn_on_constraint(self.CONSTRAINT_PARALLEL)          
                    self.BluetoothThread.beep()
                    time.sleep(0.5)
                    self.BluetoothThread.beep()
                    return
                
                elif(pen_x < self.VPCoord_Perpendicular[2] and pen_y < self.VPCoord_Perpendicular[3] and lifted==True):
                    print("Perpendicular enabled")
                    self.turn_on_constraint(self.CONSTRAINT_PERP)                    
                    self.BluetoothThread.beep()
                    time.sleep(0.5)
                    self.BluetoothThread.beep()
                    return
                
                # Copy and Paste condition is currently not used. Put them in the end.
                #elif(pen_x < self.VPCoord_Perspect[2] and pen_y < self.VPCoord_Perspect[3] and lifted==True):
                    #print("Ready to choose vanishing point")
                    ## Upon user's every new click to start the copy, clear the previous list of points first
                    #if(self.usingVP_Copy is False):
                        #self.vpCopyPointList = []
                    ## First click: start copying; second click: stop copying
                    #self.usingVP = not self.usingVP
                    #self.usingVP_Copy = not self.usingVP_Copy
                    #return
                
                
                #elif(pen_x < self.VPCoord_Paste[2] and pen_y < self.VPCoord_Paste[3] and lifted==True):
                    #print("Ready to paste")
                    #self.usingVP = True
                    #self.usingVP_Paste = True
                    ## return to prevent going further down
                    #return
                
                
            
            # State 2-a: Draw a circle/ellipse using VP function
            if(self.usingVP_Circle is True and self.usingVP_Perspect is False):
                print(self.vpPointCount)
                # if the pen is lifted off the paper, append the last new point to the list
                if(lifted==True and self.vpPointCount < 2 and not(penDataList[0] < self.VPCoord_Start[0] and penDataList[1] < self.VPCoord_Start[1])):
                    self.vpPointCount += 1
                    print("Adding points to the list")
                    self.vpShapePointList.append(penDataList[0])
                    self.vpShapePointList.append(penDataList[1])
                    self.BluetoothThread.beep()

                    # adjust based on relations
                    if (self.vpPointCount == 1):
                        self.currObject.center_x = self.vpShapePointList[0]
                        self.currObject.center_y = self.vpShapePointList[1]
                        if self.constraintAlignment_enabled is True:
                            print("applying alignment constraint on center;")
                            print("old x: " + str(self.currObject.center_x) + ", old y: " + str(self.currObject.center_y))
                            self.alignmentCenter = Alignment()
                            self.alignmentCenter.align_center(self.currObject, self.circList, self.rectList)
                            print("new x: " + str(self.currObject.center_x) + ", new y: " + str(self.currObject.center_y))
                            print("delta x: " + str(self.alignmentCenter.delta_x)  + ", delta y: " + str(self.alignmentCenter.delta_y))
                        elif self.constraintDist_enabled is True:
                            print("applying distance constraint;")
                            print("old x: " + str(self.currObject.center_x) + ", old y: " + str(self.currObject.center_y))
                            self.dist = Distance()
                            self.dist.fix_distance(self.currObject, self.lastObject, self.distMeasurementList)
                            print("new x: " + str(self.currObject.center_x) + ", new y: " + str(self.currObject.center_y))
                            print("delta x: " + str(self.dist.delta_x)  + ", delta y: " + str(self.dist.delta_y))
                        elif self.constraintConcentric_enabled is True:
                            print("applying concentric constraint;")
                            print("old x: " + str(self.currObject.center_x) + ", old y: " + str(self.currObject.center_y))
                            self.concen = Concentric()
                            self.concen.make_concentric(self.currObject, self.circList)
                            print("new x: " + str(self.currObject.center_x) + ", new y: " + str(self.currObject.center_y))
                            print("delta x: " + str(self.concen.delta_x)  + ", delta y: " + str(self.concen.delta_y))

                    elif(self.vpPointCount >= 2):
                        print("drawing the circle")
                        radius = math.sqrt(math.pow(self.currObject.center_x-self.vpShapePointList[2], 2) + math.pow(self.currObject.center_y-self.vpShapePointList[3], 2))
                        self.currObject.radius = radius
                        self.__paintBoard.paintEllipse(self.currObject.center_x, self.currObject.center_y, radius, radius)
                        # draw auxiliary lines
                        if (self.constraintAlignment_enabled is True) and (self.alignmentCenter.delta_x > 0 or self.alignmentCenter.delta_y > 0):
                            print("drawing aux line for alignment of center")
                            self.__paintBoard.paintAuxLine(self.alignmentCenter.init_x, self.alignmentCenter.init_y, self.currObject.center_x, self.currObject.center_y)
                        if (self.constraintConcentric_enabled is True) and (self.concen.delta_x > 0 or self.concen.delta_y > 0):
                            print("drawing aux line for concentric on center")
                            self.__paintBoard.paintAuxLine(self.concen.init_x, self.concen.init_y, self.currObject.center_x, self.currObject.center_y)
                        if (self.constraintDist_enabled is True) and (self.dist.delta_x > 0 or self.dist.delta_y > 0):
                            print("drawing aux line for fix distance at center")
                            self.__paintBoard.paintAuxLine(self.dist.init_x, self.dist.init_y, self.currObject.center_x, self.currObject.center_y)
                        # store parameterized circle here
                        self.circList.append(self.currObject)
                        # clear the flags and points data to go back to State 1
                        self.vpShapePointList = []
                        self.vpPointCount = 0
                        self.alignmentCenter = None
                        self.alignmentUL = None
                        self.usingVP = False
                        self.usingVP_Circle = False
                        self.turn_on_constraint(self.CONSTRAINT_ALIGNMENT)
                        return
                    
                    
            # State 2-b: Draw a rectangle using VP function
            elif(self.usingVP_Rect is True and self.usingVP_Perspect is False):
                print(self.vpPointCount)
                # if the pen is lifted off the paper, append the last new point to the list
                if(lifted==True and self.vpPointCount < 2 and not(penDataList[0] < self.VPCoord_Start[0] and penDataList[1] < self.VPCoord_Start[1])):
                    self.vpPointCount += 1
                    print("Adding points to the list")
                    self.vpShapePointList.append(penDataList[0])
                    self.vpShapePointList.append(penDataList[1])
                    self.BluetoothThread.beep()

                    if (self.vpPointCount == 1):
                        self.currObject.center_x = self.vpShapePointList[0]
                        self.currObject.center_y = self.vpShapePointList[1]
                        # adjust based on relations
                        if self.constraintDist_enabled is True:
                            print("applying distance constraint;")
                            print("old x: " + str(self.currObject.center_x) + ", old y: " + str(self.currObject.center_y))
                            self.dist = Distance()
                            self.dist.fix_distance(self.currObject, self.lastObject, self.distMeasurementList)
                            print("new x: " + str(self.currObject.center_x) + ", new y: " + str(self.currObject.center_y))
                            print("delta x: " + str(self.dist.delta_x)  + ", delta y: " + str(self.dist.delta_y))
                        elif self.constraintAlignment_enabled is True:
                            print("applying alignment constraint on center;")
                            print("old x: " + str(self.currObject.center_x) + ", old y: " + str(self.currObject.center_y))
                            self.alignmentCenter = Alignment()
                            self.alignmentCenter.align_center(self.currObject, self.circList, self.rectList)
                            print("new x: " + str(self.currObject.center_x) + ", new y: " + str(self.currObject.center_y))
                            print("delta x: " + str(self.alignmentCenter.delta_x)  + ", delta y: " + str(self.alignmentCenter.delta_y))

                    elif(self.vpPointCount >= 2):
                        # adjust based on relations
                        if self.vpPointCount == 2 and self.constraintAlignment_enabled is True:
                            self.currObject.set_upper_left_coord(self.vpShapePointList[2], self.vpShapePointList[3])
                            print("applying alignment constraint on UL corner")
                            print("old x: " + str(self.currObject.upperleft_x) + ", old y: " + str(self.currObject.upperleft_y))
                            self.alignmentUL = Alignment()
                            self.alignmentUL.align_corner(self.currObject, self.circList, self.rectList)
                            print("new x: " + str(self.currObject.upperleft_x) + ", new y: " + str(self.currObject.upperleft_y))
                            print("delta x: " + str(self.alignmentUL.delta_x)  + ", delta y: " + str(self.alignmentUL.delta_y))
                        print("drawing the rect")
                        self.__paintBoard.paintRect(self.currObject.center_x, self.currObject.center_y, self.currObject.upperleft_x, self.currObject.upperleft_y)
                        # draw auxiliary lines
                        if (self.constraintAlignment_enabled is True) and (self.alignmentCenter is not None) and (self.alignmentCenter.delta_x > 0 or self.alignmentCenter.delta_y > 0):
                            print("drawing aux line for center")
                            self.__paintBoard.paintAuxLine(self.alignmentCenter.init_x, self.alignmentCenter.init_y, self.currObject.center_x, self.currObject.center_y)
                        if (self.constraintAlignment_enabled is True) and (self.alignmentUL is not None) and (self.alignmentUL.delta_x > 0 or self.alignmentUL.delta_y > 0):
                            print("drawing aux line for UL corner")
                            self.__paintBoard.paintAuxLine(self.alignmentUL.init_x, self.alignmentUL.init_y, self.currObject.upperleft_x, self.currObject.upperleft_y)
                        if (self.constraintDist_enabled is True) and (self.dist.delta_x > 0 or self.dist.delta_y > 0):
                            print("drawing aux line for fix distance at center")
                            self.__paintBoard.paintAuxLine(self.dist.init_x, self.dist.init_y, self.currObject.center_x, self.currObject.center_y)
                        # store parameterized rectangle here
                        self.rectList.append(self.currObject)
                        # Emit the signal to the control thread, sending the 2 endpoints, current coordinates and force
                        controlRectList = self.vpShapePointList + penDataList
                        self.controlRectSignal.emit(controlRectList)
                        # clear the flags and points data to go back to State 1
                        #self.ControlThread.controlStartDrawRect()
                        self.vpPointCount = 0
                        self.alignmentCenter = None
                        self.alignmentUL = None
                        self.usingVP = False
                        self.usingVP_Rect = False
                        self.turn_on_constraint(self.CONSTRAINT_ALIGNMENT)
                        return
                    
            
            # The state to draw a perspective rectangle, still in progress
            # State 2-b-p: Draw a rectangle using VP function in perspective mode
            elif(self.usingVP_Rect is True and self.usingVP_Perspect is True):
                print(self.vpPointCount)
                # if the pen is lifted off the paper, append the last new point to the list
                if(lifted==True and self.vpPointCount < 2 and not(penDataList[0] < self.VPCoord_Start[0] and penDataList[1] < self.VPCoord_Start[1])):
                    self.vpPointCount += 1
                    print("Adding points to the list")
                    self.vpShapePointList.append(penDataList[0])
                    self.vpShapePointList.append(penDataList[1])
                    self.BluetoothThread.beep()
                    
                if(self.vpPointCount >= 2):
                    print("drawing the rect in perspective")
                    print("the perspective coord is",self.vpVpoint)
                    
                    
                    #defining the orthogonal lines
                    ## line equation is y=ax+b a=
                    firstPoint  =   [self.vpShapePointList[2], self.vpShapePointList[3]]
                    secondPoint =   [self.vpShapePointList[2],self.vpShapePointList[3]+2*abs(self.vpShapePointList[3]-self.vpShapePointList[1])]
                    slop2       =   (self.vpVpoint[1]-secondPoint[1])/(self.vpVpoint[0]-secondPoint[0])
                    y3rd        =   slop2*(2*abs(self.vpShapePointList[2]-self.vpShapePointList[0]))+secondPoint[1]
                    slop1       =   (self.vpVpoint[1]-firstPoint[1])/(self.vpVpoint[0]-firstPoint[0])
                    y4th        =   slop1*(2*abs(self.vpShapePointList[2]-self.vpShapePointList[0]))+firstPoint[1]
                    thirdPoint  =   [self.vpShapePointList[2]+2*abs(self.vpShapePointList[2]-self.vpShapePointList[0]),y3rd]
                    fourthPoint =   [self.vpShapePointList[2]+2*abs(self.vpShapePointList[2]-self.vpShapePointList[0]),y4th]
                    
                    self.__paintBoard.paintPolyg(firstPoint[0],firstPoint[1],secondPoint[0],secondPoint[1],thirdPoint[0],thirdPoint[1],fourthPoint[0],fourthPoint[1])
                    # Emit the signal to the control thread, sending the 2 endpoints, current coordinates and force
                    controlRectPList = [firstPoint[0],firstPoint[1],secondPoint[0],secondPoint[1],thirdPoint[0],thirdPoint[1],fourthPoint[0],fourthPoint[1]]
                    self.controlRectPSignal.emit(controlRectPList)
                    # clear the flags and points data to go back to State 1
                    #self.ControlThread.controlStartDrawRectP()
                    self.vpPointCount = 0
                    self.usingVP = False
                    self.usingVP_Rect = False
                    self.usingVP_Perspect=False
                    return
                    
                    
            # State 2-c: Draw a triangle using VP function
            elif(self.usingVP_Tri is True and self.usingVP_Perspect is False):
                print(self.vpPointCount)
                # if the pen is lifted off the paper, append the last new point to the list
                if(lifted==True and self.vpPointCount < 3 and  not(penDataList[0] < self.VPCoord_Start[0] and penDataList[1] < self.VPCoord_Start[1])):
                    self.vpPointCount += 1
                    print("Adding points to the list")
                    self.vpShapePointList.append(penDataList[0])
                    self.vpShapePointList.append(penDataList[1])
                    self.BluetoothThread.beep()
                    
                if(self.vpPointCount >= 3):
                    print("drawing the tri")
                    points = QPolygon([
                        QPoint(self.vpShapePointList[0], self.vpShapePointList[1]),
                        QPoint(self.vpShapePointList[2], self.vpShapePointList[3]),
                        QPoint(self.vpShapePointList[4], self.vpShapePointList[5])]
                    )   
                    self.__paintBoard.paintTriangle(points)
                    # store parameterized triangle here
                    self.currObject.x_0 = self.vpShapePointList[0]
                    self.currObject.y_0 = self.vpShapePointList[1]
                    self.currObject.x_1 = self.vpShapePointList[2]
                    self.currObject.y_1 = self.vpShapePointList[3]
                    self.currObject.x_2 = self.vpShapePointList[4]
                    self.currObject.y_2 = self.vpShapePointList[5]
                    self.triList.append(self.currObject)
                    # clear the flags and points data to go back to State 1
                    controlTriList = [self.vpShapePointList[0], self.vpShapePointList[1],self.vpShapePointList[2], self.vpShapePointList[3],self.vpShapePointList[4], self.vpShapePointList[5]]
                    self.controlTriSignal.emit(controlTriList)
                    #self.ControlThread.ControlStartDrawTri()
                    self.vpShapePointList = []
                    self.vpPointCount = 0
                    self.alignmentCenter = None
                    self.alignmentUL = None
                    self.usingVP = False
                    self.usingVP_Tri = False
                    return
                    
                    
            # State 2-d: Draw a line using VP function
            elif(self.usingVP_Line is True and self.usingVP_Perspect is False):
                print(self.vpPointCount)
                # if the pen is lifted off the papert and is outside of the virtual pallet, append the last new point to the list
                if(lifted==True and self.vpPointCount < 2 and not(penDataList[0] < self.VPCoord_Start[0] and penDataList[1] < self.VPCoord_Start[1])):#
                    self.vpPointCount += 1
                    print("Adding points to the list")
                    self.vpShapePointList.append(penDataList[0])
                    self.vpShapePointList.append(penDataList[1])
                    self.BluetoothThread.beep()
                    
                    if(self.vpPointCount >= 2):
                        print("drawing the line")
                        # store parameterized line here
                        self.currObject.set_coords(self.vpShapePointList[0], self.vpShapePointList[1], self.vpShapePointList[2], self.vpShapePointList[3])
                        # adjust based on relations
                        if self.vpPointCount == 2:
                            if self.constraintParallel_enabled is True:
                                print("applying parallel constraint on the second point")
                                print("old x_1: " + str(self.currObject.x_1) + ", old y_1: " + str(self.currObject.y_1))
                                self.para = Parallel()
                                self.para.make_para(self.currObject, self.lineList)
                                print("new x_1: " + str(self.currObject.x_1) + ", new y_1: " + str(self.currObject.y_1))
                            elif self.constraintPerpendicular_enabled is True:
                                print("applying perpendicular constraint on the second point")
                                print("old x_1: " + str(self.currObject.x_1) + ", old y_1: " + str(self.currObject.y_1))
                                self.perp = Perpendicular()
                                self.perp.make_perp(self.currObject, self.lineList)
                                print("new x_1: " + str(self.currObject.x_1) + ", new y_1: " + str(self.currObject.y_1))
                        self.lineList.append(self.currObject)
                        # draw the line
                        if(len(self.vpShapePointList)>=4):
                            self.__paintBoard.paintLine(self.currObject.x_0, self.currObject.y_0, self.currObject.x_1, self.currObject.y_1)
                        # draw auxiliary lines
                        if (self.constraintParallel_enabled is True) or (self.constraintPerpendicular_enabled is True):
                            print("drawing aux arc")
                            if (self.constraintParallel_enabled is True):
                                self.__paintBoard.paintAuxArc(self.currObject.x_0, self.currObject.y_0, self.para.init_x, self.para.init_y, self.currObject.x_1, self.currObject.y_1) 
                            else:
                                self.__paintBoard.paintAuxArc(self.currObject.x_0, self.currObject.y_0, self.perp.init_x, self.perp.init_y, self.currObject.x_1, self.currObject.y_1) 
                        # Emit the signal to the control thread, sending the 2 endpoints, current coordinates and force
                        controlLineList = self.vpShapePointList + penDataList
                        self.controlLineSignal.emit(controlLineList)
                    
                        # clear the flags and points data to go back to State 1
                        # self.vpShapePointList = []
                        #self.ControlThread.controlStartDrawLine()
                        self.vpPointCount = 0
                        self.vpShapePointList = []
                        self.alignmentCenter = None
                        self.alignmentUL = None
                        self.usingVP = False
                        self.usingVP_Line = False
                        self.usingMotor = True
                        self.usingMotor_Line = True
                        self.turn_on_constraint(self.CONSTRAINT_ALIGNMENT)
                        return
                    
                    
            # State 2-e: Draw an arc using VP function
            elif(self.usingVP_Arc is True and self.usingVP_Perspect is False):
                print(self.vpPointCount)
                # if the pen is lifted off the paper, append the last new point to the list
                if(lifted==True and self.vpPointCount < 3 and  not(penDataList[0] < self.VPCoord_Start[0] and penDataList[1] < self.VPCoord_Start[1])):
                    self.vpPointCount += 1
                    print("Adding points to the list")
                    self.vpShapePointList.append(penDataList[0])
                    self.vpShapePointList.append(penDataList[1])
                    self.BluetoothThread.beep()

                    if self.vpPointCount == 1:
                        self.currObject.set_center(self.vpShapePointList[0], self.vpShapePointList[1])
                        if self.constraintAlignment_enabled is True:
                            print("applying alignment constraint on center;")
                            print("old x: " + str(self.currObject.center_x) + ", old y: " + str(self.currObject.center_y))
                            self.alignmentCenter = Alignment()
                            self.alignmentCenter.align_center(self.currObject, self.circList, self.rectList)
                            print("new x: " + str(self.currObject.center_x) + ", new y: " + str(self.currObject.center_y))
                            print("delta x: " + str(self.alignmentCenter.delta_x)  + ", delta y: " + str(self.alignmentCenter.delta_y))
                        elif self.constraintDist_enabled is True:
                            print("applying distance constraint;")
                            print("old x: " + str(self.currObject.center_x) + ", old y: " + str(self.currObject.center_y))
                            self.dist = Distance()
                            self.dist.fix_distance(self.currObject, self.lastObject, self.distMeasurementList)
                            print("new x: " + str(self.currObject.center_x) + ", new y: " + str(self.currObject.center_y))
                            print("delta x: " + str(self.dist.delta_x)  + ", delta y: " + str(self.dist.delta_y))
                        elif self.constraintConcentric_enabled is True:
                            print("applying concentric constraint;")
                            print("old x: " + str(self.currObject.center_x) + ", old y: " + str(self.currObject.center_y))
                            self.concen = Concentric()
                            self.concen.make_concentric(self.currObject, self.circList)
                            print("new x: " + str(self.currObject.center_x) + ", new y: " + str(self.currObject.center_y))
                            print("delta x: " + str(self.concen.delta_x)  + ", delta y: " + str(self.concen.delta_y))

                    elif(self.vpPointCount >= 3):
                        # draw auxiliary lines
                        if (self.constraintAlignment_enabled is True) and (self.alignmentCenter.delta_x > 0 or self.alignmentCenter.delta_y > 0):
                            print("drawing aux line for alignment of center")
                            self.__paintBoard.paintAuxLine(self.alignmentCenter.init_x, self.alignmentCenter.init_y, self.currObject.center_x, self.currObject.center_y)
                        if (self.constraintConcentric_enabled is True) and (self.concen.delta_x > 0 or self.concen.delta_y > 0):
                            print("drawing aux line for concentric on center")
                            self.__paintBoard.paintAuxLine(self.concen.init_x, self.concen.init_y, self.currObject.center_x, self.currObject.center_y)
                        if (self.constraintDist_enabled is True) and (self.dist.delta_x > 0 or self.dist.delta_y > 0):
                            print("drawing aux line for fix distance at center")
                            self.__paintBoard.paintAuxLine(self.dist.init_x, self.dist.init_y, self.currObject.center_x, self.currObject.center_y)
                        # store parameterized arc here
                        self.currObject.set_start(self.vpShapePointList[2], self.vpShapePointList[3])
                        self.currObject.set_end(self.vpShapePointList[4], self.vpShapePointList[5])
                        self.circList.append(self.currObject)
                        print("drawing the arc")
                        self.__paintBoard.paintArc(self.currObject.center_x, self.currObject.center_y, self.currObject.start_x, self.currObject.start_y, self.currObject.end_x, self.currObject.end_y)
                        # clear the flags and points data to go back to State 1
                        self.vpShapePointList = []
                        self.vpPointCount = 0
                        self.alignmentCenter = None
                        self.alignmentUL = None
                        self.usingVP = False
                        self.usingVP_Arc = False
                        self.turn_on_constraint(self.CONSTRAINT_ALIGNMENT)
                        return
                    
                    
            # State 2-f: Draw an Bezier curve using VP function
            elif(self.usingVP_Curve is True and self.usingVP_Perspect is False):
                print(self.vpPointCount)
                # if the pen is lifted off the paper, append the last new point to the list
                if(lifted==True and self.vpPointCount < 4 and  not(penDataList[0] < self.VPCoord_Start[0] and penDataList[1] < self.VPCoord_Start[1])):
                    self.vpPointCount += 1
                    print("Adding points to the list")
                    self.vpShapePointList.append(penDataList[0])
                    self.vpShapePointList.append(penDataList[1])
                    self.BluetoothThread.beep()
                    
                if(self.vpPointCount == 4):
                    print("drawing the Bezier curve")
                    pointListX = [self.vpShapePointList[0], self.vpShapePointList[2], self.vpShapePointList[4], self.vpShapePointList[6]]
                    pointListY = [self.vpShapePointList[1], self.vpShapePointList[3], self.vpShapePointList[5], self.vpShapePointList[7]]
                    self.__paintBoard.paintBezierSpline(pointListX, pointListY)

                    # clear the flags and points data to go back to State 1
                    self.vpShapePointList = []
                    self.vpPointCount = 0
                    self.usingVP = False
                    self.usingVP_Curve = False
                    return
                    
             # State 2-g: Defining the vanishing point
            elif(self.usingVP_VPoint is True):
                print(self.vpPointCount)
                # if the pen is lifted off the paper, append the last new point to the list
                if(lifted==True and self.vpPointCount < 2 and not(penDataList[0] < self.VPCoord_Start[0] and penDataList[1] < self.VPCoord_Start[1])):
                    self.vpPointCount += 1
                    print("Adding points to the list")
                    self.vpShapePointList.append(penDataList[0])
                    self.vpShapePointList.append(penDataList[1])
                    self.BluetoothThread.beep()
                    
                if(self.vpPointCount == 1):
                    print("Vanishing point is set")
                    self.__paintBoard.paintEllipse(self.vpShapePointList[0], self.vpShapePointList[1], 2, 2)
                    # clear the flags and points data to go back to State 1
                    self.vpVpoint= [self.vpShapePointList[0],self.vpShapePointList[1]]
                    self.vpShapePointList = []
                    self.vpPointCount = 0
                    self.usingVP = False
                    self.usingVP_VPoint = False
                    return                   
           
            # State 2-h: Ruler Mode using VP function
            elif(self.usingVP_Ruler is True):
                print(self.vpPointCount)
                # if the pen is lifted off the paper, and is inside the virtual ruler space, append the last new point to the list
                if lifted==True and self.vpPointCount < 1 and penDataList[0]<self.VRCoord[2] and penDataList[1]<self.VRCoord[3]:#
                    self.vpPointCount += 1
                    print("Adding points to the list")
                    self.vpShapePointList.append(penDataList[0])
                    self.vpShapePointList.append(penDataList[1])
                    self.BluetoothThread.beep()
                    
                    if(self.vpPointCount >= 1):
                        print("Ruler mode activated")

                        # store parameterized DistMeasurement here
                        self.currObject.set_dist(self.vpShapePointList[0] - self.VRCoord[0])
                        print("distance set to: " + str(self.currObject.dist))
                        self.distMeasurementList.append(self.currObject)

                        # Emit the signal to the control thread, sending the 2 endpoints, current coordinates and force
                        controlLineList = self.vpShapePointList + penDataList
                        self.controlLineSignal.emit(controlLineList)
                    
                        # clear the flags and points data to go back to State 1
                        # self.vpShapePointList = []
                        #self.ControlThread.controlStartRuler()
                        self.vpPointCount = 0
                        self.vpShapePointList = []
                        self.usingVP = False
                        self.usingVP_Line = False
                        return
                    
                    
            # State 2-g: Copy a list of points of the shape being drawn by the user
            elif(self.usingVP_Copy is True and self.usingVP_Perspect is False):
                # even index for x, odd index for y
                self.vpShapePointList.append(penDataList[0])
                self.vpShapePointList.append(penDataList[1])
                return
                    
            # State 2-h: Paste a list of points of the shape drawn by the user
            elif(self.usingVP_Paste is True and self.usingVP_Perspect is False):
                # even index for x, odd index for y
                if(lifted==True and self.vpPointCount < 4):
                    self.vpPointCount += 1
                    print("Adding points to the list")
                    self.vpShapePointList.append(penDataList[0])
                    self.vpShapePointList.append(penDataList[1])
                # iterate through the point list and draw the points on the canvas, starting from the new point the user clicked
                while(i < len(self.vpShapePointList)/2):
                    coord = [self.penCoordinates[i]-firstX+currentX, self.penCoordinates[i+1]-firstY+currentY]
                    self.__paintBoard.penMoveEvent(coord, 0)
                    i += 2
                    
                self.usingVP = False
                self.usingVP_Paste = False
                return
                
            # State 2-i: Choosing a vanishing point on the paper. Must be put lastly in the if/else list
            elif(self.usingVP_Perspect is True):
                # even index for x, odd index for y
                if(lifted==True and self.vpPointCount < 1 and  not(penDataList[0] < self.VPCoord_Start[0] and penDataList[1] < self.VPCoord_Start[1])):
                    self.vpPointCount += 1
                    print("Storing vanishing point")
                    self.vpVanishingPoint.append(penDataList[0])
                    self.vpVanishingPoint.append(penDataList[1])
                    
                if(self.vpPointCount >= 1):
                    print("finished storing the vanishing point")
                    # clear the flags and points data to go back to State 1
                    self.vpPointCount = 0
                    return
            
            
                '''
                elif(pen_x < self.VPCoord_Arc[2] and pen_y < self.VPCoord_Arc[3]):
                    print("Arc")
                    self.usingVP = True
                    self.on_cbtn_DrawArc_clicked()
                elif(pen_x < self.VPCoord_BezierSpline[2] and pen_y < self.VPCoord_BezierSpline[3]):
                    print("BezierSpline")
                    self.usingVP = True
                    self.on_cbtn_DrawBezierSpline_clicked()
                '''
                
                #self.__paintBoard.penVPEvent(self.penCoordinates, self.penPressure)
            
            
            #state 3-d: Using the motor to draw a line with the start/end points obtained in state 2 
            #if(self.usingMotor is True and self.usingMotor_Line is True):
                ##Emit the signal to the control thread, sending the 2 endpoints, current coordinates and force
                ##controlLineList = self.vpShapePointList + penDataList
                ##self.controlLineSignal.emit(controlLineList)
                #diffX = self.vpShapePointList[0] - penDataList[0]
                #diffY = self.vpShapePointList[1] - penDataList[1]
                #print("in state 3-d")
                
                ## show the real time drawing of the motor
                #self.penCoordinates[0] = penDataList[0]
                #self.penCoordinates[1] = penDataList[1]
                #self.penPressure = penDataList[2]
                #self.__paintBoard.penMoveEvent(self.penCoordinates, self.penPressure, self.liftedDeque)
                
                #if(abs(diffX) + abs(diffY) < 40):
                    #self.vpShapePointList = []
                    #self.usingVP = False
                    #self.usingVP_Line = False
                    #self.usingMotor = False
                    #self.usingMotor_Line = True
                    #self.ControlThread.controlStopDrawLine()
                    
                #return
                

    def Quit(self):
        self.close()



# A dialog class asking for CAD drawing parameters
class Dialog(QDialog):

    answer_dict = {}    # answer_dict is a bunch of QLabels to store user inputs
    edit_dict = {}      # edit_dict is a bunch of QLineEdits associate user input numbers to field names 

    # Use a list to store the questions and answer names
    def __init__(self, fieldList, parent=None):
        super(Dialog, self).__init__(parent)

        # Layout and spacing
        grid = QtGui.QGridLayout()
        grid.setSpacing(20)
        
        for x in range(len(fieldList)):
            # initialize the answer dictionary to store answers/inputs from the user
            self.answer_dict[x] = QtGui.QLabel()
            # initialize the edit dictionary to associate variable value changes to edit changes  
            self.edit_dict[x] = QtGui.QLineEdit()
            self.edit_dict[x].textChanged.connect(getattr(self, 'q'+str(x)+'Changed'))

            # Add the dialog label and corresponding input boxes
            grid.addWidget(QtGui.QLabel(fieldList[x]), x, 0)
            grid.addWidget(self.edit_dict[x], x, 1)
            
        # Hit apply button to confirm inputs
        applyBtn = QtGui.QPushButton('Apply', self)
        applyBtn.clicked.connect(self.close)

        grid.addWidget(applyBtn,3,2)
        self.setLayout(grid)
        self.setGeometry(300, 300, 350, 300)

    # Associated functions to be called when user edits/enters the inputs
    def q0Changed(self, text):
        self.answer_dict[0].setText(text)

    def q1Changed(self, text):
        self.answer_dict[1].setText(text)

    def q2Changed(self, text):
        self.answer_dict[2].setText(text)

    def q3Changed(self, text):
        self.answer_dict[3].setText(text)

    def returnAnswers(self):
        answer_texts = []
        for x in range(len(self.answer_dict)):
            answer_texts.append(self.answer_dict[x].text())

        print(answer_texts[0])
        return answer_texts

    # Return user inputs as a list
    @staticmethod
    def getData(fieldList, parent=None):
        dialog = Dialog(fieldList)
        dialog.exec_()
        return dialog.returnAnswers()
