'''
Created on 2029-07-10 00:00

@author: Soheil 
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
from MainWidget import MainWidget
from PyQt4.QtGui import QApplication

import sys

class MainWidget(QWidget):
    app = QApplication(sys.argv) 
    bl=BluetoothThread()
    bl.start()
    exit(app.exec_())

mainWidget = MainWidget()
mainWidget.show()