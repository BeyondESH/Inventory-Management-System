#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
补充食材到库存数据
"""

import json
import os

def add_missing_ingredients():
    """添加缺失的食材到库存"""
    inventory_file = os.path.join('modern_system', 'data', 'inventory.json')
    
    # 读取现有库存
    with open(inventory_file, 'r', encoding='utf-8') as f:
        inventory = json.load(f)
    
    # 需要添加的食材
    new_ingredients = [
        {
            "id": "INV050",
            "name": "鸡蛋",
            "category": "肉类",
            "quantity": 200,
            "unit": "个",
            "price": 1.2,
            "min_stock": 50,
            "stock": 200,
            "last_update": "2025-06-21 15:00:00"
        },
        {
            "id": "INV051",
            "name": "大米",
            "category": "主食",
            "quantity": 80,
            "unit": "kg",
            "price": 4.5,
            "min_stock": 20,
            "stock": 80,
            "last_update": "2025-06-21 15:00:00"
        },
        {
            "id": "INV052",
            "name": "面包",
            "category": "主食",
            "quantity": 60,
            "unit": "个",
            "price": 8.0,
            "min_stock": 20,
            "stock": 60,
            "last_update": "2025-06-21 15:00:00"
        },
        {
            "id": "INV053",
            "name": "生菜",
            "category": "蔬菜",
            "quantity": 25,
            "unit": "kg",
            "price": 10.0,
            "min_stock": 5,
            "stock": 25,
            "last_update": "2025-06-21 15:00:00"
        },
        {
            "id": "INV054",
            "name": "猪肉",
            "category": "肉类",
            "quantity": 30,
            "unit": "kg",
            "price": 28.0,
            "min_stock": 8,
            "stock": 30,
            "last_update": "2025-06-21 15:00:00"
        },
        {
            "id": "INV055",
            "name": "生抽",
            "category": "调料",
            "quantity": 10,
            "unit": "kg",
            "price": 12.0,
            "min_stock": 2,
            "stock": 10,
            "last_update": "2025-06-21 15:00:00"
        },
        {
            "id": "INV056",
            "name": "糖",
            "category": "调料",
            "quantity": 15,
            "unit": "kg",
            "price": 8.0,
            "min_stock": 3,
            "stock": 15,
            "last_update": "2025-06-21 15:00:00"
        },
        {
            "id": "INV057",
            "name": "可乐原料",
            "category": "调料",
            "quantity": 50,
            "unit": "L",
            "price": 15.0,
            "min_stock": 10,
            "stock": 50,
            "last_update": "2025-06-21 15:00:00"
        }
    ]
    
    # 检查并添加新食材
    existing_names = {item.get('name', '') for item in inventory}
    added_count = 0
    
    for ingredient in new_ingredients:
        if ingredient['name'] not in existing_names:
            inventory.append(ingredient)
            added_count += 1
            print(f"✓ 添加食材: {ingredient['name']}")
        else:
            print(f"- 食材已存在: {ingredient['name']}")
    
    # 保存更新后的库存
    with open(inventory_file, 'w', encoding='utf-8') as f:
        json.dump(inventory, f, ensure_ascii=False, indent=2)
    
    print(f"\n总共添加了 {added_count} 个新食材")
    print("库存数据已更新!")

if __name__ == "__main__":
    add_missing_ingredients()
