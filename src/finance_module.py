#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from typing import Dict, List, Any
import datetime
import calendar

class FinanceModule:
    def __init__(self, parent_frame, title_frame, order_module=None, meal_module=None):
        self.parent_frame = parent_frame
        self.title_frame = title_frame
        self.order_module = order_module
        self.meal_module = meal_module
        
        # 财务数据
        self.financial_data = {
            "fixed_costs": {
                "人力成本": 10000.0,
                "租金": 3500.0,
                "水电费": 2000.0,
                "杂费": 1000.0
            }
        }

    def get_order_data(self):
        """获取订单数据"""
        if self.order_module and hasattr(self.order_module, 'order_data'):
            return self.order_module.order_data
        else:
            # 模拟订单数据
            return [
                {"id": 1001, "customer": "张三", "meal": "番茄牛肉面", "quantity": 2, "total": 50.0, "date": "2024-06-15", "status": "已完成"},
                {"id": 1002, "customer": "李四", "meal": "鸡蛋炒饭", "quantity": 1, "total": 18.0, "date": "2024-06-15", "status": "已完成"},
                {"id": 1003, "customer": "王五", "meal": "牛肉汉堡", "quantity": 3, "total": 96.0, "date": "2024-06-14", "status": "已完成"},
                {"id": 1004, "customer": "赵六", "meal": "蒸蛋羹", "quantity": 4, "total": 48.0, "date": "2024-06-14", "status": "已完成"},
                {"id": 1005, "customer": "陈七", "meal": "红烧肉", "quantity": 2, "total": 70.0, "date": "2024-06-13", "status": "已完成"},
                {"id": 1006, "customer": "刘八", "meal": "素食沙拉", "quantity": 3, "total": 66.0, "date": "2024-06-13", "status": "已完成"},
                {"id": 1007, "customer": "孙九", "meal": "番茄牛肉面", "quantity": 1, "total": 25.0, "date": "2024-06-12", "status": "已完成"},
                {"id": 1008, "customer": "周十", "meal": "牛肉汉堡", "quantity": 2, "total": 64.0, "date": "2024-06-12", "status": "已完成"},
            ]
    
    def get_meal_data(self):
        """获取餐食数据"""
        if self.meal_module and hasattr(self.meal_module, 'meal_data'):
            return self.meal_module.meal_data
        else:
            # 模拟餐食数据
            return [
                {"id": 1, "name": "番茄牛肉面", "price": 25.0, "category": "面食", "cook_time": 15, "active": True},
                {"id": 2, "name": "鸡蛋炒饭", "price": 18.0, "category": "米饭", "cook_time": 10, "active": True},
                {"id": 3, "name": "蒸蛋羹", "price": 12.0, "category": "汤品", "cook_time": 8, "active": True},
                {"id": 4, "name": "牛肉汉堡", "price": 32.0, "category": "西式", "cook_time": 12, "active": True},
                {"id": 5, "name": "素食沙拉", "price": 22.0, "category": "沙拉", "cook_time": 5, "active": False},
                {"id": 6, "name": "红烧肉", "price": 35.0, "category": "中式", "cook_time": 25, "active": True},
            ]
    
    def calculate_financial_data(self):
        """计算财务数据"""
        orders = self.get_order_data()
        meals = self.get_meal_data()
        
        # 只计算已完成订单的收入
        completed_orders = [order for order in orders if order["status"] == "已完成"]
        
        # 计算总收入
        total_income = sum(order["total"] for order in completed_orders)
        
        # 计算可变成本（假设每单位餐食的成本是售价的40%）
        variable_costs = sum(order["total"] * 0.4 for order in completed_orders)
        
        # 计算固定成本总额
        total_fixed_costs = sum(self.financial_data["fixed_costs"].values())
        
        # 计算净利润
        profit = total_income - total_fixed_costs - variable_costs
        
        return {
            "total_income": total_income,
            "variable_costs": variable_costs,
            "total_fixed_costs": total_fixed_costs,
            "profit": profit,
            "completed_orders": completed_orders
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
        
        # 工具栏
        toolbar_frame = tk.Frame(self.title_frame, bg="#ffffff")
        toolbar_frame.pack(side="right", padx=20, pady=15)
        
        # 编辑固定成本按钮
        edit_costs_btn = tk.Button(toolbar_frame, text="⚙️ 编辑固定成本", font=("微软雅黑", 10),
                                 bg="#9b59b6", fg="white", bd=0, padx=15, pady=5,
                                 cursor="hand2", command=self.edit_fixed_costs)
        edit_costs_btn.pack(side="right", padx=(5, 0))
        
        # 导出报表按钮
        export_btn = tk.Button(toolbar_frame, text="📊 导出报表", font=("微软雅黑", 10),
                             bg="#e67e22", fg="white", bd=0, padx=15, pady=5,
                             cursor="hand2", command=self.export_report)
        export_btn.pack(side="right", padx=5)
        
        # 刷新按钮
        refresh_btn = tk.Button(toolbar_frame, text="🔄 刷新数据", font=("微软雅黑", 10),
                              bg="#3498db", fg="white", bd=0, padx=15, pady=5,
                              cursor="hand2", command=self.show)
        refresh_btn.pack(side="right", padx=5)
        
        # 获取财务数据
        financial_data = self.calculate_financial_data()
          # 创建主要内容区域
        main_frame = tk.Frame(self.parent_frame, bg="#ffffff")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # 上部：财务概览卡片（紧凑显示）
        overview_frame = tk.Frame(main_frame, bg="#ffffff")
        overview_frame.pack(fill="x", pady=(0, 15))
        
        self.create_financial_overview(overview_frame, financial_data)
          # 中部：收入明细列表（占据主要空间）
        details_frame = tk.Frame(main_frame, bg="#ffffff")
        details_frame.pack(fill="both", expand=True)
        
        self.create_income_details(details_frame, financial_data["completed_orders"])
    
    def create_financial_overview(self, parent, financial_data):
        """创建财务概览卡片"""
        # 标题
        overview_title = tk.Label(parent, text="📊 财务概览", font=("微软雅黑", 14, "bold"),
                                bg="#ffffff", fg="#2c3e50")
        overview_title.pack(anchor="w", pady=(0, 10))
        
        # 卡片容器
        cards_frame = tk.Frame(parent, bg="#ffffff")
        cards_frame.pack(fill="x")
        
        # 收入卡片
        income_frame = tk.Frame(cards_frame, bg="#27ae60", relief="raised", bd=2)
        income_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        tk.Label(income_frame, text="总收入", font=("微软雅黑", 12, "bold"),
               bg="#27ae60", fg="white").pack(pady=5)
        tk.Label(income_frame, text=f"¥{financial_data['total_income']:,.2f}", 
               font=("微软雅黑", 18, "bold"), bg="#27ae60", fg="white").pack(pady=5)
        
        # 固定成本卡片
        fixed_frame = tk.Frame(cards_frame, bg="#e74c3c", relief="raised", bd=2)
        fixed_frame.pack(side="left", fill="both", expand=True, padx=5)
        
        tk.Label(fixed_frame, text="固定成本", font=("微软雅黑", 12, "bold"),
               bg="#e74c3c", fg="white").pack(pady=5)
        tk.Label(fixed_frame, text=f"¥{financial_data['total_fixed_costs']:,.2f}",
               font=("微软雅黑", 18, "bold"), bg="#e74c3c", fg="white").pack(pady=5)
        
        # 可变成本卡片
        variable_frame = tk.Frame(cards_frame, bg="#f39c12", relief="raised", bd=2)
        variable_frame.pack(side="left", fill="both", expand=True, padx=5)
        
        tk.Label(variable_frame, text="可变成本", font=("微软雅黑", 12, "bold"),
               bg="#f39c12", fg="white").pack(pady=5)
        tk.Label(variable_frame, text=f"¥{financial_data['variable_costs']:,.2f}",
               font=("微软雅黑", 18, "bold"), bg="#f39c12", fg="white").pack(pady=5)
        
        # 利润卡片
        profit_color = "#27ae60" if financial_data['profit'] > 0 else "#e74c3c"
        profit_frame = tk.Frame(cards_frame, bg=profit_color, relief="raised", bd=2)
        profit_frame.pack(side="right", fill="both", expand=True, padx=(5, 0))
        
        tk.Label(profit_frame, text="净利润", font=("微软雅黑", 12, "bold"),
               bg=profit_color, fg="white").pack(pady=5)
        tk.Label(profit_frame, text=f"¥{financial_data['profit']:,.2f}", 
               font=("微软雅黑", 18, "bold"), bg=profit_color, fg="white").pack(pady=5)
    
    def create_income_details(self, parent, orders):
        """创建收入明细列表"""
        # 标题
        details_title = tk.Label(parent, text="📋 收入明细", font=("微软雅黑", 14, "bold"),
                               bg="#ffffff", fg="#2c3e50")
        details_title.pack(anchor="w", pady=(0, 10))
        
        # 创建表格框架
        table_frame = tk.Frame(parent, bg="#ffffff")
        table_frame.pack(fill="both", expand=True)
          # 创建表格
        columns = ("订单ID", "客户", "餐食", "数量", "金额", "日期")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        
        # 设置列标题和宽度
        column_widths = [80, 100, 120, 60, 80, 100]
        for i, (col, width) in enumerate(zip(columns, column_widths)):
            tree.heading(col, text=col)
            tree.column(col, width=width, anchor="center")
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        # 填充数据
        total_amount = 0
        for order in orders:
            tree.insert("", "end", values=(
                order["id"], order["customer"], order["meal"], 
                order["quantity"], f"¥{order['total']:.2f}", order["date"]
            ))
            total_amount += order["total"]
        
        # 布局
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")        
        # 统计信息
        stats_frame = tk.Frame(parent, bg="#f8f9fa", relief="solid", bd=1)
        stats_frame.pack(fill="x", pady=(10, 0))
        
        tk.Label(stats_frame, text=f"共 {len(orders)} 笔订单，总金额：¥{total_amount:,.2f}", 
               font=("微软雅黑", 11, "bold"), bg="#f8f9fa", fg="#2c3e50").pack(pady=8)
      
    def edit_fixed_costs(self):
        """编辑固定成本"""
        """编辑固定成本"""
        dialog = tk.Toplevel()
        dialog.title("编辑固定成本")
        dialog.geometry("400x350")
        dialog.configure(bg="#f8f9fa")
        dialog.resizable(False, False)
        dialog.grab_set()
        
        # 居中显示对话框
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (dialog.winfo_screenheight() // 2) - (350 // 2)
        dialog.geometry(f"400x350+{x}+{y}")
        
        # 标题栏
        title_frame = tk.Frame(dialog, bg="#34495e", height=60)
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text="💼 编辑固定成本", 
                              font=("微软雅黑", 16, "bold"),
                              bg="#34495e", fg="white")
        title_label.pack(pady=15)
        
        # 表单区域
        form_frame = tk.Frame(dialog, bg="#f8f9fa")
        form_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        # 存储输入控件
        entries = {}
        
        # 创建输入字段
        row = 0
        for cost_name, cost_value in self.financial_data["fixed_costs"].items():
            # 标签
            label = tk.Label(form_frame, text=f"{cost_name}(元)", 
                           font=("微软雅黑", 11, "bold"),
                           bg="#f8f9fa", fg="#2c3e50")
            label.grid(row=row, column=0, sticky="w", pady=(10, 5))
            
            # 输入框
            entry = tk.Entry(form_frame, font=("微软雅黑", 11),
                           width=20, relief="solid", bd=1)
            entry.grid(row=row, column=1, sticky="ew", pady=(0, 5), padx=(10, 0))
            entry.insert(0, str(cost_value))
            entries[cost_name] = entry
            
            row += 1
        
        # 设置列权重
        form_frame.columnconfigure(1, weight=1)
        
        # 按钮区域
        button_frame = tk.Frame(dialog, bg="#f8f9fa")
        button_frame.pack(fill="x", padx=30, pady=(0, 20))
        
        # 取消按钮
        cancel_btn = tk.Button(button_frame, text="取消", 
                             font=("微软雅黑", 11),
                             bg="#95a5a6", fg="white", bd=0,
                             padx=20, pady=8, cursor="hand2",
                             command=dialog.destroy)
        cancel_btn.pack(side="right", padx=(15, 40))
        
        # 保存按钮
        def save_costs():
            try:
                for cost_name, entry in entries.items():
                    value = float(entry.get().strip())
                    if value < 0:
                        raise ValueError(f"{cost_name}不能为负数")
                    self.financial_data["fixed_costs"][cost_name] = value
                
                messagebox.showinfo("成功", "固定成本更新成功！")
                dialog.destroy()
                self.show()  # 刷新财务界面
                
            except ValueError as e:
                messagebox.showerror("错误", f"请输入有效的数值：{str(e)}")
        
        save_btn = tk.Button(button_frame, text="保存", 
                           font=("微软雅黑", 11),
                           bg="#27ae60", fg="white", bd=0,
                           padx=20, pady=8, cursor="hand2",
                           command=save_costs)
        save_btn.pack(side="right", padx=(0, 15))
    
    def export_report(self):
        """导出财务报表"""
        try:
            financial_data = self.calculate_financial_data()
            
            # 创建报表内容
            report_content = f"""
=== 食品服务公司财务报表 ===
生成时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

一、财务概览
- 总收入: ¥{financial_data['total_income']:,.2f}
- 固定成本: ¥{financial_data['total_fixed_costs']:,.2f}
- 可变成本: ¥{financial_data['variable_costs']:,.2f}
- 净利润: ¥{financial_data['profit']:,.2f}

二、固定成本明细
"""
            for cost_name, cost_value in self.financial_data["fixed_costs"].items():
                report_content += f"- {cost_name}: ¥{cost_value:,.2f}\n"
            
            report_content += f"""
三、订单明细
共 {len(financial_data['completed_orders'])} 笔已完成订单
"""
            for order in financial_data['completed_orders']:
                report_content += f"- 订单{order['id']}: {order['customer']} - {order['meal']} x{order['quantity']} = ¥{order['total']:.2f}\n"
            
            # 保存到文件
            import os
            filename = f"财务报表_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            filepath = os.path.join(os.getcwd(), filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(report_content)
            
            messagebox.showinfo("导出成功", f"财务报表已导出到:\n{filepath}")
            
        except Exception as e:
            messagebox.showerror("导出失败", f"导出报表时出错：{str(e)}")
