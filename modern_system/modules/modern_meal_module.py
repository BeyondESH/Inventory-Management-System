#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
现代化菜品配置模块
采用现代化设计风格的菜品管理界面
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
            def load_data(self, data_type):
                return []
            def save_data(self, data_type, data):
                return True
        data_manager = MockDataManager()

class ModernMealModule:
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
            'button': ('Microsoft YaHei UI', 11, 'bold'),
            'price': ('Microsoft YaHei UI', 14, 'bold')
        }
        
        # 菜品数据
        self.meal_data = self.load_meal_data()        # 界面变量 (延迟初始化)
        self.search_var = None
        self.category_filter_var = None
        self.status_filter_var = None
          # UI组件引用
        self.meals_container = None
        self.stats_labels = {}
    
    def load_meal_data(self):
        """从数据管理中心加载菜品数据"""
        try:
            # 从数据管理器获取菜品数据
            meals_data = data_manager.load_data('meals')
            
            # 转换数据格式以适配现有界面
            formatted_data = []
            for meal in meals_data:
                formatted_meal = {
                    "id": meal.get('id', ''),
                    "name": meal.get('name', ''),
                    "category": meal.get('category', '其他'),
                    "price": meal.get('price', 0.0),
                    "cost": meal.get('cost', 0.0),
                    "description": meal.get('description', '暂无描述'),
                    "ingredients": meal.get('ingredients', []),
                    "cooking_time": meal.get('cooking_time', 15),
                    "calories": meal.get('calories', 200),
                    "is_spicy": meal.get('is_spicy', False),
                    "is_vegetarian": meal.get('is_vegetarian', False),
                    "is_available": meal.get('is_available', True),
                    "image": meal.get('image', '�️'),
                    "created_date": meal.get('created_date', datetime.datetime.now().strftime('%Y-%m-%d'))
                }
                formatted_data.append(formatted_meal)
            
            return formatted_data
        except Exception as e:
            print(f"加载菜品数据失败: {e}")
            # 返回默认菜品数据
            return [
                {
                    "id": "MEAL001", "name": "番茄牛肉面", "category": "面食", "price": 25.0,
                    "cost": 15.0, "description": "经典番茄牛肉面，汤鲜味美",
                    "ingredients": ["番茄", "牛肉", "面条"], "cooking_time": 15,
                    "calories": 450, "is_spicy": False, "is_vegetarian": False,
                    "is_available": True, "image": "�", "created_date": "2025-06-21"
                },
                {
                    "id": "MEAL002", "name": "鸡蛋炒饭", "category": "炒饭", "price": 18.0,
                    "cost": 10.0, "description": "香喷喷的鸡蛋炒饭",
                    "ingredients": ["鸡蛋", "米饭"], "cooking_time": 10,
                    "calories": 350, "is_spicy": False, "is_vegetarian": False,
                    "is_available": True, "image": "🍚", "created_date": "2025-06-21"
                },
                {
                    "id": "MEAL003", "name": "牛肉汉堡", "category": "西餐", "price": 32.0,
                    "cost": 20.0, "description": "美味牛肉汉堡套餐",
                    "ingredients": ["牛肉", "面包", "生菜"], "cooking_time": 12,
                    "calories": 520, "is_spicy": False, "is_vegetarian": False,
                    "is_available": True, "image": "🍔", "created_date": "2025-06-21"
                },
                {
                    "id": "MEAL004", "name": "薯条", "category": "小食", "price": 12.0,
                    "cost": 6.0, "description": "酥脆金黄薯条",
                    "ingredients": ["土豆"], "cooking_time": 8,
                    "calories": 280, "is_spicy": False, "is_vegetarian": True,
                    "is_available": True, "image": "�", "created_date": "2025-06-21"                }            ]
    
    def save_meal_data(self):
        """保存菜品数据到数据管理中心"""
        try:
            # 将内部格式的数据转换为标准格式
            standard_data = []
            for meal in self.meal_data:
                standard_meal = {
                    'id': meal.get('id', ''),
                    'name': meal.get('name', ''),
                    'category': meal.get('category', '其他'),
                    'price': meal.get('price', 0.0),
                    'cost': meal.get('cost', 0.0),
                    'description': meal.get('description', ''),
                    'ingredients': meal.get('ingredients', []),
                    'cooking_time': meal.get('cooking_time', 15),
                    'calories': meal.get('calories', 200),
                    'is_spicy': meal.get('is_spicy', False),
                    'is_vegetarian': meal.get('is_vegetarian', False),
                    'is_available': meal.get('is_available', True),
                    'image': meal.get('image', '🍽️'),
                    'created_date': meal.get('created_date', datetime.datetime.now().strftime('%Y-%m-%d'))
                }
                standard_data.append(standard_meal)
            
            # 保存到数据管理器
            data_manager.save_data('meals', standard_data)
            return True
        except Exception as e:
            print(f"保存菜品数据失败: {e}")
            return False
    
    def notify_data_update(self):
        """通知其他模块数据已更新"""
        try:
            # 通知销售管理模块刷新菜品数据
            if hasattr(data_manager, 'notify_modules'):
                data_manager.notify_modules('meals_updated')
            else:
                # 直接通知已注册的模块
                if hasattr(data_manager, 'registered_modules'):
                    for module_type, module_instance in data_manager.registered_modules.items():
                        if module_type == 'sales' and hasattr(module_instance, 'refresh_meals_data'):
                            module_instance.refresh_meals_data()
        except Exception as e:
            print(f"通知其他模块失败: {e}")
    
    def show(self):
        """显示菜品配置模块"""
        # 注册到数据管理器
        data_manager.register_module('meal', self)
        
        # 重新加载最新数据
        self.meal_data = self.load_meal_data()
        
        # 初始化界面变量（如果还没有初始化）
        if self.search_var is None:
            self.search_var = tk.StringVar()
            self.category_filter_var = tk.StringVar(value="全部")
            self.status_filter_var = tk.StringVar(value="全部")
        
        self.clear_frames()
        self.update_title()
        self.create_meal_interface()
        
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
        
        icon_label = tk.Label(title_frame, text="🍜", font=('Segoe UI Emoji', 20),
                             bg=self.colors['surface'], fg=self.colors['primary'])
        icon_label.pack(side="left", padx=(30, 10), pady=20)
        
        title_label = tk.Label(title_frame, text="菜品配置", font=self.fonts['title'],
                              bg=self.colors['surface'], fg=self.colors['text_primary'])
        title_label.pack(side="left", pady=20)
        
        # 右侧操作按钮
        action_frame = tk.Frame(self.title_frame, bg=self.colors['surface'])
        action_frame.pack(side="right", padx=30, pady=20)
        
        # 菜单导出按钮
        export_btn = self.create_action_button(action_frame, "📋 导出菜单", self.export_menu)
        export_btn.pack(side="right", padx=(10, 0))
        
        # 添加菜品按钮
        add_btn = self.create_action_button(action_frame, "➕ 添加菜品", self.add_meal, primary=True)
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
        
    def create_meal_interface(self):
        """创建菜品管理界面"""
        # 主容器
        main_container = tk.Frame(self.parent_frame, bg=self.colors['background'])
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # 顶部统计卡片
        self.create_stats_cards(main_container)
        
        # 中间筛选和搜索区域
        self.create_filter_section(main_container)
        
        # 底部菜品网格
        self.create_meals_grid(main_container)
        
    def create_stats_cards(self, parent):
        """创建统计卡片"""
        stats_frame = tk.Frame(parent, bg=self.colors['background'])
        stats_frame.pack(fill="x", pady=(0, 20))
        
        # 计算统计数据
        total_meals = len(self.meal_data)
        available_meals = len([meal for meal in self.meal_data if meal['is_available']])
        avg_price = sum(meal['price'] for meal in self.meal_data) / total_meals if total_meals > 0 else 0
        spicy_meals = len([meal for meal in self.meal_data if meal['is_spicy']])
        
        cards_data = [
            {"title": "菜品总数", "value": f"{total_meals}", "icon": "🍽️", "color": self.colors['primary']},
            {"title": "在售菜品", "value": f"{available_meals}", "icon": "✅", "color": self.colors['success']},
            {"title": "平均价格", "value": f"¥{avg_price:.1f}", "icon": "💰", "color": self.colors['accent']},
            {"title": "辣味菜品", "value": f"{spicy_meals}", "icon": "🌶️", "color": self.colors['error']}
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
        
        search_label = tk.Label(search_frame, text="🔍 搜索菜品", font=self.fonts['subheading'],
                               bg=self.colors['surface'], fg=self.colors['text_primary'])
        search_label.pack(side="left")
        
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, font=self.fonts['body'],
                               bg=self.colors['background'], fg=self.colors['text_primary'],
                               bd=1, relief="solid", width=25)
        search_entry.pack(side="left", padx=(20, 10), ipady=8)
        
        search_btn = tk.Button(search_frame, text="搜索", font=self.fonts['body'],
                              bg=self.colors['primary'], fg="white", bd=0,
                              cursor="hand2", command=self.search_meals, padx=15)
        search_btn.pack(side="left")
        
        # 筛选器
        filter_controls = tk.Frame(content_frame, bg=self.colors['surface'])
        filter_controls.pack(side="right", fill="y")
        
        # 分类筛选
        category_label = tk.Label(filter_controls, text="分类:", font=self.fonts['body'],
                                 bg=self.colors['surface'], fg=self.colors['text_secondary'])
        category_label.pack(side="left", padx=(0, 5))
        
        categories = ["全部", "主食", "热菜", "素菜", "汤品", "饮品"]
        category_combo = ttk.Combobox(filter_controls, textvariable=self.category_filter_var,
                                     values=categories, state="readonly", width=10)
        category_combo.pack(side="left", padx=(0, 20))
        category_combo.bind('<<ComboboxSelected>>', lambda e: self.filter_meals())
        
        # 状态筛选
        status_label = tk.Label(filter_controls, text="状态:", font=self.fonts['body'],
                               bg=self.colors['surface'], fg=self.colors['text_secondary'])
        status_label.pack(side="left", padx=(0, 5))
        
        status_options = ["全部", "在售", "下架"]
        status_combo = ttk.Combobox(filter_controls, textvariable=self.status_filter_var,
                                   values=status_options, state="readonly", width=10)
        status_combo.pack(side="left")
        status_combo.bind('<<ComboboxSelected>>', lambda e: self.filter_meals())
        
        # 绑定回车键搜索
        search_entry.bind('<Return>', lambda e: self.search_meals())
        
    def create_meals_grid(self, parent):
        """创建菜品网格"""
        grid_frame = tk.Frame(parent, bg=self.colors['background'])
        grid_frame.pack(fill="both", expand=True)
        
        # 标题
        title_frame = tk.Frame(grid_frame, bg=self.colors['background'])
        title_frame.pack(fill="x", pady=(0, 20))
        
        title_label = tk.Label(title_frame, text="🍽️ 菜品列表", font=self.fonts['heading'],
                              bg=self.colors['background'], fg=self.colors['text_primary'])
        title_label.pack(side="left")
        
        # 滚动区域
        canvas = tk.Canvas(grid_frame, bg=self.colors['background'])
        scrollbar = ttk.Scrollbar(grid_frame, orient="vertical", command=canvas.yview)
        
        self.meals_container = tk.Frame(canvas, bg=self.colors['background'])
        
        self.meals_container.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.meals_container, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
          # 绑定鼠标滚轮
        def _on_mousewheel(event):
            try:
                if canvas.winfo_exists():
                    canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            except tk.TclError:
                pass  # Widget已被销毁，忽略错误
        
        canvas.bind("<MouseWheel>", _on_mousewheel)
        self.meals_container.bind("<MouseWheel>", _on_mousewheel)
        
        # 显示菜品
        self.refresh_meals_display()
        
    def refresh_meals_display(self):
        """刷新菜品显示"""
        # 清空现有菜品
        for widget in self.meals_container.winfo_children():
            widget.destroy()
            
        # 根据筛选条件获取菜品
        filtered_meals = self.get_filtered_meals()
        
        # 计算网格布局
        cols = 3  # 每行3个菜品卡片
        for i, meal in enumerate(filtered_meals):
            row = i // cols
            col = i % cols
            self.create_meal_card(self.meals_container, meal, row, col)
            
        # 更新统计卡片
        self.update_stats_cards()
        
    def get_filtered_meals(self):
        """获取筛选后的菜品"""
        filtered_meals = self.meal_data.copy()
        
        # 按搜索关键词筛选
        search_term = self.search_var.get().strip().lower()
        if search_term:
            filtered_meals = [meal for meal in filtered_meals 
                            if search_term in meal['name'].lower() or 
                               search_term in meal['description'].lower() or
                               any(search_term in ingredient.lower() for ingredient in meal['ingredients'])]
        
        # 按分类筛选
        category_filter = self.category_filter_var.get()
        if category_filter != "全部":
            filtered_meals = [meal for meal in filtered_meals if meal['category'] == category_filter]
        
        # 按状态筛选
        status_filter = self.status_filter_var.get()
        if status_filter != "全部":
            if status_filter == "在售":
                filtered_meals = [meal for meal in filtered_meals if meal['is_available']]
            elif status_filter == "下架":
                filtered_meals = [meal for meal in filtered_meals if not meal['is_available']]
        
        return filtered_meals
        
    def create_meal_card(self, parent, meal, row, col):
        """创建菜品卡片"""
        # 卡片框架
        card_frame = tk.Frame(parent, bg=self.colors['surface'], relief="flat", bd=1,
                             cursor="hand2")
        card_frame.grid(row=row, column=col, padx=15, pady=15, sticky="ew")
        
        # 配置网格权重
        parent.grid_columnconfigure(col, weight=1)
        
        # 卡片内容
        content_frame = tk.Frame(card_frame, bg=self.colors['surface'])
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # 顶部：图标、名称和状态
        header_frame = tk.Frame(content_frame, bg=self.colors['surface'])
        header_frame.pack(fill="x", pady=(0, 15))
        
        # 菜品图标
        icon_label = tk.Label(header_frame, text=meal["image"], font=('Segoe UI Emoji', 36),
                             bg=self.colors['surface'])
        icon_label.pack(side="left")
        
        # 名称和状态
        name_frame = tk.Frame(header_frame, bg=self.colors['surface'])
        name_frame.pack(side="right", fill="x", expand=True, padx=(15, 0))
        
        name_label = tk.Label(name_frame, text=meal["name"], font=self.fonts['subheading'],
                             bg=self.colors['surface'], fg=self.colors['text_primary'], anchor="w")
        name_label.pack(fill="x")
        
        # 标签行
        tags_frame = tk.Frame(name_frame, bg=self.colors['surface'])
        tags_frame.pack(fill="x", pady=(5, 0))
        
        # 分类标签
        category_tag = tk.Label(tags_frame, text=meal["category"], font=self.fonts['small'],
                               bg=self.colors['accent'], fg="white", padx=8, pady=2)
        category_tag.pack(side="left", padx=(0, 5))
        
        # 状态标签
        if meal["is_available"]:
            status_tag = tk.Label(tags_frame, text="在售", font=self.fonts['small'],
                                 bg=self.colors['success'], fg="white", padx=8, pady=2)
        else:
            status_tag = tk.Label(tags_frame, text="下架", font=self.fonts['small'],
                                 bg=self.colors['error'], fg="white", padx=8, pady=2)
        status_tag.pack(side="left", padx=(0, 5))
        
        # 特殊标签
        if meal["is_spicy"]:
            spicy_tag = tk.Label(tags_frame, text="辣", font=self.fonts['small'],
                                bg=self.colors['error'], fg="white", padx=8, pady=2)
            spicy_tag.pack(side="left", padx=(0, 5))
            
        if meal["is_vegetarian"]:
            veg_tag = tk.Label(tags_frame, text="素", font=self.fonts['small'],
                              bg=self.colors['success'], fg="white", padx=8, pady=2)
            veg_tag.pack(side="left", padx=(0, 5))
        
        # 描述
        desc_label = tk.Label(content_frame, text=meal["description"], font=self.fonts['small'],
                             bg=self.colors['surface'], fg=self.colors['text_secondary'],
                             wraplength=250, justify="left")
        desc_label.pack(fill="x", pady=(0, 15))
        
        # 价格和成本
        price_frame = tk.Frame(content_frame, bg=self.colors['surface'])
        price_frame.pack(fill="x", pady=(0, 15))
        
        price_label = tk.Label(price_frame, text=f"¥{meal['price']:.0f}", font=self.fonts['price'],
                              bg=self.colors['surface'], fg=self.colors['primary'])
        price_label.pack(side="left")
        
        cost_label = tk.Label(price_frame, text=f"成本: ¥{meal['cost']:.0f}", font=self.fonts['small'],
                             bg=self.colors['surface'], fg=self.colors['text_secondary'])
        cost_label.pack(side="right")
        
        # 其他信息
        info_frame = tk.Frame(content_frame, bg=self.colors['surface'])
        info_frame.pack(fill="x", pady=(0, 15))
        
        time_label = tk.Label(info_frame, text=f"⏱️ {meal['cooking_time']}分钟", font=self.fonts['small'],
                             bg=self.colors['surface'], fg=self.colors['text_secondary'])
        time_label.pack(side="left")
        
        calories_label = tk.Label(info_frame, text=f"🔥 {meal['calories']}卡", font=self.fonts['small'],
                                 bg=self.colors['surface'], fg=self.colors['text_secondary'])
        calories_label.pack(side="right")
        
        # 操作按钮
        button_frame = tk.Frame(content_frame, bg=self.colors['surface'])
        button_frame.pack(fill="x")
        
        # 编辑按钮
        edit_btn = tk.Button(button_frame, text="编辑", font=self.fonts['body'],
                            bg=self.colors['background'], fg=self.colors['text_primary'],
                            bd=1, relief="solid", cursor="hand2",
                            command=lambda m=meal: self.edit_meal(m), padx=15, pady=5)
        edit_btn.pack(side="left", padx=(0, 10))
        
        # 切换状态按钮
        if meal["is_available"]:
            toggle_btn = tk.Button(button_frame, text="下架", font=self.fonts['body'],
                                  bg=self.colors['warning'], fg="white",
                                  bd=0, relief="flat", cursor="hand2",
                                  command=lambda m=meal: self.toggle_meal_status(m), padx=15, pady=5)
        else:
            toggle_btn = tk.Button(button_frame, text="上架", font=self.fonts['body'],
                                  bg=self.colors['success'], fg="white",
                                  bd=0, relief="flat", cursor="hand2",
                                  command=lambda m=meal: self.toggle_meal_status(m), padx=15, pady=5)
        toggle_btn.pack(side="right")
        
        # 卡片悬停效果
        def on_card_enter(event):
            card_frame.configure(relief="solid", bd=2)
            
        def on_card_leave(event):
            card_frame.configure(relief="flat", bd=1)
              # 绑定悬停事件
        for widget in [card_frame, content_frame, header_frame, icon_label]:
            widget.bind("<Enter>", on_card_enter)
            widget.bind("<Leave>", on_card_leave)
    
    def update_stats_cards(self):
        """更新统计卡片"""
        filtered_meals = self.get_filtered_meals()
        
        total_meals = len(filtered_meals)
        available_meals = len([meal for meal in filtered_meals if meal['is_available']])
        avg_price = sum(meal['price'] for meal in filtered_meals) / total_meals if total_meals > 0 else 0
        spicy_meals = len([meal for meal in filtered_meals if meal['is_spicy']])
        
        # 更新标签
        if "菜品总数" in self.stats_labels:
            self.stats_labels["菜品总数"].configure(text=f"{total_meals}")
        if "在售菜品" in self.stats_labels:
            self.stats_labels["在售菜品"].configure(text=f"{available_meals}")
        if "平均价格" in self.stats_labels:
            self.stats_labels["平均价格"].configure(text=f"¥{avg_price:.1f}")
        if "辣味菜品" in self.stats_labels:
            self.stats_labels["辣味菜品"].configure(text=f"{spicy_meals}")
            
    def search_meals(self):
        """搜索菜品"""
        self.refresh_meals_display()
        
    def filter_meals(self):
        """筛选菜品"""
        self.refresh_meals_display()
        
    def add_meal(self):
        """添加菜品"""
        dialog = MealDialog(self.parent_frame, "添加菜品")
        if dialog.result:
            # 生成新ID
            new_id = f"MEAL{len(self.meal_data) + 1:03d}"
            dialog.result['id'] = new_id
            dialog.result['created_date'] = datetime.datetime.now().strftime("%Y-%m-%d")
            
            # 添加到数据
            self.meal_data.append(dialog.result)
            
            # 保存到数据管理器
            self.save_meal_data()
            
            self.refresh_meals_display()
            messagebox.showinfo("成功", "菜品添加成功！")
            
            # 通知其他模块数据更新
            self.notify_data_update()
            
    def edit_meal(self, meal):
        """编辑菜品"""
        dialog = MealDialog(self.parent_frame, "编辑菜品", meal)
        if dialog.result:
            # 更新数据
            meal.update(dialog.result)
            
            # 保存到数据管理器
            self.save_meal_data()
            
            self.refresh_meals_display()
            messagebox.showinfo("成功", "菜品信息更新成功！")
            
            # 通知其他模块数据更新
            self.notify_data_update()
            
    def toggle_meal_status(self, meal):
        """切换菜品状态"""
        action = "上架" if not meal["is_available"] else "下架"
        if messagebox.askyesno("确认操作", f"确定要{action}菜品 '{meal['name']}' 吗？"):
            meal["is_available"] = not meal["is_available"]
            
            # 保存到数据管理器
            self.save_meal_data()
            
            self.refresh_meals_display()
            messagebox.showinfo("成功", f"菜品已{action}！")
            
            # 通知其他模块数据更新
            self.notify_data_update()
            
    def export_menu(self):
        """导出菜单"""
        messagebox.showinfo("导出菜单", "菜单导出功能开发中...")

