#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
展示最终版本的库存管理界面（无统计卡片，无搜索筛选）
"""

import sys
import os
import tkinter as tk

# 添加路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
sys.path.insert(0, os.path.join(current_dir, 'modern_system'))
sys.path.insert(0, os.path.join(current_dir, 'modern_system', 'modules'))

def demo_final_inventory_interface():
    """演示最终版本的库存管理界面"""
    try:
        from modern_system.modules.modern_inventory_module import ModernInventoryModule
        
        # 创建演示窗口
        root = tk.Tk()
        root.title("库存管理模块 - 最终简化版本")
        root.geometry("1400x800")
        root.configure(bg="#F8F9FA")
        
        # 创建框架
        title_frame = tk.Frame(root, bg="#FFFFFF", height=80)
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)
        
        main_frame = tk.Frame(root, bg="#F8F9FA")
        main_frame.pack(fill="both", expand=True)
        
        # 添加标题说明
        title_label = tk.Label(title_frame, 
                              text="📦 库存管理模块 - 极简版（无统计卡片 + 无搜索筛选）",
                              font=('Microsoft YaHei UI', 14, 'bold'),
                              bg="#FFFFFF", fg="#2C3E50")
        title_label.pack(expand=True)
        
        # 创建库存管理模块
        inventory_module = ModernInventoryModule(main_frame, title_frame)
        
        print("=== 库存管理界面最终版本说明 ===")
        print("✅ 已移除顶部4个统计卡片")
        print("✅ 已移除搜索和筛选功能行")
        print("✅ 界面现在只保留核心功能:")
        print("   └─ 🍽️ 可制作菜品数量展示")
        print("   └─ 🥬 食材库存清单（纯净显示）")
        print("✅ 最简洁的界面布局，专注于核心信息")
        print("✅ 所有核心库存管理功能完整保留")
        print("\n正在显示最终版本的库存管理界面...")
        
        # 显示界面
        inventory_module.show()
        
        # 在界面上显示当前可制作菜品数量
        print("\n=== 当前库存可制作菜品情况 ===")
        possible_meals = inventory_module.calculate_possible_meals()
        for meal_name, info in possible_meals.items():
            servings = info['possible_servings']
            if servings > 0:
                status = f"✅ {servings} 份"
            else:
                status = "❌ 缺料"
            print(f"  - {meal_name}: {status}")
        
        # 显示当前食材数量
        print("\n=== 当前食材库存情况 ===")
        ingredients = inventory_module.filter_ingredients_only()
        for ingredient in ingredients:
            stock = ingredient['current_stock']
            min_stock = ingredient['min_stock']
            if stock <= min_stock:
                status = "⚠️ 偏低" if stock > 0 else "❌ 缺货"
            else:
                status = "✅ 充足"
            print(f"  - {ingredient['name']}: {stock} {ingredient['unit']} ({status})")
        
        # 运行界面
        root.mainloop()
        
    except Exception as e:
        print(f"演示失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    demo_final_inventory_interface()
