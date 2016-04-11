#!/usr/bin/env python
#coding:utf-8
import numpy as np
import matplotlib
from Tkinter import *
from matplotlib.figure import Figure
import Tkinter
import graph
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
def data1():
   ax,x,y,z = drawPic()
   ax.set_title(u'300018.SZ',fontsize = 8)
   ax.plot(x,y)
   drawPic.canvas.show()
def data2():
   ax,x,y,z = drawPic()
   ax.set_title(u'300019.SZ',fontsize = 8)
   ax.plot(x,z)
   drawPic.canvas.show()
def double():
   ax,x,y,z = drawPic()
   ax.plot(x,z)
   ax.plot(x,y)
   drawPic.canvas.show()
def clear():
      #清空图像，以使得前后两次绘制的图像不会重叠
   drawPic.f.clf()
   drawPic.a=drawPic.f.add_subplot(111)
   drawPic.canvas.show()
def drawPic():
   x,y,z = graph.excel()
   #清空图像，以使得前后两次绘制的图像不会重叠
   drawPic.f.clf()
   drawPic.a=drawPic.f.add_subplot(111)
   ax = drawPic.a
   ax.set_xticks([0,50,100,150,200,244])

   ax.set_xticklabels(x,fontsize = 13)
   x = range(len(x))

   ax.set_xlabel(u'时间')
   ax.set_ylabel(u'价格')
   return ax,x,y,z
def outDraw():
   #清空图像，以使得前后两次绘制的图像不会重叠
   drawPic.f.clf()
   drawPic.a=drawPic.f.add_subplot(111)
   graph.have_a_try()


matplotlib.use('TkAgg')
root=Tk()
#在Tk的GUI上放置一个画布，并用.grid()来调整布局
drawPic.f = Figure(figsize=(5,3), dpi=100)
drawPic.canvas = FigureCanvasTkAgg(drawPic.f, master=root)
drawPic.canvas.show()
drawPic.canvas.get_tk_widget().grid(row=2, columnspan=8)
#放置标签、文本框和按钮等部件，并设置文本框的默认值和按钮的事件函数
Label(root,text='股价走势图：').grid(row=1,column=0)
# inputEntry=Entry(root)
# inputEntry.grid(row=1,column=1)
# inputEntry.insert(0,'50')
Button(root,text='数据一',command=data1).grid(row=1,column=1,columnspan=3)
Button(root,text='数据二',command=data2).grid(row=1,column=2,columnspan=3)
Button(root,text='比较',command=double).grid(row=1,column=3,columnspan=3)
Button(root,text='放大',command=outDraw).grid(row=1,column=4,columnspan=3)
Button(root,text='清空',command=clear).grid(row=1,column=5,columnspan=3)

#启动事件循环
root.mainloop()
