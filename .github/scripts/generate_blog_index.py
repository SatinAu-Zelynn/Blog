import os
import re
import json
from datetime import datetime

# 配置路径
BLOG_DIR = "Blog"
INDEX_PATH = os.path.join(BLOG_DIR, "index.json")

# 日期提取正则（支持"2025年8月27日"格式）
DATE_PATTERN = re.compile(r'(\d{4})年(\d{1,2})月(\d{1,2})日')

def extract_date(content: str, filename: str) -> str:
    """从文件内容或文件名提取日期"""
    # 优先从内容提取
    match = DATE_PATTERN.search(content)
    if match:
        year, month, day = match.groups()
        return f"{year}-{month.zfill(2)}-{day.zfill(2)}"
    
    # 特殊文件处理（根据实际需求补充）
    special_cases = {
        "For ALL women and girls.md": "2025-03-08",  # 国际妇女节
        "72年前的今天.md": "2025-07-27"  # 朝鲜停战协定纪念日
    }
    return special_cases.get(filename, "2025-01-01")  # 默认日期

def main():
    articles = []
    # 遍历所有Markdown文件
    for filename in os.listdir(BLOG_DIR):
        if not filename.endswith(".md") or filename == "index.md":
            continue
        
        # 读取文件内容
        with open(os.path.join(BLOG_DIR, filename), "r", encoding="utf-8") as f:
            content = f.read()
        
        # 提取信息
        articles.append({
            "file": filename,
            "title": filename[:-3],  # 移除.md后缀作为标题
            "date": extract_date(content, filename)
        })
    
    # 按日期降序排序（最新的在前）
    articles.sort(key=lambda x: x["date"], reverse=True)
    
    # 写入index.json
    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
