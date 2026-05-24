import os
import re

def fix_hugo_shortcodes():
    print("🚀 [语法转换引擎] 启动：正在将 Hugo 专属语法翻译为 MkDocs 语法...")
    content_dir = 'content'
    
    if not os.path.exists(content_dir):
        print("❌ 找不到 content 文件夹！")
        return
        
    # 🗺️ 核心雷达表 (不再带前缀斜杠！)
    target_map = {}
    print("📡 正在扫描全盘文件建立路由雷达...")
    for root, dirs, files in os.walk(content_dir):
        for file in files:
            if file.endswith('.md'):
                # 算出相对于 content_dir 的路径，例如 'srs/index.md'
                rel_path = os.path.relpath(os.path.join(root, file), content_dir)
                posix_path = rel_path.replace(os.sep, '/')
                
                name_without_ext = os.path.splitext(file)[0].lower()
                folder_name = os.path.basename(root).lower()
                
                if name_without_ext in ['index', '_index', 'readme']:
                    target_map[folder_name] = posix_path
                else:
                    target_map[name_without_ext] = posix_path
                    target_map[f"{folder_name}/{name_without_ext}"] = posix_path

    count = 0
    print("🧹 开始执行深度替换...")
    for root, dirs, files in os.walk(content_dir):
        for filename in files:
            if filename.endswith('.md'):
                filepath = os.path.join(root, filename)
                # 获取当前文件所在的目录路径
                current_dir = os.path.dirname(filepath)
                
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                    original_content = content
                    
                    # 🎯 1. 抢救 Notice (警告框)
                    def replace_notice(match):
                        type_ = match.group(1)
                        title = match.group(2)
                        inner_text = match.group(3)
                        indented = "\n".join("    " + line for line in inner_text.split("\n"))
                        return f"!!! {type_} \"{title}\"\n{indented}"
                    
                    content = re.sub(
                        r'\{\{<\s*notice\s+([a-zA-Z0-9_-]+)\s+"([^"]*)"\s*>\}\}(.*?)\{\{<\s*/notice\s*>\}\}', 
                        replace_notice, content, flags=re.DOTALL
                    )
                    
                    # 🎯 2. 抢救图片路径
                    def fix_image_path(path: str) -> str:
                        path = path.strip().lstrip('/')
                        if path.startswith(('http://', 'https://', '#', 'data:')):
                            return path
                        if path.startswith('static/'):
                            return '/' + path
                        return '/static/' + path

                    def replace_md_image(match):
                        alt_text = match.group(1)
                        src = match.group(2)
                        return f'![{alt_text}]({fix_image_path(src)})'

                    content = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', replace_md_image, content)

                    def replace_hiddenphoto(match):
                        src = match.group(1)
                        caption = match.group(2).strip() if match.group(2) else ''
                        path = fix_image_path(src)
                        if caption:
                            return f'![{caption}]({path})'
                        else:
                            return f'![]({path})'

                    content = re.sub(r'\{\{<\s*hiddenphoto\s+"([^"]+)"\s*(?:"([^"]*)")?\s*>\}\}', replace_hiddenphoto, content)

                    def replace_html_img(match):
                        before_src = match.group(1)
                        src = match.group(2)
                        after_src = match.group(3)
                        return f'{before_src}{fix_image_path(src)}{after_src}'

                    content = re.sub(r'(<img\s+[^>]*?src=")([^"]+)("[\s\S]*?>)', replace_html_img, content)
                    
                    # 🎯 3. 抢救 Wiki 快捷链接
                    def replace_wiki(match):
                        args = match.group(1).strip().split()
                        if not args:
                            return match.group(0)
                        keyword = args[0]
                        lang = args[1] if len(args) > 1 else 'zh'
                        return f'[{keyword}](https://{lang}.wikipedia.org/wiki/{keyword})'
                        
                    content = re.sub(r'\{\{<\s*wiki\s+(.*?)\s*>\}\}', replace_wiki, content)
                    
                    # 🎯 4. 抢救 ref 和 page 跨页面引用 (GPS 相对路径完美版)
                    def replace_ref_page(match):
                        raw_target = match.group(1)
                        parts = raw_target.split('#', 1)
                        name = parts[0].strip('/').lower()
                        anchor = f"#{parts[1]}" if len(parts) > 1 else ""
                        
                        mapped_target = target_map.get(name)
                        if not mapped_target:
                            mapped_target = f"{name}/index.md"
                            
                        # 📍 核心魔法：算出从当前文件夹到目标文件的相对路径 (类似 ../../srs/index.md)
                        target_full_path = os.path.join(content_dir, os.path.normpath(mapped_target))
                        rel_link = os.path.relpath(target_full_path, current_dir)
                        rel_link = rel_link.replace(os.sep, '/')
                        
                        return f'[{parts[0]}]({rel_link}{anchor})'

                    content = re.sub(r'\{\{<\s*(?:ref|page)\s+"?([^"\s>]+)"?\s*>\}\}', replace_ref_page, content)

                    # 🎯 5. 抢救 abbr (缩写短代码)
                    content = re.sub(r'\{\{<\s*abbr\s+(.*?)\s*>\}\}', r'\1', content)
                    
                    if content != original_content:
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(content)
                        count += 1
                except Exception as e:
                    print(f"❌ 警告：处理 {filepath} 时发生错误: {e}")
                    
    print(f"🎉 语法清洗完毕！共拯救了 {count} 个惨遭乱码荼毒的 Markdown 文件！")

if __name__ == '__main__':
    fix_hugo_shortcodes()