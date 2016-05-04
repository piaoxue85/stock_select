# -*- encoding:utf8 -*-
# 开始重新整理代码
# 系统包
import sys
import datetime
import time
# Pyqt4包
from PyQt4 import QtCore
from PyQt4.QtGui import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QSizePolicy, QWidget, QLabel, QLineEdit, QDateEdit, QPushButton
# matplotlib包
import matplotlib
from matplotlib import dates
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.ticker import MultipleLocator, FuncFormatter
from matplotlib.finance import candlestick_ohlc
from matplotlib.figure import Figure
# Tushare 获取股票数据
import tushare as ts
# Mongodb 要打开服务才能使用
from pymongo import MongoClient

matplotlib.rcParams['font.sans-serif'] = ['SimHei'] #指定默认字体
matplotlib.rcParams['axes.unicode_minus'] = False #解决保存图像是负号'-'显示为方块的问题

# 默认头
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s
try:
    _encoding = QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)


# 将数据加工处理
# 使用tushare作为数据源,code为股票,start和en为起始结束


def source(code = '601928',start = '2016-02-01',end = '2016-04-01'):
    # start = datetime.datetime.strptime(start, "%Y-%m-%d")
    # start_s = time.mktime(start.timetuple())
    # before = start_s - 3600*24*10
    # start = time.strftime("%Y-%m-%d", time.localtime(before))
    # data = ts.get_h_data(code,start=start,end = end)
    raw_data = ts.get_h_data(code,start=start,end = end)
    # raw_data = data.iloc[:-8,:]
    num = len(raw_data)
    title = list(raw_data.columns.values)
    day = list(raw_data.index.values)
    data = []
    line = []
    value = []
    DrawEMA = []
    date = [datetime.datetime.utcfromtimestamp(each.tolist()/1e9) for each in day]
    str_date = [item.isoformat()[5:10] for item in date]
    num_date = [dates.date2num(each) for each in date]
    date.reverse()
    str_date.reverse()
    num_date.reverse()
    month_date = [each[3:5] for each in str_date]
    #开高低收,原数据是反过来的
    for i in range(num):
        data.append((num-i-1,raw_data.iloc[i][0],raw_data.iloc[i][1],raw_data.iloc[i][3],raw_data.iloc[i][2]))
        line.append(num-i)
        value.append(raw_data.iloc[i][2])

    return num, data,str_date,value

# EMA的计算公式,证明是有问题的，并不能这样子做，EMA都是从开盘日算起的


def EMA(x,n):
    if n is 1:
        return float(x[-1])
    return float(2*x[-1]+(n-1)*EMA(x[:-1],n-1))/(n + 1)

#将matplotlib的一个组件放进去


class MyMplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=9, height=6, dpi=150):
        self.fig = Figure(figsize=(width, height), dpi=dpi,facecolor='#F0F8FF')
        self.ax1 = self.fig.add_subplot(111)
        # self.ax1 = self.fig.add_axes([0.1, 0.35, 0.8, 0.58])
        # self.ax2 = self.fig.add_axes([0.1, 0.07, 0.8, 0.2])
        # self.ax1.hold(False)
        # self.ax2.hold(False)
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)


def ini():
    # 连接数据库
    con = MongoClient()
    db = con.stockdb
    collection = db.stock_holder
    return collection



def star(col, code, start, end):
    codintion = {'股票代码': code}
    multiple = col.find(codintion)
    date = []
    value = []
    d1 = datetime.datetime.strptime(start,"%Y-%m-%d")
    start_s = time.mktime(d1.timetuple())
    d2 = datetime.datetime.strptime(end,"%Y-%m-%d")
    end_s = time.mktime(d2.timetuple())
    for each in multiple:
        this = each[u'日期']
        d3 = datetime.datetime.strptime(this,"%Y-%m-%d")
        this_s = time.mktime(d3.timetuple())
        if this_s <= end_s and this_s >= start_s:
            date.append(each[u'日期'])
            value.append(each[u'星数'])
    return date, value
