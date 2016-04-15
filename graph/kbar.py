# # -*- coding: utf-8 -*-
#
# # Form implementation generated from reading ui file 'MplMainWindow.ui'
#
# #
#
# # Created: Mon Aug 11 14:18:31 2014
#
# #      by: PyQt4 UI code generator 4.10.3
#
# #
#
# # WARNING! All changes made in this file will be lost!
#
# from PyQt4 import QtCore, QtGui
# from mplCanvasWrapper import MplCanvasWrapper
#
#
# try:
#
#     _fromUtf8 = QtCore.QString.fromUtf8
#
# except AttributeError:
#
#     def _fromUtf8(s):
#
#     return s
#
# try:
#
#     _encoding = QtGui.QApplication.UnicodeUTF8
#
# def _translate(context, text, disambig):
#
# return QtGui.QApplication.translate(context, text, disambig, _encoding)
#
# except AttributeError:
#
# def _translate(context, text, disambig):
#
# return QtGui.QApplication.translate(context, text, disambig)
#
# #inheritent from QtGui.QMainWindow
#
# class Ui_MainWindow(QtGui.QMainWindow):
#
# def setupUi(self, MainWindow):
#
# MainWindow.setObjectName(_fromUtf8("MainWindow"))
#
# MainWindow.resize(690, 427)
#
# self.centralWidget = QtGui.QWidget(MainWindow)
#
# self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
#
# self.gridLayout = QtGui.QGridLayout(self.centralWidget)
#
# self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
#
# self.horizontalLayout = QtGui.QHBoxLayout()
#
# self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
#
# self.btnStart = QtGui.QPushButton(self.centralWidget)
#
# self.btnStart.setObjectName(_fromUtf8("btnStart"))
#
# self.horizontalLayout.addWidget(self.btnStart)
#
# self.btnPause = QtGui.QPushButton(self.centralWidget)
#
# self.btnPause.setObjectName(_fromUtf8("btnPause"))
#
# self.horizontalLayout.addWidget(self.btnPause)
#
# spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
#
# self.horizontalLayout.addItem(spacerItem)
#
# self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
#
# self.mplCanvas = MplCanvasWrapper(self.centralWidget)
#
# sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
#
# sizePolicy.setHorizontalStretch(0)
#
# sizePolicy.setVerticalStretch(0)
#
# sizePolicy.setHeightForWidth(self.mplCanvas.sizePolicy().hasHeightForWidth())
#
# self.mplCanvas.setSizePolicy(sizePolicy)
#
# self.mplCanvas.setObjectName(_fromUtf8("mplCanvas"))
#
# self.gridLayout.addWidget(self.mplCanvas, 1, 0, 1, 1)
#
# MainWindow.setCentralWidget(self.centralWidget)
#
# self.retranslateUi(MainWindow)
#
# QtCore.QMetaObject.connectSlotsByName(MainWindow)
#
# def retranslateUi(self, MainWindow):
#
# MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
#
# self.btnStart.setText(_translate("MainWindow", "开始", None))
#
# self.btnPause.setText(_translate("MainWindow", "暂停", None))
#
# 2）Code_MplMainWindow.py
#
# from PyQt4 import QtGui, QtCore
#
# from Ui_MplMainWindow import Ui_MainWindow
#
# class Code_MainWindow(Ui_MainWindow):
#
# def __init__(self, parent = None):
#
# super(Code_MainWindow, self).__init__(parent)
#
# self.setupUi(self)
#
# self.btnStart.clicked.connect(self.startPlot)
#
# self.btnPause.clicked.connect(self.pausePlot)
#
# def startPlot(self):
#
# ''' begin to plot'''
#
# self.mplCanvas.startPlot()
#
# pass
#
# def pausePlot(self):
#
# ''' pause plot '''
#
# self.mplCanvas.pausePlot()
#
# pass
#
# def releasePlot(self):
#
# ''' stop and release thread'''
#
# self.mplCanvas.releasePlot()
#
# def closeEvent(self,event):
#
# result = QtGui.QMessageBox.question(self,
#
# "Confirm Exit...",
#
# "Are you sure you want to exit ?",
#
# QtGui.QMessageBox.Yes| QtGui.QMessageBox.No)
#
# event.ignore()
#
# if result == QtGui.QMessageBox.Yes:
#
# self.releasePlot()#release thread's resouce
#
# event.accept()
#
# if __name__ == "__main__":
#
# import sys
#
# app = QtGui.QApplication(sys.argv)
#
# ui = Code_MainWindow()
#
# ui.show()
#
# sys.exit(app.exec_())
#
# 3）mplCanvasWrapper.py
#
# from PyQt4 import  QtGui
#
# from matplotlib.backends.backend_qt4agg import  FigureCanvasQTAgg as FigureCanvas
#
# from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
#
# from matplotlib.figure import Figure
#
# import numpy as np
#
# from array import array
#
# import time
#
# import random
#
# import threading
#
# from datetime import datetime
#
# from matplotlib.dates import  date2num, MinuteLocator, SecondLocator, DateFormatter
#
# X_MINUTES = 1
#
# Y_MAX = 100
#
# Y_MIN = 1
#
# INTERVAL = 1
#
# MAXCOUNTER = int(X_MINUTES * 60/ INTERVAL)
#
# class MplCanvas(FigureCanvas):
#
# def __init__(self):
#
# self.fig = Figure()
#
# self.ax = self.fig.add_subplot(111)
#
# FigureCanvas.__init__(self, self.fig)
#
# FigureCanvas.setSizePolicy(self, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
#
# FigureCanvas.updateGeometry(self)
#
# self.ax.set_xlabel("time of data generator")
#
# self.ax.set_ylabel('random data value')
#
# self.ax.legend()
#
# self.ax.set_ylim(Y_MIN,Y_MAX)
#
# self.ax.xaxis.set_major_locator(MinuteLocator())  # every minute is a major locator
#
# self.ax.xaxis.set_minor_locator(SecondLocator([10,20,30,40,50])) # every 10 second is a minor locator
#
# self.ax.xaxis.set_major_formatter( DateFormatter('%H:%M:%S') ) #tick label formatter
#
# self.curveObj = None # draw object
#
# def plot(self, datax, datay):
#
# if self.curveObj is None:
#
# #create draw object once
#
# self.curveObj, = self.ax.plot_date(np.array(datax), np.array(datay),'bo-')
#
# else:
#
# #update data of draw object
#
# self.curveObj.set_data(np.array(datax), np.array(datay))
#
# #update limit of X axis,to make sure it can move
#
# self.ax.set_xlim(datax[0],datax[-1])
#
# ticklabels = self.ax.xaxis.get_ticklabels()
#
# for tick in ticklabels:
#
# tick.set_rotation(25)
#
# self.draw()
#
# class  MplCanvasWrapper(QtGui.QWidget):
#
#     def __init__(self , parent =None):
#
#         QtGui.QWidget.__init__(self, parent)
#
#         self.canvas = MplCanvas()
#
#         self.vbl = QtGui.QVBoxLayout()
#
#         self.ntb = NavigationToolbar(self.canvas, parent)
#
#         self.vbl.addWidget(self.ntb)
#
#         self.vbl.addWidget(self.canvas)
#
#         self.setLayout(self.vbl)
#
#         self.dataX= []
#
#         self.dataY= []
#
#         self.initDataGenerator()
#
# def startPlot(self):
#
# self.__generating = True
#
# def pausePlot(self):
#
# self.__generating = False
#
# pass
#
# def initDataGenerator(self):
#
# self.__generating=False
#
# self.__exit = False
#
# self.tData = threading.Thread(name = "dataGenerator",target = self.generateData)
#
# self.tData.start()
#
# def releasePlot(self):
#
# self.__exit  = True
#
# self.tData.join()
#
# def generateData(self):
#
# counter=0
#
# while(True):
#
# if self.__exit:
#
# break
#
# if self.__generating:
#
# newData = random.randint(Y_MIN, Y_MAX)
#
# newTime= date2num(datetime.now())
#
# self.dataX.append(newTime)
#
# self.dataY.append(newData)
#
# self.canvas.plot(self.dataX, self.dataY)
#
# if counter >= MAXCOUNTER:
#
# self.dataX.pop(0)
#
# self.dataY.pop(0)
#
# else:
#
# counter+=1
#
# time.sleep(INTERVAL)