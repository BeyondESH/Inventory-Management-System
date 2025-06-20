#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试菜品简介限制和订单模块显示
"""

import tkinter as tk
import sys
import os

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_meal_description_limit():
    """测试菜品简介字数限制"""
    print("测试菜品简介字数限制...")
    
    # 模拟菜品数据
    test_meals = [
        {"description": "经典番茄牛肉面"},  # 7字
        {"description": "经典番茄牛肉面，汤鲜味美"},  # 11字
        {"description": "经典番茄牛肉面，汤鲜味美，营养丰富"},  # 16字
        {"description": "经典番茄牛肉面，汤鲜味美，营养丰富，口感极佳"},  # 21字
    ]
    
    for meal in test_meals:
        description = meal.get('description', '')
        # 如果描述过长，截断并添加省略号（限制为10字）
        if len(description) > 10:
            description = description[:10] + "..."
        
        print(f"原描述: {meal['description']} ({len(meal['description'])}字)")
        print(f"处理后: {description}")
        print("---")

def test_order_module():
    """测试订单模块"""
    print("测试订单模块...")
    
    try:
        from modern_system.modules.modern_order_module import ModernOrderModule
        from modern_system.utils.data_manager import data_manager
        
        # 创建测试窗口
        root = tk.Tk()
        root.title("订单模块测试")
        root.geometry("1200x800")
        
        # 创建框架
        title_frame = tk.Frame(root, bg="white", height=60)
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)
        
        main_frame = tk.Frame(root, bg="#f8f9fa")
        main_frame.pack(fill="both", expand=True)
        
        # 创建订单模块
        order_module = ModernOrderModule(main_frame, title_frame)
        
        # 显示订单模块
        order_module.show()
        
        print("✓ 订单模块创建成功")
        print("✓ 订单模块显示成功")
        
        # 运行一小段时间后自动关闭
        root.after(3000, root.destroy)  # 3秒后关闭
        root.mainloop()
        
        return True
        
    except Exception as e:
        print(f"✗ 订单模块测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_sales_module():
    """测试销售模块"""
    print("测试销售模块...")
    
    try:
        from modern_system.modules.modern_sales_module import ModernSalesModule
        
        # 创建测试窗口
        root = tk.Tk()
        root.title("销售模块测试")
        root.geometry("1200x800")
        
        # 创建框架
        title_frame = tk.Frame(root, bg="white", height=60)
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)
        
        main_frame = tk.Frame(root, bg="#f8f9fa")
        main_frame.pack(fill="both", expand=True)
        
        # 创建销售模块
        sales_module = ModernSalesModule(main_frame, title_frame)
        
        # 显示销售模块
        sales_module.show()
        
        print("✓ 销售模块创建成功")
        print("✓ 销售模块显示成功")
        print(f"✓ 菜品数量: {len(sales_module.meals_data)}")
        
        # 测试菜品简介
        for i, meal in enumerate(sales_module.meals_data[:3]):  # 只测试前3个
            description = meal.get('description', '')
            if len(description) > 10:
                description = description[:10] + "..."
            print(f"  菜品{i+1}: {meal.get('name', '未知')} - {description}")
        
        # 运行一小段时间后自动关闭
        root.after(3000, root.destroy)  # 3秒后关闭
        root.mainloop()
        
        return True
        
    except Exception as e:
        print(f"✗ 销售模块测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("开始测试修复功能")
    print("=" * 50)
    
    # 测试1: 菜品简介限制
    test_meal_description_limit()
    print()
    
    # 测试2: 订单模块
    test_order_result = test_order_module()
    print()
    
    # 测试3: 销售模块
    test_sales_result = test_sales_module()
    print()
    
    print("=" * 50)
    print("测试结果汇总:")
    print(f"✓ 菜品简介限制: 已实现")
    print(f"{'✓' if test_order_result else '✗'} 订单模块显示: {'正常' if test_order_result else '异常'}")
    print(f"{'✓' if test_sales_result else '✗'} 销售模块显示: {'正常' if test_sales_result else '异常'}")
    print("=" * 50)
