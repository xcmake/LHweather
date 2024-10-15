import requests
from bs4 import BeautifulSoup
import json
import time

# WordPress API 配置
WP_URL = 'https://game.xxcxx.lat/wp-json/wp/v2/posts'
WP_USERNAME = 'xxcxx'
WP_APP_PASSWORD = 'eJQF VKtM TRWN anRD kwte 3PO2'

# 请求头和 Cookies 配置
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Content-Type': 'application/json'
}

COOKIES = {
    'cookie': 'browserid=3296133931599084608; timezoneOffset=28800,0; steamCountry=JP%7Cca9a3680d0675664cf6cad86d2e5c475; sessionid=6c3fe4faf53fa22480a7a2b7; ak_bmsc=F723D266C1509D9A03D2EB9944333487~000000000000000000000000000000~YAAQ9DDUF4X1FnSSAQAAU2A6eRn7KFaDxCnuKp4brs1WTH5ScN4o5/L+ObdWRbAs3Xm25WTMndYFEWav6DLOSTaPLz070Zi5He31GCxVDHzrnEh0eQ4nyMJQOAdDsOq6dZYgMc+R5LTDYYRU3z/fPoF+xIse8bkN+TKbQBg459Hp0SJpl9tWczxus5KE6IDmEM3Pt4vTVpQclnOYk/rbNA6S0M7LeMxGxIZqblrL9jcW8BtkoWOsgfqYa1awLYepqoRlYWxtyuXBRZgRwMP8fvMUG2pZCA/LdzTyNgM6pUzkIvIhvcqOuOqrVDwd34pC0dIrIcbdifDUgmwq7LkNWWZjqZ+0E5mPlrTBXNrMQzffcPAvU4T09ivVsa8Bv2fZ1FGCPDNVNA==; bm_sv=78452DF7E7CA1D3B2ACA12A41FEA2ED2~YAAQ9DDUFxf8FnSSAQAA7aI6eRnO6hMTbw71dnhs904nQLR2dAJ9vHRUWOg15W5nE2Mex3JW+rCfyICrvO51VnUTLTXmEArh1bs5ZCg/HdXqBvmxJEWCHgBI/3Kdl/fooQFiI0c6bF/co0ZmjyO204Rms0k/BQAq2ak+WBRfmlCiAfu4UNirWfOS2NsYI2GXP9t5Wu4S1axC2uD7YXhc53BC/zc/iGq5fhJ4d9k73yuL4hmD/fwL3OTJF9sdqPsZ19tPAE5q~1; steamLoginSecure=76561199133524980%7C%7CeyAidHlwIjogIkpXVCIsICJhbGciOiAiRWREU0EiIH0.eyAiaXNzIjogInI6MTk2NF8yNTMwQTZCNl9CQzZDMyIsICJzdWIiOiAiNzY1NjExOTkxMzM1MjQ5ODAiLCAiYXVkIjogWyAid2ViOnN0b3JlIiBdLCAiZXhwIjogMTcyODY5NzMxMSwgIm5iZiI6IDE3MTk5NzA3MzgsICJpYXQiOiAxNzI4NjEwNzM4LCAianRpIjogIjE3NUJfMjUzMEE1NTBfREE3NTMiLCAib2F0IjogMTcyODYxMDczOCwgInJ0X2V4cCI6IDE3NDY1NTQyNTgsICJwZXIiOiAwLCAiaXBfc3ViamVjdCI6ICIxNTQuNjQuMjI2LjEzMyIsICJpcF9jb25maXJtZXIiOiAiMTAzLjExNi43Mi4xMzEiIH0.e57uz2iydc0Mi6Sz6XJ6VP0uAM8kMvkdCHEfR1ddvrST9m11N6bxxL5bnz1-JNcAssK7FevkPiUZ_L0b-ikoBQ; deep_dive_carousel_focused_app=730; deep_dive_carousel_method=default; recentapps=%7B%222995920%22%3A1728611201%2C%22413150%22%3A1728544253%2C%222358720%22%3A1724750514%7D; app_impressions=1426210%401_7_15__13%7C2995920%401_7_15__13%7C1434480%401_7_7_151_150_1%7C2106520%401_7_7_151_150_1%7C1591600%401_7_7_151_150_1%7C1730910%401_7_7_151_150_1%7C2799930%401_7_7_151_150_1%7C2764370%401_7_7_151_150_1%7C3164300%401_7_7_151_150_1%7C1189490%401_7_7_151_150_1%7C1606180%401_7_7_151_150_1%7C2875140%401_7_7_151_150_1%7C1180320%401_7_7_151_150_1%7C1426210%401_7_7_151_150_1%7C477160%401_5_9__414%7C477160%401_5_9__414%7C1462570%401_5_9__18%7C1426210%401_5_9__300%7C2555360%401_5_9__18%7C1509960%401_5_9__300%7C2316580%401_5_9__18%7C448510%401_5_9__300%7C860510%401_5_9__300'
}


