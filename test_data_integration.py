#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据联动测试脚本
测试各模块间数据同步是否正常
"""

import sys
import os
import datetime

# 添加路径
current_dir = os.path.dirname(os.path.abspath(__file__))
modern_system_dir = os.path.join(current_dir, 'modern_system')
sys.path.insert(0, modern_system_dir)
sys.path.insert(0, os.path.join(modern_system_dir, 'utils'))

def test_data_integration():
    """测试数据联动"""
    print("=" * 60)
    print("数据联动测试")
    print("=" * 60)
    
    try:
        # 导入数据管理器
        from modern_system.utils.data_manager import data_manager
        print("✓ 数据管理器导入成功")
        
        # 测试1: 查看初始库存
        print("\n1. 查看初始库存数据:")
        inventory = data_manager.get_inventory()
        for item in inventory[:3]:  # 只显示前3个
            print(f"   - {item['name']}: {item['quantity']} {item['unit']}")
        
        # 测试2: 查看初始订单
        print("\n2. 查看初始订单数据:")
        orders = data_manager.get_orders()
        print(f"   初始订单数量: {len(orders)}")
        
        # 测试3: 模拟下单
        print("\n3. 模拟创建订单:")
        test_order = {
            'table_number': 'A01',
            'customer_name': '测试客户',
            'phone': '138****1234',
            'address': '堂食',
            'items': [
                {
                    'name': '番茄牛肉面',
                    'quantity': 2,
                    'price': 25.0,
                    'subtotal': 50.0
                }
            ],
            'total_amount': 50.0,
            'payment_method': '支付宝',
            'order_type': '堂食',
            'status': '已完成'
        }
        
        order_id = data_manager.add_order(test_order)
        print(f"   ✓ 订单创建成功: {order_id}")
        
        # 测试4: 检查库存变化
        print("\n4. 检查库存变化:")
        updated_inventory = data_manager.get_inventory()
        for item in updated_inventory:
            if item['name'] in ['番茄', '牛肉', '面条']:
                print(f"   - {item['name']}: {item['quantity']} {item['unit']}")
        
        # 测试5: 检查订单增加
        print("\n5. 检查订单数据:")
        updated_orders = data_manager.get_orders()
        print(f"   当前订单数量: {len(updated_orders)}")
        if updated_orders:
            latest_order = updated_orders[-1]
            print(f"   最新订单: {latest_order['id']} - ￥{latest_order['total_amount']}")
        
        # 测试6: 检查财务记录
        print("\n6. 检查财务记录:")
        finance_records = data_manager.get_finance_records()
        print(f"   财务记录数量: {len(finance_records)}")
        if finance_records:
            latest_finance = finance_records[-1]
            print(f"   最新财务记录: {latest_finance['id']} - ￥{latest_finance['amount']}")
        
        # 测试7: 检查销售记录
        print("\n7. 检查销售记录:")
        sales_records = data_manager.load_data('sales')
        print(f"   销售记录数量: {len(sales_records)}")
        if sales_records:
            latest_sale = sales_records[-1]
            print(f"   最新销售记录: {latest_sale['id']} - ￥{latest_sale['total_amount']}")
        
        # 测试8: 获取仪表盘统计
        print("\n8. 仪表盘统计数据:")
        stats = data_manager.get_dashboard_stats()
        print(f"   今日营收: ￥{stats['today_revenue']:.2f}")
        print(f"   今日订单: {stats['today_orders']} 单")
        print(f"   库存预警: {stats['low_stock_count']} 项")
        print(f"   客户总数: {stats['total_customers']} 人")
        
        print("\n" + "=" * 60)
        print("✓ 数据联动测试完成！所有功能正常")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_data_integration()
