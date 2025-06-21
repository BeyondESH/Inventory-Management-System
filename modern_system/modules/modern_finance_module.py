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
          # 初始化Tkinter变量（指定父窗口）
        self.search_var = None
        self.date_filter_var = None
        self.type_filter_var = None
        
    def show(self):
        """显示财务管理界面"""
        if self.main_frame:
            self.main_frame.destroy()
        
        self.main_frame = tk.Frame(self.parent_frame, bg=self.colors['background'])
        self.main_frame.pack(fill="both", expand=True)
        
        # 初始化Tkinter变量（指定父窗口）
        self.search_var = tk.StringVar(self.main_frame)
        self.date_filter_var = tk.StringVar(self.main_frame, value="全部")
        self.type_filter_var = tk.StringVar(self.main_frame, value="全部")
        
        # 标题
        title_label = tk.Label(self.main_frame, text="💼 财务管理", 
                              font=self.fonts['title'],
                              bg=self.colors['background'], 
                              fg=self.colors['text_primary'])
        title_label.pack(pady=(0, 20))
          # 财务概览
        self.create_finance_overview()
        
        # 创建选项卡
        self.create_finance_tabs()
        
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
            
    def create_finance_tabs(self):
        """创建财务管理选项卡"""
        tabs_frame = tk.Frame(self.main_frame, bg=self.colors['background'])
        tabs_frame.pack(fill="both", expand=True)
        
        # 创建选项卡控件
        self.notebook = ttk.Notebook(tabs_frame)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 收支记录选项卡
        self.records_frame = tk.Frame(self.notebook, bg=self.colors['surface'])
        self.notebook.add(self.records_frame, text="📊 收支记录")
        self.create_finance_records()
        
        # 固定成本管理选项卡
        self.fixed_costs_frame = tk.Frame(self.notebook, bg=self.colors['surface'])
        self.notebook.add(self.fixed_costs_frame, text="🏢 固定成本")
        self.create_fixed_costs_management()
        
    def create_fixed_costs_management(self):
        """创建固定成本管理界面"""
        # 标题
        title_label = tk.Label(self.fixed_costs_frame, text="🏢 固定成本管理", 
                              font=self.fonts['heading'],
                              bg=self.colors['surface'], 
                              fg=self.colors['text_primary'])
        title_label.pack(pady=(10, 20))
        
        # 成本概览卡片
        overview_frame = tk.Frame(self.fixed_costs_frame, bg=self.colors['surface'])
        overview_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        cost_stats = [
            {"title": "月租金", "value": "￥8,000", "icon": "🏠", "color": self.colors['primary']},
            {"title": "员工工资", "value": "￥15,000", "icon": "👥", "color": self.colors['info']},
            {"title": "水电费", "value": "￥1,200", "icon": "⚡", "color": self.colors['warning']},
            {"title": "总固定成本", "value": "￥24,200", "icon": "💼", "color": self.colors['danger']}
        ]
        
        for stat in cost_stats:
            card = tk.Frame(overview_frame, bg=self.colors['background'], relief="solid", bd=1)
            card.pack(side="left", fill="both", expand=True, padx=(0, 10))
            
            # 图标
            icon_label = tk.Label(card, text=stat['icon'], font=('Segoe UI Emoji', 20),
                                bg=self.colors['background'], fg=stat['color'])
            icon_label.pack(pady=(10, 5))
            
            # 数值
            value_label = tk.Label(card, text=stat['value'], font=self.fonts['heading'],
                                 bg=self.colors['background'], fg=self.colors['text_primary'])
            value_label.pack()
            
            # 标题
            title_label = tk.Label(card, text=stat['title'], font=self.fonts['body'],
                                 bg=self.colors['background'], fg=self.colors['text_secondary'])
            title_label.pack(pady=(5, 10))
        
        # 固定成本列表
        list_frame = tk.Frame(self.fixed_costs_frame, bg=self.colors['surface'])
        list_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # 操作按钮
        btn_frame = tk.Frame(list_frame, bg=self.colors['surface'])
        btn_frame.pack(fill="x", pady=(0, 10))
        
        add_cost_btn = tk.Button(btn_frame, text="➕ 添加固定成本", 
                               font=self.fonts['body'],
                               bg=self.colors['primary'], fg='white',
                               bd=0, pady=8, padx=15, cursor="hand2",
                               command=self.add_fixed_cost)
        add_cost_btn.pack(side="left", padx=(0, 10))
        
        edit_cost_btn = tk.Button(btn_frame, text="✏️ 编辑成本", 
                                font=self.fonts['body'],
                                bg=self.colors['info'], fg='white',
                                bd=0, pady=8, padx=15, cursor="hand2",
                                command=self.edit_fixed_cost)
        edit_cost_btn.pack(side="left", padx=(0, 10))
        
        delete_cost_btn = tk.Button(btn_frame, text="🗑️ 删除成本", 
                                  font=self.fonts['body'],
                                  bg=self.colors['danger'], fg='white',
                                  bd=0, pady=8, padx=15, cursor="hand2",
                                  command=self.delete_fixed_cost)
        delete_cost_btn.pack(side="left")
        
        # 固定成本表格
        columns = ("成本类型", "成本项目", "金额", "周期", "下次缴费", "状态", "备注")
        self.costs_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=12)
        
        # 设置列标题和宽度
        column_widths = [100, 150, 100, 80, 120, 80, 150]
        for i, col in enumerate(columns):
            self.costs_tree.heading(col, text=col)
            self.costs_tree.column(col, width=column_widths[i], anchor="center")
        
        # 添加示例数据
        sample_costs = [
            ("租金", "店铺租金", "￥8,000", "月付", "2024-07-01", "已付", "主店面租金"),
            ("人力", "厨师工资", "￥5,000", "月付", "2024-07-01", "已付", "主厨月薪"),
            ("人力", "服务员工资", "￥3,500", "月付", "2024-07-01", "已付", "服务员月薪"),
            ("人力", "收银员工资", "￥3,200", "月付", "2024-07-01", "已付", "收银员月薪"),
            ("水电", "电费", "￥800", "月付", "2024-07-05", "未付", "店铺用电"),
            ("水电", "水费", "￥300", "月付", "2024-07-05", "未付", "店铺用水"),
            ("通讯", "网络费", "￥100", "月付", "2024-07-10", "已付", "宽带网络"),
            ("保险", "店铺保险", "￥500", "年付", "2024-12-01", "已付", "商业保险"),
            ("许可", "营业执照", "￥200", "年付", "2025-01-01", "已付", "工商年检"),
            ("设备", "设备维护", "￥600", "季付", "2024-09-01", "已付", "厨房设备维护")
        ]
        
        for cost in sample_costs:
            # 根据状态设置不同颜色
            if cost[5] == "未付":
                tags = ("unpaid",)
            else:
                tags = ("paid",)
            
            self.costs_tree.insert("", "end", values=cost, tags=tags)
        
        # 设置标签样式
        self.costs_tree.tag_configure("unpaid", background="#FFE6E6", foreground="#D63031")
        self.costs_tree.tag_configure("paid", background="#E8F5E8", foreground="#00B894")
        
        # 添加滚动条
        costs_scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.costs_tree.yview)
        self.costs_tree.configure(yscrollcommand=costs_scrollbar.set)
        
        # 布局
        self.costs_tree.pack(side="left", fill="both", expand=True)
        costs_scrollbar.pack(side="right", fill="y")
        
    def add_fixed_cost(self):
        """添加固定成本"""
        try:
            root = self.main_frame.winfo_toplevel()
            
            # 创建添加对话框
            dialog = tk.Toplevel(root)
            dialog.title("添加固定成本")
            dialog.geometry("450x500")
            dialog.configure(bg=self.colors['background'])
            dialog.transient(root)
            dialog.grab_set()
            
            # 居中显示
            dialog.update_idletasks()
            x = (dialog.winfo_screenwidth() // 2) - (225)
            y = (dialog.winfo_screenheight() // 2) - (250)
            dialog.geometry(f"450x500+{x}+{y}")
            
            # 标题
            tk.Label(dialog, text="添加固定成本", font=self.fonts['heading'],
                    bg=self.colors['background'], fg=self.colors['text_primary']).pack(pady=15)
            
            # 输入框架
            form_frame = tk.Frame(dialog, bg=self.colors['background'])
            form_frame.pack(fill="both", expand=True, padx=20, pady=10)
            
            # 成本类型
            tk.Label(form_frame, text="成本类型:", bg=self.colors['background']).pack(anchor="w")
            type_var = tk.StringVar(dialog, value="租金")
            type_combo = ttk.Combobox(form_frame, textvariable=type_var,
                                    values=["租金", "人力", "水电", "通讯", "保险", "许可", "设备", "其他"])
            type_combo.pack(fill="x", pady=(5, 15))
            
            # 成本项目
            tk.Label(form_frame, text="成本项目:", bg=self.colors['background']).pack(anchor="w")
            item_var = tk.StringVar(dialog)
            item_entry = tk.Entry(form_frame, textvariable=item_var, font=self.fonts['body'])
            item_entry.pack(fill="x", pady=(5, 15))
            
            # 金额
            tk.Label(form_frame, text="金额:", bg=self.colors['background']).pack(anchor="w")
            amount_var = tk.StringVar(dialog)
            amount_entry = tk.Entry(form_frame, textvariable=amount_var, font=self.fonts['body'])
            amount_entry.pack(fill="x", pady=(5, 15))
            
            # 缴费周期
            tk.Label(form_frame, text="缴费周期:", bg=self.colors['background']).pack(anchor="w")
            period_var = tk.StringVar(dialog, value="月付")
            period_combo = ttk.Combobox(form_frame, textvariable=period_var,
                                      values=["日付", "周付", "月付", "季付", "年付", "一次性"])
            period_combo.pack(fill="x", pady=(5, 15))
            
            # 下次缴费日期
            tk.Label(form_frame, text="下次缴费日期:", bg=self.colors['background']).pack(anchor="w")
            next_date_var = tk.StringVar(dialog)
            next_date_entry = tk.Entry(form_frame, textvariable=next_date_var, font=self.fonts['body'])
            next_date_entry.pack(fill="x", pady=(5, 5))
            tk.Label(form_frame, text="格式: YYYY-MM-DD", font=self.fonts['small'],
                    bg=self.colors['background'], fg=self.colors['text_secondary']).pack(anchor="w", pady=(0, 15))
            
            # 状态
            tk.Label(form_frame, text="状态:", bg=self.colors['background']).pack(anchor="w")
            status_var = tk.StringVar(dialog, value="未付")
            status_combo = ttk.Combobox(form_frame, textvariable=status_var,
                                      values=["已付", "未付", "逾期"])
            status_combo.pack(fill="x", pady=(5, 15))
            
            # 备注
            tk.Label(form_frame, text="备注:", bg=self.colors['background']).pack(anchor="w")
            note_var = tk.StringVar(dialog)
            note_entry = tk.Entry(form_frame, textvariable=note_var, font=self.fonts['body'])
            note_entry.pack(fill="x", pady=(5, 15))
            
            # 按钮
            btn_frame = tk.Frame(dialog, bg=self.colors['background'])
            btn_frame.pack(fill="x", padx=20, pady=20)
            
            def save_cost():
                try:
                    cost_type = type_var.get().strip()
                    item = item_var.get().strip()
                    amount_str = amount_var.get().strip()
                    period = period_var.get().strip()
                    next_date = next_date_var.get().strip()
                    status = status_var.get().strip()
                    note = note_var.get().strip()
                    
                    if not all([cost_type, item, amount_str, period]):
                        messagebox.showerror("错误", "请填写所有必填字段", parent=dialog)
                        return
                    
                    try:
                        amount = float(amount_str)
                        if amount <= 0:
                            raise ValueError
                    except ValueError:
                        messagebox.showerror("错误", "请输入有效的金额", parent=dialog)
                        return
                    
                    # 验证日期格式
                    if next_date:
                        try:
                            datetime.datetime.strptime(next_date, "%Y-%m-%d")
                        except ValueError:
                            messagebox.showerror("错误", "日期格式不正确，请使用 YYYY-MM-DD", parent=dialog)
                            return
                    
                    # 添加到表格
                    tags = ("unpaid",) if status == "未付" else ("paid",)
                    self.costs_tree.insert("", "end", values=(
                        cost_type, item, f"￥{amount:,.0f}", period, next_date, status, note
                    ), tags=tags)
                    
                    messagebox.showinfo("成功", "固定成本添加成功", parent=dialog)
                    dialog.destroy()
                    
                except Exception as e:
                    messagebox.showerror("错误", f"添加失败：{e}", parent=dialog)
            
            tk.Button(btn_frame, text="保存", command=save_cost,
                     bg=self.colors['primary'], fg='white', bd=0, pady=8, padx=20).pack(side="left")
            tk.Button(btn_frame, text="取消", command=dialog.destroy,
                     bg=self.colors['text_secondary'], fg='white', bd=0, pady=8, padx=20).pack(side="right")
                     
        except Exception as e:
            root = self.main_frame.winfo_toplevel()
            messagebox.showerror("错误", f"打开添加对话框失败：{e}", parent=root)
    
    def edit_fixed_cost(self):
        """编辑固定成本"""
        try:
            selected = self.costs_tree.selection()
            if not selected:
                messagebox.showwarning("提示", "请先选择要编辑的成本项目")
                return
            
            item = self.costs_tree.item(selected[0])
            values = item['values']
            
            root = self.main_frame.winfo_toplevel()
            messagebox.showinfo("功能提示", f"编辑功能开发中...\n选中项目: {values[1]}", parent=root)
        except Exception as e:
            root = self.main_frame.winfo_toplevel()
            messagebox.showerror("错误", f"编辑失败：{e}", parent=root)
    
    def delete_fixed_cost(self):
        """删除固定成本"""
        try:
            selected = self.costs_tree.selection()
            if not selected:
                messagebox.showwarning("提示", "请先选择要删除的成本项目")
                return
            
            item = self.costs_tree.item(selected[0])
            values = item['values']
            
            result = messagebox.askyesno("确认删除", f"确定要删除成本项目 '{values[1]}' 吗？")
            if result:
                self.costs_tree.delete(selected[0])
                messagebox.showinfo("成功", "成本项目删除成功")
        except Exception as e:
            root = self.main_frame.winfo_toplevel()
            messagebox.showerror("错误", f"删除失败：{e}", parent=root)
            
    def create_finance_records(self):
        """创建收支记录表格"""
        # 表格标题
        records_title = tk.Label(self.records_frame, text="📊 收支记录", 
                                font=self.fonts['heading'],
                                bg=self.colors['surface'], 
                                fg=self.colors['text_primary'])
        records_title.pack(pady=10)
        
        # 创建Treeview表格
        columns = ("时间", "类型", "描述", "金额", "支付方式", "备注")
        self.finance_tree = ttk.Treeview(self.records_frame, columns=columns, show='headings', height=15)
        
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
        scrollbar = ttk.Scrollbar(self.records_frame, orient="vertical", command=self.finance_tree.yview)
        self.finance_tree.configure(yscrollcommand=scrollbar.set)
        
        # 布局
        self.finance_tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y", pady=10)
        
        # 添加操作按钮
        self.create_finance_buttons(self.records_frame)
        
    def create_finance_buttons(self, parent):
        """创建财务操作按钮"""
        button_frame = tk.Frame(parent, bg=self.colors['surface'])
        button_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        # 添加收入按钮
        add_income_btn = tk.Button(button_frame, text="📈 添加收入", 
                                  font=self.fonts['body'],
                                  bg=self.colors['success'], fg='white',
                                  bd=0, pady=8, padx=15, cursor="hand2",
                                  command=self.add_income_record)
        add_income_btn.pack(side="left", padx=(0, 10))
        
        # 添加支出按钮
        add_expense_btn = tk.Button(button_frame, text="📉 添加支出", 
                                   font=self.fonts['body'],
                                   bg=self.colors['danger'], fg='white',
                                   bd=0, pady=8, padx=15, cursor="hand2",
                                   command=self.add_expense_record)
        add_expense_btn.pack(side="left", padx=(0, 10))
        
        # 导出报表按钮
        export_btn = tk.Button(button_frame, text="📊 导出报表", 
                              font=self.fonts['body'],
                              bg=self.colors['info'], fg='white',
                              bd=0, pady=8, padx=15, cursor="hand2",
                              command=self.export_finance_report)
        export_btn.pack(side="right")
        
    def add_income_record(self):
        """添加收入记录"""
        try:
            # 获取根窗口以避免Tkinter错误
            root = self.main_frame.winfo_toplevel()
            
            # 创建输入对话框
            dialog = tk.Toplevel(root)
            dialog.title("添加收入记录")
            dialog.geometry("400x300")
            dialog.configure(bg=self.colors['background'])
            dialog.transient(root)
            dialog.grab_set()
            
            # 居中显示
            dialog.update_idletasks()
            x = (dialog.winfo_screenwidth() // 2) - (200)
            y = (dialog.winfo_screenheight() // 2) - (150)
            dialog.geometry(f"400x300+{x}+{y}")
            
            # 输入字段
            tk.Label(dialog, text="添加收入记录", font=self.fonts['heading'],
                    bg=self.colors['background'], fg=self.colors['text_primary']).pack(pady=10)
            
            # 描述
            tk.Label(dialog, text="描述:", bg=self.colors['background'], 
                    fg=self.colors['text_primary']).pack(anchor="w", padx=20)
            desc_var = tk.StringVar(dialog)
            desc_entry = tk.Entry(dialog, textvariable=desc_var, font=self.fonts['body'])
            desc_entry.pack(fill="x", padx=20, pady=5)
            
            # 金额
            tk.Label(dialog, text="金额:", bg=self.colors['background'], 
                    fg=self.colors['text_primary']).pack(anchor="w", padx=20)
            amount_var = tk.StringVar(dialog)
            amount_entry = tk.Entry(dialog, textvariable=amount_var, font=self.fonts['body'])
            amount_entry.pack(fill="x", padx=20, pady=5)
            
            # 支付方式
            tk.Label(dialog, text="支付方式:", bg=self.colors['background'], 
                    fg=self.colors['text_primary']).pack(anchor="w", padx=20)
            payment_var = tk.StringVar(dialog, value="现金")
            payment_combo = ttk.Combobox(dialog, textvariable=payment_var, 
                                        values=["现金", "银行卡", "微信支付", "支付宝"])
            payment_combo.pack(fill="x", padx=20, pady=5)
            
            # 备注
            tk.Label(dialog, text="备注:", bg=self.colors['background'], 
                    fg=self.colors['text_primary']).pack(anchor="w", padx=20)
            note_var = tk.StringVar(dialog)
            note_entry = tk.Entry(dialog, textvariable=note_var, font=self.fonts['body'])
            note_entry.pack(fill="x", padx=20, pady=5)
            
            # 按钮
            btn_frame = tk.Frame(dialog, bg=self.colors['background'])
            btn_frame.pack(fill="x", padx=20, pady=20)
            
            def save_income():
                try:
                    desc = desc_var.get().strip()
                    amount_str = amount_var.get().strip()
                    payment = payment_var.get().strip()
                    note = note_var.get().strip()
                    
                    if not desc or not amount_str:
                        messagebox.showerror("错误", "请填写描述和金额", parent=dialog)
                        return
                    
                    amount = float(amount_str)
                    if amount <= 0:
                        messagebox.showerror("错误", "金额必须大于0", parent=dialog)
                        return
                    
                    # 添加到表格
                    current_time = datetime.datetime.now().strftime("%H:%M")
                    self.finance_tree.insert("", 0, values=(
                        current_time, "收入", desc, f"￥{amount:.2f}", payment, note
                    ))
                    
                    messagebox.showinfo("成功", "收入记录添加成功", parent=dialog)
                    dialog.destroy()
                    
                except ValueError:
                    messagebox.showerror("错误", "请输入有效的金额", parent=dialog)
                except Exception as e:
                    messagebox.showerror("错误", f"添加记录失败：{e}", parent=dialog)
            
            tk.Button(btn_frame, text="保存", command=save_income,
                     bg=self.colors['success'], fg='white', bd=0, pady=8, padx=20).pack(side="left")
            tk.Button(btn_frame, text="取消", command=dialog.destroy,
                     bg=self.colors['text_secondary'], fg='white', bd=0, pady=8, padx=20).pack(side="right")
                     
        except Exception as e:
            root = self.main_frame.winfo_toplevel()
            messagebox.showerror("错误", f"打开添加收入对话框失败：{e}", parent=root)
            
    def add_expense_record(self):
        """添加支出记录"""
        try:
            # 获取根窗口以避免Tkinter错误
            root = self.main_frame.winfo_toplevel()
            messagebox.showinfo("功能提示", "支出记录功能开发中...", parent=root)
        except Exception as e:
            root = self.main_frame.winfo_toplevel()
            messagebox.showerror("错误", f"功能访问失败：{e}", parent=root)
            
    def export_finance_report(self):
        """导出财务报表"""
        try:
            # 获取根窗口以避免Tkinter错误
            root = self.main_frame.winfo_toplevel()
            messagebox.showinfo("功能提示", "财务报表导出功能开发中...", parent=root)
        except Exception as e:
            root = self.main_frame.winfo_toplevel()
            messagebox.showerror("错误", f"导出功能访问失败：{e}", parent=root)
