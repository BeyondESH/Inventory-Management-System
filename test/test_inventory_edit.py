#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试库存管理模块的双击编辑功能
"""

import tkinter as tk
import sys
import os

# 添加src路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_inventory_edit_feature():
    """测试库存管理双击编辑功能"""
    print("🧪 测试库存管理模块的双击编辑功能...")
    
    try:
        from inventory_module import InventoryModule
        
        # 创建主窗口
        root = tk.Tk()
        root.title('库存管理编辑测试')
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
        print("   - 双击任意食材行进行编辑")
        print("   - 编辑对话框会预填充当前食材的所有信息")
        print("   - 可以修改任何字段：名称、库存、单位、阈值、单价、过期日期")
        print("   - 支持保存修改、删除食材、取消操作")
        print("   - 包含完整的数据验证")
        print("   - 修改后会自动刷新列表显示")
        print("   - 关闭窗口结束测试")
        
        # 显示库存管理模块
        inventory_module.show()
        
        # 居中显示窗口
        root.update_idletasks()
        x = (root.winfo_screenwidth() // 2) - (1000 // 2)
        y = (root.winfo_screenheight() // 2) - (700 // 2)
        root.geometry(f'1000x700+{x}+{y}')
        
        # 添加测试提示
        def show_help():
            from tkinter import messagebox
            messagebox.showinfo("使用提示", 
                              "双击表格中的任意食材行即可进入编辑模式！\n\n"
                              "编辑功能包括：\n"
                              "• 修改食材信息\n"
                              "• 删除食材\n"
                              "• 数据验证\n"
                              "• 自动保存")
        
        # 添加帮助按钮
        help_btn = tk.Button(title_frame, text="❓ 帮助", 
                           font=("微软雅黑", 10),
                           bg="#9b59b6", fg="white", bd=0, 
                           padx=15, pady=5, cursor="hand2",
                           command=show_help)
        help_btn.pack(side="right", padx=5)
        
        # 运行界面
        root.mainloop()
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
    
    print("🏁 测试结束")

if __name__ == "__main__":
    test_inventory_edit_feature()
