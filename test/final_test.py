#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终测试 - 优化后的登录界面
"""

import sys
import os

# 添加项目路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)  # 上一级目录
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.login_module import LoginModule

def final_test():
    """最终测试优化后的登录界面"""
    print("🎉 最终版登录界面测试")
    print("=" * 50)
    print("")
    print("✨ 最新优化:")
    print("   📏 窗口大小: 420x550 (紧凑)")
    print("   🖱️ 登录按钮: 12宽度 (适中)")
    print("   🎯 功能按钮: 都在黑色边框内，水平排列")
    print("   📱 按钮尺寸: 6宽度 (紧凑)")
    print("   🎨 布局: 简洁美观")
    print("")
    print("🎯 预期界面布局:")
    print("   ┌─────────────────────────┐")
    print("   │      🍽️ 系统标题        │")
    print("   │  ┌─────────────────────┐ │")
    print("   │  │   [用户名输入框]    │ │")
    print("   │  │   [密码输入框]      │ │")
    print("   │  │   [🔐 立即登录]     │ │")
    print("   │  │ [📝][👤][🧪] 按钮  │ │")
    print("   │  │    忘记密码？       │ │")
    print("   │  └─────────────────────┘ │")
    print("   └─────────────────────────┘")
    print("")
    print("🔥 功能测试:")
    print("   ✅ 点击 [👤 游客] → 直接进入主界面")
    print("   ✅ 点击 [📝 注册] → 注册页面")
    print("   ✅ 点击 [🧪 测试] → 测试模式")
    print("   ✅ 点击 [忘记密码？] → 密码重置")
    print("")
    print("🚀 启动界面...")
    
    def test_callback(user_manager):
        print("🎊 登录成功！用户管理器已传递到主系统")
        if user_manager.current_user:
            print(f"   当前用户: {user_manager.current_user.username}")
    
    login = LoginModule(on_login_success=test_callback)
    login.run()

if __name__ == "__main__":
    final_test()
