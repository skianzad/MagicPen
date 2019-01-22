#!/usr/bin/env python
'''
Created on 2019-01-02

@author: Yuxiang Huang
'''
import RPi.GPIO as GPIO
import socket

BUFFER_SIZE = 64              # Normally 1024, but we want fast response

addr = None

'''
    A simple WiFi server class to receive coordinates from the digital pen
'''
class WiFi():
    
    def __init__(self, TCP_IP='', TCP_Port=8080):
        
        self.WiFiInit(IP, Port)

        
    # Initialize WiFi connection
    def WiFiInit(self, TCP_IP, TCP_Port):

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind((TCP_IP, TCP_PORT))
            s.listen(1)
            conn, addr = s.accept()

            while(addr is None and conn is None):
                    conn, addr = s.accept()
                    print "waiting for connection..."

            print("Connection address:", addr)

        
    def WiFiReceive(self, BUFFER_SIZE=64):
            
            data = conn.recv(BUFFER_SIZE)
            respString = data.decode("utf-8")
            print "received data: " + data
            coordinates = respString.split(",")
            return coordinates

