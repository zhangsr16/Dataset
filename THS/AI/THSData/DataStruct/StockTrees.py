import os
import math
import pandas as pd
import copy
import joblib

# CYCLES
label_folders = [f.path for f in os.scandir("./XLSX/Stock/20250204")]

# Joblib empty
dataframes = {}
# load Joblib
# dataframes = joblib.load('./StockTrees.joblib')

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
    # week
    weekframe = copy.deepcopy(dayframe[0:period])
    try:
        hashval = copy.deepcopy(dayframe[0])
    except IndexError:
        continue
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
dataframes[stockid] = cycframes

print(len(dataframes))
joblib.dump(dataframes, './StockTree.joblib')
