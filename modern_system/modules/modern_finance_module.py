#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
现代化财务管理模块
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
            def get_finance_records(self):
                return []
            def register_module(self, module_type, instance):
                pass
        data_manager = MockDataManager()

class ModernFinanceModule:
    def __init__(self, parent_frame, title_frame, order_module=None, employee_module=None):
        self.parent_frame = parent_frame
        self.title_frame = title_frame
        self.order_module = order_module
        self.employee_module = employee_module
        
        # 注册到数据管理中心
        data_manager.register_module('finance', self)
        
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
        """显示财务管理界面"""
        if self.main_frame:
            self.main_frame.destroy()
        
        self.main_frame = tk.Frame(self.parent_frame, bg=self.colors['background'])
        self.main_frame.pack(fill="both", expand=True)
        
        # 标题
        title_label = tk.Label(self.main_frame, text="💼 财务管理", 
                              font=self.fonts['title'],
                              bg=self.colors['background'], 
                              fg=self.colors['text_primary'])
        title_label.pack(pady=(0, 20))
        
        # 财务概览
        self.create_finance_overview()
        
        # 收支记录
        self.create_finance_records()
        
    def create_finance_overview(self):
        """创建财务概览"""
        overview_frame = tk.Frame(self.main_frame, bg=self.colors['background'])
        overview_frame.pack(fill="x", pady=(0, 20))
        
        # 财务统计
        stats = [
            {"title": "今日收入", "value": "￥2,580", "icon": "💰", "color": self.colors['success']},
            {"title": "今日支出", "value": "￥680", "icon": "💸", "color": self.colors['danger']},
            {"title": "净利润", "value": "￥1,900", "icon": "📈", "color": self.colors['primary']},
            {"title": "本月收入", "value": "￥58,960", "icon": "💳", "color": self.colors['info']}
        ]
        
        for stat in stats:
            card = tk.Frame(overview_frame, bg=self.colors['surface'], relief="flat", bd=1)
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
            
    def create_finance_records(self):
        """创建收支记录表格"""
        records_frame = tk.Frame(self.main_frame, bg=self.colors['surface'])
        records_frame.pack(fill="both", expand=True)
        
        # 表格标题
        records_title = tk.Label(records_frame, text="📊 收支记录", 
                                font=self.fonts['heading'],
                                bg=self.colors['surface'], 
                                fg=self.colors['text_primary'])
        records_title.pack(pady=10)
        
        # 创建Treeview表格
        columns = ("时间", "类型", "描述", "金额", "支付方式", "备注")
        self.finance_tree = ttk.Treeview(records_frame, columns=columns, show='headings', height=15)
        
        # 设置列标题
        for col in columns:
            self.finance_tree.heading(col, text=col)
            self.finance_tree.column(col, width=120, anchor="center")
        
        # 添加示例数据
        sample_data = [
            ("12:30", "收入", "订单收入", "￥50", "微信支付", "张三-番茄牛肉面"),
            ("12:45", "收入", "订单收入", "￥18", "支付宝", "李四-鸡蛋炒饭"),
            ("09:00", "支出", "原料采购", "￥500", "现金", "蔬菜采购"),
            ("10:30", "支出", "员工工资", "￥180", "银行转账", "小王-日薪")
        ]
        
        for data in sample_data:
            self.finance_tree.insert("", "end", values=data)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(records_frame, orient="vertical", command=self.finance_tree.yview)
        self.finance_tree.configure(yscrollcommand=scrollbar.set)
        
        # 布局
        self.finance_tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y", pady=10)
