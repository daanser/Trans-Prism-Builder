import os
import shutil

def clean_ftmwiki_repo():
    print("🚀 [FtM.wiki 净化协议] 启动：正在物理粉碎无用框架的遗留文件...")
    
    # 🛡️ 核心白名单：只有这些东西配活下来
    whitelist = [
        'content',      # 核心 Markdown 源码
        'static',       # 核心静态资源（图片等）
        'mkdocs.yml',   # 咱们自己写的 MkDocs 配置文件
        'LICENSE',      # 尊重开源协议的护身符
        'README.md'     # 原始说明文档
    ]

    deleted_count = 0
    root_items = os.listdir('.')

    for item in root_items:
        # 绝对安全锁：跳过白名单，且跳过咱们自己写的所有 .py 流水线脚本
        if item in whitelist or item.endswith('.py'):
            continue

        try:
            if os.path.isdir(item):
                shutil.rmtree(item)
                print(f"💣 摧毁无用文件夹: {item}/")
            else:
                os.remove(item)
                print(f"💥 摧毁无用文件: {item}")
            deleted_count += 1
        except Exception as e:
            print(f"❌ 警告：无法删除 {item}, 错误: {e}")

    print(f"🎉 净化完成！共粉碎了 {deleted_count} 个电子垃圾！")
    print("👉 现在的项目结构已经极度纯净，随时准备接入咱们的自动化流水线！")

if __name__ == '__main__':
    clean_ftmwiki_repo()