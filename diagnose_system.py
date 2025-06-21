#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化的诊断测试脚本
"""

import sys
import os

# 添加项目路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
sys.path.insert(0, os.path.join(current_dir, 'modern_system'))

def diagnose_system():
    """诊断系统问题"""
    try:
        print("🔍 开始系统诊断...")
        
        print("1. 导入模块测试...")
        try:
            from modern_system.modules.data_manager import DataManager
            print("✅ DataManager 导入成功")
        except Exception as e:
            print(f"❌ DataManager 导入失败: {e}")
            return
        
        print("2. 创建实例测试...")
        try:
            dm = DataManager()
            print("✅ DataManager 实例创建成功")
        except Exception as e:
            print(f"❌ DataManager 实例创建失败: {e}")
            import traceback
            traceback.print_exc()
            return
        
        print("3. 检查数据文件...")
        data_path = os.path.join(current_dir, 'modern_system', 'data')
        print(f"数据目录: {data_path}")
        
        if os.path.exists(data_path):
            files = os.listdir(data_path)
            print(f"数据文件: {files}")
        else:
            print("数据目录不存在")
        
        print("4. 检查基本方法...")
        try:
            orders = dm.get_orders()
            print(f"✅ 获取订单成功，共 {len(orders)} 条")
        except Exception as e:
            print(f"❌ 获取订单失败: {e}")
        
        try:
            inventory = dm.inventory
            print(f"✅ 获取库存成功，共 {len(inventory)} 项")
        except Exception as e:
            print(f"❌ 获取库存失败: {e}")
        
        print("5. 快速订单创建测试...")
        try:
            test_order = {
                'customer_name': '快速测试',
                'items': [{'product_id': '可乐', 'quantity': 1}],
                'total_amount': 5.0
            }
            order_id = dm.create_order(test_order)
            print(f"✅ 快速订单创建成功: {order_id}")
        except Exception as e:
            print(f"⚠️ 快速订单创建失败: {e}")
        
        print("\n🎉 诊断完成！")
        
    except Exception as e:
        print(f"❌ 诊断过程出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    diagnose_system()
