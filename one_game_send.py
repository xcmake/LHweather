import requests
from bs4 import BeautifulSoup

# WordPress API 配置
wp_url = 'https://game.xxcxx.lat/wp-json/wp/v2/posts'
wp_username = 'xxcxx'
wp_app_password = 'POhl oBGu tPEa ESGV Yuig og5A'

# 请求头和 Cookies 配置（用于抓取 Steam 页面）
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Content-Type': 'application/json'
}

COOKIES = {
    'cookie': 'browserid=3296133931599084608; timezoneOffset=28800,0; lastagecheckage=1-January-1983; steamCountry=JP%7Cb22d9d5351db4b970f057633e6c62c8c; sessionid=c5e21380e11dcd5d3270205c; deep_dive_carousel_focused_app=730; deep_dive_carousel_method=default; recentapps=%7B%222917350%22%3A1728974368%2C%22534380%22%3A1728972951%2C%22239140%22%3A1728972936%2C%222567870%22%3A1728972811%2C%222015270%22%3A1728972778%2C%222933130%22%3A1728972721%2C%222195410%22%3A1728964838%2C%22454650%22%3A1728963821%2C%22269210%22%3A1728963810%2C%222878720%22%3A1728725019%7D; app_impressions=2269810%401_5_9__405%7C2370710%401_5_9__405%7C2370700%401_5_9__405%7C2370460%401_5_9__405%7C2456710%401_5_9__405%7C2325290%401_4_4__129_1%7C582010%401_4_4__636_1%7C1551360%401_4_4__636_1%7C2322010%401_4_4__636_1%7C381210%401_4_4__636_1%7C1675200%401_4_4__147%7C2239150%401_4_4__145_1%7C2141730%401_4_4__137_1%7C2113850%401_4_4__137_1%7C1637320%401_4_4__137_1%7C2593370%401_4_4__137_1%7C1101120%401_4_4__145_9%7C1272320%401_4_4__145_8%7C2917350%401_4_4__145_7%7C3092660%401_4_4__145_6%7C3034520%401_4_4__145_5%7C1663040%401_4_4__145_4%7C1790600%401_4_4__145_3%7C2679460%401_4_4__145_2%7C2956820%401_4_4__145_10%7C751630%401_4_4__141_1%7C3193770%401_4_4__141_1%7C1906020%401_4_4__141_1%7C1059530%3A1059550%3A1059570%401_4_4__141_1%7C3008340%401_5_9__18%7C2738490%401_5_9__18%7C2400770%401_5_9__18%7C1639080%401_5_9__18%7C2379780%401_5_9__300%7C646570%401_5_9__300%7C2118810%401_5_9__300%7C2440380%401_5_9__300'
}

# 目标 URL
url = 'https://store.steampowered.com/app/1426210/_/'

# 获取网页内容
rest = requests.get(url, headers=HEADERS, cookies=COOKIES)
# 解析 HTML
soup = BeautifulSoup(rest.text, 'lxml')

# 获取游戏标题
game_title = soup.find('div', class_='apphub_AppName')
title = game_title.text.strip() if game_title else "未找到标题"

# 获取特色图片的src
header_image = soup.find('img', class_='game_header_image_full')
image_src = header_image['src'] if header_image else ""

# 获取简介
wrap_rank = soup.find('div', class_='game_description_snippet')
description = wrap_rank.text.strip() if wrap_rank else "未找到简介"

# 获取推荐配置
recommendation_div = soup.find('div', class_='game_area_sys_req_leftCol')
recommended = ""
if recommendation_div:
    li_elements = recommendation_div.find_all('li')
    recommended += "\n".join(li.text.strip() for li in li_elements)
else:
    recommended = "未找到推荐配置"

# 获取截图链接并确保每张图片换行
img_links = soup.find_all('a', class_='highlight_screenshot_link')[:3]
src_list = []

for link in img_links:
    img_tag = link.find('img')  # 找到嵌套的img标签
    if img_tag and 'src' in img_tag.attrs:  # 检查是否存在img标签和src属性
        src_list.append(img_tag['src'])
        print(src_list)

# # 生成文章内容
# content = f"""
# <h3>游戏简介</h3>
# {description}
#
# <h3>游戏封面</h3>
# <img src="{image_src}" alt="游戏封面" />
#
# <h3>游戏截图</h3>
# {''.join([f'<img src="{href}" alt="游戏截图" /><br /><br />' for href in href_list])}
#
# <h3>推荐配置</h3>
# {recommended}
# """
#
# # 请求体
# post = {
#     'title': title,
#     'content': content,
#     'status': 'publish',
# }
#
# # 创建文章
# response = requests.post(wp_url, json=post, auth=(wp_username, wp_app_password))
#
# # 检查请求结果
# if response.status_code == 201:
#     print("文章创建成功！")
# else:
#     print(f"文章创建失败，状态码：{response.status_code}, 信息：{response.json()}")
