#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
订单管理模块
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from typing import Dict, List, Any

class OrderModule:
    def __init__(self, parent_frame, title_frame):
        self.parent_frame = parent_frame
        self.title_frame = title_frame
        
        # 订单数据
        self.order_data = [
            {"id": 1001, "customer": "张三", "meal": "番茄牛肉面", "quantity": 2, "total": 50.0, "date": "2024-06-15", "status": "已完成"},
            {"id": 1002, "customer": "李四", "meal": "鸡蛋炒饭", "quantity": 1, "total": 18.0, "date": "2024-06-15", "status": "进行中"},
            {"id": 1003, "customer": "王五", "meal": "牛肉汉堡", "quantity": 3, "total": 96.0, "date": "2024-06-14", "status": "已接收"},
            {"id": 1004, "customer": "赵六", "meal": "蒸蛋羹", "quantity": 4, "total": 48.0, "date": "2024-06-14", "status": "已完成"},
        ]
        
    def show(self):
        """显示订单管理模块"""
        # 清空标题栏
        for widget in self.title_frame.winfo_children():
            widget.destroy()
            
        # 清空内容区域
        for widget in self.parent_frame.winfo_children():
            widget.destroy()
        
        # 标题
        title_label = tk.Label(self.title_frame, text="📋 订单管理", font=("微软雅黑", 16, "bold"),
                             bg="#ffffff", fg="#2c3e50")
        title_label.pack(side="left", padx=20, pady=15)
        
        # 工具栏
        toolbar_frame = tk.Frame(self.title_frame, bg="#ffffff")
        toolbar_frame.pack(side="right", padx=20, pady=15)
        
        add_btn = tk.Button(toolbar_frame, text="➕ 新建订单", font=("微软雅黑", 10),
                          bg="#3498db", fg="white", bd=0, padx=15, pady=5,
                          cursor="hand2", command=self.add_order_item)
        add_btn.pack(side="right", padx=5)
        
        # 主内容
        content_frame = tk.Frame(self.parent_frame, bg="#ffffff")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # 创建表格
        columns = ("订单号", "客户", "餐食", "数量", "总金额", "下单日期", "状态")
        tree = ttk.Treeview(content_frame, columns=columns, show="headings", height=15)
        
        # 设置列标题和宽度
        column_widths = [80, 100, 150, 60, 80, 100, 80]
        for i, (col, width) in enumerate(zip(columns, column_widths)):
            tree.heading(col, text=col)
            tree.column(col, width=width, anchor="center")
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(content_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        # 填充数据
        for order in self.order_data:
            tree.insert("", "end", values=(
                order["id"], order["customer"], order["meal"], order["quantity"],
                f"¥{order['total']}", order["date"], order["status"]
            ))
        
        # 布局
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # 双击编辑功能
        tree.bind("<Double-1>", lambda e: self.edit_order_item(tree))
        
    def add_order_item(self):
        """添加订单项目"""
        messagebox.showinfo("新建订单", "新建订单功能待实现")
    
    def edit_order_item(self, tree):
        """编辑订单项目"""
        messagebox.showinfo("编辑订单", "编辑订单功能待实现")
