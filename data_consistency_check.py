#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据同步状态检查器
用于检查各模块数据是否保持一致
"""

import sys
import os
import datetime
import json

# 添加路径
current_dir = os.path.dirname(os.path.abspath(__file__))
modern_system_dir = os.path.join(current_dir, 'modern_system')
sys.path.insert(0, modern_system_dir)
sys.path.insert(0, os.path.join(modern_system_dir, 'utils'))

def check_data_consistency():
    """检查数据一致性"""
    print("=" * 70)
    print("智慧餐饮管理系统 - 数据同步状态检查")
    print("=" * 70)
    
    try:
        from modern_system.utils.data_manager import data_manager
        
        # 检查数据文件是否存在
        print("1. 数据文件检查:")
        data_dir = data_manager.data_dir
        for data_type, filename in data_manager.data_files.items():
            file_path = os.path.join(data_dir, filename)
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    print(f"   ✓ {data_type:12} ({filename:15}) - {len(data):3} 条记录")
            else:
                print(f"   ✗ {data_type:12} ({filename:15}) - 文件不存在")
        
        # 检查数据关联性
        print("\n2. 数据关联性检查:")
        
        # 获取所有数据
        orders = data_manager.get_orders()
        inventory = data_manager.get_inventory()
        meals = data_manager.load_data('meals')
        finance = data_manager.get_finance_records()
        sales = data_manager.load_data('sales')
        
        print(f"   订单数量: {len(orders)}")
        print(f"   库存项目: {len(inventory)}")
        print(f"   菜品数量: {len(meals)}")
        print(f"   财务记录: {len(finance)}")
        print(f"   销售记录: {len(sales)}")
        
        # 检查订单-财务-销售关联
        print("\n3. 订单关联检查:")
        order_ids = set(order.get('id') for order in orders)
        finance_order_ids = set(record.get('order_id') for record in finance if record.get('order_id'))
        sales_order_ids = set(record.get('order_id') for record in sales if record.get('order_id'))
        
        print(f"   订单ID数量: {len(order_ids)}")
        print(f"   财务关联订单: {len(finance_order_ids)}")
        print(f"   销售关联订单: {len(sales_order_ids)}")
        
        # 找出不匹配的订单
        missing_finance = order_ids - finance_order_ids
        missing_sales = order_ids - sales_order_ids
        
        if missing_finance:
            print(f"   ⚠️  缺少财务记录的订单: {len(missing_finance)} 个")
        if missing_sales:
            print(f"   ⚠️  缺少销售记录的订单: {len(missing_sales)} 个")
        
        if not missing_finance and not missing_sales:
            print("   ✓ 所有订单都有对应的财务和销售记录")
        
        # 检查库存状态
        print("\n4. 库存状态检查:")
        low_stock_items = data_manager.get_low_stock_items()
        total_value = sum(item.get('quantity', 0) * item.get('price', 0) for item in inventory)
        
        print(f"   库存总价值: ￥{total_value:,.2f}")
        print(f"   低库存项目: {len(low_stock_items)} 个")
        
        if low_stock_items:
            print("   预警库存:")
            for item in low_stock_items[:5]:  # 最多显示5个
                print(f"     - {item['name']}: {item['quantity']}/{item['min_stock']} {item['unit']}")
        
        # 今日业务统计
        print("\n5. 今日业务统计:")
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        
        today_orders = [order for order in orders if order.get('create_time', '').startswith(today)]
        today_revenue = sum(record.get('amount', 0) for record in finance 
                           if record.get('date') == today and record.get('type') == 'income')
        
        print(f"   今日订单: {len(today_orders)} 单")
        print(f"   今日营收: ￥{today_revenue:.2f}")
        
        if today_orders:
            print("   今日订单详情:")
            for order in today_orders[-3:]:  # 显示最近3个
                print(f"     - {order.get('id')}: ￥{order.get('total_amount', 0):.2f} ({order.get('status', '未知')})")
        
        # 数据完整性评分
        print("\n6. 数据完整性评分:")
        score = 0
        total_checks = 5
        
        # 检查1: 文件存在性
        if all(os.path.exists(os.path.join(data_dir, filename)) for filename in data_manager.data_files.values()):
            score += 1
            print("   ✓ 数据文件完整性: 100%")
        else:
            print("   ✗ 数据文件不完整")
        
        # 检查2: 订单-财务关联
        if not missing_finance:
            score += 1
            print("   ✓ 订单-财务关联: 100%")
        else:
            print(f"   ✗ 订单-财务关联: {(len(order_ids)-len(missing_finance))/len(order_ids)*100:.1f}%")
        
        # 检查3: 订单-销售关联
        if not missing_sales:
            score += 1
            print("   ✓ 订单-销售关联: 100%")
        else:
            print(f"   ✗ 订单-销售关联: {(len(order_ids)-len(missing_sales))/len(order_ids)*100:.1f}%")
        
        # 检查4: 库存数据有效性
        if all(item.get('quantity', 0) >= 0 for item in inventory):
            score += 1
            print("   ✓ 库存数据有效性: 100%")
        else:
            print("   ✗ 存在无效库存数据")
        
        # 检查5: 财务数据一致性
        finance_total = sum(record.get('amount', 0) for record in finance if record.get('type') == 'income')
        sales_total = sum(record.get('total_amount', 0) for record in sales)
        if abs(finance_total - sales_total) < 0.01:  # 允许微小误差
            score += 1
            print("   ✓ 财务-销售数据一致性: 100%")
        else:
            print(f"   ✗ 财务-销售数据不一致: ￥{abs(finance_total - sales_total):.2f}")
        
        # 总评分
        percentage = (score / total_checks) * 100
        print(f"\n数据完整性总评分: {score}/{total_checks} ({percentage:.1f}%)")
        
        if percentage >= 90:
            print("🎉 系统数据状态: 优秀")
        elif percentage >= 80:
            print("👍 系统数据状态: 良好")
        elif percentage >= 70:
            print("⚠️  系统数据状态: 一般")
        else:
            print("❌ 系统数据状态: 需要修复")
        
        print("=" * 70)
        
        return score == total_checks
        
    except Exception as e:
        print(f"✗ 检查失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    check_data_consistency()
