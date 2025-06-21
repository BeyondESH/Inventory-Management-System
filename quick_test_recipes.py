#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速测试配方修复
"""

import sys
import os
import tkinter as tk

# 添加路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
sys.path.insert(0, os.path.join(current_dir, 'modern_system'))
sys.path.insert(0, os.path.join(current_dir, 'modern_system', 'modules'))

from modern_system.modules.modern_inventory_module import ModernInventoryModule

def test_recipes():
    root = tk.Tk()
    root.withdraw()
    
    title_frame = tk.Frame(root)
    main_frame = tk.Frame(root)
    
    module = ModernInventoryModule(main_frame, title_frame)
    possible_meals = module.calculate_possible_meals()
    
    print('更新后的可制作菜品数量:')
    for meal_name, info in possible_meals.items():
        print(f'  - {meal_name}: {info["possible_servings"]} 份')

if __name__ == "__main__":
    test_recipes()
