#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
财务模块测试脚本
直接测试财务模块是否能正常工作
"""

import sys
import os

# 添加系统路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
sys.path.insert(0, os.path.join(current_dir, 'modern_system'))
sys.path.insert(0, os.path.join(current_dir, 'modern_system', 'modules'))

def test_finance_module():
    """测试财务模块"""
    print("=" * 60)
    print("🧪 财务模块测试开始")
    print("=" * 60)
    
    try:
        # 导入数据管理器
        from modern_system.modules.data_manager import data_manager
        print("✅ 数据管理器导入成功")
        
        # 测试获取财务记录
        finance_records = data_manager.get_financial_records()
        print(f"✅ 财务记录加载成功，共 {len(finance_records)} 条记录")
        
        # 显示前几条记录
        if finance_records:
            print("\n📊 最近的财务记录:")
            for i, record in enumerate(finance_records[:5]):
                print(f"  {i+1}. {record['type']}: ¥{record['amount']:.2f} - {record['description']}")
        
        # 测试财务统计
        revenue_records = data_manager.get_financial_records_by_type('revenue')
        cost_records = data_manager.get_financial_records_by_type('cost')
        
        total_revenue = sum(r['amount'] for r in revenue_records)
        total_cost = sum(abs(r['amount']) for r in cost_records)
        net_profit = total_revenue - total_cost
        
        print(f"\n💰 财务统计:")
        print(f"  总收入: ¥{total_revenue:.2f}")
        print(f"  总成本: ¥{total_cost:.2f}")
        print(f"  净利润: ¥{net_profit:.2f}")
        
        # 测试导入财务模块
        print("\n🏦 测试财务模块导入...")
        import tkinter as tk
        
        # 创建测试窗口
        root = tk.Tk()
        root.withdraw()  # 隐藏主窗口
        
        # 创建模拟的框架
        content_frame = tk.Frame(root)
        title_frame = tk.Frame(root)
        
        # 导入并创建财务模块
        from modern_system.modules.modern_finance_module import ModernFinanceModule
        finance_module = ModernFinanceModule(content_frame, title_frame)
        
        print("✅ 财务模块创建成功")
        
        # 测试刷新数据方法
        if hasattr(finance_module, 'refresh_data'):
            finance_module.refresh_data()
            print("✅ 财务模块refresh_data方法测试成功")
        else:
            print("⚠️ 财务模块缺少refresh_data方法")
        
        # 清理
        root.destroy()
        
        print("\n" + "=" * 60)
        print("✅ 财务模块测试完成 - 所有功能正常")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_finance_module()
