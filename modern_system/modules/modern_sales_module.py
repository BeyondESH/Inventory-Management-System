#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
现代化销售管理模块 - 堂食点餐系统
提供完整的堂食客户点餐和结账功能
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from typing import Dict, List, Any, Optional
import datetime
import json
import threading

# 导入数据管理中心
try:
    from .data_manager import data_manager
except ImportError:
    try:
        from data_manager import data_manager
    except ImportError:
        # 模拟数据管理器
        class MockDataManager:
            def load_data(self, data_type):
                if data_type == 'meals':
                    return [
                        {"id": "MEAL001", "name": "番茄牛肉面", "category": "面食", "price": 25.0, "image": "🍜"},
                        {"id": "MEAL002", "name": "鸡蛋炒饭", "category": "炒饭", "price": 18.0, "image": "🍚"},
                        {"id": "MEAL003", "name": "牛肉汉堡", "category": "西餐", "price": 32.0, "image": "🍔"},
                        {"id": "MEAL004", "name": "薯条", "category": "小食", "price": 12.0, "image": "🍟"},
                        {"id": "MEAL005", "name": "可乐", "category": "饮料", "price": 8.0, "image": "🥤"},
                        {"id": "MEAL006", "name": "咖啡", "category": "饮料", "price": 15.0, "image": "☕"}
                    ]
                return []
            def add_order(self, order_data):
                return f"ORD{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
            def register_module(self, module_type, instance):
                pass
        data_manager = MockDataManager()

