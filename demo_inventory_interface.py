#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
展示更新后的库存管理界面（无统计卡片）
"""

import sys
import os
import tkinter as tk

# 添加路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
sys.path.insert(0, os.path.join(current_dir, 'modern_system'))
sys.path.insert(0, os.path.join(current_dir, 'modern_system', 'modules'))

def demo_inventory_interface():
    """演示新的库存管理界面"""
    try:
        from modern_system.modules.modern_inventory_module import ModernInventoryModule
        
        # 创建演示窗口
        root = tk.Tk()
        root.title("库存管理模块 - 更新后界面")
        root.geometry("1400x900")
        root.configure(bg="#F8F9FA")
        
        # 创建框架
        title_frame = tk.Frame(root, bg="#FFFFFF", height=80)
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)
        
        main_frame = tk.Frame(root, bg="#F8F9FA")
        main_frame.pack(fill="both", expand=True)
        
        # 添加标题说明
        title_label = tk.Label(title_frame, 
                              text="📦 库存管理模块 - 已移除顶部统计卡片，直接显示可制作菜品",
                              font=('Microsoft YaHei UI', 14, 'bold'),
                              bg="#FFFFFF", fg="#2C3E50")
        title_label.pack(expand=True)
        
        # 创建库存管理模块
        inventory_module = ModernInventoryModule(main_frame, title_frame)
        
        print("=== 库存管理界面更新说明 ===")
        print("✅ 已移除顶部4个统计卡片（商品总数、库存不足、库存总值、缺货商品）")
        print("✅ 界面现在直接从'可制作菜品数量'区域开始")
        print("✅ 更简洁的界面布局，重点突出可制作菜品信息")
        print("✅ 食材库存清单仍保持完整功能")
        print("\n正在显示更新后的库存管理界面...")
        
        # 显示界面
        inventory_module.show()
        
        # 运行界面
        root.mainloop()
        
    except Exception as e:
        print(f"演示失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    demo_inventory_interface()
