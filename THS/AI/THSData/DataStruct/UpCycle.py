import os
import math
import numpy as np
import torch
import pandas as pd
import copy

# FIELD
# 上海证券交易所（日）、证券类别统计（日）
# 证券类别统计（日） Type: col成交金额汇聚，其余继承
COLNAMES = ['股票', '主板A股', '主板B股', '创业板A股', '基金', 'ETF', 'LOF', '封闭式基金', '债券',
            '债券现券', '债券回购', 'ABS', 'Year', 'Mth',
            'Week', 'Day', 'Date']

label_folder = "./XLSX/Time/Day/Type/成交金额.xlsx"

dataframes = {}
fieldframes = {}
LenCol = len(COLNAMES)
hashheader = {}
for i in range(LenCol):
    hashheader[COLNAMES[i]] = i
stockid = os.path.basename(label_folder).rstrip(".xlsx")
# 打开Excel文件
dataframe = pd.read_excel(label_folder, engine='openpyxl')

# UpPeriod
# Day
dayframe = dataframe.values
nrows = dayframe.shape[0]
ncols = dayframe.shape[1]
period = DayPos = Weekpos = 0
for row_idx in range(nrows - 1):
    if dataframe['Week'][row_idx + 1] != dataframe['Week'][row_idx]:
        period += 1
fieldframes['Day'] = dayframe
# week
weekframe = copy.deepcopy(dayframe[0:period])
hashval = copy.deepcopy(dayframe[0])
period = 0
for row_idx in range(nrows - 1):  # 表头+余尾=2df
    hashval[hashheader['Day']] += 1
    for col_idx in range(ncols - 1):
        for i in range(hashheader['Year']):
            hashval[i] += dayframe[row_idx, i]
    if dataframe['Week'][row_idx + 1] != dataframe['Week'][row_idx]:
        weekframe[period] = hashval
        hashval = copy.deepcopy(dayframe[row_idx + 1])
        period += 1
fieldframes['Week'] = weekframe
TempDataframe = pd.DataFrame(weekframe, columns=COLNAMES)
TempDataframe.to_excel('./XLSX/Time/Week/Type/' + stockid + '.xlsx', index=False)
# mth
nrows = period
period = 0
for row_idx in range(nrows - 1):
    if weekframe[row_idx][hashheader['Mth']] != weekframe[row_idx + 1][hashheader['Mth']]:
        period += 1
mthframe = copy.deepcopy(weekframe[0:period])
hashval = copy.deepcopy(weekframe[0])
period = 0
for row_idx in range(nrows - 1):
    hashval[hashheader['Week']] += 1
    for col_idx in range(ncols - 1):
        for i in range(hashheader['Year']):
            hashval[i] += dayframe[row_idx, i]
    if weekframe[row_idx + 1][hashheader['Mth']] != weekframe[row_idx][hashheader['Mth']]:
        mthframe[period] = hashval
        hashval = copy.deepcopy(weekframe[row_idx + 1])
        period += 1
fieldframes['Mth'] = mthframe
TempDataframe = pd.DataFrame(mthframe, columns=COLNAMES)
TempDataframe.to_excel('./XLSX/Time/Month/Type/' + stockid + '.xlsx', index=False)
dataframes[stockid] = fieldframes

# 上海证券交易所（日） Summary: row成交量、成交金额汇聚，换手率、流通换手率平均，其余继承
COLNAMES = ['市价总值', '平均市盈率', '成交量', '成交金额', '挂牌数', '换手率', '流通市值', '流通换手率', 'Year', 'Mth',
            'Week', 'Day', 'Date']
label_folders = [f.path for f in os.scandir("./XLSX/Time/Day/Summary")]

fieldframes = {}
LenCol = len(COLNAMES)
hashheader = {}
for i in range(LenCol):
    hashheader[COLNAMES[i]] = i
