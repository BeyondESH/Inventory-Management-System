#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
客户管理模块
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from typing import Dict, List, Any

class CustomerModule:
    def __init__(self, parent_frame, title_frame):
        self.parent_frame = parent_frame
        self.title_frame = title_frame
        
        # 客户数据
        self.customer_data = [
            {"id": 1, "name": "张三", "phone": "13800138001", "email": "zhangsan@email.com", "address": "北京市朝阳区xxx街道"},
            {"id": 2, "name": "李四", "phone": "13800138002", "email": "lisi@email.com", "address": "北京市海淀区xxx路"},
            {"id": 3, "name": "王五", "phone": "13800138003", "email": "wangwu@email.com", "address": "北京市西城区xxx胡同"},
            {"id": 4, "name": "赵六", "phone": "13800138004", "email": "zhaoliu@email.com", "address": "北京市东城区xxx大街"},
        ]
        
    def show(self):
        """显示客户管理模块"""
        # 清空标题栏
        for widget in self.title_frame.winfo_children():
            widget.destroy()
            
        # 清空内容区域
        for widget in self.parent_frame.winfo_children():
            widget.destroy()
        
        # 标题
        title_label = tk.Label(self.title_frame, text="👥 客户管理", font=("微软雅黑", 16, "bold"),
                             bg="#ffffff", fg="#2c3e50")
        title_label.pack(side="left", padx=20, pady=15)
        
        # 工具栏
        toolbar_frame = tk.Frame(self.title_frame, bg="#ffffff")
        toolbar_frame.pack(side="right", padx=20, pady=15)
        
        add_btn = tk.Button(toolbar_frame, text="➕ 添加客户", font=("微软雅黑", 10),
                          bg="#9b59b6", fg="white", bd=0, padx=15, pady=5,
                          cursor="hand2", command=self.add_customer_item)
        add_btn.pack(side="right", padx=5)
        
        # 主内容
        content_frame = tk.Frame(self.parent_frame, bg="#ffffff")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # 创建表格
        columns = ("ID", "姓名", "电话", "邮箱", "地址")
        tree = ttk.Treeview(content_frame, columns=columns, show="headings", height=15)
        
        # 设置列标题和宽度
        column_widths = [60, 100, 120, 180, 300]
        for i, (col, width) in enumerate(zip(columns, column_widths)):
            tree.heading(col, text=col)
            tree.column(col, width=width, anchor="center")
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(content_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        # 填充数据
        for customer in self.customer_data:
            tree.insert("", "end", values=(
                customer["id"], customer["name"], customer["phone"], 
                customer["email"], customer["address"]
            ))
        
        # 布局
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # 双击编辑功能
        tree.bind("<Double-1>", lambda e: self.edit_customer_item(tree))
        
    def add_customer_item(self):
        """添加客户项目"""
        messagebox.showinfo("添加客户", "添加客户功能待实现")
    
    def edit_customer_item(self, tree):
        """编辑客户项目"""
        messagebox.showinfo("编辑客户", "编辑客户功能待实现")
