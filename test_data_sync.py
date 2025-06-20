#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试菜品管理与销售管理数据同步
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk
from modern_system.modules.modern_meal_module import ModernMealModule
from modern_system.modules.modern_sales_module import ModernSalesModule
from modern_system.utils.data_manager import data_manager

def test_data_sync():
    """测试数据同步功能"""
    print("=== 测试菜品管理与销售管理数据同步 ===")
    
    # 创建主窗口
    root = tk.Tk()
    root.title("数据同步测试")
    root.geometry("1200x800")
    root.configure(bg="#F8F9FA")
    
    # 创建标题框架
    title_frame = tk.Frame(root, bg="#FFFFFF", height=70)
    title_frame.pack(fill="x")
    title_frame.pack_propagate(False)
    
    # 创建主框架
    main_frame = tk.Frame(root, bg="#F8F9FA")
    main_frame.pack(fill="both", expand=True)
    
    # 创建菜品管理模块
    meal_module = ModernMealModule(main_frame, title_frame)
    
    # 创建销售管理模块
    sales_module = ModernSalesModule(main_frame, title_frame)
    
    # 注册模块到数据管理器
    data_manager.register_module('meal', meal_module)
    data_manager.register_module('sales', sales_module)
    
    # 显示销售管理模块
    sales_module.show()
    
    # 测试按钮
    test_frame = tk.Frame(root, bg="#F8F9FA", height=50)
    test_frame.pack(fill="x", side="bottom")
    test_frame.pack_propagate(False)
    
    def switch_to_meal():
        """切换到菜品管理"""
        meal_module.show()
        print("切换到菜品管理模块")
    
    def switch_to_sales():
        """切换到销售管理"""
        sales_module.show()
        print("切换到销售管理模块")
    
    def test_notify():
        """测试通知功能"""
        print("手动触发菜品数据更新通知...")
        data_manager.notify_modules('meals_updated')
    
    # 创建测试按钮
    tk.Button(test_frame, text="切换到菜品管理", command=switch_to_meal,
              bg="#FF6B35", fg="white", font=("Microsoft YaHei UI", 10, "bold"),
              padx=15, pady=5).pack(side="left", padx=10, pady=10)
    
    tk.Button(test_frame, text="切换到销售管理", command=switch_to_sales,
              bg="#00B894", fg="white", font=("Microsoft YaHei UI", 10, "bold"),
              padx=15, pady=5).pack(side="left", padx=10, pady=10)
    
    tk.Button(test_frame, text="手动触发数据同步", command=test_notify,
              bg="#3498DB", fg="white", font=("Microsoft YaHei UI", 10, "bold"),
              padx=15, pady=5).pack(side="left", padx=10, pady=10)
    
    # 说明标签
    info_label = tk.Label(test_frame, 
                         text="测试说明: 在菜品管理中添加/编辑/删除菜品后，销售管理应自动同步显示最新菜品",
                         bg="#F8F9FA", fg="#636E72",
                         font=("Microsoft YaHei UI", 9))
    info_label.pack(side="right", padx=10, pady=10)
    
    print("数据同步测试界面已启动")
    print("1. 点击'切换到菜品管理'进行菜品管理")
    print("2. 点击'切换到销售管理'查看销售界面")
    print("3. 在菜品管理中进行操作后，销售管理应自动更新菜品列表")
    
    root.mainloop()

if __name__ == "__main__":
    test_data_sync()
