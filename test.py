import requests
from bs4 import BeautifulSoup
import pandas as pd  # 导入 pandas 库
import json

# 请求头配置
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
}

COOKIES = {
    'cookie': 'SECKEY_ABVK=TB/6lX9sVayNu9Qd+tU4x+hJR82msZoaI6rTS/s0pJA%3D; BMAP_SECKEY=TKIDV3Z9GYWg1RJfsmmp14NYbLXDRDrOcy2S0jx-3K15n3eVTPW7_k2jBgdQnhuGTjjObQ_8vweLmyW8QrylSYzIDkgNtgBr_SjUjiB6eKOUGnKdrRDKWsFzoBsus9kIxpJtSquQEAeQ8XLMbOT_oMJNVSo8PRKdc15Qeht3wtg5qXBZcaU_2ve0NVqaUQ8i; select_city=420600; lianjia_ssid=790b2bdd-8154-417a-8acd-de9eee907901; lianjia_uuid=d71e59ea-b8c3-41db-8d83-d9c3c5a1f2cd; Hm_lvt_46bf127ac9b856df503ec2dbf942b67e=1730442655; Hm_lpvt_46bf127ac9b856df503ec2dbf942b67e=1730442655; HMACCOUNT=9837F15C5F6B9245; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22192e66b75d17a0-038313ebc466ba-26011951-2359296-192e66b75d2c94%22%2C%22%24device_id%22%3A%22192e66b75d17a0-038313ebc466ba-26011951-2359296-192e66b75d2c94%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.baidu.com%2Flink%22%2C%22%24latest_referrer_host%22%3A%22www.baidu.com%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%7D%7D; _ga=GA1.2.687317964.1730442666; _gid=GA1.2.1671751403.1730442666; GUARANTEE_POPUP_SHOW=true; GUARANTEE_BANNER_SHOW=true; hip=ROPCavX4YxPu2M3oneGbSu8ZRR4qU4sdCbfqnIzkaS0gsiGFUKyvM4PexOvW2Reb_fS1XLZUQbgaIIXm0YJ73HLwdZYw2Gv8CA-M8MYWFuxO-mjmwUE_cbJqv6YYwigt-cIwPpdPRJAFbs5WOYBWVnjAQ0vE2eFJ3bWTPAxNpk9zHYn9YYhafmHXbg%3D%3D; srcid=eyJ0Ijoie1wiZGF0YVwiOlwiYjdhM2ZhYWU1NTI1ZDNjZTEzNDA0NWU4NTJhM2E1ODIxNDcwYTRkY2VhNzhkMGE3ZmU1NzE0OTZmYTJiNTc5OWQyNGZhMDE0ZDM4NDNkY2Q2YWM4MDQ3NTYxYzQ1NzAxZGE5OTU3YzIxZWQyMDU1NGRjYjEzM2JjOTU2ZGNiOGExZWY2ZTlkNzkyOGJjZGJkMTk5MWQ3NDUyMTg2M2ZlOGY4MWU4Yjc0MTJkMDYzZWIzMDYwMzgxYjgzYjM3YjM1ZmM2NWQ3OTVhZmJmY2I3OTQ3OGJlNWUzN2JmYzgzNmU1MmYzNTdjOWQ0MmJhNDEwZmFjZmU2NmYwMmU5NDNkMFwiLFwia2V5X2lkXCI6XCIxXCIsXCJzaWduXCI6XCI4MzQ3YjNlN1wifSIsInIiOiJodHRwczovL3h5LmxpYWFuaWEuY29tL3p1ZmFuZy9yY28yMXJzJUU4JUE1JTg0JUU1JUI3JTlFJUU1JThDJUJBLyIsIm9zIjoid2ViIiwidiI6IjAuMSJ9'
    # 请替换为你的实际 cookie
}

results = []

# 循环遍历每一页
for page in range(1, 101):  # 从 1 到 101
    print(f'正在处理{page}页')
    # search_url = f'https://xy.lianjia.com/zufang/pg{page}rco21rs%E8%A5%84%E5%B7%9E%E5%8C%BA/#contentList'
    search_url = f'https://wh.lianjia.com/zufang/donghugaoxin/pg{page}/#contentList'

    response = requests.get(search_url, headers=header, cookies=COOKIES, timeout=10)
    soup = BeautifulSoup(response.text, 'lxml')

    divs = soup.find_all('div', class_='content__list--item')

    for div in divs:
        # 提取标题和链接
        aside = div.find('a', class_='content__list--item--aside')
        title = aside.get('title') if aside else None
        href = aside.get('href') if aside else None

        # 拼接成完整的链接
        if href and href.startswith('/'):
            href = f'https://wh.lianjia.com{href}'

        # 提取描述信息，去除空格
        des = div.find('p', class_='content__list--item--des')
        description = des.get_text(strip=True).replace(' ', '') if des else None

        # 提取价格信息
        price = div.find('span', class_='content__list--item-price')
        price_info = price.get_text(strip=True) if price else None

        # 存储结果
        results.append({
            'title': title,
            'href': href,
            'description': description,
            'price': price_info
        })

# 将结果输出为 JSON 格式
print(json.dumps(results, ensure_ascii=False, indent=2))

# 将结果保存为 Excel 文件
df = pd.DataFrame(results)  # 创建 DataFrame
df.to_excel('wuhan.xlsx', index=False)  # 保存为 Excel 文件
