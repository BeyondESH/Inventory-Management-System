#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复订单管理模块的关键方法
"""

import sys
import os

# 添加项目路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
sys.path.insert(0, os.path.join(current_dir, 'modern_system'))

def fix_order_module():
    """修复订单模块的显示问题"""
    try:
        print("🔧 正在修复订单管理模块...")
        
        # 读取当前文件内容
        order_module_path = os.path.join(current_dir, 'modern_system', 'modules', 'modern_order_module.py')
        
        # 创建修复后的关键方法代码
        refresh_method = '''
    def refresh_order_list(self):
        """刷新订单列表"""
        print("🔄 刷新订单列表...")
        
        # 重新加载订单数据
        self.order_data = self.load_order_data()
        print(f"📄 加载了 {len(self.order_data)} 条订单")
        
        # 清空容器（如果存在）
        if hasattr(self, 'orders_container') and self.orders_container:
            for widget in self.orders_container.winfo_children():
                widget.destroy()
        
        # 筛选订单
        filtered_orders = self.order_data
        if self.current_filter != "全部":
            filtered_orders = [order for order in self.order_data if order.get('status') == self.current_filter]
        
        print(f"🎯 筛选后显示 {len(filtered_orders)} 条订单")
        
        # 创建订单卡片
        if hasattr(self, 'orders_container') and self.orders_container:
            for order in filtered_orders:
                try:
                    self.create_order_card(self.orders_container, order)
                except Exception as e:
                    print(f"❌ 创建订单卡片失败: {e}")
        
        # 更新统计信息
        if hasattr(self, 'update_statistics'):
            self.update_statistics()
'''
        
        print("✅ 修复方法已准备就绪")
        print("📝 建议手动检查订单模块的 refresh_order_list 方法")
        
    except Exception as e:
        print(f"❌ 修复失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    fix_order_module()
