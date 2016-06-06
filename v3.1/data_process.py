#-*- encoding:utf8 -*-
from data_source import *
import datetime
import math
#处理数据类
class Process(object):

    def __init__(self):

        #1#营收净增率
        self.revenue = []
        #2#EPS季增率
        self.EPS = []
        #3#毛利率净增率
        self.MLL = []
        #4#净资产收益率ROE净增率
        self.ROE = []
        #5#波动率今10MA > 前10MA，同时 10 MA > 100MA
        self.volatility = []
        #6#价格今10MA > 前10MA，同时前10MA > 前前10MA
        self.price = []
        #7#波动性:日线 周线 月线10MA都上扬
        self.synchronization = []
        #8#日线10MA上扬
        self.DAY10 = []
        #9#周线10MA上扬
        self.WEEK10 = []
        #10#月线10MA上扬
        self.MON10 = []
        #11#60 180 250天波动区间在30% 50% 100%内
        self.vola_range = []
        #12#60天波动区间在30%内
        self.vola_range60 = []
        #13#180天波动区间在50%内
        self.vola_range180 = []
        #14#250天波动区间在100%内
        self.vola_range250 = []
        #15#融资余额今10MA>前10MA,同时10MA>30MA
        self.mrg = []
        #16#户均持股前三季中有一次增加
        self.holder_avgnum = []
        #17#股东户数两季连续减少
        self.holder_num = []
        #18#十大股东变化超过3个
        self.change = []
        #19#十大股东持股比例增加
        self.holder_top10 = []
        #20、21、22#券商、基金、机构持股数量排序
        self.trader = []
        self.fund = []
        self.institude = []
        #23#换手率5MA大于前一天5MA，同时10MA大于前一天10MA
        self.turn_num = []
        #24#涨幅日、周、月都超过大盘
        self.increase = []
        # 25#袁氏选股
        self.yuan1 = []
        self.yuan2 = []
        # 29 # 公司净值（每股净资产BPS）
        self.bps = []
        # 30 # 市盈率PE
        self.pe = []
        # 31 # 每股分红送转
        self.fenhong = []
    #执行全部策略
    def exec_all(self):
        D.get_all()

    #1#营收净增率
    def process1(self):
        Data = D.wind_data1()
        this_time = Data.time
        for i in range(Data.stock_num):
            #原数据
            this_data =[]
            #本循环中股票代码
            code = str(Data.codes[i])
            #判错代码
            errcode = 0
            #上三季数据
            pre_3Q = Data.data[i][0]
            this_data.append(pre_3Q)
            if(math.isnan(pre_3Q) or pre_3Q == 0):
                print code + "没有上三季数据"
                errcode = 1
            #上两季数据
            pre_2Q = Data.data[i][1]
            this_data.append(pre_2Q)
            if(math.isnan(pre_2Q) or pre_2Q == 0):
                print code + u"没有上两季数据"
                errcode = 1
            #上一季数据
            pre_1Q = Data.data[i][2]
            this_data.append(pre_1Q)
            if(math.isnan(pre_1Q)):
                print code + u"没有上一季数据"
                errcode = 1
            #本季数据
            Q = Data.data[i][3]
            this_data.append(Q)
            if(math.isnan(Q)):
                print code + u"没有本季数据"
            if(errcode == 0):
                rate1 = pre_1Q/pre_2Q - 1
                rate2 = pre_2Q/pre_3Q - 1
                if(rate1 > rate2):
                    self.revenue.append((code,rate1,rate2,this_data,this_time))
            elif(errcode == 1):
                print code + u"数据有错"
        return self.revenue

    #2#EPS季增率
    def process2(self):
        Data = D.wind_data2()
        this_time = Data.time
        for i in range(Data.stock_num):
            #原数据
            this_data =[]
            #本循环中股票代码
            code = str(Data.codes[i])
            #判错代码
            errcode = 0
            #上三季数据
            pre_3Q = Data.data[i][0]
            this_data.append(pre_3Q)
            if(math.isnan(pre_3Q) or pre_3Q == 0 or pre_3Q == -1):
                print code + "没有上三季数据"
                errcode = 1
            #上两季数据
            pre_2Q = Data.data[i][1]
            this_data.append(pre_2Q)
            if(math.isnan(pre_2Q) or pre_2Q == 0):
                print code + u"没有上两季数据"
                errcode = 1
            #上一季数据
            pre_1Q = Data.data[i][2]
            this_data.append(pre_1Q)
            if(math.isnan(pre_1Q)):
                print code + u"没有上一季数据"
                errcode = 1
            #本季数据
            Q = Data.data[i][3]
            this_data.append(Q)
            if(math.isnan(Q)):
                print code + u"没有本季数据"
            if(errcode == 0):
                rate1 = (pre_1Q + 1)/(pre_2Q + 1) - 1
                if(pre_1Q + 1 < 0 or pre_2Q + 1 < 0):
                    rate1 = 0
                rate2 = (pre_2Q + 1)/(pre_3Q + 1) - 1
                if(pre_1Q + 1 < 0 or pre_2Q + 1 < 0):
                    rate2 = 0
                if(rate1 > rate2):
                    self.EPS.append((code,rate1,rate2,this_data,this_time))
            elif(errcode == 1):
                print code + u"数据有错"
        return self.EPS

    #3#毛利率季增率
    def process3(self):
        Data = D.wind_data3()
        this_time = Data.time
        for i in range(Data.stock_num):
            #原数据
            this_data =[]
            #本循环中股票代码
            code = str(Data.codes[i])
            #判错代码
            errcode = 0
            #上三季数据
            pre_3Q = Data.data[i][0]
            this_data.append(pre_3Q)
            if(math.isnan(pre_3Q) or pre_3Q == 0):
                print code + "没有上三季数据"
                errcode = 1
            #上两季数据
            pre_2Q = Data.data[i][1]
            this_data.append(pre_2Q)
            if(math.isnan(pre_2Q) or pre_2Q == 0):
                print code + u"没有上两季数据"
                errcode = 1
            #上一季数据
            pre_1Q = Data.data[i][2]
            this_data.append(pre_1Q)
            if(math.isnan(pre_1Q)):
                print code + u"没有上一季数据"
                errcode = 1
            #本季数据
            Q = Data.data[i][3]
            this_data.append(Q)
            if(math.isnan(Q)):
                print code + u"没有本季数据"
            if(errcode == 0):
                rate1 = (pre_1Q + 1)/(pre_2Q + 1) - 1
                if(pre_1Q + 1 < 0 or pre_2Q + 1 < 0):
                    rate1 = 0
                rate2 = (pre_2Q + 1)/(pre_3Q + 1) - 1
                if(pre_1Q + 1 < 0 or pre_2Q + 1 < 0):
                    rate2 = 0
                if(rate1 > rate2):
                    self.MLL.append((code,rate1,rate2,this_data,this_time))
            elif(errcode == 1):
                print code + u"数据有错"
        return self.MLL

    #4#净资产收益率ROE净增率
    def process4(self):
        Data = D.wind_data4()
        this_time = Data.time
        for i in range(Data.stock_num):
            #原数据
            this_data =[]
            #本循环中股票代码
            code = str(Data.codes[i])
            #判错代码
            errcode = 0
            #上三季数据
            pre_3Q = Data.data[i][0]
            this_data.append(pre_3Q)
            if(math.isnan(pre_3Q) or pre_3Q == 0):
                print code + "没有上三季数据"
                errcode = 1
            #上两季数据
            pre_2Q = Data.data[i][1]
            this_data.append(pre_2Q)
            if(math.isnan(pre_2Q) or pre_2Q == 0):
                print code + u"没有上两季数据"
                errcode = 1
            #上一季数据
            pre_1Q = Data.data[i][2]
            this_data.append(pre_1Q)
            if(math.isnan(pre_1Q)):
                print code + u"没有上一季数据"
                errcode = 1
            #本季数据
            Q = Data.data[i][3]
            this_data.append(Q)
            if(math.isnan(Q)):
                print code + u"没有本季数据"
            if(errcode == 0):
                rate1 = (pre_1Q + 1)/(pre_2Q + 1) - 1
                if(pre_1Q + 1 < 0 or pre_2Q + 1 < 0):
                    rate1 = 0
                rate2 = (pre_2Q + 1)/(pre_3Q + 1) - 1
                if(pre_1Q + 1 < 0 or pre_2Q + 1 < 0):
                    rate2 = 0
                if(rate1 > rate2):
                    self.ROE.append((code,rate1,rate2,this_data,this_time))
            elif(errcode == 1):
                print code + u"数据有错"
        return self.ROE

    #5#波动率今10MA > 前10MA，同时 10 MA > 100MA
    def process5(self):
        Data = D.wind_data5()
        for each in range(Data.stock_num):
            #时间
            this_time = Data.time
            this_data = []
            #本循环中股票代码
            code = str(Data.codes[each])
            #收盘数据
            close = Data.data[each]
            total = 0
            today_vol = self.stdevr(111,close,10)
            for i in range(10):
                vol = self.stdevr(111-i,close,10)
                total = total + vol
            MA10 = total/10
            total = 0
            for i in range(10):
                vol = self.stdevr(110-i,close,10)
                total = total + vol
            pre_MA10 = total/10
            for i in range(100):
                vol = self.stdevr(109-i,close,10)
                total = total + vol
            MA100 = total/100
            this_data.append(today_vol)
            this_data.append(pre_MA10)
            this_data.append(MA10)
            this_data.append(MA100)
            if(MA10 > pre_MA10 and MA10 > MA100):
                self.volatility.append((code,this_data,this_time))
        return self.volatility
    def stdevr(self,t,close,period):
        re_list = []
        total = 0
        for i in range(t - period,t):
            re = close[i]/close[i - 1] - 1
            re_list.append(re)
        avg = sum(re_list)/len(re_list)
        for item in re_list:
            x = (item - avg)**2
            total = total + x
        vol = (total/(len(re_list)-1))**0.5
        return vol

    #6#价格今10MA > 前10MA，同时前10MA > 前前10MA
    def process6(self):
        Data = D.wind_data6()
        this_time = Data.time
        for i in range(Data.stock_num):
            #原数据
            this_data =[]
            #本循环中股票代码
            code = str(Data.codes[i])
            #判错代码?????????
            errcode = 0
            pre_pre_MA10 = sum(Data.data[i][0:10])/10
            this_data.append(pre_pre_MA10)
            pre_MA10 = sum(Data.data[i][1:11])/10
            this_data.append(pre_MA10)
            MA10 = sum(Data.data[i][2:12])/10
            this_data.append(MA10)
            if(errcode == 0 and MA10 > pre_MA10 and pre_MA10 > pre_pre_MA10):
                self.price.append((code,this_data,this_time))
        return self.price

    #7#波动性:日线 周线 月线10MA都上扬
    def process7(self):
        Data = D.wind_data7()
        day_time = Data.time[0]
        week_time = Data.time[1]
        month_time = Data.time[2]
        day_data = Data.data[0]
        week_data = Data.data[1]
        month_data = Data.data[2]
        #判错代码?????
        errcode = 0
        #万得中周和月的时间不同
        for i in range(Data.stock_num):
            #原数据
            this_data =[]
            #本循环中股票代码
            code = str(Data.codes[i])
            errcode = 0
            #前两天10MA
            DAY_pre_MA10 = sum(day_data[i][0:10])/10
            this_data.append(DAY_pre_MA10)
            DAY_MA10 = sum(day_data[i][1:11])/10
            this_data.append(DAY_MA10)
            #前两周10MA
            WEEK_pre_MA10 = sum(week_data[i][0:10])/10
            this_data.append(WEEK_pre_MA10)
            WEEK_MA10 = sum(week_data[i][1:11])/10
            this_data.append(WEEK_MA10)
            #前两月10MA
            MON_pre_MA10 = sum(month_data[i][0:10])/10
            this_data.append(MON_pre_MA10)
            MON_MA10 = sum(month_data[i][1:11])/10
            this_data.append(MON_MA10)
            if(errcode == 0 and DAY_MA10 > DAY_pre_MA10 and WEEK_MA10 > WEEK_pre_MA10 and MON_MA10 > MON_pre_MA10):
                self.synchronization.append((code,this_data,day_time,week_time,month_time))
        return self.synchronization

    #8#日线10MA上扬
    def process8(self):
        Data = D.wind_data8()
        this_time = Data.time
        for i in range(Data.stock_num):
            #原数据
            this_data =[]
            #本循环中股票代码
            code = str(Data.codes[i])
            #判错代码?????
            errcode = 0
            #前两天10MA
            pre_MA10 = sum(Data.data[i][0:10])/10
            this_data.append(pre_MA10)
            MA10 = sum(Data.data[i][1:11])/10
            this_data.append(MA10)
            if(errcode == 0 and MA10 > pre_MA10):
                self.DAY10.append((code,this_data,this_time))
        return self.DAY10

    #9#周线10MA上扬
    def process9(self):
        Data = D.wind_data9()
        this_time = Data.time
        for i in range(Data.stock_num):
            #原数据
            this_data =[]
            #本循环中股票代码
            code = str(Data.codes[i])
            #判错代码?????
            errcode = 0
            #前两月10MA
            WEEK_pre_MA10 = sum(Data.data[i][0:10])/10
            this_data.append(WEEK_pre_MA10)
            WEEK_MA10 = sum(Data.data[i][1:11])/10
            this_data.append(WEEK_MA10)
            if(errcode == 0 and WEEK_MA10 > WEEK_pre_MA10):
                self.MON10.append((code,this_data,this_time))
        return self.MON10

    #10#月线10MA上扬
    def process10(self):
        Data = D.wind_data10()
        this_time = Data.time
        for i in range(Data.stock_num):
            #原数据
            this_data =[]
            #本循环中股票代码
            code = str(Data.codes[i])
            #判错代码?????
            errcode = 0
            #前两月10MA
            MON_pre_MA10 = sum(Data.data[i][0:10])/10
            this_data.append(MON_pre_MA10)
            MON_MA10 = sum(Data.data[i][1:11])/10
            this_data.append(MON_MA10)
            if(errcode == 0 and MON_MA10 > MON_pre_MA10):
                self.WEEK10.append((code,this_data,this_time))
        return self.WEEK10

    #11#60 180 250天波动区间在30% 50% 100%内
    def process11(self):
        Data = D.wind_data11()
        this_time = Data.time
        high_60 = Data.data[0]
        low_60 = Data.data[1]
        high_180 = Data.data[2]
        low_180 = Data.data[3]
        high_250 = Data.data[4]
        low_250 = Data.data[5]
        for i in range(Data.stock_num):
            #本循环中股票代码
            code = str(Data.codes[i])
            #本循环
            this_data = []
            #判错代码
            errcode = 0
            high1 = max(high_60[i])
            this_data.append(high1)
            if(high1 == None):
                print code + u"数据有误"
                errcode = 1
            low1 = min(low_60[i])
            this_data.append(low1)
            if(low1 == None):
                print code + u"数据有误"
                errcode = 1
            high2 = max(high_180[i])
            this_data.append(high2)
            if(high2 == None):
                print code + u"数据有误"
                errcode = 1
            low2 = min(low_180[i])
            this_data.append(low2)
            if(low2 == None):
                print code + u"数据有误"
                errcode = 1
            high3 = max(high_250[i])
            this_data.append(high3)
            if(high3 == None):
                print code + u"数据有误"
                errcode = 1
            low3 = min(low_250[i])
            this_data.append(low3)
            if(low3 == None):
                print code + u"数据有误"
                errcode = 1
            if(errcode == 0):
                x1 = low1 * 1.3
                x2 = low2 * 1.5
                x3 = low3 * 2
            if(high1 < x1 and high2 < x2 and high3 < x3 and errcode == 0):
                self.vola_range.append((code,this_data,this_time))
        return self.vola_range

    #12#60天波动区间在30%内
    def process12(self):
        Data = D.wind_data12()
        high_60 = Data.data[0]
        low_60 = Data.data[1]
        this_time = Data.time
        for i in range(Data.stock_num):
            #本循环中股票代码
            code = str(Data.codes[i])
            #本循环
            this_data = []
            #判错代码
            errcode = 0
            high1 = max(high_60[i])
            this_data.append(high1)
            if(high1 == None):
                print code + "数据有误"
                errcode = 1
            low1 = min(low_60[i])
            this_data.append(low1)
            if(low1 == None):
                print code + "数据有误"
                errcode = 1
            if(errcode == 0):
                x = low1 * 1.3
            if(high1 < x and errcode == 0):
                self.vola_range60.append((code,this_data,this_time))
        return self.vola_range60

    #13#180天波动区间在50%内
    def process13(self):
        Data = D.wind_data13()
        high_180 = Data.data[0]
        low_180 = Data.data[1]
        this_time = Data.time
        for i in range(Data.stock_num):
            #本循环中股票代码
            code = str(Data.codes[i])
            #本循环
            this_data = []
            #判错代码
            errcode = 0
            high1 = max(high_180[i])
            this_data.append(high1)
            if(high1 == None):
                print code + "数据有误"
                errcode = 1
            low1 = min(low_180[i])
            this_data.append(low1)
            if(low1 == None):
                print code + "数据有误"
                errcode = 1
            if(errcode == 0):
                x = low1 * 1.5
            if(high1 < x and errcode == 0):
                self.vola_range180.append((code,this_data,this_time))
        return self.vola_range180

    #14#250天波动区间在100%内
    def process14(self):
        Data = D.wind_data14()
        high_250 = Data.data[0]
        low_250 = Data.data[1]
        this_time = Data.time
        for i in range(Data.stock_num):
            #本循环中股票代码
            code = str(Data.codes[i])
            #本循环
            this_data = []
            #判错代码
            errcode = 0
            high1 = max(high_250[i])
            this_data.append(high1)
            if(high1 == None):
                print code + "数据有误"
                errcode = 1
            low1 = min(low_250[i])
            this_data.append(low1)
            if(low1 == None):
                print code + "数据有误"
                errcode = 1
            if(errcode == 0):
                x = low1 * 2
            if(high1 < x and errcode == 0):
                self.vola_range250.append((code,this_data,this_time))
        return self.vola_range250

    #15#融资余额今10MA>前10MA,同时10MA>30MA
    def process15(self):
        Data = D.wind_data15()
        this_time = Data.time
        for i in range(Data.stock_num):
            #判错代码 ？？？？？？？？？？？？？？？？？？？？？？？
            errcode = 0
            #原数据
            this_data =[]
            #本循环中股票代码
            code = str(Data.codes[i])
            yesterday = Data.data[i][29]
            this_data.append(yesterday)
            MA10 = sum(Data.data[i][20:30])/10
            this_data.append(MA10)
            pre_MA10 = sum(Data.data[i][19:29])/10
            this_data.append(pre_MA10)
            MA30 = sum(Data.data[i][0:30])/30
            this_data.append(MA30)
            if(errcode == 0 and MA10 > pre_MA10 and MA10 > MA30):
                self.mrg.append((code,this_data,this_time))
        return self.mrg

    #16#户均持股前三季中有一次增加
    def process16(self):
        Data = D.wind_data16()
        this_time = Data.time
        for i in range(Data.stock_num):
            #原数据
            this_data =[]
            #本循环中股票代码
            code = str(Data.codes[i])
            #判错代码
            errcode = 0
            #上三季数据
            pre_3Q = Data.data[i][0]
            this_data.append(pre_3Q)
            if(pre_3Q == None):
                print code + u"没有上三季数据"
                errcode = 1
            elif(math.isnan(pre_3Q) or pre_3Q == 0):
                print code + u"没有上三季数据"
                errcode = 1
            #上两季数据
            pre_2Q = Data.data[i][1]
            this_data.append(pre_2Q)
            if(pre_2Q == None):
                print code + u"没有上两季数据"
                errcode = 1
            elif(math.isnan(pre_2Q) or pre_2Q == 0):
                print code + u"没有上两季数据"
                errcode = 1
            #上一季数据
            pre_1Q = Data.data[i][2]
            this_data.append(pre_1Q)
            if(pre_1Q == None):
                print code + u"没有上一季数据"
                errcode = 1
            elif(math.isnan(pre_1Q)):
                print code + u"没有上一季数据"
                errcode = 1
            #本季数据
            Q = Data.data[i][3]
            this_data.append(Q)
            if(Q == None):
                print code + u"没有本季数据"
            elif(math.isnan(Q)):
                print code + u"没有本季数据"
            if(errcode == 0):
                if(pre_1Q > pre_2Q or pre_2Q > pre_3Q):
                    self.holder_avgnum.append((code,this_data,this_time))
        return self.holder_avgnum

    #17#股东户数两季连续减少
    def process17(self):
        Data = D.wind_data17()
        this_time = Data.time
        for i in range(Data.stock_num):
            #原数据
            this_data =[]
            #本循环中股票代码
            code = str(Data.codes[i])
            #判错代码
            errcode = 0
            #上三季数据
            pre_3Q = Data.data[i][0]
            this_data.append(pre_3Q)
            if(pre_3Q == None):
                print code + u"没有上三季数据"
                errcode = 1
            elif(math.isnan(pre_3Q) or pre_3Q == 0):
                print code + u"没有上三季数据"
                errcode = 1
            #上两季数据
            pre_2Q = Data.data[i][1]
            this_data.append(pre_2Q)
            if(pre_2Q == None):
                print code + u"没有上两季数据"
                errcode = 1
            elif(math.isnan(pre_2Q) or pre_2Q == 0):
                print code + u"没有上两季数据"
                errcode = 1
            #上一季数据
            pre_1Q = Data.data[i][2]
            this_data.append(pre_1Q)
            if(pre_1Q == None):
                print code + u"没有上一季数据"
                errcode = 1
            elif(math.isnan(pre_1Q)):
                print code + u"没有上一季数据"
                errcode = 1
            #本季数据
            Q = Data.data[i][3]
            this_data.append(Q)
            if(Q == None):
                print code + u"没有本季数据"
            elif(math.isnan(Q)):
                print code + u"没有本季数据"
            if(errcode == 0):
                if(pre_1Q < pre_2Q and pre_2Q < pre_3Q):
                    self.holder_num.append((code,this_data,this_time))
        return self.holder_num

    #18#十大股东变化超过3个
    def process18(self):
        Data = D.wind_data18()
        this_time = Data.time
        for i in range(Data.stock_num):
            #原数据
            this_data =[]
            #本循环中股票代码
            code = str(Data.codes[i])
            #判错代码
            errcode = 0
            #上三季数据
            pre_3Q = Data.data[i][0]
            # this_data.append(pre_3Q)
            if(pre_3Q == None):
                print code + u"没有上三季数据"
                errcode = 1
            #上两季数据
            pre_2Q = Data.data[i][1]
            this_data.append(pre_2Q)
            if(pre_2Q == None):
                print code + u"没有上两季数据"
                errcode = 1
            #上一季数据
            pre_1Q = Data.data[i][2]
            this_data.append(pre_1Q)
            if(pre_1Q == None):
                print code + u"没有上一季数据"
                errcode = 1
            #本季数据
            Q = Data.data[i][3]
            this_data.append(Q)
            if(Q == None):
                print code + u"没有本季数据"
            if(errcode == 0):
                a = pre_1Q.split(';')
                b = pre_2Q.split(';')
                # c = pre_3Q.split(';')
                x = 10 - self.holder_cmp(a,b)
                # y = 10 - holder_cmp(b,c)
                if(x > 3):
                    # for each in b:
                    #     each = each.replace(',',' ')
                    #     st = st + "," + each
                    # st = st + "\n"
                    # stock.append(st.encode('gbk'))
                    self.change.append((code,this_data,this_time,x))
            elif(errcode == 1):
                print code + u"数据有错"
        return self.change
    def holder_cmp(self,x,y):
        num = 0
        for i in x:
            for j in y:
                equ = cmp(i,j)
                if(equ == 0):
                    num = num + 1;
        return num

    #19#十大股东持股比例增加
    def process19(self):
        Data = D.wind_data19()
        this_time = Data.time
        all_data = []
        for i in range(Data.stock_num):
            #原数据
            this_data =[]
            #本循环中股票代码
            code = str(Data.codes[i])
            #判错代码
            errcode = 0
            #上三季数据
            pre_3Q = Data.data[i][0]
            this_data.append(pre_3Q)
            if(pre_3Q == None):
                print code + u"没有上三季数据"
                errcode = 1
            elif(math.isnan(pre_3Q) or pre_3Q == 0):
                print code + u"没有上三季数据"
                errcode = 1
            #上两季数据
            pre_2Q = Data.data[i][1]
            this_data.append(pre_2Q)
            if(pre_2Q == None):
                print code + u"没有上两季数据"
                errcode = 1
            elif(math.isnan(pre_2Q) or pre_2Q == 0):
                print code + u"没有上两季数据"
                errcode = 1
            #上一季数据
            pre_1Q = Data.data[i][2]
            this_data.append(pre_1Q)
            if(pre_1Q == None):
                print code + u"没有上一季数据"
                errcode = 1
            elif(math.isnan(pre_1Q)):
                print code + u"没有上一季数据"
                errcode = 1
            #本季数据
            Q = Data.data[i][3]
            this_data.append(Q)
            if(Q == None):
                print code + u"没有本季数据"
            elif(math.isnan(Q)):
                print code + u"没有本季数据"
            if(errcode == 0):
                if(pre_1Q > pre_2Q and pre_2Q > pre_3Q):
                    self.holder_top10.append((code,this_data,this_time))
            pre_1Q = Data.data[i][2]
            pre_2Q = Data.data[i][1]
            rate = pre_1Q/pre_2Q
            if(not math.isnan(rate)):
                all_data.append((code,pre_2Q,pre_1Q,rate))
        sort_all = sorted(all_data, key=lambda all_data: all_data[3], reverse=True)
        return self.holder_top10,sort_all

    #20、21、22#券商、基金、机构持股数量排序
    def process202122(self):
        Data = D.wind_data202122()
        data1 = Data.data[0]
        data2 = Data.data[1]
        data3 = Data.data[2]
        this_time = Data.time
        for i in range(Data.stock_num):
            #本循环中股票代码
            code = str(Data.codes[i])
            #判错代码
            errcode = 0
            Q = data1[i][0]
            if(Q == None):
                print code + u"没有上季数据"
                errcode = 1
            elif(math.isnan(Q)):
                print code + u"没有上季数据"
                errcode = 1
            if(errcode == 0):
                self.trader.append((code,Q,this_time))
        for i in range(Data.stock_num):
            #本循环中股票代码
            code = str(Data.codes[i])
            #判错代码
            errcode = 0
            Q = data2[i][0]
            if(Q == None):
                print code + u"没有上季数据"
                errcode = 1
            elif(math.isnan(Q)):
                print code + u"没有上季数据"
                errcode = 1
            if(errcode == 0):
                self.fund.append((code,Q,this_time))
        for i in range(Data.stock_num):
            #本循环中股票代码
            code = str(Data.codes[i])
            #判错代码
            errcode = 0
            Q = data3[i][0]
            if(Q == None):
                print code + u"没有本季数据"
                errcode = 1
            elif(math.isnan(Q)):
                print code + u"没有本季数据"
                errcode = 1
            if(errcode == 0):
                self.institude.append((code,Q,this_time))
        x = sorted(self.trader,key = lambda trader: trader[1],reverse=True)
        y = sorted(self.fund,key = lambda fund: fund[1],reverse=True)
        z = sorted(self.institude,key = lambda institude: institude[1],reverse=True)
        return x,y,z

    #23#换手率5MA大于前一天5MA，同时10MA大于前一天10MA
    def process23(self):
        Data = D.wind_data23()
        this_time = Data.time
        for i in range(Data.stock_num):
            #原数据
            this_data =[]
            #本循环中股票代码
            code = str(Data.codes[i])
            #判错代码?????????
            errcode = 0
            #今日换手率
            to = Data.data[i][10]
            this_data.append(to)
            pre_MA5 = sum(Data.data[i][5:10])/5
            this_data.append(pre_MA5)
            MA5 = sum(Data.data[i][6:11])/5
            this_data.append(MA5)
            pre_MA10 = sum(Data.data[i][0:10])/10
            this_data.append(pre_MA10)
            MA10 = sum(Data.data[i][1:11])/10
            this_data.append(MA10)
            if(errcode == 0 and MA5 > pre_MA5 and MA10 > pre_MA10):
                self.turn_num.append((code,this_data,this_time))
        return self.turn_num

    #24#涨幅日、周、月都超过大盘
    def process24(self):
        Data = D.wind_data24()
        this_time = Data.time
        day_scale = Data.data[0][0][20]/Data.data[0][0][19] - 1
        week_scale = Data.data[0][0][20]/Data.data[0][0][15] - 1
        month_scale = Data.data[0][0][20]/Data.data[0][0][0] - 1
        for i in range(Data.stock_num):
            # 原数据
            this_data = []
            # 本循环中股票代码
            code = str(Data.codes[i])
            #判错代码
            errcode = 0
            day = Data.data[1][i][20] / Data.data[1][i][19] - 1
            week = Data.data[1][i][20] / Data.data[1][i][15] - 1
            month = Data.data[1][i][20] / Data.data[1][i][0] - 1
            this_data.append(day)
            this_data.append(week)
            this_data.append(month)
            this_data.append(day_scale)
            this_data.append(week_scale)
            this_data.append(month_scale)
            if(day >= day_scale and week >= week_scale and month >= month_scale and errcode == 0):
                self.increase.append((code, this_data, this_time))
        return self.increase
    #25#袁氏选股
    def process25(self):
        Data = D.wind_data25()
        this_time = Data.time
        all = []
        for i in range(Data.stock_num):
            # 原数据
            this_data1 = []
            # 本循环中股票代码
            code = str(Data.codes[i])
            #判错代码
            errcode = 0
            day_today = Data.data[0][i][252]
            day_pre_5 = Data.data[0][i][247]
            day_pre_60 = Data.data[0][i][192]
            this_data1.append(day_today)
            this_data1.append(day_pre_5)
            this_data1.append(day_pre_60)
            if(day_today > day_pre_5 and day_pre_5 > day_pre_60 and errcode == 0):
                self.yuan1.append((code, this_data1, this_time))
        for i in range(Data.stock_num):
            # 原数据
            this_data2 = []
            # 本循环中股票代码
            code = str(Data.codes[i])
            #判错代码
            errcode = 0
            day_today = Data.data[0][i][252]
            day_pre_5 = Data.data[0][i][247]
            day_pre_250 = Data.data[0][i][0]
            this_data2.append(day_today)
            this_data2.append(day_pre_5)
            this_data2.append(day_pre_250)
            if (day_today > day_pre_5 and day_pre_5 > day_pre_250 and errcode == 0):
                self.yuan2.append((code, this_data2, this_time))
        for i in range(Data.stock_num):
            # 本循环中股票代码
            code = str(Data.codes[i])
            day_today = Data.data[0][i][252]
            day_pre_5 = Data.data[0][i][247]
            day_pre_60 = Data.data[0][i][192]
            day_pre_250 = Data.data[0][i][0]
            all.append((code,day_today,day_pre_5,day_pre_60,day_pre_250))
        return self.yuan1,self.yuan2,all

    # 27 # 股本，总股本和流通股本
    def process27(self):
        Data = D.wind_data27()
        data1 = Data.data[0]
        data2 = Data.data[1]
        this_time = Data.time
        for i in range(Data.stock_num):
            # 本循环中股票代码
            code = str(Data.codes[i])
            # 判错代码
            errcode = 0
            Q = data1[i][0]
            if (Q == None):
                print code + u"没有上季数据"
                errcode = 1
            elif (math.isnan(Q)):
                print code + u"没有上季数据"
                errcode = 1
            if (errcode == 0):
                self.trader.append((code, Q, this_time))
        for i in range(Data.stock_num):
            # 本循环中股票代码
            code = str(Data.codes[i])
            # 判错代码
            errcode = 0
            Q = data2[i][0]
            if (Q == None):
                print code + u"没有上季数据"
                errcode = 1
            elif (math.isnan(Q)):
                print code + u"没有上季数据"
                errcode = 1
            if (errcode == 0):
                self.fund.append((code, Q, this_time))
        x = sorted(self.trader, key=lambda trader: trader[1], reverse=True)
        y = sorted(self.fund, key=lambda fund: fund[1], reverse=True)
        return x,y
    # 29 # 公司净值（每股净资产BPS）
    def process29(self):
        Data = D.wind_data29()
        data = Data.data
        this_time = Data.time
        for i in range(Data.stock_num):
            # 本循环中股票代码
            code = str(Data.codes[i])
            # 判错代码
            errcode = 0
            Q = data[i][0]
            if (Q == None):
                print code + u"没有上季数据"
                errcode = 1
            elif (math.isnan(Q)):
                print code + u"没有上季数据"
                errcode = 1
            if (errcode == 0):
                self.bps.append((code, Q, this_time))
        x = sorted(self.bps, key=lambda trader: trader[1], reverse=True)
        return x
    # 30 # 市盈率PE
    def process30(self):
        Data = D.wind_data30()
        data = Data.data
        this_time = Data.time
        for i in range(Data.stock_num):
            # 本循环中股票代码
            code = str(Data.codes[i])
            # 判错代码
            errcode = 0
            Q = data[i][0]
            if (Q == None):
                print code + u"没有上季数据"
                errcode = 1
            elif (math.isnan(Q)):
                print code + u"没有上季数据"
                errcode = 1
            if (errcode == 0):
                self.pe.append((code, Q, this_time))
        x = sorted(self.pe, key=lambda trader: trader[1], reverse=True)
        return x
    # 31 # 每股分红送转
    def process31(self):
        Data = D.wind_data31()
        data = Data.data
        this_time = Data.time
        for i in range(Data.stock_num):
            # 本循环中股票代码
            code = str(Data.codes[i])
            # 判错代码
            errcode = 0
            Q = data[i][0]
            if (Q == None):
                print code + u"没有上季数据"
                errcode = 1
            elif (math.isnan(Q)):
                print code + u"没有上季数据"
                errcode = 1
            if (errcode == 0):
                self.fenhong.append((code, Q, this_time))
        x = sorted(self.fenhong, key=lambda trader: trader[1], reverse=True)
        return x
P = Process()