import requests
from bs4 import BeautifulSoup

# 目标URL
url = 'https://quote.eastmoney.com/concept/sh603777.html'

# 发送HTTP GET请求
response = requests.get(url)

# 检查请求是否成功
if response.status_code == 200:
    # 解析HTML内容
    soup = BeautifulSoup(response.text, 'html.parser')

    # 打印网页标题
    print("网页标题:", soup.title.string)

    # 打印网页中的所有链接
    for link in soup.find_all('a'):
        print(link.get('href'))
else:
    print(f"请求失败，状态码: {response.status_code}")