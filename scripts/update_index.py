import os
import json
import frontmatter  # 解析 MD 中的元数据（如标题、日期）
from datetime import datetime

BLOG_DIR = "Blog"
INDEX_PATH = os.path.join(BLOG_DIR, "index.json")

def extract_md_info(file_path):
    """提取 MD 文件的信息"""
    with open(file_path, 'r', encoding='utf-8') as f:
        post = frontmatter.load(f)
    
    # 文件名（不含路径）
    file_name = os.path.basename(file_path)
    
    # 标题：优先用 MD 中的 title 元数据，否则用文件名（去掉 .md）
    title = post.get('title') or file_name.replace('.md', '')
    
    # 日期：优先用 MD 中的 date 元数据，否则从内容/文件名提取
    date_str = post.get('date')
    if not date_str:
        # 示例：从文件名提取（如“2025-09-15 标题.md”）
        import re
        match = re.search(r'\d{4}-\d{2}-\d{2}', file_name)
        if match:
            date_str = match.group()
        else:
            # 从内容提取（如“2025年8月27日”）
            match = re.search(r'(\d{4})年(\d{1,2})月(\d{1,2})日', post.content)
            if match:
                date_str = f"{match.group(1)}-{match.group(2).zfill(2)}-{match.group(3).zfill(2)}"
            else:
                #  fallback：文件修改时间
                mtime = os.path.getmtime(file_path)
                date_str = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d")
    
    return {
        "file": file_name,
        "title": title,
        "date": date_str
    }

def main():
    # 扫描所有 MD 文件
    md_files = [f for f in os.listdir(BLOG_DIR) if f.endswith('.md')]
    posts = []
    for file in md_files:
        if file == 'index.json':
            continue
        info = extract_md_info(os.path.join(BLOG_DIR, file))
        posts.append(info)
    
    # 按日期倒序排序（最新的在前）
    posts.sort(key=lambda x: x['date'], reverse=True)
    
    # 写入 index.json
    with open(INDEX_PATH, 'w', encoding='utf-8') as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