for label_folder in label_folders:
    stockid = os.path.basename(label_folder).rstrip(".xlsx")
    # 打开Excel文件
    dataframe = pd.read_excel(label_folder, engine='openpyxl')

    # UpPeriod
    # Day
    dayframe = dataframe.values
    nrows = dayframe.shape[0]
    ncols = dayframe.shape[1]
    period = DayPos = Weekpos = 0
    for row_idx in range(nrows - 1):
        if dataframe['Week'][row_idx + 1] != dataframe['Week'][row_idx]:
            period += 1
    fieldframes['Day'] = dayframe
    # week
    weekframe = copy.deepcopy(dayframe[0:period])
    hashval = copy.deepcopy(dayframe[0])
    period = 0
    for row_idx in range(nrows - 1):  # 表头+余尾=2df
        hashval[hashheader['Day']] += 1
        for col_idx in range(ncols - 1):
            hashval[hashheader['成交量']] += dayframe[row_idx, hashheader['成交量']]
            hashval[hashheader['成交金额']] += dayframe[row_idx, hashheader['成交金额']]
            hashval[hashheader['流通换手率']] += dayframe[row_idx, hashheader['流通换手率']]
            hashval[hashheader['换手率']] += dayframe[row_idx, hashheader['换手率']]
        if dataframe['Week'][row_idx + 1] != dataframe['Week'][row_idx]:
            hashval[hashheader['换手率']] /= hashval[hashheader['Day']]
            hashval[hashheader['流通换手率']] /= hashval[hashheader['Day']]
            weekframe[period] = hashval
            hashval = copy.deepcopy(dayframe[row_idx + 1])
            period += 1
    fieldframes['Week'] = weekframe
    TempDataframe = pd.DataFrame(weekframe, columns=COLNAMES)
    TempDataframe.to_excel('./XLSX/Time/Week/Summary/' + stockid + '.xlsx', index=False)
    # mth
    nrows = period
    period = 0
    for row_idx in range(nrows - 1):
        if weekframe[row_idx][hashheader['Mth']] != weekframe[row_idx + 1][hashheader['Mth']]:
            period += 1
    mthframe = copy.deepcopy(weekframe[0:period])
    hashval = copy.deepcopy(weekframe[0])
    period = 0
    for row_idx in range(nrows - 1):
        hashval[hashheader['Week']] += 1
        for col_idx in range(ncols - 1):
            hashval[hashheader['成交量']] += weekframe[row_idx, hashheader['成交量']]
            hashval[hashheader['成交金额']] += weekframe[row_idx, hashheader['成交金额']]
            hashval[hashheader['流通换手率']] += weekframe[row_idx, hashheader['流通换手率']]
            hashval[hashheader['换手率']] += weekframe[row_idx, hashheader['换手率']]
        if weekframe[row_idx + 1][hashheader['Mth']] != weekframe[row_idx][hashheader['Mth']]:
            hashval[hashheader['换手率']] /= hashval[hashheader['Week']]
            hashval[hashheader['流通换手率']] /= hashval[hashheader['Week']]
            mthframe[period] = hashval
            hashval = copy.deepcopy(weekframe[row_idx + 1])
            period += 1
    fieldframes['Mth'] = mthframe
    TempDataframe = pd.DataFrame(mthframe, columns=COLNAMES)
    TempDataframe.to_excel('./XLSX/Time/Month/Summary/' + stockid + '.xlsx', index=False)
    dataframes[stockid] = fieldframes

# CYCLES
label_folders = [f.path for f in os.scandir("./XLSX/Stock")]
dataframes = {}
cycframes = {}
COLNAMES = ['日期', '股票代码', '开盘', '收盘', '最高', '最低', '成交量', '成交额', '振幅', '涨跌幅', '涨跌额',
            '换手率', 'Year', 'Mth', 'Week', 'Day']

