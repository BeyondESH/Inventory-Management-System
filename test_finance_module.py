#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试财务模块的固定成本功能
"""

import tkinter as tk
from tkinter import ttk
import sys
import os

# 添加路径以导入模块
sys.path.append(os.path.join(os.path.dirname(__file__), 'modern_system'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'modern_system', 'modules'))

try:
    from modern_system.modules.modern_finance_module import ModernFinanceModule
except ImportError:
    from modern_finance_module import ModernFinanceModule

def test_finance_module():
    """测试财务模块功能"""
    
    # 创建主窗口
    root = tk.Tk()
    root.title("财务模块测试")
    root.geometry("1200x800")
    root.configure(bg='#F8F9FA')
    
    try:
        # 创建主框架
        main_frame = tk.Frame(root, bg='#F8F9FA')
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 创建标题框架
        title_frame = tk.Frame(main_frame, bg='#F8F9FA')
        title_frame.pack(fill="x", pady=(0, 10))
        
        # 添加标题
        title_label = tk.Label(title_frame, text="财务管理系统测试", 
                             font=('Microsoft YaHei UI', 18, 'bold'),
                             bg='#F8F9FA', fg='#2D3436')
        title_label.pack()
        
        # 创建内容框架
        content_frame = tk.Frame(main_frame, bg='#FFFFFF', relief="solid", bd=1)
        content_frame.pack(fill="both", expand=True)
        
        # 创建财务模块实例
        finance_module = ModernFinanceModule(content_frame, title_frame)
        
        # 显示财务模块
        finance_module.show()
        
        print("财务模块测试启动成功！")
        print("功能测试项目:")
        print("1. 查看固定成本管理选项卡")
        print("2. 测试添加固定成本功能")
        print("3. 测试编辑固定成本功能")
        print("4. 测试删除固定成本功能")
        print("5. 检查数据持久化（添加/编辑/删除后数据是否保存到文件）")
        print("6. 重启程序验证数据是否正确加载")
        
    except Exception as e:
        print(f"创建财务模块失败: {e}")
        import traceback
        traceback.print_exc()
        
        # 显示错误信息
        error_label = tk.Label(main_frame, 
                             text=f"模块加载失败: {e}", 
                             font=('Microsoft YaHei UI', 12),
                             bg='#F8F9FA', fg='#E74C3C')
        error_label.pack(pady=50)
    
    # 启动主循环
    root.mainloop()

if __name__ == "__main__":
    print("=" * 60)
    print("财务模块功能测试")
    print("=" * 60)
    
    test_finance_module()
