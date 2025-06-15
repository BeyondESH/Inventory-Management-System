#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试修复后的登录界面高度
"""

import sys
import os

# 添加项目路径
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from src.login_module import LoginModule

def test_fixed_height():
    """测试修复高度后的登录界面"""
    print("🔧 测试修复后的登录界面（高度750px，可调整大小）...")
    
    def test_callback(user_manager):
        print("回调测试成功")
    
    login = LoginModule(on_login_success=test_callback)
    
    print("✅ 登录界面已创建，现在应该显示所有按钮:")
    print("   - 窗口高度: 750px (之前是600px)")
    print("   - 窗口可调整大小: 是")
    print("   - 应该看到5个按钮:")
    print("     1. 🔐 立即登录 (绿色)")
    print("     2. 📝 注册账户 (蓝色)")
    print("     3. 👤 游客体验 (橙色)")
    print("     4. 🧪 测试模式 (红色)")
    print("     5. 忘记密码？ (文字链接)")
    
    login.run()

if __name__ == "__main__":
    test_fixed_height()
