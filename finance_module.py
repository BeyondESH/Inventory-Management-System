#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
财务管理模块
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from typing import Dict, List, Any

class FinanceModule:
    def __init__(self, parent_frame, title_frame):
        self.parent_frame = parent_frame
        self.title_frame = title_frame
        
        # 财务数据
        self.financial_data = {
            "monthly_income": 15800.0,
            "fixed_costs": {
                "人力成本": 10000.0,
                "租金": 3500.0,
                "水电费": 2000.0,
                "杂费": 1000.0
            },
            "variable_costs": 5200.0,
            "profit": 0.0  # 计算得出
        }
        
    def show(self):
        """显示财务管理模块"""
        # 清空标题栏
        for widget in self.title_frame.winfo_children():
            widget.destroy()
            
        # 清空内容区域
        for widget in self.parent_frame.winfo_children():
            widget.destroy()
        
        # 标题
        title_label = tk.Label(self.title_frame, text="💰 财务管理", font=("微软雅黑", 16, "bold"),
                             bg="#ffffff", fg="#2c3e50")
        title_label.pack(side="left", padx=20, pady=15)
        
        # 主内容
        content_frame = tk.Frame(self.parent_frame, bg="#ffffff")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # 计算利润
        total_fixed = sum(self.financial_data["fixed_costs"].values())
        profit = self.financial_data["monthly_income"] - total_fixed - self.financial_data["variable_costs"]
        self.financial_data["profit"] = profit
        
        # 收入卡片
        income_frame = tk.Frame(content_frame, bg="#27ae60", relief="raised", bd=2)
        income_frame.pack(fill="x", pady=10)
        
        tk.Label(income_frame, text="月度总收入", font=("微软雅黑", 12, "bold"),
               bg="#27ae60", fg="white").pack(pady=5)
        tk.Label(income_frame, text=f"¥{self.financial_data['monthly_income']:,.2f}", 
               font=("微软雅黑", 20, "bold"), bg="#27ae60", fg="white").pack(pady=5)
        
        # 成本分析
        costs_frame = tk.Frame(content_frame, bg="#ffffff")
        costs_frame.pack(fill="both", expand=True, pady=10)
        
        # 固定成本
        fixed_frame = tk.Frame(costs_frame, bg="#e74c3c", relief="raised", bd=2)
        fixed_frame.pack(side="left", fill="both", expand=True, padx=5)
        
        tk.Label(fixed_frame, text="固定成本", font=("微软雅黑", 12, "bold"),
               bg="#e74c3c", fg="white").pack(pady=5)
        
        for cost_name, cost_value in self.financial_data["fixed_costs"].items():
            tk.Label(fixed_frame, text=f"{cost_name}: ¥{cost_value:,.2f}",
                   font=("微软雅黑", 10), bg="#e74c3c", fg="white").pack(pady=2)
        
        tk.Label(fixed_frame, text=f"小计: ¥{total_fixed:,.2f}",
               font=("微软雅黑", 12, "bold"), bg="#e74c3c", fg="white").pack(pady=5)
        
        # 可变成本
        variable_frame = tk.Frame(costs_frame, bg="#f39c12", relief="raised", bd=2)
        variable_frame.pack(side="right", fill="both", expand=True, padx=5)
        
        tk.Label(variable_frame, text="可变成本", font=("微软雅黑", 12, "bold"),
               bg="#f39c12", fg="white").pack(pady=5)
        tk.Label(variable_frame, text=f"¥{self.financial_data['variable_costs']:,.2f}",
               font=("微软雅黑", 16, "bold"), bg="#f39c12", fg="white").pack(pady=20)
        
        # 利润显示
        profit_color = "#27ae60" if profit > 0 else "#e74c3c"
        profit_frame = tk.Frame(content_frame, bg=profit_color, relief="raised", bd=2)
        profit_frame.pack(fill="x", pady=10)
        
        tk.Label(profit_frame, text="月度净利润", font=("微软雅黑", 12, "bold"),
               bg=profit_color, fg="white").pack(pady=5)
        tk.Label(profit_frame, text=f"¥{profit:,.2f}", 
               font=("微软雅黑", 20, "bold"), bg=profit_color, fg="white").pack(pady=5)