col = ini()


class sub_canvas(MyMplCanvas):
    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)


        self.widget = QWidget(self)
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.label_1 = QLabel(self.widget)
        self.horizontalLayout.addWidget(self.label_1)
        self.lineEdit = QLineEdit(self.widget)
        self.horizontalLayout.addWidget(self.lineEdit)
        self.label_2 = QLabel(self.widget)
        self.horizontalLayout.addWidget(self.label_2)
        self.dateEdit = QDateEdit(self.widget)
        self.horizontalLayout.addWidget(self.dateEdit)
        self.label_3 = QLabel(self.widget)
        self.horizontalLayout.addWidget(self.label_3)
        self.dateEdit_2 = QDateEdit(self.widget)
        self.horizontalLayout.addWidget(self.dateEdit_2)
        self.button1 = QPushButton(self.widget)
        self.horizontalLayout.addWidget(self.button1)
        self.button2 = QPushButton(self.widget)
        self.horizontalLayout.addWidget(self.button2)
        self.lineEdit.setText(QtCore.QString('600198'))
        three_month = QtCore.QDate.currentDate().toJulianDay() - 40
        self.dateEdit.setDate(QtCore.QDate.fromJulianDay(three_month))
        self.dateEdit_2.setDate(QtCore.QDate.currentDate())
        self.label_1.setText(_translate("MainWindow", "股票代码", None))
        self.label_2.setText(_translate("MainWindow", "起始时间", None))
        self.label_3.setText(_translate("MainWindow", "终止时间", None))
        self.button1.setText(_translate("MainWindow", "提交", None))
        self.button2.setText(_translate("MainWindow", "清除", None))

        self.button1.clicked.connect(self.get_value)
        self.button2.clicked.connect(self.clear)

    # 定义横坐标格式的回调函数
    def my_major_formatter(self, x, pos):
        for i in range(self.num):
            if (x == i):
                return self.str_date[i]
                # 定义横坐标格式的回调函数

    def my_star_formatter(self, x, pos):
        for i in range(len(self.star_date)):
            if (x == i):
                return self.star_date[i]

    def update_figure(self):

        self.fig.clf()
        self.ax1 = self.fig.add_subplot(111)
        self.ax2 = self.ax1.twinx()  # 创建第二个坐标轴
        # self.ax1 = self.fig.add_axes([0.1, 0.35, 0.8, 0.58])
        # self.ax2 = self.fig.add_axes([0.1, 0.07, 0.8, 0.2])
        # 子图一
        self.ax1.set_xticks(range(self.num))
        xmajorLocator = MultipleLocator(5)  # 将x主刻度标签设置为3的倍数
        xminorLocator = MultipleLocator(1)  # 将x副刻度标签设置为1的倍数
        self.ax1.xaxis.set_major_locator(xmajorLocator)
        self.ax1.xaxis.set_minor_locator(xminorLocator)
        self.ax1.xaxis.set_major_formatter(FuncFormatter(self.my_major_formatter))
        self.ax1.grid()
        self.ax2.bar(range(len(self.star_date)), self.star_value, picker=True, color='#FFFF00', width = 0.5,edgecolor = 'black')

        self.ax2.set_ylim(0, 80)
        candlestick_ohlc(self.ax1, self.data, width=0.5, colorup='r', colordown='g')
        lim = self.ax1.get_ylim()
        # self.ax1.hold(False)
        # self.ax2.hold(False)
        self.ax1.set_ylim(lim[0] * 0.95, lim[1])
        for tick in self.ax1.xaxis.get_major_ticks():
            tick.label1.set_fontsize(8)
            tick.label1.set_rotation(75)
        for tick in self.ax1.yaxis.get_major_ticks():
            tick.label1.set_fontsize(8)
            tick.label1.set_rotation(30)
        for tick in self.ax2.xaxis.get_major_ticks():
            tick.label1.set_fontsize(8)
            tick.label1.set_rotation(75)
        for tick in self.ax2.yaxis.get_major_ticks():
            tick.label1.set_fontsize(8)
            tick.label1.set_rotation(30)
        # 子图二

        # self.ax2.set_xticks(range(self.num))
        # self.ax2.xaxis.set_major_locator(xmajorLocator)
        # self.ax2.xaxis.set_minor_locator(xminorLocator)
        # self.ax2.grid()
        # self.ax2.set_xticklabels(self.str_date, rotation=25, horizontalalignment='right')

        # self.ax2.bar(range(len(self.star_date)), self.star_value, picker=True, color='#FFFF00')
        # #self.ax2.xaxis.set_major_locator(xmajorLocator)
        # self.ax2.xaxis.set_major_formatter(FuncFormatter(self.my_major_formatter))
        # for label in self.ax2.get_xticklabels():
        #     label.set_picker(True)
        # for tick in self.ax2.xaxis.get_major_ticks():
        #     tick.label1.set_fontsize(5)
        #     tick.label1.set_rotation(90)
        # for tick in self.ax2.yaxis.get_major_ticks():
        #     tick.label1.set_fontsize(5)
        #     tick.label1.set_rotation(30)
        #
        self.draw()
        # self.fig.clf()

    def get_value(self):
        code = QtCore.QString(self.lineEdit.text())
        start = QtCore.QString(self.dateEdit.text())
        end = QtCore.QString(self.dateEdit_2.text())
        code = unicode(code)
        start = datetime.date(int(start.split("/")[0]), int(start.split("/")[1]), int(start.split("/")[2])).isoformat()
        end = datetime.date(int(end.split("/")[0]), int(end.split("/")[1]), int(end.split("/")[2])).isoformat()

        self.num, self.data, self.str_date, self.value = source(code,start,end)
        self.star_date, self.star_value = star(col, code, start, end)
        self.update_figure()
    def clear(self):
        self.fig.clf()
        self.ax1 = self.fig.add_subplot(111)
        # self.ax1 = self.fig.add_axes([0.1, 0.35, 0.8, 0.58])
        # self.ax2 = self.fig.add_axes([0.1, 0.07, 0.8, 0.2])
        self.draw()
class ApplicationWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("Stock select graph")

        self.main_widget = QWidget(self)

        self.vbl = QVBoxLayout(self.main_widget)
        self.qmc = sub_canvas(self.main_widget, width=9, height=6, dpi=200)
        self.ntb = NavigationToolbar(self.qmc,self.main_widget)



        self.vbl.addWidget(self.qmc)
        # self.vbl.addWidget(self.widget)
        self.vbl.addWidget(self.ntb)
        self.setGeometry(100, 100, 1600, 900)
        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)



app = QApplication(sys.argv)
aw = ApplicationWindow()
aw.show()
widget = QWidget()
app.exec_()

# 数据库mongodb



# def drawPic():
#
#    #清空图像，以使得前后两次绘制的图像不会重叠
#    drawPic.f.clf()
#    drawPic.a=drawPic.f.add_subplot(111)
#    ax = drawPic.a
#
#    ax.set_xticklabels(x,fontsize = 13)
#    x = range(len(x))
#
#    ax.set_xlabel(u'时间')
#    ax.set_ylabel(u'价格')
#    return ax,x,y,z
#
# matplotlib.use('TkAgg')
# root=Tk()
# #在Tk的GUI上放置一个画布，并用.grid()来调整布局
# drawPic.figure = Figure(figsize=(5,3), dpi=200)
# drawPic.canvas = FigureCanvasTkAgg(drawPic.f, master=root)
# drawPic.canvas.show()
# drawPic.canvas.get_tk_widget().grid(row=2, columnspan=8)
# #放置标签、文本框和按钮等部件，并设置文本框的默认值和按钮的事件函数
# Label(root,text='股价走势图：').grid(row=1,column=0)
# inputEntry=Entry(root)
# inputEntry.grid(row=1,column=1)
# inputEntry.insert(0,'50')
# Button(root,text='数据一',command=data1).grid(row=1,column=1,columnspan=3)
