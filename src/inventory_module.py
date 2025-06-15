#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
库存管理模块
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from typing import Dict, List, Any

class InventoryModule:
    def __init__(self, parent_frame, title_frame):
        self.parent_frame = parent_frame
        self.title_frame = title_frame
        
        # 库存数据
        self.inventory_data = [
            {"id": 1, "name": "面粉", "current_stock": 50, "unit": "kg", "threshold": 10, "unit_cost": 3.5, "expiry": "2024-12-30"},
            {"id": 2, "name": "鸡蛋", "current_stock": 200, "unit": "个", "threshold": 50, "unit_cost": 0.8, "expiry": "2024-07-15"},
            {"id": 3, "name": "牛肉", "current_stock": 25, "unit": "kg", "threshold": 5, "unit_cost": 35.0, "expiry": "2024-07-01"},
            {"id": 4, "name": "番茄", "current_stock": 80, "unit": "kg", "threshold": 15, "unit_cost": 4.2, "expiry": "2024-06-25"},
            {"id": 5, "name": "一次性餐盒", "current_stock": 500, "unit": "个", "threshold": 100, "unit_cost": 0.5, "expiry": "2025-06-01"},
        ]
        
    def show(self):
        """显示库存管理模块"""
        # 清空标题栏
        for widget in self.title_frame.winfo_children():
            widget.destroy()
            
        # 清空内容区域
        for widget in self.parent_frame.winfo_children():
            widget.destroy()
        
        # 标题
        title_label = tk.Label(self.title_frame, text="📦 库存管理", font=("微软雅黑", 16, "bold"),
                             bg="#ffffff", fg="#2c3e50")
        title_label.pack(side="left", padx=20, pady=15)
        
        # 工具栏
        toolbar_frame = tk.Frame(self.title_frame, bg="#ffffff")
        toolbar_frame.pack(side="right", padx=20, pady=15)
        
        add_btn = tk.Button(toolbar_frame, text="➕ 添加食材", font=("微软雅黑", 10),
                          bg="#27ae60", fg="white", bd=0, padx=15, pady=5,
                          cursor="hand2", command=self.add_inventory_item)
        add_btn.pack(side="right", padx=5)
        
        # 主内容
        content_frame = tk.Frame(self.parent_frame, bg="#ffffff")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # 创建表格
        columns = ("ID", "食材名称", "当前库存", "单位", "安全库存", "单价", "过期日期", "状态")
        tree = ttk.Treeview(content_frame, columns=columns, show="headings", height=15)
        
        # 设置列标题和宽度
        column_widths = [60, 120, 100, 60, 100, 80, 120, 80]
        for i, (col, width) in enumerate(zip(columns, column_widths)):
            tree.heading(col, text=col)
            tree.column(col, width=width, anchor="center")
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(content_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        # 填充数据
        for item in self.inventory_data:
            status = "⚠️ 库存不足" if item["current_stock"] <= item["threshold"] else "✅ 正常"
            tree.insert("", "end", values=(
                item["id"], item["name"], item["current_stock"], item["unit"],
                item["threshold"], f"¥{item['unit_cost']}", item["expiry"], status
            ))
        
        # 布局
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # 双击编辑功能
        tree.bind("<Double-1>", lambda e: self.edit_inventory_item(tree))
        
    def add_inventory_item(self):
        """添加库存项目"""
        messagebox.showinfo("添加食材", "添加食材功能待实现")
    
    def edit_inventory_item(self, tree):
        """编辑库存项目"""
        messagebox.showinfo("编辑食材", "编辑食材功能待实现")
