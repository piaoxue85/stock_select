import sys
import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import random
import matplotlib.pyplot as plt

class GUIForm(QtGui.QDialog):

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self,parent)
        # self.ui = Ui_Dialog()
        # self.ui.setupUi(self)

        QtCore.QObject.connect(self.ui.pushButton,
                               QtCore.SIGNAL('clicked()'), self.PlotFunc)

    def PlotFunc(self):
        randValList = random.sample(range(0, 10), 10)
        print(randValList)
        self.ui.PlotWidget.canvas.ax.clear()
        self.ui.PlotWidget.canvas.ax.plot(randValList)

    def callFunc(self):
        myapp.PlotFunc()


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = GUIForm()
    myapp.show()
    sys.exit(app.exec_())