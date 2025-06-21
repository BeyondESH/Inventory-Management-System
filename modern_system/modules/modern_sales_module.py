#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modern Sales Management Module - Dine-in Ordering System
Provides complete dine-in customer ordering and checkout functionality
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from typing import Dict, List, Any, Optional
import datetime
import json
import threading

# Import data management center
try:
    from .data_manager import data_manager
except ImportError:
    try:
        from data_manager import data_manager
    except ImportError:
        # Mock data manager
        class MockDataManager:
            def load_data(self, data_type):
                if data_type == 'meals':
                    return [
                        {"id": "MEAL001", "name": "Tomato Beef Noodles", "category": "Noodles", "price": 25.0, "image": "🍜"},
                        {"id": "MEAL002", "name": "Egg Fried Rice", "category": "Fried Rice", "price": 18.0, "image": "🍚"},
                        {"id": "MEAL003", "name": "Beef Burger", "category": "Western", "price": 32.0, "image": "🍔"},
                        {"id": "MEAL004", "name": "French Fries", "category": "Snacks", "price": 12.0, "image": "🍟"},
                        {"id": "MEAL005", "name": "Coke", "category": "Drinks", "price": 8.0, "image": "🥤"},
                        {"id": "MEAL006", "name": "Coffee", "category": "Drinks", "price": 15.0, "image": "☕"}
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
        
        # Register with the data management center
        data_manager.register_module('sales', self)
        
        # Modern color scheme
        self.colors = {
            'primary': '#FF6B35',      # Main color
            'secondary': '#F7931E',    # Secondary color
            'accent': '#FFD23F',       # Accent color
            'background': '#F8F9FA',   # Background color
            'surface': '#FFFFFF',      # Card background
            'text_primary': '#2D3436', # Primary text
            'text_secondary': '#636E72', # Secondary text
            'border': '#E0E0E0',       # Border
            'success': '#00B894',      # Success color
            'warning': '#FDCB6E',      # Warning color
            'error': '#E84393',        # Error color
            'card_shadow': '#F0F0F0',  # Card shadow
            'white': '#FFFFFF',        # White
            'cart_bg': '#FFF8E1',
            'selected': '#E8F5E8',
            'info': '#3498DB',         # Info color
            'danger': '#E74C3C'        # Danger color
        }
        
        # Font configuration
        self.fonts = {
            'title': ('Segoe UI', 16, 'bold'),
            'heading': ('Segoe UI', 14, 'bold'),
            'body': ('Segoe UI', 12),
            'small': ('Segoe UI', 10),
            'price': ('Segoe UI', 14, 'bold'),
            'cart_title': ('Segoe UI', 13, 'bold')
        }
          # Cart data
        self.cart_items = []
        self.total_amount = 0.0
        self.current_table = "Table 1"
        
        # Meal data
        self.meals_data = self.load_meals_data()
        self.categories = list(set(meal.get('category', 'Other') for meal in self.meals_data))
        self.current_category = "All" if self.categories else "Noodles"
        
        self.main_frame = None
        self.table_var = None  # Lazy initialization
        
    def load_meals_data(self):
        """Load meal data - only show available meals"""
        try:
            meals = data_manager.load_data('meals')
            # Filter to show only available meals
            available_meals = []
            for meal in meals:
                # Check if the meal is available
                is_available = meal.get('is_available', True)  # Default to True
                if isinstance(is_available, str):
                    is_available = is_available.lower() in ['true', '1', 'yes', 'on shelf']
                elif isinstance(is_available, int):
                    is_available = is_available == 1
                
                # Check if there is enough inventory for the meal
                has_inventory = self.check_meal_inventory(meal)
                
                if is_available and has_inventory:
                    # Add default icons and descriptions for meals from the database, and ensure compatibility with all UI fields
                    # name field
                    if 'name' not in meal:
                        meal['name'] = meal.get('meal_name', '')
                    # price field
                    if 'price' not in meal:
                        meal['price'] = meal.get('meal_price', 0)
                    # id field
                    if 'id' not in meal:
                        meal['id'] = meal.get('meal_id', meal.get('id', ''))
                    # category field
                    if 'category' not in meal:
                        meal['category'] = meal.get('meal_category', 'Other')
                    # image field
                    if 'image' not in meal:
                        meal_name = meal['name'].lower()
                        if 'noodle' in meal_name or 'rice' in meal_name:
                            meal['image'] = '🍜'
                        elif 'burger' in meal_name:
                            meal['image'] = '🍔'
                        elif 'fries' in meal_name:
                            meal['image'] = '🍟'
                        elif 'coke' in meal_name or 'soda' in meal_name:
                            meal['image'] = '🥤'
                        elif 'coffee' in meal_name:
                            meal['image'] = '☕'
                        elif 'chicken' in meal_name:
                            meal['image'] = '🍗'
                        elif 'fish' in meal_name:
                            meal['image'] = '🐟'
                        elif 'tofu' in meal_name:
                            meal['image'] = '🥘'
                        else:
                            meal['image'] = '🍽️'
                    # description field
                    if 'description' not in meal:
                        meal['description'] = meal.get('meal_details', f"A delicious {meal['name']}")
                    
                    available_meals.append(meal)
            
            print(f"✅ Sales module loaded {len(available_meals)} available and in-stock meals")
            return available_meals
            
        except Exception as e:
            print(f"Error loading meal data: {e}")
            # Default meal data (only available items)
            return [
                {"id": "MEAL001", "name": "Salmon Set Meal", "category": "Set Meal", "price": 45.0, "image": "🍣", "description": "Fresh salmon sashimi with special sauce.", "is_available": True},
                {"id": "MEAL002", "name": "Homestyle Chicken Rice", "category": "Rice", "price": 22.0, "image": "🍗", "description": "Tender chicken with fragrant rice.", "is_available": True},
                {"id": "MEAL003", "name": "Seafood Fried Rice", "category": "Rice", "price": 32.0, "image": "🦐", "description": "Fresh seafood with fried rice.", "is_available": True},
                {"id": "MEAL004", "name": "Classic Beef Rice", "category": "Rice", "price": 28.0, "image": "🍖", "description": "Tender beef with rice, a classic pairing.", "is_available": True},
                {"id": "MEAL005", "name": "Vegetable Set Meal", "category": "Set Meal", "price": 18.0, "image": "🥦", "description": "Seasonal vegetables, healthy and vegetarian.", "is_available": True},
                {"id": "MEAL006", "name": "Spicy Tofu", "category": "Chinese", "price": 16.0, "image": "🥘", "description": "Classic Sichuan dish, spicy and flavorful.", "is_available": True}
            ]
        
    def show(self):
        """Show the dine-in ordering interface"""
        self.clear_frames()
        self.update_title()

        if self.main_frame:
            self.main_frame.destroy()
        
        self.main_frame = tk.Frame(self.parent_frame, bg=self.colors['background'])
        self.main_frame.pack(fill="both", expand=True)
        
        # Top info bar
        self.create_top_info_bar()
        
        # Main content area
        content_frame = tk.Frame(self.main_frame, bg=self.colors['background'])
        content_frame.pack(fill="both", expand=True, pady=10)
        
        # Left side: meal display area
        self.create_menu_area(content_frame)
        
        # Right side: shopping cart area
        self.create_cart_area(content_frame)
        
    def update_title(self):
        """Update the module title"""
        title_frame = tk.Frame(self.title_frame, bg=self.colors['surface'])
        title_frame.pack(side="left", fill="y")
        
        icon_label = tk.Label(title_frame, text="🍽️", font=('Segoe UI Emoji', 20),
                             bg=self.colors['surface'], fg=self.colors['primary'])
        icon_label.pack(side="left", padx=(30, 10), pady=20)
        
        title_label = tk.Label(title_frame, text="Dine-in Sales", font=self.fonts['title'],
                              bg=self.colors['surface'], fg=self.colors['text_primary'])
        title_label.pack(side="left", pady=20)

    def clear_frames(self):
        """Clear the content and title frames."""
        for widget in self.parent_frame.winfo_children():
            widget.destroy()
        for widget in self.title_frame.winfo_children():
            widget.destroy()

    def create_top_info_bar(self):
        """Create the top info bar"""
        info_frame = tk.Frame(self.main_frame, bg=self.colors['surface'], height=80)
        info_frame.pack(fill="x", padx=10, pady=(0, 10))
        info_frame.pack_propagate(False)
          # Left side: title and table number
        left_frame = tk.Frame(info_frame, bg=self.colors['surface'])
        left_frame.pack(side="left", fill="y", padx=20, pady=10)
        
        title_label = tk.Label(left_frame, text="🍽️ Dine-in Ordering", 
                              font=self.fonts['title'],
                              bg=self.colors['surface'], 
                              fg=self.colors['text_primary'])
        title_label.pack(anchor="w")
        
        # Table number selection
        table_frame = tk.Frame(left_frame, bg=self.colors['surface'])
        table_frame.pack(anchor="w", pady=(5, 0))
        
        table_label = tk.Label(table_frame, text="Current Table:", 
                              font=self.fonts['body'],
                              bg=self.colors['surface'], 
                              fg=self.colors['text_secondary'])
        table_label.pack(side="left")
        
        self.table_var = tk.StringVar(left_frame, value=self.current_table)
        table_combo = ttk.Combobox(table_frame, textvariable=self.table_var, 
                                  values=[f"Table {i}" for i in range(1, 21)], 
                                  width=10, state="readonly")
        table_combo.pack(side="left", padx=(10, 0))
        table_combo.bind('<<ComboboxSelected>>', self.on_table_changed)
        
        # Right side: current time and server
        right_frame = tk.Frame(info_frame, bg=self.colors['surface'])
        right_frame.pack(side="right", fill="y", padx=20, pady=10)
        
        time_label = tk.Label(right_frame, 
                             text=f"⏰ {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}",
                             font=self.fonts['body'],
                             bg=self.colors['surface'], 
                             fg=self.colors['text_secondary'])
        time_label.pack(anchor="e")
        
        staff_label = tk.Label(right_frame, text="👤 Server: Alex",
                              font=self.fonts['body'],
                              bg=self.colors['surface'], 
                              fg=self.colors['text_secondary'])
        staff_label.pack(anchor="e", pady=(5, 0))
        
    def create_menu_area(self, parent):
        """Create the meal display area"""
        menu_frame = tk.Frame(parent, bg=self.colors['surface'])
        menu_frame.pack(side="left", fill="both", expand=True, padx=(10, 5))
        
        # Category navigation
        self.create_category_nav(menu_frame)
        
        # Meal grid
        self.create_menu_grid(menu_frame)
        
    def create_category_nav(self, parent):
        """Create category navigation"""
        nav_frame = tk.Frame(parent, bg=self.colors['surface'], height=60)
        nav_frame.pack(fill="x", padx=10, pady=10)
        nav_frame.pack_propagate(False)
        
        # Add "All" category
        all_categories = ["All"] + self.categories
        
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
        """Create the meal grid"""
        # Scrolling frame
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
        
        # Display meals
        self.display_meals()
        
    def display_meals(self):
        """Display meals"""
        # Clear existing meals
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # Filter meals
        if self.current_category == "All":
            filtered_meals = self.meals_data
        else:
            filtered_meals = [meal for meal in self.meals_data 
                            if meal.get('category') == self.current_category]
        
        # Create meal cards (3-column layout)
        row = 0
        col = 0
        for meal in filtered_meals:
            meal_card = self.create_meal_card(self.scrollable_frame, meal)
            meal_card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            
            col += 1
            if col >= 3:  # 3 per row
                col = 0
                row += 1
        
        # Configure column weights
        for i in range(3):
            self.scrollable_frame.columnconfigure(i, weight=1)
            
    def create_meal_card(self, parent, meal):
        """Create a meal card, with fallbacks for fields to prevent KeyError"""
        card = tk.Frame(parent, bg=self.colors['background'], relief="flat", bd=1)
        card.configure(width=200, height=180)
        card.pack_propagate(False)
        # Meal icon
        icon_label = tk.Label(card, text=meal.get('image', '🍽️'), 
                             font=('Segoe UI Emoji', 32),
                             bg=self.colors['background'])
        icon_label.pack(pady=(15, 5))
        # Meal name
        name_label = tk.Label(card, text=meal.get('name', ''), 
                             font=self.fonts['heading'],
                             bg=self.colors['background'], 
                             fg=self.colors['text_primary'])
        name_label.pack()
        # Description
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
        # Price
        price = meal.get('price', 0)
        bottom_frame = tk.Frame(card, bg=self.colors['background'])
        bottom_frame.pack(side="bottom", fill="x", pady=(10, 0))
        price_label = tk.Label(bottom_frame, text=f"${price:.2f}",
                              font=self.fonts['price'],
                              bg=self.colors['background'],
                              fg=self.colors['primary'])
        price_label.pack(side="left", padx=(10, 0))
        # Add to cart button
        add_btn = tk.Button(bottom_frame, text="Add to Cart", font=self.fonts['small'],
                            bg=self.colors['primary'], fg="white", bd=0, padx=10, pady=3,
                            cursor="hand2", command=lambda m=meal: self.add_to_cart(m))
        add_btn.pack(side="right", padx=(0, 10))
        return card

    def create_cart_area(self, parent):
        """Create the shopping cart area"""
        cart_frame = tk.Frame(parent, bg=self.colors['surface'], width=350)
        cart_frame.pack(side="right", fill="y", padx=(5, 10))
        cart_frame.pack_propagate(False)
        
        # Cart Title
        cart_title_frame = tk.Frame(cart_frame, bg=self.colors['primary'], height=50)
        cart_title_frame.pack(fill="x")
        cart_title_frame.pack_propagate(False)

        cart_title_label = tk.Label(cart_title_frame, text="🛒 Shopping Cart",
                                   font=self.fonts['cart_title'],
                                   bg=self.colors['primary'], fg=self.colors['white'])
        cart_title_label.pack(pady=12)
        
        # Cart items area
        cart_list_canvas = tk.Canvas(cart_frame, bg=self.colors['surface'], highlightthickness=0)
        cart_list_scrollbar = ttk.Scrollbar(cart_frame, orient="vertical", command=cart_list_canvas.yview)
        self.cart_list_frame = tk.Frame(cart_list_canvas, bg=self.colors['surface'])

        self.cart_list_frame.bind(
            "<Configure>",
            lambda e: cart_list_canvas.configure(
                scrollregion=cart_list_canvas.bbox("all")
            )
        )

        cart_list_canvas.create_window((0, 0), window=self.cart_list_frame, anchor="nw")
        cart_list_canvas.configure(yscrollcommand=cart_list_scrollbar.set)
        
        cart_list_canvas.pack(side="top", fill="both", expand=True)
        cart_list_scrollbar.pack(side="right", fill="y")
        
        # Cart bottom area (total, checkout button)
        self.create_cart_bottom(cart_frame)

        self.update_cart_display()
        
    def create_cart_bottom(self, parent):
        """Create the bottom part of the cart"""
        bottom_frame = tk.Frame(parent, bg=self.colors['surface'], height=120)
        bottom_frame.pack(side="bottom", fill="x")
        bottom_frame.pack_propagate(False)
        
        # Separator
        ttk.Separator(bottom_frame, orient='horizontal').pack(fill='x', padx=10)
        
        # Total amount
        total_frame = tk.Frame(bottom_frame, bg=self.colors['surface'])
        total_frame.pack(fill="x", padx=20, pady=10)
        
        total_label = tk.Label(total_frame, text="Total:", 
                              font=self.fonts['heading'],
                              bg=self.colors['surface'], 
                              fg=self.colors['text_primary'])
        total_label.pack(side="left")
        
        self.total_amount_label = tk.Label(total_frame, text="¥ 0.00",
                                          font=self.fonts['heading'],
                                          bg=self.colors['surface'], 
                                          fg=self.colors['primary'])
        self.total_amount_label.pack(side="right")
        
        # Action buttons
        button_frame = tk.Frame(bottom_frame, bg=self.colors['surface'])
        button_frame.pack(fill="both", expand=True, padx=10)
        
        clear_btn = tk.Button(button_frame, text="Clear Cart",
                             bg=self.colors['danger'], fg=self.colors['white'],
                             font=self.fonts['body'], bd=0, cursor="hand2",
                             command=self.clear_cart_with_confirm)
        clear_btn.pack(side="left", expand=True, fill="both", padx=5, ipady=10)
        
        checkout_btn = tk.Button(button_frame, text="Checkout",
                                bg=self.colors['success'], fg=self.colors['white'],
                                font=self.fonts['body'], bd=0, cursor="hand2",
                                command=self.checkout)
        checkout_btn.pack(side="right", expand=True, fill="both", padx=5, ipady=10)
        
    def switch_category(self, category):
        """Switch meal category"""
        self.current_category = category
        
        # Update the style of the currently selected button
        for btn in self.category_buttons.values():
            btn.config(bg=self.colors['background'], fg=self.colors['text_secondary'])
            
        if category in self.category_buttons:
            self.category_buttons[category].config(bg=self.colors['primary'], fg=self.colors['white'])
        
        # Update the meal display area
        self.display_meals()
        
    def add_to_cart(self, meal):
        """Add a meal to the shopping cart"""
        # Check if it already exists
        for item in self.cart_items:
            if item['id'] == meal['id']:
                item['quantity'] += 1
                break
        else:
            # Add new meal
            cart_item = {
                'id': meal['id'],
                'name': meal['name'],
                'price': meal['price'],
                'quantity': 1,                'image': meal.get('image', '🍽️')
            }
            self.cart_items.append(cart_item)
        
        # Update display
        self.update_cart_display()
        
        # Show simple success feedback (without using messagebox)
        self.show_add_success_feedback(meal['name'])
        
    def remove_from_cart(self, meal_id):
        """Remove a meal from the cart"""
        self.cart_items = [item for item in self.cart_items if item['id'] != meal_id]
        self.update_cart_display()
        
    def update_quantity(self, meal_id, change):
        """Update meal quantity"""
        for item in self.cart_items:
            if item['id'] == meal_id:
                item['quantity'] += change
                if item['quantity'] <= 0:
                    self.remove_from_cart(meal_id)
                break
        self.update_cart_display()
        
    def update_cart_display(self):
        """Update the display of the shopping cart"""
        # Clear existing display
        for widget in self.cart_list_frame.winfo_children():
            widget.destroy()
        
        if not self.cart_items:
            no_items_label = tk.Label(self.cart_list_frame, text="Cart is empty",
                                     font=self.fonts['body'],
                                     bg=self.colors['surface'], fg=self.colors['text_secondary'])
            no_items_label.pack(pady=20)
        else:
            # Display cart items
            for item in self.cart_items:
                self.create_cart_item(item)
        
        # Calculate total amount
        self.total_amount = sum(item['price'] * item['quantity'] for item in self.cart_items)
        self.total_amount_label.config(text=f"¥ {self.total_amount:.2f}")
        
    def create_cart_item(self, item):
        """Create a shopping cart item"""
        item_frame = tk.Frame(self.cart_list_frame, bg=self.colors['surface'], padx=10, pady=5)
        item_frame.pack(fill="x")
        
        # Left side: meal name
        name_label = tk.Label(item_frame, text=item['name'], font=self.fonts['body'],
                             bg=self.colors['surface'], fg=self.colors['text_primary'], anchor="w")
        name_label.pack(side="left", fill="x", expand=True)
        
        # Right side: quantity and price
        right_frame = tk.Frame(item_frame, bg=self.colors['surface'])
        right_frame.pack(side="right")
        
        # Quantity control
        qty_frame = tk.Frame(right_frame, bg=self.colors['surface'])
        qty_frame.pack(side="left", padx=10)
        
        minus_btn = tk.Button(qty_frame, text="-", command=lambda: self.update_quantity(item['id'], -1),
                             font=('Segoe UI', 10, 'bold'), width=2, height=1,
                             bg=self.colors['background'], fg=self.colors['text_primary'], bd=0)
        minus_btn.pack(side="left")
        
        qty_label = tk.Label(qty_frame, text=str(item['quantity']), font=self.fonts['body'],
                            bg=self.colors['surface'], fg=self.colors['text_primary'], width=3)
        qty_label.pack(side="left", padx=5)
        
        plus_btn = tk.Button(qty_frame, text="+", command=lambda: self.update_quantity(item['id'], 1),
                            font=('Segoe UI', 10, 'bold'), width=2, height=1,
                            bg=self.colors['background'], fg=self.colors['text_primary'], bd=0)
        plus_btn.pack(side="left")
        
        # Price
        price = item['price'] * item['quantity']
        price_label = tk.Label(right_frame, text=f"¥{price:.2f}",
                              font=self.fonts['body'],
                              bg=self.colors['surface'], fg=self.colors['text_primary'], width=7, anchor="e")
        price_label.pack(side="left")
        
    def clear_cart(self):
        """Clear the shopping cart"""
        self.cart_items.clear()
        self.update_cart_display()
    
    def clear_cart_with_confirm(self):
        """Clear the shopping cart with a confirmation dialog"""
        if not self.cart_items:
            messagebox.showinfo("Info", "The shopping cart is already empty.", parent=self.parent_frame)
            return

        if messagebox.askyesno("Confirm", "Are you sure you want to clear the cart?", parent=self.parent_frame):
            self.clear_cart()
            messagebox.showinfo("Success", "The shopping cart has been cleared.", parent=self.parent_frame)
    
    def on_table_changed(self, event=None):
        """Table number changed event"""
        self.current_table = self.table_var.get()
        print(f"Table changed to: {self.current_table}")
    
    def checkout(self):
        """Checkout process"""
        if not self.cart_items:
            messagebox.showwarning("Warning", "The shopping cart is empty, please add items first.", parent=self.parent_frame)
            return
            
        self.show_checkout_dialog()
    
    def show_checkout_dialog(self):
        """Show the checkout dialog"""
        dialog = tk.Toplevel(self.parent_frame)
        dialog.title("Checkout")
        dialog.geometry("700x550")
        dialog.transient(self.parent_frame)
        dialog.grab_set()
        dialog.resizable(False, False)
        dialog.configure(bg=self.colors['background'])
        
        # Center the dialog
        dialog.update_idletasks()
        x = self.parent_frame.winfo_rootx() + (self.parent_frame.winfo_width() - dialog.winfo_width()) // 2
        y = self.parent_frame.winfo_rooty() + (self.parent_frame.winfo_height() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")

        # Top banner
        top_frame = tk.Frame(dialog, bg=self.colors['primary'], height=60)
        top_frame.pack(fill="x")
        top_frame.pack_propagate(False)
        
        title_label = tk.Label(top_frame, text="Confirm Order and Pay",
                              font=self.fonts['title'],
                              bg=self.colors['primary'], fg=self.colors['white'])
        title_label.pack(pady=15)
        
        # Main content
        main_frame = tk.Frame(dialog, bg=self.colors['background'], padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)

        # Left: order details
        left_frame = tk.Frame(main_frame, bg=self.colors['surface'], padx=15, pady=15)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

        tk.Label(left_frame, text="Order Details", font=self.fonts['heading'],
                 bg=self.colors['surface'], fg=self.colors['text_primary']).pack(anchor="w", pady=(0, 10))

        # Order items list
        items_canvas = tk.Canvas(left_frame, bg=self.colors['surface'], highlightthickness=0)
        items_scrollbar = ttk.Scrollbar(left_frame, orient="vertical", command=items_canvas.yview)
        items_list_frame = tk.Frame(items_canvas, bg=self.colors['surface'])

        items_list_frame.bind(
            "<Configure>", lambda e: items_canvas.configure(scrollregion=items_canvas.bbox("all"))
        )
        items_canvas.create_window((0, 0), window=items_list_frame, anchor="nw")
        items_canvas.configure(yscrollcommand=items_scrollbar.set)
        
        items_canvas.pack(side="left", fill="both", expand=True)
        items_scrollbar.pack(side="right", fill="y")
        
        # Populate order items
        for item in self.cart_items:
            item_row = tk.Frame(items_list_frame, bg=self.colors['surface'])
            item_row.pack(fill="x", pady=2)
            tk.Label(item_row, text=f"{item['name']} x{item['quantity']}",
                     bg=self.colors['surface'], font=self.fonts['body']).pack(side="left")
            tk.Label(item_row, text=f"¥{item['price'] * item['quantity']:.2f}",
                     bg=self.colors['surface'], font=self.fonts['body']).pack(side="right")
        
        ttk.Separator(left_frame, orient='horizontal').pack(fill='x', pady=10, side="bottom")

        # Right: payment options
        right_frame = tk.Frame(main_frame, bg=self.colors['surface'], padx=15, pady=15)
        right_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        tk.Label(right_frame, text="Payment Method", font=self.fonts['heading'],
                 bg=self.colors['surface'], fg=self.colors['text_primary']).pack(anchor="w", pady=(0, 10))
        
        # Payment buttons
        payment_methods = [
            ("Credit Card", "💳", self.colors['info']),
            ("Alipay", "支付宝", self.colors['info']),
            ("WeChat Pay", "微信", self.colors['success']),
            ("Cash", "💵", self.colors['warning'])
        ]
        
        for method, icon, color in payment_methods:
            btn = tk.Button(right_frame, text=f" {icon} {method} ",
                           font=self.fonts['body'],
                           bg=color, fg=self.colors['white'],
                           bd=0, cursor="hand2", width=20,
                           command=lambda m=method: self.process_payment(dialog, m))
            btn.pack(fill="x", pady=8, ipady=10)
        
        # Bottom: Total amount and cancel button
        bottom_frame = tk.Frame(dialog, bg=self.colors['background'], padx=20, pady=10)
        bottom_frame.pack(fill="x", side="bottom")

        total_checkout_label = tk.Label(bottom_frame, text=f"Total: ¥ {self.total_amount:.2f}",
                                       font=self.fonts['title'],
                                       bg=self.colors['background'], fg=self.colors['primary'])
        total_checkout_label.pack(side="left")
        
        cancel_btn = tk.Button(bottom_frame, text="Cancel",
                              font=self.fonts['body'],
                              bg=self.colors['text_secondary'], fg=self.colors['white'],
                              bd=0, cursor="hand2", command=dialog.destroy)
        cancel_btn.pack(side="right", padx=10, ipady=8)

    def process_payment(self, dialog, payment_method):
        """Process the payment"""
        # Disable all payment buttons to prevent multiple clicks
        self._disable_payment_buttons(dialog)
        
        # Display processing animation/message
        processing_label = tk.Label(dialog, text=f"Processing {payment_method} payment...",
                                    font=self.fonts['body'], bg=self.colors['background'])
        processing_label.place(relx=0.5, rely=0.5, anchor="center")

        # Simulate payment processing in a separate thread
        def _do_payment():
            import time, random
            time.sleep(random.uniform(1.5, 3.0)) # Simulate network delay
            
            # On success
            if random.random() > 0.1: # 90% success rate
                order_data = {
                    "table_id": self.current_table,
                    "items": self.cart_items,
                    "total_amount": self.total_amount,
                    "payment_method": payment_method,
                    "status": "Completed"
                }
                # Use data_manager to add the order
                order_id = data_manager.add_order(order_data)
                
                # Update UI on the main thread
                dialog.after(0, self._handle_payment_success, dialog, order_id, payment_method)
            # On failure
            else:
                dialog.after(0, self._handle_payment_error, dialog, "Payment gateway timeout")
            
            # Remove processing message
            dialog.after(0, processing_label.destroy)

        threading.Thread(target=_do_payment, daemon=True).start()

    def _disable_payment_buttons(self, widget):
        """Recursively disable all buttons in a widget."""
        for child in widget.winfo_children():
            if isinstance(child, tk.Button):
                child.config(state="disabled", bg=self.colors['text_secondary'])
            else:
                self._disable_payment_buttons(child)

    def _handle_payment_success(self, dialog, order_id, payment_method):
        """Handle successful payment UI updates."""
        def close_and_clean():
            dialog.destroy()
            self.clear_cart()
            # Notify other modules
            self._safe_notify_modules(order_id)
            
        success_msg = f"Payment Successful!\nOrder ID: {order_id}\nMethod: {payment_method}"
        
        # Show a confirmation dialog
        confirm_dialog = tk.Toplevel(self.parent_frame)
        confirm_dialog.title("Success")
        confirm_dialog.geometry("350x200")
        confirm_dialog.transient(self.parent_frame)
        confirm_dialog.grab_set()
        
        main_frame = tk.Frame(confirm_dialog, bg=self.colors['surface'], padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)
        
        icon_label = tk.Label(main_frame, text="✅", font=('Segoe UI Emoji', 40), bg=self.colors['surface'])
        icon_label.pack()
        
        tk.Label(main_frame, text=success_msg, font=self.fonts['body'], justify='center', bg=self.colors['surface']).pack(pady=10)
        
        ok_button = tk.Button(main_frame, text="OK", command=close_and_clean,
                              bg=self.colors['success'], fg='white', font=self.fonts['body'], bd=0, padx=20, pady=8)
        ok_button.pack(pady=10)
        
        dialog.destroy() # Close the original checkout dialog

    def _handle_payment_error(self, dialog, error):
        """Handle payment error UI updates."""
        messagebox.showerror("Payment Failed", f"An error occurred: {error}.\nPlease try again.", parent=dialog)
        # Re-enable payment buttons
        self._enable_payment_buttons(dialog)
        
    def _enable_payment_buttons(self, widget):
        """Recursively re-enable payment buttons."""
        payment_methods_map = {
            "Credit Card": self.colors['info'],
            "Alipay": self.colors['info'],
            "WeChat Pay": self.colors['success'],
            "Cash": self.colors['warning']
        }
        for child in widget.winfo_children():
            if isinstance(child, tk.Button):
                button_text = child.cget("text").strip()
                for method, color in payment_methods_map.items():
                    if method in button_text:
                        child.config(state="normal", bg=color)
                        break
                else: # For Cancel button
                    child.config(state="normal")
            else:
                self._enable_payment_buttons(child)
                
    def _safe_notify_modules(self, order_id):
        """Safely notify other modules about the new order."""
        try:
            # Notify the order module
            if hasattr(self.order_module, 'notify_order_created'):
                print(f"Sales module: Notifying order module about new order {order_id}")
                # Call in the main thread to avoid Tkinter issues
                self.parent_frame.after(100, self.order_module.notify_order_created, order_id)
            else:
                print("Sales module: Order module not available or doesn't have notify_order_created method.")
                
            # Notify the inventory module
            if hasattr(self.inventory_module, 'notify_order_created'):
                print(f"Sales module: Notifying inventory module about new order {order_id}")
                # Call in the main thread
                self.parent_frame.after(100, self.inventory_module.notify_order_created, order_id)
            else:
                print("Sales module: Inventory module not available or doesn't have notify_order_created method.")
                
        except Exception as e:
            print(f"Error notifying other modules: {e}")
            
    # Method to be called by other modules (e.g., Data Manager)
    def notify_order_created(self, order_id):
        """
        Public method that can be called by other modules to notify this module
        that an order has been created.
        In the sales module, this might be used to update table status, but
        for now, we'll just print a confirmation.
        """
        print(f"✅ Sales module received confirmation for order: {order_id}")

    def clear_cart(self):
        """Clear all items from the cart"""
        self.cart_items.clear()
        self.update_cart_display()
        
    def show_add_success_feedback(self, meal_name):
        """Show brief feedback when an item is added to the cart."""
        feedback_label = tk.Label(self.main_frame, text=f"'{meal_name}' added to cart",
                                  bg=self.colors['success'], fg=self.colors['white'],
                                  font=self.fonts['body'], padx=20, pady=10)
        feedback_label.place(relx=0.5, rely=0.95, anchor="center")
        feedback_label.after(2000, feedback_label.destroy)

    def refresh_meals_data(self):
        """Refresh meal data and update the display."""
        print("Sales module: Refreshing meals data...")
        self.meals_data = self.load_meals_data()
        self.categories = list(set(meal.get('category', 'Other') for meal in self.meals_data))
        self.display_meals()
        
    def check_meal_inventory(self, meal):
        """Check if there is enough inventory to make a meal."""
        # If inventory module is not available, assume there is enough stock
        if not self.inventory_module or not hasattr(self.inventory_module, 'get_inventory_status_for_meal'):
            return True
            
        try:
            # Check inventory status for the given meal
            # This requires the inventory module to have a specific method.
            is_sufficient, _ = self.inventory_module.get_inventory_status_for_meal(meal['name'])
            return is_sufficient
        except Exception as e:
            # If there's an error (e.g., recipe not found), assume it's not available
            print(f"Could not check inventory for {meal.get('name', 'Unknown Meal')}: {e}")
            return False
