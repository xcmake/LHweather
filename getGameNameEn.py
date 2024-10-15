import re
import json

# 数据列表
# 读取本地 JSON 文件
input_file = "game_detail_old.json"
with open(input_file, "r", encoding="utf-8") as file:
    data = json.load(file)

def extract_english_title(title):
    # 提取所有英文内容，并排除单独的 'v' 和 'PC'
    matches = re.findall(r'\b(?!v\b)(?!PC\b)[A-Za-z\s:]+\b', title)
    # 去掉每个匹配项的前后空格，过滤并拼接成完整字符串
    filtered_matches = [word.strip() for word in matches if word.strip().lower() not in ['v', 'pc']]
    # 返回拼接后的英文标题字符串，并移除首尾空格
    return " ".join(filtered_matches).strip()


# 分类数据列表
success_data = []
failed_data = []

# 提取并分类
for item in data:
    eng_title = extract_english_title(item["title"])
    if eng_title:  # 如果提取到英文标题
        item["title"] = eng_title
        success_data.append(item)
    else:  # 如果没有提取到英文标题
        failed_data.append(item)


# 保存到新的JSON文件
with open("game_detail_new_en.json", "w", encoding="utf-8") as file:
    json.dump(success_data, file, ensure_ascii=False, indent=4)

# 保存没有获取到英文标题的数据到failed_titles.json
with open("game_detail_new_zh.json", "w", encoding="utf-8") as file:
    json.dump(failed_data, file, ensure_ascii=False, indent=4)


# 打印保存成功信息
print("获取成功")
