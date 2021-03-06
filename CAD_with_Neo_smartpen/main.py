'''
Created on 2019-01-01 00:00

@author: Yuxiang
'''

from MainWidget import MainWidget
from PyQt4.QtGui import QApplication

import sys
import logging.config
logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='%(message)s')

def main():
    app = QApplication(sys.argv) 
    
    # pass in index of difficulty
    mainWidget = MainWidget(float(sys.argv[1]))
    mainWidget.show()
    
    exit(app.exec_())
    
    
if __name__ == '__main__':
    main()

