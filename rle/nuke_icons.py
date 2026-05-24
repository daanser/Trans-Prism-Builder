import os
import re

def nuke_vitepress_icons():
    print("🚀 [排雷针] 启动：正在全盘清洗会导致 MkDocs 猝死的 VitePress 专属图标配置...")
    count = 0
    for root, dirs, files in os.walk('content'):
        for filename in files:
            if filename.endswith('.md'):
                filepath = os.path.join(root, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                    original_content = content
                    
                    # 🎯 物理抹除 YAML 头里的 icon: xxx
                    # 匹配行首的 icon: 后面跟着任意字符，直接替换为空
                    content = re.sub(r'^icon:\s*.*$', '', content, flags=re.MULTILINE)
                    
                    if content != original_content:
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(content)
                        count += 1
                except Exception as e:
                    print(f"❌ 处理 {filepath} 失败: {e}")
                    
    print(f"🎉 排雷完毕！共成功拆除了 {count} 颗会导致 SVG 找不到的炸弹！")

if __name__ == '__main__':
    nuke_vitepress_icons()