class ModernSalesModule:
    def __init__(self, parent_frame, title_frame, meal_module=None, inventory_module=None, order_module=None):
        self.parent_frame = parent_frame
        self.title_frame = title_frame
        self.meal_module = meal_module
        self.inventory_module = inventory_module
        self.order_module = order_module
        
        # 注册到数据管理中心
        data_manager.register_module('sales', self)
        
        # 现代化配色方案
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
            'cart_bg': '#FFF8E1',
            'selected': '#E8F5E8',
            'info': '#3498DB',         # 信息色
            'danger': '#E74C3C'        # 危险色
        }
        
        # 字体配置
        self.fonts = {
            'title': ('Microsoft YaHei UI', 16, 'bold'),
            'heading': ('Microsoft YaHei UI', 14, 'bold'),
            'body': ('Microsoft YaHei UI', 12),
            'small': ('Microsoft YaHei UI', 10),
            'price': ('Microsoft YaHei UI', 14, 'bold'),
            'cart_title': ('Microsoft YaHei UI', 13, 'bold')
        }
          # 购物车数据
        self.cart_items = []
        self.total_amount = 0.0
        self.current_table = "桌号1"
        
        # 菜品数据
        self.meals_data = self.load_meals_data()
        self.categories = list(set(meal.get('category', '其他') for meal in self.meals_data))
        self.current_category = "全部" if self.categories else "面食"
        
        self.main_frame = None
        self.table_var = None  # 延迟初始化
        
    def load_meals_data(self):
        """加载菜品数据 - 只显示上架的菜品"""
        try:
            meals = data_manager.load_data('meals')
            # 过滤只显示上架的菜品
            available_meals = []
            for meal in meals:
                # 检查菜品是否上架
                is_available = meal.get('is_available', True)  # 默认为True
                if isinstance(is_available, str):
                    is_available = is_available.lower() in ['true', '1', 'yes', '上架']
                elif isinstance(is_available, int):
                    is_available = is_available == 1
                
                # 检查菜品是否有足够库存
                has_inventory = self.check_meal_inventory(meal)
                
                if is_available and has_inventory:
                    # 为数据库中的餐食添加默认图标和描述，并兼容所有UI字段
                    # name字段
                    if 'name' not in meal:
                        meal['name'] = meal.get('meal_name', '')
                    # price字段
                    if 'price' not in meal:
                        meal['price'] = meal.get('meal_price', 0)
                    # id字段
                    if 'id' not in meal:
                        meal['id'] = meal.get('meal_id', meal.get('id', ''))
                    # category字段
                    if 'category' not in meal:
                        meal['category'] = meal.get('meal_category', '其他')
                    # image字段
                    if 'image' not in meal:
                        meal_name = meal['name'].lower()
                        if '面' in meal_name or '饭' in meal_name:
                            meal['image'] = '🍜'
                        elif '汉堡' in meal_name:
                            meal['image'] = '🍔'
                        elif '薯条' in meal_name:
                            meal['image'] = '🍟'
                        elif '可乐' in meal_name:
                            meal['image'] = '🥤'
                        elif '咖啡' in meal_name:
                            meal['image'] = '☕'
                        elif '鸡' in meal_name:
                            meal['image'] = '🍗'
                        elif '鱼' in meal_name:
                            meal['image'] = '🐟'
                        elif '豆腐' in meal_name:
                            meal['image'] = '🥘'
                        else:
                            meal['image'] = '🍽️'
                    # description字段
                    if 'description' not in meal:
                        meal['description'] = meal.get('meal_details', f"美味的{meal['name']}")
                    
                    available_meals.append(meal)
            
            print(f"✅ 销售模块加载了 {len(available_meals)} 个上架且有库存的菜品")
            return available_meals
            
        except Exception as e:
            print(f"加载餐食数据异常: {e}")
            # 默认菜品数据（只包含上架的）
            return [
                {"id": "MEAL001", "name": "番茄牛肉面", "category": "面食", "price": 25.0, "image": "🍜", "description": "经典番茄牛肉面，汤鲜味美", "is_available": True},
                {"id": "MEAL002", "name": "鸡蛋炒饭", "category": "炒饭", "price": 18.0, "image": "🍚", "description": "香喷喷的鸡蛋炒饭", "is_available": True},
                {"id": "MEAL003", "name": "牛肉汉堡", "category": "西餐", "price": 32.0, "image": "🍔", "description": "美味牛肉汉堡套餐", "is_available": True},
                {"id": "MEAL004", "name": "薯条", "category": "小食", "price": 12.0, "image": "🍟", "description": "酥脆金黄薯条", "is_available": True},
                {"id": "MEAL005", "name": "可乐", "category": "饮料", "price": 8.0, "image": "🥤", "description": "冰爽可乐", "is_available": True},
                {"id": "MEAL006", "name": "咖啡", "category": "饮料", "price": 15.0, "image": "☕", "description": "香浓咖啡", "is_available": True},
                {"id": "MEAL007", "name": "宫保鸡丁", "category": "川菜", "price": 28.0, "image": "🍗", "description": "经典川菜宫保鸡丁", "is_available": True},
                {"id": "MEAL008", "name": "麻婆豆腐", "category": "川菜", "price": 22.0, "image": "🥘", "description": "麻辣鲜香麻婆豆腐", "is_available": True}
            ]
        
    def show(self):
        """显示堂食点餐界面"""
        if self.main_frame:
            self.main_frame.destroy()
        
        self.main_frame = tk.Frame(self.parent_frame, bg=self.colors['background'])
        self.main_frame.pack(fill="both", expand=True)
        
        # 顶部信息栏
        self.create_top_info_bar()
        
        # 主内容区域
        content_frame = tk.Frame(self.main_frame, bg=self.colors['background'])
        content_frame.pack(fill="both", expand=True, pady=10)
        
        # 左侧菜品展示区
        self.create_menu_area(content_frame)
        
        # 右侧购物车区
        self.create_cart_area(content_frame)
        
    def create_top_info_bar(self):
        """创建顶部信息栏"""
        info_frame = tk.Frame(self.main_frame, bg=self.colors['surface'], height=80)
        info_frame.pack(fill="x", padx=10, pady=(0, 10))
        info_frame.pack_propagate(False)
          # 左侧标题和桌号
        left_frame = tk.Frame(info_frame, bg=self.colors['surface'])
        left_frame.pack(side="left", fill="y", padx=20, pady=10)
        
        title_label = tk.Label(left_frame, text="🍽️ 堂食点餐系统", 
                              font=self.fonts['title'],
                              bg=self.colors['surface'], 
                              fg=self.colors['text_primary'])
        title_label.pack(anchor="w")
        
        # 桌号选择
        table_frame = tk.Frame(left_frame, bg=self.colors['surface'])
        table_frame.pack(anchor="w", pady=(5, 0))
        
        table_label = tk.Label(table_frame, text="当前桌号:", 
                              font=self.fonts['body'],
                              bg=self.colors['surface'], 
                              fg=self.colors['text_secondary'])
        table_label.pack(side="left")
        
        self.table_var = tk.StringVar(left_frame, value=self.current_table)
        table_combo = ttk.Combobox(table_frame, textvariable=self.table_var, 
                                  values=[f"桌号{i}" for i in range(1, 21)], 
                                  width=10, state="readonly")
        table_combo.pack(side="left", padx=(10, 0))
        table_combo.bind('<<ComboboxSelected>>', self.on_table_changed)
        
        # 右侧当前时间和服务员
        right_frame = tk.Frame(info_frame, bg=self.colors['surface'])
        right_frame.pack(side="right", fill="y", padx=20, pady=10)
        
        time_label = tk.Label(right_frame, 
                             text=f"⏰ {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}",
                             font=self.fonts['body'],
                             bg=self.colors['surface'], 
                             fg=self.colors['text_secondary'])
        time_label.pack(anchor="e")
        
        staff_label = tk.Label(right_frame, text="👤 服务员: 小王",
                              font=self.fonts['body'],
                              bg=self.colors['surface'], 
                              fg=self.colors['text_secondary'])
        staff_label.pack(anchor="e", pady=(5, 0))
        
    def create_menu_area(self, parent):
        """创建菜品展示区"""
        menu_frame = tk.Frame(parent, bg=self.colors['surface'])
        menu_frame.pack(side="left", fill="both", expand=True, padx=(10, 5))
        
        # 分类导航
        self.create_category_nav(menu_frame)
        
        # 菜品网格
        self.create_menu_grid(menu_frame)
        
    def create_category_nav(self, parent):
        """创建分类导航"""
        nav_frame = tk.Frame(parent, bg=self.colors['surface'], height=60)
        nav_frame.pack(fill="x", padx=10, pady=10)
        nav_frame.pack_propagate(False)
        
        # 添加"全部"分类
        all_categories = ["全部"] + self.categories
        
        self.category_buttons = {}
        for category in all_categories:
            btn = tk.Button(nav_frame, text=category,
                          font=self.fonts['body'],
                          bg=self.colors['primary'] if category == self.current_category else self.colors['background'],
                          fg='white' if category == self.current_category else self.colors['text_primary'],
                          bd=0, pady=8, padx=15,
                          cursor="hand2",
                          command=lambda c=category: self.switch_category(c))
            btn.pack(side="left", padx=5)
            self.category_buttons[category] = btn
            
    def create_menu_grid(self, parent):
        """创建菜品网格"""
        # 滚动框架
        canvas = tk.Canvas(parent, bg=self.colors['surface'])
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg=self.colors['surface'])
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=10)
        scrollbar.pack(side="right", fill="y")
        
        # 显示菜品
        self.display_meals()
        
    def display_meals(self):
        """显示菜品"""
        # 清除现有菜品
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # 筛选菜品
        if self.current_category == "全部":
            filtered_meals = self.meals_data
        else:
            filtered_meals = [meal for meal in self.meals_data 
                            if meal.get('category') == self.current_category]
        
        # 创建菜品卡片（3列布局）
        row = 0
        col = 0
        for meal in filtered_meals:
            meal_card = self.create_meal_card(self.scrollable_frame, meal)
            meal_card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            
            col += 1
            if col >= 3:  # 每行3个
                col = 0
                row += 1
        
        # 配置列权重
        for i in range(3):
            self.scrollable_frame.columnconfigure(i, weight=1)
            
    def create_meal_card(self, parent, meal):
        """创建菜品卡片，字段兜底防止KeyError"""
        card = tk.Frame(parent, bg=self.colors['background'], relief="flat", bd=1)
        card.configure(width=200, height=180)
        card.pack_propagate(False)
        # 菜品图标
        icon_label = tk.Label(card, text=meal.get('image', '🍽️'), 
                             font=('Segoe UI Emoji', 32),
                             bg=self.colors['background'])
        icon_label.pack(pady=(15, 5))
        # 菜品名称
        name_label = tk.Label(card, text=meal.get('name', ''), 
                             font=self.fonts['heading'],
                             bg=self.colors['background'], 
                             fg=self.colors['text_primary'])
        name_label.pack()
        # 描述
        description = meal.get('description', '')
        if len(description) > 10:
            description = description[:10] + "..."
        desc_label = tk.Label(card, text=description, 
                             font=self.fonts['small'],
                             bg=self.colors['background'], 
                             fg=self.colors['text_secondary'],
                             wraplength=150,
                             justify='left',
                             height=1)
        desc_label.pack()
        # 价格
        price = meal.get('price', 0)
        bottom_frame = tk.Frame(card, bg=self.colors['background'])
        bottom_frame.pack(side="bottom", fill="x", pady=(10, 0))
        price_label = tk.Label(bottom_frame, text=f"￥{price:.0f}",
                              font=self.fonts['price'],
                              bg=self.colors['background'],
                              fg=self.colors['primary'])
        price_label.pack(side="left", padx=(10, 0))
        # 加入购物车按钮
        add_btn = tk.Button(bottom_frame, text="加入购物车", font=self.fonts['small'],
                            bg=self.colors['primary'], fg="white", bd=0, padx=10, pady=3,
                            cursor="hand2", command=lambda m=meal: self.add_to_cart(m))
        add_btn.pack(side="right", padx=(0, 10))
        return card

    def create_cart_area(self, parent):
        """创建购物车区域"""
        cart_frame = tk.Frame(parent, bg=self.colors['cart_bg'], width=350)
        cart_frame.pack(side="right", fill="y", padx=(5, 10))
        cart_frame.pack_propagate(False)
        
        # 购物车标题
        cart_title = tk.Label(cart_frame, text="🛒 购物车", 
                             font=self.fonts['cart_title'],
                             bg=self.colors['cart_bg'], 
                             fg=self.colors['text_primary'])
        cart_title.pack(pady=(15, 10))
        
        # 购物车列表容器
        list_container = tk.Frame(cart_frame, bg=self.colors['cart_bg'])
        list_container.pack(fill="both", expand=True, padx=15)
        
        # 购物车列表（滚动）
        cart_canvas = tk.Canvas(list_container, bg=self.colors['cart_bg'], highlightthickness=0)
        cart_scrollbar = ttk.Scrollbar(list_container, orient="vertical", command=cart_canvas.yview)
        self.cart_list_frame = tk.Frame(cart_canvas, bg=self.colors['cart_bg'])
        
        self.cart_list_frame.bind(
            "<Configure>",
            lambda e: cart_canvas.configure(scrollregion=cart_canvas.bbox("all"))
        )
        
        cart_canvas.create_window((0, 0), window=self.cart_list_frame, anchor="nw")
        cart_canvas.configure(yscrollcommand=cart_scrollbar.set)
        
        cart_canvas.pack(side="left", fill="both", expand=True)
        cart_scrollbar.pack(side="right", fill="y")
        
        # 底部合计和结账区域
        self.create_cart_bottom(cart_frame)
        
        # 初始显示空购物车
        self.update_cart_display()
        
    def create_cart_bottom(self, parent):
        """创建购物车底部区域"""
        bottom_frame = tk.Frame(parent, bg=self.colors['cart_bg'])
        bottom_frame.pack(fill="x", side="bottom", padx=15, pady=15)
        
        # 分隔线
        separator = tk.Frame(bottom_frame, bg=self.colors['border'], height=1)
        separator.pack(fill="x", pady=(0, 15))
        
        # 总计
        total_frame = tk.Frame(bottom_frame, bg=self.colors['cart_bg'])
        total_frame.pack(fill="x", pady=(0, 15))
        
        tk.Label(total_frame, text="总计:", font=self.fonts['heading'],
                bg=self.colors['cart_bg'], fg=self.colors['text_primary']).pack(side="left")
        
        self.total_label = tk.Label(total_frame, text="￥0.00", 
                                   font=self.fonts['price'],
                                   bg=self.colors['cart_bg'], 
                                   fg=self.colors['primary'])
        self.total_label.pack(side="right")
        
        # 结账按钮
        self.checkout_btn = tk.Button(bottom_frame, text="💳 立即结账",
                                     font=self.fonts['heading'],
                                     bg=self.colors['primary'], fg='white',
                                     bd=0, pady=12, cursor="hand2",
                                     command=self.checkout,
                                     state="disabled")
        self.checkout_btn.pack(fill="x", pady=(0, 5))
        
        # 清空购物车按钮
        clear_btn = tk.Button(bottom_frame, text="🗑️ 清空购物车",
                             font=self.fonts['body'],
                             bg=self.colors['text_secondary'], fg='white',
                             bd=0, pady=8, cursor="hand2",
                             command=self.clear_cart_with_confirm)
        clear_btn.pack(fill="x")
        
    def switch_category(self, category):
        """切换菜品分类"""
        # 更新当前分类
        old_category = self.current_category
        self.current_category = category
        
        # 更新按钮样式
        if old_category in self.category_buttons:
            self.category_buttons[old_category].configure(
                bg=self.colors['background'], 
                fg=self.colors['text_primary']
            )
        
        if category in self.category_buttons:
            self.category_buttons[category].configure(
                bg=self.colors['primary'], 
                fg='white'
            )
        
        # 重新显示菜品
        self.display_meals()
        
    def add_to_cart(self, meal):
        """添加菜品到购物车"""
        # 检查是否已存在
        for item in self.cart_items:
            if item['id'] == meal['id']:
                item['quantity'] += 1
                break
        else:
            # 新增菜品
            cart_item = {
                'id': meal['id'],
                'name': meal['name'],
                'price': meal['price'],
                'quantity': 1,                'image': meal.get('image', '🍽️')
            }
            self.cart_items.append(cart_item)
        
        # 更新显示
        self.update_cart_display()
        
        # 显示简单的添加成功提示（不使用messagebox）
        self.show_add_success_feedback(meal['name'])
        
    def remove_from_cart(self, meal_id):
        """从购物车移除菜品"""
        self.cart_items = [item for item in self.cart_items if item['id'] != meal_id]
        self.update_cart_display()
        
    def update_quantity(self, meal_id, change):
        """更新菜品数量"""
        for item in self.cart_items:
            if item['id'] == meal_id:
                item['quantity'] += change
                if item['quantity'] <= 0:
                    self.remove_from_cart(meal_id)
                break
        self.update_cart_display()
        
    def update_cart_display(self):
        """更新购物车显示"""
        # 清空现有显示
        for widget in self.cart_list_frame.winfo_children():
            widget.destroy()
        
        if not self.cart_items:
            # 空购物车提示
            empty_label = tk.Label(self.cart_list_frame, 
                                  text="🛒 购物车是空的\n点击菜品添加到购物车",
                                  font=self.fonts['body'],
                                  bg=self.colors['cart_bg'], 
                                  fg=self.colors['text_secondary'],
                                  justify="center")
            empty_label.pack(expand=True, pady=50)
        else:
            # 显示购物车商品
            for item in self.cart_items:
                self.create_cart_item(item)
        
        # 计算总金额
        self.total_amount = sum(item['price'] * item['quantity'] for item in self.cart_items)
        self.total_label.configure(text=f"￥{self.total_amount:.2f}")
        
        # 更新结账按钮状态
        if self.cart_items:
            self.checkout_btn.configure(state="normal")
        else:
            self.checkout_btn.configure(state="disabled")
            
    def create_cart_item(self, item):
        """创建购物车商品项"""
        item_frame = tk.Frame(self.cart_list_frame, bg=self.colors['surface'], 
                             relief="flat", bd=1)
        item_frame.pack(fill="x", pady=5, padx=5)
        
        # 商品信息行
        info_frame = tk.Frame(item_frame, bg=self.colors['surface'])
        info_frame.pack(fill="x", padx=10, pady=8)
        
        # 商品图标和名称
        left_frame = tk.Frame(info_frame, bg=self.colors['surface'])
        left_frame.pack(side="left", fill="x", expand=True)
        
        tk.Label(left_frame, text=item['image'], 
                font=('Segoe UI Emoji', 16),
                bg=self.colors['surface']).pack(side="left")
        
        tk.Label(left_frame, text=item['name'], 
                font=self.fonts['body'],
                bg=self.colors['surface'], 
                fg=self.colors['text_primary']).pack(side="left", padx=(8, 0))
        
        # 删除按钮
        del_btn = tk.Button(info_frame, text="❌",
                           font=('Segoe UI Emoji', 12),
                           bg=self.colors['surface'], fg=self.colors['danger'],
                           bd=0, cursor="hand2",
                           command=lambda: self.remove_from_cart(item['id']))
        del_btn.pack(side="right")
        
        # 数量和价格行
        control_frame = tk.Frame(item_frame, bg=self.colors['surface'])
        control_frame.pack(fill="x", padx=10, pady=(0, 8))
        
        # 数量控制
        qty_frame = tk.Frame(control_frame, bg=self.colors['surface'])
        qty_frame.pack(side="left")
        
        minus_btn = tk.Button(qty_frame, text="➖",
                             font=('Segoe UI Emoji', 12),
                             bg=self.colors['background'], 
                             bd=0, cursor="hand2", width=3,
                             command=lambda: self.update_quantity(item['id'], -1))
        minus_btn.pack(side="left")
        
        qty_label = tk.Label(qty_frame, text=str(item['quantity']),
                            font=self.fonts['body'],
                            bg=self.colors['surface'], 
                            fg=self.colors['text_primary'],
                            width=3)
        qty_label.pack(side="left", padx=5)
        
        plus_btn = tk.Button(qty_frame, text="➕",
                            font=('Segoe UI Emoji', 12),
                            bg=self.colors['background'], 
                            bd=0, cursor="hand2", width=3,
                            command=lambda: self.update_quantity(item['id'], 1))
        plus_btn.pack(side="left")
          # 小计
        subtotal = item['price'] * item['quantity']
        price_label = tk.Label(control_frame, text=f"￥{subtotal:.2f}",
                              font=self.fonts['price'],
                              bg=self.colors['surface'], 
                              fg=self.colors['primary'])
        price_label.pack(side="right")
        
    def clear_cart(self):
        """清空购物车"""
        self.cart_items.clear()
        self.update_cart_display()
    
    def clear_cart_with_confirm(self):
        """清空购物车（带确认对话框）"""
        if self.cart_items:
            try:
                root = self.main_frame.winfo_toplevel()
                result = messagebox.askyesno("确认清空", "确定要清空购物车吗？", parent=root)
                if result:
                    self.clear_cart()
            except Exception as e:
                print(f"清空购物车确认对话框错误: {e}")
                # 如果对话框出错，直接清空
                self.clear_cart()
    
    def on_table_changed(self, event=None):
        """桌号改变事件"""
        self.current_table = self.table_var.get()
    
    def checkout(self):
        """结账处理"""
        if not self.cart_items:
            root = self.main_frame.winfo_toplevel()
            messagebox.showwarning("提示", "购物车是空的！", parent=root)
            return
          # 创建结账对话框
        self.show_checkout_dialog()
    
    def show_checkout_dialog(self):
        """显示结账对话框"""
        # 获取根窗口
        root = self.main_frame.winfo_toplevel()
        dialog = tk.Toplevel(root)
        dialog.title("结账")
        dialog.configure(bg=self.colors['background'])
        dialog.transient(root)
        dialog.grab_set()
        dialog.resizable(False, False)  # 禁止调整大小
          # 设置对话框大小和位置，调整尺寸确保按钮可见
        dialog_width = 450
        dialog_height = 650  # 增加高度
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog_width // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog_height // 2)
        dialog.geometry(f"{dialog_width}x{dialog_height}+{x}+{y}")
        
        # 创建主容器 - 分为内容区和按钮区
        main_container = tk.Frame(dialog, bg=self.colors['background'])
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # 内容区域（可滚动）- 限制高度确保按钮区域可见
        content_container = tk.Frame(main_container, bg=self.colors['background'])
        content_container.pack(fill="both", expand=True, pady=(0, 15))
        
        content_canvas = tk.Canvas(content_container, bg=self.colors['background'], 
                                  highlightthickness=0, height=450)  # 限制画布高度
        content_scrollbar = ttk.Scrollbar(content_container, orient="vertical", command=content_canvas.yview)
        content_frame = tk.Frame(content_canvas, bg=self.colors['background'])
        
        content_frame.bind(
            "<Configure>",
            lambda e: content_canvas.configure(scrollregion=content_canvas.bbox("all"))
        )
        
        content_canvas.create_window((0, 0), window=content_frame, anchor="nw")
        content_canvas.configure(yscrollcommand=content_scrollbar.set)
        
        # 标题
        title_label = tk.Label(content_frame, text="💳 订单结账", 
                              font=self.fonts['title'],
                              bg=self.colors['background'], 
                              fg=self.colors['text_primary'])
        title_label.pack(pady=(0, 20))
        
        # 订单信息
        info_frame = tk.Frame(content_frame, bg=self.colors['surface'], relief="flat", bd=1)
        info_frame.pack(fill="x", pady=(0, 15))
        
        tk.Label(info_frame, text=f"桌号: {self.current_table}", 
                font=self.fonts['body'],
                bg=self.colors['surface'], 
                fg=self.colors['text_primary']).pack(anchor="w", padx=15, pady=5)
        
        tk.Label(info_frame, text=f"时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}", 
                font=self.fonts['body'],
                bg=self.colors['surface'], 
                fg=self.colors['text_primary']).pack(anchor="w", padx=15, pady=5)
        
        # 商品列表
        items_frame = tk.Frame(content_frame, bg=self.colors['surface'], relief="flat", bd=1)
        items_frame.pack(fill="x", pady=(0, 15))
        
        tk.Label(items_frame, text="订单明细:", 
                font=self.fonts['heading'],
                bg=self.colors['surface'], 
                fg=self.colors['text_primary']).pack(anchor="w", padx=15, pady=(10, 5))
        
        for item in self.cart_items:
            item_line = f"{item['name']} x{item['quantity']} = ￥{item['price'] * item['quantity']:.2f}"
            tk.Label(items_frame, text=item_line, 
                    font=self.fonts['body'],
                    bg=self.colors['surface'], 
                    fg=self.colors['text_secondary']).pack(anchor="w", padx=30, pady=2)
        
        # 总计
        total_frame = tk.Frame(content_frame, bg=self.colors['surface'], relief="flat", bd=1)
        total_frame.pack(fill="x", pady=(0, 15))
        
        tk.Label(total_frame, text=f"总计: ￥{self.total_amount:.2f}", 
                font=self.fonts['price'],
                bg=self.colors['surface'],
                fg=self.colors['primary']).pack(anchor="w", padx=15, pady=10)
        
        # 支付方式
        payment_frame = tk.Frame(content_frame, bg=self.colors['background'])
        payment_frame.pack(fill="x", pady=(0, 20))
        
        tk.Label(payment_frame, text="选择支付方式:", 
                font=self.fonts['heading'],
                bg=self.colors['background'], 
                fg=self.colors['text_primary']).pack(anchor="w")
        
        payment_var = tk.StringVar(dialog, value="现金")
        payment_methods = [
            ("💵 现金支付", "现金"),
            ("💳 刷卡支付", "银行卡"),
            ("📱 微信支付", "微信支付"),
            ("📱 支付宝", "支付宝")
        ]
        
        for text, value in payment_methods:
            rb = tk.Radiobutton(payment_frame, text=text, variable=payment_var, value=value,
                               font=self.fonts['body'], bg=self.colors['background'],
                               fg=self.colors['text_primary'])
            rb.pack(anchor="w", pady=2)
          # 布局内容区域
        content_canvas.pack(side="left", fill="both", expand=True)
        content_scrollbar.pack(side="right", fill="y")
        
        # 固定在底部的按钮容器 - 确保始终可见
        button_container = tk.Frame(main_container, bg=self.colors['background'], height=70)
        button_container.pack(side="bottom", fill="x")
        button_container.pack_propagate(False)
        
        # 按钮框架
        btn_frame = tk.Frame(button_container, bg=self.colors['background'])
        btn_frame.pack(fill="both", expand=True, pady=10)
        
        confirm_btn = tk.Button(btn_frame, text="✅ 确认支付",
                               font=self.fonts['heading'],
                               bg=self.colors['success'], fg='white',
                               bd=0, pady=12, cursor="hand2",
                               command=lambda: self.process_payment(dialog, payment_var.get()))
        confirm_btn.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        cancel_btn = tk.Button(btn_frame, text="❌ 取消",
                              font=self.fonts['body'],
                              bg=self.colors['text_secondary'], fg='white',
                              bd=0, pady=12, cursor="hand2",
                              command=dialog.destroy)
        cancel_btn.pack(side="right", fill="both", expand=True)
        
    def process_payment(self, dialog, payment_method):
        """处理支付"""
        print("🔄 开始处理支付...")
        
        # 立即禁用支付按钮，防止重复点击
        try:
            for widget in dialog.winfo_children():
                self._disable_payment_buttons(widget)
        except Exception as e:
            print(f"禁用按钮时出错: {e}")
        
        # 立即更新界面显示
        try:
            dialog.update_idletasks()
        except Exception as e:
            print(f"更新界面时出错: {e}")
        
        # 在独立的函数中处理支付逻辑，避免阻塞UI
        def _do_payment():
            try:
                print("📦 准备订单数据...")
                # 准备订单项目用于库存检查
                order_items = []
                meals_data = []
                for item in self.cart_items:
                    order_items.append({
                        'product_id': item.get('id', item.get('meal_id', item['name'])),
                        'quantity': item['quantity'],
                        'name': item['name'],
                        'id': item.get('id', item.get('meal_id', '')),
                        'price': item.get('price', 0)
                    })
                    meals_data.append({
                        'name': item['name'],
                        'price': item['price'],
                        'quantity': item['quantity'],
                        'subtotal': item['price'] * item['quantity']
                    })
                # 创建订单数据 - 适配数据库字段
                order_data = {
                    'items': order_items,
                    'meals': meals_data,
                    'customer_id': 1,  # 默认客户ID，实际应从登录用户获取
                    'employee_id': 1,  # 默认员工ID
                    'payment_method_id': 1,  # 默认支付方式ID
                    'delivery_date': datetime.datetime.now().strftime('%Y-%m-%d'),
                    'order_status': '已接收',
                    'note': f"桌号: {self.current_table}",
                    'quantity': sum(item['quantity'] for item in self.cart_items),
                    'total_amount': self.total_amount,
                    'customer_name': f"桌号{self.current_table}",
                    'phone': '',
                    'address': '堂食',
                    'payment_method': payment_method,
                    'order_type': '堂食'
                }
                print(f"💰 订单总金额: ￥{self.total_amount:.2f}")
                print("🏪 创建订单...")
                order_id = data_manager.create_order(order_data)
                print(f"✅ 订单创建成功: {order_id}")
                dialog.after(0, lambda: self._handle_payment_success(dialog, order_id, payment_method))
            except Exception as e:
                print(f"❌ 支付处理失败: {e}")
                dialog.after(0, lambda e=e: self._handle_payment_error(dialog, e))
        
        # 使用线程处理支付逻辑，避免阻塞UI
        payment_thread = threading.Thread(target=_do_payment)
        payment_thread.start()
    
    def _disable_payment_buttons(self, widget):
        """递归禁用支付按钮"""
        try:
            if isinstance(widget, tk.Button):
                text = widget.cget('text')
                if "确认支付" in text:
                    widget.configure(state="disabled", text="💳 处理中...")
            
            if hasattr(widget, 'winfo_children'):
                for child in widget.winfo_children():
                    self._disable_payment_buttons(child)
        except:
            pass
    
    def _handle_payment_success(self, dialog, order_id, payment_method):
        """处理支付成功"""
        try:
            print(f"✅ 支付成功！订单号: {order_id}, 支付方式: {payment_method}")
    
            # 定义清理和关闭的函数
            def close_and_clean():
                try:
                    # 确保对话框存在再销毁
                    if dialog and dialog.winfo_exists():
                        dialog.destroy()
                    
                    # 清理购物车并刷新界面
                    self.clear_cart()
                    self.refresh_meals_data()
                    
                    # 安全地通知其他模块
                    self._safe_notify_modules(order_id)
                    
                except Exception as e:
                    print(f"关闭支付对话框并清理时出错: {e}")
    
            # 显示成功信息，这会阻塞直到用户点击OK
            success_msg = f"订单 {order_id} 支付成功！\n感谢您的惠顾！"
            messagebox.showinfo("支付成功", success_msg, parent=dialog)
            
            # 用户点击OK后，执行清理操作
            # 使用 after(0, ...) 确保在当前事件循环的下个空闲时段执行
            # 这样可以避免直接在消息框回调中销毁父窗口可能引发的问题
            dialog.after(0, close_and_clean)
    
        except tk.TclError as e:
            # 如果窗口已销毁，则忽略错误
            if "invalid command name" not in str(e):
                print(f"处理支付成功时发生Tkinter错误: {e}")
        except Exception as e:
            print(f"处理支付成功时发生意外错误: {e}")

    def _handle_payment_error(self, dialog, error):
        """处理支付错误"""
        try:
            print(f"🔧 处理支付错误: {error}")
            
            error_msg = str(error)
            if "库存不足" in error_msg or "库存" in error_msg:
                messagebox.showerror("库存不足", 
                                    "部分商品库存不足，无法完成订单。\n请联系工作人员或选择其他商品。",
                                    parent=dialog)
            else:
                messagebox.showerror("支付失败", f"支付处理失败：{error_msg}", parent=dialog)
            
            # 重新启用支付按钮
            self._enable_payment_buttons(dialog)
            
        except Exception as e:
            print(f"处理支付错误时出错: {e}")
    
    def _enable_payment_buttons(self, widget):
        """递归启用支付按钮"""
        try:
            if isinstance(widget, tk.Button):
                text = widget.cget('text')
                if "处理中" in text:
                    widget.configure(state="normal", text="✅ 确认支付")
            
            if hasattr(widget, 'winfo_children'):
                for child in widget.winfo_children():
                    self._enable_payment_buttons(child)
        except:
            pass
    
    def _safe_notify_modules(self, order_id):
        """安全地通知其他模块"""
        try:
            print(f"📢 通知其他模块订单创建: {order_id}")
            
            # 通知订单模块
            if self.order_module and hasattr(self.order_module, 'refresh_order_list'):
                try:
                    self.order_module.refresh_order_list()
                    print("✅ 订单模块已通知")
                except Exception as e:
                    print(f"⚠️ 通知订单模块失败: {e}")
            
            # 通知库存模块
            if self.inventory_module and hasattr(self.inventory_module, 'refresh_inventory'):
                try:
                    self.inventory_module.refresh_inventory()
                    print("✅ 库存模块已通知")
                except Exception as e:
                    print(f"⚠️ 通知库存模块失败: {e}")
            
            # 通知财务模块
            if hasattr(self, 'finance_module') and self.finance_module and hasattr(self.finance_module, 'refresh_finance_records'):
                try:
                    self.finance_module.refresh_finance_records()
                    print("✅ 财务模块已通知")
                except Exception as e:
                    print(f"⚠️ 通知财务模块失败: {e}")
            
        except Exception as e:
            print(f"⚠️ 通知模块时发生错误（不影响订单）: {e}")
    
    def notify_order_created(self, order_id):
        """通知其他模块订单已创建"""
        try:
            print(f"开始通知其他模块，订单ID: {order_id}")
            
            # 使用try-except为每个模块单独处理，避免一个模块出错影响其他模块
            
            # 通知订单模块刷新（延迟执行，避免阻塞）
            if self.order_module and hasattr(self.order_module, 'refresh_order_list'):
                try:
                    # 延迟执行刷新，避免阻塞UI
                    if hasattr(self, 'main_frame') and self.main_frame:
                        self.main_frame.after(500, self.order_module.refresh_order_list)
                    else:
                        self.order_module.refresh_order_list()
                    print("✅ 已通知订单模块刷新")
                except Exception as e:
                    print(f"⚠️ 通知订单模块失败: {e}")
            
            # 通知库存模块刷新（延迟执行，避免阻塞）
            if self.inventory_module and hasattr(self.inventory_module, 'refresh_inventory'):
                try:
                    # 延迟执行刷新，避免阻塞UI
                    if hasattr(self, 'main_frame') and self.main_frame:
                        self.main_frame.after(1000, self.inventory_module.refresh_inventory)
                    else:
                        self.inventory_module.refresh_inventory()
                    print("✅ 已通知库存模块刷新")
                except Exception as e:
                    print(f"⚠️ 通知库存模块失败: {e}")
                    
            print(f"✅ 订单 {order_id} 通知完成")
        except Exception as e:
            print(f"⚠️ 通知模块刷新时发生错误（不影响订单创建）：{e}")
    
    def clear_cart(self):
        """清空购物车"""
        self.cart_items.clear()
        self.update_cart_display()
    
    def show_add_success_feedback(self, meal_name):
        """显示添加成功的非阻塞反馈"""
        # 创建临时反馈标签
        feedback_label = tk.Label(self.main_frame, 
                                 text=f"✅ {meal_name} 已添加到购物车",
                                 font=self.fonts['body'],
                                 bg=self.colors['success'], 
                                 fg='white',
                                 padx=20, pady=10)
        feedback_label.place(relx=0.5, rely=0.1, anchor="center")
        
        # 2秒后自动消失
        self.main_frame.after(2000, feedback_label.destroy)
        
    def refresh_meals_data(self):
        """刷新菜品数据（由菜品管理模块调用）"""
        try:
            # 重新加载菜品数据
            self.meals_data = self.load_meals_data()
            # 更新分类
            self.categories = list(set(meal.get('category', '其他') for meal in self.meals_data))
            # 如果当前页面已显示，刷新显示
            if hasattr(self, 'main_frame') and self.main_frame:
                self.display_meals()
        except Exception as e:
            print(f"刷新菜品数据失败: {e}")
    
    def check_meal_inventory(self, meal):
        """检查菜品是否有足够的库存"""
        try:
            # 如果没有库存模块，默认返回True
            if not self.inventory_module:
                return True
            
            # 从库存模块获取配方数据
            if hasattr(self.inventory_module, 'calculate_possible_meals'):
                possible_meals = self.inventory_module.calculate_possible_meals()
                meal_name = meal.get('name', meal.get('meal_name', ''))
                
                # 检查是否可以制作至少1份
                if meal_name in possible_meals:
                    return possible_meals[meal_name]['possible_servings'] > 0
            
            # 如果无法获取库存信息，默认返回True
            return True
            
        except Exception as e:
            print(f"检查菜品库存失败: {e}")
            return True  # 出错时默认显示菜品
