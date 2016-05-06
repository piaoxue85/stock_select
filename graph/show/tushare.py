def TushareSource(code = '601928',start = '2016-02-01',end = '2016-04-01'):
    raw_data = ts.get_h_data(code,start=start,end = end)
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
        value.append(raw_data.iloc[i][2])

    return num, data,str_date,value