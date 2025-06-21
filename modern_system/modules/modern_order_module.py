#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modern Order Management Module
Based on modern takeout platform style order management interface
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from typing import Dict, List, Any, Optional
import datetime
import json
import os

# Import data management center
try:
    from .data_manager import data_manager
except ImportError:
    try:
        from data_manager import data_manager
    except ImportError:
        # If import fails, create a simple mock data manager
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
        
        # Register to data management center
        data_manager.register_module('order', self)
        
        # Modern color scheme
        self.colors = {
            'primary': '#FF6B35',        # Primary orange
            'primary_dark': '#E5522A',   # Dark orange
            'secondary': '#4ECDC4',      # Teal
            'success': '#2ECC71',        # Success green
            'warning': '#F39C12',        # Warning orange
            'danger': '#E74C3C',         # Danger red
            'info': '#3498DB',           # Info blue
            'light': '#ECF0F1',          # Light gray
            'dark': '#2C3E50',           # Dark blue gray
            'white': '#FFFFFF',          # White
            'background': '#F8F9FA',     # Background color
            'card': '#FFFFFF',           # Card background
            'border': '#E1E8ED',         # Border color
            'text': '#2C3E50',           # Text color
            'text_light': '#7F8C8D',     # Light text color
            'shadow': '#BDC3C7'          # Shadow color
        }
        
        # Order status color scheme
        self.status_colors = {
            'Pending': '#F39C12',
            'Accepted': '#3498DB',
            'Preparing': '#9B59B6',
            'Paused': '#7f8c8d',
            'Delivering': '#E67E22',
            'Ready for Pickup': '#16a085',
            'Completed': '#2ECC71',
            'Cancelled': '#E74C3C',
            'Archived': '#bdc3c7'
        }
        
        # Order data - get from data management center
        self.order_data = self.load_order_data()
        
        # Interface state variables
        self.selected_order = None
        self.current_filter = "All"
        self.search_keyword = ""
        self.stats_frame = None
        self.orders_container = None
    
    def load_order_data(self):
        """Load order data from data management center"""
        try:
            orders = data_manager.get_orders()
            # Convert data format to adapt to existing interface
            formatted_orders = []
            for order in orders:
                # Process meal data
                meals = []
                items = order.get('items', [])
                for item in items:
                    meal = {
                        "name": item.get('name', item.get('product_id', 'Unknown Dish')),
                        "price": item.get('price', 0),
                        "quantity": item.get('quantity', 1)
                    }
                    meals.append(meal)
                
                formatted_order = {
                    "id": order.get('id', ''),
                    "customer": order.get('customer_name', order.get('table_number', 'Unknown Customer')),
                    "phone": order.get('customer_phone', order.get('phone', '')),
                    "address": order.get('delivery_address', order.get('address', 'Dine-in')),
                    "meals": meals,
                    "total": order.get('total_amount', order.get('total', 0)),
                    "create_time": order.get('create_time', '').replace('T', ' ')[:16] if 'T' in order.get('create_time', '') else order.get('create_time', ''),
                    "status": order.get('status', 'Pending'),
                    "type": order.get('order_type', order.get('type', 'Takeout')),
                    "payment": order.get('payment_method', order.get('payment', 'Cash')),
                    "note": order.get('note', '')
                }
                formatted_orders.append(formatted_order)
            
            # If no data or too little data, use default sample data
            if len(formatted_orders) < 3:
                print("Order data is limited, adding sample data...")
                formatted_orders.extend(self.get_default_order_data())
            
            return formatted_orders
        except Exception as e:
            print(f"Failed to load order data: {e}")
            return self.get_default_order_data()
    
    def get_default_order_data(self):
        """Get default order data"""
        return [
            {
                "id": 1001, 
                "customer": "John Smith", 
                "phone": "138****1234",
                "address": "123 Main Street, Chaoyang District, Beijing",
                "meals": [
                    {"name": "Tomato Beef Noodles", "price": 25.0, "quantity": 2},
                    {"name": "Cola", "price": 5.0, "quantity": 1}
                ],
                "total": 55.0, 
                "create_time": "2024-06-15 12:30", 
                "status": "Completed", 
                "type": "Takeout",
                "payment": "WeChat Pay",
                "note": "Less spicy"
            },
            {
                "id": 1002, 
                "customer": "Jane Doe", 
                "phone": "139****5678",
                "address": "88 Business Road, Haidian District, Beijing",
                "meals": [
                    {"name": "Egg Fried Rice", "price": 18.0, "quantity": 1}
                ],
                "total": 18.0, 
                "create_time": "2024-06-15 12:45", 
                "status": "Preparing", 
                "type": "Takeout",
                "payment": "Alipay",
                "note": ""
            },
            {
                "id": 1003, 
                "customer": "Mike Johnson", 
                "phone": "136****9012",
                "address": "66 Old Alley, Xicheng District, Beijing",
                "meals": [
                    {"name": "Beef Burger", "price": 32.0, "quantity": 3},
                    {"name": "French Fries", "price": 12.0, "quantity": 2}
                ],
                "total": 120.0, 
                "create_time": "2024-06-15 11:20", 
                "status": "Pending", 
                "type": "Takeout",
                "payment": "Cash",
                "note": "No onions in burger"
            },
            {
                "id": 1004, 
                "customer": "Sarah Wilson", 
                "phone": "137****3456",
                "address": "Dine-in",
                "meals": [
                    {"name": "Braised Pork", "price": 35.0, "quantity": 1},
                    {"name": "Rice", "price": 3.0, "quantity": 2}
                ],
                "total": 41.0, 
                "create_time": "2024-06-15 13:15", 
                "status": "Delivering", 
                "type": "Dine-in",
                "payment": "WeChat Pay",
                "note": ""            }
        ]
        
        self.selected_order = None
        self.current_filter = "All"
        self.search_keyword = ""
    
    def create_status_card(self, parent, status, count, color):
        """Create status statistics card"""
        card_frame = tk.Frame(parent, bg=self.colors['card'], relief='flat', bd=1,
                             highlightbackground=self.colors['border'], highlightthickness=1)
        card_frame.pack(side='left', padx=10, pady=5, fill='both', expand=True)
        
        # Set minimum size
        card_frame.configure(width=200, height=100)
        
        # Status icon and number
        icon_frame = tk.Frame(card_frame, bg=color, width=80, height=80)
        icon_frame.pack(side='left', padx=15, pady=10)
        icon_frame.pack_propagate(False)
        
        count_label = tk.Label(icon_frame, text=str(count), font=('Microsoft YaHei UI', 18, 'bold'),
                              bg=color, fg=self.colors['white'])
        count_label.pack(expand=True)
        
        # Status information
        info_frame = tk.Frame(card_frame, bg=self.colors['card'])
        info_frame.pack(side='left', padx=(0, 15), pady=15, fill='both', expand=True)
        
        status_label = tk.Label(info_frame, text=status, font=('Microsoft YaHei UI', 12, 'bold'),
                               bg=self.colors['card'], fg=self.colors['text'])
        status_label.pack(anchor='w', pady=(5, 0))
        
        desc_label = tk.Label(info_frame, text='Order quantity', font=('Microsoft YaHei UI', 10),
                             bg=self.colors['card'], fg=self.colors['text_light'])
        desc_label.pack(anchor='w', pady=(0, 5))
        
        return card_frame
    
    def create_order_card(self, parent, order):
        """Create order card"""
        card_frame = tk.Frame(parent, bg=self.colors['card'], relief='flat', bd=1,
                             highlightbackground=self.colors['border'], highlightthickness=1)
        card_frame.pack(fill='x', padx=5, pady=5)
        
        # Card header
        header_frame = tk.Frame(card_frame, bg=self.colors['card'], height=50)
        header_frame.pack(fill='x', padx=15, pady=(15, 10))
        header_frame.pack_propagate(False)
        
        # Order number and status
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
        
        # Status label
        status_color = self.status_colors.get(order['status'], self.colors['info'])
        status_frame = tk.Frame(header_frame, bg=status_color, padx=10, pady=5)
        status_frame.pack(side='right', pady=5)
        
        status_label = tk.Label(status_frame, text=order['status'], 
                               font=('Microsoft YaHei UI', 10, 'bold'),
                               bg=status_color, fg=self.colors['white'])
        status_label.pack()
        
        # Customer information
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
        
        # Meal information
        meals_frame = tk.Frame(card_frame, bg=self.colors['background'], padx=10, pady=8)
        meals_frame.pack(fill='x', padx=15, pady=5)
        
        for meal in order['meals']:
            meal_item = tk.Label(meals_frame, 
                               text=f"🍽️ {meal['name']} × {meal['quantity']} = ¥{meal['price'] * meal['quantity']:.2f}", 
                               font=('Microsoft YaHei UI', 10),
                               bg=self.colors['background'], fg=self.colors['text'],
                               anchor='w')
            meal_item.pack(fill='x', pady=2)
        
        # Order total and action buttons
        bottom_frame = tk.Frame(card_frame, bg=self.colors['card'])
        bottom_frame.pack(fill='x', padx=15, pady=(5, 15))
        
        # Total
        total_label = tk.Label(bottom_frame, text=f"Total: ¥{order['total']:.2f}", 
                              font=('Microsoft YaHei UI', 12, 'bold'),
                              bg=self.colors['card'], fg=self.colors['primary'])
        total_label.pack(side='left')
        
        # Payment method and type
        payment_label = tk.Label(bottom_frame, text=f"{order['payment']} | {order['type']}", 
                               font=('Microsoft YaHei UI', 9),
                               bg=self.colors['card'], fg=self.colors['text_light'])
        payment_label.pack(side='left', padx=(20, 0))
        
        # Action buttons
        actions_frame = tk.Frame(bottom_frame, bg=self.colors['card'])
        actions_frame.pack(side='right')

        # View details button
        detail_btn = tk.Button(actions_frame, text="View Details",
                              font=('Microsoft YaHei UI', 9),
                              bg=self.colors['info'], fg=self.colors['white'],
                              bd=0, padx=15, pady=5, cursor='hand2',
                              command=lambda o=order: self.show_order_detail(o))
        detail_btn.pack(side='right', padx=5)

        # Dynamic add status action buttons
        order_status = order.get('status', 'Unknown')
        order_type = order.get('type', 'Takeout')

        if order_status == 'Pending':
            self.add_action_button(actions_frame, "Accept", self.colors['success'],
                                   lambda o=order: self.update_order_status(o['id'], 'Accepted'))
            self.add_action_button(actions_frame, "Cancel", self.colors['danger'],
                                   lambda o=order: self.update_order_status(o['id'], 'Cancelled'))

        elif order_status == 'Accepted':
            self.add_action_button(actions_frame, "Start Preparing", self.colors['warning'],
                                   lambda o=order: self.update_order_status(o['id'], 'Preparing'))
            self.add_action_button(actions_frame, "Cancel", self.colors['danger'],
                                   lambda o=order: self.update_order_status(o['id'], 'Cancelled'))

        elif order_status == 'Preparing':
            next_status = 'Delivering' if order_type == 'Takeout' else 'Ready for Pickup'
            self.add_action_button(actions_frame, "Finish Preparing", self.colors['primary'],
                                   lambda o=order, s=next_status: self.update_order_status(o['id'], s))
            self.add_action_button(actions_frame, "Pause", '#7f8c8d',
                                   lambda o=order: self.update_order_status(o['id'], 'Paused'))

        elif order_status == 'Paused':
             self.add_action_button(actions_frame, "Continue Preparing", self.colors['success'],
                                   lambda o=order: self.update_order_status(o['id'], 'Preparing'))

        elif order_status == 'Delivering' or order_status == 'Ready for Pickup':
            self.add_action_button(actions_frame, "Delivered", self.colors['success'],
                                   lambda o=order: self.update_order_status(o['id'], 'Completed'))

        elif order_status == 'Completed':
            self.add_action_button(actions_frame, "Archive", self.colors['info'],
                                   lambda o=order: self.update_order_status(o['id'], 'Archived'))
        
        # Note information
        if order.get('note'):
            note_frame = tk.Frame(card_frame, bg=self.colors['light'], padx=10, pady=5)
            note_frame.pack(fill='x', padx=15, pady=(0, 15))
            
            note_label = tk.Label(note_frame, text=f"📝 Note: {order['note']}", 
                                 font=('Microsoft YaHei UI', 9),
                                 bg=self.colors['light'], fg=self.colors['text'])
            note_label.pack(anchor='w')
        
        return card_frame

    def add_action_button(self, parent, text, color, command):
        """Helper function, used to create standardized action buttons"""
        btn = tk.Button(parent, text=text,
                        font=('Microsoft YaHei UI', 9),
                        bg=color, fg=self.colors['white'],
                        bd=0, padx=15, pady=5, cursor='hand2',
                        command=command)
        btn.pack(side='right', padx=5)

    def update_order_status(self, order_id, new_status):
        """Update order status and refresh UI"""
        success = data_manager.update_order_status(order_id, new_status)
        if success:
            messagebox.showinfo("Success", f"Order #{order_id} status has been updated to: {new_status}")
            # Reload data from database to ensure consistency
            self.refresh_data()
        else:
            messagebox.showerror("Failed", "Failed to update order status, please try again")
    
    def show_order_detail(self, order):
        """Show order details"""
        detail_window = tk.Toplevel()
        detail_window.title(f"Order Details - #{order['id']}")
        detail_window.geometry("500x600")
        detail_window.configure(bg=self.colors['background'])
        detail_window.resizable(False, False)
        
        # Title
        title_frame = tk.Frame(detail_window, bg=self.colors['primary'], height=60)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text="【Test Modified V2】Order Details #" + str(order['id']),
                              font=('Microsoft YaHei UI', 16, 'bold'),
                              bg=self.colors['primary'], fg=self.colors['white'])
        title_label.pack(expand=True)
        
        # Details content
        content_frame = tk.Frame(detail_window, bg=self.colors['background'])
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Basic information
        info_frame = tk.Frame(content_frame, bg=self.colors['card'], padx=20, pady=15)
        info_frame.pack(fill='x', pady=(0, 10))
        
        tk.Label(info_frame, text="Basic Information", font=('Microsoft YaHei UI', 12, 'bold'),
                bg=self.colors['card'], fg=self.colors['text']).pack(anchor='w')
        
        info_text = f"""Order Number: #{order['id']}
Customer Name: {order['customer']}
Contact Phone: {order['phone']}
Delivery Address: {order['address']}
Order Type: {order['type']}
Payment Method: {order['payment']}
Order Time: {order['create_time']}
Order Status: {order['status']}"""
        
        tk.Label(info_frame, text=info_text, font=('Microsoft YaHei UI', 10),
                bg=self.colors['card'], fg=self.colors['text'], justify='left').pack(anchor='w', pady=(10, 0))
        
        # Meal information
        meals_frame = tk.Frame(content_frame, bg=self.colors['card'], padx=20, pady=15)
        meals_frame.pack(fill='x', pady=(0, 10))
        
        tk.Label(meals_frame, text="Meal Information", font=('Microsoft YaHei UI', 12, 'bold'),
                bg=self.colors['card'], fg=self.colors['text']).pack(anchor='w')
        
        for meal in order['meals']:
            meal_frame = tk.Frame(meals_frame, bg=self.colors['background'], padx=10, pady=5)
            meal_frame.pack(fill='x', pady=5)
            
            tk.Label(meal_frame, text=meal['name'], font=('Microsoft YaHei UI', 10, 'bold'),
                    bg=self.colors['background'], fg=self.colors['text']).pack(side='left')
            
            tk.Label(meal_frame, text=f"¥{meal['price']:.2f} × {meal['quantity']} = ¥{meal['price'] * meal['quantity']:.2f}", 
                    font=('Microsoft YaHei UI', 10),
                    bg=self.colors['background'], fg=self.colors['text']).pack(side='right')
        
        # Total
        total_frame = tk.Frame(meals_frame, bg=self.colors['primary'], padx=10, pady=8)
        total_frame.pack(fill='x', pady=(10, 0))
        
        tk.Label(total_frame, text=f"Order Total: ¥{order['total']:.2f}", 
                font=('Microsoft YaHei UI', 12, 'bold'),
                bg=self.colors['primary'], fg=self.colors['white']).pack()
        
        # Note information
        if order['note']:
            note_frame = tk.Frame(content_frame, bg=self.colors['card'], padx=20, pady=15)
            note_frame.pack(fill='x', pady=(0, 10))
            
            tk.Label(note_frame, text="Note Information", font=('Microsoft YaHei UI', 12, 'bold'),
                    bg=self.colors['card'], fg=self.colors['text']).pack(anchor='w')
            
            tk.Label(note_frame, text=order['note'], font=('Microsoft YaHei UI', 10),
                    bg=self.colors['card'], fg=self.colors['text'], wraplength=400).pack(anchor='w', pady=(10, 0))
          # Close button
        tk.Button(content_frame, text="Close", font=('Microsoft YaHei UI', 10),
                 bg=self.colors['text_light'], fg=self.colors['white'],
                 bd=0, padx=30, pady=8, cursor='hand2',
                 command=detail_window.destroy).pack(pady=20)
    
    def filter_orders(self, status):
        """Filter orders"""
        self.current_filter = status
        self.refresh_order_list()
        
        # Update filter button status display
        self.update_filter_buttons()
    
    def refresh_data(self):
        """Reload data from database and refresh entire UI"""
        # 1. Reload latest data from database
        self.order_data = self.load_order_data()
        
        # 2. Update statistics card
        self.update_statistics()
        
        # 3. Refresh order list
        if hasattr(self, 'orders_container'):
            self.refresh_order_list()
    
    def update_statistics(self):
        """Update statistics information"""
        if not self.stats_frame:
            return
            
        # Clear existing statistics cards
        for widget in self.stats_frame.winfo_children():
            widget.destroy()
        
        # Count orders by status
        status_counts = {status: 0 for status in self.status_colors}
        for order in self.order_data:
            status = order.get('status', 'Unknown')
            if status in status_counts:
                status_counts[status] += 1
        
        # Recreate statistics cards
        # We only display orders with status or some key statuses to avoid UI being too crowded
        key_statuses = ['Pending', 'Preparing', 'Delivering', 'Ready for Pickup', 'Completed', 'Cancelled']
        
        # Add other statuses of existing orders
        for status, count in status_counts.items():
            if count > 0 and status not in key_statuses:
                key_statuses.append(status)

        for status in key_statuses:
             if status in status_counts:
                count = status_counts[status]
                color = self.status_colors.get(status, '#bdc3c7')
                self.create_status_card(self.stats_frame, status, count, color)
    
    def add_new_order(self):
        """Add new order"""
        # Create new order window
        order_window = tk.Toplevel()
        order_window.title("New Order")
        order_window.geometry("600x800")  # Increase height from 700 to 800
        order_window.configure(bg=self.colors['background'])
        order_window.resizable(False, False)
        
        # Title
        title_frame = tk.Frame(order_window, bg=self.colors['primary'], height=60)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text="New Order", 
                              font=('Microsoft YaHei UI', 16, 'bold'),
                              bg=self.colors['primary'], fg=self.colors['white'])
        title_label.pack(expand=True)
        
        # Form content
        form_frame = tk.Frame(order_window, bg=self.colors['background'])
        form_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Customer information
        customer_frame = tk.Frame(form_frame, bg=self.colors['card'], padx=20, pady=15)
        customer_frame.pack(fill='x', pady=(0, 10))
        
        tk.Label(customer_frame, text="Customer Information", font=('Microsoft YaHei UI', 12, 'bold'),
                bg=self.colors['card'], fg=self.colors['text']).pack(anchor='w')
        
        # Customer name
        name_frame = tk.Frame(customer_frame, bg=self.colors['card'])
        name_frame.pack(fill='x', pady=5)
        tk.Label(name_frame, text="Customer Name:", font=('Microsoft YaHei UI', 10),
                bg=self.colors['card'], fg=self.colors['text']).pack(side='left')
        customer_name_var = tk.StringVar(order_window)
        name_entry = tk.Entry(name_frame, textvariable=customer_name_var, font=('Microsoft YaHei UI', 10))
        name_entry.pack(side='right', fill='x', expand=True, padx=(10, 0))
        
        # Contact phone
        phone_frame = tk.Frame(customer_frame, bg=self.colors['card'])
        phone_frame.pack(fill='x', pady=5)
        tk.Label(phone_frame, text="Contact Phone:", font=('Microsoft YaHei UI', 10),
                bg=self.colors['card'], fg=self.colors['text']).pack(side='left')
        customer_phone_var = tk.StringVar(order_window)
        phone_entry = tk.Entry(phone_frame, textvariable=customer_phone_var, font=('Microsoft YaHei UI', 10))
        phone_entry.pack(side='right', fill='x', expand=True, padx=(10, 0))
        
        # Delivery address
        address_frame = tk.Frame(customer_frame, bg=self.colors['card'])
        address_frame.pack(fill='x', pady=5)
        tk.Label(address_frame, text="Delivery Address:", font=('Microsoft YaHei UI', 10),
                bg=self.colors['card'], fg=self.colors['text']).pack(side='left')
        customer_address_var = tk.StringVar(order_window)
        address_entry = tk.Entry(address_frame, textvariable=customer_address_var, font=('Microsoft YaHei UI', 10))
        address_entry.pack(side='right', fill='x', expand=True, padx=(10, 0))
        
        # Order type
        type_frame = tk.Frame(customer_frame, bg=self.colors['card'])
        type_frame.pack(fill='x', pady=5)
        tk.Label(type_frame, text="Order Type:", font=('Microsoft YaHei UI', 10),
                bg=self.colors['card'], fg=self.colors['text']).pack(side='left')
        order_type_var = tk.StringVar(order_window, value="Takeout")
        type_combo = ttk.Combobox(type_frame, textvariable=order_type_var, 
                                 values=["Takeout", "Dine-in"], state="readonly")
        type_combo.pack(side='right', padx=(10, 0))
        
        # Payment method
        payment_frame = tk.Frame(customer_frame, bg=self.colors['card'])
        payment_frame.pack(fill='x', pady=5)
        tk.Label(payment_frame, text="Payment Method:", font=('Microsoft YaHei UI', 10),
                bg=self.colors['card'], fg=self.colors['text']).pack(side='left')
        payment_var = tk.StringVar(order_window, value="WeChat Pay")
        payment_combo = ttk.Combobox(payment_frame, textvariable=payment_var, 
                                    values=["WeChat Pay", "Alipay", "Cash", "Bank Card"], state="readonly")
        payment_combo.pack(side='right', padx=(10, 0))
        
        # Note
        note_frame = tk.Frame(customer_frame, bg=self.colors['card'])
        note_frame.pack(fill='x', pady=5)
        tk.Label(note_frame, text="Order Note:", font=('Microsoft YaHei UI', 10),
                bg=self.colors['card'], fg=self.colors['text']).pack(anchor='w')
        note_var = tk.StringVar(order_window)
        note_entry = tk.Entry(note_frame, textvariable=note_var, font=('Microsoft YaHei UI', 10))
        note_entry.pack(fill='x', pady=(5, 0))
        
        # Meal selection
        meals_frame = tk.Frame(form_frame, bg=self.colors['card'], padx=20, pady=15)
        meals_frame.pack(fill='both', expand=True, pady=(0, 10))
        
        tk.Label(meals_frame, text="Meal Selection", font=('Microsoft YaHei UI', 12, 'bold'),
                bg=self.colors['card'], fg=self.colors['text']).pack(anchor='w')
        
        # Simplified meal selection (should be obtained from meal module)
        sample_meals = [
            {"name": "Tomato Beef Noodles", "price": 25.0},
            {"name": "Egg Fried Rice", "price": 18.0},
            {"name": "Beef Burger", "price": 32.0},
            {"name": "Braised Pork", "price": 35.0},
            {"name": "Cola", "price": 5.0},
            {"name": "Rice", "price": 3.0}
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
            
            # Quantity selection
            qty_var = tk.IntVar(value=1)
            meal_vars[f"{meal['name']}_qty"] = qty_var
            
            tk.Label(meal_frame, text="Quantity:", font=('Microsoft YaHei UI', 9),
                    bg=self.colors['background'], fg=self.colors['text']).pack(side='right', padx=(0, 5))
            
            qty_spinbox = tk.Spinbox(meal_frame, from_=1, to=10, width=5, textvariable=qty_var)
            qty_spinbox.pack(side='right')
        
        # Buttons
        button_frame = tk.Frame(form_frame, bg=self.colors['background'])
        button_frame.pack(fill='x', pady=10)
        
        def save_order():
            # Verify input
            if not customer_name_var.get() or not customer_phone_var.get():
                messagebox.showerror("Error", "Please fill in customer name and contact phone")
                return
            
            # Collect selected meals
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
                messagebox.showerror("Error", "Please select at least one meal")
                return
            
            try:
                # Prepare order data for stock check
                order_items = []
                for meal in order_meals:
                    order_items.append({
                        'product_id': meal['name'],  # Use meal name as product ID
                        'quantity': meal['quantity']
                    })
                
                # Create order data
                order_data = {
                    "customer_name": customer_name_var.get(),
                    "phone": customer_phone_var.get(),
                    "address": customer_address_var.get() if customer_address_var.get() else "Dine-in",
                    "items": order_items,
                    "meals": order_meals,  # Keep original meals format for display
                    "total_amount": total_amount,
                    "type": order_type_var.get(),
                    "payment": payment_var.get(),
                    "note": note_var.get(),
                    "status": "Pending"
                }
                
                # Use data manager to create order (including stock check)
                try:
                    order_id = data_manager.create_order(order_data)
                    messagebox.showinfo("Success", f"Order #{order_id} created successfully!")
                    order_window.destroy()
                    self.refresh_order_list()
                except ValueError as e:
                    if "Stock insufficient" in str(e):
                        messagebox.showerror("Stock insufficient", "Current stock insufficient, unable to create order.\nPlease check meal stock and try again.")
                    else:
                        messagebox.showerror("Error", f"Failed to create order: {e}")
                    return
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to create order: {e}")
                    return
                    
            except Exception as e:
                messagebox.showerror("Error", f"Order processing failed: {e}")
                return
        
        save_btn = tk.Button(button_frame, text="Save Order", 
                           font=('Microsoft YaHei UI', 10, 'bold'),
                           bg=self.colors['primary'], fg=self.colors['white'],
                           bd=0, padx=30, pady=8, cursor='hand2',
                           command=save_order)
        save_btn.pack(side='right', padx=5)
        
        cancel_btn = tk.Button(button_frame, text="Cancel", 
                             font=('Microsoft YaHei UI', 10),
                             bg=self.colors['text_light'], fg=self.colors['white'],
                             bd=0, padx=30, pady=8, cursor='hand2',
                             command=order_window.destroy)
        cancel_btn.pack(side='right', padx=5)
    
    def on_data_changed(self, event_type, data):
        """Handle data change notification"""
        if event_type in ['order_added', 'order_updated']:
            # Refresh order data
            self.order_data = self.load_order_data()
            # If current displaying order interface, refresh display
            if hasattr(self, 'order_list_frame'):
                self.refresh_order_list()
    
    def refresh_order_list(self):
        """Refresh order list"""
        # Reload order data
        self.order_data = self.load_order_data()
        
        # Clear container (if exists)
        if hasattr(self, 'orders_container') and self.orders_container:
            for widget in self.orders_container.winfo_children():
                widget.destroy()
        
        # Filter and search orders
        filtered_orders = self.order_data
        
        # Apply status filter
        if self.current_filter != "All":
            filtered_orders = [order for order in self.order_data if order['status'] == self.current_filter]
        
        # Apply search
        if hasattr(self, 'search_keyword') and self.search_keyword:
            filtered_orders = [order for order in filtered_orders 
                              if self.search_keyword.lower() in order.get('customer', '').lower() 
                              or self.search_keyword in str(order['id'])
                              or self.search_keyword.lower() in order.get('phone', '').lower()]
        
        # Create order card
        if hasattr(self, 'orders_container') and self.orders_container:
            for order in filtered_orders:
                self.create_order_card(self.orders_container, order)
        
        # Update statistics information
        self.update_statistics()
    
    def update_title_frame(self):
        """Update title frame but keep breadcrumb navigation"""
        # Do not clear entire title_frame, but find and update specific elements
        # If title_frame is empty or no suitable element found, create new title
        found_title = False
        
        try:
            for widget in self.title_frame.winfo_children():
                if isinstance(widget, tk.Frame):
                    for child in widget.winfo_children():
                        if isinstance(child, tk.Label):
                            text = child.cget("text")
                            # If it's module title (not breadcrumb), then update
                            if "Order Management" in text or ("Management" in text and "Home" not in text):
                                child.configure(text="📋 Order Management")
                                found_title = True
                                break
                    if found_title:
                        break
        except tk.TclError:
            # Widget may have been destroyed
            pass
        
        # If no existing title found, create new title area
        if not found_title:
            # Title bar
            title_container = tk.Frame(self.title_frame, bg=self.colors['white'])
            title_container.pack(fill='x', side='bottom')  # Put at bottom, does not affect breadcrumbs
            
            # Title
            title_label = tk.Label(title_container, text="📋 Order Management", 
                                  font=('Microsoft YaHei UI', 18, 'bold'),
                                  bg=self.colors['white'], fg=self.colors['text'])
            title_label.pack(side='left', padx=20, pady=15)
            
            # Action buttons
            actions_frame = tk.Frame(title_container, bg=self.colors['white'])
            actions_frame.pack(side='right', padx=20, pady=15)
            
            # New order button
            add_btn = tk.Button(actions_frame, text="➕ New Order", 
                               font=('Microsoft YaHei UI', 10, 'bold'),
                               bg=self.colors['primary'], fg=self.colors['white'],
                               bd=0, padx=20, pady=8, cursor='hand2',
                               command=self.add_new_order)
            add_btn.pack(side='right', padx=5)
            
            # Refresh button
            refresh_btn = tk.Button(actions_frame, text="🔄 Refresh", 
                                   font=('Microsoft YaHei UI', 10),
                                   bg=self.colors['info'], fg=self.colors['white'],
                                   bd=0, padx=20, pady=8, cursor='hand2',
                                   command=self.refresh_order_list)
            refresh_btn.pack(side='right', padx=5)
            
            # Export button
            export_btn = tk.Button(actions_frame, text="📊 Export", 
                                  font=('Microsoft YaHei UI', 10),
                                  bg=self.colors['success'], fg=self.colors['white'],
                                  bd=0, padx=20, pady=8, cursor='hand2',
                                  command=self.export_orders)
            export_btn.pack(side='right', padx=5)
    
    def show(self):
        """Show order management interface"""
        self.clear_frames()
        self.update_title_frame()
        
        # Create main container
        main_frame = tk.Frame(self.parent_frame, bg=self.colors['background'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Top statistics information
        self.stats_frame = tk.Frame(main_frame, bg=self.colors['background'])
        self.stats_frame.pack(fill='x', pady=(10, 5))
        
        # Filter and search
        self.create_filter_bar(main_frame)
        
        # Order list
        self.create_order_list(main_frame)
        
        # First load refresh data
        self.refresh_data()

    def clear_frames(self):
        """Clear all subframes"""
        for widget in self.parent_frame.winfo_children():
            widget.destroy()

    def create_filter_bar(self, parent):
        """Create filter bar"""
        filter_frame = tk.Frame(parent, bg=self.colors['background'])
        filter_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(filter_frame, text="Filter Orders:", font=('Microsoft YaHei UI', 12, 'bold'),
                bg=self.colors['background'], fg=self.colors['text']).pack(side='left')
        
        # Store filter buttons for subsequent status update
        self.filter_buttons = {}
        filter_buttons = ["All", "Pending", "Accepted", "Preparing", "Delivering", "Completed", "Cancelled"]
        
        for filter_name in filter_buttons:
            btn_color = self.colors['primary'] if filter_name == self.current_filter else self.colors['light']
            text_color = self.colors['white'] if filter_name == self.current_filter else self.colors['text']
            
            filter_btn = tk.Button(filter_frame, text=filter_name, 
                                  font=('Microsoft YaHei UI', 9),
                                  bg=btn_color, fg=text_color,
                                  bd=0, padx=15, pady=5, cursor='hand2',
                                  command=lambda f=filter_name: self.filter_orders(f))
            filter_btn.pack(side='left', padx=5)
            self.filter_buttons[filter_name] = filter_btn
    
    def update_filter_buttons(self):
        """Update filter button status display"""
        if hasattr(self, 'filter_buttons'):
            for filter_name, button in self.filter_buttons.items():
                try:
                    if filter_name == self.current_filter:
                        button.configure(bg=self.colors['primary'], fg=self.colors['white'])
                    else:
                        button.configure(bg=self.colors['light'], fg=self.colors['text'])
                except tk.TclError:
                    # Button may have been destroyed
                    pass
    
    def create_order_list(self, parent):
        """Create order list"""
        # Order list container
        list_frame = tk.Frame(parent, bg=self.colors['background'])
        list_frame.pack(fill='both', expand=True)
        
        # Scroll area
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
        
        # Initial display
        self.refresh_order_list()
        
        # Bind mouse wheel events
        def on_mousewheel(event):
            try:
                if canvas.winfo_exists():
                    canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            except tk.TclError:
                pass  # Widget may have been destroyed, ignore error
        
        canvas.bind("<MouseWheel>", on_mousewheel)
        self.orders_container.bind("<MouseWheel>", on_mousewheel)

    def export_orders(self):
        """Export order data"""
        try:
            from tkinter import filedialog
            import datetime
            
            # Create export selection dialog
            dialog = tk.Toplevel(self.parent_frame)
            dialog.title("Export Order Data")
            dialog.geometry("400x300")
            dialog.configure(bg=self.colors['background'])
            dialog.transient(self.parent_frame)
            dialog.grab_set()
            
            # Center display
            dialog.update_idletasks()
            x = (dialog.winfo_screenwidth() // 2) - (200)
            y = (dialog.winfo_screenheight() // 2) - (150)
            dialog.geometry(f"400x300+{x}+{y}")
            
            # Title
            tk.Label(dialog, text="Export Order Data", font=('Microsoft YaHei UI', 14, 'bold'),
                    bg=self.colors['background'], fg=self.colors['text']).pack(pady=15)
            
            # Export options frame
            options_frame = tk.Frame(dialog, bg=self.colors['background'])
            options_frame.pack(fill="both", expand=True, padx=20, pady=10)
            
            # Export format selection
            tk.Label(options_frame, text="Select Export Format:", font=('Microsoft YaHei UI', 12),
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
            
            # Status filter
            tk.Label(options_frame, text="Status Filter:", font=('Microsoft YaHei UI', 12),
                    bg=self.colors['background'], fg=self.colors['text']).pack(anchor="w", pady=(20, 10))
            
            status_var = tk.StringVar(dialog, value="All")
            status_options = ["All", "Pending", "Accepted", "Preparing", "Delivering", "Completed", "Cancelled"]
            
            status_combo = ttk.Combobox(options_frame, textvariable=status_var, 
                                      values=status_options, state="readonly", width=20)
            status_combo.pack(anchor="w")
            
            # Button frame
            btn_frame = tk.Frame(dialog, bg=self.colors['background'])
            btn_frame.pack(fill="x", padx=20, pady=20)
            
            def do_export():
                try:
                    file_format = format_var.get()
                    status_filter = status_var.get()
                    
                    # Get current timestamp
                    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"Order Data_{status_filter}_{timestamp}"
                    
                    # Select save path
                    if file_format == "Excel":
                        file_path = filedialog.asksaveasfilename(
                            defaultextension=".xlsx",
                            filetypes=[("Excel File", "*.xlsx")],
                            initialname=filename
                        )
                        if file_path:
                            success = self.export_orders_to_excel(file_path, status_filter)
                    elif file_format == "CSV":
                        file_path = filedialog.asksaveasfilename(
                            defaultextension=".csv",
                            filetypes=[("CSV File", "*.csv")],
                            initialname=filename
                        )
                        if file_path:
                            success = self.export_orders_to_csv(file_path, status_filter)
                    elif file_format == "PDF":
                        file_path = filedialog.asksaveasfilename(
                            defaultextension=".pdf",
                            filetypes=[("PDF File", "*.pdf")],
                            initialname=filename
                        )
                        if file_path:
                            success = self.export_orders_to_pdf(file_path, status_filter)
                    
                    if success:
                        messagebox.showinfo("Export Success", f"Order data successfully exported to {file_format} format", parent=dialog)
                        dialog.destroy()
                    else:
                        messagebox.showerror("Export Failed", "Error occurred during export", parent=dialog)
                        
                except Exception as e:
                    messagebox.showerror("Error", f"Export failed: {e}", parent=dialog)
            
            tk.Button(btn_frame, text="📊 Start Export", command=do_export,
                     bg=self.colors['primary'], fg='white', bd=0, pady=8, padx=20,
                     font=('Microsoft YaHei UI', 10)).pack(side="left")
            tk.Button(btn_frame, text="Cancel", command=dialog.destroy,
                     bg=self.colors['text_light'], fg='white', bd=0, pady=8, padx=20,
                     font=('Microsoft YaHei UI', 10)).pack(side="right")
                     
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open export dialog: {e}")
    
    def export_orders_to_excel(self, file_path: str, status_filter: str) -> bool:
        """Export order to Excel format"""
        try:
            import openpyxl
            from openpyxl.styles import Font, Alignment, PatternFill
            
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "Order Data"
            
            # Set title
            title = f"Smart Restaurant Management System - Order Data ({status_filter})"
            ws['A1'] = title
            ws['A1'].font = Font(size=16, bold=True)
            ws.merge_cells('A1:H1')
            
            # Set header style
            header_font = Font(bold=True, color="FFFFFF")
            header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
            header_alignment = Alignment(horizontal="center", vertical="center")
            
            # Header
            headers = ["Order Number", "Customer Name", "Contact Phone", "Delivery Address", "Meal", "Total Amount", "Order Status", "Order Time"]
            ws.append(headers)
            
            # Set header style
            for cell in ws[2]:
                cell.font = header_font
                cell.fill = header_fill
                cell.alignment = header_alignment
            
            # Get order data
            orders = self.get_filtered_orders(status_filter)
            
            # Add data
            for order in orders:
                # Process meal information
                meals_text = ""
                for meal in order.get('meals', []):
                    meals_text += f"{meal.get('name', '')}x{meal.get('quantity', 1)} "
                
                row = [
                    f"#{order.get('id', '')}",
                    order.get('customer', ''),
                    order.get('phone', ''),
                    order.get('address', ''),
                    meals_text.strip(),
                    f"￥{order.get('total', 0):.2f}",
                    order.get('status', ''),
                    order.get('create_time', '')
                ]
                ws.append(row)
            
            # Adjust column width
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
            messagebox.showerror("Error", "Please install openpyxl library: pip install openpyxl")
            return False
        except Exception as e:
            print(f"Failed to export Excel: {e}")
            return False
    
    def export_orders_to_csv(self, file_path: str, status_filter: str) -> bool:
        """Export order to CSV format"""
        try:
            import csv
            
            with open(file_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
                fieldnames = ["Order Number", "Customer Name", "Contact Phone", "Delivery Address", "Meal", "Total Amount", "Order Status", "Order Time"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                # Get order data
                orders = self.get_filtered_orders(status_filter)
                
                for order in orders:
                    # Process meal information
                    meals_text = ""
                    for meal in order.get('meals', []):
                        meals_text += f"{meal.get('name', '')}x{meal.get('quantity', 1)} "
                    
                    writer.writerow({
                        "Order Number": f"#{order.get('id', '')}",
                        "Customer Name": order.get('customer', ''),
                        "Contact Phone": order.get('phone', ''),
                        "Delivery Address": order.get('address', ''),
                        "Meal": meals_text.strip(),
                        "Total Amount": f"￥{order.get('total', 0):.2f}",
                        "Order Status": order.get('status', ''),
                        "Order Time": order.get('create_time', '')
                    })
            
            return True
            
        except Exception as e:
            print(f"Failed to export CSV: {e}")
            return False
    
    def export_orders_to_pdf(self, file_path: str, status_filter: str) -> bool:
        """Export order to PDF format"""
        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib import colors
            
            doc = SimpleDocTemplate(file_path, pagesize=A4)
            story = []
            
            # Title style
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=16,
                spaceAfter=30,
                alignment=1  # Center
            )
            
            # Add title
            title = Paragraph(f"Smart Restaurant Management System - Order Data ({status_filter})", title_style)
            story.append(title)
            story.append(Spacer(1, 20))
            
            # Get order data
            orders = self.get_filtered_orders(status_filter)
            
            # Create table data
            table_data = [["Order Number", "Customer Name", "Contact Phone", "Delivery Address", "Meal", "Total Amount", "Order Status", "Order Time"]]
            
            for order in orders:
                # Process meal information
                meals_text = ""
                for meal in order.get('meals', []):
                    meals_text += f"{meal.get('name', '')}x{meal.get('quantity', 1)} "
                
                row = [
                    f"#{order.get('id', '')}",
                    order.get('customer', ''),
                    order.get('phone', ''),
                    order.get('address', ''),
                    meals_text.strip(),
                    f"￥{order.get('total', 0):.2f}",
                    order.get('status', ''),
                    order.get('create_time', '')
                ]
                table_data.append(row)
            
            # Create table
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
            messagebox.showerror("Error", "Please install reportlab library: pip install reportlab")
            return False
        except Exception as e:
            print(f"Failed to export PDF: {e}")
            return False
    
    def get_filtered_orders(self, status_filter: str) -> List[Dict]:
        """Get filtered order data"""
        if status_filter == "All":
            return self.order_data
        else:
            return [order for order in self.order_data if order.get('status') == status_filter]
