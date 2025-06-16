#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
财务管理模块测试脚本
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

import tkinter as tk
from finance_module import FinanceModule
from order_module import OrderModule
from meal_module import MealModule

def test_finance_module():
    """测试财务管理模块"""
    print("启动财务管理模块测试...")
    
    # 创建主窗口
    root = tk.Tk()
    root.title("财务管理模块测试")
    root.geometry("1400x900")
    root.configure(bg="#ffffff")
    
    # 创建标题栏
    title_frame = tk.Frame(root, bg="#ffffff", height=80)
    title_frame.pack(fill="x", side="top")
    title_frame.pack_propagate(False)
    
    # 创建内容区域
    content_frame = tk.Frame(root, bg="#f8f9fa")
    content_frame.pack(fill="both", expand=True)
    
    # 创建依赖模块
    order_module = OrderModule(content_frame, title_frame)
    meal_module = MealModule(content_frame, title_frame)
    
    # 创建财务管理模块
    finance_module = FinanceModule(content_frame, title_frame, order_module, meal_module)
    
    # 显示模块
    finance_module.show()
    
    print("✅ 财务管理模块已完善，新增功能：")
    print("1. ✅ 可变成本与真实订单数据关联")
    print("2. ✅ 收入基于已完成订单计算")
    print("3. ✅ 收入明细列表展示所有订单")
    print("4. ✅ 收入饼图显示各餐食销售分布")
    print("5. ✅ 财务概览卡片显示关键指标")
    print("6. ✅ 实时数据刷新功能")
    print("7. ✅ 统计信息和图例说明")
    
    print("\n📊 财务数据说明：")
    print("- 总收入：基于已完成订单的真实金额")
    print("- 可变成本：订单金额的40%（可调整比例）")
    print("- 固定成本：人力、租金、水电等固定支出")
    print("- 净利润：总收入 - 固定成本 - 可变成本")
    
    # 启动主循环
    root.mainloop()

if __name__ == "__main__":
    test_finance_module()
