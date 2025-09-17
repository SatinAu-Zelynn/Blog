import os
import re
import json
from pathlib import Path  # 使用pathlib更可靠地处理路径

# 基于脚本所在位置计算Blog目录路径（推荐）
# 脚本路径：.github/scripts/generate_blog_index.py
# 因此仓库根目录为脚本目录的上两级（.. 表示上一级）
SCRIPT_DIR = Path(__file__).parent  # 脚本所在目录（.github/scripts）
REPO_ROOT = SCRIPT_DIR.parent.parent  # 仓库根目录
BLOG_DIR = REPO_ROOT / "Blog"  # 拼接Blog目录路径（绝对路径，更可靠）
INDEX_PATH = BLOG_DIR / "index.json"

# 扩展日期提取正则（保持不变）
DATE_PATTERNS = [
    re.compile(r'(\d{4})年(\d{1,2})月(\d{1,2})日'),
    re.compile(r'(\d{4})年(\d{1,2})月'),
    re.compile(r'(\d{4})-(\d{1,2})-(\d{1,2})'),
    re.compile(r'(\d{2})年(\d{1,2})月(\d{1,2})日')
]

def extract_date(content: str, filename: str) -> str:
    # 保持原逻辑不变
    for pattern in DATE_PATTERNS:
        match = pattern.search(content)
        if match:
            groups = match.groups()
            year = groups[0]
            if len(year) == 2:
                year = f"19{year}"
            month = groups[1].zfill(2)
            day = groups[2].zfill(2) if len(groups) > 2 else "01"
            return f"{year}-{month}-{day}"
    
    filename_match = re.search(r'(\d{1,2})月(\d{1,2})日', filename)
    if filename_match:
        month, day = filename_match.groups()
        return f"2025-{month.zfill(2)}-{day.zfill(2)}"
    
    special_cases = {
        "For ALL women and girls.md": "2025-03-08",
        "72年前的今天.md": "2025-07-27",
        "80年前的这个月.md": "2025-06-25",
        "今天是诺曼底登陆81周年.md": "2025-06-06"
    }
    return special_cases.get(filename, "2025-01-01")

def main():
    try:
        # 检查Blog目录是否存在
        if not BLOG_DIR.exists():
            raise FileNotFoundError(f"Blog目录不存在，请确认路径：{BLOG_DIR}")
        if not BLOG_DIR.is_dir():
            raise NotADirectoryError(f"{BLOG_DIR} 不是一个目录")
        
        articles = []
        # 遍历Markdown文件（使用pathlib的glob更可靠）
        for md_file in BLOG_DIR.glob("*.md"):
            filename = md_file.name
            if filename == "index.md":
                continue  # 跳过index.md
            
            # 读取文件内容
            try:
                with open(md_file, "r", encoding="utf-8") as f:
                    content = f.read()
            except UnicodeDecodeError:
                with open(md_file, "r", encoding="gbk") as f:
                    content = f.read()
            
            articles.append({
                "file": filename,
                "title": filename[:-3],
                "date": extract_date(content, filename)
            })
        
        # 排序并写入index.json
        articles.sort(key=lambda x: x["date"], reverse=True)
        with open(INDEX_PATH, "w", encoding="utf-8") as f:
            json.dump(articles, f, ensure_ascii=False, indent=2)
            
    except Exception as e:
        print(f"执行出错: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()
