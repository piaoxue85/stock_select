# -*- encoding:utf-8 -*-
from data_write import *

# 数据库mongodb


def ini():
    # 连接数据库
    con = MongoClient()
    db = con.stockdb
    collection = db.stock_holder
    return collection

# 代码统计


def star_db():
    # today_name = u'v2.2选股2016-05-09.xlsx'
    # today = u'2016-05-09'
    codes = D.all_code().split(",")
    length = len(codes)
    wb = open_workbook(today_name)
    ws = open_sheet(wb, u'股票代码')
    all = []
    for y in range(3, 25):
        for x in range(length):
            all.append(ws.cell(row=x + 1 + 1, column=y).value)
    for y in range(25, 28):
        for x in range(300):
            all.append(ws.cell(row=x + 1 + 1, column=y).value)
    for x in range(length):
        all.append(ws.cell(row=x + 1 + 1, column=28).value)
    col = ini()
    myset = set(all)
    result = []
    for each in myset:
        if each:
            code = each[0:6]
            result.append((each, all.count(each)))
            data = {
                u'股票代码': code,
                u'星数': all.count(each),
                u'日期': today
            }
            col.insert(data)
    print 123

def test_db():
    con = MongoClient('172.19.20.38:27017')
    db = con.stockdb
    collection = db.stock_holder

    codintion = {u'股票代码': "600198"}
    data = collection.find(codintion)
    for each in data:
        print each
    print 123

# test_db()
star_db()