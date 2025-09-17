import os
import re
import json
from pathlib import Path

# 脚本路径调试
SCRIPT_PATH = Path(__file__).resolve()
SCRIPT_DIR = SCRIPT_PATH.parent  # .github/scripts
REPO_ROOT = SCRIPT_DIR.parent.parent  # 仓库根目录（直接存放所有.md文件）
BLOG_DIR = REPO_ROOT  # 关键修正：博客文件在仓库根目录，而非Blog子目录
INDEX_PATH = BLOG_DIR / "index.json"  # index.json也在根目录

# 打印路径调试信息
print(f"脚本绝对路径: {SCRIPT_PATH}")
print(f"仓库根目录路径: {REPO_ROOT}")
print(f"博客文件目录路径: {BLOG_DIR}")  # 现在应与仓库根目录一致

# 日期提取正则（保持不变）
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
        # 检查博客目录（仓库根目录）是否存在
        if not BLOG_DIR.exists():
            raise FileNotFoundError(f"博客目录不存在：{BLOG_DIR}")
        if not BLOG_DIR.is_dir():
            raise NotADirectoryError(f"{BLOG_DIR} 不是目录")
        
        articles = []
        # 遍历根目录下的.md文件，排除非文件（如image/.git/.github等目录）
        for item in BLOG_DIR.iterdir():
            if item.is_file() and item.suffix == ".md" and item.name != "index.md":
                filename = item.name
                # 读取文件内容
                try:
                    with open(item, "r", encoding="utf-8") as f:
                        content = f.read()
                except UnicodeDecodeError:
                    with open(item, "r", encoding="gbk") as f:
                        content = f.read()
                
                articles.append({
                    "file": filename,
                    "title": filename[:-3],
                    "date": extract_date(content, filename)
                })
        
        # 排序并写入index.json（根目录下）
        articles.sort(key=lambda x: x["date"], reverse=True)
        with open(INDEX_PATH, "w", encoding="utf-8") as f:
            json.dump(articles, f, ensure_ascii=False, indent=2)
            
    except Exception as e:
        print(f"执行出错: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()
