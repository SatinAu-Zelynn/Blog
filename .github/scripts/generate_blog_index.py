import os
import json
import re
from datetime import datetime

# 配置路径
BLOG_DIR = "Blog"
INDEX_PATH = os.path.join(BLOG_DIR, "index.json")

# 日期提取正则（支持多种格式）
DATE_PATTERNS = [
    re.compile(r'(\d{4})年(\d{1,2})月(\d{1,2})日'),  # 匹配"2025年8月27日"
    re.compile(r'(\d{4})-(\d{2})-(\d{2})'),         # 匹配"2025-08-27"
    re.compile(r'(\d{1,2})月(\d{1,2})日'),          # 匹配"8月27日"（默认当年）
]

def extract_date(content: str) -> str:
    """从Markdown内容中提取日期，返回YYYY-MM-DD格式"""
    current_year = datetime.now().year  # 处理无年份的日期时使用当前年份
    
    for pattern in DATE_PATTERNS:
        match = pattern.search(content)
        if match:
            groups = match.groups()
            if len(groups) == 3:  # 有年份的格式（2025年8月27日或2025-08-27）
                year, month, day = groups
            else:  # 无年份的格式（8月27日）
                year, month, day = current_year, groups[0], groups[1]
            
            # 补全前导零并格式化
            return f"{year}-{int(month):02d}-{int(day):02d}"
    
    # 如果未提取到日期，使用文件修改时间作为 fallback
    return datetime.now().strftime("%Y-%m-%d")

def generate_index():
    posts = []
    
    # 遍历Blog目录下的所有md文件
    for filename in os.listdir(BLOG_DIR):
        if not filename.endswith(".md"):
            continue  # 只处理Markdown文件
        
        file_path = os.path.join(BLOG_DIR, filename)
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # 提取信息
        title = filename[:-3]  # 移除.md后缀作为标题
        date = extract_date(content)
        
        posts.append({
            "file": filename,
            "title": title,
            "date": date
        })
    
    # 按日期降序排序（最新的在前）
    posts.sort(key=lambda x: x["date"], reverse=True)
    
    # 写入index.json
    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)
    
    print(f"已生成索引，共包含 {len(posts)} 篇文章")

if __name__ == "__main__":
    generate_index()
