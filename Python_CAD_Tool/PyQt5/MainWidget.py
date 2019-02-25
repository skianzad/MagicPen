# -*- coding: utf-8 -*-
'''
Created on 2019-01-01

@author: Yuxiang
'''
from PyQt5 import QtWidgets
from PyQt5.Qt import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PaintBoard import PaintBoard
from WiFi import WiFiThread


class MainWidget(QWidget):

    # Define virtual panel coordinates for different shapes/regions
    VPCoord_Start   =   [316, 332]           #LeftTopX, Y
    VPCoord_Circle  =   [316, 332, 336, 363] #LeftTopX, Y, RightBotX, Y 
    VPCoord_Rect    =   [336, 332, 356, 363] #LeftTopX, Y, RightBotX, Y    
    VPCoord_Tri     =   [316, 363, 336, 395] #LeftTopX, Y, RightBotX, Y 
    VPCoord_Line    =   [336, 363, 356, 395] #LeftTopX, Y, RightBotX, Y

    # A flag to check if the user is currently using the virtual panel
    usingVP = False

    def __init__(self, Parent=None):
        '''
                Constructor
        ''' 
        super().__init__(Parent)

        #The NeoSmartpen custom paper is 88.3 x 114.2 in raw coordinates
        rawLimitX = 88
        rawLimitY = 114
        multiplier = 4
        
        paintSizeX = rawLimitX * multiplier
        paintSizeY = rawLimitY * multiplier
        mainSizeX = paintSizeX + 30
        mainSizeY = paintSizeY + 170

        self.__InitData(paintSizeX, paintSizeY) #First initialize data, then initialize view/interface
        self.__InitView(mainSizeX, mainSizeY)
        self.__InitWiFi()

        
    def __InitWiFi(self):
        '''
                  initialize the tcp server
        '''
        self.WiFiThread = WiFiThread()
        self.WiFiThread.sigOut.connect(self.free_draw_updates)
        # self.WiFiThread.sigOut.connect(self.VP_draw_updates)
        self.WiFiThread.start()


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
        self.sub_layout_control.setSpacing(5)
        self.sub_layout_CAD.setSpacing(5)
        self.sub_layout_root.setContentsMargins(0, 0, 10, 0)
        
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
        self.__comboBox_penColor.currentIndexChanged.connect(self.on_PenColorChange) #Connect to function on_PenColorChange
        self.sub_layout_control.addWidget(self.__comboBox_penColor, 3, 1)


    # Initialize buttons for CAD functionalities
    def __init_CAD_buttons(self):
        self.__cbtn_DrawCircle = QPushButton("Circle")
        self.__cbtn_DrawCircle.setParent(self)
        self.__cbtn_DrawCircle.clicked.connect(self.on_cbtn_DrawCircle_clicked)
        self.sub_layout_CAD.addWidget(self.__cbtn_DrawCircle, 1, 0)

        self.__cbtn_DrawRect = QPushButton("Rectangle")
        self.__cbtn_DrawRect.setParent(self)
        self.__cbtn_DrawRect.clicked.connect(self.on_cbtn_DrawRect_clicked)
        self.sub_layout_CAD.addWidget(self.__cbtn_DrawRect, 1, 1)

        self.__cbtn_DrawTriangle = QPushButton("Triangle")
        self.__cbtn_DrawTriangle.setParent(self)
        self.__cbtn_DrawTriangle.clicked.connect(self.on_cbtn_DrawTriangle_clicked)
        self.sub_layout_CAD.addWidget(self.__cbtn_DrawTriangle, 2, 0)

        
        self.__cbtn_DrawTriangle = QPushButton("Arc")
        self.__cbtn_DrawTriangle.setParent(self)
        self.__cbtn_DrawTriangle.clicked.connect(self.on_cbtn_DrawTriangle_clicked)
        self.sub_layout_CAD.addWidget(self.__cbtn_DrawTriangle, 2, 1)

        self.__cbtn_DrawLine = QPushButton("Line")
        self.__cbtn_DrawLine.setParent(self)
        self.__cbtn_DrawLine.clicked.connect(self.on_cbtn_DrawLine_clicked)
        self.sub_layout_CAD.addWidget(self.__cbtn_DrawLine, 3, 0)

        self.__cbtn_DrawTriangle = QPushButton("Spline")
        self.__cbtn_DrawTriangle.setParent(self)
        self.__cbtn_DrawTriangle.clicked.connect(self.on_cbtn_DrawTriangle_clicked)
        self.sub_layout_CAD.addWidget(self.__cbtn_DrawTriangle, 3, 1)
        

    def __fillColorList(self, comboBox):

        index_black = 0
        index = 0
        for color in self.__colorList: 
            if color == "black":
                index_black = index
            index += 1
            pix = QPixmap(70,20)
            pix.fill(QColor(color))
            comboBox.addItem(QIcon(pix),None)
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


    '''
    def on_cbtn_DrawArc_clicked(self):
        painter = QPainter(self)
        window = Dialog(['center', 'upper left point'])
        data = window.getData(['center', 'upper left point'])
        center_x = int(data[0].split(',')[0])
        center_y = int(data[0].split(',')[1])
        upper_left_x = int(data[1].split(',')[0])
        upper_left_y = int(data[1].split(',')[1])
        self.__paintBoard.paintRect(center_x, center_y, upper_left_x, upper_left_y)

    def on_cbtn_DrawSpline_clicked(self):
        painter = QPainter(self)
        window = Dialog(['center', 'upper left point'])
        data = window.getData(['center', 'upper left point'])
        center_x = int(data[0].split(',')[0])
        center_y = int(data[0].split(',')[1])
        upper_left_x = int(data[1].split(',')[0])
        upper_left_y = int(data[1].split(',')[1])
        self.__paintBoard.paintRect(center_x, center_y, upper_left_x, upper_left_y)
    '''


    # Free drawing functionalities
    def free_draw_updates(self, penDataList):
        if penDataList is not None:
            # print(penDataList)
            if(penDataList[0] < self.VPCoord_Start[0] or penDataList[1] < self.VPCoord_Start[1]):
                self.penCoordinates[0] = penDataList[0]
                self.penCoordinates[1] = penDataList[1]
                self.penPressure = penDataList[2]
                self.__paintBoard.penMoveEvent(self.penCoordinates, self.penPressure)

            elif(penDataList[2] > 200 and self.usingVP is False):
                '''
                self.penCoordinates[0] = penDataList[0]
                self.penCoordinates[1] = penDataList[1]
                self.penPressure = penDataList[2]
                '''
                # print(penDataList)
                pen_x = penDataList[0]
                pen_y = penDataList[1]
                pen_pressure = penDataList[2]

                # Check which region the pen is in and prepare to draw shape accordingly
                if(pen_x < self.VPCoord_Circle[2] and pen_y < self.VPCoord_Circle[3]):
                    print("Circle")
                    self.usingVP = True
                    self.on_cbtn_DrawCircle_clicked()
                elif(pen_x < self.VPCoord_Rect[2] and pen_y < self.VPCoord_Rect[3]):
                    print("Rect")
                    self.usingVP = True
                    self.on_cbtn_DrawRect_clicked()
                elif(pen_x < self.VPCoord_Tri[2] and pen_y < self.VPCoord_Tri[3]):
                    print("Tri")
                    self.usingVP = True
                    self.on_cbtn_DrawTriangle_clicked()
                elif(pen_x < self.VPCoord_Line[2] and pen_y < self.VPCoord_Line[3]):
                    print("Line")
                    self.usingVP = True
                    self.on_cbtn_DrawLine_clicked()
                
                #self.__paintBoard.penVPEvent(self.penCoordinates, self.penPressure)


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
        grid = QtWidgets.QGridLayout()
        grid.setSpacing(20)
        
        for x in range(len(fieldList)):
            # initialize the answer dictionary to store answers/inputs from the user
            self.answer_dict[x] = QtWidgets.QLabel()
            # initialize the edit dictionary to associate variable value changes to edit changes  
            self.edit_dict[x] = QtWidgets.QLineEdit()
            self.edit_dict[x].textChanged.connect(getattr(self, 'q'+str(x)+'Changed'))

            # Add the dialog label and corresponding input boxes
            grid.addWidget(QtWidgets.QLabel(fieldList[x]), x, 0)
            grid.addWidget(self.edit_dict[x], x, 1)
            
        # Hit apply button to confirm inputs
        applyBtn = QtWidgets.QPushButton('Apply', self)
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
