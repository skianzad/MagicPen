'''
Created on 2019-01-01 00:00

@author: Yuxiang
'''

from MainWidget import MainWidget
from PyQt4.QtGui import QApplication

import sys

def main():
    app = QApplication(sys.argv) 
    
    mainWidget = MainWidget()
    mainWidget.show()
    
    exit(app.exec_())
    
    
if __name__ == '__main__':
    main()

