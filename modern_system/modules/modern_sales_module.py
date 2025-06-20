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
            'border': '#E1E8ED',
            'cart_bg': '#FFF8E1',
            'selected': '#E8F5E8'
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
        """加载菜品数据"""
        try:
            return data_manager.load_data('meals')
        except:
            # 默认菜品数据
            return [
                {"id": "MEAL001", "name": "番茄牛肉面", "category": "面食", "price": 25.0, "image": "🍜", "description": "经典番茄牛肉面，汤鲜味美"},
                {"id": "MEAL002", "name": "鸡蛋炒饭", "category": "炒饭", "price": 18.0, "image": "🍚", "description": "香喷喷的鸡蛋炒饭"},
                {"id": "MEAL003", "name": "牛肉汉堡", "category": "西餐", "price": 32.0, "image": "🍔", "description": "美味牛肉汉堡套餐"},
                {"id": "MEAL004", "name": "薯条", "category": "小食", "price": 12.0, "image": "🍟", "description": "酥脆金黄薯条"},
                {"id": "MEAL005", "name": "可乐", "category": "饮料", "price": 8.0, "image": "🥤", "description": "冰爽可乐"},
                {"id": "MEAL006", "name": "咖啡", "category": "饮料", "price": 15.0, "image": "☕", "description": "香浓咖啡"},
                {"id": "MEAL007", "name": "宫保鸡丁", "category": "川菜", "price": 28.0, "image": "🍗", "description": "经典川菜宫保鸡丁"},
                {"id": "MEAL008", "name": "麻婆豆腐", "category": "川菜", "price": 22.0, "image": "🥘", "description": "麻辣鲜香麻婆豆腐"}
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
        
        self.table_var = tk.StringVar(value=self.current_table)
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
        """创建菜品卡片"""
        card = tk.Frame(parent, bg=self.colors['background'], relief="flat", bd=1)
        card.configure(width=200, height=180)
        card.pack_propagate(False)
        
        # 菜品图标
        icon_label = tk.Label(card, text=meal.get('image', '🍽️'), 
                             font=('Segoe UI Emoji', 32),
                             bg=self.colors['background'])
        icon_label.pack(pady=(15, 5))
        
        # 菜品名称
        name_label = tk.Label(card, text=meal['name'], 
                             font=self.fonts['heading'],
                             bg=self.colors['background'], 
                             fg=self.colors['text_primary'])
        name_label.pack()        # 描述 - 限制显示为一行
        description = meal.get('description', '')
        # 如果描述过长，截断并添加省略号（限制为10字）
        if len(description) > 10:
            description = description[:10] + "..."
        
        desc_label = tk.Label(card, text=description, 
                             font=self.fonts['small'],
                             bg=self.colors['background'], 
                             fg=self.colors['text_secondary'],
                             wraplength=150,
                             justify='left',
                             height=1)  # 限制为1行
        desc_label.pack(pady=(2, 5))
        
        # 价格和添加按钮
        bottom_frame = tk.Frame(card, bg=self.colors['background'])
        bottom_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        price_label = tk.Label(bottom_frame, text=f"￥{meal['price']:.0f}", 
                              font=self.fonts['price'],
                              bg=self.colors['background'], 
                              fg=self.colors['primary'])
        price_label.pack(side="left")
        
        add_btn = tk.Button(bottom_frame, text="➕",
                           font=('Segoe UI Emoji', 16),
                           bg=self.colors['primary'], fg='white',
                           bd=0, width=3, cursor="hand2",
                           command=lambda m=meal: self.add_to_cart(m))
        add_btn.pack(side="right")
        
        # 悬停效果
        def on_enter(e):
            card.configure(bg=self.colors['selected'])
            icon_label.configure(bg=self.colors['selected'])
            name_label.configure(bg=self.colors['selected'])
            desc_label.configure(bg=self.colors['selected'])
            bottom_frame.configure(bg=self.colors['selected'])
            price_label.configure(bg=self.colors['selected'])
            
        def on_leave(e):
            card.configure(bg=self.colors['background'])
            icon_label.configure(bg=self.colors['background'])
            name_label.configure(bg=self.colors['background'])
            desc_label.configure(bg=self.colors['background'])
            bottom_frame.configure(bg=self.colors['background'])
            price_label.configure(bg=self.colors['background'])
        
        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)
        
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
                             command=self.clear_cart)
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
        if self.cart_items:
            result = messagebox.askyesno("确认清空", "确定要清空购物车吗？")
            if result:
                self.cart_items.clear()
                self.update_cart_display()
    
    def on_table_changed(self, event=None):
        """桌号改变事件"""
        self.current_table = self.table_var.get()
    
    def checkout(self):
        """结账处理"""
        if not self.cart_items:
            messagebox.showwarning("提示", "购物车是空的！")
            return
        
        # 创建结账对话框
        self.show_checkout_dialog()
    
    def show_checkout_dialog(self):
        """显示结账对话框"""
        # 获取根窗口
        root = self.main_frame.winfo_toplevel()
        dialog = tk.Toplevel(root)
        dialog.title("结账")
        dialog.geometry("400x500")
        dialog.configure(bg=self.colors['background'])
        dialog.transient(root)
        dialog.grab_set()
        
        # 居中显示
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (dialog.winfo_screenheight() // 2) - (500 // 2)
        dialog.geometry(f"400x500+{x}+{y}")
        
        # 标题
        title_label = tk.Label(dialog, text="💳 订单结账", 
                              font=self.fonts['title'],
                              bg=self.colors['background'], 
                              fg=self.colors['text_primary'])
        title_label.pack(pady=20)
        
        # 订单信息
        info_frame = tk.Frame(dialog, bg=self.colors['surface'], relief="flat", bd=1)
        info_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        tk.Label(info_frame, text=f"桌号: {self.current_table}", 
                font=self.fonts['body'],
                bg=self.colors['surface'], 
                fg=self.colors['text_primary']).pack(anchor="w", padx=15, pady=5)
        
        tk.Label(info_frame, text=f"时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}", 
                font=self.fonts['body'],
                bg=self.colors['surface'], 
                fg=self.colors['text_primary']).pack(anchor="w", padx=15, pady=5)
        
        # 商品列表
        items_frame = tk.Frame(dialog, bg=self.colors['surface'], relief="flat", bd=1)
        items_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
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
        tk.Label(items_frame, text=f"总计: ￥{self.total_amount:.2f}", 
                font=self.fonts['price'],
                bg=self.colors['surface'],                fg=self.colors['primary']).pack(anchor="w", padx=15, pady=(10, 15))
        
        # 支付方式
        payment_frame = tk.Frame(dialog, bg=self.colors['background'])
        payment_frame.pack(fill="x", padx=20, pady=(0, 20))
        
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
        
        # 按钮
        btn_frame = tk.Frame(dialog, bg=self.colors['background'])
        btn_frame.pack(fill="x", padx=20, pady=20)
        
        confirm_btn = tk.Button(btn_frame, text="✅ 确认支付",
                               font=self.fonts['heading'],
                               bg=self.colors['success'], fg='white',
                               bd=0, pady=10, cursor="hand2",
                               command=lambda: self.process_payment(dialog, payment_var.get()))
        confirm_btn.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        cancel_btn = tk.Button(btn_frame, text="❌ 取消",
                              font=self.fonts['body'],
                              bg=self.colors['text_secondary'], fg='white',
                              bd=0, pady=10, cursor="hand2",
                              command=dialog.destroy)
        cancel_btn.pack(side="right", fill="x", expand=True)
        
    def process_payment(self, dialog, payment_method):
        """处理支付"""
        try:
            # 创建订单数据
            order_data = {
                'table_number': self.current_table,
                'customer_name': f"{self.current_table}客户",
                'phone': '',
                'address': '堂食',
                'items': [
                    {
                        'name': item['name'],
                        'quantity': item['quantity'],
                        'price': item['price'],
                        'subtotal': item['price'] * item['quantity']
                    }
                    for item in self.cart_items
                ],
                'total_amount': self.total_amount,
                'payment_method': payment_method,
                'order_type': '堂食',
                'status': '已完成',
                'create_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # 保存订单
            order_id = data_manager.add_order(order_data)
            
            # 关闭对话框
            dialog.destroy()
            
            # 显示成功消息
            messagebox.showinfo("支付成功", 
                              f"订单已完成！\n"
                              f"订单号: {order_id}\n"
                              f"支付方式: {payment_method}\n"
                              f"金额: ￥{self.total_amount:.2f}")
            
            # 清空购物车
            self.cart_items.clear()
            self.update_cart_display()
            
        except Exception as e:
            messagebox.showerror("支付失败", f"处理支付时发生错误：{e}")
    
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
        """刷新菜品数据（当菜品管理模块有更新时调用）"""
        try:
            # 重新加载菜品数据
            self.meals_data = self.load_meals_data()
            
            # 重新生成分类列表
            self.categories = list(set(meal.get('category', '其他') for meal in self.meals_data))
            
            # 如果界面已显示，刷新菜品展示
            if self.main_frame and self.main_frame.winfo_exists():
                # 重新创建分类导航
                if hasattr(self, 'category_buttons'):
                    self.create_category_nav(self.menu_frame)
                
                # 重新显示菜品
                self.display_meals()
                
            print("销售管理模块：菜品数据已刷新")
        except Exception as e:
            print(f"刷新菜品数据失败: {e}")
