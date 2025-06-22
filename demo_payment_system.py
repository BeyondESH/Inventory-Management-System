#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
销售支付流程演示脚本
启动系统并演示完整的销售、支付、库存扣减流程
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

# 添加系统路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
sys.path.insert(0, os.path.join(current_dir, 'modern_system'))
sys.path.insert(0, os.path.join(current_dir, 'modern_system', 'modules'))
sys.path.insert(0, os.path.join(current_dir, 'modern_system', 'core'))

def test_complete_flow():
    """完整流程测试"""
    print("=" * 60)
    print("🚀 启动完整系统演示")
    print("=" * 60)
    
    try:        # 导入主系统
        from modern_system.core.modern_ui_system import ModernFoodServiceSystem
        from modern_system.modules.data_manager import data_manager
        
        print("✅ 系统模块导入成功")
        
        # 显示当前库存状态
        print("\n📦 当前库存状态:")
        inventory = data_manager.get_inventory()
        for item in inventory[:5]:
            print(f"  - {item['name']}: {item['current_stock']:.2f} {item['unit']}")
        
        print("\n💰 当前财务状态:")
        finance = data_manager.load_financial_records()
        print(f"  - 财务记录数: {len(finance)}")
        if finance:
            total_revenue = sum(r['amount'] for r in finance if r['type'] == 'revenue')
            total_cost = sum(abs(r['amount']) for r in finance if r['type'] == 'cost')
            print(f"  - 总收入: ¥{total_revenue:.2f}")
            print(f"  - 总成本: ¥{total_cost:.2f}")
            print(f"  - 净利润: ¥{total_revenue - total_cost:.2f}")
        
        print("\n📋 当前订单状态:")
        orders = data_manager.get_orders()
        print(f"  - 订单总数: {len(orders)}")
        
        print("\n🍽️ 可用菜品:")
        meals = data_manager.get_meals()
        for meal in meals[:3]:
            print(f"  - {meal['name']}: ¥{meal['price']:.2f} (食材: {', '.join(meal.get('ingredients', []))})")
        
        print(f"\n🎯 系统演示说明:")
        print("1. 系统将启动完整的餐厅管理界面")
        print("2. 进入销售模块")
        print("3. 添加菜品到购物车")
        print("4. 进行支付")
        print("5. 观察库存、财务、图表模块的自动更新")
        print("\n按任意键启动系统...")
        input()
        
        # 创建并启动主系统
        print("🚀 启动系统...")
        app = ModernFoodServiceSystem()
        
        # 显示使用说明
        def show_usage_info():
            info = """
演示使用说明：

1. 点击左侧导航栏的"销售管理"
2. 选择菜品并添加到购物车
3. 点击"结账"按钮
4. 选择支付方式完成支付
5. 观察以下变化：
   - 库存模块：相关食材数量减少
   - 财务模块：新增收入和成本记录
   - 图表模块：统计数据更新

注意：系统会自动为每个菜品扣减对应的食材库存，
并在财务模块中记录收入和成本。

关闭此对话框后系统将启动。
"""
            messagebox.showinfo("系统演示说明", info)
        
        app.root.after(1000, show_usage_info)
        app.run()
        
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_complete_flow()
