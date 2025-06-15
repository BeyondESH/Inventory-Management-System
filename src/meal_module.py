#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
餐食配置模块
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from typing import Dict, List, Any

class MealModule:
    def __init__(self, parent_frame, title_frame):
        self.parent_frame = parent_frame
        self.title_frame = title_frame
        
        # 餐食配置数据
        self.meal_data = [
            {"id": 1, "name": "番茄牛肉面", "price": 25.0, "active": True, "description": "经典番茄牛肉面"},
            {"id": 2, "name": "鸡蛋炒饭", "price": 18.0, "active": True, "description": "香滑鸡蛋炒饭"},
            {"id": 3, "name": "蒸蛋羹", "price": 12.0, "active": True, "description": "嫩滑蒸蛋羹"},
            {"id": 4, "name": "牛肉汉堡", "price": 32.0, "active": True, "description": "美式牛肉汉堡"},
            {"id": 5, "name": "素食沙拉", "price": 22.0, "active": False, "description": "健康素食沙拉"},
        ]
        
    def show(self):
        """显示餐食配置模块"""
        # 清空标题栏
        for widget in self.title_frame.winfo_children():
            widget.destroy()
            
        # 清空内容区域
        for widget in self.parent_frame.winfo_children():
            widget.destroy()
        
        # 标题
        title_label = tk.Label(self.title_frame, text="🍜 餐食配置", font=("微软雅黑", 16, "bold"),
                             bg="#ffffff", fg="#2c3e50")
        title_label.pack(side="left", padx=20, pady=15)
        
        # 工具栏
        toolbar_frame = tk.Frame(self.title_frame, bg="#ffffff")
        toolbar_frame.pack(side="right", padx=20, pady=15)
        
        add_btn = tk.Button(toolbar_frame, text="➕ 添加餐食", font=("微软雅黑", 10),
                          bg="#e67e22", fg="white", bd=0, padx=15, pady=5,
                          cursor="hand2", command=self.add_meal_item)
        add_btn.pack(side="right", padx=5)
        
        # 主内容 - 使用网格布局显示餐食卡片
        content_frame = tk.Frame(self.parent_frame, bg="#ffffff")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # 创建滚动区域
        canvas = tk.Canvas(content_frame, bg="#ffffff")
        scrollbar = ttk.Scrollbar(content_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#ffffff")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # 创建餐食卡片
        row, col = 0, 0
        for meal in self.meal_data:
            self.create_meal_card(scrollable_frame, meal, row, col)
            col += 1
            if col >= 3:  # 每行3个卡片
                col = 0
                row += 1
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def create_meal_card(self, parent, meal, row, col):
        """创建餐食卡片"""
        card_frame = tk.Frame(parent, bg="#f8f9fa", relief="raised", bd=1)
        card_frame.grid(row=row, column=col, padx=10, pady=10, sticky="ew")
        
        # 餐食名称
        name_label = tk.Label(card_frame, text=meal["name"], font=("微软雅黑", 14, "bold"),
                            bg="#f8f9fa", fg="#2c3e50")
        name_label.pack(pady=(10, 5))
        
        # 价格
        price_label = tk.Label(card_frame, text=f"¥{meal['price']}", font=("微软雅黑", 12),
                             bg="#f8f9fa", fg="#e74c3c")
        price_label.pack(pady=2)
        
        # 描述
        desc_label = tk.Label(card_frame, text=meal["description"], font=("微软雅黑", 9),
                            bg="#f8f9fa", fg="#7f8c8d", wraplength=150)
        desc_label.pack(pady=2)
        
        # 状态
        status_text = "✅ 启用中" if meal["active"] else "❌ 已停用"
        status_color = "#27ae60" if meal["active"] else "#e74c3c"
        status_label = tk.Label(card_frame, text=status_text, font=("微软雅黑", 9),
                              bg="#f8f9fa", fg=status_color)
        status_label.pack(pady=2)
        
        # 操作按钮
        btn_frame = tk.Frame(card_frame, bg="#f8f9fa")
        btn_frame.pack(pady=10)
        
        edit_btn = tk.Button(btn_frame, text="编辑", font=("微软雅黑", 8),
                           bg="#3498db", fg="white", bd=0, padx=10,
                           cursor="hand2", command=lambda: self.edit_meal_item(meal))
        edit_btn.pack(side="left", padx=2)
        
        toggle_btn = tk.Button(btn_frame, text="停用" if meal["active"] else "启用",
                             font=("微软雅黑", 8), bg="#e67e22", fg="white", bd=0, padx=10,
                             cursor="hand2", command=lambda: self.toggle_meal_status(meal))
        toggle_btn.pack(side="left", padx=2)
        
    def add_meal_item(self):
        """添加餐食项目"""
        messagebox.showinfo("添加餐食", "添加餐食功能待实现")
    
    def edit_meal_item(self, meal):
        """编辑餐食项目"""
        messagebox.showinfo("编辑餐食", f"编辑餐食 {meal['name']} 功能待实现")
    
    def toggle_meal_status(self, meal):
        """切换餐食状态"""
        meal["active"] = not meal["active"]
        self.show()  # 刷新界面
