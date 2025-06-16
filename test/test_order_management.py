#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试订单管理模块的完整功能
"""

import tkinter as tk
import sys
import os

# 添加src路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_order_management_features():
    """测试订单管理模块的所有功能"""
    print("🧪 测试订单管理模块的完整功能...")
    
    try:
        from order_module import OrderModule
        
        # 创建主窗口
        root = tk.Tk()
        root.title('订单管理模块功能测试')
        root.geometry('1200x800')
        root.configure(bg='#f7f7f7')
        
        # 创建标题框架
        title_frame = tk.Frame(root, bg="#ffffff", height=60)
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)
        
        # 创建内容框架
        content_frame = tk.Frame(root, bg="#ffffff")
        content_frame.pack(fill="both", expand=True)
        
        # 创建订单管理模块
        order_module = OrderModule(content_frame, title_frame)
        
        print("✅ 订单管理模块创建成功！")
        print("📝 功能测试说明：")
        print()
        print("🔹 1. 新建订单功能测试：")
        print("   - 点击 '➕ 新建订单' 按钮")
        print("   - 填写完整的订单信息（客户、餐食、数量、单价、日期、状态）")
        print("   - 支持餐食下拉选择和自定义输入")
        print("   - 自动计算总金额")
        print("   - 数据验证和保存")
        print()
        print("🔹 2. 双击编辑功能测试：")
        print("   - 双击任意订单行进入编辑模式")
        print("   - 编辑对话框预填充所有订单信息")
        print("   - 订单号为只读，其他字段可编辑")
        print("   - 支持删除订单功能")
        print()
        print("🔹 3. 选择状态提醒测试：")
        print("   - 默认状态：'💡 点击选择订单以启用修改功能'")
        print("   - 选中状态：'✅ 已选中：#订单号 客户 - 餐食 (状态)'")
        print("   - 文字颜色动态变化（灰色/绿色）")
        print()
        print("🔹 4. 修改订单按钮测试：")
        print("   - 初始状态：灰色禁用")
        print("   - 选中订单后：橙色可用")
        print("   - 点击后打开编辑对话框")
        print()
        print("🔹 5. 数据功能测试：")
        print("   - 自动生成递增订单号")
        print("   - 总金额自动计算（数量 × 单价）")
        print("   - 日期格式验证")
        print("   - 完整的数据验证机制")
        print()
        print("🔹 关闭窗口结束测试")
        
        # 显示订单管理模块
        order_module.show()
        
        # 居中显示窗口
        root.update_idletasks()
        x = (root.winfo_screenwidth() // 2) - (1200 // 2)
        y = (root.winfo_screenheight() // 2) - (800 // 2)
        root.geometry(f'1200x800+{x}+{y}')
        
        # 添加功能说明按钮
        def show_features():
            from tkinter import messagebox
            messagebox.showinfo("功能说明", 
                              "📋 订单管理模块功能完整列表：\n\n"
                              "🔸 新建订单：\n"
                              "   • 完整的表单输入\n"
                              "   • 餐食下拉选择\n"
                              "   • 自动计算总金额\n"
                              "   • 数据验证机制\n\n"
                              "🔸 编辑订单：\n"
                              "   • 双击订单行编辑\n"
                              "   • 修改订单按钮编辑\n"
                              "   • 预填充现有数据\n"
                              "   • 支持删除功能\n\n"
                              "🔸 状态管理：\n"
                              "   • 选择状态提醒\n"
                              "   • 按钮状态变化\n"
                              "   • 实时信息显示")
        
        help_btn = tk.Button(title_frame, text="📖 功能说明", 
                           font=("微软雅黑", 10),
                           bg="#9b59b6", fg="white", bd=0, 
                           padx=15, pady=5, cursor="hand2",
                           command=show_features)
        help_btn.pack(side="right", padx=5)
        
        # 运行界面
        root.mainloop()
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
    
    print("🏁 测试结束")

if __name__ == "__main__":
    test_order_management_features()