for label_folder in label_folders:
    stockid = os.path.basename(label_folder).rstrip(".xlsx")
    # 打开Excel文件
    dataframe = pd.read_excel(label_folder, engine='openpyxl')

    # UpPeriod
    # Day
    dataframe['Year'] = 0
    dataframe['Mth'] = 0
    dataframe['Week'] = 0
    dataframe['Day'] = 0
    dayframe = dataframe.values
    nrows = dayframe.shape[0]
    ncols = dayframe.shape[1]
    hashheader = {}
    varnames = dataframe.columns.values
    for i in range(ncols):
        hashheader[varnames[i]] = i

    # UpPeriod
    # Day
    period = DayPos = Weekpos = 0
    for row_idx in range(nrows - 1):
        dayframe[row_idx][hashheader['Day']] = DayPos
        dayframe[row_idx][hashheader['Week']] = Weekpos
        dayframe[row_idx][hashheader['Mth']] = dataframe['日期'][row_idx].month
        dayframe[row_idx][hashheader['Year']] = dataframe['日期'][row_idx].year
        DayPos += 1
        if dataframe['日期'][row_idx + 1] - dataframe['日期'][row_idx] != pd.Timedelta('1 days 00:00:00'):
            period += 1
            Weekpos += 1
            DayPos = 0
        if dataframe['日期'][row_idx + 1].month != dataframe['日期'][row_idx].month:
            Weekpos = 0
    cycframes['Day'] = dayframe
    TempDataframe = pd.DataFrame(dayframe, columns=COLNAMES)
    os.makedirs('./XLSX/Time/Day', exist_ok=True)
    TempDataframe.to_excel('./XLSX/Time/Day/' + stockid + '.xlsx', index=False)
    # week
    weekframe = copy.deepcopy(dayframe[0:period])
    hashval = copy.deepcopy(dayframe[0])
    period = 0
    flag = 0
    hashval[hashheader['最低']] = math.inf
    for row_idx in range(nrows - 1):  # 表头+余尾=2df
        hashval[hashheader['Day']] += 1
        for col_idx in range(ncols - 1):
            hashval[hashheader['成交量']] += dayframe[row_idx, hashheader['成交量']]
            hashval[hashheader['成交额']] += dayframe[row_idx, hashheader['成交额']]
            hashval[hashheader['涨跌额']] += dayframe[row_idx, hashheader['涨跌额']]
            hashval[hashheader['振幅']] += dayframe[row_idx, hashheader['振幅']]
            hashval[hashheader['换手率']] += dayframe[row_idx, hashheader['换手率']]
            hashval[hashheader['涨跌幅']] += dayframe[row_idx, hashheader['涨跌幅']]
            if flag == 0:
                hashval[hashheader['开盘']] = dayframe[row_idx, hashheader['开盘']]
                hashval[hashheader['日期']] = dayframe[row_idx, hashheader['日期']]
                flag = 1

            if hashval[hashheader['最高']] < dayframe[row_idx, hashheader['最高']]:
                hashval[hashheader['最高']] = dayframe[row_idx, hashheader['最高']]
            if hashval[hashheader['最低']] > dayframe[row_idx, hashheader['最低']]:
                hashval[hashheader['最低']] = dayframe[row_idx, hashheader['最低']]

        if dayframe[row_idx + 1][0] - dayframe[row_idx][0] != pd.Timedelta('1 days 00:00:00'):
            hashval[hashheader['收盘']] = dayframe[row_idx, hashheader['收盘']]
            hashval[hashheader['振幅']] /= hashval[hashheader['Day']]
            hashval[hashheader['换手率']] /= hashval[hashheader['Day']]
            hashval[hashheader['涨跌幅']] /= hashval[hashheader['Day']]
            weekframe[period] = hashval
            hashval = copy.deepcopy(dayframe[row_idx + 1])
            hashval[hashheader['最低']] = math.inf
            period += 1
            flag = 0
    cycframes['Week'] = weekframe
    TempDataframe = pd.DataFrame(weekframe, columns=COLNAMES)
    os.makedirs('./XLSX/Time/Week', exist_ok=True)
    TempDataframe.to_excel('./XLSX/Time/Week/' + stockid + '.xlsx', index=False)
    # mth
    nrows = period
    period = 0
    for row_idx in range(nrows - 1):
        if weekframe[row_idx][0].month != weekframe[row_idx + 1][0].month:
            period += 1
    mthframe = copy.deepcopy(weekframe[0:period])
    hashval = copy.deepcopy(weekframe[0])
    period = 0
    flag = 0
    hashval[hashheader['最低']] = math.inf
    for row_idx in range(nrows - 1):
        hashval[hashheader['Week']] += 1
        for col_idx in range(ncols - 1):
            hashval[hashheader['成交量']] += weekframe[row_idx, hashheader['成交量']]
            hashval[hashheader['成交额']] += weekframe[row_idx, hashheader['成交额']]
            hashval[hashheader['涨跌额']] += weekframe[row_idx, hashheader['涨跌额']]
            hashval[hashheader['振幅']] += weekframe[row_idx, hashheader['振幅']]
            hashval[hashheader['换手率']] += weekframe[row_idx, hashheader['换手率']]
            hashval[hashheader['涨跌幅']] += weekframe[row_idx, hashheader['涨跌幅']]
            if flag == 0:
                hashval[hashheader['开盘']] = weekframe[row_idx, hashheader['开盘']]
                hashval[hashheader['日期']] = weekframe[row_idx, hashheader['日期']]
                flag = 1

            if hashval[hashheader['最高']] < weekframe[row_idx, hashheader['最高']]:
                hashval[hashheader['最高']] = weekframe[row_idx, hashheader['最高']]
            if hashval[hashheader['最低']] > weekframe[row_idx, hashheader['最低']]:
                hashval[hashheader['最低']] = weekframe[row_idx, hashheader['最低']]

        if weekframe[row_idx][0].month != weekframe[row_idx + 1][0].month:
            hashval[hashheader['收盘']] = weekframe[row_idx, hashheader['收盘']]
            hashval[hashheader['振幅']] /= hashval[hashheader['Week']]
            hashval[hashheader['换手率']] /= hashval[hashheader['Week']]
            hashval[hashheader['涨跌幅']] /= hashval[hashheader['Week']]
            mthframe[period] = hashval
            hashval = copy.deepcopy(weekframe[row_idx + 1])
            hashval[hashheader['最低']] = math.inf
            period += 1
            flag = 0
    cycframes['Mth'] = mthframe
    TempDataframe = pd.DataFrame(mthframe, columns=COLNAMES)
    os.makedirs('./XLSX/Time/Month', exist_ok=True)
    TempDataframe.to_excel('./XLSX/Time/Month/' + stockid + '.xlsx', index=False)
    dataframes[stockid] = cycframes
