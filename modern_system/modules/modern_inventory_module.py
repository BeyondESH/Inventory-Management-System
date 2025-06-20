#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
现代化库存管理模块
采用现代化设计风格的库存管理界面
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from typing import Dict, List, Any
import datetime
import json
import os

class ModernInventoryModule:
    def __init__(self, parent_frame, title_frame):
        self.parent_frame = parent_frame
        self.title_frame = title_frame
        
        # 现代化颜色主题
        self.colors = {
            'primary': '#FF6B35',      # 主色调
            'secondary': '#F7931E',    # 次色调
            'accent': '#FFD23F',       # 强调色
            'background': '#F8F9FA',   # 背景色
            'surface': '#FFFFFF',      # 卡片背景
            'text_primary': '#2D3436', # 主文字
            'text_secondary': '#636E72', # 次文字
            'border': '#E0E0E0',       # 边框
            'success': '#00B894',      # 成功色
            'warning': '#FDCB6E',      # 警告色
            'error': '#E84393',        # 错误色
            'card_shadow': '#F0F0F0'   # 卡片阴影
        }
        
        # 字体配置
        self.fonts = {
            'title': ('Microsoft YaHei UI', 20, 'bold'),
            'heading': ('Microsoft YaHei UI', 16, 'bold'),
            'subheading': ('Microsoft YaHei UI', 14, 'bold'),
            'body': ('Microsoft YaHei UI', 12),
            'small': ('Microsoft YaHei UI', 10),
            'button': ('Microsoft YaHei UI', 11, 'bold')
        }
        
        # 库存数据
        self.inventory_data = self.load_inventory_data()
        
        # 界面变量
        self.search_var = tk.StringVar()
        self.category_filter_var = tk.StringVar(value="全部")
        self.stock_filter_var = tk.StringVar(value="全部")
        
        # UI组件引用
        self.inventory_tree = None
        self.stats_labels = {}
        
    def load_inventory_data(self):
        """加载库存数据"""
        # 示例库存数据
        return [
            {"id": 1, "name": "牛肉", "category": "肉类", "current_stock": 25, "min_stock": 10, "max_stock": 100, "unit": "公斤", "price": 45.0, "supplier": "优质肉类供应商", "last_updated": "2025-06-19"},
            {"id": 2, "name": "大米", "category": "主食", "current_stock": 150, "min_stock": 50, "max_stock": 300, "unit": "公斤", "price": 6.5, "supplier": "优质粮食供应商", "last_updated": "2025-06-18"},
            {"id": 3, "name": "土豆", "category": "蔬菜", "current_stock": 8, "min_stock": 20, "max_stock": 80, "unit": "公斤", "price": 3.2, "supplier": "新鲜蔬菜供应商", "last_updated": "2025-06-20"},
            {"id": 4, "name": "鸡蛋", "category": "禽蛋", "current_stock": 200, "min_stock": 100, "max_stock": 500, "unit": "个", "price": 0.8, "supplier": "优质禽蛋供应商", "last_updated": "2025-06-19"},
            {"id": 5, "name": "番茄", "category": "蔬菜", "current_stock": 30, "min_stock": 15, "max_stock": 60, "unit": "公斤", "price": 4.5, "supplier": "新鲜蔬菜供应商", "last_updated": "2025-06-20"},
            {"id": 6, "name": "面粉", "category": "主食", "current_stock": 80, "min_stock": 40, "max_stock": 200, "unit": "公斤", "price": 4.8, "supplier": "优质粮食供应商", "last_updated": "2025-06-18"},
            {"id": 7, "name": "食用油", "category": "调料", "current_stock": 12, "min_stock": 10, "max_stock": 50, "unit": "升", "price": 15.0, "supplier": "优质调料供应商", "last_updated": "2025-06-17"},
            {"id": 8, "name": "盐", "category": "调料", "current_stock": 45, "min_stock": 20, "max_stock": 100, "unit": "包", "price": 2.5, "supplier": "优质调料供应商", "last_updated": "2025-06-15"},
        ]
        
    def show(self):
        """显示库存管理模块"""
        self.clear_frames()
        self.update_title()
        self.create_inventory_interface()
        
    def clear_frames(self):
        """清空框架"""
        for widget in self.parent_frame.winfo_children():
            widget.destroy()
        for widget in self.title_frame.winfo_children():
            widget.destroy()
            
    def update_title(self):
        """更新标题"""
        # 左侧标题
        title_frame = tk.Frame(self.title_frame, bg=self.colors['surface'])
        title_frame.pack(side="left", fill="y")
        
        icon_label = tk.Label(title_frame, text="📦", font=('Segoe UI Emoji', 20),
                             bg=self.colors['surface'], fg=self.colors['primary'])
        icon_label.pack(side="left", padx=(30, 10), pady=20)
        
        title_label = tk.Label(title_frame, text="库存管理", font=self.fonts['title'],
                              bg=self.colors['surface'], fg=self.colors['text_primary'])
        title_label.pack(side="left", pady=20)
        
        # 右侧操作按钮
        action_frame = tk.Frame(self.title_frame, bg=self.colors['surface'])
        action_frame.pack(side="right", padx=30, pady=20)
        
        # 导出报表按钮
        export_btn = self.create_action_button(action_frame, "📊 导出报表", self.export_report)
        export_btn.pack(side="right", padx=(10, 0))
        
        # 添加库存按钮
        add_btn = self.create_action_button(action_frame, "➕ 添加商品", self.add_inventory_item, primary=True)
        add_btn.pack(side="right", padx=(10, 0))
        
    def create_action_button(self, parent, text, command, primary=False):
        """创建操作按钮"""
        if primary:
            bg_color = self.colors['primary']
            fg_color = "white"
            hover_color = self.colors['secondary']
        else:
            bg_color = self.colors['background']
            fg_color = self.colors['text_secondary']
            hover_color = self.colors['border']
            
        btn = tk.Button(parent, text=text, font=self.fonts['body'],
                       bg=bg_color, fg=fg_color, bd=0, relief="flat",
                       cursor="hand2", command=command, padx=20, pady=8)
        
        # 悬停效果
        def on_enter(event):
            btn.configure(bg=hover_color)
        def on_leave(event):
            btn.configure(bg=bg_color)
            
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
        return btn
        
    def create_inventory_interface(self):
        """创建库存管理界面"""
        # 主容器
        main_container = tk.Frame(self.parent_frame, bg=self.colors['background'])
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # 顶部统计卡片
        self.create_stats_cards(main_container)
        
        # 中间筛选和搜索区域
        self.create_filter_section(main_container)
        
        # 底部库存列表
        self.create_inventory_list(main_container)
        
    def create_stats_cards(self, parent):
        """创建统计卡片"""
        stats_frame = tk.Frame(parent, bg=self.colors['background'])
        stats_frame.pack(fill="x", pady=(0, 20))
        
        # 计算统计数据
        total_items = len(self.inventory_data)
        low_stock_items = len([item for item in self.inventory_data if item['current_stock'] <= item['min_stock']])
        total_value = sum(item['current_stock'] * item['price'] for item in self.inventory_data)
        out_of_stock = len([item for item in self.inventory_data if item['current_stock'] == 0])
        
        cards_data = [
            {"title": "商品总数", "value": f"{total_items}", "icon": "📦", "color": self.colors['primary']},
            {"title": "库存不足", "value": f"{low_stock_items}", "icon": "⚠️", "color": self.colors['warning']},
            {"title": "库存总值", "value": f"¥{total_value:,.0f}", "icon": "💰", "color": self.colors['success']},
            {"title": "缺货商品", "value": f"{out_of_stock}", "icon": "🚫", "color": self.colors['error']}
        ]
        
        for i, card_data in enumerate(cards_data):
            self.create_stats_card(stats_frame, card_data, i)
            
    def create_stats_card(self, parent, data, index):
        """创建单个统计卡片"""
        card_frame = tk.Frame(parent, bg=self.colors['surface'], relief="flat", bd=1)
        card_frame.grid(row=0, column=index, padx=10, pady=10, sticky="ew")
        
        # 配置网格权重
        parent.grid_columnconfigure(index, weight=1)
        
        # 卡片内容
        content_frame = tk.Frame(card_frame, bg=self.colors['surface'])
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # 图标和标题行
        header_frame = tk.Frame(content_frame, bg=self.colors['surface'])
        header_frame.pack(fill="x", pady=(0, 10))
        
        icon_label = tk.Label(header_frame, text=data["icon"], font=('Segoe UI Emoji', 24),
                             bg=self.colors['surface'], fg=data["color"])
        icon_label.pack(side="left")
        
        title_label = tk.Label(header_frame, text=data["title"], font=self.fonts['body'],
                              bg=self.colors['surface'], fg=self.colors['text_secondary'])
        title_label.pack(side="right")
        
        # 数值
        value_label = tk.Label(content_frame, text=data["value"], font=self.fonts['title'],
                              bg=self.colors['surface'], fg=self.colors['text_primary'])
        value_label.pack(anchor="w")
        
        # 保存引用用于更新
        self.stats_labels[data["title"]] = value_label
        
    def create_filter_section(self, parent):
        """创建筛选区域"""
        filter_frame = tk.Frame(parent, bg=self.colors['surface'], height=80)
        filter_frame.pack(fill="x", pady=(0, 20))
        filter_frame.pack_propagate(False)
        
        content_frame = tk.Frame(filter_frame, bg=self.colors['surface'])
        content_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        # 搜索框
        search_frame = tk.Frame(content_frame, bg=self.colors['surface'])
        search_frame.pack(side="left", fill="y")
        
        search_label = tk.Label(search_frame, text="🔍 搜索商品", font=self.fonts['subheading'],
                               bg=self.colors['surface'], fg=self.colors['text_primary'])
        search_label.pack(side="left")
        
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, font=self.fonts['body'],
                               bg=self.colors['background'], fg=self.colors['text_primary'],
                               bd=1, relief="solid", width=25)
        search_entry.pack(side="left", padx=(20, 10), ipady=8)
        
        search_btn = tk.Button(search_frame, text="搜索", font=self.fonts['body'],
                              bg=self.colors['primary'], fg="white", bd=0,
                              cursor="hand2", command=self.search_inventory, padx=15)
        search_btn.pack(side="left")
        
        # 筛选器
        filter_controls = tk.Frame(content_frame, bg=self.colors['surface'])
        filter_controls.pack(side="right", fill="y")
        
        # 分类筛选
        category_label = tk.Label(filter_controls, text="分类:", font=self.fonts['body'],
                                 bg=self.colors['surface'], fg=self.colors['text_secondary'])
        category_label.pack(side="left", padx=(0, 5))
        
        categories = ["全部", "肉类", "蔬菜", "主食", "禽蛋", "调料"]
        category_combo = ttk.Combobox(filter_controls, textvariable=self.category_filter_var,
                                     values=categories, state="readonly", width=10)
        category_combo.pack(side="left", padx=(0, 20))
        category_combo.bind('<<ComboboxSelected>>', lambda e: self.filter_inventory())
        
        # 库存状态筛选
        stock_label = tk.Label(filter_controls, text="库存状态:", font=self.fonts['body'],
                              bg=self.colors['surface'], fg=self.colors['text_secondary'])
        stock_label.pack(side="left", padx=(0, 5))
        
        stock_status = ["全部", "正常", "不足", "缺货"]
        stock_combo = ttk.Combobox(filter_controls, textvariable=self.stock_filter_var,
                                  values=stock_status, state="readonly", width=10)
        stock_combo.pack(side="left")
        stock_combo.bind('<<ComboboxSelected>>', lambda e: self.filter_inventory())
        
        # 绑定回车键搜索
        search_entry.bind('<Return>', lambda e: self.search_inventory())
        
    def create_inventory_list(self, parent):
        """创建库存列表"""
        list_frame = tk.Frame(parent, bg=self.colors['surface'])
        list_frame.pack(fill="both", expand=True)
        
        # 标题
        title_frame = tk.Frame(list_frame, bg=self.colors['surface'])
        title_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        title_label = tk.Label(title_frame, text="📋 库存清单", font=self.fonts['heading'],
                              bg=self.colors['surface'], fg=self.colors['text_primary'])
        title_label.pack(side="left")
        
        # 创建表格
        table_frame = tk.Frame(list_frame, bg=self.colors['surface'])
        table_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # 定义列
        columns = ("ID", "商品名称", "分类", "当前库存", "最小库存", "单位", "单价", "状态", "供应商", "更新时间")
        
        # 创建Treeview
        self.inventory_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        
        # 设置列标题和宽度
        column_widths = {
            "ID": 50,
            "商品名称": 120,
            "分类": 80,
            "当前库存": 80,
            "最小库存": 80,
            "单位": 60,
            "单价": 80,
            "状态": 80,
            "供应商": 150,
            "更新时间": 100
        }
        
        for col in columns:
            self.inventory_tree.heading(col, text=col)
            self.inventory_tree.column(col, width=column_widths.get(col, 100), anchor="center")
        
        # 滚动条
        v_scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.inventory_tree.yview)
        h_scrollbar = ttk.Scrollbar(table_frame, orient="horizontal", command=self.inventory_tree.xview)
        
        self.inventory_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # 布局
        self.inventory_tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        # 配置网格权重
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        # 绑定双击事件
        self.inventory_tree.bind("<Double-1>", self.edit_inventory_item)
        
        # 右键菜单
        self.create_context_menu()
        
        # 加载数据
        self.refresh_inventory_list()
        
    def create_context_menu(self):
        """创建右键菜单"""
        self.context_menu = tk.Menu(self.inventory_tree, tearoff=0)
        self.context_menu.add_command(label="编辑", command=self.edit_selected_item)
        self.context_menu.add_command(label="删除", command=self.delete_selected_item)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="补货", command=self.restock_item)
        self.context_menu.add_command(label="调整库存", command=self.adjust_stock)
        
        def show_context_menu(event):
            try:
                self.context_menu.tk_popup(event.x_root, event.y_root)
            finally:
                self.context_menu.grab_release()
        
        self.inventory_tree.bind("<Button-3>", show_context_menu)
        
    def refresh_inventory_list(self):
        """刷新库存列表"""
        # 清空现有数据
        for item in self.inventory_tree.get_children():
            self.inventory_tree.delete(item)
        
        # 获取筛选后的数据
        filtered_data = self.get_filtered_data()
        
        # 插入数据
        for item in filtered_data:
            # 判断库存状态
            if item['current_stock'] == 0:
                status = "缺货"
                status_color = "red"
            elif item['current_stock'] <= item['min_stock']:
                status = "不足"
                status_color = "orange"
            else:
                status = "正常"
                status_color = "green"
            
            # 插入行
            item_id = self.inventory_tree.insert("", "end", values=(
                item['id'],
                item['name'],
                item['category'],
                item['current_stock'],
                item['min_stock'],
                item['unit'],
                f"¥{item['price']:.2f}",
                status,
                item['supplier'],
                item['last_updated']
            ))
            
            # 根据状态设置行颜色
            if status == "缺货":
                self.inventory_tree.set(item_id, "状态", "🚫 缺货")
            elif status == "不足":
                self.inventory_tree.set(item_id, "状态", "⚠️ 不足")
            else:
                self.inventory_tree.set(item_id, "状态", "✅ 正常")
        
        # 更新统计卡片
        self.update_stats_cards()
        
    def get_filtered_data(self):
        """获取筛选后的数据"""
        filtered_data = self.inventory_data.copy()
        
        # 按搜索关键词筛选
        search_term = self.search_var.get().strip().lower()
        if search_term:
            filtered_data = [item for item in filtered_data 
                           if search_term in item['name'].lower() or 
                              search_term in item['category'].lower() or
                              search_term in item['supplier'].lower()]
        
        # 按分类筛选
        category_filter = self.category_filter_var.get()
        if category_filter != "全部":
            filtered_data = [item for item in filtered_data if item['category'] == category_filter]
        
        # 按库存状态筛选
        stock_filter = self.stock_filter_var.get()
        if stock_filter != "全部":
            if stock_filter == "正常":
                filtered_data = [item for item in filtered_data if item['current_stock'] > item['min_stock']]
            elif stock_filter == "不足":
                filtered_data = [item for item in filtered_data if 0 < item['current_stock'] <= item['min_stock']]
            elif stock_filter == "缺货":
                filtered_data = [item for item in filtered_data if item['current_stock'] == 0]
        
        return filtered_data
        
    def update_stats_cards(self):
        """更新统计卡片"""
        filtered_data = self.get_filtered_data()
        
        total_items = len(filtered_data)
        low_stock_items = len([item for item in filtered_data if item['current_stock'] <= item['min_stock']])
        total_value = sum(item['current_stock'] * item['price'] for item in filtered_data)
        out_of_stock = len([item for item in filtered_data if item['current_stock'] == 0])
        
        # 更新标签
        if "商品总数" in self.stats_labels:
            self.stats_labels["商品总数"].configure(text=f"{total_items}")
        if "库存不足" in self.stats_labels:
            self.stats_labels["库存不足"].configure(text=f"{low_stock_items}")
        if "库存总值" in self.stats_labels:
            self.stats_labels["库存总值"].configure(text=f"¥{total_value:,.0f}")
        if "缺货商品" in self.stats_labels:
            self.stats_labels["缺货商品"].configure(text=f"{out_of_stock}")
            
    def search_inventory(self):
        """搜索库存"""
        self.refresh_inventory_list()
        
    def filter_inventory(self):
        """筛选库存"""
        self.refresh_inventory_list()
        
    def add_inventory_item(self):
        """添加库存商品"""
        dialog = InventoryItemDialog(self.parent_frame, "添加商品")
        if dialog.result:
            # 生成新ID
            new_id = max([item['id'] for item in self.inventory_data], default=0) + 1
            dialog.result['id'] = new_id
            dialog.result['last_updated'] = datetime.datetime.now().strftime("%Y-%m-%d")
            
            # 添加到数据
            self.inventory_data.append(dialog.result)
            self.refresh_inventory_list()
            messagebox.showinfo("成功", "商品添加成功！")
            
    def edit_inventory_item(self, event):
        """编辑库存商品"""
        self.edit_selected_item()
        
    def edit_selected_item(self):
        """编辑选中的商品"""
        selected = self.inventory_tree.selection()
        if not selected:
            messagebox.showwarning("提示", "请选择要编辑的商品")
            return
            
        item_id = int(self.inventory_tree.item(selected[0])['values'][0])
        item_data = next((item for item in self.inventory_data if item['id'] == item_id), None)
        
        if item_data:
            dialog = InventoryItemDialog(self.parent_frame, "编辑商品", item_data)
            if dialog.result:
                # 更新数据
                item_data.update(dialog.result)
                item_data['last_updated'] = datetime.datetime.now().strftime("%Y-%m-%d")
                self.refresh_inventory_list()
                messagebox.showinfo("成功", "商品信息更新成功！")
                
    def delete_selected_item(self):
        """删除选中的商品"""
        selected = self.inventory_tree.selection()
        if not selected:
            messagebox.showwarning("提示", "请选择要删除的商品")
            return
            
        item_name = self.inventory_tree.item(selected[0])['values'][1]
        if messagebox.askyesno("确认删除", f"确定要删除商品 '{item_name}' 吗？"):
            item_id = int(self.inventory_tree.item(selected[0])['values'][0])
            self.inventory_data = [item for item in self.inventory_data if item['id'] != item_id]
            self.refresh_inventory_list()
            messagebox.showinfo("成功", "商品删除成功！")
            
    def restock_item(self):
        """补货"""
        selected = self.inventory_tree.selection()
        if not selected:
            messagebox.showwarning("提示", "请选择要补货的商品")
            return
            
        item_id = int(self.inventory_tree.item(selected[0])['values'][0])
        item_data = next((item for item in self.inventory_data if item['id'] == item_id), None)
        
        if item_data:
            quantity = simpledialog.askinteger("补货", f"请输入 {item_data['name']} 的补货数量：", minvalue=1)
            if quantity:
                item_data['current_stock'] += quantity
                item_data['last_updated'] = datetime.datetime.now().strftime("%Y-%m-%d")
                self.refresh_inventory_list()
                messagebox.showinfo("成功", f"已为 {item_data['name']} 补货 {quantity} {item_data['unit']}")
                
    def adjust_stock(self):
        """调整库存"""
        selected = self.inventory_tree.selection()
        if not selected:
            messagebox.showwarning("提示", "请选择要调整库存的商品")
            return
            
        item_id = int(self.inventory_tree.item(selected[0])['values'][0])
        item_data = next((item for item in self.inventory_data if item['id'] == item_id), None)
        
        if item_data:
            new_stock = simpledialog.askinteger("调整库存", 
                                               f"{item_data['name']} 当前库存：{item_data['current_stock']} {item_data['unit']}\n请输入新的库存数量：", 
                                               minvalue=0)
            if new_stock is not None:
                item_data['current_stock'] = new_stock
                item_data['last_updated'] = datetime.datetime.now().strftime("%Y-%m-%d")
                self.refresh_inventory_list()
                messagebox.showinfo("成功", f"{item_data['name']} 库存已调整为 {new_stock} {item_data['unit']}")
                
    def export_report(self):
        """导出报表"""
        messagebox.showinfo("导出报表", "报表导出功能开发中...")

