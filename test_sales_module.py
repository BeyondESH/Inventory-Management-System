#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
销售管理模块独立测试
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

# 添加项目路径
current_dir = os.path.dirname(os.path.abspath(__file__))
modern_system_dir = os.path.join(current_dir, 'modern_system')
sys.path.insert(0, current_dir)
sys.path.insert(0, modern_system_dir)
sys.path.insert(0, os.path.join(modern_system_dir, 'modules'))
sys.path.insert(0, os.path.join(modern_system_dir, 'utils'))

def test_sales_module():
    """测试销售管理模块"""
    try:
        print("🧪 测试销售管理模块...")
        
        # 导入销售模块
        from modern_system.modules.modern_sales_module import ModernSalesModule
        
        # 创建主窗口
        root = tk.Tk()
        root.title("销售管理模块测试")
        root.geometry("1200x800")
        root.configure(bg="#F8F9FA")
        
        # 创建容器
        main_frame = tk.Frame(root, bg="#F8F9FA")
        main_frame.pack(fill="both", expand=True)
        
        title_frame = tk.Frame(root, bg="#FFFFFF", height=60)
        title_frame.pack(fill="x", side="top")
        
        # 创建销售模块实例
        sales_module = ModernSalesModule(main_frame, title_frame)
        
        # 显示界面
        sales_module.show()
        
        print("✅ 销售管理模块加载成功！")
        print("📋 功能说明：")
        print("  - 分类浏览菜品")
        print("  - 点击 ➕ 添加到购物车")
        print("  - 在购物车中调整数量")
        print("  - 选择桌号并结账")
        
        # 显示提示窗口
        messagebox.showinfo("测试说明", 
                           "🍽️ 堂食点餐系统测试\n\n"
                           "功能介绍：\n"
                           "• 分类浏览菜品\n"
                           "• 点击 ➕ 添加到购物车\n"
                           "• 在购物车中调整数量\n"
                           "• 选择桌号并结账\n"
                           "• 支持多种支付方式\n\n"
                           "请体验完整的点餐流程！")
        
        # 运行界面
        root.mainloop()
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        messagebox.showerror("测试失败", f"无法加载销售模块: {e}")

if __name__ == "__main__":
    test_sales_module()
