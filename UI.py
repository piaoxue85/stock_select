#-*- encoding:utf-8 -*-
from Tkinter import *
import tkMessageBox
import stock_select
import os
def execute():
    os.getcwd()
    os.system(u"策略.xlsx".encode('gbk'))
def indro():
    text = u"由于出季报时间不齐，当季以上季度为基准\n" \
           u"策略一：营收季增率当季大于上季\n" \
           u"策略二：EPS季增率当季大于上季\n" \
           u"策略三：毛利率季增率当季大于上季\n" \
           u"策略四：ROE季增率当季大于上季\n\n" \
           u"策略五：波动率今天的10MA>前一天10MA,同时今天10MA>100MA(波动率的算法：第T天的波动率以（T-10,T]为区间算出的波动率,之后再取MA)\n\n" \
           u"策略六：当天10MA大于前一天10MA，同时前一天10MA大于前两天10MA。即是10MA连续两天上扬\n\n" \
           u"策略七：日线10MA上扬，周线10MA上扬，月线10MA上扬\n\n" \
           u"策略八：日线10MA上扬\n" \
           u"策略九：周线10MA上扬\n" \
           u"策略十：月线10MA上扬\n\n" \
           u"策略十一：过去60天、180天、250天波动的区间分别在30%、50%、100%之内，即最高价与最低价的范围,最高最低包括了盘中价格，非收盘价\n\n" \
           u"策略十二：过去60天波动小于30%\n" \
           u"策略十三：过去180天波动小于50%\n" \
           u"策略十四：过去250天波动小于100%\n" \
           u"注意：过去60、180、250天专指交易日,11、12、13、14策略表头日期代表开始的时间节点\n\n" \
           u"策略十五：融资余额的前一天10MA大于前两天的10MA，同时前一天10MA大于前一天的30MA（由于万得终端收盘后也接收不到最新融资余额）\n\n" \
           u"策略十六：户均持股前三季中有一次增加\n" \
           u"策略十七：股东户数连续两季减少\n" \
           u"策略十八：十大股东变化数量超过3个\n" \
           u"策略十九：十大股东持股比例增加\n" \
           u"策略二十：券商持股、基金持股、机构持股分别排序\n" \
           u"策略二十三：换手率今日5MA大于前一日5MA，今日10MA大于前一日10MA\n"
    tkMessageBox.showinfo(title=u'策略说明', message=text)
def guide():
    text = u"本版本为选股生成器V1.2，数据源来自万得python接口\n" \
           u"copyright@陈秋远,邮箱380133194@qq.com\n" \
           u"本版本使用说明：\n" \
           u"每点击一个策略将会在名为”策略”的excel中生成sheet，其中一个名为“股票”的sheet是总表，选出的股票按照顺序按列占据位置。\n" \
           u"另一个sheet为该策略的一些具体数据\n" \
           u"点击“执行所有策略”将执行所有策略，耗时较长请耐心等待。“股票”sheet会呈现所有股票，所有策略的子sheet也会生成\n"
    tkMessageBox.showinfo(title=u'使用说明', message=text)
root=Tk()
root.geometry('600x600+0+0')
# Grid 网格布局
l1 = Label(root, text = u'股票池生成器V1.2')
l1.grid(row = 0, column = 0)
la = Label(root, text = u'公司价值')
la.grid(row = 1, column = 0)
lb = Label(root, text = u'筹码分布')
lb.grid(row = 1, column = 1)
lc = Label(root, text = u'市场波动')
lc.grid(row = 1, column = 2)
ld = Label(root, text = u'操作')
ld.grid(row = 1, column = 3)
le = Label(root, text = u'说明')
le.grid(row = 1, column = 4)
#公司价值
Button(root,text=u'策略1:营收季增率', command = stock_select.strategy1).grid(row=2,column=0)
Button(root,text=u'策略2:EPS季增率', command = stock_select.strategy2).grid(row=3,column=0)
Button(root,text=u'策略3:毛利率季增率', command = stock_select.strategy3).grid(row=4,column=0)
Button(root,text=u'策略4:ROE季增率', command = stock_select.strategy4).grid(row=5,column=0)
#筹码分布
Button(root,text=u'策略15:融资余额', command = stock_select.strategy15).grid(row=2,column=1)
Button(root,text=u'策略16:户均持股', command = stock_select.strategy16).grid(row=3,column=1)
Button(root,text=u'策略17:股东户数', command = stock_select.strategy17).grid(row=4,column=1)
Button(root,text=u'策略18:十大股东变化数量', command = stock_select.strategy18).grid(row=5,column=1)
Button(root,text=u'策略19:十大股东持股比例', command = stock_select.strategy19).grid(row=6,column=1)
Button(root,text=u'策略20:券商、基金、机构持股', command = stock_select.strategy202122).grid(row=7,column=1)
Button(root,text=u'策略23:换手率', command = stock_select.strategy23).grid(row=8,column=1)
#市场波动
Button(root,text=u'策略5:波动率', command = stock_select.strategy5).grid(row=2,column=2)
Button(root,text=u'策略6:价格', command = stock_select.strategy6).grid(row=3,column=2)
Button(root,text=u'策略7:日周月10MA', command = stock_select.strategy7).grid(row=4,column=2)
Button(root,text=u'策略8:日线10MA', command = stock_select.strategy8).grid(row=5,column=2)
Button(root,text=u'策略9:周线10MA', command = stock_select.strategy9).grid(row=6,column=2)
Button(root,text=u'策略10:月线10MA', command = stock_select.strategy10).grid(row=7,column=2)
Button(root,text=u'策略11:波动区间', command = stock_select.strategy11).grid(row=8,column=2)
Button(root,text=u'策略12:60天波动区间', command = stock_select.strategy12).grid(row=9,column=2)
Button(root,text=u'策略13:180天波动区间', command = stock_select.strategy13).grid(row=10,column=2)
Button(root,text=u'策略14:250天波动区间', command = stock_select.strategy14).grid(row=11,column=2)


Button(root,text=u'执行所有策略', command = stock_select.write).grid(row=2,column=3)
Button(root,text=u'打开EXCEL', command = execute).grid(row=3,column=3)

Button(root,text=u'策略说明', command = indro).grid(row=2,column=4)
Button(root,text=u'使用说明', command = guide).grid(row=3,column=4)
listb  = Listbox(root)

root.mainloop()
