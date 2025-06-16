#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试库存管理模块的添加食材功能
"""

import tkinter as tk
import sys
import os

# 添加src路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_inventory_add_feature():
    """测试库存管理添加食材功能"""
    print("🧪 测试库存管理模块的添加食材功能...")
    
    try:
        from inventory_module import InventoryModule
        
        # 创建主窗口
        root = tk.Tk()
        root.title('库存管理测试')
        root.geometry('1000x700')
        root.configure(bg='#f7f7f7')
        
        # 创建标题框架
        title_frame = tk.Frame(root, bg="#ffffff", height=60)
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)
        
        # 创建内容框架
        content_frame = tk.Frame(root, bg="#ffffff")
        content_frame.pack(fill="both", expand=True)
        
        # 创建库存管理模块
        inventory_module = InventoryModule(content_frame, title_frame)
        
        print("✅ 库存管理模块创建成功！")
        print("📝 测试说明：")
        print("   - 点击 '➕ 添加食材' 按钮测试添加功能")
        print("   - 新的添加对话框应该包含完整的表单字段")
        print("   - 包括：食材名称、当前库存、单位、安全库存阈值、单价、过期日期")
        print("   - 支持输入验证和数据保存")
        print("   - 关闭窗口结束测试")
        
        # 显示库存管理模块
        inventory_module.show()
        
        # 居中显示窗口
        root.update_idletasks()
        x = (root.winfo_screenwidth() // 2) - (1000 // 2)
        y = (root.winfo_screenheight() // 2) - (700 // 2)
        root.geometry(f'1000x700+{x}+{y}')
        
        # 运行界面
        root.mainloop()
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
    
    print("🏁 测试结束")

if __name__ == "__main__":
    test_inventory_add_feature()
