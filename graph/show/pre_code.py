#使用pyqt4
import matplotlib
matplotlib.use("Qt4Agg")
from matplotlib import dates
from matplotlib.finance import candlestick_ohlc
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FuncFormatter
from Tkinter import *
from pylab import *
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
import tushare as ts

#使用tushare作为数据源,code为股票,start和en为起始结束
raw_data = ts.get_h_data('601928',start='2016-02-01',end = '2016-04-01')

#定义横坐标格式的回调函数
def my_major_formatter(x,pos):
    for i in range(num):
        if(x == i):
            return str_date[i]

#将数据加工处理
num = len(raw_data)
title = list(raw_data.columns.values)
day = list(raw_data.index.values)
data = []
line = []
value = []
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
    value.append(raw_data.iloc[i][2]-10)

#绘图部分
fig= plt.figure(figsize = (9,6),dpi = 150,facecolor='#F0F8FF')

#备用代码
# fig.subplots_adjust(bottom=0.2)
# yearsFmt = dates.DateFormatter('%Y-%m-%d')
# dayFmt = dates.DateFormatter('%Y-%m-%d')
# ax1.xaxis.set_major_formatter(yearsFmt)
# ax1.xaxis.set_minor_formatter(dayFmt)
# ax1.set_xticklabels(xdays, rotation=25, horizontalalignment='right')
# plt.bar(value)

#子图一
ax1 = fig.add_axes([0.1,0.35,0.8,0.6])
# ax1.set_xticks(range(num))
xmajorLocator   = MultipleLocator(3) #将x主刻度标签设置为3的倍数
ax1.xaxis.set_major_locator(xmajorLocator)
ax1.xaxis.set_major_formatter(FuncFormatter(my_major_formatter))
ax1.grid()
for tick in ax1.xaxis.get_major_ticks():
    tick.label1.set_fontsize(10)
    tick.label1.set_rotation(30)
candlestick_ohlc(ax1, data, width=0.6,colorup='r', colordown='g')

#子图二
ax2 = fig.add_axes([0.1,0.1,0.8,0.18])
ax2.set_xticks(range(num))
ax2.set_xticklabels(str_date, rotation=25, horizontalalignment='right')
bar = ax2.bar(range(num), value, picker=True, color='#FFFF00')
ax2.xaxis.set_major_locator(xmajorLocator)
ax2.xaxis.set_major_formatter(FuncFormatter(my_major_formatter))
for label in ax2.get_xticklabels():
    label.set_picker(True)

#响应按钮并连接
def _onpick1(event):
    print 123
fig.canvas.mpl_connect('pick_event', _onpick1)

def draw():
    fig.clf()

#绘制

# plt.show()
