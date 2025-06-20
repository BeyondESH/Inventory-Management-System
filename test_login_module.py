#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
登录模块测试脚本
专门测试注册和忘记密码页面的按钮显示
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

# 添加项目路径
current_dir = os.path.dirname(os.path.abspath(__file__))
modern_system_dir = os.path.join(current_dir, 'modern_system')
sys.path.insert(0, current_dir)
sys.path.insert(0, modern_system_dir)
sys.path.insert(0, os.path.join(modern_system_dir, 'modules'))

def test_login_module():
    """测试登录模块"""
    try:
        print("🧪 测试登录模块...")
        
        # 导入登录模块
        from modern_system.modules.modern_login_module import ModernLoginModule
        
        def test_callback(user_info):
            print(f"✅ 登录成功回调测试通过: {user_info['name']}")
            messagebox.showinfo("测试成功", f"登录成功！用户: {user_info['name']}")
        
        # 创建登录应用
        login_app = ModernLoginModule(test_callback)
        
        print("✅ 登录模块创建成功！")
        print("📋 测试说明：")
        print("  1. 点击'注册账户'按钮，检查注册页面两个按钮是否正常显示")
        print("  2. 点击'忘记密码'按钮，检查忘记密码页面两个按钮是否正常显示")
        print("  3. 测试各种表单操作和按钮功能")
        
        # 显示测试提示
        messagebox.showinfo("登录模块测试", 
                           "🔍 登录模块功能测试\n\n"
                           "请测试以下功能：\n"
                           "• 点击'注册账户'检查按钮显示\n"
                           "• 点击'忘记密码'检查按钮显示\n"
                           "• 测试表单输入和提交\n"
                           "• 检查按钮样式和响应\n\n"
                           "默认登录账户：\n"
                           "用户名: admin\n"
                           "密码: admin123")
        
        # 运行登录界面
        login_app.run()
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        messagebox.showerror("测试失败", f"无法加载登录模块: {e}")

if __name__ == "__main__":
    test_login_module()
