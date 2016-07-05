# -*- encoding:utf8 -*-
# 开始重新整理代码
# 系统包
import sys
import datetime
import time
# Pyqt4包
import PyQt4
from PyQt4 import QtCore
from PyQt4.QtGui import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QSizePolicy, QWidget, QLabel, QLineEdit, QDateEdit, QPushButton, QKeyEvent, QTreeWidget, QListWidget,QTreeWidgetItem
# matplotlib包
import matplotlib
from matplotlib import dates
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.ticker import MultipleLocator, FuncFormatter
from matplotlib.finance import candlestick_ohlc
from matplotlib.figure import Figure
# Tushare 获取股票数据
# import tushare as ts
# Mongodb 要打开服务才能使用
from pymongo import MongoClient

matplotlib.rcParams['font.sans-serif'] = ['SimHei'] #指定默认字体
matplotlib.rcParams['axes.unicode_minus'] = False #解决保存图像是负号'-'显示为方块的问题

# EMA的计算公式,证明是有问题的，并不能这样子做，因为从券商的数据来看，EMA都是从开盘日算起的,所以还是使用万得的数据

import WindPy


# time = x.Times
print 123
def ema(x,n):
    if n is 1:
        return float(x[-1])
    return float(2*x[-1]+(n-1)*ema(x[:-1],n-1))/(n + 1)

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
# 使用tushare作为数据源,code为股票,start和en为起始结束,事实发现tushare还是有问题的，所以决定改用万得



def source(code = '601928',start = '2016-03-25', end = '2016-05-04'):
    CFFEXlist = []
    SHFElist = []
    DCElist = []
    CZCElist = []
    CFFEX = "IF.CFE,IH.CFE,IC.CFE,TF.CFE,T.CFE,TT.CFE,AF.CFE,EF.CFE,"
    SHFE = "CU.SHF,AL.SHF,ZN.SHF,PB.SHF,AU.SHF,AG.SHF,RB.SHF,RU.SHF,FU.SHF,WR.SHF,BU.SHF,HC.SHF,NI.SHF,SN.SHF,IM.SHF"
    DCE = "A.DCE,M.DCE,Y.DCE,P.DCE,C.DCE,I.DCE,JM.DCE,J,DCE,L.DCE,V.DCE,B.DCE,JD.DCE,FB.DCE,BB.DCE,PP.DCE,CS.DCE"
    CZCE = "WH.CZC,OI,CZC,CF.CZC,SR.CZC,RI.CZC,ZC.CZC,TA.CZC,FG.CZC,MA.CZC,RM.CZC,RS.CZC,PM.CZC,JR.CZC,LR.CZC,SM.CZC,SF.CZC"
    CFFEXlist = CFFEX.split(",")
    SHFElist = SHFE.split(",")
    DCElist = DCE.split(",")
    CZCElist = CZCE.split(",")
    CFFEXcode = code + ".CFE"
    SHFEcode = code + ".SHF"
    DCEcode = code + ".DCE"
    CZCEcode = code + ".CZC"
    if CFFEXcode in CFFEXlist:
        code = CFFEXcode
    if SHFEcode in SHFElist:
        code = SHFEcode
    if DCEcode in DCElist:
        code = DCEcode
    if CZCEcode in CZCElist:
        code = CZCEcode

    ema = []
    kbar = []
    str_date = []
    volume = []
    WindPy.w.start()
    data = WindPy.w.wsd(code, "open,high,low,close,EXPMA,sec_name", start, end,"Fill=Previous;EXPMA_N=10")
    data_volume = WindPy.w.wsd(code, "volume", start, end, "Fill=Previous")
    num  = len(data.Times)
    name = data.Data[5][0]
    for i in range(num):
        kbar.append((i,data.Data[0][i], data.Data[1][i], data.Data[2][i], data.Data[3][i]))
        ema.append(data.Data[4][i])
        str_date.append(data.Times[i].isoformat()[5:10])
        volume.append(data_volume.Data[0][i])
    return num,kbar,str_date,ema,name,volume

# 将matplotlib的一个组件放进去


class MyMplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=9, height=6, dpi=150):
        self.fig = Figure(figsize=(width, height), dpi=dpi,facecolor='#F0F8FF')
        self.ax1 = self.fig.add_axes([0.22, 0.1, 0.7, 0.7])
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
    con = MongoClient('172.19.20.38:27017')
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
        self.treeWidget = QTreeWidget(self.widget)
        self.horizontalLayout.addWidget(self.treeWidget)
        self.label_1 = QLabel(self.widget)
        self.horizontalLayout.addWidget(self.label_1)
        self.label_2 = QLabel(self.widget )
        self.lineEdit = QLineEdit(self.widget)
        self.horizontalLayout.addWidget(self.lineEdit)
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
        self.lineEdit.setText(QtCore.QString('M'))
        three_month = QtCore.QDate.currentDate().toJulianDay() - 60
        self.dateEdit.setDate(QtCore.QDate.fromJulianDay(three_month))
        self.dateEdit_2.setDate(QtCore.QDate.currentDate())
        self.button1.clicked.connect(self.get_value)
        self.button2.clicked.connect(self.clear)

        self.treeWidget.headerItem().setText(0, _translate("MainWindow", "期货品种", None))
        self.root1 = QTreeWidgetItem(self.treeWidget)
        self.root1.setText(0, _translate("MainWindow", "中金所", None))
        self.root2 = QTreeWidgetItem(self.treeWidget)
        self.root2.setText(0, _translate("MainWindow", "上海期货", None))
        self.root3 = QTreeWidgetItem(self.treeWidget)
        self.root3.setText(0, _translate("MainWindow", "大连商品", None))
        self.root4 = QTreeWidgetItem(self.treeWidget)
        self.root4.setText(0, _translate("MainWindow", "郑州商品", None))
        self.child11 = QTreeWidgetItem(self.root1)
        self.child12 = QTreeWidgetItem(self.root1)
        self.child13 = QTreeWidgetItem(self.root1)
        self.child14 = QTreeWidgetItem(self.root1)
        self.child15 = QTreeWidgetItem(self.root1)
        self.child16 = QTreeWidgetItem(self.root1)
        self.child17 = QTreeWidgetItem(self.root1)
        self.child18 = QTreeWidgetItem(self.root1)
        self.child11.setText(0, _translate("MainWindow", "CFFEX 沪深300指数期货(IF)", None))
        self.child12.setText(0, _translate("MainWindow", "CFFEX 上证50指数期货(IH)", None))
        self.child13.setText(0, _translate("MainWindow", "CFFEX 中证500指数期货(IC)", None))
        self.child14.setText(0, _translate("MainWindow", "CFFEX 5年期国债期货(TF)", None))
        self.child15.setText(0, _translate("MainWindow", "CFFEX 10年期国债期货(T)", None))
        self.child16.setText(0, _translate("MainWindow", "CFFEX 3年期国债期货（仿真）(TT)", None))
        self.child17.setText(0, _translate("MainWindow", "CFFEX 澳元兑美元（AUDUSD）期货（仿真）(AF)", None))
        self.child18.setText(0, _translate("MainWindow", "CFFEX 欧元兑美元（EURUSD）期货（仿真）(EF)", None))
        self.child21 = QTreeWidgetItem(self.root2)
        self.child22 = QTreeWidgetItem(self.root2)
        self.child23 = QTreeWidgetItem(self.root2)
        self.child24 = QTreeWidgetItem(self.root2)
        self.child25 = QTreeWidgetItem(self.root2)
        self.child26 = QTreeWidgetItem(self.root2)
        self.child27 = QTreeWidgetItem(self.root2)
        self.child28 = QTreeWidgetItem(self.root2)
        self.child29 = QTreeWidgetItem(self.root2)
        self.child210 = QTreeWidgetItem(self.root2)
        self.child211 = QTreeWidgetItem(self.root2)
        self.child212 = QTreeWidgetItem(self.root2)
        self.child213 = QTreeWidgetItem(self.root2)
        self.child214 = QTreeWidgetItem(self.root2)
        self.child21.setText(0, _translate("MainWindow", "SHFE 铜(CU)", None))
        self.child22.setText(0, _translate("MainWindow", "SHFE 铝(AL)", None))
        self.child23.setText(0, _translate("MainWindow", "SHFE 铅(ZN)", None))
        self.child24.setText(0, _translate("MainWindow", "SHFE 黄金(AU)", None))
        self.child25.setText(0, _translate("MainWindow", "SHFE 白银(AG)", None))
        self.child26.setText(0, _translate("MainWindow", "SHFE 螺纹钢(RB)", None))
        self.child27.setText(0, _translate("MainWindow", "SHFE 橡胶(RU)", None))
        self.child28.setText(0, _translate("MainWindow", "SHFE 燃油(FU)", None))
        self.child29.setText(0, _translate("MainWindow", "SHFE 线材(WR)", None))
        self.child210.setText(0, _translate("MainWindow", "SHFE 石油沥青(BU)", None))
        self.child211.setText(0, _translate("MainWindow", "SHFE 热轧卷板(HC)", None))
        self.child212.setText(0, _translate("MainWindow", "SHFE 镍(NI)", None))
        self.child213.setText(0, _translate("MainWindow", "SHFE 锡(SN)", None))
        self.child214.setText(0, _translate("MainWindow", "SHFE 上期有色金属指数期货（仿真）(IM)", None))
        self.child31 = QTreeWidgetItem(self.root3)
        self.child32 = QTreeWidgetItem(self.root3)
        self.child33 = QTreeWidgetItem(self.root3)
        self.child34 = QTreeWidgetItem(self.root3)
        self.child35 = QTreeWidgetItem(self.root3)
        self.child36 = QTreeWidgetItem(self.root3)
        self.child37 = QTreeWidgetItem(self.root3)
        self.child38 = QTreeWidgetItem(self.root3)
        self.child39 = QTreeWidgetItem(self.root3)
        self.child310 = QTreeWidgetItem(self.root3)
        self.child311 = QTreeWidgetItem(self.root3)
        self.child312 = QTreeWidgetItem(self.root3)
        self.child313 = QTreeWidgetItem(self.root3)
        self.child314 = QTreeWidgetItem(self.root3)
        self.child31.setText(0, _translate("MainWindow", "DCE 豆一(A)", None))
        self.child32.setText(0, _translate("MainWindow", "DCE 豆粕(M)", None))
        self.child33.setText(0, _translate("MainWindow", "DCE 豆油(Y)", None))
        self.child34.setText(0, _translate("MainWindow", "DCE 棕榈油(P)", None))
        self.child35.setText(0, _translate("MainWindow", "DCE 玉米(C)", None))
        self.child36.setText(0, _translate("MainWindow", "DCE 铁矿石(I)", None))
        self.child37.setText(0, _translate("MainWindow", "DCE 焦炭(JM)", None))
        self.child38.setText(0, _translate("MainWindow", "DCE PVC(V)", None))
        self.child39.setText(0, _translate("MainWindow", "DCE 豆二(B)", None))
        self.child310.setText(0, _translate("MainWindow", "DCE 鸡蛋(JD)", None))
        self.child311.setText(0, _translate("MainWindow", "DCE 纤维板(FB)", None))
        self.child312.setText(0, _translate("MainWindow", "DCE 胶合板(BB)", None))
        self.child313.setText(0, _translate("MainWindow", "DCE 聚丙烯(PP)", None))
        self.child314.setText(0, _translate("MainWindow", "DCE 玉米淀粉(CS)", None))
        self.child41 = QTreeWidgetItem(self.root4)
        self.child42 = QTreeWidgetItem(self.root4)
        self.child43 = QTreeWidgetItem(self.root4)
        self.child44 = QTreeWidgetItem(self.root4)
        self.child45 = QTreeWidgetItem(self.root4)
        self.child46 = QTreeWidgetItem(self.root4)
        self.child47 = QTreeWidgetItem(self.root4)
        self.child48 = QTreeWidgetItem(self.root4)
        self.child49 = QTreeWidgetItem(self.root4)
        self.child410 = QTreeWidgetItem(self.root4)
        self.child411 = QTreeWidgetItem(self.root4)
        self.child412 = QTreeWidgetItem(self.root4)
        self.child413 = QTreeWidgetItem(self.root4)
        self.child414 = QTreeWidgetItem(self.root4)
        self.child415 = QTreeWidgetItem(self.root4)
        self.child416 = QTreeWidgetItem(self.root4)
        self.child41.setText(0, _translate("MainWindow", "CZCE 强麦(WH)", None))
        self.child42.setText(0, _translate("MainWindow", "CZCE 菜油(OI)", None))
        self.child43.setText(0, _translate("MainWindow", "CZCE 棉花(CF)", None))
        self.child44.setText(0, _translate("MainWindow", "CZCE 白糖(SR)", None))
        self.child45.setText(0, _translate("MainWindow", "CZCE 早籼稻(RI)", None))
        self.child46.setText(0, _translate("MainWindow", "CZCE 动力煤(ZC)", None))
        self.child47.setText(0, _translate("MainWindow", "CZCE PTA(TA)", None))
        self.child48.setText(0, _translate("MainWindow", "CZCE 玻璃(FG)", None))
        self.child49.setText(0, _translate("MainWindow", "CZCE 甲醇(MA)", None))
        self.child410.setText(0, _translate("MainWindow", "CZCE 菜籽油(RM)", None))
        self.child411.setText(0, _translate("MainWindow", "CZCE 油菜籽(RS)", None))
        self.child412.setText(0, _translate("MainWindow", "CZCE 普麦(PM)", None))
        self.child413.setText(0, _translate("MainWindow", "CZCE 粳稻(JR)", None))
        self.child414.setText(0, _translate("MainWindow", "CZCE 晚籼稻(LR)", None))
        self.child415.setText(0, _translate("MainWindow", "CZCE 锰硅(SM)", None))
        self.child416.setText(0, _translate("MainWindow", "CZCE 硅铁(LR)", None))
        # self.treeWidget.addTopLevelItem(self.root)
        # self.treeWidget.addTopLevelItem(self.root)
        self.label_1.setText(_translate("MainWindow", "期货品种", None))
        self.label_2.setText(_translate("MainWindow", "起始时间", None))
        self.label_3.setText(_translate("MainWindow", "终止时间", None))
        self.button1.setText(_translate("MainWindow", "提交", None))
        self.button2.setText(_translate("MainWindow", "清除", None))
    def keyPressEvent(self, event):
        keyEvent = QKeyEvent(event)
        if keyEvent.key() == QtCore.Qt.Key_Enter or keyEvent.key() == QtCore.Qt.Key_Return:
            self.get_value()
        if keyEvent.key() == QtCore.Qt.Key_0:
            self.get_value()

    # 定义横坐标格式的回调函数
    def my_major_formatter(self, x, pos):
        for i in range(self.num):
            if (x == i):
                return self.str_date[i]

    def get_value(self):
        code = QtCore.QString(self.lineEdit.text())
        start = QtCore.QString(self.dateEdit.text())
        end = QtCore.QString(self.dateEdit_2.text())
        code = unicode(code)
        start = datetime.date(int(start.split("/")[0]), int(start.split("/")[1]), int(start.split("/")[2])).isoformat()
        end = datetime.date(int(end.split("/")[0]), int(end.split("/")[1]), int(end.split("/")[2])).isoformat()

        self.num, self.kbar, self.str_date, self.ema, self.name, self.volume= source(code, start, end)
        self.star_date, self.star_value = star(col, code, start, end)
        self.update_figure()
    def update_figure(self):

        self.fig.clf()
        self.ax1 = self.fig.add_axes([0.22, 0.1, 0.7, 0.7])
        self.ax2 = self.ax1.twinx()  # 创建第二个坐标轴,为同图
        # 子图一
        WindPy.w.start()
        self.ax1.set_xticks(range(self.num))
        xmajorLocator = MultipleLocator(5)  # 将x主刻度标签设置为3的倍数
        xminorLocator = MultipleLocator(1)  # 将x副刻度标签设置为1的倍数
        self.ax1.xaxis.set_major_locator(xmajorLocator)
        self.ax1.xaxis.set_minor_locator(xminorLocator)
        self.ax1.xaxis.set_major_formatter(FuncFormatter(self.my_major_formatter))
        self.ax1.grid()

        # self.ax2.bar(range(len(self.star_date)), self.star_value, picker=True, color='#FFFF00', width = 0.5,edgecolor = 'black')
        self.ax1.plot(range(self.num),self.ema,linewidth = 0.5,color = "blue")
        self.ax2.bar(range(self.num),self.volume)
        from matplotlib.font_manager import FontProperties
        font = FontProperties(size=14)  # 设置字体
        self.ax1.set_title(self.name)
        self.ax1.set_ylabel(u'价格')
        # self.ax2.set_ylabel(u'星数')
        #极端情况1
        # high_1 = self.kbar[0][2]
        # low_1 = self.kbar[0][3]
        # ema_1 = self.ema[0]
        # deviate_1 = max(abs(high_1 - ema_1),abs(low_1 - ema_1))
        # high_2 = self.kbar[1][2]
        # low_2 = self.kbar[1][3]
        # ema_2 = self.ema[1]
        # deviate_2 = max(abs(high_2 - ema_2),abs(low_2 - ema_2))
        # high_3 = self.kbar[2][2]
        # low_3 = self.kbar[2][3]
        # ema_3 = self.ema[2]
        # deviate_3 = max(abs(high_3 - ema_3),abs(low_3 - ema_3))
        # high_4 = self.kbar[3][2]
        # low_4 = self.kbar[3][3]
        # ema_4 = self.ema[3]
        # deviate_4 = max(abs(high_4 - ema_4),abs(low_4 - ema_4))
        # high_5 = self.kbar[4][2]
        # low_5 = self.kbar[4][3]
        # ema_5 = self.ema[4]
        # deviate_5 = max(abs(high_5 - ema_5),abs(low_5 - ema_5))
        # high_6 = self.kbar[5][2]
        # low_6 = self.kbar[5][3]
        # ema_6 = self.ema[5]
        # deviate_6 = max(abs(high_6 - ema_6),abs(low_6 - ema_6))
        # for i in range(6,self.num):
        #     high_7 = self.kbar[i][2]
        #     low_7 = self.kbar[i][3]
        #     ema_7 = self.ema[i]
        #     deviate_7 = max(abs(high_7 - ema_7),abs(low_7 - ema_7))
        #     condition1 = deviate_5 > deviate_3 > deviate_2 > deviate_1 or deviate_4 > deviate_3 > deviate_2 > deviate_1
        #     condition2 = ema_5 > ema_4 > ema_3 > ema_2 > ema_1 or ema_1 > ema_2 > ema_3 > ema_4 > ema_5
        #     condition3 = deviate_5 > deviate_6 > deviate_7
        #     if condition1 and condition2 and condition3 :
        #         self.ax1.annotate('E', xy=(i, low_7), xytext=(i+ 1, low_7+0.5), arrowprops=dict(arrowstyle="->"))
        #     deviate_1 = deviate_2
        #     deviate_2 = deviate_3
        #     deviate_3 = deviate_4
        #     deviate_4 = deviate_5
        #     deviate_5 = deviate_6
        #     deviate_6 = deviate_7
        #     ema_1 = ema_2
        #     ema_2 = ema_3
        #     ema_3 = ema_4
        #     ema_4 = ema_5
        #     ema_5 = ema_6
        #     ema_6 = ema_7
        # 极端情况2
        high_1 = self.kbar[0][2]
        low_1 = self.kbar[0][3]
        ema_1 = self.ema[0]
        deviate_1 = max(abs(high_1 - ema_1),abs(low_1 - ema_1))
        high_2 = self.kbar[1][2]
        low_2 = self.kbar[1][3]
        ema_2 = self.ema[1]
        deviate_2 = max(abs(high_2 - ema_2),abs(low_2 - ema_2))
        high_3 = self.kbar[2][2]
        low_3 = self.kbar[2][3]
        ema_3 = self.ema[2]
        deviate_3 = max(abs(high_3 - ema_3),abs(low_3 - ema_3))
        high_4 = self.kbar[3][2]
        low_4 = self.kbar[3][3]
        ema_4 = self.ema[3]
        deviate_4 = max(abs(high_4 - ema_4), abs(low_4 - ema_4))
        high_5 = self.kbar[3][2]
        low_5 = self.kbar[3][3]
        ema_5 = self.ema[3]
        deviate_5 = max(abs(high_5 - ema_5), abs(low_5 - ema_5))
        lim1 = self.ax1.get_ylim()
        # distance = 0.3
        distance = (lim1[1] - lim1[0])/9
        for i in range(5,self.num):
            alpha = 1.10
            beta = 0.90
            high_6 = self.kbar[i][2]
            low_6 = self.kbar[i][3]
            ema_6 = self.ema[i]
            deviate_6 = max(abs(high_6 - ema_6),abs(low_6 - ema_6))
            condition1 = deviate_4 > deviate_3 > deviate_2 or deviate_4 > deviate_3 > deviate_1 or deviate_4 > deviate_2 > deviate_1
            condition2 = ema_4 > ema_3 > ema_2 or ema_2 > ema_3 > ema_4
            condition3 = deviate_4 > deviate_5 * beta and deviate_4 > deviate_6
            top = high_4 - ema_4
            bottom = ema_4 - low_4
            condition4 = (low_4 < low_5 * alpha and low_4 < low_6 and top < bottom) or (high_4 > high_5 * beta and high_4 > high_6 and top > bottom)
            condition5 = top < bottom
            condition6 = top > bottom
            condition7 = high_3 < ema_3 and high_4 < ema_4 and high_5 < ema_5 and high_6 > ema_6 * alpha
            condition8 = low_3 > ema_3 and low_4 > ema_4 and low_5 > ema_5 and low_6 < ema_6 * beta
            matplotlib.rcParams.update({'font.size': 9})
            if condition1 and condition2 and condition3 and condition4 and condition5 or condition7:
                self.ax1.annotate(u'多', xy=(i, low_6), xytext=(i-0.5, low_6 - distance), arrowprops=dict(arrowstyle="-"))
            if condition1 and condition2 and condition3 and condition4 and condition6 or condition8:
                self.ax1.annotate(u'空', xy=(i, high_6), xytext=(i-0.5, high_6 + distance), arrowprops=dict(arrowstyle="-"))
            deviate_1 = deviate_2
            deviate_2 = deviate_3
            deviate_3 = deviate_4
            deviate_4 = deviate_5
            deviate_5 = deviate_6
            ema_1 = ema_2
            ema_2 = ema_3
            ema_3 = ema_4
            ema_4 = ema_5
            ema_5 = ema_6
            low_1 = low_2
            low_2 = low_3
            low_3 = low_4
            low_4 = low_5
            low_5 = low_6
            high_1 = high_2
            high_2 = high_3
            high_3 = high_4
            high_4 = high_5
            high_5 = high_6
        # self.ax1.annotate('extreme', xy=(18, 16.8), xytext=(20, 16), arrowprops=dict(arrowstyle="->"))
        # self.ax2.set_ylim(0, 80)
        candlestick_ohlc(self.ax1, self.kbar, width=0.5, colorup='r', colordown='g')
        # self.ax1.hold(False)
        # self.ax2.hold(False)
        lim = self.ax1.get_ylim()
        self.ax1.set_ylim(lim[0] * 0.95, lim[1])
        lim2 = self.ax2.get_ylim()
        self.ax2.set_ylim(lim2[0],lim2[1]*8)
        for tick in self.ax1.xaxis.get_major_ticks():
            tick.label1.set_fontsize(8)
            tick.label1.set_rotation(75)
        for tick in self.ax1.yaxis.get_major_ticks():
            tick.label1.set_fontsize(8)
            tick.label1.set_rotation(30)
        # for tick in self.ax2.xaxis.get_major_ticks():
        #     tick.label1.set_fontsize(8)
        #     tick.label1.set_rotation(75)
        # for tick in self.ax2.yaxis.get_major_ticks():
        #     tick.label1.set_fontsize(8)
        #     tick.label1.set_rotation(30)
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


    def clear(self):
        self.fig.clf()
        self.ax1 = self.fig.add_axes([0.22, 0.1, 0.7, 0.7])
        # self.ax1 = self.fig.add_axes([0.1, 0.35, 0.8, 0.58])
        # self.ax2 = self.fig.add_axes([0.1, 0.07, 0.8, 0.2])
        self.draw()
class ApplicationWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("Future select graph")

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

    def keyPressEvent(self, event):
        keyEvent = QKeyEvent(event)
        if keyEvent.key() == QtCore.Qt.Key_Enter or keyEvent.key() == QtCore.Qt.Key_Return:
            self.qmc.get_value()
        if keyEvent.key() == QtCore.Qt.Key_0:
            self.get_value()
class SlaveWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle("Future select graph")

        self.main_widget = QWidget(self)

        self.vbl = QVBoxLayout(self.main_widget)
        self.qmc = sub_canvas(self.main_widget, width=9, height=6, dpi=200)
        self.ntb = NavigationToolbar(self.qmc, self.main_widget)

        self.vbl.addWidget(self.qmc)
        # self.vbl.addWidget(self.widget)
        self.vbl.addWidget(self.ntb)
        self.setGeometry(100, 100, 1600, 900)
        self.main_widget.setFocus()
        # self.setInputContext(self.main_widget)
# app = QApplication(sys.argv)
# aw = ApplicationWindow()
# aw.show()
# widget = QWidget()
# app.exec_()
# app = QApplication(sys.argv)
# aw = SlaveWindow()
# aw.show()
# app.exec_()

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
