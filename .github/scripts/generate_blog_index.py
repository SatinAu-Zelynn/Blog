import os
import re
import json
from datetime import datetime

# 配置路径（确保与实际仓库结构一致）
BLOG_DIR = "Blog"
INDEX_PATH = os.path.join(BLOG_DIR, "index.json")

# 扩展日期提取正则（支持更多格式）
DATE_PATTERNS = [
    re.compile(r'(\d{4})年(\d{1,2})月(\d{1,2})日'),  # 2025年8月27日
    re.compile(r'(\d{4})年(\d{1,2})月'),            # 2025年6月
    re.compile(r'(\d{4})-(\d{1,2})-(\d{1,2})'),     # 2025-08-27
    re.compile(r'(\d{2})年(\d{1,2})月(\d{1,2})日')  # 44年6月6日（诺曼底登陆）
]

def extract_date(content: str, filename: str) -> str:
    """增强版日期提取逻辑"""
    # 1. 从文件内容提取日期
    for pattern in DATE_PATTERNS:
        match = pattern.search(content)
        if match:
            groups = match.groups()
            # 处理年份（如"44年"转换为1944年）
            year = groups[0]
            if len(year) == 2:
                year = f"19{year}"  # 适用于20世纪事件
            month = groups[1].zfill(2)
            day = groups[2].zfill(2) if len(groups) > 2 else "01"  # 缺少年份补1日
            return f"{year}-{month}-{day}"
    
    # 2. 从文件名提取日期（如"6月12日世界无童工日"）
    filename_match = re.search(r'(\d{1,2})月(\d{1,2})日', filename)
    if filename_match:
        month, day = filename_match.groups()
        # 假设文件名中的日期为当前年份（可根据实际需求调整）
        return f"2025-{month.zfill(2)}-{day.zfill(2)}"
    
    # 3. 特殊文件手动映射（补充更多实际案例）
    special_cases = {
        "For ALL women and girls.md": "2025-03-08",
        "72年前的今天.md": "2025-07-27",
        "80年前的这个月.md": "2025-06-25",
        "今天是诺曼底登陆81周年.md": "2025-06-06"
    }
    return special_cases.get(filename, "2025-01-01")

def main():
    try:
        articles = []
        # 遍历所有Markdown文件
        for filename in os.listdir(BLOG_DIR):
            if not filename.endswith(".md") or filename == "index.md":
                continue
            
            file_path = os.path.join(BLOG_DIR, filename)
            # 跳过目录（只处理文件）
            if not os.path.isfile(file_path):
                continue
            
            # 读取文件内容（兼容不同编码）
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
            except UnicodeDecodeError:
                # 尝试其他编码
                with open(file_path, "r", encoding="gbk") as f:
                    content = f.read()
            
            # 提取信息
            articles.append({
                "file": filename,
                "title": filename[:-3],
                "date": extract_date(content, filename)
            })
        
        # 按日期降序排序
        articles.sort(key=lambda x: x["date"], reverse=True)
        
        # 写入index.json
        with open(INDEX_PATH, "w", encoding="utf-8") as f:
            json.dump(articles, f, ensure_ascii=False, indent=2)
            
    except Exception as e:
        print(f"执行出错: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()
