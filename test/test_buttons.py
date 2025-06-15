#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试登录界面按钮显示
"""

import sys
import os

# 添加项目路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)  # 上一级目录
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.login_module import LoginModule

def test_login_buttons():
    """测试登录界面按钮"""
    print("正在创建登录界面...")
    
    def test_callback(user_manager):
        print(f"登录成功回调: {user_manager}")
    
    # 创建登录界面
    login = LoginModule(on_login_success=test_callback)
    
    # 检查界面状态
    print(f"当前界面状态: {login.current_view}")
    print("窗口创建完成，应该显示以下按钮:")
    print("1. 🔐 立即登录 (绿色)")
    print("2. 📝 注册账户 (蓝色)")
    print("3. 👤 游客体验 (橙色)")
    print("4. 🧪 测试模式 (红色)")
    print("5. 忘记密码？ (文字链接)")
    
    login.run()

if __name__ == "__main__":
    test_login_buttons()
