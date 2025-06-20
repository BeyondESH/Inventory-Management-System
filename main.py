#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智慧餐饮管理系统主启动文件
项目入口点 - 使用现代化登录界面
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

# 获取项目根目录
current_dir = os.path.dirname(os.path.abspath(__file__))
modern_system_dir = os.path.join(current_dir, 'modern_system')

# 添加项目路径
for path in [current_dir, modern_system_dir]:
    if path not in sys.path:
        sys.path.insert(0, path)

def main():
    """主函数，启动现代化登录系统"""
    try:
        print("正在启动智慧餐饮管理系统...")
        
        # 检查modern_system目录是否存在
        if not os.path.exists(modern_system_dir):
            messagebox.showerror("错误", f"找不到modern_system目录: {modern_system_dir}")
            return
        
        # 导入并启动现代化登录模块
        try:
            from modern_system.modules.modern_login_module import ModernLoginModule
            
            # 创建主窗口（隐藏）
            root = tk.Tk()
            root.withdraw()  # 隐藏主窗口
            
            # 启动登录界面
            login_app = ModernLoginModule()
            login_app.run()
            
        except ImportError as e:
            messagebox.showerror("导入错误", f"无法导入登录模块: {e}")
            print(f"导入错误: {e}")
            
            # 尝试直接运行main_modern.py
            main_modern_path = os.path.join(current_dir, 'main_modern.py')
            if os.path.exists(main_modern_path):
                print("尝试运行main_modern.py...")
                exec(open(main_modern_path).read())
            else:
                print("未找到main_modern.py文件")
                
    except Exception as e:
        print(f"启动系统时发生错误: {e}")
        messagebox.showerror("系统错误", f"启动系统时发生错误: {e}")

if __name__ == "__main__":
    main()
