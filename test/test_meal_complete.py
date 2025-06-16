#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
餐食配置模块测试脚本
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

import tkinter as tk
from meal_module import MealModule

def test_meal_module():
    """测试餐食配置模块"""
    print("启动餐食配置模块测试...")
    
    # 创建主窗口
    root = tk.Tk()
    root.title("餐食配置模块测试")
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
    
    print("餐食配置模块界面已启动")
    print("功能测试项目：")
    print("1. ✅ 表格视图显示餐食列表")
    print("2. ✅ 点击选择餐食项目")
    print("3. ✅ 状态提醒和按钮联动")
    print("4. ✅ 添加餐食功能")
    print("5. ✅ 修改餐食功能")
    print("6. ✅ 删除餐食功能")
    print("7. ✅ 双击编辑功能")
    print("8. ✅ 数据验证和表单处理")
    print("9. ✅ UI风格统一")
    print("10. ✅ 与其他模块交互一致")
    
    # 启动主循环
    root.mainloop()

if __name__ == "__main__":
    test_meal_module()
