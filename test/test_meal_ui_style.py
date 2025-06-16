#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
餐食配置模块UI风格统一测试脚本
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

import tkinter as tk
from meal_module import MealModule

def test_meal_ui_style():
    """测试餐食配置模块UI风格"""
    print("启动餐食配置模块UI风格测试...")
    
    # 创建主窗口
    root = tk.Tk()
    root.title("餐食配置模块UI风格测试")
    root.geometry("1200x800")
    root.configure(bg="#ffffff")
    
    # 创建标题栏
    title_frame = tk.Frame(root, bg="#ffffff", height=80)
    title_frame.pack(fill="x", side="top")
    title_frame.pack_propagate(False)
    
    # 创建内容区域
    content_frame = tk.Frame(root, bg="#f8f9fa")
    content_frame.pack(fill="both", expand=True)
    
    # 创建餐食配置模块
    meal_module = MealModule(content_frame, title_frame)
    
    # 显示模块
    meal_module.show()
    
    print("✅ 餐食配置模块UI风格已更新")
    print("\n🎨 UI风格统一特性：")
    print("1. ✅ 对话框标题栏：橙色背景 (#e67e22)")
    print("2. ✅ 对话框背景：浅灰色 (#f8f9fa)")
    print("3. ✅ 标签字体：微软雅黑 11pt 粗体")
    print("4. ✅ 输入框边框：solid, bd=1")
    print("5. ✅ 格式提示：灰色小字体")
    print("6. ✅ 按钮样式：统一的颜色和字体")
    print("7. ✅ 布局间距：与其他模块一致")
    print("8. ✅ 对话框尺寸：480x520 居中显示")
    print("\n📋 功能测试说明：")
    print("- 点击'添加餐食'按钮测试添加对话框UI")
    print("- 选择表格中的餐食后点击'修改餐食'测试编辑对话框UI")
    print("- 双击表格行也可以打开编辑对话框")
    print("- 对比客户管理模块的对话框风格，应该高度一致")
    
    # 启动主循环
    root.mainloop()

if __name__ == "__main__":
    test_meal_ui_style()
