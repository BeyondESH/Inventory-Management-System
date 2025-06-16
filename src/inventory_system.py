#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
食品服务公司库存、订单与预算管理系统
基于tkinter的图形界面管理系统
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import os
import datetime
from typing import Dict, List, Any

# 导入各个模块
try:
    from .inventory_module import InventoryModule
    from .meal_module import MealModule
    from .order_module import OrderModule
    from .customer_module import CustomerModule
    from .finance_module import FinanceModule
except ImportError:
    from inventory_module import InventoryModule
    from meal_module import MealModule
    from order_module import OrderModule
    from customer_module import CustomerModule
    from finance_module import FinanceModule

class InventoryManagementSystem:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("食品服务公司管理系统")
        self.root.geometry("1200x800")
        self.root.configure(bg="#f7f7f7")
        self.root.resizable(True, True)
        
        # 用户管理器（将从登录模块传入）
        self.user_manager = None
        
        # 设置窗口图标
        self.set_window_icon()
        
        # 当前选中的模块
        self.current_module = None
        
        # 创建主界面布局
        self.create_main_layout()
        
        # 创建界面元素
        self.create_widgets()        
        # 初始化各个模块
        self.init_modules()
        
        # 默认选择库存管理模块
        self.select_module("inventory")
        
    def set_window_icon(self):
        """设置窗口图标"""
        try:
            # 获取项目根目录的image文件夹路径
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(current_dir)
            icon_path = os.path.join(project_root, "image", "icon", "main.ico")
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except:
            pass
    
    def init_modules(self):
        """初始化各个模块"""        # 初始化各个业务模块
        self.inventory_module = InventoryModule(self.main_content_frame, self.title_frame)
        self.meal_module = MealModule(self.main_content_frame, self.title_frame)
        self.order_module = OrderModule(self.main_content_frame, self.title_frame)
        self.customer_module = CustomerModule(self.main_content_frame, self.title_frame)
        # 财务模块需要访问订单和餐食数据
        self.finance_module = FinanceModule(self.main_content_frame, self.title_frame, 
                                          self.order_module, self.meal_module)
        
    def create_main_layout(self):
        """创建主布局"""
        # 主容器
        self.main_frame = tk.Frame(self.root, bg="#f7f7f7")
        self.main_frame.pack(fill="both", expand=True)
        
        # 左侧导航栏 - 改为管理系统导航
        self.nav_frame = tk.Frame(self.main_frame, bg="#2c3e50", width=200)
        self.nav_frame.pack(side="left", fill="y")
        self.nav_frame.pack_propagate(False)
        
        # 右侧内容区域
        self.content_frame = tk.Frame(self.main_frame, bg="#ffffff")
        self.content_frame.pack(side="right", fill="both", expand=True)
        
    def create_widgets(self):
        """创建界面元素"""
        self.create_navigation()
        self.create_content_area()
        
    def create_navigation(self):
        """创建左侧导航栏"""
        # 系统标题
        title_frame = tk.Frame(self.nav_frame, bg="#34495e", height=80)
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)
        
        system_title = tk.Label(title_frame, text="管理系统", font=("微软雅黑", 16, "bold"), 
                              bg="#34495e", fg="white")
        system_title.pack(pady=20)
        
        # 导航按钮
        nav_buttons = [
            {"text": "📦 库存管理", "module": "inventory", "icon": "📦"},
            {"text": "🍜 餐食配置", "module": "meal", "icon": "🍜"},
            {"text": "📋 订单管理", "module": "order", "icon": "📋"},
            {"text": "👥 客户管理", "module": "customer", "icon": "👥"},
            {"text": "💰 财务管理", "module": "finance", "icon": "💰"},
        ]

        self.nav_buttons = {}
        for btn_info in nav_buttons:
            btn_frame = tk.Frame(self.nav_frame, bg="#2c3e50")
            btn_frame.pack(fill="x", pady=2)
            
            btn = tk.Button(btn_frame, text=btn_info["text"], font=("微软雅黑", 12),
                          bg="#2c3e50", fg="#ecf0f1", bd=0, padx=40, pady=15,
                          activebackground="#3498db", cursor="hand2", anchor="w",
                          command=lambda m=btn_info["module"]: self.select_module(m))
            btn.pack(fill="x")
            
            self.nav_buttons[btn_info["module"]] = btn

        # 底部信息
        info_frame = tk.Frame(self.nav_frame, bg="#2c3e50")
        info_frame.pack(side="bottom", fill="x", pady=20)
        
        # 用户信息显示
        user_frame = tk.Frame(info_frame, bg="#34495e")
        user_frame.pack(fill="x", pady=(0, 10))
        
        self.user_label = tk.Label(user_frame, text="未登录", font=("微软雅黑", 10, "bold"),
                                  bg="#34495e", fg="#e74c3c", pady=5)
        self.user_label.pack()
        
        # 更新用户信息显示
        self.update_user_info()
        
        current_time = datetime.datetime.now().strftime("%Y-%m-%d")
        time_label = tk.Label(info_frame, text=f"今日：{current_time}", font=("微软雅黑", 9),
                            bg="#2c3e50", fg="#95a5a6")
        time_label.pack(pady=5)
        
    def create_content_area(self):
        """创建右侧内容区域"""
        # 顶部标题栏
        self.title_frame = tk.Frame(self.content_frame, bg="#ffffff", height=60)
        self.title_frame.pack(fill="x")
        self.title_frame.pack_propagate(False)
        
        # 分割线
        separator = tk.Frame(self.content_frame, bg="#e0e0e0", height=1)
        separator.pack(fill="x")
        
        # 主内容区域
        self.main_content_frame = tk.Frame(self.content_frame, bg="#ffffff")
        self.main_content_frame.pack(fill="both", expand=True)
        
    def select_module(self, module_name):
        """选择模块"""
        # 重置所有按钮样式
        for btn in self.nav_buttons.values():
            btn.configure(bg="#2c3e50", fg="#ecf0f1")
        
        # 设置选中按钮样式
        if module_name in self.nav_buttons:
            self.nav_buttons[module_name].configure(bg="#3498db", fg="white")
        
        self.current_module = module_name
        self.update_content_area()
        
    def update_content_area(self):
        """更新内容区域"""
        # 根据选中模块显示相应内容
        if self.current_module == "inventory":
            self.inventory_module.show()
        elif self.current_module == "meal":
            self.meal_module.show()
        elif self.current_module == "order":
            self.order_module.show()
        elif self.current_module == "customer":
            self.customer_module.show()
        elif self.current_module == "finance":
            self.finance_module.show()
    
    def set_user_manager(self, user_manager):
        """设置用户管理器"""
        self.user_manager = user_manager
        self.update_user_info()
    
    def update_user_info(self):
        """更新用户信息显示"""
        if hasattr(self, 'user_label'):
            if self.user_manager and self.user_manager.current_user:
                user = self.user_manager.current_user
                if user.username == "游客":
                    self.user_label.configure(text="👤 游客模式", fg="#f39c12")
                else:
                    self.user_label.configure(text=f"👤 {user.username}", fg="#27ae60")
            else:
                self.user_label.configure(text="未登录", fg="#e74c3c")
    
    def run(self):
        """运行应用程序"""
        print("正在启动食品服务公司管理系统...")
        self.root.mainloop()

if __name__ == "__main__":
    app = InventoryManagementSystem()
    app.run()
