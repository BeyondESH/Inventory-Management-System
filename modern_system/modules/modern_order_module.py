#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
现代化订单管理模块
基于现代化外卖平台风格的订单管理界面
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from typing import Dict, List, Any, Optional
import datetime
import json
import os

# 导入数据管理中心
try:
    from .data_manager import data_manager
except ImportError:
    try:
        from data_manager import data_manager
    except ImportError:
        # 如果导入失败，创建一个简单的模拟数据管理器
        class MockDataManager:
            def register_module(self, module_type, instance):
                pass
            def get_orders(self, status_filter=None):
                return []
            def update_order_status(self, order_id, new_status):
                return True
            def add_order(self, order_data):
                return "MOCK_ORDER_ID"
        data_manager = MockDataManager()

class ModernOrderModule:
    def __init__(self, parent_frame, title_frame, inventory_module=None, customer_module=None):
        self.parent_frame = parent_frame
        self.title_frame = title_frame
        self.inventory_module = inventory_module
        self.customer_module = customer_module
        
        # 注册到数据管理中心
        data_manager.register_module('order', self)
        
        # 现代化配色方案
        self.colors = {
            'primary': '#FF6B35',        # 主橙色
            'primary_dark': '#E5522A',   # 深橙色
            'secondary': '#4ECDC4',      # 青绿色
            'success': '#2ECC71',        # 成功绿
            'warning': '#F39C12',        # 警告橙
            'danger': '#E74C3C',         # 危险红
            'info': '#3498DB',           # 信息蓝
            'light': '#ECF0F1',          # 浅灰
            'dark': '#2C3E50',           # 深蓝灰
            'white': '#FFFFFF',          # 白色
            'background': '#F8F9FA',     # 背景色
            'card': '#FFFFFF',           # 卡片背景
            'border': '#E1E8ED',         # 边框色
            'text': '#2C3E50',           # 文本色
            'text_light': '#7F8C8D',     # 浅文本色
            'shadow': '#BDC3C7'          # 阴影色
        }
        
        # 订单状态配色
        self.status_colors = {
            '待接单': '#F39C12',
            '已接单': '#3498DB',
            '制作中': '#9B59B6',
            '配送中': '#E67E22',
            '已完成': '#2ECC71',
            '已取消': '#E74C3C'
        }
          # 订单数据 - 从数据管理中心获取
        self.order_data = self.load_order_data()
        
        self.selected_order = None
        self.current_filter = "全部"
        self.search_keyword = ""
    
    def load_order_data(self):
        """从数据管理中心加载订单数据"""
        try:
            orders = data_manager.get_orders()
            # 转换数据格式以适配现有界面
            formatted_orders = []
            for order in orders:
                formatted_order = {
                    "id": order.get('id', ''),
                    "customer": order.get('customer_name', '未知客户'),
                    "phone": order.get('customer_phone', ''),
                    "address": order.get('delivery_address', '堂食'),
                    "meals": order.get('items', []),
                    "total": order.get('total_amount', 0),
                    "create_time": order.get('create_time', ''),
                    "status": order.get('status', '待处理'),
                    "type": order.get('order_type', '外卖'),
                    "payment": order.get('payment_method', '现金'),
                    "note": order.get('note', '')
                }
                formatted_orders.append(formatted_order)
            return formatted_orders
        except Exception as e:
            print(f"加载订单数据失败: {e}")
            return self.get_default_order_data()
    
    def get_default_order_data(self):
        """获取默认订单数据"""
        return [
            {
                "id": 1001, 
                "customer": "张三", 
                "phone": "138****1234",
                "address": "北京市朝阳区xxx街道1号",
                "meals": [
                    {"name": "番茄牛肉面", "price": 25.0, "quantity": 2},
                    {"name": "可乐", "price": 5.0, "quantity": 1}
                ],
                "total": 55.0, 
                "create_time": "2024-06-15 12:30", 
                "status": "已完成", 
                "type": "外卖",
                "payment": "微信支付",
                "note": "少放辣椒"
            },
            {
                "id": 1002, 
                "customer": "李四", 
                "phone": "139****5678",
                "address": "北京市海淀区xxx路88号",
                "meals": [
                    {"name": "鸡蛋炒饭", "price": 18.0, "quantity": 1}
                ],
                "total": 18.0, 
                "create_time": "2024-06-15 12:45", 
                "status": "制作中", 
                "type": "外卖",
                "payment": "支付宝",
                "note": ""
            },
            {
                "id": 1003, 
                "customer": "王五", 
                "phone": "136****9012",
                "address": "北京市西城区xxx胡同66号",
                "meals": [
                    {"name": "牛肉汉堡", "price": 32.0, "quantity": 3},
                    {"name": "薯条", "price": 12.0, "quantity": 2}
                ],
                "total": 120.0, 
                "create_time": "2024-06-15 11:20", 
                "status": "待接单", 
                "type": "外卖",
                "payment": "现金",
                "note": "汉堡不要洋葱"
            },
            {
                "id": 1004, 
                "customer": "赵六", 
                "phone": "137****3456",
                "address": "堂食",
                "meals": [
                    {"name": "红烧肉", "price": 35.0, "quantity": 1},
                    {"name": "米饭", "price": 3.0, "quantity": 2}
                ],
                "total": 41.0, 
                "create_time": "2024-06-15 13:15", 
                "status": "配送中", 
                "type": "堂食",
                "payment": "微信支付",
                "note": ""            }
        ]
        
        self.selected_order = None
        self.current_filter = "全部"
        self.search_keyword = ""
    
    def create_status_card(self, parent, status, count, color):
        """创建状态统计卡片"""
        card_frame = tk.Frame(parent, bg=self.colors['card'], relief='flat', bd=1,
                             highlightbackground=self.colors['border'], highlightthickness=1)
        card_frame.pack(side='left', padx=10, pady=5, fill='both', expand=True)
        
        # 设置最小尺寸
        card_frame.configure(width=200, height=100)
        
        # 状态图标和数字
        icon_frame = tk.Frame(card_frame, bg=color, width=80, height=80)
        icon_frame.pack(side='left', padx=15, pady=10)
        icon_frame.pack_propagate(False)
        
        count_label = tk.Label(icon_frame, text=str(count), font=('Microsoft YaHei UI', 18, 'bold'),
                              bg=color, fg=self.colors['white'])
        count_label.pack(expand=True)
        
        # 状态信息
        info_frame = tk.Frame(card_frame, bg=self.colors['card'])
        info_frame.pack(side='left', padx=(0, 15), pady=15, fill='both', expand=True)
        
        status_label = tk.Label(info_frame, text=status, font=('Microsoft YaHei UI', 12, 'bold'),
                               bg=self.colors['card'], fg=self.colors['text'])
        status_label.pack(anchor='w', pady=(5, 0))
        
        desc_label = tk.Label(info_frame, text='订单数量', font=('Microsoft YaHei UI', 10),
                             bg=self.colors['card'], fg=self.colors['text_light'])
        desc_label.pack(anchor='w', pady=(0, 5))
        
        return card_frame
    
    def create_order_card(self, parent, order):
        """创建订单卡片"""
        card_frame = tk.Frame(parent, bg=self.colors['card'], relief='flat', bd=1,
                             highlightbackground=self.colors['border'], highlightthickness=1)
        card_frame.pack(fill='x', padx=5, pady=5)
        
        # 卡片头部
        header_frame = tk.Frame(card_frame, bg=self.colors['card'], height=50)
        header_frame.pack(fill='x', padx=15, pady=(15, 10))
        header_frame.pack_propagate(False)
        
        # 订单号和状态
        order_info_frame = tk.Frame(header_frame, bg=self.colors['card'])
        order_info_frame.pack(side='left', fill='y')
        
        order_id_label = tk.Label(order_info_frame, text=f"#{order['id']}", 
                                 font=('Microsoft YaHei UI', 14, 'bold'),
                                 bg=self.colors['card'], fg=self.colors['primary'])
        order_id_label.pack(anchor='w')
        
        time_label = tk.Label(order_info_frame, text=order['create_time'], 
                             font=('Microsoft YaHei UI', 10),
                             bg=self.colors['card'], fg=self.colors['text_light'])
        time_label.pack(anchor='w')
        
        # 状态标签
        status_color = self.status_colors.get(order['status'], self.colors['info'])
        status_frame = tk.Frame(header_frame, bg=status_color, padx=10, pady=5)
        status_frame.pack(side='right', pady=5)
        
        status_label = tk.Label(status_frame, text=order['status'], 
                               font=('Microsoft YaHei UI', 10, 'bold'),
                               bg=status_color, fg=self.colors['white'])
        status_label.pack()
        
        # 客户信息
        customer_frame = tk.Frame(card_frame, bg=self.colors['card'])
        customer_frame.pack(fill='x', padx=15, pady=5)
        
        customer_label = tk.Label(customer_frame, text=f"👤 {order['customer']} | 📞 {order['phone']}", 
                                 font=('Microsoft YaHei UI', 11),
                                 bg=self.colors['card'], fg=self.colors['text'])
        customer_label.pack(anchor='w')
        
        address_label = tk.Label(customer_frame, text=f"📍 {order['address']}", 
                                font=('Microsoft YaHei UI', 10),
                                bg=self.colors['card'], fg=self.colors['text_light'])
        address_label.pack(anchor='w')
        
        # 菜品信息
        meals_frame = tk.Frame(card_frame, bg=self.colors['background'], padx=10, pady=8)
        meals_frame.pack(fill='x', padx=15, pady=5)
        
        for meal in order['meals']:
            meal_item = tk.Label(meals_frame, 
                               text=f"🍽️ {meal['name']} × {meal['quantity']} = ¥{meal['price'] * meal['quantity']:.2f}", 
                               font=('Microsoft YaHei UI', 10),
                               bg=self.colors['background'], fg=self.colors['text'],
                               anchor='w')
            meal_item.pack(fill='x', pady=2)
        
        # 订单总额和操作按钮
        bottom_frame = tk.Frame(card_frame, bg=self.colors['card'])
        bottom_frame.pack(fill='x', padx=15, pady=(5, 15))
        
        # 总额
        total_label = tk.Label(bottom_frame, text=f"总计：¥{order['total']:.2f}", 
                              font=('Microsoft YaHei UI', 12, 'bold'),
                              bg=self.colors['card'], fg=self.colors['primary'])
        total_label.pack(side='left')
        
        # 支付方式和类型
        payment_label = tk.Label(bottom_frame, text=f"{order['payment']} | {order['type']}", 
                               font=('Microsoft YaHei UI', 9),
                               bg=self.colors['card'], fg=self.colors['text_light'])
        payment_label.pack(side='left', padx=(20, 0))
        
        # 操作按钮
        actions_frame = tk.Frame(bottom_frame, bg=self.colors['card'])
        actions_frame.pack(side='right')
        
        # 查看详情按钮
        detail_btn = tk.Button(actions_frame, text="查看详情", 
                              font=('Microsoft YaHei UI', 9),
                              bg=self.colors['info'], fg=self.colors['white'],
                              bd=0, padx=15, pady=5, cursor='hand2',
                              command=lambda: self.show_order_detail(order))
        detail_btn.pack(side='right', padx=5)
        
        # 状态操作按钮
        if order['status'] == '待接单':
            accept_btn = tk.Button(actions_frame, text="接单", 
                                  font=('Microsoft YaHei UI', 9),
                                  bg=self.colors['success'], fg=self.colors['white'],
                                  bd=0, padx=15, pady=5, cursor='hand2',
                                  command=lambda: self.update_order_status(order['id'], '已接单'))
            accept_btn.pack(side='right', padx=5)
        elif order['status'] == '已接单':
            start_btn = tk.Button(actions_frame, text="开始制作", 
                                 font=('Microsoft YaHei UI', 9),
                                 bg=self.colors['warning'], fg=self.colors['white'],
                                 bd=0, padx=15, pady=5, cursor='hand2',
                                 command=lambda: self.update_order_status(order['id'], '制作中'))
            start_btn.pack(side='right', padx=5)
        elif order['status'] == '制作中':
            finish_btn = tk.Button(actions_frame, text="完成制作", 
                                  font=('Microsoft YaHei UI', 9),
                                  bg=self.colors['primary'], fg=self.colors['white'],
                                  bd=0, padx=15, pady=5, cursor='hand2',
                                  command=lambda: self.update_order_status(order['id'], '配送中' if order['type'] == '外卖' else '已完成'))
            finish_btn.pack(side='right', padx=5)
        elif order['status'] == '配送中':
            complete_btn = tk.Button(actions_frame, text="完成配送", 
                                    font=('Microsoft YaHei UI', 9),
                                    bg=self.colors['success'], fg=self.colors['white'],
                                    bd=0, padx=15, pady=5, cursor='hand2',
                                    command=lambda: self.update_order_status(order['id'], '已完成'))
            complete_btn.pack(side='right', padx=5)
        
        # 备注信息
        if order['note']:
            note_frame = tk.Frame(card_frame, bg=self.colors['light'], padx=10, pady=5)
            note_frame.pack(fill='x', padx=15, pady=(0, 15))
            
            note_label = tk.Label(note_frame, text=f"📝 备注：{order['note']}", 
                                 font=('Microsoft YaHei UI', 9),
                                 bg=self.colors['light'], fg=self.colors['text'])
            note_label.pack(anchor='w')
        
        return card_frame
    
    def update_order_status(self, order_id, new_status):
        """更新订单状态"""
        for order in self.order_data:
            if order['id'] == order_id:
                order['status'] = new_status
                messagebox.showinfo("成功", f"订单 #{order_id} 状态已更新为：{new_status}")
                self.refresh_order_list()
                break
    
    def show_order_detail(self, order):
        """显示订单详情"""
        detail_window = tk.Toplevel()
        detail_window.title(f"订单详情 - #{order['id']}")
        detail_window.geometry("500x600")
        detail_window.configure(bg=self.colors['background'])
        detail_window.resizable(False, False)
        
        # 标题
        title_frame = tk.Frame(detail_window, bg=self.colors['primary'], height=60)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text=f"订单详情 #{order['id']}", 
                              font=('Microsoft YaHei UI', 16, 'bold'),
                              bg=self.colors['primary'], fg=self.colors['white'])
        title_label.pack(expand=True)
        
        # 详情内容
        content_frame = tk.Frame(detail_window, bg=self.colors['background'])
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # 基本信息
        info_frame = tk.Frame(content_frame, bg=self.colors['card'], padx=20, pady=15)
        info_frame.pack(fill='x', pady=(0, 10))
        
        tk.Label(info_frame, text="基本信息", font=('Microsoft YaHei UI', 12, 'bold'),
                bg=self.colors['card'], fg=self.colors['text']).pack(anchor='w')
        
        info_text = f"""订单号：#{order['id']}
客户姓名：{order['customer']}
联系电话：{order['phone']}
配送地址：{order['address']}
订单类型：{order['type']}
支付方式：{order['payment']}
下单时间：{order['create_time']}
订单状态：{order['status']}"""
        
        tk.Label(info_frame, text=info_text, font=('Microsoft YaHei UI', 10),
                bg=self.colors['card'], fg=self.colors['text'], justify='left').pack(anchor='w', pady=(10, 0))
        
        # 菜品信息
        meals_frame = tk.Frame(content_frame, bg=self.colors['card'], padx=20, pady=15)
        meals_frame.pack(fill='x', pady=(0, 10))
        
        tk.Label(meals_frame, text="菜品信息", font=('Microsoft YaHei UI', 12, 'bold'),
                bg=self.colors['card'], fg=self.colors['text']).pack(anchor='w')
        
        for meal in order['meals']:
            meal_frame = tk.Frame(meals_frame, bg=self.colors['background'], padx=10, pady=5)
            meal_frame.pack(fill='x', pady=5)
            
            tk.Label(meal_frame, text=meal['name'], font=('Microsoft YaHei UI', 10, 'bold'),
                    bg=self.colors['background'], fg=self.colors['text']).pack(side='left')
            
            tk.Label(meal_frame, text=f"¥{meal['price']:.2f} × {meal['quantity']} = ¥{meal['price'] * meal['quantity']:.2f}", 
                    font=('Microsoft YaHei UI', 10),
                    bg=self.colors['background'], fg=self.colors['text']).pack(side='right')
        
        # 总计
        total_frame = tk.Frame(meals_frame, bg=self.colors['primary'], padx=10, pady=8)
        total_frame.pack(fill='x', pady=(10, 0))
        
        tk.Label(total_frame, text=f"订单总计：¥{order['total']:.2f}", 
                font=('Microsoft YaHei UI', 12, 'bold'),
                bg=self.colors['primary'], fg=self.colors['white']).pack()
        
        # 备注信息
        if order['note']:
            note_frame = tk.Frame(content_frame, bg=self.colors['card'], padx=20, pady=15)
            note_frame.pack(fill='x', pady=(0, 10))
            
            tk.Label(note_frame, text="备注信息", font=('Microsoft YaHei UI', 12, 'bold'),
                    bg=self.colors['card'], fg=self.colors['text']).pack(anchor='w')
            
            tk.Label(note_frame, text=order['note'], font=('Microsoft YaHei UI', 10),
                    bg=self.colors['card'], fg=self.colors['text'], wraplength=400).pack(anchor='w', pady=(10, 0))
        
        # 关闭按钮
        tk.Button(content_frame, text="关闭", font=('Microsoft YaHei UI', 10),
                 bg=self.colors['text_light'], fg=self.colors['white'],
                 bd=0, padx=30, pady=8, cursor='hand2',
                 command=detail_window.destroy).pack(pady=20)
    
    def filter_orders(self, status):
        """筛选订单"""
        self.current_filter = status
        self.refresh_order_list()
    
    def refresh_order_list(self):
        """刷新订单列表"""
        # 清空列表
        for widget in self.orders_container.winfo_children():
            widget.destroy()
        
        # 从数据管理中心获取订单数据
        try:
            all_orders = data_manager.get_orders()
            self.order_data = all_orders
        except:
            # 如果获取失败，使用默认数据
            pass
        
        # 筛选和搜索订单
        filtered_orders = self.order_data
        
        # 应用状态筛选
        if self.current_filter != "全部":
            filtered_orders = [order for order in self.order_data if order['status'] == self.current_filter]
        
        # 应用搜索
        if self.search_keyword:
            filtered_orders = [order for order in filtered_orders 
                              if self.search_keyword in order['customer_name'].lower() 
                              or self.search_keyword in str(order['id'])
                              or self.search_keyword in order['table_number'].lower()]
        
        # 创建订单卡片
        for order in filtered_orders:
            self.create_order_card(self.orders_container, order)
        
        # 更新统计信息
        self.update_statistics()
    
    def refresh_data(self):
        """刷新数据（由数据管理中心调用）"""
        if hasattr(self, 'orders_container'):
            self.refresh_order_list()
    
    def update_statistics(self):
        """更新统计信息"""
        # 清空统计卡片
        for widget in self.stats_frame.winfo_children():
            widget.destroy()
        
        # 统计各状态订单数量
        status_counts = {}
        for status in self.status_colors.keys():
            status_counts[status] = len([order for order in self.order_data if order['status'] == status])
        
        # 创建统计卡片 - 显示所有状态，包括数量为0的
        for status, count in status_counts.items():
            color = self.status_colors[status]
            self.create_status_card(self.stats_frame, status, count, color)
    
    def add_new_order(self):
        """添加新订单"""
        # 创建新订单窗口
        order_window = tk.Toplevel()
        order_window.title("新建订单")
        order_window.geometry("600x700")
        order_window.configure(bg=self.colors['background'])
        order_window.resizable(False, False)
        
        # 标题
        title_frame = tk.Frame(order_window, bg=self.colors['primary'], height=60)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text="新建订单", 
                              font=('Microsoft YaHei UI', 16, 'bold'),
                              bg=self.colors['primary'], fg=self.colors['white'])
        title_label.pack(expand=True)
        
        # 表单内容
        form_frame = tk.Frame(order_window, bg=self.colors['background'])
        form_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # 客户信息
        customer_frame = tk.Frame(form_frame, bg=self.colors['card'], padx=20, pady=15)
        customer_frame.pack(fill='x', pady=(0, 10))
        
        tk.Label(customer_frame, text="客户信息", font=('Microsoft YaHei UI', 12, 'bold'),
                bg=self.colors['card'], fg=self.colors['text']).pack(anchor='w')
        
        # 客户姓名
        name_frame = tk.Frame(customer_frame, bg=self.colors['card'])
        name_frame.pack(fill='x', pady=5)
        tk.Label(name_frame, text="客户姓名:", font=('Microsoft YaHei UI', 10),
                bg=self.colors['card'], fg=self.colors['text']).pack(side='left')
        customer_name_var = tk.StringVar()
        name_entry = tk.Entry(name_frame, textvariable=customer_name_var, font=('Microsoft YaHei UI', 10))
        name_entry.pack(side='right', fill='x', expand=True, padx=(10, 0))
        
        # 联系电话
        phone_frame = tk.Frame(customer_frame, bg=self.colors['card'])
        phone_frame.pack(fill='x', pady=5)
        tk.Label(phone_frame, text="联系电话:", font=('Microsoft YaHei UI', 10),
                bg=self.colors['card'], fg=self.colors['text']).pack(side='left')
        customer_phone_var = tk.StringVar()
        phone_entry = tk.Entry(phone_frame, textvariable=customer_phone_var, font=('Microsoft YaHei UI', 10))
        phone_entry.pack(side='right', fill='x', expand=True, padx=(10, 0))
        
        # 配送地址
        address_frame = tk.Frame(customer_frame, bg=self.colors['card'])
        address_frame.pack(fill='x', pady=5)
        tk.Label(address_frame, text="配送地址:", font=('Microsoft YaHei UI', 10),
                bg=self.colors['card'], fg=self.colors['text']).pack(side='left')
        customer_address_var = tk.StringVar()
        address_entry = tk.Entry(address_frame, textvariable=customer_address_var, font=('Microsoft YaHei UI', 10))
        address_entry.pack(side='right', fill='x', expand=True, padx=(10, 0))
        
        # 订单类型
        type_frame = tk.Frame(customer_frame, bg=self.colors['card'])
        type_frame.pack(fill='x', pady=5)
        tk.Label(type_frame, text="订单类型:", font=('Microsoft YaHei UI', 10),
                bg=self.colors['card'], fg=self.colors['text']).pack(side='left')
        order_type_var = tk.StringVar(value="外卖")
        type_combo = ttk.Combobox(type_frame, textvariable=order_type_var, 
                                 values=["外卖", "堂食"], state="readonly")
        type_combo.pack(side='right', padx=(10, 0))
        
        # 支付方式
        payment_frame = tk.Frame(customer_frame, bg=self.colors['card'])
        payment_frame.pack(fill='x', pady=5)
        tk.Label(payment_frame, text="支付方式:", font=('Microsoft YaHei UI', 10),
                bg=self.colors['card'], fg=self.colors['text']).pack(side='left')
        payment_var = tk.StringVar(value="微信支付")
        payment_combo = ttk.Combobox(payment_frame, textvariable=payment_var, 
                                    values=["微信支付", "支付宝", "现金", "银行卡"], state="readonly")
        payment_combo.pack(side='right', padx=(10, 0))
        
        # 备注
        note_frame = tk.Frame(customer_frame, bg=self.colors['card'])
        note_frame.pack(fill='x', pady=5)
        tk.Label(note_frame, text="订单备注:", font=('Microsoft YaHei UI', 10),
                bg=self.colors['card'], fg=self.colors['text']).pack(anchor='w')
        note_var = tk.StringVar()
        note_entry = tk.Entry(note_frame, textvariable=note_var, font=('Microsoft YaHei UI', 10))
        note_entry.pack(fill='x', pady=(5, 0))
        
        # 菜品选择
        meals_frame = tk.Frame(form_frame, bg=self.colors['card'], padx=20, pady=15)
        meals_frame.pack(fill='both', expand=True, pady=(0, 10))
        
        tk.Label(meals_frame, text="菜品选择", font=('Microsoft YaHei UI', 12, 'bold'),
                bg=self.colors['card'], fg=self.colors['text']).pack(anchor='w')
        
        # 简化的菜品选择（实际应该从菜品模块获取）
        sample_meals = [
            {"name": "番茄牛肉面", "price": 25.0},
            {"name": "鸡蛋炒饭", "price": 18.0},
            {"name": "牛肉汉堡", "price": 32.0},
            {"name": "红烧肉", "price": 35.0},
            {"name": "可乐", "price": 5.0},
            {"name": "米饭", "price": 3.0}
        ]
        
        selected_meals = []
        meal_vars = {}
        
        for meal in sample_meals:
            meal_frame = tk.Frame(meals_frame, bg=self.colors['background'], padx=10, pady=5)
            meal_frame.pack(fill='x', pady=2)
            
            var = tk.IntVar()
            meal_vars[meal['name']] = var
            
            cb = tk.Checkbutton(meal_frame, text=f"{meal['name']} - ¥{meal['price']:.2f}",
                               variable=var, font=('Microsoft YaHei UI', 10),
                               bg=self.colors['background'], fg=self.colors['text'])
            cb.pack(side='left')
            
            # 数量选择
            qty_var = tk.IntVar(value=1)
            meal_vars[f"{meal['name']}_qty"] = qty_var
            
            tk.Label(meal_frame, text="数量:", font=('Microsoft YaHei UI', 9),
                    bg=self.colors['background'], fg=self.colors['text']).pack(side='right', padx=(0, 5))
            
            qty_spinbox = tk.Spinbox(meal_frame, from_=1, to=10, width=5, textvariable=qty_var)
            qty_spinbox.pack(side='right')
        
        # 按钮
        button_frame = tk.Frame(form_frame, bg=self.colors['background'])
        button_frame.pack(fill='x', pady=10)
        
        def save_order():
            # 验证输入
            if not customer_name_var.get() or not customer_phone_var.get():
                messagebox.showerror("错误", "请填写客户姓名和联系电话")
                return
            
            # 收集选中的菜品
            order_meals = []
            total_amount = 0
            
            for meal in sample_meals:
                if meal_vars[meal['name']].get():
                    quantity = meal_vars[f"{meal['name']}_qty"].get()
                    order_meals.append({
                        "name": meal['name'],
                        "price": meal['price'],
                        "quantity": quantity
                    })
                    total_amount += meal['price'] * quantity
            
            if not order_meals:
                messagebox.showerror("错误", "请至少选择一个菜品")
                return
            
            # 生成新订单ID
            new_id = max([order['id'] for order in self.order_data]) + 1
            
            # 创建新订单
            new_order = {
                "id": new_id,
                "customer": customer_name_var.get(),
                "phone": customer_phone_var.get(),
                "address": customer_address_var.get() if customer_address_var.get() else "堂食",
                "meals": order_meals,
                "total": total_amount,
                "create_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                "status": "待接单",
                "type": order_type_var.get(),
                "payment": payment_var.get(),
                "note": note_var.get()
            }
            
            self.order_data.append(new_order)
            messagebox.showinfo("成功", f"订单 #{new_id} 创建成功！")
            order_window.destroy()
            self.refresh_order_list()
        
        save_btn = tk.Button(button_frame, text="保存订单", 
                           font=('Microsoft YaHei UI', 10, 'bold'),
                           bg=self.colors['primary'], fg=self.colors['white'],
                           bd=0, padx=30, pady=8, cursor='hand2',
                           command=save_order)
        save_btn.pack(side='right', padx=5)
        
        cancel_btn = tk.Button(button_frame, text="取消", 
                             font=('Microsoft YaHei UI', 10),
                             bg=self.colors['text_light'], fg=self.colors['white'],
                             bd=0, padx=30, pady=8, cursor='hand2',
                             command=order_window.destroy)
        cancel_btn.pack(side='right', padx=5)
    
    def on_data_changed(self, event_type, data):
        """处理数据变更通知"""
        if event_type in ['order_added', 'order_updated']:
            # 刷新订单数据
            self.order_data = self.load_order_data()
            # 如果当前正在显示订单界面，刷新显示
            if hasattr(self, 'order_list_frame'):
                self.refresh_order_list()
    
    def refresh_order_list(self):
        """刷新订单列表显示"""
        if hasattr(self, 'order_list_frame') and self.order_list_frame.winfo_exists():
            self.update_order_list()
            self.update_status_cards()
    
    def show(self):
        """显示订单管理界面"""
        # 清空父框架
        for widget in self.parent_frame.winfo_children():
            widget.destroy()
        for widget in self.title_frame.winfo_children():
            widget.destroy()
        
        # 设置父框架背景
        self.parent_frame.configure(bg=self.colors['background'])
        
        # 标题栏
        title_container = tk.Frame(self.title_frame, bg=self.colors['white'])
        title_container.pack(fill='x')
        
        # 标题
        title_label = tk.Label(title_container, text="📋 订单管理", 
                              font=('Microsoft YaHei UI', 18, 'bold'),
                              bg=self.colors['white'], fg=self.colors['text'])
        title_label.pack(side='left', padx=20, pady=15)
        
        # 操作按钮
        actions_frame = tk.Frame(title_container, bg=self.colors['white'])
        actions_frame.pack(side='right', padx=20, pady=15)
        
        # 新建订单按钮
        add_btn = tk.Button(actions_frame, text="➕ 新建订单", 
                           font=('Microsoft YaHei UI', 10, 'bold'),
                           bg=self.colors['primary'], fg=self.colors['white'],
                           bd=0, padx=20, pady=8, cursor='hand2',
                           command=self.add_new_order)
        add_btn.pack(side='right', padx=5)
        
        # 刷新按钮
        refresh_btn = tk.Button(actions_frame, text="🔄 刷新", 
                               font=('Microsoft YaHei UI', 10),
                               bg=self.colors['info'], fg=self.colors['white'],
                               bd=0, padx=20, pady=8, cursor='hand2',
                               command=self.refresh_order_list)
        refresh_btn.pack(side='right', padx=5)
        
        # 主内容区域
        main_frame = tk.Frame(self.parent_frame, bg=self.colors['background'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # 统计卡片区域
        self.stats_frame = tk.Frame(main_frame, bg=self.colors['background'])
        self.stats_frame.pack(fill='x', pady=(0, 20))
        
        # 筛选按钮区域
        filter_frame = tk.Frame(main_frame, bg=self.colors['background'])
        filter_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(filter_frame, text="筛选订单：", font=('Microsoft YaHei UI', 12, 'bold'),
                bg=self.colors['background'], fg=self.colors['text']).pack(side='left')
        
        filter_buttons = ["全部", "待接单", "已接单", "制作中", "配送中", "已完成", "已取消"]
        for filter_name in filter_buttons:
            btn_color = self.colors['primary'] if filter_name == self.current_filter else self.colors['light']
            text_color = self.colors['white'] if filter_name == self.current_filter else self.colors['text']
            
            filter_btn = tk.Button(filter_frame, text=filter_name, 
                                  font=('Microsoft YaHei UI', 9),
                                  bg=btn_color, fg=text_color,
                                  bd=0, padx=15, pady=5, cursor='hand2',
                                  command=lambda f=filter_name: self.filter_orders(f))
            filter_btn.pack(side='left', padx=5)
        
        # 订单列表容器
        list_frame = tk.Frame(main_frame, bg=self.colors['background'])
        list_frame.pack(fill='both', expand=True)
        
        # 滚动区域
        canvas = tk.Canvas(list_frame, bg=self.colors['background'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=canvas.yview)
        self.orders_container = tk.Frame(canvas, bg=self.colors['background'])
        
        self.orders_container.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.orders_container, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # 初始化显示
        self.refresh_order_list()
          # 绑定鼠标滚轮事件
        def on_mousewheel(event):
            try:
                if canvas.winfo_exists():
                    canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            except tk.TclError:
                pass  # Widget已被销毁，忽略错误
        
        canvas.bind("<MouseWheel>", on_mousewheel)
        self.orders_container.bind("<MouseWheel>", on_mousewheel)
