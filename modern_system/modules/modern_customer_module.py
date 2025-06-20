#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
现代化客户管理模块
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, List, Any, Optional
import datetime
import json

# 导入数据管理中心
try:
    from .data_manager import data_manager
except ImportError:
    try:
        from data_manager import data_manager
    except ImportError:
        # 模拟数据管理器
        class MockDataManager:
            def load_data(self, data_type):
                return []
            def register_module(self, module_type, instance):
                pass
        data_manager = MockDataManager()

class ModernCustomerModule:
    def __init__(self, parent_frame, title_frame):
        self.parent_frame = parent_frame
        self.title_frame = title_frame
        
        # 注册到数据管理中心
        data_manager.register_module('customer', self)
        
        # 现代化配色方案
        self.colors = {
            'primary': '#FF6B35',
            'secondary': '#F7931E',
            'success': '#00B894',
            'warning': '#FDCB6E',
            'danger': '#E74C3C',
            'info': '#3498DB',
            'background': '#F8F9FA',
            'surface': '#FFFFFF',
            'text_primary': '#2D3436',
            'text_secondary': '#636E72',
            'border': '#E1E8ED'
        }
        
        # 字体配置
        self.fonts = {
            'title': ('Microsoft YaHei UI', 16, 'bold'),
            'heading': ('Microsoft YaHei UI', 14, 'bold'),
            'body': ('Microsoft YaHei UI', 12),
            'small': ('Microsoft YaHei UI', 10)
        }
        
        self.main_frame = None
        self.customer_data = self.load_customer_data()
        
    def load_customer_data(self):
        """加载客户数据"""
        try:
            return data_manager.load_data('customers')
        except:
            return [
                {"id": "CUST001", "name": "张三", "phone": "138****1234", "address": "北京市朝阳区xxx街道1号", "total_orders": 15, "total_amount": 1580.0},
                {"id": "CUST002", "name": "李四", "phone": "139****5678", "address": "北京市海淀区xxx路88号", "total_orders": 8, "total_amount": 890.0},
                {"id": "CUST003", "name": "王五", "phone": "136****9012", "address": "北京市西城区xxx胡同66号", "total_orders": 12, "total_amount": 1250.0}
            ]
        
    def show(self):
        """显示客户管理界面"""
        if self.main_frame:
            self.main_frame.destroy()
        
        self.main_frame = tk.Frame(self.parent_frame, bg=self.colors['background'])
        self.main_frame.pack(fill="both", expand=True)
        
        # 标题
        title_label = tk.Label(self.main_frame, text="👥 客户管理", 
                              font=self.fonts['title'],
                              bg=self.colors['background'], 
                              fg=self.colors['text_primary'])
        title_label.pack(pady=(0, 20))
        
        # 客户统计
        self.create_customer_stats()
        
        # 客户列表
        self.create_customer_list()
        
    def create_customer_stats(self):
        """创建客户统计"""
        stats_frame = tk.Frame(self.main_frame, bg=self.colors['background'])
        stats_frame.pack(fill="x", pady=(0, 20))
        
        # 统计数据
        total_customers = len(self.customer_data)
        total_orders = sum(customer.get('total_orders', 0) for customer in self.customer_data)
        total_amount = sum(customer.get('total_amount', 0) for customer in self.customer_data)
        avg_amount = total_amount / total_customers if total_customers > 0 else 0
        
        stats = [
            {"title": "客户总数", "value": str(total_customers), "icon": "👥", "color": self.colors['primary']},
            {"title": "总订单数", "value": str(total_orders), "icon": "📋", "color": self.colors['info']},
            {"title": "总消费额", "value": f"￥{total_amount:.0f}", "icon": "💰", "color": self.colors['success']},
            {"title": "平均消费", "value": f"￥{avg_amount:.0f}", "icon": "📊", "color": self.colors['secondary']}
        ]
        
        for stat in stats:
            card = tk.Frame(stats_frame, bg=self.colors['surface'], relief="flat", bd=1)
            card.pack(side="left", fill="both", expand=True, padx=(0, 10))
            
            # 图标
            icon_label = tk.Label(card, text=stat['icon'], font=('Segoe UI Emoji', 24),
                                bg=self.colors['surface'], fg=stat['color'])
            icon_label.pack(pady=(10, 5))
            
            # 数值
            value_label = tk.Label(card, text=stat['value'], font=self.fonts['heading'],
                                 bg=self.colors['surface'], fg=self.colors['text_primary'])
            value_label.pack()
            
            # 标题
            title_label = tk.Label(card, text=stat['title'], font=self.fonts['body'],
                                 bg=self.colors['surface'], fg=self.colors['text_secondary'])
            title_label.pack(pady=(5, 10))
            
    def create_customer_list(self):
        """创建客户列表"""
        list_frame = tk.Frame(self.main_frame, bg=self.colors['surface'])
        list_frame.pack(fill="both", expand=True)
        
        # 表格标题
        list_title = tk.Label(list_frame, text="📋 客户列表", 
                             font=self.fonts['heading'],
                             bg=self.colors['surface'], 
                             fg=self.colors['text_primary'])
        list_title.pack(pady=10)
        
        # 创建Treeview表格
        columns = ("客户ID", "姓名", "电话", "地址", "订单数", "消费金额")
        self.customer_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        # 设置列标题
        for col in columns:
            self.customer_tree.heading(col, text=col)
            if col == "地址":
                self.customer_tree.column(col, width=200, anchor="w")
            else:
                self.customer_tree.column(col, width=120, anchor="center")
        
        # 添加客户数据
        for customer in self.customer_data:
            values = (
                customer.get('id', ''),
                customer.get('name', ''),
                customer.get('phone', ''),
                customer.get('address', ''),
                customer.get('total_orders', 0),
                f"￥{customer.get('total_amount', 0):.0f}"
            )
            self.customer_tree.insert("", "end", values=values)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.customer_tree.yview)
        self.customer_tree.configure(yscrollcommand=scrollbar.set)
        
        # 布局
        self.customer_tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y", pady=10)
