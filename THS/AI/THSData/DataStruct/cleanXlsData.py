import os
import pandas as pd

def replace_errors_in_excel(file_path, replacements):
    # 读取xls文件
    df = pd.read_excel(file_path, engine='openpyxl', dtype=str)
    # 替换错误字符
    for error_char, replacement_char in replacements.items():
        df = df.applymap(lambda x: x.replace(error_char, replacement_char) if isinstance(x, str) else x)
    # 尝试将所有列转换为数值类型
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='ignore')
    # 删除原xls文件
    os.remove(file_path)
    # 保存为xlsx文件
    df.to_excel(file_path, index=False)

def trans_summary_dataframe(file_path):
    df = pd.read_excel(file_path, engine='openpyxl')
    # 将 'index_column' 列设置为新的行索引
    df.set_index('单日情况', inplace=True)
    # 转置 DataFrame
    df_transposed = df.transpose()
    # 重置索引以便查看
    df_transposed.reset_index(inplace=True)
    # 获取新的列名
    new_columns = df_transposed.columns.tolist()
    new_columns[0] = '版块'
    df_transposed.columns = new_columns
    # 删除原xls文件
    os.remove(file_path)
    # 保存为xlsx文件
    df_transposed.to_excel(file_path, index=False)


# 设置要处理的目录
directory = "./"  # 替换为你的目录路径
# 替换
replacements = {
    "%": "",
    "↑": "",
    "↓": "",
    "-": "",
    "亏损": "-1",
    "负资产": "-1",
}
for filename in os.listdir(directory):
    if filename.endswith('.xlsx'):
        file_path = os.path.join(directory, filename)
        trans_summary_dataframe(file_path)
        #replace_errors_in_excel(file_path, replacements)
