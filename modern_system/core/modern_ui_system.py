#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
现代化食品服务管理系统界面
采用现代化设计风格的图形界面管理系统
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import os
import datetime
from typing import Dict, List, Any
import json

# 导入各个模块
try:
    from ..modules.modern_sales_module import ModernSalesModule
    from ..modules.modern_inventory_module import ModernInventoryModule
    from ..modules.modern_meal_module import ModernMealModule
    from ..modules.modern_order_module import ModernOrderModule
    from ..modules.modern_customer_module import ModernCustomerModule
    from ..modules.modern_finance_module import ModernFinanceModule
    from ..modules.modern_employee_module import ModernEmployeeModule
    from ..ui.meituan_charts_module import ModernChartsModule
    from ..utils.data_manager import data_manager
except ImportError:
    import sys
    import os
    # 添加模块路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    modules_dir = os.path.join(os.path.dirname(current_dir), 'modules')
    ui_dir = os.path.join(os.path.dirname(current_dir), 'ui')
    utils_dir = os.path.join(os.path.dirname(current_dir), 'utils')
    sys.path.insert(0, modules_dir)
    sys.path.insert(0, ui_dir)
    sys.path.insert(0, utils_dir)
    
    try:
        from modern_sales_module import ModernSalesModule
        from modern_inventory_module import ModernInventoryModule
        from modern_meal_module import ModernMealModule
        from modern_order_module import ModernOrderModule
        from modern_customer_module import ModernCustomerModule
        from modern_finance_module import ModernFinanceModule
        from modern_employee_module import ModernEmployeeModule
        from meituan_charts_module import ModernChartsModule
        from data_manager import data_manager
    except ImportError as e:
        print(f"导入模块失败: {e}")
        # 创建简单的模拟类
        class MockModule:
            def __init__(self, *args, **kwargs):
                pass
            def show(self):
                pass
        
        ModernSalesModule = MockModule
        ModernInventoryModule = MockModule
        ModernMealModule = MockModule
        ModernOrderModule = MockModule
        ModernCustomerModule = MockModule
        ModernFinanceModule = MockModule
        ModernEmployeeModule = MockModule
        ModernChartsModule = MockModule
        
        class MockDataManager:
            def get_dashboard_stats(self):
                return {
                    'today_sales': 12580,
                    'order_count': 156,
                    'inventory_alerts': 8,
                    'customer_count': 2340
                }
        data_manager = MockDataManager()

