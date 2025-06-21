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

# 导入数据管理器
try:
    from ..utils.data_manager import data_manager
except ImportError:
    try:
        from data_manager import data_manager
    except ImportError:
        # 创建模拟数据管理器
        class MockDataManager:
            def get_inventory(self):
                return []
            def save_data(self, data_type, data):
                return True
            def update_inventory(self, item_id, quantity):
                return True
        data_manager = MockDataManager()

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
            'card_shadow': '#F0F0F0',  # 卡片阴影
            'white': '#FFFFFF',        # 白色
            'info': '#3498DB'          # 信息色
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
        self.inventory_data = self.load_inventory_data()        # 界面变量 (延迟初始化)
        self.search_var = None
        self.category_filter_var = None
        self.stock_filter_var = None
          # UI组件引用
        self.inventory_tree = None
        self.stats_labels = {}
    
    def load_inventory_data(self):
        """从数据管理中心加载库存数据"""
        try:
            # 从数据管理器获取库存数据
            inventory_data = data_manager.get_inventory()
            
            # 转换数据格式以适配现有界面
            formatted_data = []
            for item in inventory_data:
                formatted_item = {
                    "id": item.get('id', ''),
                    "name": item.get('name', ''),
                    "category": item.get('category', ''),
                    "current_stock": item.get('quantity', 0),
                    "min_stock": item.get('min_stock', 0),
                    "max_stock": item.get('max_stock', 100),
                    "unit": item.get('unit', '个'),
                    "price": item.get('price', 0.0),
                    "supplier": item.get('supplier', '未知供应商'),
                    "last_updated": item.get('update_time', datetime.datetime.now().strftime('%Y-%m-%d'))
                }
                formatted_data.append(formatted_item)
            
            return formatted_data
        except Exception as e:
            print(f"加载库存数据失败: {e}")            # 返回丰富的默认示例数据
            return [
                # 蔬菜类
                {"id": "INV001", "name": "番茄", "category": "蔬菜", "current_stock": 50, "min_stock": 10, "max_stock": 100, "unit": "kg", "price": 8.0, "supplier": "优质蔬菜供应商", "last_updated": "2025-06-21"},
                {"id": "INV002", "name": "洋葱", "category": "蔬菜", "current_stock": 30, "min_stock": 8, "max_stock": 80, "unit": "kg", "price": 6.0, "supplier": "优质蔬菜供应商", "last_updated": "2025-06-21"},
                {"id": "INV003", "name": "青椒", "category": "蔬菜", "current_stock": 25, "min_stock": 5, "max_stock": 60, "unit": "kg", "price": 12.0, "supplier": "优质蔬菜供应商", "last_updated": "2025-06-21"},
                {"id": "INV004", "name": "生菜", "category": "蔬菜", "current_stock": 40, "min_stock": 10, "max_stock": 80, "unit": "kg", "price": 10.0, "supplier": "优质蔬菜供应商", "last_updated": "2025-06-21"},
                {"id": "INV005", "name": "胡萝卜", "category": "蔬菜", "current_stock": 35, "min_stock": 8, "max_stock": 70, "unit": "kg", "price": 7.0, "supplier": "优质蔬菜供应商", "last_updated": "2025-06-21"},
                
                # 肉类
                {"id": "INV010", "name": "牛肉", "category": "肉类", "current_stock": 20, "min_stock": 5, "max_stock": 50, "unit": "kg", "price": 68.0, "supplier": "优质肉类供应商", "last_updated": "2025-06-21"},
                {"id": "INV011", "name": "猪肉", "category": "肉类", "current_stock": 25, "min_stock": 5, "max_stock": 60, "unit": "kg", "price": 28.0, "supplier": "优质肉类供应商", "last_updated": "2025-06-21"},
                {"id": "INV012", "name": "鸡胸肉", "category": "肉类", "current_stock": 15, "min_stock": 3, "max_stock": 40, "unit": "kg", "price": 22.0, "supplier": "优质肉类供应商", "last_updated": "2025-06-21"},
                {"id": "INV013", "name": "鸡蛋", "category": "肉类", "current_stock": 200, "min_stock": 50, "max_stock": 300, "unit": "个", "price": 1.2, "supplier": "优质肉类供应商", "last_updated": "2025-06-21"},
                
                # 主食类
                {"id": "INV020", "name": "面条", "category": "主食", "current_stock": 100, "min_stock": 20, "max_stock": 200, "unit": "包", "price": 3.5, "supplier": "优质粮食供应商", "last_updated": "2025-06-21"},
                {"id": "INV021", "name": "大米", "category": "主食", "current_stock": 80, "min_stock": 15, "max_stock": 150, "unit": "kg", "price": 4.5, "supplier": "优质粮食供应商", "last_updated": "2025-06-21"},
                {"id": "INV022", "name": "面包", "category": "主食", "current_stock": 60, "min_stock": 20, "max_stock": 120, "unit": "个", "price": 8.0, "supplier": "优质粮食供应商", "last_updated": "2025-06-21"},
                {"id": "INV023", "name": "土豆", "category": "主食", "current_stock": 45, "min_stock": 10, "max_stock": 90, "unit": "kg", "price": 5.0, "supplier": "优质蔬菜供应商", "last_updated": "2025-06-21"},
                
                # 饮料类
                {"id": "INV030", "name": "可乐", "category": "饮料", "current_stock": 80, "min_stock": 30, "max_stock": 150, "unit": "瓶", "price": 5.0, "supplier": "饮料供应商", "last_updated": "2025-06-21"},
                {"id": "INV031", "name": "雪碧", "category": "饮料", "current_stock": 75, "min_stock": 25, "max_stock": 120, "unit": "瓶", "price": 5.0, "supplier": "饮料供应商", "last_updated": "2025-06-21"},
                {"id": "INV032", "name": "橙汁", "category": "饮料", "current_stock": 50, "min_stock": 20, "max_stock": 100, "unit": "瓶", "price": 8.0, "supplier": "饮料供应商", "last_updated": "2025-06-21"},
                {"id": "INV033", "name": "咖啡豆", "category": "饮料", "current_stock": 5, "min_stock": 2, "max_stock": 20, "unit": "kg", "price": 180.0, "supplier": "咖啡供应商", "last_updated": "2025-06-21"},
                {"id": "INV034", "name": "牛奶", "category": "饮料", "current_stock": 40, "min_stock": 15, "max_stock": 80, "unit": "瓶", "price": 6.0, "supplier": "乳制品供应商", "last_updated": "2025-06-21"},
                
                # 调料类
                {"id": "INV040", "name": "食用油", "category": "调料", "current_stock": 10, "min_stock": 3, "max_stock": 25, "unit": "瓶", "price": 25.0, "supplier": "调料供应商", "last_updated": "2025-06-21"},
                {"id": "INV041", "name": "生抽", "category": "调料", "current_stock": 8, "min_stock": 2, "max_stock": 20, "unit": "瓶", "price": 12.0, "supplier": "调料供应商", "last_updated": "2025-06-21"},
                {"id": "INV042", "name": "老抽", "category": "调料", "current_stock": 6, "min_stock": 2, "max_stock": 15, "unit": "瓶", "price": 15.0, "supplier": "调料供应商", "last_updated": "2025-06-21"},
                {"id": "INV043", "name": "盐", "category": "调料", "current_stock": 20, "min_stock": 5, "max_stock": 50, "unit": "包", "price": 3.0, "supplier": "调料供应商", "last_updated": "2025-06-21"},
                {"id": "INV044", "name": "糖", "category": "调料", "current_stock": 15, "min_stock": 3, "max_stock": 30, "unit": "包", "price": 8.0, "supplier": "调料供应商", "last_updated": "2025-06-21"},
                {"id": "INV045", "name": "辣椒粉", "category": "调料", "current_stock": 12, "min_stock": 3, "max_stock": 25, "unit": "包", "price": 18.0, "supplier": "调料供应商", "last_updated": "2025-06-21"}
            ]
    
    def show(self):
        """显示库存管理模块"""
        # 注册到数据管理器
        data_manager.register_module('inventory', self)
        
        # 重新加载最新数据
        self.inventory_data = self.load_inventory_data()
          # 初始化界面变量（如果还没有初始化）
        if self.search_var is None:
            self.search_var = tk.StringVar(self.parent_frame)
            self.category_filter_var = tk.StringVar(self.parent_frame, value="全部")
            self.stock_filter_var = tk.StringVar(self.parent_frame, value="全部")
        
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
        
        # 刷新按钮
        refresh_btn = tk.Button(action_frame, text="🔄 刷新", 
                               font=('Microsoft YaHei UI', 10),
                               bg=self.colors['primary'], fg=self.colors['white'],
                               bd=0, padx=20, pady=8, cursor='hand2',
                               command=self.refresh_inventory)
        refresh_btn.pack(side='right', padx=5)
        
        # 导出按钮
        export_btn = tk.Button(action_frame, text="📊 导出", 
                              font=('Microsoft YaHei UI', 10),
                              bg=self.colors['success'], fg=self.colors['white'],
                              bd=0, padx=20, pady=8, cursor='hand2',
                              command=self.export_inventory)
        export_btn.pack(side='right', padx=5)
        
    def create_inventory_interface(self):
        """创建库存管理界面"""        # 主容器
        main_container = tk.Frame(self.parent_frame, bg=self.colors['background'])
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # 顶部统计卡片 - 已隐藏
        # self.create_stats_cards(main_container)
          # 可制作菜品展示区域
        self.create_possible_meals_section(main_container)
        
        # 中间筛选和搜索区域 - 已隐藏
        # self.create_filter_section(main_container)
        
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
        
        title_label = tk.Label(title_frame, text="🥬 食材库存清单", font=self.fonts['heading'],
                              bg=self.colors['surface'], fg=self.colors['text_primary'])
        title_label.pack(side="left")
        
        # 提示信息
        tip_label = tk.Label(title_frame, text="（仅显示原材料，不含成品菜品）", 
                            font=self.fonts['small'],
                            bg=self.colors['surface'], fg=self.colors['text_secondary'])
        tip_label.pack(side="left", padx=(10, 0))
        
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
                item['last_updated']            ))
            
            # 根据状态设置行颜色
            if status == "缺货":
                self.inventory_tree.set(item_id, "状态", "🚫 缺货")
            elif status == "不足":
                self.inventory_tree.set(item_id, "状态", "⚠️ 不足")
            else:
                self.inventory_tree.set(item_id, "状态", "✅ 正常")
        
        # 更新统计卡片 - 已隐藏统计卡片
        # self.update_stats_cards()
    
    def get_filtered_data(self):
        """获取筛选后的数据"""
        filtered_data = self.inventory_data.copy()
        
        # 移除搜索和筛选功能，仅保留食材过滤
        # 按搜索关键词筛选 - 已移除
        # 按分类筛选 - 已移除  
        # 按库存状态筛选 - 已移除
        
        # 过滤只显示食材（原料），不显示成品菜品
        finished_product_keywords = [
            '炒饭', '面条', '汉堡', '红烧肉', '可乐', '米饭', '牛肉面', '炒面',
            '汤', '粥', '饮料', '咖啡', '奶茶', '果汁', '沙拉'
        ]
        
        ingredient_categories = [
            '蔬菜', '肉类', '主食', '调料', '海鲜', '豆制品', '干货', '冷冻食品'
        ]
        
        final_filtered_data = []
        for item in filtered_data:
            item_name = item['name']
            item_category = item['category']
            
            # 检查是否为成品菜品
            is_finished_product = any(keyword in item_name for keyword in finished_product_keywords)
            
            # 检查分类是否为食材分类
            is_ingredient_category = item_category in ingredient_categories
            
            # 只有既不是成品菜品，又属于食材分类的商品才显示
            if not is_finished_product and is_ingredient_category:
                final_filtered_data.append(item)
        
        return final_filtered_data
    
    def filter_ingredients_only(self):
        """过滤只显示食材（原料），不显示成品菜品"""
        # 定义成品菜品的关键词，这些不应该出现在食材库存中
        finished_product_keywords = [
            '炒饭', '面条', '汉堡', '红烧肉', '可乐', '米饭', '牛肉面', '炒面',
            '汤', '粥', '饮料', '咖啡', '奶茶', '果汁', '沙拉'
        ]
        
        # 定义食材分类，只显示这些分类的商品
        ingredient_categories = [
            '蔬菜', '肉类', '主食', '调料', '海鲜', '豆制品', '干货', '冷冻食品'
        ]
        
        filtered_data = []
        for item in self.inventory_data:
            item_name = item['name']
            item_category = item['category']
            
            # 检查是否为成品菜品
            is_finished_product = any(keyword in item_name for keyword in finished_product_keywords)
            
            # 检查分类是否为食材分类
            is_ingredient_category = item_category in ingredient_categories
            
            # 只有既不是成品菜品，又属于食材分类的商品才显示
            if not is_finished_product and is_ingredient_category:
                filtered_data.append(item)
        
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
            # 生成新ID - 找到最大编号并+1
            existing_ids = [item['id'] for item in self.inventory_data if item['id'].startswith('INV')]
            if existing_ids:
                # 提取数字部分，找到最大值
                max_num = max([int(id_str[3:]) for id_str in existing_ids])
                new_id = f"INV{max_num + 1:03d}"  # 格式化为INV001这样的格式
            else:
                new_id = "INV001"
            
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
            
        item_id = self.inventory_tree.item(selected[0])['values'][0]  # 直接获取字符串ID，不转换为int
        item_data = next((item for item in self.inventory_data if item['id'] == item_id), None)
        
        if item_data:
            dialog = InventoryItemDialog(self.parent_frame, "编辑商品", item_data)
            if dialog.result:                # 更新数据
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
            item_id = self.inventory_tree.item(selected[0])['values'][0]  # 直接获取字符串ID
            self.inventory_data = [item for item in self.inventory_data if item['id'] != item_id]
            self.refresh_inventory_list()
            messagebox.showinfo("成功", "商品删除成功！")
            
    def restock_item(self):
        """补货"""
        selected = self.inventory_tree.selection()
        if not selected:
            messagebox.showwarning("提示", "请选择要补货的商品")
            return
            
        item_id = self.inventory_tree.item(selected[0])['values'][0]  # 直接获取字符串ID
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
            
        item_id = self.inventory_tree.item(selected[0])['values'][0]  # 直接获取字符串ID
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
                
    def export_inventory(self):
        """导出库存数据"""
        try:
            from tkinter import filedialog
            import datetime
            
            # 创建导出选择对话框
            dialog = tk.Toplevel(self.parent_frame)
            dialog.title("导出库存数据")
            dialog.geometry("400x300")
            dialog.configure(bg=self.colors['background'])
            dialog.transient(self.parent_frame)
            dialog.grab_set()
            
            # 居中显示
            dialog.update_idletasks()
            x = (dialog.winfo_screenwidth() // 2) - (200)
            y = (dialog.winfo_screenheight() // 2) - (150)
            dialog.geometry(f"400x300+{x}+{y}")
            
            # 标题
            tk.Label(dialog, text="导出库存数据", font=('Microsoft YaHei UI', 14, 'bold'),
                    bg=self.colors['background'], fg=self.colors['text']).pack(pady=15)
            
            # 导出选项框架
            options_frame = tk.Frame(dialog, bg=self.colors['background'])
            options_frame.pack(fill="both", expand=True, padx=20, pady=10)
            
            # 导出格式选择
            tk.Label(options_frame, text="选择导出格式:", font=('Microsoft YaHei UI', 12),
                    bg=self.colors['background'], fg=self.colors['text']).pack(anchor="w", pady=(0, 10))
            
            format_var = tk.StringVar(dialog, value="Excel")
            format_options = ["Excel", "CSV", "PDF"]
            
            format_frame = tk.Frame(options_frame, bg=self.colors['background'])
            format_frame.pack(anchor="w")
            
            for i, fmt in enumerate(format_options):
                rb = tk.Radiobutton(format_frame, text=fmt, variable=format_var, value=fmt,
                                  font=('Microsoft YaHei UI', 10), bg=self.colors['background'], 
                                  fg=self.colors['text'], selectcolor=self.colors['surface'])
                rb.grid(row=0, column=i, sticky="w", padx=(0, 20))
            
            # 库存类型筛选
            tk.Label(options_frame, text="库存类型:", font=('Microsoft YaHei UI', 12),
                    bg=self.colors['background'], fg=self.colors['text']).pack(anchor="w", pady=(20, 10))
            
            type_var = tk.StringVar(dialog, value="全部")
            type_options = ["全部", "原料", "容器"]
            
            type_combo = ttk.Combobox(options_frame, textvariable=type_var, 
                                    values=type_options, state="readonly", width=20)
            type_combo.pack(anchor="w")
            
            # 按钮框架
            btn_frame = tk.Frame(dialog, bg=self.colors['background'])
            btn_frame.pack(fill="x", padx=20, pady=20)
            
            def do_export():
                try:
                    file_format = format_var.get()
                    inventory_type = type_var.get()
                    
                    # 获取当前时间戳
                    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"库存数据_{inventory_type}_{timestamp}"
                    
                    # 选择保存路径
                    if file_format == "Excel":
                        file_path = filedialog.asksaveasfilename(
                            defaultextension=".xlsx",
                            filetypes=[("Excel文件", "*.xlsx")],
                            initialname=filename
                        )
                        if file_path:
                            success = self.export_inventory_to_excel(file_path, inventory_type)
                    elif file_format == "CSV":
                        file_path = filedialog.asksaveasfilename(
                            defaultextension=".csv",
                            filetypes=[("CSV文件", "*.csv")],
                            initialname=filename
                        )
                        if file_path:
                            success = self.export_inventory_to_csv(file_path, inventory_type)
                    elif file_format == "PDF":
                        file_path = filedialog.asksaveasfilename(
                            defaultextension=".pdf",
                            filetypes=[("PDF文件", "*.pdf")],
                            initialname=filename
                        )
                        if file_path:
                            success = self.export_inventory_to_pdf(file_path, inventory_type)
                    
                    if success:
                        messagebox.showinfo("导出成功", f"库存数据已成功导出为 {file_format} 格式", parent=dialog)
                        dialog.destroy()
                    else:
                        messagebox.showerror("导出失败", "导出过程中发生错误", parent=dialog)
                        
                except Exception as e:
                    messagebox.showerror("错误", f"导出失败：{e}", parent=dialog)
            
            tk.Button(btn_frame, text="📊 开始导出", command=do_export,
                     bg=self.colors['primary'], fg='white', bd=0, pady=8, padx=20,
                     font=('Microsoft YaHei UI', 10)).pack(side="left")
            tk.Button(btn_frame, text="取消", command=dialog.destroy,
                     bg=self.colors['text_light'], fg='white', bd=0, pady=8, padx=20,
                     font=('Microsoft YaHei UI', 10)).pack(side="right")
                     
        except Exception as e:
            messagebox.showerror("错误", f"打开导出对话框失败：{e}")
    
    def export_inventory_to_excel(self, file_path: str, inventory_type: str) -> bool:
        """导出库存为Excel格式"""
        try:
            import openpyxl
            from openpyxl.styles import Font, Alignment, PatternFill
            
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "库存数据"
            
            # 设置标题
            title = f"智慧餐饮管理系统 - 库存数据 ({inventory_type})"
            ws['A1'] = title
            ws['A1'].font = Font(size=16, bold=True)
            ws.merge_cells('A1:F1')
            
            # 设置表头样式
            header_font = Font(bold=True, color="FFFFFF")
            header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
            header_alignment = Alignment(horizontal="center", vertical="center")
            
            # 表头
            headers = ["物品名称", "类型", "当前库存", "单位", "预警阈值", "状态"]
            ws.append(headers)
            
            # 设置表头样式
            for cell in ws[2]:
                cell.font = header_font
                cell.fill = header_fill
                cell.alignment = header_alignment
            
            # 获取库存数据
            inventory_data = self.get_filtered_inventory(inventory_type)
            
            # 添加数据
            for item in inventory_data:
                # 判断库存状态
                current_stock = item.get('stock', 0)
                warning_threshold = item.get('warning_threshold', 0)
                status = "正常" if current_stock > warning_threshold else "预警"
                
                row = [
                    item.get('name', ''),
                    item.get('type', ''),
                    current_stock,
                    item.get('unit', ''),
                    warning_threshold,
                    status
                ]
                ws.append(row)
            
            # 调整列宽
            for column in ws.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 50)
                ws.column_dimensions[column_letter].width = adjusted_width
            
            wb.save(file_path)
            return True
            
        except ImportError:
            messagebox.showerror("错误", "请安装openpyxl库：pip install openpyxl")
            return False
        except Exception as e:
            print(f"导出Excel失败: {e}")
            return False
    
    def export_inventory_to_csv(self, file_path: str, inventory_type: str) -> bool:
        """导出库存为CSV格式"""
        try:
            import csv
            
            with open(file_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
                fieldnames = ["物品名称", "类型", "当前库存", "单位", "预警阈值", "状态"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                # 获取库存数据
                inventory_data = self.get_filtered_inventory(inventory_type)
                
                for item in inventory_data:
                    # 判断库存状态
                    current_stock = item.get('stock', 0)
                    warning_threshold = item.get('warning_threshold', 0)
                    status = "正常" if current_stock > warning_threshold else "预警"
                    
                    writer.writerow({
                        "物品名称": item.get('name', ''),
                        "类型": item.get('type', ''),
                        "当前库存": current_stock,
                        "单位": item.get('unit', ''),
                        "预警阈值": warning_threshold,
                        "状态": status
                    })
            
            return True
            
        except Exception as e:
            print(f"导出CSV失败: {e}")
            return False
    
    def export_inventory_to_pdf(self, file_path: str, inventory_type: str) -> bool:
        """导出库存为PDF格式"""
        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib import colors
            
            doc = SimpleDocTemplate(file_path, pagesize=A4)
            story = []
            
            # 标题样式
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=16,
                spaceAfter=30,
                alignment=1  # 居中
            )
            
            # 添加标题
            title = Paragraph(f"智慧餐饮管理系统 - 库存数据 ({inventory_type})", title_style)
            story.append(title)
            story.append(Spacer(1, 20))
            
            # 获取库存数据
            inventory_data = self.get_filtered_inventory(inventory_type)
            
            # 创建表格数据
            table_data = [["物品名称", "类型", "当前库存", "单位", "预警阈值", "状态"]]
            
            for item in inventory_data:
                # 判断库存状态
                current_stock = item.get('stock', 0)
                warning_threshold = item.get('warning_threshold', 0)
                status = "正常" if current_stock > warning_threshold else "预警"
                
                row = [
                    item.get('name', ''),
                    item.get('type', ''),
                    current_stock,
                    item.get('unit', ''),
                    warning_threshold,
                    status
                ]
                table_data.append(row)
            
            # 创建表格
            table = Table(table_data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.beige, colors.white])
            ]))
            story.append(table)
            
            doc.build(story)
            return True
            
        except ImportError:
            messagebox.showerror("错误", "请安装reportlab库：pip install reportlab")
            return False
        except Exception as e:
            print(f"导出PDF失败: {e}")
            return False
    
    def get_filtered_inventory(self, inventory_type: str) -> List[Dict]:
        """获取筛选后的库存数据"""
        if inventory_type == "全部":
            return self.inventory_data
        else:
            return [item for item in self.inventory_data if item.get('type') == inventory_type]
    
    def refresh_inventory(self):
        """刷新库存数据"""
        try:
            # 重新加载库存数据
            self.inventory_data = self.load_inventory_data()
            # 重新显示库存列表
            self.refresh_inventory_list()
            # 刷新可制作菜品
            self.refresh_possible_meals()
            messagebox.showinfo("刷新成功", "库存数据已刷新")
        except Exception as e:
            messagebox.showerror("刷新失败", f"刷新库存数据时发生错误：{e}")
    
    def load_recipe_data(self):
        """加载配方数据"""
        try:
            recipes_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'recipes.json')
            if os.path.exists(recipes_file):
                with open(recipes_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                print("配方文件不存在，使用默认配方")
                return self.get_default_recipes()
        except Exception as e:
            print(f"加载配方数据失败: {e}")
            return self.get_default_recipes()
    
    def get_default_recipes(self):
        """获取默认配方数据"""
        return [
            {
                "meal_id": "MEAL001",
                "meal_name": "番茄牛肉面",
                "ingredients": [
                    {"ingredient_name": "番茄", "quantity_per_serving": 0.2, "unit": "kg"},
                    {"ingredient_name": "牛肉", "quantity_per_serving": 0.15, "unit": "kg"},
                    {"ingredient_name": "面条", "quantity_per_serving": 0.25, "unit": "包"}
                ]
            },
            {
                "meal_id": "MEAL002",
                "meal_name": "鸡蛋炒饭",
                "ingredients": [
                    {"ingredient_name": "鸡蛋", "quantity_per_serving": 2, "unit": "个"},
                    {"ingredient_name": "大米", "quantity_per_serving": 0.3, "unit": "kg"}
                ]
            }
        ]
    
    def calculate_possible_meals(self):
        """计算当前库存可制作的菜品数量"""
        recipes = self.load_recipe_data()
        inventory_dict = {item['name']: item['current_stock'] for item in self.inventory_data}
        
        possible_meals = {}
        
        for recipe in recipes:
            meal_name = recipe['meal_name']
            min_possible = float('inf')
            
            for ingredient in recipe['ingredients']:
                ingredient_name = ingredient['ingredient_name']
                required_quantity = ingredient['quantity_per_serving']
                
                if ingredient_name in inventory_dict:
                    current_stock = inventory_dict[ingredient_name]
                    possible_servings = int(current_stock / required_quantity)
                    min_possible = min(min_possible, possible_servings)
                else:
                    min_possible = 0
                    break
            
            if min_possible == float('inf'):
                min_possible = 0
                
            possible_meals[meal_name] = {
                'possible_servings': min_possible,
                'recipe': recipe
            }
        
        return possible_meals

    def create_possible_meals_section(self, parent):
        """创建可制作菜品展示区域"""
        section_frame = tk.Frame(parent, bg=self.colors['background'])
        section_frame.pack(fill="x", pady=(0, 20))
        
        # 标题
        title_frame = tk.Frame(section_frame, bg=self.colors['background'])
        title_frame.pack(fill="x", pady=(0, 15))
        
        title_label = tk.Label(title_frame, text="🍽️ 可制作菜品数量", 
                              font=self.fonts['heading'],
                              bg=self.colors['background'], 
                              fg=self.colors['text_primary'])
        title_label.pack(side="left")
        
        # 刷新按钮
        refresh_btn = tk.Button(title_frame, text="🔄 刷新", 
                               font=self.fonts['body'],
                               bg=self.colors['primary'], fg="white",
                               bd=0, relief="flat", cursor="hand2",
                               command=self.refresh_possible_meals,
                               padx=15, pady=5)
        refresh_btn.pack(side="right")
        
        # 可制作菜品卡片容器
        self.meals_container = tk.Frame(section_frame, bg=self.colors['background'])
        self.meals_container.pack(fill="x")
        
        # 初始加载可制作菜品
        self.refresh_possible_meals()
    
    def refresh_possible_meals(self):
        """刷新可制作菜品显示"""
        # 清空现有显示
        for widget in self.meals_container.winfo_children():
            widget.destroy()
        
        # 计算可制作菜品
        possible_meals = self.calculate_possible_meals()
        
        if not possible_meals:
            no_data_label = tk.Label(self.meals_container, 
                                   text="暂无配方数据",
                                   font=self.fonts['body'],
                                   bg=self.colors['background'],
                                   fg=self.colors['text_secondary'])
            no_data_label.pack(pady=20)
            return
        
        # 创建卡片网格
        row = 0
        col = 0
        max_cols = 4
        
        for meal_name, meal_info in possible_meals.items():
            self.create_meal_card(self.meals_container, meal_name, meal_info, row, col)
            
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
        
        # 配置网格权重
        for i in range(max_cols):
            self.meals_container.grid_columnconfigure(i, weight=1)
    
    def create_meal_card(self, parent, meal_name, meal_info, row, col):
        """创建菜品卡片"""
        possible_servings = meal_info['possible_servings']
        recipe = meal_info['recipe']
        
        # 根据可制作数量确定颜色
        if possible_servings == 0:
            card_color = self.colors['error']
            text_color = "white"
            status_text = "缺料"
        elif possible_servings < 5:
            card_color = self.colors['warning']
            text_color = "white"
            status_text = "库存低"
        else:
            card_color = self.colors['success']
            text_color = "white"
            status_text = "充足"
        
        # 卡片框架
        card_frame = tk.Frame(parent, bg=card_color, relief="flat", bd=1)
        card_frame.grid(row=row, column=col, padx=8, pady=8, sticky="ew")
        
        # 卡片内容
        content_frame = tk.Frame(card_frame, bg=card_color)
        content_frame.pack(fill="both", expand=True, padx=15, pady=12)
        
        # 菜品名称
        name_label = tk.Label(content_frame, text=meal_name,
                             font=self.fonts['subheading'],
                             bg=card_color, fg=text_color)
        name_label.pack(anchor="w")
        
        # 可制作数量
        count_label = tk.Label(content_frame, text=f"可制作: {possible_servings} 份",
                              font=self.fonts['body'],
                              bg=card_color, fg=text_color)
        count_label.pack(anchor="w", pady=(2, 0))
        
        # 状态标签
        status_label = tk.Label(content_frame, text=status_text,
                               font=self.fonts['small'],
                               bg=card_color, fg=text_color)
        status_label.pack(anchor="w", pady=(2, 0))
        
        # 点击查看详情
        def show_recipe_detail():
            self.show_recipe_detail_dialog(meal_name, recipe, possible_servings)
        
        card_frame.bind("<Button-1>", lambda e: show_recipe_detail())
        content_frame.bind("<Button-1>", lambda e: show_recipe_detail())
        name_label.bind("<Button-1>", lambda e: show_recipe_detail())
        count_label.bind("<Button-1>", lambda e: show_recipe_detail())
        status_label.bind("<Button-1>", lambda e: show_recipe_detail())
        
        # 悬停效果
        def on_enter(event):
            card_frame.configure(relief="raised", bd=2)
        
        def on_leave(event):
            card_frame.configure(relief="flat", bd=1)
        
        card_frame.bind("<Enter>", on_enter)
        card_frame.bind("<Leave>", on_leave)
    
    def show_recipe_detail_dialog(self, meal_name, recipe, possible_servings):
        """显示配方详情对话框"""
        dialog = tk.Toplevel()
        dialog.title(f"配方详情 - {meal_name}")
        dialog.geometry("500x900")
        dialog.configure(bg=self.colors['background'])
        dialog.resizable(False, False)
        
        # 居中显示
        dialog.transient(self.parent_frame.winfo_toplevel())
        dialog.grab_set()
        
        # 标题
        title_frame = tk.Frame(dialog, bg=self.colors['primary'], height=60)
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text=f"🍽️ {meal_name}",
                              font=self.fonts['heading'],
                              bg=self.colors['primary'], fg="white")
        title_label.pack(expand=True)
        
        # 内容区域
        content_frame = tk.Frame(dialog, bg=self.colors['background'])
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # 可制作数量信息
        count_frame = tk.Frame(content_frame, bg=self.colors['surface'], padx=15, pady=10)
        count_frame.pack(fill="x", pady=(0, 15))
        
        tk.Label(count_frame, text=f"当前可制作: {possible_servings} 份",
                font=self.fonts['subheading'],
                bg=self.colors['surface'], fg=self.colors['primary']).pack()
        
        # 配方表
        recipe_frame = tk.Frame(content_frame, bg=self.colors['surface'])
        recipe_frame.pack(fill="both", expand=True)
        
        # 表头
        header_frame = tk.Frame(recipe_frame, bg=self.colors['primary'])
        header_frame.pack(fill="x")
        
        tk.Label(header_frame, text="食材名称", font=self.fonts['body'],
                bg=self.colors['primary'], fg="white", width=15).pack(side="left", padx=5, pady=8)
        tk.Label(header_frame, text="单份用量", font=self.fonts['body'],
                bg=self.colors['primary'], fg="white", width=12).pack(side="left", padx=5, pady=8)
        tk.Label(header_frame, text="当前库存", font=self.fonts['body'],
                bg=self.colors['primary'], fg="white", width=12).pack(side="left", padx=5, pady=8)
        tk.Label(header_frame, text="状态", font=self.fonts['body'],
                bg=self.colors['primary'], fg="white", width=8).pack(side="left", padx=5, pady=8)
        
        # 滚动区域
        canvas = tk.Canvas(recipe_frame, bg=self.colors['surface'])
        scrollbar = ttk.Scrollbar(recipe_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['surface'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # 食材列表
        inventory_dict = {item['name']: item for item in self.inventory_data}
        
        for i, ingredient in enumerate(recipe['ingredients']):
            ingredient_name = ingredient['ingredient_name']
            required_qty = ingredient['quantity_per_serving']
            unit = ingredient['unit']
            
            # 获取当前库存
            current_stock = 0
            if ingredient_name in inventory_dict:
                current_stock = inventory_dict[ingredient_name]['current_stock']
            
            # 判断状态
            if current_stock >= required_qty:
                status = "✅ 充足"
                status_color = self.colors['success']
            elif current_stock > 0:
                status = "⚠️ 不足"
                status_color = self.colors['warning']
            else:
                status = "❌ 缺料"
                status_color = self.colors['error']
            
            # 行背景色
            row_bg = self.colors['background'] if i % 2 == 0 else self.colors['surface']
            
            row_frame = tk.Frame(scrollable_frame, bg=row_bg)
            row_frame.pack(fill="x", pady=1)
            
            tk.Label(row_frame, text=ingredient_name, font=self.fonts['body'],
                    bg=row_bg, fg=self.colors['text_primary'], width=15).pack(side="left", padx=5, pady=5)
            tk.Label(row_frame, text=f"{required_qty} {unit}", font=self.fonts['body'],
                    bg=row_bg, fg=self.colors['text_primary'], width=12).pack(side="left", padx=5, pady=5)
            tk.Label(row_frame, text=f"{current_stock} {unit}", font=self.fonts['body'],
                    bg=row_bg, fg=self.colors['text_primary'], width=12).pack(side="left", padx=5, pady=5)
            tk.Label(row_frame, text=status, font=self.fonts['small'],
                    bg=row_bg, fg=status_color, width=8).pack(side="left", padx=5, pady=5)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # 关闭按钮
        close_btn = tk.Button(content_frame, text="关闭", font=self.fonts['body'],
                             bg=self.colors['text_secondary'], fg="white",
                             bd=0, relief="flat", cursor="hand2",
                             command=dialog.destroy, padx=20, pady=8)
        close_btn.pack(pady=15)

class InventoryItemDialog:
    """库存商品对话框"""
    def __init__(self, parent, title, item_data=None):
        self.result = None
          # 创建对话框窗口
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("500x900")  # 增加高度从600到700
        self.dialog.configure(bg="#f8f9fa")
        self.dialog.resizable(False, False)
        self.dialog.grab_set()
        
        # 居中显示
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