def load_json(file_path):
    """加载本地 JSON 文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"加载 JSON 文件失败: {e}")
        return {}


def fetch_game_data(url):
    """抓取 Steam Store 页面的游戏数据"""
    try:
        response = requests.get(url, headers=HEADERS, cookies=COOKIES, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"请求 URL 失败 ({url}): {e}")
        return None

    soup = BeautifulSoup(response.text, 'lxml')

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
    main_div = soup.find_all('div', class_='highlight_player_item')
    href_list = []
    for div in main_div:
        links = div.find_all('a', href=True)
        for link in links:
            href_list.append(link['href'])
            if len(href_list) >= 3:  # 只获取前三个链接
                break
        if len(href_list) >= 3:
            break

    return {
        'title': title,
        'image_src': image_src,
        'description': description,
        'recommended': recommended,
        'screenshots': href_list
    }


def create_post_content(game_data):
    """根据抓取的数据生成文章内容"""
    screenshots_html = ''.join(
        [f'<img src="{href}" alt="游戏截图" /><br /><br />' for href in game_data['screenshots']])
    content = f"""
    <h3>游戏简介</h3>
    {game_data['description']}

    <h3>游戏封面</h3>
    <img src="{game_data['image_src']}" alt="游戏封面" />

    <h3>游戏截图</h3>
    {screenshots_html}

    <h3>推荐配置</h3>
    {game_data['recommended']}
    """
    return content


def post_to_wordpress(title, content):
    """通过 WordPress REST API 发布文章"""
    post = {
        'title': title,
        'content': content,
        'status': 'publish',
    }
    try:
        response = requests.post(WP_URL, json=post, auth=(WP_USERNAME, WP_APP_PASSWORD))
        response.raise_for_status()
        if response.status_code == 201:
            print(f"文章 '{title}' 创建成功！")
        else:
            print(f"文章 '{title}' 创建失败，状态码：{response.status_code}, 信息：{response.json()}")
    except requests.RequestException as e:
        print(f"发布文章 '{title}' 失败: {e}")


def main():
    # 加载 JSON 文件
    json_file = 'game_links.json'  # 替换为你的 JSON 文件路径
    games = load_json(json_file)
    if not games:
        print("没有游戏数据可处理。")
        return

    for game_title, url in games.items():
        print(f"处理游戏: {game_title}")
        game_data = fetch_game_data(url)
        if game_data is None:
            print(f"跳过游戏: {game_title}")
            continue

        # 如果需要使用 JSON 中的标题而不是抓取的标题，可以覆盖
        # game_data['title'] = game_title

        content = create_post_content(game_data)
        post_to_wordpress(game_data['title'], content)

        # 为了避免过快的请求，建议添加延时
        time.sleep(2)  # 延时2秒，可根据需要调整


if __name__ == "__main__":
    main()
