import requests
from bs4 import BeautifulSoup
import json

# 请求头配置
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
}

# 从 game_detail_new_en.json 文件读取数据
input_file = "game_detail_new_en.json"
with open(input_file, "r", encoding="utf-8") as file:
    data = json.load(file)

# 搜索每个标题并获取 Steam 链接
for item in data:
    title = item["title"]
    search_url = f'https://store.steampowered.com/search/?term={title}'
    response = requests.get(search_url, headers=header)
    soup = BeautifulSoup(response.text, 'lxml')

    # 查找搜索结果中的第一个链接
    a_tags = soup.find('div', id='search_resultsRows')
    if a_tags:
        a_link = a_tags.find('a')
        if a_link:
            href = a_link.get('href')
            # 将 Steam 链接添加到该数据项的 steam_link 字段
            item["steam_link"] = href
        else:
            # 如果找不到链接，使用 None 作为占位
            item["steam_link"] = None
    else:
        item["steam_link"] = None

# 保存更新后的数据到同一个文件 game_detail_new_en.json
with open("game_detail_new_en.json", "w", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

print("所有 Steam 链接已更新并保存到 game_detail_new_en.json 文件中。")
