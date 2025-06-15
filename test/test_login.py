#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试登录界面的脚本
"""

import sys
import os

# 添加项目路径
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from src.login_module import LoginModule

def test_login():
    """测试登录界面"""
    print("正在创建登录界面...")
    
    def dummy_callback(user_manager):
        print(f"登录成功，用户管理器: {user_manager}")
        print(f"当前用户: {user_manager.current_user.username if user_manager.current_user else 'None'}")
    
    login = LoginModule(on_login_success=dummy_callback)
    print("登录界面创建完成，准备显示...")
    login.run()

if __name__ == "__main__":
    test_login()
