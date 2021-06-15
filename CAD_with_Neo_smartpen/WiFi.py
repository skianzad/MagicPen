#!/usr/bin/env python
'''
Created on 2021-02-28

@author: Guanxiong, Yuxiang
'''
from PyQt5.QtCore import *
import socket
import threading

'''
    Class to represent a stroke as a sequence of pen-tip positions
    when the pen is pressed against paper.
'''
class Stroke():

    # arguments:
    # index - indicate the order of this stroke;
    #         0 if the first stroke created since program
    #         started
    def __init__(self, index): 
        self.index = index
        self.done = False
        self.xCoords = []
        self.yCoords = []

    
    # append x and y coordinates to the stroke
    def append_coord(self, xCoord, yCoord):
        assert self.done is False
        self.xCoords.append(xCoord)
        self.yCoords.append(yCoord)
        return

    
    # complete the stroke
    def complete_stroke(self):
        self.done =True
        return

    
    # get the length of the stroke
    def get_length(self):
        return len(self.xCoords)

'''
    A simple WiFi server to transmit pen data to a client upon request.
'''
class WiFiThread(QThread):
    
    def __init__(self, sigPenData=None, tcpIP='', tcpPort=8080, bufferSize = 21, parent=None):
        super(WiFiThread,self).__init__(parent)
        
        self.__TCP_IP = tcpIP
        self.__TCP_PORT = tcpPort
        self.__BUFFER_SIZE = bufferSize
        self.conn = None
        self.addr = None

        # set min pressure to be recognized as stroke point 
        self.FORCE_STROKE_MIN = 5.0
        
        # stroke data protected by a conditional variable
        # (and its associated lock)
        self.stroke = None
        self.strokeConVar = threading.Condition()

        # index to track the index of the last stroke requested
        # by client
        self.strokeReqCounter = -1

        assert sigPenData is not None
        sigPenData.connect(self.update_stroke_state)
        return

        
    # Initialize WiFi connection
    def socket_init(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.__TCP_IP, self.__TCP_PORT))
        s.listen(1)
        # Wait until a connection is established/accepted
        print("Waiting for connection...")
        self.conn, self.addr = s.accept()
        assert (self.conn is not None) and (self.addr is not None)
        return


    # update stroke state upon being called from the bluetooth thread
    def update_stroke_state(self, penDataList):
        #print("Updating pen data")

        # extract point data
        xCoord = penDataList[0]
        yCoord = penDataList[1]
        pressure = penDataList[2]

        # update stroke state
        with self.strokeConVar:
            # if the last stroke does not exist or is done, then
            # create a new stroke
            if (self.stroke is None) or (self.stroke.done is True):
                if pressure >= self.FORCE_STROKE_MIN:
                    # create the first stroke since program started
                    if self.stroke is None:
                        self.stroke = Stroke(0)
                        self.stroke.append_coord(xCoord, yCoord)
                    # define a new stroke with index incremented by 1
                    else:
                        self.stroke = Stroke(self.stroke.index + 1)
                        self.stroke.append_coord(xCoord, yCoord)
                else:
                    pass
            # if the last stroke is not done, then either add a point
            # or terminate the stroke
            else:
                if pressure >= self.FORCE_STROKE_MIN:
                    self.stroke.append_coord(xCoord, yCoord)
                else:
                    self.stroke.complete_stroke()
                    self.strokeConVar.notify()

        return


    # The overwritten run method monitors requests from client.
    # Upon a valid request, wait until a new stroke is completed,
    # then transmit the stroke to the client
    def run(self):
        self.socket_init()
        
        # monitor request and transmit data upon request
        while(self.addr is not None and self.conn is not None):
            # decode request
            dataRequest = self.conn.recv(self.__BUFFER_SIZE)
            dataRequestString = dataRequest.decode("utf-8")
            #print(dataRequestString)

            # transmit pen data upon valid request
            if dataRequestString == "data":
                #print("Received request for stroke data")
                
                with self.strokeConVar:
                    # sleep until a new stroke is completed
                    while (
                        (self.stroke is None) or
                        (self.stroke.done is False) or 
                        (self.strokeReqCounter>=self.stroke.index)
                    ):
                        #print("waiting for new stroke")
                        self.strokeConVar.wait()
                    
                    # update last-seen stroke index
                    self.strokeReqCounter = self.stroke.index

                    # assemble pen stroke data string
                    # string formatted as x_0,y_0/x_1,y_1/.../x_(N-1),y_(N-1)/
                    # for a stroke of N points
                    dataTransmitString = ''
                    for i in range(0, self.stroke.get_length()):
                        dataTransmitString = dataTransmitString + str(self.stroke.xCoords[i]) + ',' + str(self.stroke.yCoords[i]) + '/'
                    
                    # transmit pen data
                    #print(dataTransmitString)
                    dataTransmit = dataTransmitString.encode('utf-8')
                    self.conn.send(dataTransmit)

        print("WIFI server exited")
        return
            

