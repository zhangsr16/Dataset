import os
import pandas as pd


def replace_errors_in_excel(file_path, replacements):
    try:
        # 读取xls文件
        df = pd.read_excel(file_path, engine='openpyxl', dtype=str)
        # 替换错误字符
        for error_char, replacement_char in replacements.items():
            df = df.map(lambda x: x.replace(error_char, replacement_char) if isinstance(x, str) else x)
        # 删除原xls文件
        os.remove(file_path)
        # 保存为xlsx文件
        df.to_excel(file_path, index=False)


    except Exception as e:
        print(f"Failed to process {file_path}: {e}")


def batch_process_xls(directory, replacements):
    # 遍历目录中的所有文件
    for filename in os.listdir(directory):
        if filename.endswith('.xlsx'):
            file_path = os.path.join(directory, filename)
            replace_errors_in_excel(file_path, replacements)


# 设置要处理的目录和要替换的字符
directory = "F:/Desktop/THS/data/test2"  # 替换为你的目录路径
replacements = {
    "%": "",
    "↑": "",
    "↓": "",
    "-": "",
    "亏损": "-1",
    "负资产": "-1",
}  # 替换为你要替换的错误字符和正确字符的对应关系

batch_process_xls(directory, replacements)
