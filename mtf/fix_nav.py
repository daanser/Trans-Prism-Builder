import os
import re

def fix_navigation():
    print("🚀 [终极导航重构] 启动：正在精准提炼子目录中文名...")
    base_dir = 'content'
    
    # 顶级目录专属国旗标签
    lang_map = {
        'zh-cn': '🇨🇳 简体中文 (zh-cn)',
        'zh-hant': '🇭🇰 繁體中文 (zh-hant)',
        'ja': '🇯🇵 日本語 (ja)',
        'en': '🇬🇧 English (en)',
        'es': '🇪🇸 Español (es)',
        'ko': '🇰🇷 한국어 (ko)',
        'fr': '🇫🇷 Français (fr)'
    }

    if not os.path.exists(base_dir):
        print("❌ 找不到 content 文件夹！")
        return

    # 1. 暴力清除所有旧的 .pages，准备干净的画布
    for root, dirs, files in os.walk(base_dir):
        if '.pages' in files:
            os.remove(os.path.join(root, '.pages'))

    # 2. 深入每个文件夹，重新生成精准的 .pages
    count = 0
    for root, dirs, files in os.walk(base_dir):
        rel_path = os.path.relpath(root, base_dir)
        folder_name = os.path.basename(root)
        
        if rel_path == '.':
            continue
            
        title = None
        
        # 🎯 场景 A: 顶级语言目录，直接上国旗
        if rel_path in lang_map:
            title = lang_map[rel_path]
        
        # 🎯 场景 B: 所有的子目录（比如 docs, medicine, psyco）
        else:
            # 寻找子目录的入口文件
            index_files = [f for f in files if f.lower() in ['index.md', '_index.md', 'readme.md']]
            if index_files:
                filepath = os.path.join(root, index_files[0])
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                        # 魔法1：尝试抓取 YAML/TOML 配置里的 title: "xxx" 或 title="xxx"
                        match_meta = re.search(r'^title\s*[:=]\s*[\'"]?([^\n\'"]+)[\'"]?', content, re.MULTILINE | re.IGNORECASE)
                        if match_meta:
                            title = match_meta.group(1).strip()
                        else:
                            # 魔法2：尝试抓取 Markdown 的一级标题 # xxx
                            match_h1 = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
                            if match_h1:
                                title = match_h1.group(1).strip()
                                
                        # 🚫 防复读机拦截网：如果抓出来的又是全局标题，强行修正！
                        if title:
                            title_lower = title.lower()
                            if "mtf.wiki" in title_lower or "稳态光盒" in title:
                                if folder_name.lower() == 'docs':
                                    title = '文档库' # 给 docs 强行赋一个好听的中文名
                                elif folder_name.lower() == 'about':
                                    title = '关于我们'
                                else:
                                    title = None # 放弃，让 MkDocs 自己处理
                except Exception:
                    pass
                    
        # 3. 只有提取到了完美合法的中文名，才生成配置文件
        if title:
            pages_path = os.path.join(root, '.pages')
            with open(pages_path, 'w', encoding='utf-8') as f:
                # 防止标题里自带单引号搞崩 YAML
                safe_title = title.replace("'", "''")
                f.write(f"title: '{safe_title}'\n")
            count += 1
            print(f"✅ 生成侧边栏节点: [{folder_name}] -> {title}")
            
    print(f"🎉 侧边栏完美重构！共精准生成了 {count} 个导航配置文件！")

if __name__ == '__main__':
    fix_navigation()