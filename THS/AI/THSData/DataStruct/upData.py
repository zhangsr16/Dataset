import akshare as ak
import pandas as pd
from datetime import datetime
import joblib

current_time = datetime.now()
g_Month = str(current_time.year) + '02'
g_Day = current_time.strftime('%Y%m%d')

######### Day
# Type
Option = 'Type'
NumCols = ['数量', '成交金额', '总市值', '流通市值']
ROWNAMES = ['股票', '主板A股', '主板B股', '创业板A股', '基金', 'ETF', 'LOF', '封闭式基金', '债券',
            '债券现券', '债券回购', 'ABS']
dataframe = ak.stock_szse_summary(date=g_Day)
dataframe = dataframe[dataframe.apply(lambda row: row['证券类别'] in ROWNAMES, axis=1)]
dataframe = dataframe.fillna(0)

# # Summary
# Option = 'Summary'
# NumCols = ['股票', '主板A', '主板B', '科创板', '股票回购']
# ROWNAMES = ['市价总值', '平均市盈率', '成交量', '成交金额', '挂牌数', '换手率', '流通市值', '流通换手率']
# dataframe = ak.stock_sse_deal_daily(date=g_Day)
# dataframe = dataframe[dataframe.apply(lambda row: row['单日情况'] in ROWNAMES, axis=1)]

dataframe.to_excel('./XLSX/'+Option+'/' + g_Day + '.xlsx', index=False)
WindowPoint = joblib.load('./XLSX/'+Option+'/WindowPoint.joblib')
WeekState = joblib.load('./XLSX/'+Option+'/WeekState.joblib')
MonthState = joblib.load('./XLSX/'+Option+'/MonthState.joblib')
YearState = joblib.load('./XLSX/'+Option+'/YearState.joblib')
DatePoint = WindowPoint['Dates']
DatePoint[0] = DatePoint[1]
DatePoint[1] = pd.Timestamp(g_Day)
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

########### Mth
# Area
df = pd.DataFrame(ak.stock_szse_area_summary(date=g_Month))
df = df.sort_values(by='地区')
df = df.fillna(0)
df.to_excel('./XLSX/Area/' + g_Month + '.xlsx', index=False)
# Field
df = ak.stock_szse_sector_summary(symbol="当月", date=g_Month)
df = df.fillna(0)
df.to_excel('./XLSX/Field/' + g_Month + '.xlsx', index=False)
