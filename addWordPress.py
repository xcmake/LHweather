import requests
from bs4 import BeautifulSoup
import json
import time
import base64
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

# WordPress API 配置
WP_POSTS_URL = 'https://game.xxcxx.lat/wp-json/wp/v2/posts'
WP_TAGS_URL = 'https://game.xxcxx.lat/wp-json/wp/v2/tags'
WP_USERNAME = 'xxcxx'
WP_APP_PASSWORD = 'POhl oBGu tPEa ESGV Yuig og5A'

# 基本认证头
credentials = f"{WP_USERNAME}:{WP_APP_PASSWORD}"
token = base64.b64encode(credentials.encode())
HEADERS_AUTH = {
    'Authorization': f'Basic {token.decode("utf-8")}',
    'Content-Type': 'application/json'
}

# 请求头和 Cookies 配置（用于抓取 Steam 页面）
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Content-Type': 'application/json'
}

COOKIES = {
    'cookie': 'browserid=3296133931599084608; timezoneOffset=28800,0; lastagecheckage=1-January-1983; steamCountry=JP%7Cb22d9d5351db4b970f057633e6c62c8c; sessionid=c5e21380e11dcd5d3270205c; deep_dive_carousel_focused_app=730; deep_dive_carousel_method=default; recentapps=%7B%222917350%22%3A1728974368%2C%22534380%22%3A1728972951%2C%22239140%22%3A1728972936%2C%222567870%22%3A1728972811%2C%222015270%22%3A1728972778%2C%222933130%22%3A1728972721%2C%222195410%22%3A1728964838%2C%22454650%22%3A1728963821%2C%22269210%22%3A1728963810%2C%222878720%22%3A1728725019%7D; app_impressions=2269810%401_5_9__405%7C2370710%401_5_9__405%7C2370700%401_5_9__405%7C2370460%401_5_9__405%7C2456710%401_5_9__405%7C2325290%401_4_4__129_1%7C582010%401_4_4__636_1%7C1551360%401_4_4__636_1%7C2322010%401_4_4__636_1%7C381210%401_4_4__636_1%7C1675200%401_4_4__147%7C2239150%401_4_4__145_1%7C2141730%401_4_4__137_1%7C2113850%401_4_4__137_1%7C1637320%401_4_4__137_1%7C2593370%401_4_4__137_1%7C1101120%401_4_4__145_9%7C1272320%401_4_4__145_8%7C2917350%401_4_4__145_7%7C3092660%401_4_4__145_6%7C3034520%401_4_4__145_5%7C1663040%401_4_4__145_4%7C1790600%401_4_4__145_3%7C2679460%401_4_4__145_2%7C2956820%401_4_4__145_10%7C751630%401_4_4__141_1%7C3193770%401_4_4__141_1%7C1906020%401_4_4__141_1%7C1059530%3A1059550%3A1059570%401_4_4__141_1%7C3008340%401_5_9__18%7C2738490%401_5_9__18%7C2400770%401_5_9__18%7C1639080%401_5_9__18%7C2379780%401_5_9__300%7C646570%401_5_9__300%7C2118810%401_5_9__300%7C2440380%401_5_9__300'
}

# 锁用于线程安全地访问标签缓存
tag_cache_lock = Lock()
existing_tags_cache = {}


def load_json(file_path):
    """加载本地 JSON 文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"加载 JSON 文件失败: {e}")
        return []


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
        recommended = "暂无"

    # 获取截图链接并确保每张图片换行
    img_links = soup.find_all('a', class_='highlight_screenshot_link')[:3]
    href_list = []
    for link in img_links:
        href = link.get('href')
        href_list.append(href)

    # 获取游戏标签
    tags_div = soup.find('div', class_='glance_tags popular_tags')
    game_tags = []

    if tags_div:
        # 获取前两个包含 href 属性的 <a> 标签
        for tag in tags_div.find_all('a', href=True)[:2]:
            game_tags.append(tag.get_text(strip=True))
    else:
        print(f"未找到游戏标签 for {title}")

    return {
        'title': title,
        'image_src': image_src,
        'description': description,
        'recommended': recommended,
        'screenshots': href_list,
        'game_tags': game_tags  # 添加游戏标签到返回的数据中
    }


def create_post_content(game_data):
    """根据抓取的数据生成文章内容，包括下载按钮"""
    download_link = game_data.get('download_link', '#')  # 获取下载链接，默认为 #
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

    <h3>下载链接</h3>
    {download_link}
    """
    return content


