'''
Created on 2019-01-02

@author: Yuxiang Huang
'''
from MainWidget import MainWidget
from PyQt5.QtWidgets import QApplication

import sys

'''
	The main function of the CAD application
'''
def main():
    app = QApplication(sys.argv) 
    
    mainWidget = MainWidget()
    mainWidget.show()
    
    exit(app.exec_())
    
    
if __name__ == '__main__':
    main()

    
