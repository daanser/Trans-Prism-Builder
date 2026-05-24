import os
import shutil

def clean_rle_repo():
    print("🚀 [RLE.wiki 破壁机] 启动：正在粉碎 Node.js 框架，提取核心资产...")
    
    # 🎯 核心魔法：把 VitePress 的 docs 变成 MkDocs 的 content
    if os.path.exists('docs'):
        if os.path.exists('content'):
            shutil.rmtree('content') # 防冲突清理
        os.rename('docs', 'content')
        print("✅ 移花接木：已将 docs 目录重命名为 content，旧流水线对接成功！")

    # 🛡️ 核心白名单
    whitelist = [
        'content',      # 刚改名过来的核心 Markdown 源码库
        'mkdocs.yml',   # 咱们手搓的神级配置文件
        'LICENSE',      # 护身符
    ]

    deleted_count = 0
    for item in os.listdir('.'):
        # 放过白名单、所有的流水线脚本和说明文档
        if item in whitelist or item.endswith('.py') or item.endswith('.md'):
            continue

        try:
            if os.path.isdir(item):
                shutil.rmtree(item)
            else:
                os.remove(item)
            deleted_count += 1
        except Exception:
            pass

    print(f"🎉 净化完成！共粉碎了 {deleted_count} 个前端依赖垃圾！")

if __name__ == '__main__':
    clean_rle_repo()