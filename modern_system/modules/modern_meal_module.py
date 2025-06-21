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
            'card_shadow': '#F0F0F0',   # 卡片阴影
            'info': '#366092',         # 信息色
            'white': '#FFFFFF',        # 白色
            'danger': '#E74C3C'        # 危险色
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
        
        # 统计标签引用
        self.stats_labels = {}
    
    def load_meal_data(self):
        """从数据管理中心加载菜品数据"""
        try:
            # get_meals 已经做了UI字段兼容
            return data_manager.get_meals()
        except Exception as e:
            print(f"❌ 加载菜品数据失败: {e}")
            return []
    
    def save_meal_data(self):
        """保存菜品数据到数据管理中心 - 此方法已废弃，操作应实时保存"""
        print("⚠️ save_meal_data 方法已废弃，所有操作应实时调用data_manager。")
        return False
    
    def notify_data_update(self):
        """通知其他模块数据已更新"""
        print("📢 通知所有模块菜品数据已更新...")
        # 这是一个简化的实现，实际项目中可能需要更精细的发布/订阅系统
        sales_module = data_manager.get_module('sales')
        if sales_module and hasattr(sales_module, 'refresh_meals_data'):
            try:
                sales_module.refresh_meals_data()
                print("✅ 已通知销售模块刷新")
            except Exception as e:
                print(f"⚠️ 通知销售模块失败: {e}")
        
        inventory_module = data_manager.get_module('inventory')
        if inventory_module and hasattr(inventory_module, 'refresh_possible_meals'):
            try:
                inventory_module.refresh_possible_meals()
                print("✅ 已通知库存模块刷新可制作菜品")
            except Exception as e:
                print(f"⚠️ 通知库存模块失败: {e}")
    
    def show(self):
        """显示菜品配置模块"""
        # 注册到数据管理器
        data_manager.register_module('meal', self)
        
        # 重新加载最新数据
        self.meal_data = self.load_meal_data()
        
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
        
        # 添加菜品按钮
        add_btn = tk.Button(action_frame, text="➕ 添加菜品", 
                           font=('Microsoft YaHei UI', 10),
                           bg=self.colors['primary'], fg=self.colors['white'],
                           bd=0, padx=20, pady=8, cursor='hand2',
                           command=self.add_meal)
        add_btn.pack(side='right', padx=5)
        
        # 刷新按钮
        refresh_btn = tk.Button(action_frame, text="🔄 刷新", 
                               font=('Microsoft YaHei UI', 10),
                               bg=self.colors['info'], fg=self.colors['white'],
                               bd=0, padx=20, pady=8, cursor='hand2',
                               command=self.refresh_meals)
        refresh_btn.pack(side='right', padx=5)
        
        # 导出按钮
        export_btn = tk.Button(action_frame, text="📊 导出", 
                              font=('Microsoft YaHei UI', 10),
                              bg=self.colors['success'], fg=self.colors['white'],
                              bd=0, padx=20, pady=8, cursor='hand2',
                              command=self.export_meals)
        export_btn.pack(side='right', padx=5)
        
    def create_meal_interface(self):
        """创建菜品管理界面"""
        # 主容器
        main_container = tk.Frame(self.parent_frame, bg=self.colors['background'])
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # 顶部统计卡片
        self.create_stats_cards(main_container)
        
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
        # 清空现有显示
        for widget in self.meals_container.winfo_children():
            widget.destroy()
        
        # 获取所有菜品数据
        meals_to_show = self.get_filtered_meals()
        
        if not meals_to_show:
            no_data_label = tk.Label(self.meals_container, 
                                   text="暂无菜品数据",
                                   font=self.fonts['body'],
                                   bg=self.colors['background'],
                                   fg=self.colors['text_secondary'])
            no_data_label.pack(pady=50)
            return
        
        # 创建网格布局
        row = 0
        col = 0
        max_cols = 4
        
        for meal in meals_to_show:
            self.create_meal_card(self.meals_container, meal, row, col)
            
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
        
        # 配置网格权重
        for i in range(max_cols):
            self.meals_container.grid_columnconfigure(i, weight=1)
        
        # 更新统计卡片
        self.update_stats_cards()
        
    def get_filtered_meals(self):
        """获取筛选后的菜品列表"""
        # 直接返回所有菜品，不进行筛选
        return self.meal_data
    
    def filter_meals(self):
        """筛选菜品（已简化，直接刷新显示）"""
        self.refresh_meals_display()
        
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
        total_meals = len(self.meal_data)
        available_meals = len([meal for meal in self.meal_data if meal['is_available']])
        avg_price = sum(meal['price'] for meal in self.meal_data) / total_meals if total_meals > 0 else 0
        spicy_meals = len([meal for meal in self.meal_data if meal['is_spicy']])
        
        # 更新标签
        if "菜品总数" in self.stats_labels:
            self.stats_labels["菜品总数"].config(text=f"{total_meals}")
        if "在售菜品" in self.stats_labels:
            self.stats_labels["在售菜品"].config(text=f"{available_meals}")
        if "平均价格" in self.stats_labels:
            self.stats_labels["平均价格"].config(text=f"¥{avg_price:.1f}")
        if "辣味菜品" in self.stats_labels:
            self.stats_labels["辣味菜品"].config(text=f"{spicy_meals}")
            
    def add_meal(self):
        """添加新菜品"""
        dialog = MealDialog(self.parent_frame, "添加新菜品")
        if dialog.result:
            try:
                meal_info = dialog.result['basic_info']
                ingredients = dialog.result['ingredients']
                new_meal_id = data_manager.add_meal(meal_info)
                if ingredients:
                    data_manager.update_meal_recipe(new_meal_id, ingredients)
                messagebox.showinfo("成功", f"菜品 '{meal_info['name']}' 添加成功！")
                self.refresh_meals()
                self.notify_data_update()
            except Exception as e:
                messagebox.showerror("添加失败", f"添加菜品时出错: {e}")

    def edit_meal(self, meal):
        """编辑菜品"""
        dialog = MealDialog(self.parent_frame, f"编辑菜品 - {meal['name']}", meal_data=meal)
        if dialog.result:
            try:
                meal_info = dialog.result['basic_info']
                ingredients = dialog.result['ingredients']
                meal_id = meal['id']
                data_manager.update_meal(meal_id, meal_info)
                data_manager.update_meal_recipe(meal_id, ingredients)
                messagebox.showinfo("成功", f"菜品 '{meal_info['name']}' 更新成功！")
                self.refresh_meals()
                self.notify_data_update()
            except Exception as e:
                messagebox.showerror("更新失败", f"更新菜品时出错: {e}")

    def toggle_meal_status(self, meal):
        """上架或下架菜品"""
        new_status = not meal.get('is_available', False)
        action_text = "上架" if new_status else "下架"
        
        if messagebox.askyesno("确认操作", f"确定要 {action_text} 菜品 '{meal['name']}' 吗？"):
            try:
                data_manager.update_meal(meal['id'], {'is_available': new_status})
                messagebox.showinfo("成功", f"菜品已成功 {action_text}！")
                self.refresh_meals()
                self.notify_data_update()
            except Exception as e:
                messagebox.showerror("操作失败", f"操作失败: {e}")
            
    def export_meals(self):
        """导出菜品数据"""
        try:
            from tkinter import filedialog
            import datetime
            
            # 创建导出选择对话框
            dialog = tk.Toplevel(self.parent_frame)
            dialog.title("导出菜品数据")
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
            tk.Label(dialog, text="导出菜品数据", font=('Microsoft YaHei UI', 14, 'bold'),
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
            
            # 菜品状态筛选
            tk.Label(options_frame, text="菜品状态:", font=('Microsoft YaHei UI', 12),
                    bg=self.colors['background'], fg=self.colors['text']).pack(anchor="w", pady=(20, 10))
            
            status_var = tk.StringVar(dialog, value="全部")
            status_options = ["全部", "上架", "下架"]
            
            status_combo = ttk.Combobox(options_frame, textvariable=status_var, 
                                      values=status_options, state="readonly", width=20)
            status_combo.pack(anchor="w")
            
            # 按钮框架
            btn_frame = tk.Frame(dialog, bg=self.colors['background'])
            btn_frame.pack(fill="x", padx=20, pady=20)
            
            def do_export():
                try:
                    file_format = format_var.get()
                    meal_status = status_var.get()
                    
                    # 获取当前时间戳
                    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"菜品数据_{meal_status}_{timestamp}"
                    
                    # 选择保存路径
                    if file_format == "Excel":
                        file_path = filedialog.asksaveasfilename(
                            defaultextension=".xlsx",
                            filetypes=[("Excel文件", "*.xlsx")],
                            initialname=filename
                        )
                        if file_path:
                            success = self.export_meals_to_excel(file_path, meal_status)
                    elif file_format == "CSV":
                        file_path = filedialog.asksaveasfilename(
                            defaultextension=".csv",
                            filetypes=[("CSV文件", "*.csv")],
                            initialname=filename
                        )
                        if file_path:
                            success = self.export_meals_to_csv(file_path, meal_status)
                    elif file_format == "PDF":
                        file_path = filedialog.asksaveasfilename(
                            defaultextension=".pdf",
                            filetypes=[("PDF文件", "*.pdf")],
                            initialname=filename
                        )
                        if file_path:
                            success = self.export_meals_to_pdf(file_path, meal_status)
                    
                    if success:
                        messagebox.showinfo("导出成功", f"菜品数据已成功导出为 {file_format} 格式", parent=dialog)
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
    
    def export_meals_to_excel(self, file_path: str, meal_status: str) -> bool:
        """导出菜品为Excel格式"""
        try:
            import openpyxl
            from openpyxl.styles import Font, Alignment, PatternFill
            
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "菜品数据"
            
            # 设置标题
            title = f"智慧餐饮管理系统 - 菜品数据 ({meal_status})"
            ws['A1'] = title
            ws['A1'].font = Font(size=16, bold=True)
            ws.merge_cells('A1:F1')
            
            # 设置表头样式
            header_font = Font(bold=True, color="FFFFFF")
            header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
            header_alignment = Alignment(horizontal="center", vertical="center")
            
            # 表头
            headers = ["菜品名称", "价格", "分类", "状态", "描述", "创建时间"]
            ws.append(headers)
            
            # 设置表头样式
            for cell in ws[2]:
                cell.font = header_font
                cell.fill = header_fill
                cell.alignment = header_alignment
            
            # 获取菜品数据
            meals = self.get_filtered_meals_for_export(meal_status)
            
            # 添加数据
            for meal in meals:
                row = [
                    meal.get('name', ''),
                    f"￥{meal.get('price', 0):.2f}",
                    meal.get('category', ''),
                    meal.get('status', ''),
                    meal.get('description', ''),
                    meal.get('created_at', '')
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
    
    def export_meals_to_csv(self, file_path: str, meal_status: str) -> bool:
        """导出菜品为CSV格式"""
        try:
            import csv
            
            with open(file_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
                fieldnames = ["菜品名称", "价格", "分类", "状态", "描述", "创建时间"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                # 获取菜品数据
                meals = self.get_filtered_meals_for_export(meal_status)
                
                for meal in meals:
                    writer.writerow({
                        "菜品名称": meal.get('name', ''),
                        "价格": f"￥{meal.get('price', 0):.2f}",
                        "分类": meal.get('category', ''),
                        "状态": meal.get('status', ''),
                        "描述": meal.get('description', ''),
                        "创建时间": meal.get('created_at', '')
                    })
            
            return True
            
        except Exception as e:
            print(f"导出CSV失败: {e}")
            return False
    
    def export_meals_to_pdf(self, file_path: str, meal_status: str) -> bool:
        """导出菜品为PDF格式"""
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
            title = Paragraph(f"智慧餐饮管理系统 - 菜品数据 ({meal_status})", title_style)
            story.append(title)
            story.append(Spacer(1, 20))
            
            # 获取菜品数据
            meals = self.get_filtered_meals_for_export(meal_status)
            
            # 创建表格数据
            table_data = [["菜品名称", "价格", "分类", "状态", "描述", "创建时间"]]
            
            for meal in meals:
                row = [
                    meal.get('name', ''),
                    f"￥{meal.get('price', 0):.2f}",
                    meal.get('category', ''),
                    meal.get('status', ''),
                    meal.get('description', ''),
                    meal.get('created_at', '')
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
    
    def get_filtered_meals_for_export(self, meal_status: str) -> List[Dict]:
        """获取筛选后的菜品数据用于导出"""
        if meal_status == "全部":
            return self.meal_data
        else:
            return [meal for meal in self.meal_data if meal.get('status') == meal_status]
    
    def refresh_meals(self):
        """刷新菜品数据"""
        try:
            # 重新加载菜品数据
            self.meal_data = data_manager.get_meals()
            # 重新显示菜品列表
            self.refresh_meals_display()
            messagebox.showinfo("刷新成功", "菜品数据已刷新")
        except Exception as e:
            messagebox.showerror("刷新失败", f"刷新菜品数据时发生错误：{e}")

class MealDialog:
    """菜品编辑/添加对话框，带配方管理"""
    def __init__(self, parent, title, meal_data=None):
        self.result = None
        self.meal_data = meal_data if meal_data else {}
        
        # 从数据管理器获取所有可用作配料的库存物品
        try:
            self.all_ingredients_master = data_manager.get_inventory()
        except Exception as e:
            print(f"❌ 无法从数据库获取原料列表: {e}")
            self.all_ingredients_master = []

        # 获取当前菜品的配方
        self.current_ingredients = []
        if self.meal_data.get('id'):
            try:
                # 注意：get_recipes返回的是所有菜品的配方列表
                all_recipes = data_manager.get_recipes()
                this_recipe = next((r for r in all_recipes if r['meal_id'] == self.meal_data['id']), None)
                if this_recipe and 'ingredients' in this_recipe:
                    # 将数据库配方格式转换为UI所需格式
                    for ing_db in this_recipe['ingredients']:
                        ing_master = next((m for m in self.all_ingredients_master if m['name'] == ing_db['ingredient_name']), None)
                        if ing_master:
                            self.current_ingredients.append({
                                'id': ing_master['id'],
                                'name': ing_db['ingredient_name'],
                                'quantity': ing_db['quantity_per_serving'],
                                'unit': ing_master.get('unit', '')
                            })
            except Exception as e:
                print(f"❌ 获取菜品配方失败: {e}")

        # 创建对话框窗口
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("550x750")
        self.colors = {
            'primary': '#FF6B35', 'background': '#F8F9FA', 'surface': '#FFFFFF',
            'text_primary': '#2D3436', 'text_secondary': '#636E72', 'border': '#E0E0E0'
        }
        self.fonts = {
            'heading': ('Microsoft YaHei UI', 16, 'bold'), 'body': ('Microsoft YaHei UI', 12),
            'button': ('Microsoft YaHei UI', 11, 'bold'), 'subheading': ('Microsoft YaHei UI', 14, 'bold')
        }
        self.dialog.configure(bg=self.colors['background'])
        self.dialog.resizable(False, False)
        self.dialog.grab_set()

        # 初始化UI变量
        self.name_var = tk.StringVar(self.dialog, value=self.meal_data.get('name', ''))
        self.category_var = tk.StringVar(self.dialog, value=self.meal_data.get('category', ''))
        self.price_var = tk.DoubleVar(self.dialog, value=self.meal_data.get('price', 0.0))
        self.cost_var = tk.DoubleVar(self.dialog, value=self.meal_data.get('cost', 0.0))
        self.is_available_var = tk.BooleanVar(self.dialog, value=self.meal_data.get('is_available', True))
        self.description_var = None # Text组件不能直接用StringVar

        self.create_dialog_ui()

    def create_dialog_ui(self):
        """创建对话框界面"""
        main_frame = tk.Frame(self.dialog, bg=self.colors['surface'])
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        tk.Label(main_frame, text="🍽️ 菜品信息", font=self.fonts['heading'], bg=self.colors['surface'], fg=self.colors['text_primary']).pack(pady=(0, 20))
        
        self.create_form_field(main_frame, "菜品名称 *", self.name_var, "entry")
        self.create_form_field(main_frame, "菜品分类 *", self.category_var, "combo", ["主食", "炒菜", "汤羹", "凉菜", "饮品", "小食"])
        self.create_form_field(main_frame, "售价 *", self.price_var, "entry")
        self.create_form_field(main_frame, "成本", self.cost_var, "entry")
        self.create_form_field(main_frame, "描述", None, "text")
        
        self.create_ingredients_section(main_frame)
        self.create_options_section(main_frame)

        button_frame = tk.Frame(main_frame, bg=self.colors['surface'])
        button_frame.pack(fill="x", pady=(20, 0))
        tk.Button(button_frame, text="取消", font=self.fonts['button'], bg=self.colors['background'], fg=self.colors['text_secondary'], bd=0, command=self.cancel, padx=30, pady=10).pack(side="right", padx=(10, 0))
        tk.Button(button_frame, text="确定", font=self.fonts['button'], bg=self.colors['primary'], fg="white", bd=0, command=self.ok, padx=30, pady=10).pack(side="right")

    def create_ingredients_section(self, parent):
        """创建配方管理部分"""
        section_frame = tk.Frame(parent, bg=self.colors['background'], bd=1, relief="groove", padx=5, pady=5)
        section_frame.pack(fill="x", pady=10)
        
        tk.Label(section_frame, text="🥬 配方管理", font=self.fonts['subheading'], bg=self.colors['background'], fg=self.colors['text_primary']).pack(pady=5)
        
        add_frame = tk.Frame(section_frame, bg=self.colors['background'])
        add_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Label(add_frame, text="选择原料:", bg=self.colors['background']).pack(side="left")
        self.ingredient_var = tk.StringVar()
        ingredient_names = [ing['name'] for ing in self.all_ingredients_master]
        self.ingredient_combo = ttk.Combobox(add_frame, textvariable=self.ingredient_var, values=ingredient_names, width=15, state="readonly")
        self.ingredient_combo.pack(side="left", padx=5)

        tk.Label(add_frame, text="数量:", bg=self.colors['background']).pack(side="left")
        self.quantity_var = tk.DoubleVar(value=0.1)
        tk.Entry(add_frame, textvariable=self.quantity_var, width=8).pack(side="left", padx=5)

        tk.Button(add_frame, text="➕ 添加", command=self.add_ingredient).pack(side="left", padx=10)

        list_frame = tk.Frame(section_frame)
        list_frame.pack(fill="both", expand=True, padx=10, pady=5)
        self.ingredients_listbox = tk.Listbox(list_frame, height=5)
        self.ingredients_listbox.pack(side="left", fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.ingredients_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.ingredients_listbox.config(yscrollcommand=scrollbar.set)
        
        tk.Button(section_frame, text="🗑️ 删除选中配料", command=self.remove_ingredient).pack(pady=5)
        
        self.refresh_ingredients_list()

    def add_ingredient(self):
        """添加配料到列表"""
        name = self.ingredient_var.get()
        try:
            quantity = self.quantity_var.get()
        except tk.TclError:
            messagebox.showwarning("输入错误", "请输入有效的数量。")
            return

        if not name or quantity <= 0:
            messagebox.showwarning("输入错误", "请选择一个原料并输入正数数量。")
            return
            
        selected_ingredient = next((ing for ing in self.all_ingredients_master if ing['name'] == name), None)
        if not selected_ingredient:
            messagebox.showerror("错误", "选择的原料不存在！")
            return

        if any(ing['id'] == selected_ingredient['id'] for ing in self.current_ingredients):
            messagebox.showwarning("重复添加", "该原料已在配方中。")
            return

        self.current_ingredients.append({
            'id': selected_ingredient['id'], # ingredient_id
            'name': name, 'quantity': quantity, 'unit': selected_ingredient.get('unit', '')
        })
        self.refresh_ingredients_list()
        self.ingredient_var.set('')
        self.quantity_var.set(0.1)

    def remove_ingredient(self):
        """从列表中移除配料"""
        selected_indices = self.ingredients_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("未选择", "请选择要删除的配料。")
            return
        
        # 从后往前删，避免索引错乱
        for i in sorted(selected_indices, reverse=True):
            del self.current_ingredients[i]
        self.refresh_ingredients_list()

    def refresh_ingredients_list(self):
        """刷新配料列表显示"""
        self.ingredients_listbox.delete(0, tk.END)
        for ing in self.current_ingredients:
            display_text = f"{ing['name']} - {ing['quantity']} {ing.get('unit', '')}"
            self.ingredients_listbox.insert(tk.END, display_text)

    def create_options_section(self, parent):
        """创建开关选项"""
        options_frame = tk.Frame(parent, bg=self.colors['surface'])
        options_frame.pack(fill="x", pady=10)
        tk.Checkbutton(options_frame, text="是否上架", variable=self.is_available_var, bg=self.colors['surface']).pack(side="left")

    def create_form_field(self, parent, label_text, variable, field_type, options=None):
        """通用表单字段创建器"""
        field_frame = tk.Frame(parent, bg=self.colors['surface'])
        field_frame.pack(fill="x", pady=8)
        
        label = tk.Label(field_frame, text=label_text, font=self.fonts['body'], bg=self.colors['surface'], fg=self.colors['text_secondary'], anchor="w", width=10)
        label.pack(side="left")
        
        if field_type == "entry":
            widget = tk.Entry(field_frame, textvariable=variable, font=self.fonts['body'], bg=self.colors['background'], bd=1, relief="solid")
        elif field_type == "combo":
            widget = ttk.Combobox(field_frame, textvariable=variable, values=options, font=self.fonts['body'], state="readonly")
        elif field_type == "text":
            widget = tk.Text(field_frame, height=4, font=self.fonts['body'], bg=self.colors['background'], bd=1, relief="solid")
            self.description_var = widget
            widget.insert("1.0", self.meal_data.get('description', ''))
        
        widget.pack(side="left", fill="x", expand=True, padx=10)

    def ok(self):
        """点击确定，验证并收集数据"""
        try:
            price = self.price_var.get()
            cost = self.cost_var.get()
            if price < 0 or cost < 0:
                messagebox.showerror("错误", "价格和成本不能为负数")
                return
        except tk.TclError:
            messagebox.showerror("错误", "请输入有效的价格和成本")
            return
            
        if not self.name_var.get().strip():
            messagebox.showerror("错误", "请输入菜品名称")
            return

        self.result = {
            'basic_info': {
                'name': self.name_var.get().strip(), 'category': self.category_var.get(),
                'price': price, 'cost': cost,
                'description': self.description_var.get("1.0", tk.END).strip(),
                'is_available': self.is_available_var.get(),
            },
            'ingredients': self.current_ingredients
        }
        self.dialog.destroy()
        
    def cancel(self):
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
