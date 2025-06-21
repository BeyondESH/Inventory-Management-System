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
        
        # 定义登录成功回调
        def on_login_success(user_info, login_window):
            print(f"用户登录成功: {user_info['name']}")
            try:
                # 关闭登录窗口（如果存在）
                if login_window:
                    login_window.destroy()
                
                # 导入主界面系统
                try:
                    from modern_system.core.modern_ui_system import ModernFoodServiceSystem
                    print("✓ 成功导入主系统")
                except ImportError as e:
                    print(f"✗ 主系统导入失败: {e}")
                    try:
                        # 备用导入
                        sys.path.append(os.path.join(modern_system_dir, 'core'))
                        from modern_ui_system import ModernFoodServiceSystem
                        print("✓ 使用备用方式导入主系统")
                    except ImportError as e2:
                        print(f"✗ 备用导入主系统也失败: {e2}")
                        messagebox.showerror("导入错误", f"无法导入主系统: {e2}")
                        return
                
                # 创建并启动主系统
                main_app = ModernFoodServiceSystem()
                print("✓ 主系统创建成功，正在启动...")
                main_app.run()
            except Exception as e:
                print(f"✗ 主系统启动失败: {e}")
                messagebox.showerror("启动错误", f"主系统启动失败: {e}")
        
        # 显示简化登录界面
        def show_simple_login():
            login_root = tk.Tk()
            login_root.title("智慧餐饮管理系统 - 登录")
            login_root.geometry("500x400")
            login_root.configure(bg="#FF6B35")
            login_root.resizable(False, False)
            
            # 居中显示
            login_root.eval('tk::PlaceWindow . center')
            
            # 标题区域
            title_frame = tk.Frame(login_root, bg="#FF6B35")
            title_frame.pack(expand=True, fill="both", padx=40, pady=40)
            
            # 系统图标
            tk.Label(title_frame, text="🍽️", font=('Segoe UI Emoji', 64), 
                    bg="#FF6B35", fg="white").pack(pady=(20, 10))
            
            # 系统标题
            tk.Label(title_frame, text="智慧餐饮管理系统", 
                    font=('Microsoft YaHei UI', 24, 'bold'),
                    bg="#FF6B35", fg="white").pack(pady=(0, 10))
            
            # 版本信息
            tk.Label(title_frame, text="现代化版本 v2.0", 
                    font=('Microsoft YaHei UI', 14),
                    bg="#FF6B35", fg="white").pack(pady=(0, 30))
            
            # 登录按钮
            def guest_login():
                login_root.destroy()
                on_login_success({'name': '游客用户', 'type': 'guest'}, None)
            
            login_btn = tk.Button(title_frame, text="🚀 开始使用系统", 
                                font=('Microsoft YaHei UI', 16, 'bold'),
                                bg="white", fg="#FF6B35",
                                padx=30, pady=15, bd=0,
                                cursor="hand2",
                                command=guest_login)
            login_btn.pack(pady=20)
            
            # 说明文字
            tk.Label(title_frame, text="点击上方按钮进入系统主界面", 
                    font=('Microsoft YaHei UI', 12),
                    bg="#FF6B35", fg="white").pack(pady=(10, 0))
            
            login_root.mainloop()
        
        # 尝试导入并使用完整登录模块
        print("正在加载登录模块...")
        try:
            from modern_system.modules.modern_login_module import ModernLoginModule
            print("✓ 成功导入登录模块")
            app = ModernLoginModule(on_login_success)
            app.run()
        except Exception as e:
            print(f"⚠️ 完整登录模块不可用，使用简化登录界面: {e}")
            show_simple_login()
        
    except Exception as e:
        error_msg = f"启动系统时发生错误: {e}"
        print(f"✗ {error_msg}")
        messagebox.showerror("系统错误", error_msg)

if __name__ == "__main__":
    main()
