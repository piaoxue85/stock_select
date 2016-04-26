#-*- endcoding:utf8 -*-

x = [1,2,3,4,5,6,2,3,4,2]

def EMA(x,n):
    if n is 1:
        return float(x[-1])
    return float(2*x[-1]+(n-1)*EMA(x[:-1],n-1))/(n + 1)

import datetime
import time
start = "2016-12-01"
start = datetime.datetime.strptime(start, "%Y-%m-%d")
start_s = time.mktime(start.timetuple())
before = start_s - 22
start = time.strftime("%Y-%m-%d",time.localtime(before))
print start