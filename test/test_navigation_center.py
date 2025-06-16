#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试主界面左侧导航栏模块文字水平居中效果
"""

import tkinter as tk
import sys
import os

# 添加src路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_navigation_center():
    """测试导航栏文字居中效果"""
    print("🧪 测试主界面导航栏文字居中...")
    
    try:
        from inventory_system import InventoryManagementSystem
        
        # 创建主系统实例
        app = InventoryManagementSystem()
        
        print("✅ 主界面创建成功！")
        print("📝 测试说明：")
        print("   - 左侧导航栏的模块文字应该水平居中显示")
        print("   - 包括：📦 库存管理、🍜 餐食配置、📋 订单管理、👥 客户管理、💰 财务管理")
        print("   - 关闭窗口结束测试")
        
        # 居中显示窗口
        app.root.update_idletasks()
        x = (app.root.winfo_screenwidth() // 2) - (1200 // 2)
        y = (app.root.winfo_screenheight() // 2) - (800 // 2)
        app.root.geometry(f'1200x800+{x}+{y}')
        
        # 运行界面
        app.run()
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
    
    print("🏁 测试结束")

if __name__ == "__main__":
    test_navigation_center()
