#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
食品服务公司管理系统启动器
"""

import tkinter as tk

# 支持两种导入方式：作为包导入和直接运行
try:
    from ..modules.modern_login_module import ModernLoginModule
    from .modern_ui_system import ModernFoodServiceSystem
except ImportError:
    import sys
    import os
    # 添加模块路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    modules_dir = os.path.join(os.path.dirname(current_dir), 'modules')
    sys.path.insert(0, modules_dir)
    sys.path.insert(0, current_dir)
    from modern_login_module import ModernLoginModule
    from modern_ui_system import ModernFoodServiceSystem

class SystemLauncher:
    def __init__(self):
        pass
        
    def start_main_system(self, user_info):
        """启动主管理系统"""
        app = ModernFoodServiceSystem()
        # 传递用户信息给主系统
        if hasattr(app, 'set_user_info'):
            app.set_user_info(user_info)
        app.run()
        
    def run(self):
        """运行系统启动器"""
        # 创建登录模块，传入成功登录后的回调函数
        login = ModernLoginModule(on_login_success=self.start_main_system)
        login.run()

if __name__ == "__main__":
    launcher = SystemLauncher()
    launcher.run()
