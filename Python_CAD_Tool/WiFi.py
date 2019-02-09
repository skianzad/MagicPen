#!/usr/bin/env python
'''
Created on 2019-01-01

@author: Yuxiang
'''
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import RPi.GPIO as GPIO
import socket


'''
    A simple WiFi server to receive coordinates from the digital pen
'''
class WiFiThread(QThread):

    __TCP_IP = ''
    __TCP_PORT = 8080
    __BUFFER_SIZE = 20
    conn = None
    addr = None
    sigOut = pyqtSignal(list)
    
    def __init__(self, tcpIP='', tcpPort=8080, bufferSize = 20, parent=None):
        super(WiFiThread,self).__init__(parent)
        
        self.__TCP_IP = tcpIP
        self.__TCP_PORT = tcpPort
        self.__BUFFER_SIZE = bufferSize

        
    # Initialize WiFi connection
    def socketInit(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.__TCP_IP, self.__TCP_PORT))
        s.listen(1)
        # Wait until a connection is established/accepted
        print("Waiting for connection...")
        self.conn, self.addr = s.accept()
      
        while(self.addr is None and self.conn is None):
            self.conn, self.addr = s.accept()

        print("Connection address:", self.addr)


    # overwrite  the run method to continously receive data from the socket
    def run(self):
        self.socketInit()
        
        while(self.addr is not None and self.conn is not None):
            data = self.conn.recv(self.__BUFFER_SIZE)
            dataString = data.decode("utf-8")
            # print(dataString)
            
            rawCoordinates = dataString.split("/")[0].split(",")
            rawPressure = dataString.split("/")[1]
            rawXCoord = rawCoordinates[0]
            rawYCoord = rawCoordinates[1]

            dataList = [rawXCoord, rawYCoord, rawPressure]
            self.sigOut.emit(dataList)
            

