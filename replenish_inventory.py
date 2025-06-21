#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
补充库存数据
"""

import sys
import os
import json

# 添加项目路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
sys.path.insert(0, os.path.join(current_dir, 'modern_system'))

def replenish_inventory():
    """补充库存数据"""
    try:
        print("📦 正在补充库存数据...")
        
        from modern_system.modules.data_manager import DataManager
        
        # 创建数据管理器实例
        dm = DataManager()
        
        # 为每个库存项目补充数量
        for item in dm.inventory:
            item['stock'] = 100  # 设置库存为100
            item['last_update'] = "2024-06-21 10:00:00"
        
        # 添加更多库存项目（对应菜品）
        additional_inventory = [
            {
                "id": "INV005",
                "name": "鸡蛋炒饭",
                "category": "成品",
                "stock": 50,
                "min_stock": 10,
                "max_stock": 200,
                "unit": "份",
                "cost_price": 12.0,
                "last_update": "2024-06-21 10:00:00",
                "supplier": "厨房制作"
            },
            {
                "id": "INV006", 
                "name": "牛肉汉堡",
                "category": "成品",
                "stock": 30,
                "min_stock": 5,
                "max_stock": 100,
                "unit": "个",
                "cost_price": 18.0,
                "last_update": "2024-06-21 10:00:00",
                "supplier": "厨房制作"
            },
            {
                "id": "INV007",
                "name": "薯条", 
                "category": "成品",
                "stock": 80,
                "min_stock": 15,
                "max_stock": 150,
                "unit": "份",
                "cost_price": 6.0,
                "last_update": "2024-06-21 10:00:00",
                "supplier": "厨房制作"
            }
        ]
        
        # 检查并添加新的库存项目
        existing_names = [item['name'] for item in dm.inventory]
        for new_item in additional_inventory:
            if new_item['name'] not in existing_names:
                dm.inventory.append(new_item)
        
        # 保存库存数据
        dm.save_inventory()
        
        print("✅ 库存补充完成！")
        print("\n📦 当前库存状态:")
        for item in dm.inventory:
            print(f"   📦 {item['name']}: {item['stock']} {item.get('unit', '件')}")
        
    except Exception as e:
        print(f"❌ 库存补充失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    replenish_inventory()
