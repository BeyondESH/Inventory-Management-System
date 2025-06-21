#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试库存管理模块的食材过滤和可制作菜品功能
"""

import sys
import os
import tkinter as tk

# 添加路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
sys.path.insert(0, os.path.join(current_dir, 'modern_system'))
sys.path.insert(0, os.path.join(current_dir, 'modern_system', 'modules'))

def test_inventory_features():
    """测试库存管理功能"""
    try:
        from modern_system.modules.modern_inventory_module import ModernInventoryModule
        
        # 创建测试窗口
        root = tk.Tk()
        root.title("库存管理模块测试")
        root.geometry("1200x800")
        
        # 创建框架
        title_frame = tk.Frame(root, bg="#FFFFFF", height=80)
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)
        
        main_frame = tk.Frame(root, bg="#F8F9FA")
        main_frame.pack(fill="both", expand=True)
        
        # 创建库存管理模块
        inventory_module = ModernInventoryModule(main_frame, title_frame)
        
        # 测试配方数据加载
        print("测试配方数据加载...")
        recipes = inventory_module.load_recipe_data()
        print(f"✓ 成功加载 {len(recipes)} 个配方")
        
        # 测试可制作菜品计算
        print("\n测试可制作菜品计算...")
        possible_meals = inventory_module.calculate_possible_meals()
        print("可制作菜品数量:")
        for meal_name, info in possible_meals.items():
            print(f"  - {meal_name}: {info['possible_servings']} 份")
        
        # 测试食材过滤
        print("\n测试食材过滤...")
        filtered_ingredients = inventory_module.filter_ingredients_only()
        print(f"✓ 过滤后食材数量: {len(filtered_ingredients)}")
        print("食材列表:")
        for ingredient in filtered_ingredients[:10]:  # 只显示前10个
            print(f"  - {ingredient['name']} ({ingredient['category']}): {ingredient['current_stock']} {ingredient['unit']}")
        
        # 显示界面
        print("\n显示库存管理界面...")
        inventory_module.show()
        
        # 运行界面
        root.mainloop()
        
    except Exception as e:
        print(f"测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_inventory_features()
