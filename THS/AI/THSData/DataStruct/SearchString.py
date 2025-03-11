import os


def search_files(directory, search_text, file_extension=None):
    """
    在指定目录及其子目录中搜索包含特定字符串的文件。

    :param directory: 要搜索的目录路径
    :param search_text: 要搜索的字符串
    :param file_extension: 文件扩展名过滤器（例如 ".txt"），如果为 None 则处理所有文件
    :return: 包含搜索字符串的文件路径列表
    """
    matching_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            # 如果指定了文件扩展名过滤器，则跳过不匹配的文件
            if file_extension and not file.endswith(file_extension):
                continue

            file_path = os.path.join(root, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # 如果搜索文本存在于文件内容中，则添加到匹配文件列表
            if search_text in content:
                matching_files.append(file_path)
    return matching_files


def replace_in_files(file_list, search_text, replace_text):
    """
    在指定文件列表中搜索并替换特定字符串。

    :param file_list: 包含要处理的文件路径列表
    :param search_text: 要搜索的字符串
    :param replace_text: 要替换的字符串
    """
    for file_path in file_list:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 进行替换并写回文件
        new_content = content.replace(search_text, replace_text)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Replaced '{search_text}' with '{replace_text}' in {file_path}")


search_text = 'ipv6'
directory = './Tools/SearchString'
matching_files = search_files(directory, search_text)
if matching_files:
    print("Matching files found:")
    for file_path in matching_files:
        print(file_path)

replace_text = '0'
replace_in_files(matching_files, search_text, replace_text)