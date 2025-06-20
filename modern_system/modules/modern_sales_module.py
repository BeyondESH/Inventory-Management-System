#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
现代化销售管理模块
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
            def get_sales_data(self):
                return []
            def register_module(self, module_type, instance):
                pass
        data_manager = MockDataManager()

class ModernSalesModule:
    def __init__(self, parent_frame, title_frame, meal_module=None, inventory_module=None, order_module=None):
        self.parent_frame = parent_frame
        self.title_frame = title_frame
        self.meal_module = meal_module
        self.inventory_module = inventory_module
        self.order_module = order_module
        
        # 注册到数据管理中心
        data_manager.register_module('sales', self)
        
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
        
    def show(self):
        """显示销售管理界面"""
        if self.main_frame:
            self.main_frame.destroy()
        
        self.main_frame = tk.Frame(self.parent_frame, bg=self.colors['background'])
        self.main_frame.pack(fill="both", expand=True)
        
        # 标题
        title_label = tk.Label(self.main_frame, text="💰 销售管理", 
                              font=self.fonts['title'],
                              bg=self.colors['background'], 
                              fg=self.colors['text_primary'])
        title_label.pack(pady=(0, 20))
        
        # 销售统计卡片
        self.create_sales_stats()
        
        # 销售记录表格
        self.create_sales_table()
        
    def create_sales_stats(self):
        """创建销售统计卡片"""
        stats_frame = tk.Frame(self.main_frame, bg=self.colors['background'])
        stats_frame.pack(fill="x", pady=(0, 20))
        
        # 统计数据
        stats = [
            {"title": "今日销售额", "value": "￥2,580", "icon": "💰", "color": self.colors['success']},
            {"title": "本月销售额", "value": "￥58,960", "icon": "📈", "color": self.colors['primary']},
            {"title": "销售订单", "value": "156", "icon": "📋", "color": self.colors['info']},
            {"title": "平均客单价", "value": "￥68", "icon": "💳", "color": self.colors['secondary']}
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
            
    def create_sales_table(self):
        """创建销售记录表格"""
        table_frame = tk.Frame(self.main_frame, bg=self.colors['surface'])
        table_frame.pack(fill="both", expand=True)
        
        # 表格标题
        table_title = tk.Label(table_frame, text="📊 销售记录", 
                              font=self.fonts['heading'],
                              bg=self.colors['surface'], 
                              fg=self.colors['text_primary'])
        table_title.pack(pady=10)
        
        # 创建Treeview表格
        columns = ("时间", "客户", "商品", "数量", "金额", "支付方式")
        self.sales_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        # 设置列标题
        for col in columns:
            self.sales_tree.heading(col, text=col)
            self.sales_tree.column(col, width=120, anchor="center")
        
        # 添加示例数据
        sample_data = [
            ("12:30", "张三", "番茄牛肉面", "2", "￥50", "微信支付"),
            ("12:45", "李四", "鸡蛋炒饭", "1", "￥18", "支付宝"),
            ("13:15", "王五", "牛肉汉堡", "3", "￥96", "现金"),
            ("13:30", "赵六", "薯条+可乐", "2", "￥24", "微信支付")
        ]
        
        for data in sample_data:
            self.sales_tree.insert("", "end", values=data)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.sales_tree.yview)
        self.sales_tree.configure(yscrollcommand=scrollbar.set)
        
        # 布局
        self.sales_tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y", pady=10)
