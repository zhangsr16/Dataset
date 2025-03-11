import os
import pandas as pd

def FIELDSummary():
    ROWNAMES = ['市价总值', '平均市盈率', '成交量', '成交金额', '挂牌数', '换手率', '流通市值', '流通换手率']
    label_folders = [f.path for f in os.scandir('./XLSX/Summary/')]
    for label_folder in label_folders:
        # NewFrame
        dataframe = pd.read_excel(label_folder, engine='openpyxl')
        dayframe = dataframe[dataframe.apply(lambda row: row['单日情况'] in ROWNAMES, axis=1)]
        dayframe = dayframe.fillna(0)
        dayframe.to_excel(label_folder, index=False)

def FIELDArea():
    ROWNAMES = ['市价总值', '平均市盈率', '成交量', '成交金额', '挂牌数', '换手率', '流通市值', '流通换手率']
    label_folders = [f.path for f in os.scandir('./XLSX/Area/')]
    for label_folder in label_folders:
        # NewFrame
        dataframe = pd.read_excel(label_folder, engine='openpyxl')
        dayframe = dataframe.sort_values(by='地区')
        dayframe = dayframe.fillna(0)
        dayframe.to_excel(label_folder, index=False)

def FIELDType():
    ROWNAMES = ['股票', '主板A股', '主板B股', '创业板A股', '基金', 'ETF', 'LOF', '封闭式基金', '债券',
                '债券现券', '债券回购', 'ABS']
    label_folders = [f.path for f in os.scandir('./XLSX/Type/')]
    for label_folder in label_folders:
        # NewFrame
        dataframe = pd.read_excel(label_folder, engine='openpyxl')
        dayframe = dataframe[dataframe.apply(lambda row: row['证券类别'] in ROWNAMES, axis=1)]
        dayframe = dayframe.fillna(0)
        dayframe.to_excel(label_folder, index=False)

FIELDType()