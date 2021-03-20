#!/usr/bin/env python
'''
Created on 2021-02-28

@author: Guanxiong, Yuxiang
'''
from PyQt4.QtCore import *
import socket
import threading

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

        self.xCoord = -1
        self.yCoord = -1
        self.pressure = -1
        self.penDataLock = threading.Lock()

        assert sigPenData is not None
        sigPenData.connect(self.updatePenData)
        return

        
    # Initialize WiFi connection
    def socketInit(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.__TCP_IP, self.__TCP_PORT))
        s.listen(1)
        # Wait until a connection is established/accepted
        print("Waiting for connection...")
        self.conn, self.addr = s.accept()
        assert (self.conn is not None) and (self.addr is not None)
        return


    # update pen x, y coordinate and pressure upon being called
    # from the bluetooth thread
    def updatePenData(self, penDataList):
        #print("Updating pen data")
        self.penDataLock.acquire()
        self.xCoord = penDataList[0]
        self.yCoord = penDataList[1]
        self.pressure = penDataList[2]
        self.penDataLock.release()
        return


    # Overwrite the run method to monitor request from client. Upon request, transmit
    # pen data (pressure, etc.) to client 
    def run(self):
        self.socketInit()
        
        # monitor request and transmit data upon request
        while(self.addr is not None and self.conn is not None):
            # decode request
            dataRequest = self.conn.recv(self.__BUFFER_SIZE)
            dataRequestString = dataRequest.decode("utf-8")
            # print(dataRequestString)

            # transmit pen data upon valid request
            if dataRequestString == "data":
                #print("Received request for pen data")
                # assemble pen data string
                self.penDataLock.acquire()
                dataTransmitString = str(self.xCoord) + ',' + str(self.yCoord) + '/' + str(self.pressure)
                self.penDataLock.release()
                # transmit pen data
                #print(dataTransmitString)
                dataTransmit = dataTransmitString.encode('utf-8')
                self.conn.send(dataTransmit)

        print("WIFI server exited")
        return
            

