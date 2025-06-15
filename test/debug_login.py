#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试登录界面 - 检查按钮创建情况
"""

import sys
import os
import tkinter as tk

# 添加项目路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)  # 上一级目录
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.login_module import LoginModule

class DebugLoginModule(LoginModule):
    def create_login_interface(self):
        """重写登录界面创建方法，添加调试信息"""
        print("🔍 开始创建登录界面...")
        super().create_login_interface()
        
        # 检查窗口中的所有按钮
        print("🔍 检查窗口中的按钮:")
        self.check_buttons(self.root)
    
    def check_buttons(self, widget, level=0):
        """递归检查所有按钮"""
        indent = "  " * level
        if isinstance(widget, tk.Button):
            print(f"{indent}✅ 发现按钮: '{widget['text']}' - 背景色: {widget['bg']}")
        
        for child in widget.winfo_children():
            self.check_buttons(child, level + 1)

def test_debug_login():
    """测试调试版登录界面"""
    print("正在创建调试版登录界面...")
    
    def test_callback(user_manager):
        print(f"登录成功回调: {user_manager}")
    
    # 创建调试版登录界面
    login = DebugLoginModule(on_login_success=test_callback)
    login.run()

if __name__ == "__main__":
    test_debug_login()
