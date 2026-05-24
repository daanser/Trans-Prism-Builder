import os
import shutil
import time

def prepare_static():
    print("🚀 [自动化构建链] 启动：正在整合 static 与 favicon 资源...")
    
    # 确保 content 文件夹存在
    if not os.path.exists('content'):
        print("❌ 致命错误：找不到 content 文件夹，请确认在项目根目录运行！")
        return

    # --- 1. 处理 static 文件夹 ---
    source_static = 'static'
    dest_static = os.path.join('content', 'static')
    
    try:
        # 如果根目录下有 static，需要移动
        if os.path.exists(source_static):
            # 如果 content 里面已经有旧的，先清理防止冲突
            if os.path.exists(dest_static):
                print("🧹 发现 content/static 中已有旧数据，正在清理...")
                shutil.rmtree(dest_static)
            
            shutil.move(source_static, 'content/')
            print("✅ 转移成功：static 文件夹已完美并入 content/static！")
            
            # 🎯 核心护航：强制系统休眠 0.1 秒，等待文件系统 I/O 状态彻底刷新
            time.sleep(0.1)
            print("⏳ I/O 状态刷新完毕，准备处理图标...")
            
        else:
            if not os.path.exists(dest_static):
                print("⚠️ 警告：到处都找不到 static 文件夹，请确认源码！")
            else:
                print("✅ 检查通过：static 已经在 content 里面了。")

        # --- 2. 处理 favicon.png ---
        # 精准定位：它在 content 根目录，要放进 content/static
        favicon_src = os.path.join('content', 'favicon.png')
        favicon_dest = os.path.join('content', 'static', 'favicon.png')
        
        if os.path.exists(favicon_src):
            # 确保目标文件夹存在（防弹设计）
            os.makedirs(dest_static, exist_ok=True)
            
            # 安全复制
            shutil.copy(favicon_src, favicon_dest)
            print("✅ 图标就位：content/favicon.png 已成功复制到 static 资源库！")
        elif os.path.exists(favicon_dest):
            print("✅ 图标就位：favicon.png 已经在 static 里了，无需重复复制！")
        else:
            print(f"⚠️ 警告：找不到 {favicon_src}！")

    except Exception as e:
        print(f"❌ 处理静态资源时发生底层错误: {e}")

if __name__ == '__main__':
    prepare_static()