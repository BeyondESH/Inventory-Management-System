#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试库存管理页面的修改库存按钮功能
"""

import tkinter as tk
import sys
import os

# 添加src路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_edit_button_feature():
    """测试修改库存按钮功能"""
    print("🧪 测试库存管理页面的修改库存按钮功能...")
    
    try:
        from inventory_module import InventoryModule
        
        # 创建主窗口
        root = tk.Tk()
        root.title('修改库存按钮测试')
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
        print("   🔹 顶部工具栏现在有两个按钮：")
        print("      - ➕ 添加食材（绿色）")
        print("      - ✏️ 修改库存（橙色，初始禁用）")
        print()
        print("   🔹 按钮状态变化：")
        print("      - 未选中任何项目时：修改库存按钮为灰色禁用状态")
        print("      - 点击选中一个食材行时：修改库存按钮变为橙色可用状态")
        print("      - 点击空白处取消选择时：修改库存按钮又变为禁用状态")
        print()
        print("   🔹 功能测试：")
        print("      1. 点击任意食材行选中它")
        print("      2. 观察修改库存按钮变为可用")
        print("      3. 点击修改库存按钮打开编辑对话框")
        print("      4. 编辑对话框功能与双击编辑一致")
        print()
        print("   🔹 关闭窗口结束测试")
        
        # 显示库存管理模块
        inventory_module.show()
        
        # 居中显示窗口
        root.update_idletasks()
        x = (root.winfo_screenwidth() // 2) - (1000 // 2)
        y = (root.winfo_screenheight() // 2) - (700 // 2)
        root.geometry(f'1000x700+{x}+{y}')
        
        # 添加状态指示器
        status_frame = tk.Frame(title_frame, bg="#ffffff")
        status_frame.pack(side="left", padx=(50, 0))
        
        status_label = tk.Label(status_frame, text="状态：未选中任何项目", 
                              font=("微软雅黑", 10),
                              bg="#ffffff", fg="#7f8c8d")
        status_label.pack()
        
        # 重写选择事件处理以添加状态显示
        original_on_select = inventory_module.on_item_select
        def enhanced_on_select(event):
            original_on_select(event)
            selected_items = inventory_module.tree.selection()
            if selected_items:
                # 获取选中的食材名称
                item_values = inventory_module.tree.item(selected_items[0])['values']
                if item_values:
                    food_name = item_values[1]  # 食材名称在第二列
                    status_label.config(text=f"状态：已选中 '{food_name}'", fg="#27ae60")
            else:
                status_label.config(text="状态：未选中任何项目", fg="#7f8c8d")
        
        inventory_module.on_item_select = enhanced_on_select
        inventory_module.tree.bind("<<TreeviewSelect>>", enhanced_on_select)
        
        # 运行界面
        root.mainloop()
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
    
    print("🏁 测试结束")

if __name__ == "__main__":
    test_edit_button_feature()
