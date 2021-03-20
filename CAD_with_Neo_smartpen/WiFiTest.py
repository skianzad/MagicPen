#!/usr/bin/env python
'''
Created on 2021-03-17

@author: Guanxiong
'''
from PyQt4.QtCore import *
import socket
import threading
import time


'''
    A simple WiFi client to request pen data, and decode x, y
    coordinates and pressure upon receiving it
'''
class WiFiClient(QThread):
    
    def __init__(self, tcpIP='', tcpPort=8080, bufferSize = 21, parent=None):
        super(WiFiClient,self).__init__(parent)
        
        self.__TCP_IP = tcpIP
        self.__TCP_PORT = tcpPort
        self.__BUFFER_SIZE = bufferSize
        self.conn = None

        print('initialized')

        
    # Initialize WiFi connection
    def socketInit(self):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Wait until a connection is established/accepted
        print("Waiting for connection...")
        self.conn.connect((self.__TCP_IP, self.__TCP_PORT))
        print("Connected to server")
        return


    # Overwrite the run method to monitor request from client. Upon request, transmit
    # pen data (pressure, etc.) to client 
    def run(self):
        self.socketInit()
        
        # monitor request and transmit data upon request
        while(self.conn is not None):
            # transmit request
            requestString = "data"
            request = requestString.encode('utf-8')
            self.conn.send(request)

            # decode data
            data = self.conn.recv(self.__BUFFER_SIZE)
            dataString = data.decode("utf-8")
            print(dataString)
            coords = dataString.split("/")[0].split(",")
            xCoord = coords[0]
            yCoord = coords[1]
            pressure = dataString.split("/")[1]

        print("WIFI client exited")
        return

def main():
    wifiCl = WiFiClient(tcpIP='192.168.0.103')
    wifiCl.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass    
    
if __name__ == '__main__':
    main()


