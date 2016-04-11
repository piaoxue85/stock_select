#-*- encoding:utf8 -*-
import datetime
import matplotlib.pyplot as plt
from matplotlib import dates
from matplotlib.finance import candlestick_ohlc
from matplotlib.ticker import MultipleLocator
import tushare as ts
x = ts.get_h_data('601928',start='2016-03-01',end = '2016-04-01')


y = len(x)
title = list(x.columns.values)
day = list(x.index.values)
z = []
line = []
value = []
d = [datetime.datetime.utcfromtimestamp(each.tolist()/1e9) for each in day]
str_d = [item.isoformat()[5:10] for item in d]
dd = [dates.date2num(each) for each in d]
d.reverse()
dd.reverse()
str_d.reverse()
xdays = str_d

for i in range(y):
    z.append((y-i,x.iloc[i][0],x.iloc[i][1],x.iloc[i][3],x.iloc[i][2]))
    line.append(y-i)
    value.append(x.iloc[i][2] - 10)
value.reverse()
fig= plt.figure()
ax1 = fig.add_axes([0.1,0.35,0.8,0.6])
ax2 = fig.add_axes([0.1,0.1,0.8,0.18])
fig.subplots_adjust(bottom=0.2)
# yearsFmt = dates.DateFormatter('%Y-%m-%d')
# dayFmt = dates.DateFormatter('%Y-%m-%d')
# ax1.xaxis.set_major_formatter(yearsFmt)
# ax1.xaxis.set_minor_formatter(dayFmt)
fig.autofmt_xdate()
length = len(xdays)
ax1.set_xticks(range(length))
ax1.set_xticklabels(xdays, rotation=25, horizontalalignment='right')
xmajorLocator   = MultipleLocator(2) #将x主刻度标签设置为20的倍数
ax1.xaxis.set_major_locator(xmajorLocator)

# ax1.set_xticks([0,length/8,length/8 * 2,length/8 * 3,length/8 * 4,length/8 * 5,length/8 * 6,length/8 * 7,length-1])
ax2.set_xticks(range(length))
ax2.set_xticklabels(xdays, rotation=25, horizontalalignment='right')
# ax2.set_xticks([0,length/8,length/8 * 2,length/8 * 3,length/8 * 4,length/8 * 5,length/8 * 6,length/8 * 7,length-1])

ax2.bar(range(length),value)
# plt.bar(value)
candlestick_ohlc(ax1, z, width=0.6,colorup='r', colordown='g')
plt.show()

def my_formatter(x,pos):
    for i in range(len(xdays)):
        if(x == i):
            return xdays[i]