#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
添加菜品库存数据脚本
"""

import sys
import os
import json

# 添加项目路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
sys.path.insert(0, os.path.join(current_dir, 'modern_system'))

def add_menu_inventory():
    """添加菜品库存数据"""
    try:
        from modern_system.modules.data_manager import DataManager
        
        print("🍽️ 正在添加菜品库存...")
        
        # 创建数据管理器实例
        dm = DataManager()
        
        # 菜品库存数据
        menu_items = [
            {"id": "MEAL001", "name": "番茄牛肉面", "category": "菜品", "stock": 50, "unit": "份", "price": 25.0},
            {"id": "MEAL002", "name": "鸡蛋炒饭", "category": "菜品", "stock": 30, "unit": "份", "price": 18.0},
            {"id": "MEAL003", "name": "牛肉汉堡", "category": "菜品", "stock": 25, "unit": "个", "price": 32.0},
            {"id": "MEAL004", "name": "薯条", "category": "菜品", "stock": 40, "unit": "份", "price": 12.0},
            {"id": "MEAL005", "name": "可乐", "category": "饮料", "stock": 100, "unit": "瓶", "price": 8.0},
            {"id": "MEAL006", "name": "咖啡", "category": "饮料", "stock": 60, "unit": "杯", "price": 15.0},
            {"id": "MEAL007", "name": "红烧肉", "category": "菜品", "stock": 20, "unit": "份", "price": 35.0},
            {"id": "MEAL008", "name": "米饭", "category": "主食", "stock": 80, "unit": "碗", "price": 3.0}
        ]
        
        # 添加到现有库存中
        for item in menu_items:
            # 检查是否已存在
            existing = dm.find_inventory_item(item['id'])
            if existing:
                print(f"  ✓ 更新 {item['name']} 库存: {existing['stock']} -> {item['stock']}")
                existing.update(item)
            else:
                print(f"  + 添加 {item['name']} 库存: {item['stock']} {item['unit']}")
                dm.inventory.append(item)
        
        # 保存库存数据
        dm.save_inventory()
        
        print(f"✅ 成功添加 {len(menu_items)} 个菜品的库存数据")
        print("📊 当前库存概览:")
        for item in dm.inventory:
            if item.get('category') in ['菜品', '饮料', '主食']:
                print(f"   {item['name']}: {item['stock']} {item['unit']}")
        
    except Exception as e:
        print(f"❌ 添加库存数据失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    add_menu_inventory()
