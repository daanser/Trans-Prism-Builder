import os
import re

def fix_vitepress_syntax():
    print("🚀 [VitePress 翻译官] 启动：正在清洗 Vue 组件与专属语法...")
    count = 0
    
    for root, dirs, files in os.walk('content'):
        for filename in files:
            if filename.endswith('.md'):
                filepath = os.path.join(root, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                    original_content = content
                    
                    # 🎯 1. 物理超度 Vue 脚本块 (<script setup> ... </script>)
                    content = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL)
                    
                    # 🎯 2. 物理超度自定义标签 (比如 <HomeContent> 和 </HomeContent>)
                    content = re.sub(r'</?HomeContent>', '', content)
                    
                    # 🎯 3. 核心转换：把 ::: tip 变成 !!! tip 
                    # VitePress: ::: tip 标题 \n 内容 \n :::
                    # MkDocs:    !!! tip "标题" \n    内容 (需要缩进)
                    def replace_admonition(match):
                        ad_type = match.group(1).strip()
                        title = match.group(2).strip()
                        body = match.group(3).strip()
                        
                        indented_body = "\n".join("    " + line for line in body.split("\n"))
                        title_part = f' "{title}"' if title else ' ""'
                        return f'!!! {ad_type}{title_part}\n{indented_body}\n'
                        
                    # 使用多行模式匹配 ::: 块
                    content = re.sub(r'^:::\s*([a-zA-Z0-9_-]+)(.*?)\n(.*?)^:::', replace_admonition, content, flags=re.DOTALL | re.MULTILINE)
                    
                    if content != original_content:
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(content)
                        count += 1
                except Exception as e:
                    print(f"❌ 警告：处理 {filepath} 时发生错误: {e}")
                    
    print(f"🎉 翻译完毕！共清洗了 {count} 个包含 VitePress 专属语法的 Markdown 文件！")

if __name__ == '__main__':
    fix_vitepress_syntax()