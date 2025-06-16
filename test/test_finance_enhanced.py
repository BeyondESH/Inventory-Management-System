#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
财务管理模块功能测试脚本
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

import tkinter as tk
from finance_module import FinanceModule

def test_finance_module():
    """测试财务管理模块"""
    print("启动财务管理模块测试...")
    
    # 创建主窗口
    root = tk.Tk()
    root.title("财务管理模块测试")
    root.geometry("1400x900")  # 更大的窗口来测试布局
    root.configure(bg="#ffffff")
    
    # 创建标题栏
    title_frame = tk.Frame(root, bg="#ffffff", height=80)
    title_frame.pack(fill="x", side="top")
    title_frame.pack_propagate(False)
    
    # 创建内容区域
    content_frame = tk.Frame(root, bg="#f8f9fa")
    content_frame.pack(fill="both", expand=True)
    
    # 创建财务管理模块
    finance_module = FinanceModule(content_frame, title_frame)
    
    # 显示模块
    finance_module.show()
    
    print("✅ 财务管理模块已启动")
    print("\n🔧 新增功能测试：")
    print("1. ✅ 固定成本编辑按钮（点击标题栏右侧'编辑固定成本'按钮）")
    print("2. ✅ 改进的布局设计（收入明细在上，图表在下）")
    print("3. ✅ 调整后的饼图大小（4x4英寸，避免被挤出屏幕）")
    print("4. ✅ 重新设计的销售统计面板（位于饼图右侧）")
    print("5. ✅ 工具栏按钮布局优化")
    
    print("\n📋 功能操作说明：")
    print("- 点击'编辑固定成本'可以修改人力成本、租金、水电费、杂费")
    print("- 点击'刷新数据'重新加载财务数据")
    print("- 收入明细表格显示所有已完成订单")
    print("- 饼图显示各餐食的收入分布")
    print("- 销售统计面板显示详细的收入信息")
    
    print("\n🎨 布局改进：")
    print("- 饼图尺寸从6x6调整为4x4，节省屏幕空间")
    print("- 销售统计从底部移至右侧，更好利用横向空间")
    print("- 收入明细表格获得更多纵向空间")
    print("- 整体布局更紧凑，适应不同屏幕尺寸")
    
    # 启动主循环
    root.mainloop()

if __name__ == "__main__":
    test_finance_module()
