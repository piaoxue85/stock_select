#-*- encoding:utf8 -*-
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class mainWindow(QWidget):
    def __init__(self, parent = None):
        super(mainWindow, self).__init__(parent)
        button = QPushButton('弹出新窗口', self)
        self.slavewindow = slaveWindow()
        self.connect(button, SIGNAL('clicked()'), self.slavewindow.show)

class slaveWindow(QWidget):
    def __init__(self, parent = None):
        super(slaveWindow, self).__init__(parent)

def main():
    app = QApplication(sys.argv)
    mainwindow = mainWindow()
    mainwindow.show()
    app.exec_()

main()