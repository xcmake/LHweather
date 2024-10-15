import re

# 数据列表
data = [
    {
        "href": "https://www.2cyshare.com/post/3764.html",
        "title": "消逝的光芒2 人与仁之战 Dying Light 2 v1.18.0c单机版+v1.18.0c联机版|集成全DLC|国语配音|官方中文，有升级补丁",
        "download_link": "https://pan.quark.cn/s/7c6429c69de8"
    },
    {
        "href": "https://www.2cyshare.com/post/4054.html",
        "title": "指环王：重返莫瑞亚 The Lord of the Rings: Return to Moria v1.3.2.157411版|官方中文",
        "download_link": "https://pan.quark.cn/s/d35ecbc7b413"
    },
    {
        "href": "https://www.2cyshare.com/post/4141.html",
        "title": "寂静之歌 v0.7.0（Songs Of Silence）免安装中文版",
        "download_link": "https://pan.quark.cn/s/eac294ff3789"
    },
    {
        "href": "https://www.2cyshare.com/post/676.html",
        "title": "双人成行（It Takes Two）",
        "download_link": "https://pan.quark.cn/s/39698053daed"
    },
    {
        "href": "https://www.2cyshare.com/post/4029.html",
        "title": "罗宾汉 - 舍伍德建造者 Robin Hood-Sherwood Builders v04.08.19.01版|官方中文",
        "download_link": "https://pan.quark.cn/s/e30be1e7a20b"
    },
    {
        "href": "https://www.2cyshare.com/post/4034.html",
        "title": "幻日夜羽 -蜃景努玛梓- yohanuma NUMAZU in the MIRAGE v1.0.14版|官方中文",
        "download_link": "https://pan.quark.cn/s/faae521adca7"
    },
    {
        "href": "https://www.2cyshare.com/post/4043.html",
        "title": "史莱姆牧场2 v0.5.2（Slime Rancher 2）免安装中文版",
        "download_link": "https://pan.quark.cn/s/8ae541a45379"
    },
    {
        "href": "https://www.2cyshare.com/post/4032.html",
        "title": "【PC/安卓/汉化】《樱之刻 – 于樱花之森下漫步》美少女游戏",
        "download_link": "https://pan.quark.cn/s/b3b7719ac59f"
    }
]

def extract_english_title(title):
    # 提取所有英文内容，并排除单独的 'v' 和 'PC'
    matches = re.findall(r'\b(?!v\b)(?!PC\b)[A-Za-z\s:]+\b', title)

    # 去掉每个匹配项的前后空格，过滤并拼接成完整字符串
    filtered_matches = [word.strip() for word in matches if word.strip().lower() not in ['v', 'pc']]

    # 返回拼接后的英文标题字符串，并移除首尾空格
    return " ".join(filtered_matches).strip()


# 提取所有英文标题
english_titles = []
for item in data:
    eng_title = extract_english_title(item["title"])
    if eng_title:  # 确保提取到有效内容
        english_titles.append(eng_title)

# 打印提取的英文标题
print(english_titles)