def get_tag_id(tag_name):
    """
    获取或创建标签并返回其 ID。
    使用 existing_tags_cache 来缓存已存在的标签，减少 API 请求次数。
    """
    tag_name_lower = tag_name.lower()
    with tag_cache_lock:
        if tag_name_lower in existing_tags_cache:
            return existing_tags_cache[tag_name_lower]

    # 首先尝试获取标签
    params = {'search': tag_name, 'per_page': 100}
    try:
        response = requests.get(WP_TAGS_URL, headers=HEADERS_AUTH, params=params)
        response.raise_for_status()
        tags = response.json()
        for tag in tags:
            if tag['name'].lower() == tag_name_lower:
                with tag_cache_lock:
                    existing_tags_cache[tag_name_lower] = tag['id']
                return tag['id']
    except requests.RequestException as e:
        print(f"获取标签 '{tag_name}' 失败: {e}")
        return None

    # 如果标签不存在，则创建新标签
    new_tag = {
        'name': tag_name,
        'description': f'自动创建的标签: {tag_name}',
        'slug': tag_name_lower.replace(' ', '-')
    }
    try:
        response = requests.post(WP_TAGS_URL, headers=HEADERS_AUTH, json=new_tag)
        response.raise_for_status()
        tag = response.json()
        print(f"创建新标签 '{tag_name}'，ID: {tag['id']}")
        with tag_cache_lock:
            existing_tags_cache[tag_name_lower] = tag['id']
        return tag['id']
    except requests.RequestException as e:
        print(f"创建标签 '{tag_name}' 失败: {e}")
        return None


def post_to_wordpress(title, content, tags):
    """通过 WordPress REST API 发布文章，并添加标签"""
    # 获取所有标签的 ID
    tag_ids = []
    for tag in tags:
        tag_id = get_tag_id(tag)
        if tag_id:
            tag_ids.append(tag_id)

    post = {
        'title': title,
        'content': content,
        'status': 'publish',
    }

    if tag_ids:
        post['tags'] = tag_ids  # 传递标签 ID 列表

    try:
        response = requests.post(WP_POSTS_URL, headers=HEADERS_AUTH, json=post)
        response.raise_for_status()
        if response.status_code == 201:
            print(f"文章 '{title}' 创建成功！")
        else:
            print(f"文章 '{title}' 创建失败，状态码：{response.status_code}, 信息：{response.json()}")
    except requests.RequestException as e:
        print(f"发布文章 '{title}' 失败: {e}")


def process_game(game):
    """处理单个游戏的数据抓取和文章发布"""
    game_title = game.get('title')
    url = game.get('steam_link')
    download_link = game.get('download_link', '#')  # 获取下载链接
    if not game_title or not url:
        print("游戏数据缺失 'title' 或 'steam_link'，跳过。")
        return

    print(f"处理游戏: {game_title}")
    game_data = fetch_game_data(url)
    if game_data is None:
        print(f"跳过游戏: {game_title}")
        return

    # 添加下载链接到 game_data
    game_data['download_link'] = download_link

    content = create_post_content(game_data)

    tags_to_add = game_data.get('game_tags', [])

    # 发布文章并添加标签
    post_to_wordpress(game_data['title'], content, tags_to_add)


def main():
    # 加载 JSON 文件
    json_file = 'game_detail_new_en.json'  # 替换为你的 JSON 文件路径
    games = load_json(json_file)

    if not games:
        print("没有游戏数据可处理。")
        return

    # 设置线程池大小，根据实际情况调整
    max_workers = 5

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # 提交所有任务
        futures = [executor.submit(process_game, game) for game in games]

        # 可选：处理任务完成后的结果
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"任务执行失败: {e}")

    print("所有游戏处理完成。")


if __name__ == "__main__":
    main()
