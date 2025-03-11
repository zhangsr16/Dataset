import os
import numpy as np
import pandas as pd

fieldframes = {}

CYCLES = ['Month', 'Week', 'Day']
# FIELD
# 地区交易排序（月）、股票行业成交（月）、上海证券交易所（日）、证券类别统计（日）
FPTIONS = ['Type', 'Area', 'Field', 'Summary']
COLNAMES = [['数量', '成交金额', '总市值', '流通市值'],
            ['总交易额', '占市场', '股票交易额', '基金交易额', '债券交易额'],
            ['交易天数', '成交金额-人民币元', '成交金额-占总计', '成交股数-股数', '成交股数-占总计', '成交笔数-笔',
             '成交笔数-占总计']
    , ['股票', '主板A', '主板B', '科创板', '股票回购']]
# for fption in FPTIONS:
#     for cyc in CYCLES:
#         os.makedirs('./XLSX/Time/' + cyc + '/' + fption, exist_ok=True)


############Summary
def FIELDSummary():
    fption = 'Summary'
    COLNAMES = ['股票', '主板A', '主板B', '科创板', '股票回购']
    NEWCOLS = ['Year', 'Mth', 'Week', 'Day', 'Date']
    ROWNAMES = ['市价总值', '平均市盈率', '成交量', '成交金额', '挂牌数', '换手率', '流通市值', '流通换手率']
    label_folders = [f.path for f in os.scandir('./XLSX/Summary/')]
    LenCol = len(COLNAMES)
    LenDay = len(label_folders)
    LenRow = len(ROWNAMES)
    hashcol = {}
    for i in range(LenCol):
        hashcol[COLNAMES[i]] = i
    TempMatrix = np.empty((LenDay, LenCol, LenRow + len(NEWCOLS)))
    Dates = [[]]
    period = periodMth = DayPos = WeekPos = 0
    idx = 0
    for label_folder in label_folders:
        DayPos += 1
        if len(Dates) == 1:
            Dates[0] = (os.path.basename(label_folder).rstrip(".xlsx"))
            Dates.append(Dates[0])
        else:
            Dates[0] = Dates[1]
            Dates[1] = (os.path.basename(label_folder).rstrip(".xlsx"))
            if pd.Timestamp(Dates[1]) - pd.Timestamp(Dates[0]) != pd.Timedelta('1 days 00:00:00'):
                DayPos = 0
                WeekPos += 1
                period += 1
            if pd.Timestamp(Dates[1]).month != pd.Timestamp(Dates[0]).month:
                WeekPos = 0
                periodMth += 1
        # NewFrame
        dataframe = pd.read_excel(label_folder, engine='openpyxl')
        dayframe = dataframe[dataframe.apply(lambda row: row['单日情况'] in ROWNAMES, axis=1)]
        dayframe = dayframe.fillna(0)
        dayframe.to_excel('./XLSX/Type/' + label_folder, index=False)
        dayframe = dayframe.reset_index(drop=True)
        hashrow = {}
        for i in range(LenRow):
            hashrow[ROWNAMES[i]] = i
        for col_idx in COLNAMES:
            row = 0
            for row_idx in ROWNAMES:
                try:
                    TempMatrix[idx, hashcol[col_idx], row] = dayframe[col_idx][hashrow[row_idx]]
                except KeyError as _:
                    print("Warning!: no exist in COLNAMES.")
                    continue
                row += 1
            TempMatrix[idx, hashcol[col_idx], row] = pd.Timestamp(Dates[0]).year
            TempMatrix[idx, hashcol[col_idx], row + 1] = pd.Timestamp(Dates[0]).month
            TempMatrix[idx, hashcol[col_idx], row + 2] = WeekPos
            TempMatrix[idx, hashcol[col_idx], row + 3] = DayPos
            TempMatrix[idx, hashcol[col_idx], row + 4] = Dates[0]
        idx += 1
    for col_idx in COLNAMES:
        TempDataframe = pd.DataFrame(index=range(idx), columns=ROWNAMES + NEWCOLS)
        for iday in range(idx):
            row = 0
            for row_idx in (ROWNAMES + NEWCOLS):
                TempDataframe[row_idx][iday] = TempMatrix[iday, hashcol[col_idx], row]
                row += 1
        TempDataframe.to_excel('./XLSX/Time/Day/Summary/' + col_idx + '.xlsx', index=False)


