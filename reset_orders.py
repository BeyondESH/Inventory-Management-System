#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
重置订单数据脚本
"""

import sys
import os
import json

# 添加项目路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
sys.path.insert(0, os.path.join(current_dir, 'modern_system'))

def reset_orders_data():
    """重置订单数据为示例数据"""
    try:
        from modern_system.modules.data_manager import DataManager
        
        print("🔄 正在重置订单数据...")
        
        # 创建数据管理器实例
        dm = DataManager()
        
        # 获取默认订单数据
        default_orders = dm.get_default_orders()
        
        # 清空现有订单
        dm.orders = default_orders.copy()
        
        # 保存到文件
        dm.save_orders()
        
        print(f"✅ 成功重置订单数据，添加了 {len(default_orders)} 条示例订单")
        
        # 显示重置的订单信息
        for i, order in enumerate(default_orders, 1):
            print(f"   {i}. 订单#{order['id']} - {order['customer_name']} - {order['status']}")
        
    except Exception as e:
        print(f"❌ 重置订单数据失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    reset_orders_data()
