#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试优化后的登录界面 - 按钮尺寸和排布
"""

import sys
import os

# 添加项目路径
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from src.login_module import LoginModule

def test_optimized_ui():
    """测试优化后的UI"""
    print("🎨 测试优化后的登录界面...")
    print("")
    print("✨ UI 优化改进:")
    print("   - 窗口尺寸: 420x650 (更紧凑)")
    print("   - 主登录按钮: 更小更精致 (18宽度)")
    print("   - 功能按钮: 更小更紧凑 (10-22宽度)")
    print("   - 字体大小: 适中 (10-14px)")
    print("   - 间距: 更紧凑的布局")
    print("   - 按钮高度: 减小padding")
    print("")
    print("🎯 现在应该看到更美观的界面，包括:")
    print("   1. 🔐 立即登录 (绿色，适中大小)")
    print("   2. 📝 注册账户 (蓝色，紧凑)")
    print("   3. 👤 游客体验 (橙色，紧凑)")
    print("   4. 🧪 测试模式 (红色，中等)")
    print("   5. 忘记密码？ (小文字链接)")
    print("")
    
    def test_callback(user_manager):
        print("登录成功回调测试")
    
    login = LoginModule(on_login_success=test_callback)
    login.run()

if __name__ == "__main__":
    test_optimized_ui()
