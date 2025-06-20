#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试忘记密码页面按钮显示
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

# 添加路径
current_dir = os.path.dirname(os.path.abspath(__file__))
modern_system_dir = os.path.join(current_dir, 'modern_system')
sys.path.insert(0, current_dir)
sys.path.insert(0, modern_system_dir)
sys.path.insert(0, os.path.join(modern_system_dir, 'modules'))

def test_forgot_password_form():
    """测试忘记密码表单按钮"""
    try:
        from modern_system.modules.modern_login_module import ModernLoginModule
        
        def on_login_success(user_info):
            print(f"登录成功: {user_info}")
        
        # 创建登录模块
        app = ModernLoginModule(on_login_success)
        
        # 显示忘记密码页面
        app.show_forgot_password()
        
        print("✅ 忘记密码页面创建成功！")
        print("📋 检查事项：")
        print("  1. 确认页面中有两个按钮：'返回登录' 和 '重置密码'")
        print("  2. 检查按钮是否并列显示且大小一致")
        print("  3. 测试填写表单和按钮功能")
        print("  4. 关闭窗口结束测试")
        
        # 运行应用
        app.run()
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        messagebox.showerror("测试错误", f"测试失败: {e}")

if __name__ == "__main__":
    print("🧪 测试忘记密码页面按钮...")
    test_forgot_password_form()
