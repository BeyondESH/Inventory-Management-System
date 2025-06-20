#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
销售模块 - 堂食点单系统
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, List, Any
import datetime

class SalesModule:
    def __init__(self, parent_frame, title_frame, meal_module=None, inventory_module=None, order_module=None):
        self.parent_frame = parent_frame
        self.title_frame = title_frame
        self.meal_module = meal_module
        self.inventory_module = inventory_module
        self.order_module = order_module
        
        # 购物车数据
        self.cart_items = []
        self.total_amount = 0.0
        
        # 客户信息变量
        self.customer_name_var = tk.StringVar() if parent_frame else None
        self.table_var = tk.StringVar() if parent_frame else None
        self.total_var = tk.StringVar(value="¥0.00") if parent_frame else None
        
        # UI组件引用
        self.status_label = None
        self.cart_listbox_frame = None
        
    def show(self):
        """显示销售模块"""
        # 清空标题栏
        for widget in self.title_frame.winfo_children():
            widget.destroy()
            
        # 清空内容区域
        for widget in self.parent_frame.winfo_children():
            widget.destroy()
            
        # 标题
        title_label = tk.Label(self.title_frame, text="🛒 堂食点单", font=("微软雅黑", 16, "bold"),
                             bg="#ffffff", fg="#2c3e50")
        title_label.pack(side="left", padx=20, pady=15)
        
        # 状态提醒区域
        status_frame = tk.Frame(self.title_frame, bg="#ffffff")
        status_frame.pack(side="left", padx=(20, 0), pady=15)
        
        self.status_label = tk.Label(status_frame, text="💡 选择菜品开始点单", 
                                   font=("微软雅黑", 10), bg="#ffffff", fg="#7f8c8d")
        self.status_label.pack()
        
        # 创建主框架
        main_frame = tk.Frame(self.parent_frame, bg="#ecf0f1")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # 左侧菜品区域（占60%）
        left_frame = tk.Frame(main_frame, bg="#ffffff", relief="raised", bd=1)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # 右侧购物车区域（占40%）
        right_frame = tk.Frame(main_frame, bg="#ffffff", relief="raised", bd=1)
        right_frame.pack(side="right", fill="y", padx=(10, 0))
        right_frame.config(width=400)
        
        self.create_menu_area(left_frame)
        self.create_cart_area(right_frame)
        
    def create_menu_area(self, parent):
        """创建菜品显示区域"""
        # 菜品区域标题
        menu_title = tk.Label(parent, text="📋 菜品选择", font=("微软雅黑", 14, "bold"),
                            bg="#ffffff", fg="#2c3e50")
        menu_title.pack(pady=15)
        
        # 创建滚动框架
        canvas = tk.Canvas(parent, bg="#ffffff")
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#ffffff")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=15, pady=(0, 15))
        scrollbar.pack(side="right", fill="y")
        
        # 菜品网格布局
        self.display_menu_items(scrollable_frame)
        
        # 绑定鼠标滚轮
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
    def display_menu_items(self, parent):
        """显示菜品列表"""
        if not self.meal_module or not hasattr(self.meal_module, 'meal_data'):
            no_data_label = tk.Label(parent, text="暂无菜品数据", font=("微软雅黑", 12),
                                   bg="#ffffff", fg="#7f8c8d")
            no_data_label.pack(pady=50)
            return
            
        # 按类别组织菜品
        categories = {}
        for meal in self.meal_module.meal_data:
            category = meal.get("category", "其他")
            if category not in categories:
                categories[category] = []
            categories[category].append(meal)
        
        row = 0
        for category, meals in categories.items():
            # 类别标题
            category_label = tk.Label(parent, text=f"🍽️ {category}", 
                                    font=("微软雅黑", 12, "bold"),
                                    bg="#ffffff", fg="#2c3e50")
            category_label.grid(row=row, column=0, columnspan=3, sticky="w", padx=15, pady=(15, 5))
            row += 1
            
            # 菜品卡片
            col = 0
            for meal in meals:
                self.create_meal_card(parent, meal, row, col)
                col += 1
                if col >= 3:  # 每行3个
                    col = 0
                    row += 1
            
            if col > 0:  # 如果最后一行没满，移到下一行
                row += 1
                
    def create_meal_card(self, parent, meal, row, col):
        """创建菜品卡片"""
        card_frame = tk.Frame(parent, bg="#f8f9fa", relief="solid", bd=1)
        card_frame.grid(row=row, column=col, padx=10, pady=8, sticky="nsew")
        
        # 菜品名称
        name_label = tk.Label(card_frame, text=meal["name"], font=("微软雅黑", 11, "bold"),
                            bg="#f8f9fa", fg="#2c3e50")
        name_label.pack(pady=(10, 5))
        
        # 价格
        price_label = tk.Label(card_frame, text=f"¥{meal['price']:.2f}", 
                             font=("微软雅黑", 10), bg="#f8f9fa", fg="#e74c3c")
        price_label.pack(pady=(0, 5))
        
        # 库存状态
        if self.inventory_module:
            can_order, stock_msg = self.inventory_module.check_ingredients_availability(meal["name"], 1)
            if can_order:
                stock_label = tk.Label(card_frame, text="✅ 有库存", font=("微软雅黑", 9),
                                     bg="#f8f9fa", fg="#27ae60")
            else:
                stock_label = tk.Label(card_frame, text="❌ 缺库存", font=("微软雅黑", 9),
                                     bg="#f8f9fa", fg="#e74c3c")
        else:
            stock_label = tk.Label(card_frame, text="未知库存", font=("微软雅黑", 9),
                                 bg="#f8f9fa", fg="#7f8c8d")
        stock_label.pack(pady=(0, 5))
        
        # 添加按钮
        add_btn = tk.Button(card_frame, text="➕ 添加", font=("微软雅黑", 9),
                          bg="#3498db", fg="white", relief="flat",
                          command=lambda m=meal: self.add_to_cart(m))
        add_btn.pack(pady=(0, 10), padx=10, fill="x")
        
        # 鼠标悬停效果
        def on_enter(e):
            card_frame.config(bg="#e8f4f8")
            name_label.config(bg="#e8f4f8")
            price_label.config(bg="#e8f4f8")
            stock_label.config(bg="#e8f4f8")
            
        def on_leave(e):
            card_frame.config(bg="#f8f9fa")
            name_label.config(bg="#f8f9fa")
            price_label.config(bg="#f8f9fa")
            stock_label.config(bg="#f8f9fa")
            
        card_frame.bind("<Enter>", on_enter)
        card_frame.bind("<Leave>", on_leave)
        
    def create_cart_area(self, parent):
        """创建购物车区域"""
        # 购物车标题
        cart_title = tk.Label(parent, text="🛒 购物车", font=("微软雅黑", 14, "bold"),
                            bg="#ffffff", fg="#2c3e50")
        cart_title.pack(pady=15)
        
        # 客户信息区域
        info_frame = tk.Frame(parent, bg="#ffffff")
        info_frame.pack(fill="x", padx=15, pady=(0, 10))
        
        # 桌号输入
        tk.Label(info_frame, text="桌号:", font=("微软雅黑", 10),
                bg="#ffffff", fg="#2c3e50").pack(anchor="w")
        table_entry = tk.Entry(info_frame, textvariable=self.table_var, font=("微软雅黑", 10))
        table_entry.pack(fill="x", pady=(2, 10))
        table_entry.insert(0, "A01")  # 默认桌号
        
        # 购物车列表区域
        cart_frame = tk.Frame(parent, bg="#ffffff")
        cart_frame.pack(fill="both", expand=True, padx=15)
        
        # 购物车列表
        self.cart_listbox_frame = tk.Frame(cart_frame, bg="#f8f9fa", relief="sunken", bd=1)
        self.cart_listbox_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        # 总计显示
        total_frame = tk.Frame(parent, bg="#ffffff")
        total_frame.pack(fill="x", padx=15, pady=(0, 10))
        
        tk.Label(total_frame, text="总计:", font=("微软雅黑", 12, "bold"),
                bg="#ffffff", fg="#2c3e50").pack(side="left")
        tk.Label(total_frame, textvariable=self.total_var, font=("微软雅黑", 12, "bold"),
                bg="#ffffff", fg="#e74c3c").pack(side="right")
        
        # 操作按钮
        btn_frame = tk.Frame(parent, bg="#ffffff")
        btn_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        clear_btn = tk.Button(btn_frame, text="🗑️ 清空", font=("微软雅黑", 10),
                            bg="#95a5a6", fg="white", relief="flat",
                            command=self.clear_cart)
        clear_btn.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        checkout_btn = tk.Button(btn_frame, text="💳 结算", font=("微软雅黑", 10),
                               bg="#27ae60", fg="white", relief="flat",
                               command=self.checkout)
        checkout_btn.pack(side="right", fill="x", expand=True, padx=(5, 0))
        
        # 初始化购物车显示
        self.update_cart_display()
        
    def add_to_cart(self, meal):
        """添加菜品到购物车"""
        # 检查库存
        if self.inventory_module:
            can_order, message = self.inventory_module.check_ingredients_availability(meal["name"], 1)
            if not can_order:
                if self.parent_frame:
                    messagebox.showerror("库存不足", f"无法添加 {meal['name']}:\n{message}")
                return
        
        # 检查购物车中是否已有该菜品
        existing_item = None
        for item in self.cart_items:
            if item["name"] == meal["name"]:
                existing_item = item
                break
        
        if existing_item:
            # 增加数量
            existing_item["quantity"] += 1
            existing_item["subtotal"] = existing_item["quantity"] * existing_item["price"]
        else:
            # 添加新菜品
            cart_item = {
                "id": meal["id"],
                "name": meal["name"],
                "price": meal["price"],
                "quantity": 1,
                "subtotal": meal["price"]
            }
            self.cart_items.append(cart_item)
        
        # 更新显示
        self.update_cart_display()
        if self.status_label:
            self.status_label.config(text=f"✅ 已添加 {meal['name']}", fg="#27ae60")
            
    def remove_from_cart(self, item_name):
        """从购物车移除菜品"""
        self.cart_items = [item for item in self.cart_items if item["name"] != item_name]
        self.update_cart_display()
        if self.status_label:
            self.status_label.config(text=f"🗑️ 已移除 {item_name}", fg="#e74c3c")
    
    def update_quantity(self, item_name, new_quantity):
        """更新菜品数量"""
        if new_quantity <= 0:
            self.remove_from_cart(item_name)
            return
            
        for item in self.cart_items:
            if item["name"] == item_name:
                # 检查库存
                if self.inventory_module:
                    can_order, message = self.inventory_module.check_ingredients_availability(
                        item_name, new_quantity)
                    if not can_order:
                        if self.parent_frame:
                            messagebox.showerror("库存不足", f"无法更新数量:\n{message}")
                        return
                
                item["quantity"] = new_quantity
                item["subtotal"] = item["quantity"] * item["price"]
                break
        
        self.update_cart_display()
        
    def update_cart_display(self):
        """更新购物车显示"""
        if not self.cart_listbox_frame:
            return
            
        # 清空现有显示
        for widget in self.cart_listbox_frame.winfo_children():
            widget.destroy()
        
        if not self.cart_items:
            empty_label = tk.Label(self.cart_listbox_frame, text="购物车为空", 
                                 font=("微软雅黑", 10), bg="#f8f9fa", fg="#7f8c8d")
            empty_label.pack(pady=20)
        else:
            for item in self.cart_items:
                self.create_cart_item_widget(item)
        
        # 更新总计
        self.total_amount = sum(item["subtotal"] for item in self.cart_items)
        if self.total_var:
            self.total_var.set(f"¥{self.total_amount:.2f}")
        
    def create_cart_item_widget(self, item):
        """创建购物车项目组件"""
        item_frame = tk.Frame(self.cart_listbox_frame, bg="#ffffff", relief="solid", bd=1)
        item_frame.pack(fill="x", padx=5, pady=2)
        
        # 菜品名称
        name_label = tk.Label(item_frame, text=item["name"], font=("微软雅黑", 10, "bold"),
                            bg="#ffffff", fg="#2c3e50")
        name_label.pack(anchor="w", padx=8, pady=(5, 0))
        
        # 价格和数量控制
        control_frame = tk.Frame(item_frame, bg="#ffffff")
        control_frame.pack(fill="x", padx=8, pady=(2, 5))
        
        # 单价
        price_label = tk.Label(control_frame, text=f"¥{item['price']:.2f}", 
                             font=("微软雅黑", 9), bg="#ffffff", fg="#7f8c8d")
        price_label.pack(side="left")
        
        # 数量控制
        qty_frame = tk.Frame(control_frame, bg="#ffffff")
        qty_frame.pack(side="right")
        
        # 减少按钮
        dec_btn = tk.Button(qty_frame, text="−", font=("微软雅黑", 10), width=2,
                          bg="#e74c3c", fg="white", relief="flat",
                          command=lambda: self.update_quantity(item["name"], item["quantity"] - 1))
        dec_btn.pack(side="left")
        
        # 数量显示
        qty_label = tk.Label(qty_frame, text=str(item["quantity"]), font=("微软雅黑", 10),
                           bg="#ffffff", fg="#2c3e50", width=3)
        qty_label.pack(side="left")
        
        # 增加按钮
        inc_btn = tk.Button(qty_frame, text="＋", font=("微软雅黑", 10), width=2,
                          bg="#27ae60", fg="white", relief="flat",
                          command=lambda: self.update_quantity(item["name"], item["quantity"] + 1))
        inc_btn.pack(side="left")
        
        # 小计
        subtotal_label = tk.Label(item_frame, text=f"小计: ¥{item['subtotal']:.2f}", 
                                font=("微软雅黑", 9), bg="#ffffff", fg="#e74c3c")
        subtotal_label.pack(anchor="e", padx=8, pady=(0, 5))
        
    def clear_cart(self):
        """清空购物车"""
        if not self.cart_items:
            if self.parent_frame:
                messagebox.showinfo("提示", "购物车已经是空的")
            return
        
        if not self.parent_frame or messagebox.askyesno("确认", "确定要清空购物车吗？"):
            self.cart_items.clear()
            self.update_cart_display()
            if self.status_label:
                self.status_label.config(text="🗑️ 购物车已清空", fg="#e74c3c")
    
    def get_next_order_id(self):
        """获取下一个订单号"""
        if self.order_module and hasattr(self.order_module, 'order_data') and self.order_module.order_data:
            return max([order["id"] for order in self.order_module.order_data]) + 1
        return 1001
    
    def checkout(self):
        """结算"""
        if not self.cart_items:
            if self.parent_frame:
                messagebox.showwarning("提示", "购物车为空，无法结算")
            return
        
        # 先生成订单号，用于创建客户名
        new_order_id = self.get_next_order_id()
          # 获取桌号信息
        if hasattr(self, '_test_table_number'):
            table_number = self._test_table_number
        else:
            table_number = self.table_var.get().strip() if self.table_var else "A01"
        
        if self.parent_frame:  # 有UI时进行桌号验证
            if not table_number:
                messagebox.showwarning("提示", "请输入桌号")
                return
        
        # 堂食客户名统一格式：堂食+订单号
        customer_name = f"堂食{new_order_id}"
          # 创建订单
        try:
            order_summary = []
            total_amount = 0.0  # 重新计算总金额
            
            for item in self.cart_items:
                # 检查最终库存
                if self.inventory_module:
                    can_order, message = self.inventory_module.check_ingredients_availability(
                        item["name"], item["quantity"])
                    if not can_order:
                        if self.parent_frame:
                            messagebox.showerror("库存不足", 
                                               f"结算失败，{item['name']} 库存不足:\n{message}")
                        return
                
                order_summary.append(f"{item['name']} x{item['quantity']}")
                total_amount += item["subtotal"]  # 累加小计            # 生成订单
            if self.order_module:
                # 自动创建或获取堂食客户信息
                if hasattr(self.order_module, 'auto_create_dine_in_customer'):
                    customer_id = self.order_module.auto_create_dine_in_customer(customer_name, table_number)
                
                # 创建统一格式的订单数据
                new_order = {
                    "id": new_order_id,
                    "customer": f"{customer_name} (桌号:{table_number})",
                    "items": " | ".join(order_summary),
                    "quantity": sum(item["quantity"] for item in self.cart_items),
                    "total": total_amount,  # 使用重新计算的总金额
                    "status": "进行中",
                    "date": datetime.datetime.now().strftime("%Y-%m-%d"),
                    "type": "堂食",
                    "table": table_number,
                    "notes": "堂食订单"
                }
                
                # 添加订单到订单管理模块
                self.order_module.order_data.append(new_order)
                
                # 保存订单数据
                if hasattr(self.order_module, 'save_data'):
                    self.order_module.save_data()
                
                # 自动扣减库存（通过订单模块处理）
                if self.inventory_module:
                    for item in self.cart_items:
                        success = self.inventory_module.consume_ingredients(item["name"], item["quantity"])
                        if not success:
                            if self.parent_frame:
                                messagebox.showwarning("警告", f"订单已创建，但扣减 {item['name']} 库存时出现异常")
            
            # 清空购物车
            self.cart_items.clear()
            self.update_cart_display()
            
            # 重置客户信息
            if self.table_var:
                self.table_var.set("A01")
              # 显示成功信息
            success_msg = f"订单创建成功！\n订单号: {new_order_id}\n客户: {customer_name}\n桌号: {table_number}\n总金额: ¥{total_amount:.2f}"
            if self.parent_frame:
                messagebox.showinfo("结算成功", success_msg)
            
            if self.status_label:
                self.status_label.config(text=f"✅ 订单 {new_order_id} 创建成功", fg="#27ae60")
                
        except Exception as e:
            error_msg = f"结算失败: {str(e)}"
            if self.parent_frame:
                messagebox.showerror("错误", error_msg)
            if self.status_label:
                self.status_label.config(text="❌ 结算失败", fg="#e74c3c")
    
    # 测试接口方法
    def test_add_item(self, meal_name, quantity=1):
        """测试用：添加菜品到购物车"""
        if not self.meal_module:
            return False
            
        # 查找菜品
        meal = None
        for m in self.meal_module.meal_data:
            if m["name"] == meal_name:
                meal = m
                break
        
        if not meal:
            return False
          # 添加到购物车
        for _ in range(quantity):
            self.add_to_cart(meal)
        
        return True
    
    def test_checkout(self, table_number="A01"):
        """测试用：结算购物车"""
        # 在测试环境中，直接传递桌号参数
        if not self.parent_frame:  # 无UI环境
            self._test_table_number = table_number
        elif self.table_var:
            self.table_var.set(table_number)
        
        self.checkout()
        return len(self.cart_items) == 0  # 成功结算后购物车应该为空
    
    def get_cart_summary(self):
        """获取购物车摘要"""
        return {
            "items": self.cart_items.copy(),
            "total": self.total_amount,
            "count": len(self.cart_items)
        }
