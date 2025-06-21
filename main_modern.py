#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
现代化智慧餐饮管理系统启动文件
直接启动现代化登录界面
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox, ttk

# 获取项目路径
current_dir = os.path.dirname(os.path.abspath(__file__))
modern_system_dir = os.path.join(current_dir, 'modern_system')

# 添加路径到系统路径
sys.path.insert(0, current_dir)
sys.path.insert(0, modern_system_dir)
sys.path.insert(0, os.path.join(modern_system_dir, 'modules'))
sys.path.insert(0, os.path.join(modern_system_dir, 'core'))

def show_startup_splash():
    """显示启动画面"""
    splash = tk.Tk()
    splash.title("智慧餐饮管理系统")
    splash.geometry("400x300")
    splash.configure(bg="#FF6B35")
    splash.resizable(False, False)
    
    # 居中显示
    splash.eval('tk::PlaceWindow . center')
    
    # 图标和标题
    title_frame = tk.Frame(splash, bg="#FF6B35")
    title_frame.pack(expand=True, fill="both")
    
    # 系统图标
    icon_label = tk.Label(title_frame, text="🍽️", font=('Segoe UI Emoji', 48), 
                         bg="#FF6B35", fg="white")
    icon_label.pack(pady=(60, 20))
    
    # 系统标题
    title_label = tk.Label(title_frame, text="智慧餐饮管理系统", 
                          font=('Microsoft YaHei UI', 20, 'bold'),
                          bg="#FF6B35", fg="white")
    title_label.pack(pady=(0, 10))
    
    # 版本信息
    version_label = tk.Label(title_frame, text="现代化版本 v2.0", 
                            font=('Microsoft YaHei UI', 12),
                            bg="#FF6B35", fg="white")
    version_label.pack(pady=(0, 30))
    
    # 进度条
    progress_frame = tk.Frame(title_frame, bg="#FF6B35")
    progress_frame.pack(fill="x", padx=50)
    
    progress = ttk.Progressbar(progress_frame, mode='indeterminate', length=300)
    progress.pack()
    progress.start()
    
    # 状态标签
    status_label = tk.Label(title_frame, text="正在加载系统组件...", 
                           font=('Microsoft YaHei UI', 10),
                           bg="#FF6B35", fg="white")
    status_label.pack(pady=(20, 0))
    
    # 自动关闭
    splash.after(3000, splash.destroy)
    splash.mainloop()

def main():
    """主启动函数"""
    try:
        print("=" * 50)
        print("智慧餐饮管理系统启动中...")
        print("=" * 50)
        
        # 直接启动，不显示启动画面
        print("正在加载登录模块...")
        
        # 导入登录模块
        try:
            from modern_system.modules.modern_login_module import ModernLoginModule
            print("✓ 成功导入登录模块")
        except ImportError as e:
            print(f"✗ 导入登录模块失败: {e}")
            try:
                from modern_login_module import ModernLoginModule
                print("✓ 使用备用导入方式成功")
            except ImportError as e2:
                print(f"✗ 备用导入也失败: {e2}")
                messagebox.showerror("导入错误", f"无法导入登录模块:\n{e}\n\n备用导入也失败:\n{e2}")
                return
        
        # 创建并启动登录应用
        print("正在启动登录界面...")
          # 定义登录成功回调
        def on_login_success(user_info, login_window):
            print(f"用户登录成功: {user_info['name']}")
            try:
                # 关闭登录窗口
                login_window.destroy()
                
                # 导入主界面系统
                from modern_system.core.modern_ui_system import ModernFoodServiceSystem
                
                # 创建并启动主系统
                main_app = ModernFoodServiceSystem()
                print("✓ 主系统创建成功，正在启动...")
                main_app.run()
            except ImportError as e:
                print(f"✗ 主系统导入失败: {e}")
                messagebox.showerror("导入错误", f"无法导入主系统: {e}")
            except Exception as e:
                print(f"✗ 主系统启动失败: {e}")
                messagebox.showerror("启动错误", f"主系统启动失败: {e}")
        
        app = ModernLoginModule(on_login_success)
        app.run()
        
    except Exception as e:
        error_msg = f"启动系统时发生错误: {e}"
        print(f"✗ {error_msg}")
        messagebox.showerror("系统错误", error_msg)

if __name__ == "__main__":
    main()
