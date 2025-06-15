#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
食品服务公司管理系统启动器
"""

import tkinter as tk

# 支持两种导入方式：作为包导入和直接运行
try:
    from .login_module import LoginModule
    from .inventory_system import InventoryManagementSystem
except ImportError:
    from login_module import LoginModule
    from inventory_system import InventoryManagementSystem

class SystemLauncher:
    def __init__(self):
        pass
        
    def start_main_system(self, user_manager=None):
        """启动主管理系统"""
        app = InventoryManagementSystem()
        if user_manager:
            # 将用户管理器传递给主系统，以便主系统知道当前登录用户
            app.set_user_manager(user_manager)
        app.run()
        
    def run(self):
        """运行系统启动器"""
        # 创建登录模块，传入成功登录后的回调函数
        login = LoginModule(on_login_success=self.start_main_system)
        login.run()

if __name__ == "__main__":
    launcher = SystemLauncher()
    launcher.run()
