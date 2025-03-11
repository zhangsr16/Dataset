import os
import math
import numpy as np
import torch
import pandas as pd
import copy
import joblib

# Option
# Option will effect the dataprocess
Option = 'Summary'
NumCols = ['股票', '主板A', '主板B', '科创板', '股票回购']
# Option = 'Type'
# NumCols = ['数量', '成交金额', '总市值', '流通市值']

label_folders = [f.path for f in os.scandir("./XLSX/" + Option)]

# First use
pos = 0
DatePoint = [[]]
WindowPoint = {'Dates': DatePoint, 'Days': 0, 'Weeks': 0, 'Months': 0, 'Years': 0}
# Reuse
if pos != 0:
    WindowPoint = joblib.load("./XLSX/" + Option + '/WindowPoint.joblib')
    WeekState = joblib.load("./XLSX/" + Option + './WeekState.joblib')
    MonthState = joblib.load("./XLSX/" + Option + './MonthState.joblib')
    YearState = joblib.load("./XLSX/" + Option + './YearState.joblib')

for label_folder in label_folders:
    if not label_folder.endswith('.xlsx'):
        continue
    try:
        dataframe = pd.read_excel(label_folder, engine='openpyxl')
    except PermissionError as e:
        # 捕获 PermissionError 并打印错误信息
        print(f"权限错误：{e}")
        break
    except Exception as e:
        # 捕获其他可能的异常
        print(f"发生未知错误：{e}")
        break
    # DatePoint
    date = os.path.basename(label_folder).rstrip(".xlsx")
    date = pd.Timestamp(date)
    if pos == 0:
        DatePoint[0] = date
        DatePoint.append(date)
        # TempState
        # if origin not change, use 'hashval2 = dataframe', just point reuse
        WeekState = copy.deepcopy(dataframe)
        MonthState = copy.deepcopy(dataframe)
        YearState = copy.deepcopy(dataframe)
        pos += 1
        continue
    else:
        DatePoint[0] = DatePoint[1]
        DatePoint[1] = date
    pos += 1

    WindowPoint['Days'] += 1
    WeekState[NumCols] += dataframe[NumCols]
    MonthState[NumCols] += dataframe[NumCols]
    YearState[NumCols] += dataframe[NumCols]
    if DatePoint[1] - DatePoint[0] != pd.Timedelta('1 days 00:00:00'):
        WeekState.to_excel(
            './XLSX/' + Option + '/Weeks/' + DatePoint[0].strftime('%Y%m%d') + '-' + str(WindowPoint['Days']) + '.xlsx',
            index=False)
        WindowPoint['Days'] = 0
        WindowPoint['Weeks'] += 1
        WeekState[NumCols] = 0
    if DatePoint[1].month != DatePoint[0].month:
        MonthState.to_excel('./XLSX/' + Option + '/Months/' + DatePoint[0].strftime('%Y%m%d') + '-' + str(
            WindowPoint['Weeks']) + '.xlsx', index=False)
        WindowPoint['Weeks'] = 0
        WindowPoint['Months'] += 1
        MonthState[NumCols] = 0
    if DatePoint[1].year != DatePoint[0].year:
        YearState.to_excel('./XLSX/' + Option + '/Years/' + DatePoint[0].strftime('%Y%m%d') + '-' + str(
            WindowPoint['Months']) + '.xlsx', index=False)
        WindowPoint['Months'] = 0
        WindowPoint['Years'] += 1
        YearState[NumCols] = 0

joblib.dump(WindowPoint, './XLSX/' + Option + '/WindowPoint.joblib')
joblib.dump(WeekState, './XLSX/' + Option + '/WeekState.joblib')
joblib.dump(MonthState, './XLSX/' + Option + '/MonthState.joblib')
joblib.dump(YearState, './XLSX/' + Option + '/YearState.joblib')
