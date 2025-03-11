import akshare as ak
import pandas as pd

filename = 'data.txt'
array = []
with open(filename, 'r') as file:
    for line in file:
        line = line.strip()  # 去除行尾换行符和空格
        elements = line.split()  # 将行字符串按空格分隔为数组
        array.extend(elements)  # 将行数组添加到总数组中

#print(dates)
for id in array:
    df0 = pd.DataFrame(ak.stock_zh_a_hist(symbol=id, period="daily", start_date="20190101", end_date='20240928', adjust="hfq"))
# 写入CSV文件
    temp='./identity/'+id+'.xlsx'
    df0.to_excel(temp, index=False)
