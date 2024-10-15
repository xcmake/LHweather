import requests
from bs4 import BeautifulSoup
import time
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

# 请求头配置
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
}

# 基础 URL
base_url = 'https://www.2cyshare.com/category-5'

# 存储所有页面结果的列表
results = []

# 获取游戏列表
def fetch_game_list(page_num):
    url = f"{base_url}_{page_num}.html" if page_num > 1 else f"{base_url}.html"
    print(f"正在处理第 {page_num} 页: {url}")
    game_list = []

    try:
        # 获取网页内容
        response = requests.get(url, headers=header)
        response.raise_for_status()  # 如果请求失败，抛出HTTPError
        soup = BeautifulSoup(response.text, 'lxml')

        # 查找所有符合条件的 h2 标签
        h2_tags = soup.find_all('h2', class_='item-title')

        # 提取每个 h2 标签下 a 标签的 href 和 title 属性
        for h2_tag in h2_tags:
            a_tag = h2_tag.find('a')
            if a_tag:
                href = a_tag.get('href')
                title = a_tag.get('title')
                game_list.append({'href': href, 'title': title})
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")

    return game_list


# 获取下载链接
def fetch_download_link(game):
    try:
        detail_url = game['href']
        # 发送请求访问详情页
        response = requests.get(detail_url, headers=header)
        response.raise_for_status()

        # 解析页面内容
        soup = BeautifulSoup(response.text, 'lxml')

        # 查找具有 's-links' 类的 <span> 标签
        span_tag = soup.find('span', class_='s-links')

        if span_tag:
            # 在 <span> 标签内查找 <a> 标签
            a_tag = span_tag.find('a', href=True)

            if a_tag:
                # 获取 href 属性值并保存
                game['download_link'] = a_tag['href']
            else:
                game['download_link'] = None
                print(f"在 {detail_url} 的 <span> 标签内未找到 <a> 标签。")
        else:
            game['download_link'] = None
            print(f"未找到具有 's-links' 类的 <span> 标签：{detail_url}")
    except requests.exceptions.RequestException as e:
        print(f"无法获取详情页: {game['href']}. 错误信息: {e}")
        game['download_link'] = None

    return game


# 使用多线程获取所有游戏列表
def main():
    start_time = time.time()

    # 使用 ThreadPoolExecutor 来并发处理游戏列表页
    with ThreadPoolExecutor(max_workers=10) as executor:
        # 提交任务获取 120 页游戏列表
        futures = [executor.submit(fetch_game_list, page_num) for page_num in range(1, 121)]

        # 等待所有任务完成
        for future in as_completed(futures):
            results.extend(future.result())

    # 使用多线程获取所有游戏的下载链接
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(fetch_download_link, game) for game in results]

        # 收集所有包含下载链接的游戏
        final_results = [future.result() for future in as_completed(futures)]

    # 过滤掉没有下载链接的游戏
    final_results_with_download = [game for game in final_results if game.get('download_link')]

    # 保存为 JSON 文件
    with open('game_detail_old.json', 'w', encoding='utf-8') as f:
        json.dump(final_results_with_download, f, ensure_ascii=False, indent=4)

    print(f"任务完成，共耗时: {time.time() - start_time:.2f} 秒")


if __name__ == "__main__":
    main()
