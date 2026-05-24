import os
import shutil

def clean_mtfwiki_repo():
    print("🚀 [MtF.wiki 净化协议] 启动：正在执行物理级大清洗...")
    
    # 🛡️ 核心白名单：MtF.wiki 专属护城河
    whitelist = [
        'content',      # 核心 Markdown 源码库
        'static',       # 核心静态资源（如果还没被 move_static 移动的话）
        'mkdocs.yml',   # 咱们手搓的神级配置文件
        'LICENSE',      # 尊重开源协议的护身符
    ]

    deleted_count = 0
    root_items = os.listdir('.')

    for item in root_items:
        # 🔐 绝对安全锁：
        # 1. 在白名单里的直接放过
        # 2. 所有的 .py 流水线脚本必须活下来（你的雇佣兵军团）
        # 3. 所有的 .md 说明文档 (如 README-EN.md, index.md) 给予保留
        if item in whitelist or item.endswith('.py') or item.endswith('.md'):
            continue

        try:
            if os.path.isdir(item):
                shutil.rmtree(item)
                print(f"💣 摧毁无用/残留文件夹: {item}/")
            else:
                os.remove(item)
                print(f"💥 摧毁无用/残留文件: {item}")
            deleted_count += 1
        except Exception as e:
            print(f"❌ 警告：无法删除 {item}, 错误: {e}")

    print(f"🎉 净化完成！共粉碎了 {deleted_count} 个电子垃圾和历史残留构建！")
    print("👉 现在的 MtF.wiki 已经是一块极致纯净的画布，随时准备重构！")

if __name__ == '__main__':
    clean_mtfwiki_repo()