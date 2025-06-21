#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智慧餐饮管理系统 - 最终启动器
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox, ttk

# 添加项目路径
current_dir = os.path.dirname(os.path.abspath(__file__))
modern_system_dir = os.path.join(current_dir, 'modern_system')
sys.path.insert(0, current_dir)
sys.path.insert(0, modern_system_dir)

def create_splash_screen():
    """创建启动画面"""
    splash = tk.Tk()
    splash.title("智慧餐饮管理系统")
    splash.geometry("500x350")
    splash.configure(bg="#FF6B35")
    splash.resizable(False, False)
    splash.overrideredirect(True)  # 无边框窗口
    
    # 居中显示
    splash.eval('tk::PlaceWindow . center')
    
    # 主框架
    main_frame = tk.Frame(splash, bg="#FF6B35")
    main_frame.pack(fill="both", expand=True)
    
    # 顶部空间
    tk.Frame(main_frame, bg="#FF6B35", height=40).pack()
    
    # 系统图标
    icon_label = tk.Label(main_frame, text="🍽️", font=('Segoe UI Emoji', 64), 
                         bg="#FF6B35", fg="white")
    icon_label.pack(pady=(20, 10))
    
    # 系统标题
    title_label = tk.Label(main_frame, text="智慧餐饮管理系统", 
                          font=('Microsoft YaHei UI', 24, 'bold'),
                          bg="#FF6B35", fg="white")
    title_label.pack(pady=(0, 5))
    
    # 副标题
    subtitle_label = tk.Label(main_frame, text="现代化餐饮管理解决方案", 
                             font=('Microsoft YaHei UI', 14),
                             bg="#FF6B35", fg="white")
    subtitle_label.pack(pady=(0, 20))
    
    # 版本信息
    version_label = tk.Label(main_frame, text="Version 2.0 - 现代化版本", 
                            font=('Microsoft YaHei UI', 11),
                            bg="#FF6B35", fg="white")
    version_label.pack(pady=(0, 20))
    
    # 进度条框架
    progress_frame = tk.Frame(main_frame, bg="#FF6B35")
    progress_frame.pack(pady=(0, 10))
      # 进度条
    progress = ttk.Progressbar(progress_frame, mode='indeterminate', length=300, 
                              style='TProgressbar')
    progress.pack()
    progress.start(10)
    
    # 状态标签
    status_label = tk.Label(main_frame, text="正在初始化系统组件...", 
                           font=('Microsoft YaHei UI', 11),
                           bg="#FF6B35", fg="white")
    status_label.pack(pady=(15, 0))
    
    # 功能特色
    features_frame = tk.Frame(main_frame, bg="#FF6B35")
    features_frame.pack(pady=(15, 0))
    
    features = ["✓ 现代化UI设计", "✓ 模块化架构", "✓ 数据实时同步", "✓ 智能统计分析"]
    for feature in features:
        feature_label = tk.Label(features_frame, text=feature, 
                               font=('Microsoft YaHei UI', 9),
                               bg="#FF6B35", fg="white")
        feature_label.pack(anchor="w")
    
    # 定义关闭函数，确保进度条停止
    def close_splash():
        try:
            progress.stop()  # 停止进度条动画
        except:
            pass
        splash.destroy()
    
    # 3秒后自动关闭
    splash.after(3000, close_splash)
    
    return splash

def main():
    """主启动函数"""
    try:
        print("🚀 智慧餐饮管理系统启动中...")
        
        # 显示启动画面
        splash = create_splash_screen()
        splash.mainloop()
          # 导入并启动登录模块
        print("📱 加载登录模块...")
        from modern_system.modules.modern_login_module import ModernLoginModule
          # 定义登录成功回调
        def on_login_success(user_info, login_window=None):
            print(f"✅ 用户登录成功: {user_info['name']}")
            # 如果传递了登录窗口，关闭它
            if login_window:
                try:
                    login_window.destroy()
                except:
                    pass
            
            try:
                # 导入主界面系统
                from modern_system.core.modern_ui_system import ModernFoodServiceSystem
                
                # 创建并启动主系统
                main_app = ModernFoodServiceSystem()
                print("🎯 主系统启动成功！")
                main_app.run()
            except ImportError as e:
                print(f"❌ 主系统导入失败: {e}")
                messagebox.showerror("导入错误", f"无法导入主系统: {e}")
            except Exception as e:
                print(f"❌ 主系统启动失败: {e}")
                messagebox.showerror("启动错误", f"主系统启动失败: {e}")
        
        # 创建登录应用
        login_app = ModernLoginModule(on_login_success)
        print("✅ 系统启动成功！")
        
        # 运行登录界面
        login_app.run()
        
    except ImportError as e:
        error_msg = f"模块导入失败: {e}\n\n请检查以下文件是否存在:\n- modern_system/modules/modern_login_module.py\n- modern_system/core/modern_ui_system.py"
        print(f"❌ {error_msg}")
        messagebox.showerror("导入错误", error_msg)
        
    except Exception as e:
        error_msg = f"系统启动失败: {e}"
        print(f"❌ {error_msg}")
        messagebox.showerror("启动错误", error_msg)

if __name__ == "__main__":
    main()
