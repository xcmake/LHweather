import requests
from bs4 import BeautifulSoup
import json

# 请求头配置
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
}

# 搜索每个标题并获取 Steam 链接
search_url = 'https://store.steampowered.com/app/534380/2/'
response = requests.get(search_url, headers=header)
soup = BeautifulSoup(response.text, 'lxml')

img_links = soup.find_all('a', class_='highlight_screenshot_link')[:3]
# 提取 href 属性
for link in img_links:
    href = link.get('href')
    print("图片链接:", href)

# print(soup)