class MealDialog:
    """菜品对话框"""
    def __init__(self, parent, title, meal_data=None):
        self.result = None
        
        # 创建对话框窗口
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("600x700")
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
        self.name_var = tk.StringVar(self.dialog, value=meal_data['name'] if meal_data else "")
        self.category_var = tk.StringVar(self.dialog, value=meal_data['category'] if meal_data else "")
        self.price_var = tk.DoubleVar(self.dialog, value=meal_data['price'] if meal_data else 0.0)
        self.cost_var = tk.DoubleVar(self.dialog, value=meal_data['cost'] if meal_data else 0.0)
        self.description_var = tk.StringVar(self.dialog, value=meal_data['description'] if meal_data else "")
        self.cooking_time_var = tk.IntVar(self.dialog, value=meal_data['cooking_time'] if meal_data else 0)
        self.calories_var = tk.IntVar(self.dialog, value=meal_data['calories'] if meal_data else 0)
        self.is_spicy_var = tk.BooleanVar(self.dialog, value=meal_data['is_spicy'] if meal_data else False)
        self.is_vegetarian_var = tk.BooleanVar(self.dialog, value=meal_data['is_vegetarian'] if meal_data else False)
        self.is_available_var = tk.BooleanVar(self.dialog, value=meal_data['is_available'] if meal_data else True)
        self.image_var = tk.StringVar(self.dialog, value=meal_data['image'] if meal_data else "🍽️")
        
        # 食材列表
        self.ingredients = meal_data['ingredients'].copy() if meal_data else []
        
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
        
        # 滚动区域
        canvas = tk.Canvas(main_frame, bg=self.colors['surface'])
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['surface'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # 标题
        title_label = tk.Label(scrollable_frame, text="🍜 菜品信息", font=self.fonts['heading'],
                              bg=self.colors['surface'], fg=self.colors['text_primary'])
        title_label.pack(pady=(0, 20))
        
        # 基本信息
        self.create_basic_info_section(scrollable_frame)
        
        # 详细信息
        self.create_detail_info_section(scrollable_frame)
        
        # 食材管理
        self.create_ingredients_section(scrollable_frame)
        
        # 选项设置
        self.create_options_section(scrollable_frame)
        
        # 按钮区域
        button_frame = tk.Frame(scrollable_frame, bg=self.colors['surface'])
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
        
    def create_basic_info_section(self, parent):
        """创建基本信息区域"""
        section_frame = tk.Frame(parent, bg=self.colors['surface'])
        section_frame.pack(fill="x", pady=(0, 20))
        
        section_title = tk.Label(section_frame, text="📝 基本信息", font=self.fonts['body'],
                                bg=self.colors['surface'], fg=self.colors['text_primary'])
        section_title.pack(anchor="w", pady=(0, 10))
        
        # 菜品名称
        self.create_form_field(section_frame, "菜品名称 *", self.name_var, "entry")
        
        # 分类和图标
        row_frame = tk.Frame(section_frame, bg=self.colors['surface'])
        row_frame.pack(fill="x", pady=10)
        
        left_frame = tk.Frame(row_frame, bg=self.colors['surface'])
        left_frame.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.create_form_field(left_frame, "分类 *", self.category_var, "combo", 
                              ["主食", "热菜", "素菜", "汤品", "饮品", "甜品"])
        
        right_frame = tk.Frame(row_frame, bg=self.colors['surface'])
        right_frame.pack(side="right", fill="x", expand=True, padx=(10, 0))
        self.create_form_field(right_frame, "图标", self.image_var, "entry")
        
        # 价格和成本
        row_frame2 = tk.Frame(section_frame, bg=self.colors['surface'])
        row_frame2.pack(fill="x", pady=10)
        
        left_frame2 = tk.Frame(row_frame2, bg=self.colors['surface'])
        left_frame2.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.create_form_field(left_frame2, "售价 (¥) *", self.price_var, "entry")
        
        right_frame2 = tk.Frame(row_frame2, bg=self.colors['surface'])
        right_frame2.pack(side="right", fill="x", expand=True, padx=(10, 0))
        self.create_form_field(right_frame2, "成本 (¥) *", self.cost_var, "entry")
        
    def create_detail_info_section(self, parent):
        """创建详细信息区域"""
        section_frame = tk.Frame(parent, bg=self.colors['surface'])
        section_frame.pack(fill="x", pady=(0, 20))
        
        section_title = tk.Label(section_frame, text="📋 详细信息", font=self.fonts['body'],
                                bg=self.colors['surface'], fg=self.colors['text_primary'])
        section_title.pack(anchor="w", pady=(0, 10))
        
        # 描述
        self.create_form_field(section_frame, "菜品描述", self.description_var, "text")
        
        # 制作时间和热量
        row_frame = tk.Frame(section_frame, bg=self.colors['surface'])
        row_frame.pack(fill="x", pady=10)
        
        left_frame = tk.Frame(row_frame, bg=self.colors['surface'])
        left_frame.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.create_form_field(left_frame, "制作时间 (分钟)", self.cooking_time_var, "entry")
        
        right_frame = tk.Frame(row_frame, bg=self.colors['surface'])
        right_frame.pack(side="right", fill="x", expand=True, padx=(10, 0))
        self.create_form_field(right_frame, "热量 (卡路里)", self.calories_var, "entry")
        
    def create_ingredients_section(self, parent):
        """创建食材区域"""
        section_frame = tk.Frame(parent, bg=self.colors['surface'])
        section_frame.pack(fill="x", pady=(0, 20))
        
        section_title = tk.Label(section_frame, text="🥗 食材配料", font=self.fonts['body'],
                                bg=self.colors['surface'], fg=self.colors['text_primary'])
        section_title.pack(anchor="w", pady=(0, 10))
        
        # 食材列表
        ingredients_frame = tk.Frame(section_frame, bg=self.colors['background'])
        ingredients_frame.pack(fill="x", pady=(0, 10))
        
        self.ingredients_listbox = tk.Listbox(ingredients_frame, height=4, font=self.fonts['body'])
        self.ingredients_listbox.pack(fill="x")
        
        # 添加食材
        add_ingredient_frame = tk.Frame(section_frame, bg=self.colors['surface'])
        add_ingredient_frame.pack(fill="x")
        
        self.ingredient_var = tk.StringVar()
        ingredient_entry = tk.Entry(add_ingredient_frame, textvariable=self.ingredient_var,
                                   font=self.fonts['body'], width=30)
        ingredient_entry.pack(side="left", padx=(0, 10), ipady=5)
        
        add_btn = tk.Button(add_ingredient_frame, text="添加", font=self.fonts['body'],
                           bg=self.colors['primary'], fg="white", bd=0,
                           cursor="hand2", command=self.add_ingredient, padx=15)
        add_btn.pack(side="left", padx=(0, 10))
        
        remove_btn = tk.Button(add_ingredient_frame, text="删除", font=self.fonts['body'],
                              bg=self.colors['background'], fg=self.colors['text_secondary'], bd=1,
                              cursor="hand2", command=self.remove_ingredient, padx=15)
        remove_btn.pack(side="left")
        
        # 刷新食材列表
        self.refresh_ingredients_list()
        
    def create_options_section(self, parent):
        """创建选项区域"""
        section_frame = tk.Frame(parent, bg=self.colors['surface'])
        section_frame.pack(fill="x", pady=(0, 20))
        
        section_title = tk.Label(section_frame, text="⚙️ 菜品设置", font=self.fonts['body'],
                                bg=self.colors['surface'], fg=self.colors['text_primary'])
        section_title.pack(anchor="w", pady=(0, 10))
        
        # 选项复选框
        options_frame = tk.Frame(section_frame, bg=self.colors['surface'])
        options_frame.pack(fill="x")
        
        spicy_check = tk.Checkbutton(options_frame, text="🌶️ 辣味菜品", variable=self.is_spicy_var,
                                    bg=self.colors['surface'], font=self.fonts['body'],
                                    activebackground=self.colors['surface'])
        spicy_check.pack(anchor="w", pady=2)
        
        veg_check = tk.Checkbutton(options_frame, text="🥬 素食菜品", variable=self.is_vegetarian_var,
                                  bg=self.colors['surface'], font=self.fonts['body'],
                                  activebackground=self.colors['surface'])
        veg_check.pack(anchor="w", pady=2)
        
        available_check = tk.Checkbutton(options_frame, text="✅ 当前在售", variable=self.is_available_var,
                                        bg=self.colors['surface'], font=self.fonts['body'],
                                        activebackground=self.colors['surface'])
        available_check.pack(anchor="w", pady=2)
        
    def create_form_field(self, parent, label_text, variable, field_type, options=None):
        """创建表单字段"""
        field_frame = tk.Frame(parent, bg=self.colors['surface'])
        field_frame.pack(fill="x", pady=5)
        
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
        elif field_type == "text":
            text_entry = tk.Entry(field_frame, textvariable=variable, font=self.fonts['body'],
                                 bg=self.colors['background'], bd=1, relief="solid")
            text_entry.pack(fill="x", ipady=8)
            
    def add_ingredient(self):
        """添加食材"""
        ingredient = self.ingredient_var.get().strip()
        if ingredient and ingredient not in self.ingredients:
            self.ingredients.append(ingredient)
            self.ingredient_var.set("")
            self.refresh_ingredients_list()
            
    def remove_ingredient(self):
        """删除食材"""
        selection = self.ingredients_listbox.curselection()
        if selection:
            index = selection[0]
            del self.ingredients[index]
            self.refresh_ingredients_list()
            
    def refresh_ingredients_list(self):
        """刷新食材列表"""
        self.ingredients_listbox.delete(0, tk.END)
        for ingredient in self.ingredients:
            self.ingredients_listbox.insert(tk.END, ingredient)
            
    def ok(self):
        """确定按钮处理"""
        # 验证必填字段
        if not self.name_var.get().strip():
            messagebox.showerror("错误", "请输入菜品名称")
            return
        if not self.category_var.get().strip():
            messagebox.showerror("错误", "请选择菜品分类")
            return
            
        # 验证数值
        try:
            price = self.price_var.get()
            cost = self.cost_var.get()
            cooking_time = self.cooking_time_var.get()
            calories = self.calories_var.get()
            
            if price <= 0 or cost <= 0:
                messagebox.showerror("错误", "价格和成本必须大于0")
                return
                
            if cooking_time < 0 or calories < 0:
                messagebox.showerror("错误", "制作时间和热量不能为负数")
                return
                
        except tk.TclError:
            messagebox.showerror("错误", "请输入有效的数值")
            return
        
        # 保存结果
        self.result = {
            'name': self.name_var.get().strip(),
            'category': self.category_var.get(),
            'price': price,
            'cost': cost,
            'description': self.description_var.get().strip(),
            'ingredients': self.ingredients.copy(),
            'cooking_time': cooking_time,
            'calories': calories,
            'is_spicy': self.is_spicy_var.get(),
            'is_vegetarian': self.is_vegetarian_var.get(),
            'is_available': self.is_available_var.get(),
            'image': self.image_var.get().strip() or "🍽️"
        }
        
        self.dialog.destroy()
        
    def cancel(self):
        """取消按钮处理"""
        self.dialog.destroy()

if __name__ == "__main__":
    # 测试代码
    root = tk.Tk()
    root.title("现代化菜品管理模块测试")
    root.geometry("1400x900")
    root.configure(bg="#f8f9fa")
    
    title_frame = tk.Frame(root, bg="#ffffff", height=70)
    title_frame.pack(fill="x")
    title_frame.pack_propagate(False)
    
    main_frame = tk.Frame(root, bg="#f8f9fa")
    main_frame.pack(fill="both", expand=True)
    
    meal_module = ModernMealModule(main_frame, title_frame)
    meal_module.show()
    
    root.mainloop()
