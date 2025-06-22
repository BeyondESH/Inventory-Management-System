#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
订单流程测试脚本
测试支付后库存扣减、财务更新等功能
"""

import sys
import os
import json

# 添加项目路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(current_dir, 'modern_system', 'modules'))

from data_manager import data_manager

def test_order_flow():
    """测试完整的订单流程"""
    print("=" * 60)
    print("开始测试订单流程")
    print("=" * 60)
    
    # 1. 显示初始库存状态
    print("\n1. 初始库存状态:")
    inventory = data_manager.get_inventory()
    for item in inventory[:5]:  # 只显示前5项
        print(f"   {item['name']}: {item['current_stock']} {item['unit']}")
    
    # 2. 显示初始财务记录数量
    initial_finance_count = len(data_manager.get_financial_records())
    print(f"\n2. 初始财务记录数量: {initial_finance_count}")
    
    # 3. 获取菜品信息
    meals = data_manager.get_meals()
    if not meals:
        print("❌ 没有可用菜品")
        return
    
    test_meal = meals[0]  # 使用第一个菜品进行测试
    print(f"\n3. 测试菜品: {test_meal['name']}")
    print(f"   价格: ¥{test_meal['price']}")
    print(f"   食材: {test_meal.get('ingredients', [])}")
    
    # 4. 创建测试订单
    print(f"\n4. 创建订单...")
    order_data = {
        'meal_id': test_meal['id'],
        'customer_id': 'TEST_CUSTOMER',
        'quantity': 2,
        'note': '测试订单 - 库存扣减验证',
        'status': 'Received'
    }
    
    order_id = data_manager.create_order(order_data)
    
    if order_id:
        print(f"   ✅ 订单创建成功: {order_id}")
    else:
        print("   ❌ 订单创建失败")
        return
    
    # 5. 检查库存变化
    print(f"\n5. 库存变化:")
    new_inventory = data_manager.get_inventory()
    for item in new_inventory[:5]:  # 只显示前5项
        old_item = next((x for x in inventory if x['id'] == item['id']), None)
        if old_item:
            stock_change = item['current_stock'] - old_item['current_stock']
            if stock_change != 0:
                print(f"   {item['name']}: {old_item['current_stock']} → {item['current_stock']} (变化: {stock_change})")
            else:
                print(f"   {item['name']}: {item['current_stock']} {item['unit']} (无变化)")
    
    # 6. 检查财务记录
    print(f"\n6. 财务记录变化:")
    new_finance_records = data_manager.get_financial_records()
    new_finance_count = len(new_finance_records)
    print(f"   财务记录数量: {initial_finance_count} → {new_finance_count}")
    
    # 显示最新的财务记录
    if new_finance_count > initial_finance_count:
        print("   新增财务记录:")
        recent_records = sorted(new_finance_records, key=lambda x: x.get('create_time', ''), reverse=True)
        for record in recent_records[:3]:  # 显示最近3条记录
            record_type = record.get('type', 'unknown')
            amount = record.get('amount', 0)
            description = record.get('description', 'No description')
            print(f"     - {record_type}: ¥{amount:.2f} ({description})")
    
    # 7. 检查仪表盘统计
    print(f"\n7. 仪表盘统计:")
    data_manager.update_dashboard_stats()
    stats = data_manager.dashboard_stats
    print(f"   今日销售额: ¥{stats.get('today_sales', 0):.2f}")
    print(f"   今日订单数: {stats.get('order_count', 0)}")
    print(f"   低库存项目: {stats.get('low_stock_count', 0)}")
    print(f"   客户数量: {stats.get('customer_count', 0)}")
    
    print("\n" + "=" * 60)
    print("订单流程测试完成")
    print("=" * 60)

def test_ingredient_consumption():
    """测试食材消耗计算"""
    print("\n" + "=" * 60)
    print("测试食材消耗计算")
    print("=" * 60)
    
    # 获取一个有食材信息的菜品
    meals = data_manager.get_meals()
    for meal in meals:
        ingredients = meal.get('ingredients', [])
        if ingredients:
            print(f"\n菜品: {meal['name']}")
            print(f"食材: {ingredients}")
            
            # 模拟制作1份和5份的食材消耗
            for quantity in [1, 5]:
                print(f"\n制作 {quantity} 份所需食材:")
                
                # 这里使用与data_manager相同的消耗标准
                ingredient_consumption = {
                    'Tomato': 0.2, 'Beef': 0.15, 'Noodles': 0.1,
                    'Egg': 0.05, 'Rice': 0.08, 'Chicken': 0.15,
                    'Pork': 0.15, 'Fish': 0.2, 'Potato': 0.1,
                    'Onion': 0.05, 'Carrot': 0.05, 'Cabbage': 0.1,
                    'Oil': 0.02, 'Salt': 0.005, 'Soy Sauce': 0.01,
                }
                
                for ingredient in ingredients:
                    required = ingredient_consumption.get(ingredient, 0.1) * quantity
                    print(f"   {ingredient}: {required:.3f} kg/unit")
            break
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    print("启动订单流程测试...")
    test_order_flow()
    test_ingredient_consumption()