class ModernFoodServiceSystem:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("智慧餐饮管理系统")
        self.root.geometry("1400x900")
        self.root.configure(bg="#f8f9fa")
        self.root.resizable(True, True)
        
        # 现代化颜色主题
        self.colors = {
            'primary': '#FF6B35',      # 主色调 - 橙红色
            'secondary': '#F7931E',    # 次色调 - 橙色
            'accent': '#FFD23F',       # 强调色 - 黄色
            'background': '#F8F9FA',   # 背景色
            'surface': '#FFFFFF',      # 卡片背景
            'text_primary': '#2D3436', # 主文字
            'text_secondary': '#636E72', # 次文字
            'success': '#00B894',      # 成功色
            'warning': '#FDCB6E',      # 警告色
            'error': '#E84393',        # 错误色
            'border': '#E0E0E0',       # 边框
            'sidebar': '#2D3436',      # 侧边栏背景
            'nav_hover': '#636E72'     # 导航悬停
        }
        
        # 字体配置
        self.fonts = {
            'title': ('Microsoft YaHei UI', 18, 'bold'),
            'heading': ('Microsoft YaHei UI', 14, 'bold'),
            'body': ('Microsoft YaHei UI', 12),
            'small': ('Microsoft YaHei UI', 10),
            'nav': ('Microsoft YaHei UI', 13, 'bold')        }
        
        # 当前模块
        self.current_module = "sales"
        
        # 模块定义（移除仪表盘）
        self.modules = {
            "sales": {"text": "销售管理", "icon": "💰"},
            "inventory": {"text": "库存管理", "icon": "📦"},
            "meal": {"text": "菜品管理", "icon": "🍽️"},
            "order": {"text": "订单管理", "icon": "📋"},
            "customer": {"text": "客户管理", "icon": "👥"},
            "employee": {"text": "员工管理", "icon": "👤"},
            "finance": {"text": "财务管理", "icon": "💼"},
            "charts": {"text": "数据图表", "icon": "📈"}
        }
        
        # 初始化界面
        self.setup_window()
        self.create_modern_layout()
        self.create_modern_widgets()
        self.init_modules()
        self.update_content_area()
        
    def setup_window(self):
        """设置窗口属性"""
        # 设置图标
        try:
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            icon_path = os.path.join(project_root, "image", "icon", "main.ico")
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except:
            pass
    
    def create_modern_layout(self):
        """创建现代化布局"""
        # 主容器
        self.main_container = tk.Frame(self.root, bg=self.colors['background'])
        self.main_container.pack(fill="both", expand=True, padx=0, pady=0)
        
        # 顶部导航栏
        self.top_nav = tk.Frame(self.main_container, bg=self.colors['surface'], height=70)
        self.top_nav.pack(fill="x", side="top")
        self.top_nav.pack_propagate(False)
        
        # 主内容区域
        self.content_container = tk.Frame(self.main_container, bg=self.colors['background'])
        self.content_container.pack(fill="both", expand=True)
        
        # 左侧导航面板
        self.sidebar = tk.Frame(self.content_container, bg=self.colors['sidebar'], width=280)
        self.sidebar.pack(side="left", fill="y", padx=(0, 0))
        self.sidebar.pack_propagate(False)
        
        # 右侧内容区域
        self.main_content = tk.Frame(self.content_container, bg=self.colors['background'])
        self.main_content.pack(side="right", fill="both", expand=True, padx=(20, 20), pady=(20, 20))
        
    def create_modern_widgets(self):
        """创建现代化界面元素"""
        self.create_top_navigation()
        self.create_sidebar_navigation()
        self.create_content_area()
        
    def create_top_navigation(self):
        """创建顶部导航栏"""
        # 左侧logo和标题
        logo_frame = tk.Frame(self.top_nav, bg=self.colors['surface'])
        logo_frame.pack(side="left", fill="y", padx=20)
        
        # 系统图标
        icon_label = tk.Label(logo_frame, text="🍽️", font=('Segoe UI Emoji', 24), 
                             bg=self.colors['surface'], fg=self.colors['primary'])
        icon_label.pack(side="left", padx=(0, 10), pady=15)
        
        # 系统标题
        title_label = tk.Label(logo_frame, text="智慧餐饮", font=self.fonts['title'], 
                              bg=self.colors['surface'], fg=self.colors['text_primary'])
        title_label.pack(side="left", pady=15)
        
        # 右侧用户信息
        user_frame = tk.Frame(self.top_nav, bg=self.colors['surface'])
        user_frame.pack(side="right", fill="y", padx=20)
        
        # 当前时间
        time_label = tk.Label(user_frame, text=datetime.datetime.now().strftime("%H:%M"),
                             font=self.fonts['body'], bg=self.colors['surface'], 
                             fg=self.colors['text_secondary'])
        time_label.pack(side="right", padx=(10, 0), pady=15)
        
        # 用户信息
        user_label = tk.Label(user_frame, text="👤 管理员", font=self.fonts['body'],
                             bg=self.colors['surface'], fg=self.colors['text_primary'])
        user_label.pack(side="right", pady=15)
        
    def create_sidebar_navigation(self):
        """创建侧边栏导航"""
        # 导航标题
        nav_title = tk.Label(self.sidebar, text="系统导航", font=self.fonts['heading'],
                           bg=self.colors['sidebar'], fg='white', pady=20)
        nav_title.pack(fill="x")
        
        # 导航按钮容器
        self.nav_buttons = {}
        
        for module_id, module_info in self.modules.items():
            btn_frame = tk.Frame(self.sidebar, bg=self.colors['sidebar'])
            btn_frame.pack(fill="x", padx=10, pady=2)
            
            # 创建导航按钮 - 修复anchor为center实现居中
            btn = tk.Button(btn_frame, 
                          text=f"{module_info['icon']} {module_info['text']}",
                          font=self.fonts['nav'],
                          bg=self.colors['sidebar'] if module_id != self.current_module else self.colors['primary'],
                          fg='white',
                          bd=0,
                          pady=12,
                          cursor="hand2",
                          anchor="center",  # 修复为center实现按钮内容居中
                          command=lambda mid=module_id: self.switch_module(mid))
            btn.pack(fill="x")
            
            # 悬停效果
            def on_enter(e, button=btn, mid=module_id):
                if mid != self.current_module:
                    button.configure(bg=self.colors['nav_hover'])
            
            def on_leave(e, button=btn, mid=module_id):
                if mid != self.current_module:
                    button.configure(bg=self.colors['sidebar'])
            
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)
            
            self.nav_buttons[module_id] = btn
            
    def create_content_area(self):
        """创建内容区域"""
        # 内容头部
        self.content_header = tk.Frame(self.main_content, bg=self.colors['surface'], height=80)
        self.content_header.pack(fill="x", pady=(0, 20))
        self.content_header.pack_propagate(False)
        
        # 面包屑导航
        breadcrumb_frame = tk.Frame(self.content_header, bg=self.colors['surface'])
        breadcrumb_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        
        self.breadcrumb_label = tk.Label(breadcrumb_frame, text="首页 / 仪表盘", 
                                  font=self.fonts['body'], bg=self.colors['surface'],
                                  fg=self.colors['text_secondary'])
        self.breadcrumb_label.pack(side="left")
        
        # 主内容框架
        self.main_content_frame = tk.Frame(self.main_content, bg=self.colors['background'])
        self.main_content_frame.pack(fill="both", expand=True)
        
    def switch_module(self, module_id):
        """切换模块"""
        # 更新当前模块
        old_module = self.current_module
        self.current_module = module_id
          # 更新导航按钮样式
        if old_module in self.nav_buttons:
            self.nav_buttons[old_module].configure(bg=self.colors['sidebar'])
        
        if module_id in self.nav_buttons:
            self.nav_buttons[module_id].configure(bg=self.colors['primary'])
        
        # 更新面包屑
        self.update_breadcrumb()
        
        # 更新内容区域
        self.update_content_area()
        
    def update_breadcrumb(self):
        """更新面包屑导航"""
        if self.current_module in self.modules:
            module_info = self.modules[self.current_module]
            breadcrumb_text = f"首页 / {module_info['text']}"
            
            # 查找并更新面包屑标签
            try:
                for widget in self.content_header.winfo_children():
                    if isinstance(widget, tk.Frame):
                        for child in widget.winfo_children():
                            if isinstance(child, tk.Label) and hasattr(child, 'cget'):
                                try:
                                    current_text = child.cget("text")
                                    if "首页" in current_text:
                                        child.configure(text=breadcrumb_text)
                                        break
                                except tk.TclError:
                                    # Widget已被销毁，跳过
                                    continue
            except tk.TclError:
                # 如果widget已被销毁，忽略错误
                pass
        
    def init_modules(self):
        """初始化各个模块"""
        try:
            # 初始化各个业务模块
            self.inventory_module = ModernInventoryModule(self.main_content_frame, self.content_header)
            self.meal_module = ModernMealModule(self.main_content_frame, self.content_header)
            self.customer_module = ModernCustomerModule(self.main_content_frame, self.content_header)
            self.order_module = ModernOrderModule(self.main_content_frame, self.content_header, 
                                          self.inventory_module, self.customer_module)
            self.sales_module = ModernSalesModule(self.main_content_frame, self.content_header, 
                                          self.meal_module, self.inventory_module, self.order_module)
            self.employee_module = ModernEmployeeModule(self.main_content_frame, self.content_header)
            self.finance_module = ModernFinanceModule(self.main_content_frame, self.content_header, 
                                              self.order_module, self.employee_module)
            self.charts_module = ModernChartsModule(self.main_content_frame, self.content_header)
        except Exception as e:
            print(f"初始化模块失败: {e}")
            # 创建模拟模块
            class MockModule:
                def show(self):
                    print("模拟模块显示")
            
            self.inventory_module = MockModule()
            self.meal_module = MockModule()
            self.customer_module = MockModule()
            self.order_module = MockModule()
            self.sales_module = MockModule()
            self.employee_module = MockModule()
            self.finance_module = MockModule()
            self.charts_module = MockModule()
    
    def update_content_area(self):
        """更新内容区域"""
        # 清空当前内容
        for widget in self.main_content_frame.winfo_children():
            widget.pack_forget()
        
        # 根据选中模块显示相应内容
        try:
            if self.current_module == "sales":
                self.sales_module.show()
            elif self.current_module == "inventory":
                self.inventory_module.show()
            elif self.current_module == "meal":
                self.meal_module.show()
            elif self.current_module == "order":
                self.order_module.show()
            elif self.current_module == "customer":
                self.customer_module.show()
            elif self.current_module == "employee":
                self.employee_module.show()
            elif self.current_module == "finance":
                self.finance_module.show()
            elif self.current_module == "charts":
                self.charts_module.show()
            else:
                # 默认显示销售管理
                self.sales_module.show()
        except Exception as e:
            print(f"显示模块失败: {e}")
            # 出错时也显示销售管理
            try:
                self.sales_module.show()
            except:
                print("无法显示任何模块")
    
    def show_dashboard(self):
        """显示仪表盘"""
        # 创建仪表盘内容
        dashboard_frame = tk.Frame(self.main_content_frame, bg=self.colors['background'])
        dashboard_frame.pack(fill="both", expand=True)
        
        # 欢迎信息
        welcome_frame = tk.Frame(dashboard_frame, bg=self.colors['surface'], 
                               relief="flat", bd=1)
        welcome_frame.pack(fill="x", pady=(0, 20))
        
        welcome_label = tk.Label(welcome_frame, 
                               text="🎉 欢迎使用智慧餐饮管理系统",
                               font=self.fonts['title'], 
                               bg=self.colors['surface'],
                               fg=self.colors['text_primary'],
                               pady=30)
        welcome_label.pack()
        
        # 统计卡片容器 - 修改为2行2列布局
        stats_container = tk.Frame(dashboard_frame, bg=self.colors['background'])
        stats_container.pack(fill="x", pady=(0, 20))
        
        # 第一行卡片
        stats_row1 = tk.Frame(stats_container, bg=self.colors['background'])
        stats_row1.pack(fill="x", pady=(0, 10))
          # 第二行卡片
        stats_row2 = tk.Frame(stats_container, bg=self.colors['background'])
        stats_row2.pack(fill="x")
        
        # 从数据管理中心获取统计数据
        try:
            stats_data = data_manager.get_dashboard_stats()
        except:
            # 默认统计数据
            stats_data = {
                'today_revenue': 12580,
                'today_orders': 156,
                'low_stock_count': 8,
                'total_customers': 2340
            }
        
        # 统计卡片配置
        stats = [
            {"title": "今日销售", "value": f"￥{stats_data['today_revenue']:,.2f}", "icon": "💰", "color": self.colors['success']},
            {"title": "订单数量", "value": str(stats_data['today_orders']), "icon": "📋", "color": self.colors['primary']},
            {"title": "库存预警", "value": str(stats_data['low_stock_count']), "icon": "⚠️", "color": self.colors['warning']},
            {"title": "客户总数", "value": f"{stats_data['total_customers']:,}", "icon": "👥", "color": self.colors['secondary']}
        ]
        
        # 创建统计卡片 - 2行2列
        for i, stat in enumerate(stats):
            # 选择放置的行
            parent_row = stats_row1 if i < 2 else stats_row2
            
            card = tk.Frame(parent_row, bg=self.colors['surface'], 
                          relief="flat", bd=1, width=300, height=120)
            card.pack(side="left", padx=(0, 20) if i % 2 == 0 else 0, 
                     fill="both", expand=True)
            card.pack_propagate(False)
            
            # 图标
            icon_label = tk.Label(card, text=stat['icon'], font=('Segoe UI Emoji', 32),
                                bg=self.colors['surface'], fg=stat['color'])
            icon_label.pack(pady=(15, 5))
            
            # 数值
            value_label = tk.Label(card, text=stat['value'], font=self.fonts['heading'],
                                 bg=self.colors['surface'], fg=self.colors['text_primary'])
            value_label.pack()
            
            # 标题
            title_label = tk.Label(card, text=stat['title'], font=self.fonts['body'],
                                 bg=self.colors['surface'], fg=self.colors['text_secondary'])
            title_label.pack(pady=(5, 15))
        
        # 快速操作
        actions_frame = tk.Frame(dashboard_frame, bg=self.colors['background'])
        actions_frame.pack(fill="x")
        
        actions_title = tk.Label(actions_frame, text="快速操作", font=self.fonts['heading'],
                               bg=self.colors['background'], fg=self.colors['text_primary'])
        actions_title.pack(anchor="w", pady=(0, 10))
        
        # 操作按钮
        actions_container = tk.Frame(actions_frame, bg=self.colors['background'])
        actions_container.pack(fill="x")
        
        actions = [
            {"text": "📝 新建订单", "module": "order"},
            {"text": "🍽️ 管理菜品", "module": "meal"},
            {"text": "📦 查看库存", "module": "inventory"},
            {"text": "📊 查看报表", "module": "charts"}
        ]
        
        for action in actions:
            btn = tk.Button(actions_container, text=action['text'], 
                          font=self.fonts['body'], bg=self.colors['primary'],
                          fg='white', bd=0, pady=10, padx=20, cursor="hand2",
                          command=lambda m=action['module']: self.switch_module(m))
            btn.pack(side="left", padx=(0, 10))
    
    def run(self):
        """运行系统"""
        try:
            self.root.mainloop()
        except Exception as e:
            print(f"运行系统时出错: {e}")

def main():
    """主函数"""
    app = ModernFoodServiceSystem()
    app.run()

if __name__ == "__main__":
    main()
