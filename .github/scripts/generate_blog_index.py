import os
import json
import re
from datetime import datetime

# 定位仓库根目录（脚本位于 .github/scripts，根目录是其祖父目录）
SCRIPT_PATH = os.path.abspath(__file__)  # 脚本绝对路径
SCRIPT_DIR = os.path.dirname(SCRIPT_PATH)  # .github/scripts
GITHUB_DIR = os.path.dirname(SCRIPT_DIR)  # .github
REPO_ROOT = os.path.dirname(GITHUB_DIR)  # 仓库根目录（直接包含所有.md文件）

# 根目录即为存放.md文件的目录，index.json也在根目录
BLOG_DIR = REPO_ROOT  # 直接使用根目录作为博客文件目录
INDEX_PATH = os.path.join(REPO_ROOT, "index.json")  # 索引文件在根目录

# 日期提取正则（保持不变）
DATE_PATTERNS = [
    re.compile(r'(\d{4})年(\d{1,2})月(\d{1,2})日'),
    re.compile(r'(\d{4})-(\d{2})-(\d{2})'),
    re.compile(r'(\d{1,2})月(\d{1,2})日'),
]

def extract_date(content: str) -> str:
    current_year = datetime.now().year
    for pattern in DATE_PATTERNS:
        match = pattern.search(content)
        if match:
            groups = match.groups()
            if len(groups) == 3:
                year, month, day = groups
            else:
                year, month, day = current_year, groups[0], groups[1]
            return f"{year}-{int(month):02d}-{int(day):02d}"
    return datetime.now().strftime("%Y-%m-%d")

def generate_index():
    # 检查根目录是否存在（理论上必然存在，仅作提示）
    if not os.path.isdir(BLOG_DIR):
        raise FileNotFoundError(f"未找到仓库根目录，请检查路径：{BLOG_DIR}")
    
    posts = []
    # 遍历根目录下的所有文件，仅处理.md文件（排除子目录如image、.github等）
    for filename in os.listdir(BLOG_DIR):
        file_path = os.path.join(BLOG_DIR, filename)
        # 跳过目录，只处理以.md结尾的文件
        if os.path.isfile(file_path) and filename.endswith(".md"):
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            title = filename[:-3]  # 去掉.md后缀作为标题
            date = extract_date(content)
            posts.append({
                "file": filename,
                "title": title,
                "date": date
            })
    
    # 按日期倒序排序
    posts.sort(key=lambda x: x["date"], reverse=True)
    # 写入根目录下的index.json
    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)
    print(f"已生成索引，共包含 {len(posts)} 篇文章")

if __name__ == "__main__":
    generate_index()