class InventoryItemDialog:
    """库存商品对话框"""
    def __init__(self, parent, title, item_data=None):
        self.result = None
        
        # 创建对话框窗口
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("500x600")
        self.dialog.configure(bg="#f8f9fa")
        self.dialog.resizable(False, False)
        self.dialog.grab_set()
        
        # 居中显示
        self.dialog.transient(parent)
        self.center_window()
        
        # 颜色主题
        self.colors = {
            'primary': '#FF6B35',
            'background': '#F8F9FA',
            'surface': '#FFFFFF',
            'text_primary': '#2D3436',
            'text_secondary': '#636E72',
            'border': '#E0E0E0'
        }
        
        # 字体
        self.fonts = {
            'heading': ('Microsoft YaHei UI', 16, 'bold'),
            'body': ('Microsoft YaHei UI', 12),
            'button': ('Microsoft YaHei UI', 11, 'bold')
        }
          # 创建变量
        self.name_var = tk.StringVar(self.dialog, value=item_data['name'] if item_data else "")
        self.category_var = tk.StringVar(self.dialog, value=item_data['category'] if item_data else "")
        self.current_stock_var = tk.IntVar(self.dialog, value=item_data['current_stock'] if item_data else 0)
        self.min_stock_var = tk.IntVar(self.dialog, value=item_data['min_stock'] if item_data else 0)
        self.max_stock_var = tk.IntVar(self.dialog, value=item_data['max_stock'] if item_data else 0)
        self.unit_var = tk.StringVar(self.dialog, value=item_data['unit'] if item_data else "")
        self.price_var = tk.DoubleVar(self.dialog, value=item_data['price'] if item_data else 0.0)
        self.supplier_var = tk.StringVar(self.dialog, value=item_data['supplier'] if item_data else "")
        
        # 创建界面
        self.create_dialog_ui()
        
    def center_window(self):
        """窗口居中"""
        self.dialog.update_idletasks()
        width = self.dialog.winfo_width()
        height = self.dialog.winfo_height()
        x = (self.dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (height // 2)
        self.dialog.geometry(f'{width}x{height}+{x}+{y}')
        
    def create_dialog_ui(self):
        """创建对话框界面"""
        # 主容器
        main_frame = tk.Frame(self.dialog, bg=self.colors['surface'])
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # 标题
        title_label = tk.Label(main_frame, text="📦 商品信息", font=self.fonts['heading'],
                              bg=self.colors['surface'], fg=self.colors['text_primary'])
        title_label.pack(pady=(0, 20))
        
        # 表单字段
        fields = [
            ("商品名称 *", self.name_var, "entry"),
            ("商品分类 *", self.category_var, "combo", ["主食", "肉类", "蔬菜", "禽蛋", "调料", "其他"]),
            ("当前库存 *", self.current_stock_var, "entry"),
            ("最小库存 *", self.min_stock_var, "entry"),
            ("最大库存 *", self.max_stock_var, "entry"),
            ("单位 *", self.unit_var, "combo", ["公斤", "克", "升", "毫升", "个", "包", "盒", "袋"]),
            ("单价 *", self.price_var, "entry"),
            ("供应商", self.supplier_var, "entry")
        ]
        
        for field_name, field_var, field_type, *options in fields:
            self.create_form_field(main_frame, field_name, field_var, field_type, options[0] if options else None)
        
        # 按钮区域
        button_frame = tk.Frame(main_frame, bg=self.colors['surface'])
        button_frame.pack(fill="x", pady=(20, 0))
        
        # 取消按钮
        cancel_btn = tk.Button(button_frame, text="取消", font=self.fonts['button'],
                              bg=self.colors['background'], fg=self.colors['text_secondary'],
                              bd=0, relief="flat", cursor="hand2", command=self.cancel,
                              padx=30, pady=10)
        cancel_btn.pack(side="right", padx=(10, 0))
        
        # 确定按钮
        ok_btn = tk.Button(button_frame, text="确定", font=self.fonts['button'],
                          bg=self.colors['primary'], fg="white",
                          bd=0, relief="flat", cursor="hand2", command=self.ok,
                          padx=30, pady=10)
        ok_btn.pack(side="right")
        
    def create_form_field(self, parent, label_text, variable, field_type, options=None):
        """创建表单字段"""
        field_frame = tk.Frame(parent, bg=self.colors['surface'])
        field_frame.pack(fill="x", pady=10)
        
        # 标签
        label = tk.Label(field_frame, text=label_text, font=self.fonts['body'],
                        bg=self.colors['surface'], fg=self.colors['text_secondary'], anchor="w")
        label.pack(fill="x", pady=(0, 5))
        
        # 输入控件
        if field_type == "entry":
            entry = tk.Entry(field_frame, textvariable=variable, font=self.fonts['body'],
                            bg=self.colors['background'], bd=1, relief="solid")
            entry.pack(fill="x", ipady=8)
        elif field_type == "combo" and options:
            combo = ttk.Combobox(field_frame, textvariable=variable, values=options,
                                font=self.fonts['body'], state="readonly")
            combo.pack(fill="x", ipady=5)
            
    def ok(self):
        """确定按钮处理"""
        # 验证必填字段
        if not self.name_var.get().strip():
            messagebox.showerror("错误", "请输入商品名称")
            return
        if not self.category_var.get().strip():
            messagebox.showerror("错误", "请选择商品分类")
            return
        if not self.unit_var.get().strip():
            messagebox.showerror("错误", "请选择单位")
            return
            
        # 验证数值
        try:
            current_stock = self.current_stock_var.get()
            min_stock = self.min_stock_var.get()
            max_stock = self.max_stock_var.get()
            price = self.price_var.get()
            
            if current_stock < 0 or min_stock < 0 or max_stock < 0 or price < 0:
                messagebox.showerror("错误", "数值不能为负数")
                return
                
            if min_stock > max_stock:
                messagebox.showerror("错误", "最小库存不能大于最大库存")
                return
                
        except tk.TclError:
            messagebox.showerror("错误", "请输入有效的数值")
            return
        
        # 保存结果
        self.result = {
            'name': self.name_var.get().strip(),
            'category': self.category_var.get(),
            'current_stock': current_stock,
            'min_stock': min_stock,
            'max_stock': max_stock,
            'unit': self.unit_var.get(),
            'price': price,
            'supplier': self.supplier_var.get().strip()
        }
        
        self.dialog.destroy()
        
    def cancel(self):
        """取消按钮处理"""
        self.dialog.destroy()

if __name__ == "__main__":
    # 测试代码
    root = tk.Tk()
    root.title("现代化库存管理模块测试")
    root.geometry("1400x900")
    root.configure(bg="#f8f9fa")
    
    title_frame = tk.Frame(root, bg="#ffffff", height=70)
    title_frame.pack(fill="x")
    title_frame.pack_propagate(False)
    
    main_frame = tk.Frame(root, bg="#f8f9fa")
    main_frame.pack(fill="both", expand=True)
    
    inventory_module = ModernInventoryModule(main_frame, title_frame)
    inventory_module.show()
    
    root.mainloop()