############Field
def FIELDField():
    fption = 'Field'
    COLNAMES = ['交易天数', '成交金额-人民币元', '成交金额-占总计', '成交股数-股数', '成交股数-占总计', '成交笔数-笔',
                '成交笔数-占总计']
    ROWNAMES = ['合计', '农林牧渔', '采矿业', '制造业', '水电煤气', '建筑业', '批发零售', '运输仓储', '住宿餐饮',
                '信息技术', '金融业', '房地产', '商务服务', '科研服务', '公共环保', '居民服务', '教育', '卫生',
                '文化传播',
                '综合']
    NEWCOLS = ['Year', 'Mth', 'Date']
    label_folders = [f.path for f in os.scandir('./XLSX/Field/')]
    LenCol = len(COLNAMES)
    LenDay = len(label_folders)
    LenRow = len(ROWNAMES)
    hashcol = {}
    for i in range(LenCol):
        hashcol[COLNAMES[i]] = i
    TempMatrix = np.empty((LenDay, LenCol, LenRow + len(NEWCOLS)))
    idx = 0
    for label_folder in label_folders:
        Date = (os.path.basename(label_folder).rstrip(".xlsx"))
        # NewFrame
        dataframe = pd.read_excel(label_folder, engine='openpyxl')
        dayframe = dataframe.fillna(0)
        hashrow = {}
        for i in range(LenRow):
            hashrow[ROWNAMES[i]] = i
        for col_idx in COLNAMES:
            row = 0
            for row_idx in ROWNAMES:
                try:
                    TempMatrix[idx, hashcol[col_idx], row] = dayframe[col_idx][hashrow[row_idx]]
                except KeyError as _:
                    print("Warning!: no exist in COLNAMES.")
                    continue
                row += 1
            TempMatrix[idx, hashcol[col_idx], row] = Date[0:4]  # Year
            TempMatrix[idx, hashcol[col_idx], row + 1] = Date[4:6]  # Month
            TempMatrix[idx, hashcol[col_idx], row + 2] = Date
        idx += 1
    for col_idx in COLNAMES:
        TempDataframe = pd.DataFrame(index=range(idx), columns=ROWNAMES + NEWCOLS)
        for iday in range(idx):
            row = 0
            for row_idx in (ROWNAMES + NEWCOLS):
                TempDataframe[row_idx][iday] = TempMatrix[iday, hashcol[col_idx], row]
                row += 1
        TempDataframe.to_excel('./XLSX/Time/Month/Field/' + col_idx + '.xlsx', index=False)


############Area
def FIELDArea():
    fption = 'Area'
    COLNAMES = ['总交易额', '占市场', '股票交易额', '基金交易额', '债券交易额']
    ROWNAMES = ['上海', '深圳', '北京', '浙江', '江苏', '广东', '福建', '广州', '山东', '四川', '湖北', '湖南', '安徽',
                '境外地区', '河南', '辽宁', '西藏', '江西', '陕西', '河北', '重庆', '天津', '山西', '广西', '黑龙江',
                '吉林', '云南', '内蒙古', '贵州', '新疆', '海南', '甘肃', '宁夏', '青海']
    NEWCOLS = ['Year', 'Mth', 'Date']
    label_folders = [f.path for f in os.scandir('./XLSX/Area/')]
    LenCol = len(COLNAMES)
    LenDay = len(label_folders)
    LenRow = len(ROWNAMES)
    hashcol = {}
    for i in range(LenCol):
        hashcol[COLNAMES[i]] = i
    TempMatrix = np.empty((LenDay, LenCol, LenRow + len(NEWCOLS)))
    idx = 0
    for label_folder in label_folders:
        Date = (os.path.basename(label_folder).rstrip(".xlsx"))
        # NewFrame
        dataframe = pd.read_excel(label_folder, engine='openpyxl')
        dayframe = dataframe.fillna(0)
        hashrow = {}
        for i in range(LenRow):
            hashrow[ROWNAMES[i]] = i
        for col_idx in COLNAMES:
            row = 0
            for row_idx in ROWNAMES:
                try:
                    TempMatrix[idx, hashcol[col_idx], row] = dayframe[col_idx][hashrow[row_idx]]
                except KeyError as _:
                    print("Warning!: no exist in COLNAMES.")
                    continue
                row += 1
            TempMatrix[idx, hashcol[col_idx], row] = Date[0:4]  # Year
            TempMatrix[idx, hashcol[col_idx], row + 1] = Date[4:6]  # Month
            TempMatrix[idx, hashcol[col_idx], row + 2] = Date
        idx += 1
    for col_idx in COLNAMES:
        TempDataframe = pd.DataFrame(index=range(idx), columns=ROWNAMES + NEWCOLS)
        for iday in range(idx):
            row = 0
            for row_idx in (ROWNAMES + NEWCOLS):
                TempDataframe[row_idx][iday] = TempMatrix[iday, hashcol[col_idx], row]
                row += 1
        TempDataframe.to_excel('./XLSX/Time/Month/Area/' + col_idx + '.xlsx', index=False)


