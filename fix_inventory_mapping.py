#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复菜品库存映射问题
"""

import sys
import os

# 添加项目路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
sys.path.insert(0, os.path.join(current_dir, 'modern_system'))

def fix_inventory_mapping():
    """修复菜品库存映射"""
    try:
        print("🔧 修复菜品库存映射...")
        
        from modern_system.modules.data_manager import DataManager
        
        # 创建数据管理器实例
        dm = DataManager()
        
        # 添加完整的菜品库存项目
        meals_inventory = [
            {
                "id": "MEAL001",
                "name": "番茄牛肉面",
                "category": "成品菜品",
                "stock": 50,
                "min_stock": 10,
                "max_stock": 100,
                "unit": "份",
                "cost_price": 15.0,
                "last_update": "2024-06-21 10:00:00",
                "supplier": "厨房制作"
            },
            {
                "id": "MEAL002", 
                "name": "鸡蛋炒饭",
                "category": "成品菜品",
                "stock": 60,
                "min_stock": 15,
                "max_stock": 120,
                "unit": "份",
                "cost_price": 12.0,
                "last_update": "2024-06-21 10:00:00",
                "supplier": "厨房制作"
            },
            {
                "id": "MEAL003",
                "name": "牛肉汉堡",
                "category": "成品菜品",
                "stock": 40,
                "min_stock": 8,
                "max_stock": 80,
                "unit": "个",
                "cost_price": 20.0,
                "last_update": "2024-06-21 10:00:00",
                "supplier": "厨房制作"
            },
            {
                "id": "MEAL004",
                "name": "红烧肉",
                "category": "成品菜品", 
                "stock": 30,
                "min_stock": 5,
                "max_stock": 60,
                "unit": "份",
                "cost_price": 25.0,
                "last_update": "2024-06-21 10:00:00",
                "supplier": "厨房制作"
            },
            {
                "id": "MEAL005",
                "name": "可乐",
                "category": "饮料",
                "stock": 100,
                "min_stock": 20,
                "max_stock": 200,
                "unit": "瓶",
                "cost_price": 3.0,
                "last_update": "2024-06-21 10:00:00",
                "supplier": "饮料供应商"
            },
            {
                "id": "MEAL006",
                "name": "米饭",
                "category": "主食",
                "stock": 80,
                "min_stock": 20,
                "max_stock": 150,
                "unit": "份",
                "cost_price": 2.0,
                "last_update": "2024-06-21 10:00:00",
                "supplier": "厨房制作"
            },
            {
                "id": "MEAL007",
                "name": "薯条",
                "category": "小食",
                "stock": 70,
                "min_stock": 15,
                "max_stock": 120,
                "unit": "份",
                "cost_price": 6.0,
                "last_update": "2024-06-21 10:00:00",
                "supplier": "厨房制作"
            }
        ]
        
        # 检查并添加菜品库存项目
        existing_names = [item['name'] for item in dm.inventory]
        added_count = 0
        
        for meal_item in meals_inventory:
            if meal_item['name'] not in existing_names:
                dm.inventory.append(meal_item)
                added_count += 1
                print(f"✅ 添加菜品库存: {meal_item['name']} - {meal_item['stock']} {meal_item['unit']}")
        
        # 保存库存数据
        if added_count > 0:
            dm.save_inventory()
            print(f"\n🎉 成功添加 {added_count} 个菜品库存项目")
        else:
            print("\n📝 所有菜品库存项目已存在")
        
        print("\n📦 当前完整库存状态:")
        for item in dm.inventory:
            category = item.get('category', '未分类')
            print(f"   📦 {item['name']} ({category}): {item['stock']} {item.get('unit', '件')}")
        
    except Exception as e:
        print(f"❌ 修复库存映射失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    fix_inventory_mapping()
