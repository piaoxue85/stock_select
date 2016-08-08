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
    today_name = u'v3.2选股2016-08-04.xlsx'
    today = u'2016-08-04'
    codes = D.Codes.split(",")
    length = len(codes)
    wb = open_workbook(today_name)
    ws = open_sheet(wb, u'股票代码')
    all = []
    # 公司价值
    for y in range(num_company + 1, num_company + 5):
        for x in range(length):
            all.append(ws.cell(row=x + 1 + 1, column=y).value)
    # 筹码
    for y in range(num_chips + 1, num_chips + 6):
        for x in range(length):
            all.append(ws.cell(row=x + 1 + 1, column=y).value)
    for y in range(num_chips + 6, num_chips + 9):
        for x in range(300):
            all.append(ws.cell(row=x + 1 + 1, column=y).value)
    for x in range(length):
        all.append(ws.cell(row=x + 1 + 1, column=num_chips + 9).value)
    for y in range(num_chips + 10, num_chips + 12):
        for x in range(300):
            all.append(ws.cell(row=x + 1 + 1, column=y).value)

    # 市场波动
    for y in range(num_stock + 1, num_stock + 14):
        for x in range(length):
            all.append(ws.cell(row=x + 1 + 1, column=y).value)

    # 财务
    for y in range(num_finance + 1, num_finance + 4):
        for x in range(300):
            all.append(ws.cell(row=x + 1 + 1, column=y).value)

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