############Type
def FIELDType():
    fption = 'Type'
    COLNAMES = ['数量', '成交金额', '总市值', '流通市值']
    NEWCOLS = ['Year', 'Mth', 'Week', 'Day', 'Date']
    # del = 中小板 期权
    ROWNAMES = ['股票', '主板A股', '主板B股', '创业板A股', '基金', 'ETF', 'LOF', '封闭式基金', '债券',
                '债券现券', '债券回购', 'ABS']
    label_folders = [f.path for f in os.scandir('./XLSX/Type/')]
    LenCol = len(COLNAMES)
    LenDay = len(label_folders)
    LenRow = len(ROWNAMES)
    hashcol = {}
    for i in range(LenCol):
        hashcol[COLNAMES[i]] = i
    TempMatrix = np.empty((LenDay, LenCol, LenRow + len(NEWCOLS)))
    Dates = [[]]
    period = periodMth = DayPos = WeekPos = 0
    idx = 0
    for label_folder in label_folders:
        DayPos += 1
        if len(Dates) == 1:
            Dates[0] = (os.path.basename(label_folder).rstrip(".xlsx"))
            Dates.append(Dates[0])
        else:
            Dates[0] = Dates[1]
            Dates[1] = (os.path.basename(label_folder).rstrip(".xlsx"))
            if pd.Timestamp(Dates[1]) - pd.Timestamp(Dates[0]) != pd.Timedelta('1 days 00:00:00'):
                DayPos = 0
                WeekPos += 1
                period += 1
            if pd.Timestamp(Dates[1]).month != pd.Timestamp(Dates[0]).month:
                WeekPos = 0
                periodMth += 1
        # NewFrame
        dataframe = pd.read_excel(label_folder, engine='openpyxl')
        dayframe = dataframe[dataframe.apply(lambda row: row['证券类别'] in ROWNAMES, axis=1)]
        dayframe = dayframe.fillna(0)
        dayframe = dayframe.reset_index(drop=True)
        hashrow = {}
        for i in range(LenRow):
            hashrow[ROWNAMES[i]] = i
        for col_idx in COLNAMES:
            row = 0
            for row_idx in ROWNAMES:
                try:
                    TempMatrix[idx, hashcol[col_idx], row] = dayframe[col_idx][hashrow[row_idx]]
                except KeyError as _:
                    print("Warning!: no exist in COLNAMES.")
                    continue
                row += 1
            TempMatrix[idx, hashcol[col_idx], row] = pd.Timestamp(Dates[0]).year
            TempMatrix[idx, hashcol[col_idx], row + 1] = pd.Timestamp(Dates[0]).month
            TempMatrix[idx, hashcol[col_idx], row + 2] = WeekPos
            TempMatrix[idx, hashcol[col_idx], row + 3] = DayPos
            TempMatrix[idx, hashcol[col_idx], row + 4] = Dates[0]
        idx += 1
    for col_idx in COLNAMES:
        TempDataframe = pd.DataFrame(index=range(idx), columns=ROWNAMES + NEWCOLS)
        for iday in range(idx):
            row = 0
            for row_idx in (ROWNAMES + NEWCOLS):
                TempDataframe[row_idx][iday] = TempMatrix[iday, hashcol[col_idx], row]
                row += 1
        TempDataframe.to_excel('./XLSX/Time/Day/Type/' + col_idx + '.xlsx', index=False)

FIELDSummary()
