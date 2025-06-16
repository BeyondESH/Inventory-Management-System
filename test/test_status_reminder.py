#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试库存管理页面的选中状态文字提醒功能
"""

import tkinter as tk
import sys
import os

# 添加src路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_status_reminder_feature():
    """测试选中状态文字提醒功能"""
    print("🧪 测试库存管理页面的选中状态文字提醒功能...")
    
    try:
        from inventory_module import InventoryModule
        
        # 创建主窗口
        root = tk.Tk()
        root.title('状态文字提醒测试')
        root.geometry('1200x700')
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
        print("   🔹 顶部标题栏布局：")
        print("      - 左侧：📦 库存管理 标题")
        print("      - 中间：状态提醒文字")
        print("      - 右侧：✏️ 修改库存 和 ➕ 添加食材 按钮")
        print()
        print("   🔹 状态文字变化测试：")
        print("      1. 初始状态：'💡 点击选择食材以启用修改功能' (灰色)")
        print("      2. 选中食材：'✅ 已选中：食材名 (库存: 数量 单位)' (绿色)")
        print("      3. 取消选择：回到初始状态提示文字")
        print()
        print("   🔹 功能验证：")
        print("      - 点击不同食材，观察状态文字实时更新")
        print("      - 显示具体的食材名称和库存信息")
        print("      - 文字颜色会根据状态变化（灰色/绿色）")
        print("      - 按钮状态同步变化（禁用/启用）")
        print()
        print("   🔹 关闭窗口结束测试")
        
        # 显示库存管理模块
        inventory_module.show()
        
        # 居中显示窗口
        root.update_idletasks()
        x = (root.winfo_screenwidth() // 2) - (1200 // 2)
        y = (root.winfo_screenheight() // 2) - (700 // 2)
        root.geometry(f'1200x700+{x}+{y}')
        
        # 添加使用提示
        def show_usage_tip():
            from tkinter import messagebox
            messagebox.showinfo("使用提示", 
                              "👆 观察标题栏中间的状态提醒文字\n\n"
                              "🔸 默认状态：\n"
                              "   💡 点击选择食材以启用修改功能\n\n"
                              "🔸 选中状态：\n"
                              "   ✅ 已选中：面粉 (库存: 50 kg)\n\n"
                              "🔸 操作说明：\n"
                              "   • 点击任意食材行查看状态变化\n"
                              "   • 点击空白处取消选择\n"
                              "   • 文字颜色会自动变化")
        
        # 添加提示按钮
        tip_btn = tk.Button(title_frame, text="💬 使用提示", 
                          font=("微软雅黑", 10),
                          bg="#9b59b6", fg="white", bd=0, 
                          padx=10, pady=5, cursor="hand2",
                          command=show_usage_tip)
        tip_btn.pack(side="right", padx=(0, 10))
        
        # 运行界面
        root.mainloop()
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
    
    print("🏁 测试结束")

if __name__ == "__main__":
    test_status_reminder_feature()
