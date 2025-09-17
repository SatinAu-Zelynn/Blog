import os
import json
import re
from datetime import datetime

# 定位根目录（脚本位于 .github/scripts，根目录是其祖父目录）
SCRIPT_PATH = os.path.abspath(__file__)  # 脚本绝对路径
SCRIPT_DIR = os.path.dirname(SCRIPT_PATH)  # .github/scripts
GITHUB_DIR = os.path.dirname(SCRIPT_DIR)  # .github
REPO_ROOT = os.path.dirname(GITHUB_DIR)  # 项目根目录（main分支根目录）

# 根目录下的Blog文件夹路径
BLOG_DIR = os.path.join(REPO_ROOT, "Blog")
INDEX_PATH = os.path.join(BLOG_DIR, "index.json")

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
    # 检查Blog目录是否存在（根目录下）
    if not os.path.isdir(BLOG_DIR):
        raise FileNotFoundError(f"根目录下未找到Blog文件夹，请确认路径：{BLOG_DIR}")
    
    posts = []
    for filename in os.listdir(BLOG_DIR):
        if not filename.endswith(".md"):
            continue
        file_path = os.path.join(BLOG_DIR, filename)
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        title = filename[:-3]
        date = extract_date(content)
        posts.append({
            "file": filename,
            "title": title,
            "date": date
        })
    
    posts.sort(key=lambda x: x["date"], reverse=True)
    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)
    print(f"已生成索引，共包含 {len(posts)} 篇文章")

if __name__ == "__main__":
    generate_index()
