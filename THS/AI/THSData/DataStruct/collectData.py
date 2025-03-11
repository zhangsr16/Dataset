import akshare as ak
import pandas as pd
import numpy as np
import os

#################################### 时间
#################### 拼接时间戳
# cycle = 6  # Years
# years = [0] * cycle
# mths = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
# days = []
# i = 0
# fstyear = 2019
# while i < cycle:
#     years[i] = fstyear + i
#     years[i] = str(years[i])
#     i = i + 1
# dates = ['0'] * cycle * 12
# i = 0
# for y in years:
#     for m in mths:
#         tempstr = y + m
#         dates[i] = tempstr
#         i = i + 1
dates = ['202408', '202409', '202410', '202411', '202412', '202501']
# for d in range(1, 32):
#     if d < 12:
#         days.append(mths[d - 1])
#     else:
#         days.append(str(d))
#################### 导入时间戳date.txt
# df = pd.DataFrame(
#     ak.stock_zh_a_hist(symbol='603777', period="daily", start_date="20240926", end_date='20250217', adjust="hfq"))
# df.to_excel('./XLSX/000034.xlsx', index=False)
#################### 修改时间戳date.txt
# dates = []
# with open('./XLSX/date.txt', 'r') as file:
#     for date in file:
#         dates.append(date.strip())  # 去除尾空

#################################### Spider
# # 当天总貌
# ak.stock_sse_summary()
############ 月
# # 地区
# for mth in dates:
#     df= pd.DataFrame((ak.stock_szse_area_summary(date='202501')))
#     df.to_excel('./XLSX/Area/'+mth+'.xlsx', index=False)
# # 行业
# for date in dates:
#     df = ak.stock_szse_sector_summary(symbol="当月", date=date)
#     if df.shape[0] != 0:
#         df.to_excel('./XLSX/Field/' + date + '.xlsx', index=False)
############# 日
# 证券类别
# for date in dates:
#     df = ak.stock_szse_summary(date=date)
#     if df.shape[0] != 0:
#         df.to_excel('./XLSX/Type/' + date + '.xlsx', index=False)
# # 交易所
# for date in dates:
#     df = ak.stock_sse_deal_daily(date=date)
#     if df.shape[0] != 0:
#         df.to_excel('./XLSX/Summary/' + date + '.xlsx', index=False)
# 个股历史
# 继承
label_folders = [f.path for f in os.scandir("./XLSX/Stock/20240927")]
for label_folder in label_folders:
    stockid = os.path.basename(label_folder).rstrip(".xlsx")
    df0 = pd.DataFrame(
        ak.stock_zh_a_hist(symbol=stockid, period="daily", start_date="20240928", end_date='20250127',
                           adjust="hfq"))  # 后复权
    # 写入CSV文件
    temp = './XLSX/Stock/20250204/' + stockid + '.xlsx'
    df0.to_excel(temp, index=False)

# Cold start
array = []
with open('./XLSX/symbol.txt', 'r') as file:
    for line in file:
        line = line.strip()  # 去除尾空
        elements = line.split()  # 按分隔为数组
        array.extend(elements)  # 将行数组添加到总数组中
for stockid in array:
    df0 = pd.DataFrame(
        ak.stock_zh_a_hist(symbol=stockid, period="daily", start_date="20190101", end_date='20240928', adjust="hfq"))  # 后复权
    # 写入CSV文件
    temp = './XLSX/Stock/20250204/' + stockid + '.xlsx'
    df0.to_excel(temp, index=False)

# 重构数据结构
fption = 'Type'
# 交易所 地区 行业 类型
dataframe = pd.read_excel('./CNXLSX/' + fption + '.xlsx', engine='openpyxl').dropna(subset=['date'])
dataframe = dataframe.reset_index(drop=True)
nrows = dataframe.shape[0]
start = end = 0
for row_idx in range(nrows - 1):
    end += 1
    if dataframe['date'][row_idx] != dataframe['date'][row_idx + 1]:
        df = dataframe[start:end]
        del (df['date'])
        df.to_excel('./XLSX/' + fption + '/' + str(int(dataframe['date'][row_idx])) + '.xlsx', index=False)
        start = end
