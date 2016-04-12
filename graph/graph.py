# -*- encoding:utf-8 -*-
import matplotlib.pyplot as plt
import xlrd
from pylab import *
import datetime
import matplotlib.dates as mdates
from matplotlib import dates
from matplotlib.finance import *
import time,datetime
mpl.rcParams['font.sans-serif'] = ['SimHei'] #指定默认字体
mpl.rcParams['axes.unicode_minus'] = False #解决保存图像是负号'-'显示为方块的问题

def excel():
    data1 = xlrd.open_workbook(u'300017.xlsx')
    table1 = data1.sheet_by_name(u'300017')
    data2 = xlrd.open_workbook(u'300019.xlsx')
    table2 = data2.sheet_by_name(u'300019')
    a = table1.col_values(0)
    b = table1.col_values(1)
    c = table2.col_values(1)
    x = []
    y = []
    z = []
    for each in a:
        if(each == ''):
          break
        date = xlrd.xldate_as_tuple(each,0)
        d = str(date[0]) + "-" + str(date[1]) + "-" + str(date[2])
        x.append(d)
    for each in b:
        if(each == ''):
          break
        y.append(float(each))
    for each in c:
        if(each == ''):
          break
        z.append(float(each))
    return x,y,z

def hey():
    x=[1,2,3,4]
    y=[5,4,3,2]
    plt.figure()
    plt.subplot(231)
    plt.plot(x,y)
    plt.subplot(232)
    plt.bar(x,y)
    plt.subplot(233)
    plt.barh(x,y)
    plt.subplot(234)
    plt.bar(x,y)
    y1=[7,8,5,3]
    plt.bar(x,y1,bottom=y,color='r')
    plt.subplot(235)
    plt.boxplot(x)
    #绘制盒图
    plt.subplot(236)
    plt.scatter(x,y)
    plt.show()

def have_a_try():
    x = []
    y = []
    z = []
    day,y,z = excel()
    fig = plt.figure()

    plt.annotate(u'值得关注', xy=(50, 100), xytext=(90, 90),
            arrowprops=dict(facecolor='black', shrink=0.05),
            )

    fig.suptitle(u'股价',fontsize =15,fontweight = 'bold')
    ax = fig.add_subplot(1,1,1)
    # plt.xticks(range(len(x)),x)
    # ax.set_xticks([0,50,100,150,200,244])
    from matplotlib.dates import AutoDateLocator, DateFormatter
    m = datetime.datetime.strptime('2013-2-2', '%Y-%m-%d')
    n = m.date()
    x = [datetime.datetime.strptime(d, '%Y-%m-%d').date() for d in day]

    yearsFmt = mdates.DateFormatter('%Y-%m-%d')
    ax.xaxis.set_major_formatter(yearsFmt)
    # ax.xaxis.
    # date = map(dates.date2num,x)
    # autodates = AutoDateLocator()
    # ax.set_xticklabels(x,fontsize = 13)
    # x = range(len(x))
    date1 = (2015, 4, 3)
    date2 = (2015, 10, 6)
    quotes = quotes_historical_yahoo_ohlc('AAPL', date1, date2)
    candlestick_ohlc(ax, quotes, width=0.6, colorup='r', colordown='g')

    ax.set_title(u'300018.SZ',fontsize = 8)
    ax.set_xlabel(u'时间')
    ax.set_ylabel(u'价格')
    plt.plot(x,y)
    plt.plot(x,z)
    plt.grid(True)
    fig.autofmt_xdate()
    plt.legend(['300017','300018'])
    plt.show()

def time():
    x = datetime.date(2015,5,3)
    return x

def book():
    fig = plt.figure()
    plt.xticks((0,1,2),['201322','201333','201433'])
    x = [0,1,2]
    y = [2,3,4]
    plt.plot(x,y)
    plt.show()
if __name__ == '__main__':
    have_a_try()