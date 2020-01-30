#!/usr/bin/env python
from __future__ import print_function
import RPi.GPIO as GPIO
import socket
import time
import threading
import ctypes
# THE BNO055.
import logging
import math
import sys
from Adafruit_BNO055 import BNO055
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import numpy as np


class ControlThread(QThread):
        
        
        global activeControl
        activeControl   =       False
        fullDrive       =       False
        # Defining the hardware PWM
        global DIR2 
        DIR2            =       16
        global DIR1 
        DIR1            =       20
        global pwm_Pin1
        pwm_Pin1=1
        global pwm_Pin2
        pwm_Pin2=23
        pwmLib=ctypes.CDLL('libwiringPi.so')
        pwmLib.wiringPiSetup()
        pwmLib.pinMode(pwm_Pin1,2)
        pwmLib.pinMode(pwm_Pin2,2)
        pwmLib.pwmSetMode(0)
        #pwmLib.pwmSetRange(1024)
        pwmLib.pwmSetClock(2)
        pwmLib.pwmWrite(pwm_Pin1,0)
        pwmLib.pwmSetMode(0)
        pwmLib.pwmSetClock(2)
        pwmLib.pwmWrite(pwm_Pin2,0)


        GPIO.setmode(GPIO.BCM)
        TCP_IP =''
        TCP_PORT = 8080
        BUFFER_SIZE = 1024              # Normally 1024, but we want fast response

        # Set up GPIO pin numbers for different directions
        global UP 
        global DOWN 
        global LEFT 
        global RIGHT 
        global BUTTON 
        global contact
        global target
        target=[0,0]
        contact= False
        UP = 22
        DOWN = 23
        LEFT = 27
        RIGHT = 17
        BUTTON = 24
        SPI1 = 10
        SPI2 = 9
        SPI3 = 11

    
        GPIO.setup(UP,GPIO.IN)          
        GPIO.setup(DOWN,GPIO.IN)
        GPIO.setup(LEFT,GPIO.IN)
        GPIO.setup(RIGHT,GPIO.IN)
        GPIO.setup(BUTTON,GPIO.IN)

        GPIO.setup(DIR1, GPIO.OUT)
        GPIO.setup(DIR2, GPIO.OUT)
        GPIO.setup(8, GPIO.OUT)
        GPIO.output(8, 1)

        # create an object p for PWM on port 25 at 50 Hertz  

        # create x, y coordinates
        x = 0
        y = 0
        p = False
        size = 10000
        PWMDuty = 0
        global start_time
        start_time = time.time()
        
        # start and end coordinates of the shapes
        lineStartCoord = [0, 0]
        lineEndCoord = [0, 0]
        
        # coordinate anf force of the digital pen
        currPenCoord = [0, 0]
        currPenForce = 0

        #BNO055 initialization

        # Create and configure the BNO sensor connection.  Make sure only ONE of the
        # below 'bno = ...' lines is uncommented:
        # Raspberry Pi configuration with serial UART and RST connected to GPIO 4:
        bno = BNO055.BNO055(serial_port='/dev/serial0', rst=4) #setting the reset pin to PIN4
        # Enable verbose debug logging if -v is passed as a parameter.
        if len(sys.argv) == 2 and sys.argv[1].lower() == '-v':
            logging.basicConfig(level=logging.DEBUG)

        # Initialize the BNO055 and stop if something went wrong.
        if not bno.begin():
            raise RuntimeError('Failed to initialize BNO055! Is the sensor connected?')

        # Print system status and self test result.
        status, self_test, error = bno.get_system_status()
        print('System status: {0}'.format(status))
        print('Self test result (0x0F is normal): 0x{0:02X}'.format(self_test))
        # Print out an error if system status is in error mode.
        if status == 0x01:
            print('System error: {0}'.format(error))
            print('See datasheet section 4.3.59 for the meaning.')

        # Print BNO055 software revision and other diagnostic data.
        sw, bl, accel, mag, gyro = bno.get_revision()
        print('Software version:   {0}'.format(sw))
        print('Bootloader version: {0}'.format(bl))
        print('Accelerometer ID:   0x{0:02X}'.format(accel))
        print('Magnetometer ID:    0x{0:02X}'.format(mag))
        print('Gyroscope ID:       0x{0:02X}\n'.format(gyro))

        print('Reading BNO055 data, press Ctrl-C to quit...')
        heading0, roll0, pitch0 = bno.read_euler()
        def PointsInCircum(self,r,n,phi):
                return [(math.cos(2*math.pi/n*x+phi)*r,math.sin(2*math.pi/n*x+phi)*r) for x in range(0,n+1)]  # defining the points on the Circum of a circle
            
        def DriveControl(self):
                self.start_time = time.time()
                threading.Timer(0.01, self.DriveControl).start()
                #print('inside the thread',self.currPenCoord)
                if(self.activeControl==True):
                        offset=100
                        gain=500
                        distance=np.subtract(self.target,self.currPenCoord)
                        distance[0]=distance[0]*(math.cos(math.pi*((360+self.heading-self.heading0)%360)/180))+distance[1]*math.sin(math.pi*((360+self.heading-self.heading0)%360)/180)
                        distance[1]=distance[1]*(math.cos(math.pi*((360+self.heading-self.heading0)%360)/180))-distance[0]*math.sin(math.pi*((360+self.heading-self.heading0)%360)/180)

                        #print('control_loop', distance)
                        distancep=[self.target[0]-self.lineEndCoord[0]-self.x*1.7,self.target[1]-self.lineEndCoord[1]-self.y*1.55]
                        #print(distancep,self.x,self.y,self.lineEndCoord,self.target)
                        normV=np.linalg.norm(distancep,2)
                        if (normV==0):
                                normV=1000;
                        if(abs(distancep[0])>5 or (abs(distancep[1]>5))):
                                velocity=np.divide(distancep,normV)
                                velocity=np.divide(distance,normV)
                        else:
                                 normV=np.linalg.norm(distance,2)
                                 velocity=np.divide(distance,normV)
                        #print(velocity[0]*600,normV)
                        if(self.currPenForce>100):       #variable pressure gain
                                gain=500*abs((180-self.currPenForce))/80
                                self.x=0
                                self.y=0
                                self.lineEndCoord=self.currPenCoord
                                offset=0
                        else:
                                gain=500
                                offset=100
                                
                        #gain=400                #shared control acrivation 
                        
                        
                        if((abs(distance[0])>5 or abs(distance[1])>5)and self.currPenForce>10): #self.currPenForce>10 and
                                #print('inside control thread',self.currPenForce)
                                if (abs(distancep[0])>10 or abs(distancep[1])>10): # updating the starting point based on the current absolute position and running the controller again 
                                
                                        if (velocity[0]>0):#x direction control
                                                GPIO.output(DIR2,0)
                                                self.pwmLib.pwmWrite(pwm_Pin2,int(np.round(offset+100+velocity[0]*gain*1))) #going right
                                        else:
                                                GPIO.output(DIR2,1)
                                                self.pwmLib.pwmWrite(pwm_Pin2,int(np.round(offset+abs(velocity[0])*gain)))
                                                
                                        if (velocity[1]>0): #y direction control
                                                GPIO.output(DIR1,1)
                                                self.pwmLib.pwmWrite(pwm_Pin1,int(np.round(offset+velocity[1]*gain)))
                                        else: 
                                                GPIO.output(DIR1,0)
                                                self.pwmLib.pwmWrite(pwm_Pin1,int(np.round(offset+abs(velocity[1])*gain)))   #going up 
                                else:
                                        self.x=0
                                        self.y=0
                                        self.pwmLib.pwmWrite(pwm_Pin2,0)
                                        self.pwmLib.pwmWrite(pwm_Pin1,0)
                                        time.sleep(1)
                                        self.lineEndCoord=self.currPenCoord
                                        

                        
                        elif((abs(distance[0])<10 and abs(distance[1])<10)): # to make sure that we get to the absolute destination
                                self.pwmLib.pwmWrite(pwm_Pin2,0)
                                self.pwmLib.pwmWrite(pwm_Pin1,0)
                                self.activeControl=False
                                self.token='done'
                                print('done with drawing')
                                
                elif(self.fullDrive==True):
                        offset=100
                        gain=500
                        distance=np.subtract(self.target,self.currPenCoord)
                        self.RulerEnd   =       self.target
                        self.RulerStart =       self.currPenCoord
                        #distance[0]=distance[0]*(math.cos(math.pi*((360+self.heading-self.heading0)%360)/180))+distance[1]*math.sin(math.pi*((360+self.heading-self.heading0)%360)/180)
                        #distance[1]=distance[1]*(math.cos(math.pi*((360+self.heading-self.heading0)%360)/180))-distance[0]*math.sin(math.pi*((360+self.heading-self.heading0)%360)/180)
                        #print(distancep,self.x,self.y,self.lineEndCoord,self.target)
                        normV=np.linalg.norm(distance,2)
                        #print('distance',distance)
                        #print('self.target',self.target)
                        #print('self.current',self.currPenCoord)
                        if (normV==0):
                                normV=1000;
                        else:
                                normV=np.linalg.norm(distance,2)
                                velocity=np.divide(distance,normV)
                        #print('rect1',self.mode,distance,)

                        if ((self.mode=='Rect' or self.mode=='RectP') and self.state==2):
                                if(distance[1]>0):
                                        GPIO.output(DIR1,1)
                                        self.pwmLib.pwmWrite(pwm_Pin1,int(np.round(offset+300))) #going down
                                        
                                elif(distance[1]<-10):
                                        GPIO.output(DIR1,0)
                                        self.pwmLib.pwmWrite(pwm_Pin1,int(np.round(offset+400))) #going up
                                else:
                                        self.pwmLib.pwmWrite(pwm_Pin1,0)
                                        
                                if (self.currPenCoord[0]+self.x*1.7<self.target[0] and self.currPenForce>10):
                                        GPIO.output(DIR2,0)
                                        self.pwmLib.pwmWrite(pwm_Pin2,int(np.round(offset+400))) #pushing right
                                else:
                                        self.pwmLib.pwmWrite(pwm_Pin2,0)
                                        self.x=0
                                
                                if((abs(distance[0])<15 and (distance[1])<0)): # to make sure that we get to the absolute destination
                                        self.pwmLib.pwmWrite(pwm_Pin2,0)
                                        self.pwmLib.pwmWrite(pwm_Pin1,0)
                                        self.fullDrive=False
                                        print('done with state 1 rect drawing')
                                        
                        if ((self.mode=='Rect' or self.mode=='RectP') and self.state==3):
                                if(distance[0]>0):
                                        GPIO.output(DIR2,0)
                                        self.pwmLib.pwmWrite(pwm_Pin2,int(np.round(offset+400))) #going right
                                elif(distance[0]<-10):
                                        GPIO.output(DIR2,1)
                                        self.pwmLib.pwmWrite(pwm_Pin2,int(np.round(offset+400))) #going left
                                        
                                else:
                                        self.pwmLib.pwmWrite(pwm_Pin2,0)
                                        
                                if (self.RulerEnd[0]-self.RulerStart[0]!=0):
                                        slop    =   (self.RulerEnd[1]-self.RulerStart[1])/(self.RulerEnd[0]-self.RulerStart[0])
                                else:
                                        slop=0
                        
                                yline     =   slop*((self.currPenCoord[0]-self.RulerStart[0]))+self.RulerStart[1]-3
                                
                                if (self.currPenCoord[1]+self.y*1.45>yline and self.currPenForce>10):
                                        GPIO.output(DIR1,0)
                                        self.pwmLib.pwmWrite(pwm_Pin1,int(np.round(offset+400)))
                                else:
                                        self.pwmLib.pwmWrite(pwm_Pin1,0)
                                        self.y=0 
                                
                                if((abs(distance[1])<15 and (distance[0])<0)): # to make sure that we get to the absolute destination
                                        self.pwmLib.pwmWrite(pwm_Pin2,0)
                                        self.pwmLib.pwmWrite(pwm_Pin1,0)
                                        self.fullDrive=False
                                        print('done with state 1 rect drawing')
                                        
                        if ((self.mode=='Rect' or self.mode=='RectP')and self.state==4):
                                if(distance[1]<0):
                                        GPIO.output(DIR1,0)
                                        self.pwmLib.pwmWrite(pwm_Pin1,int(np.round(offset+400))) #going up
                                        
                                elif(distance[1]>10):
                                        GPIO.output(DIR1,1)
                                        self.pwmLib.pwmWrite(pwm_Pin1,int(np.round(offset+400))) #going down
                                else:
                                        self.pwmLib.pwmWrite(pwm_Pin1,0)
                                        
                                if (self.currPenCoord[0]+self.x*1.7>self.target[0] and self.currPenForce>10):
                                        GPIO.output(DIR2,1)
                                        self.pwmLib.pwmWrite(pwm_Pin2,int(np.round(offset+400))) # going left
                                else:
                                        self.pwmLib.pwmWrite(pwm_Pin2,0)
                                        self.x=0
                                
                                if((abs(distance[0])<15 and (distance[1])>0)): # to make sure that we get to the absolute destination
                                        self.pwmLib.pwmWrite(pwm_Pin2,0)
                                        self.pwmLib.pwmWrite(pwm_Pin1,0)
                                        self.fullDrive=False
                                        print('done with state 1 rect drawing')
                                        
                        if (self.state==5):
                                if(distance[0]<0):
                                        GPIO.output(DIR2,1)
                                        self.pwmLib.pwmWrite(pwm_Pin2,int(np.round(offset+400))) #going left
                                        
                                elif(distance[0]>10):
                                        GPIO.output(DIR2,0)
                                        self.pwmLib.pwmWrite(pwm_Pin2,int(np.round(offset+400))) #going right
                                else:
                                        self.pwmLib.pwmWrite(pwm_Pin2,0)
                                        
                                if (self.RulerEnd[0]-self.RulerStart[0]!=0):
                                        slop    =   (self.RulerEnd[1]-self.RulerStart[1])/(self.RulerEnd[0]-self.RulerStart[0])
                                else:
                                        slop=0
                        
                                yline     =   slop*((self.currPenCoord[0]-self.RulerStart[0]))+self.RulerStart[1]-3
                                
                                if (self.currPenCoord[1]+self.y*1.45<yline and self.currPenForce>10):
                                        GPIO.output(DIR1,1)
                                        self.pwmLib.pwmWrite(pwm_Pin1,int(np.round(offset+450))) #pushing down

                                else:
                                        self.pwmLib.pwmWrite(pwm_Pin1,0)
                                        self.y=0 
                                
                                if((abs(distance[1])<15 and (distance[0])>0)): # to make sure that we get to the absolute destination
                                        self.pwmLib.pwmWrite(pwm_Pin2,0)
                                        self.pwmLib.pwmWrite(pwm_Pin1,0)
                                        self.fullDrive=False
                                        print('done with state 1 rect drawing')
                        
                elif(self.mode=='Rect'):
                        if(self.state==1):
                                self.x=0
                                self.y=0 
                                self.lineStartCoord=[self.RectCorCoord[0],self.RectCorCoord[1]+(2*abs(self.RectCorCoord[1]-self.RectCentCoord[1]))] 
                                self.target=self.lineStartCoord
                                self.lineEndCoord=self.currPenCoord
                                self.fullDrive=True
                                self.state=2
                                print('starting the first line')
                        elif(self.state==2):
                                self.x=0
                                self.y=0 
                                #time.sleep(.1)
                                self.lineStartCoord=[self.RectCorCoord[0]+(2*abs(self.RectCorCoord[0]-self.RectCentCoord[0])),self.RectCorCoord[1]+(2*abs(self.RectCorCoord[1]-self.RectCentCoord[1]))]
                                self.target=self.lineStartCoord
                                self.lineEndCoord=self.currPenCoord
                                self.fullDrive=True
                                self.state=3
                                print('starting the second line')
                        elif(self.state==3):
                                self.x=0
                                self.y=0 
                                #time.sleep(.1)
                                self.lineStartCoord=[self.RectCorCoord[0]+(2*abs(self.RectCorCoord[0]-self.RectCentCoord[0])),self.RectCorCoord[1]]
                                self.target=self.lineStartCoord
                                self.lineEndCoord=self.currPenCoord
                                self.fullDrive=True
                                self.state=4
                                print('starting the third line')
                        elif(self.state==4):
                                self.x=0
                                self.y=0                                
                                #time.sleep(.1)
                                self.lineStartCoord=[self.RectCorCoord[0],self.RectCorCoord[1]]
                                self.target=self.lineStartCoord
                                self.lineEndCoord=self.currPenCoord
                                self.fullDrive=True
                                self.state=5
                                self.mode='none'
                                print('starting the fourth line')
                        
                elif(self.mode=='RectP'):
                        if(self.state==1):
                                self.x=0
                                self.y=0 
                                self.lineStartCoord=self.Rect2
                                self.target=self.Rect2
                                self.lineEndCoord=self.currPenCoord
                                self.fullDrive=True
                                self.state=2
                                print('starting the first line')
                        elif(self.state==2):
                                self.x=0
                                self.y=0 
                                time.sleep(.1)
                                self.lineStartCoord=self.Rect3
                                self.target=self.Rect3
                                self.lineEndCoord=self.currPenCoord
                                self.activeControl=True
                                self.state=3
                                print('starting the second line')
                        elif(self.state==3):
                                self.x=0
                                self.y=0 
                                time.sleep(.1)
                                self.lineStartCoord=self.Rect4
                                self.target=self.Rect4
                                self.lineEndCoord=self.currPenCoord
                                self.activeControl=True
                                self.state=4
                                print('starting the third line')
                        elif(self.state==4):
                                self.x=0
                                self.y=0                                
                                time.sleep(.1)
                                self.lineStartCoord=self.Rect1
                                self.target=self.Rect1
                                self.lineEndCoord=self.currPenCoord
                                self.activeControl=True
                                self.state=5
                                self.mode='none'
                                print('starting the fourth line')
                #making a Triangle                
                elif(self.mode=='Tri'):
                        if(self.state==1):
                                self.x=0
                                self.y=0 
                                self.lineStartCoord=self.TriSecond
                                self.target=self.TriSecond
                                self.lineEndCoord=self.TriFirst
                                self.activeControl=True
                                self.state=2
                                print('starting the first line')
                        elif(self.state==2):
                                self.x=0
                                self.y=0 
                                time.sleep(.1)
                                self.lineStartCoord=self.TriThird
                                self.target=self.TriThird
                                self.lineEndCoord=self.currPenCoord
                                self.activeControl=True
                                #self.mode='none'   # temporary for the demo
                                self.state=3
                                print('starting the second line')
                        elif(self.state==3):
                                self.x=0
                                self.y=0 
                                time.sleep(.1)
                                self.lineStartCoord=self.TriFirst
                                self.target=self.TriFirst
                                self.lineEndCoord=self.currPenCoord
                                self.activeControl=True
                                self.mode='none'
                                self.state=4
                                print('starting the third line')
 
                elif(self.mode=='Ruler'):
                        offset   =      100
                        gain     =      340
                        if(self.currPenForce>150):       #variable pressure gain
                                gain    =       300*abs((180-self.currPenForce))/80
                                offset   =      0
                                
                        else:
                                gain     =      300
                                offset   =      100
                                
                        #gain=340                # no shared control
                        
                        velocity =      [.0,1]
                        if (self.RulerEnd[0]-self.RulerStart[0]!=0):
                                slop    =   (self.RulerEnd[1]-self.RulerStart[1])/(self.RulerEnd[0]-self.RulerStart[0])
                        else:
                                slop=0
                        
                        yline     =   slop*((self.currPenCoord[0]-self.RulerStart[0]))+self.RulerStart[1]-3
                        if (self.currPenCoord[1]+self.y*1.45>yline and self.currPenForce>10):
                                GPIO.output(DIR1,0)
                                self.pwmLib.pwmWrite(pwm_Pin1,int(np.round(offset+velocity[1]*gain)))
                                GPIO.output(DIR2,0)
                                self.pwmLib.pwmWrite(pwm_Pin2,int(np.round(offset+100+velocity[0]*gain*1)))
                        else: 
                                self.pwmLib.pwmWrite(pwm_Pin2,0)
                                self.pwmLib.pwmWrite(pwm_Pin1,0)
                                self.x=0
                                self.y=0
                        if (abs(self.currPenCoord[0]-self.RulerEnd[0])<10 and abs(self.currPenCoord[1]-self.RulerEnd[1])<10):
                                self.mode='none'
                                self.pwmLib.pwmWrite(pwm_Pin2,0)
                                self.pwmLib.pwmWrite(pwm_Pin1,0)
                                print('done with ruler mode')
                                
                elif(self.mode=='Circ'):
                        offset   =      50
                        if(self.currPenForce>80):       #variable pressure gain
                                gain=400*abs((200-self.currPenForce))/80
                                self.x=0
                                self.y=0
                                self.lineEndCoord=self.currPenCoord
                                offset=0
                        else:
                                gain=400
                                offset=100
                        point=[self.CircCorCoord[0],self.CircCorCoord[1]]
                        center=[self.CircCentCoord[0],self.CircCentCoord[1]]
                        distance=[(point[0]-center[0]),(point[1]-center[1])]
                        
                        r=math.sqrt(distance[0]*distance[0]+distance[1]*distance[1])
                        #points=self.PointsInCircum(r,300,phi)   
                        #print('Points',points)
                        _currentpoint=[self.CircCorCoord[0]+self.x*1.7-center[0],self.CircCorCoord[1]+self.y*1.7-center[1]]
                        _currentpoint=np.subtract(self.currPenCoord,center)
                        tan=[]
                        phi0=math.atan2(distance[1],distance[0])        
                        phi=math.atan2(_currentpoint[1],_currentpoint[0])
                        r_current=math.sqrt(_currentpoint[0]*_currentpoint[0]+_currentpoint[1]*_currentpoint[1])
                        if (_currentpoint[1]!=0 and _currentpoint[0]!=0 ):
                                tan=[abs(1/(_currentpoint[1]/_currentpoint[0]))]

                        
                        #vx_corr=[r-(r_current)*math.cos(phi),(r-r_current)*math.sin(phi)]
                        #elif(_currentpoint[0]==0):
                            #    tan=[0]
                       # else:
                         #      tan=[10]
 
                        Vs=[np.ones(1),tan]
                        #Vs=np.add(Vs,vx_corr)
                        normV=np.linalg.norm(Vs,2)
                        velocity=np.divide(Vs,normV)
                        #normVc=np.linalg.norm(vx_corr,2)
                        #velocityc=np.divide(vx_corr,3*normV)
                        #velocity=[velocity[0]+velocityc[0],velocity[1]+velocityc[1]]
                        #print("velocity",velocity)
                        velocity[1]=-velocity[1]
                        
                        if (_currentpoint[0]>0 and _currentpoint[1]<0):
                                velocity[1]=-velocity[1]
                                #print("region 1")
                        elif (_currentpoint[0]>0 and _currentpoint[1]>0):
                                velocity[0]=-velocity[0]
                                velocity[1]=-velocity[1]
                               # print("region 2")
                                self.flagC=True
                        elif (_currentpoint[0]<0 and _currentpoint[1]>0):
                                velocity[0]=-velocity[0]
                                velocity[1]=velocity[1]
                               # print("region 3")
                        elif (_currentpoint[0]<0 and _currentpoint[1]<0):
                                velocity[0]=velocity[0]
                                print("region 4")
                        _currentpointR=np.add(_currentpoint,center)                
                        #print('_currentpoint',_currentpoint)
                        distancep=np.subtract(_currentpointR,self.CircCorCoord)
                        
                        if ((abs(phi-phi0)>10 or abs(distancep[1])>10) or self.flagC==False): # updating the starting point based on the current absolute position and running the controller again 
                        
                                if (velocity[0]>0):#x direction control
                                        GPIO.output(DIR2,0)
                                        self.pwmLib.pwmWrite(pwm_Pin2,int(np.round(offset+100+velocity[0]*gain*1))) #going right
                                else:
                                        GPIO.output(DIR2,1)
                                        self.pwmLib.pwmWrite(pwm_Pin2,int(np.round(offset+abs(velocity[0])*gain)))
                                        
                                if (velocity[1]>0): #y direction control
                                        GPIO.output(DIR1,1)
                                        self.pwmLib.pwmWrite(pwm_Pin1,int(np.round(offset+velocity[1]*gain)))
                                else: 
                                        GPIO.output(DIR1,0)
                                        self.pwmLib.pwmWrite(pwm_Pin1,int(np.round(offset+abs(velocity[1])*gain)))   #going up 
                        else:
                                self.x=0
                                self.y=0
                                self.pwmLib.pwmWrite(pwm_Pin2,0)
                                self.pwmLib.pwmWrite(pwm_Pin1,0)
                                self.mode='none'
                                print('done with Circ mode')
                        #
                        #self.pwmLib.pwmWrite(pwm_Pin2,0)
                        #self.pwmLib.pwmWrite(pwm_Pin1,0)
                        #print('done with Circ mode')

                               
                #if((time.time() - self.start_time)>0.01):
                     #   print ((time.time() - self.start_time))
               #  self.start_time = time.time()
                #print('In Control Loop')
         
                             
        def Orientation(self):
                # Read the Euler angles for heading, roll, pitch (all in degrees).
                self.heading, self.roll, self.pitch = self.bno.read_euler()
                # Read the calibration status, 0=uncalibrated and 3=fully calibrated.
                sys, gyro, accel, mag = self.bno.get_calibration_status()
                # Print everything out.
                #print('Heading={0:0.2F} Roll={1:0.2F} Pitch={2:0.2F}\t'.format(math.sin(math.pi*((360+self.heading-self.heading0)%360)/180), self.roll, self.pitch ))
                #print ((time.time() - start_time))
                self.start_time = time.time()
                #print ("PWMDuty is: " + str(PWMDuty))
                threading.Timer(0.03, self.Orientation).start()

     
        #~ def WiFiComms():
                #~ global PWMDuty
                
                #~ s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                #~ s.bind((TCP_IP, TCP_PORT))
                #~ s.listen(1)
                #~ conn, addr = s.accept()

                #~ while(addr is None and conn is None):
                        #~ conn, addr = s.accept()
                        #~ #print "waiting for connection..."

                #~ print("Connection address:", addr)
                       
                #~ while(addr is not None and conn is not None):
                        #~ conn.sendall((str(x)+str(",")+str(y)+str(",////////")).encode("utf-8"))  # echo
                        #~ data = conn.recv(BUFFER_SIZE)
                        #~ PWMDuty = float(data)
                        #~ data.decode()
                        #~ #print "received data: " + data

                
        def incY(self, channel):
                self.y += 1
                #~ if self.y > size:
                        #~ self.y = size
               # print ("y: " , str(self.y))

        def decY(self, channel):
                self.y -= 1
                #~ if self.y < -size:
                        #~ self.y = -size
               # print ("y: " , str(self.y))

        def incX(self, channel):
                self.x += 1
                #~ if self.x > size:
                        #~ self.x = size
               # print("x: " , str(self.x))

        def decX(self, channel):
                self.x -= 1
                #~ if self.x < -size:
                        #~ self.x = -size
                #print ("x: ", str(self.x))
                
        def btnPress(self, channel):
                BUTTON = 24
                global p11
                if(GPIO.input(BUTTON)):
                        p = False
                        self.contact=False
                  #      print ("btn release")
                else:
                        p = True
                        self.contact=True
                #        print ("btn press")
        def gpos(self, globaldata):
                self.currPenCoord=[globaldata[0],globaldata[1]]
                self.currPenForce = globaldata[2] 
                #print('global coordinate',globaldata[0],globaldata[1]) 
                      
        def receiveLineData(self, lineData):
                self.lineStartCoord = [lineData[0], lineData[1]]
                self.lineEndCoord = [lineData[2], lineData[3]]
                self.currPenCoord = [lineData[4], lineData[5]]
                if(len(lineData)>6):
                        self.currPenForce = lineData[6]
                elif(len(lineData)<=6):
                        self.currPenForce=0
        
                # print(self.lineStartCoord, self.lineEndCoord, self.currPenCoord, self.currPenForce)
                #print("inside the control thread")
       
        def controlStartDrawLine(self):
                offset=100
                gain=500
                self.activeControl=True
                self.x=0
                self.y=0
                self.mode='line'
                print("start draw line",self.activeControl)
                #print(self.lineStartCoord, self.lineEndCoord, self.currPenCoord, self.currPenForce)
                self.target=self.lineStartCoord
 
        
        #~ def controlStopDrawLine(self):

                #~ print("stop draw line")
                #~ self.activeControl=False
                #~ #print(self.lineStartCoord, self.lineEndCoord, self.currPenCoord, self.currPenForce)
                #~ self.pwmLib.pwmWrite(pwm_Pin2,0)
                #~ self.pwmLib.pwmWrite(pwm_Pin1,0)
 
 
 
        def receiveCircData(self, lineData):
                self.CircCentCoord = [lineData[0], lineData[1]]
                self.CircCorCoord = [lineData[2], lineData[3]]
                self.currPenCoord = [lineData[4], lineData[5]]
                if(lineData[6]):
                        self.currPenForce = lineData[6]
                
        def controlStartDrawCirc(self):
               
                print("start draw Circ", self.CircCentCoord,self.CircCorCoord)
                self.state=1
                self.x=0
                self.y=0
                self.flagC=False
                self.mode='Circ'
                
        #draw rectangle in perspective        
        def receiveRectData(self, lineData):
                self.RectCentCoord = [lineData[0], lineData[1]]
                self.RectCorCoord = [lineData[2], lineData[3]]
                self.currPenCoord = [lineData[4], lineData[5]]
                if(lineData[6]):
                        self.currPenForce = lineData[6]
                
        def controlStartDrawRect(self):
               
                print("start draw Rect", self.RectCentCoord,self.RectCorCoord)
                self.state=1
                self.mode='Rect'
                
        def receiveRectPData(self, lineData):
                self.Rect1      = [lineData[0], lineData[1]]
                self.Rect2      = [lineData[2], lineData[3]]
                self.Rect3      = [lineData[4], lineData[5]]
                self.Rect4      = [lineData[6], lineData[7]]
        def controlStartDrawRectP(self):
               
                print("start draw Rect in perspective", self.Rect1 ,self.Rect2,self.Rect3 ,self.Rect4)
                self.state=1
                self.mode='RectP'
                
                
                
        def controlStartRuler(self):
               
                print("start Ruler", self.lineStartCoord,self.lineEndCoord)
                self.RulerEnd   =       self.lineStartCoord
                self.RulerStart =       self.lineEndCoord
                self.mode='Ruler'
                                        

                
        def receiveTriData(self, lineData):
                self.TriFirst = [lineData[0], lineData[1]]
                self.TriSecond = [lineData[2], lineData[3]]
                self.TriThird = [lineData[4], lineData[5]]

                
        def ControlStartDrawTri(self):
                print("start draw Triangle", self.TriFirst,self.TriSecond,self.TriThird)
                self.state=1
                self.mode='Tri'
                
        def run(self):
                self.activeControl=False
                self.mode=''
                self.target=[0,0]
                # add event handler to GPIO pins to detect edges
                GPIO.add_event_detect(UP, GPIO.BOTH, callback=self.incY)
                GPIO.add_event_detect(DOWN, GPIO.BOTH, callback=self.decY)
                GPIO.add_event_detect(LEFT, GPIO.BOTH, callback=self.incX)
                GPIO.add_event_detect(RIGHT, GPIO.BOTH, callback=self.decX)
                GPIO.add_event_detect(BUTTON, GPIO.BOTH, callback=self.btnPress)

                thread1 = threading.Thread(target=self.DriveControl)
                thread2 = threading.Thread(target=self.Orientation)       # changing frequency is 1kHz when interval is 0.2ms
                thread1.start()
                thread2.start()          


