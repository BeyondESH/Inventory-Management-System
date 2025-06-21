#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modern Customer Management Module
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, List, Any, Optional
import datetime
import json

# Import data management center
try:
    from ..utils.data_manager import data_manager
except ImportError:
    try:
        from data_manager import data_manager
    except ImportError:
        # Mock data manager
        class MockDataManager:
            def get_customers(self):
                return []
            def register_module(self, module_type, instance):
                pass
            def add_customer(self, data):
                return "CUST_NEW"
            def update_customer(self, cust_id, data):
                return True
            def delete_customer(self, cust_id):
                return True
        data_manager = MockDataManager()

class ModernCustomerModule:
    def __init__(self, parent_frame, title_frame):
        self.parent_frame = parent_frame
        self.title_frame = title_frame
        
        # Register with data management center
        data_manager.register_module('customer', self)
        
        # Modern color scheme
        self.colors = {
            'primary': '#3498DB',      # Primary
            'secondary': '#2ECC71',    # Secondary
            'accent': '#F1C40F',       # Accent
            'background': '#F8F9FA',   # Background
            'surface': '#FFFFFF',      # Card background
            'text_primary': '#2D3436', # Main text
            'text_secondary': '#636E72', # Secondary text
            'border': '#E0E0E0',       # Border
            'success': '#27AE60',      # Success
            'warning': '#F39C12',      # Warning
            'error': '#E74C3C',        # Error
            'card_shadow': '#F0F0F0',  # Card shadow
            'white': '#FFFFFF',        # White
            'info': '#3498DB',         # Info
            'danger': '#E74C3C'        # Danger
        }
        
        # Font configuration
        self.fonts = {
            'title': ('Segoe UI', 20, 'bold'),
            'heading': ('Segoe UI', 16, 'bold'),
            'subheading': ('Segoe UI', 14, 'bold'),
            'body': ('Segoe UI', 12),
            'small': ('Segoe UI', 10),
            'button': ('Segoe UI', 11, 'bold')
        }
        
        self.main_frame = None
        self.customer_data = [] # Lazy loading
        self.customer_tree = None
        self.stats_labels = {}

    def load_customer_data(self):
        """Load customer data from the data manager"""
        try:
            customers = data_manager.get_customers()
            if not customers:
                return self.get_default_customers()
            
            # Process data for UI compatibility
            formatted_customers = []
            for cust in customers:
                formatted_customers.append({
                    'id': cust.get('customer_id', cust.get('id')),
                    'name': f"{cust.get('first_name', '')} {cust.get('last_name', '')}".strip(),
                    'phone': cust.get('customer_phone', cust.get('phone', '')),
                    'address': cust.get('customer_address', cust.get('address', '')),
                    'email': cust.get('customer_email', cust.get('email', '')),
                    'total_orders': cust.get('total_orders', 0),
                    'total_amount': cust.get('total_amount', 0.0)
                })
            return formatted_customers
        except Exception as e:
            print(f"Failed to load customer data: {e}")
            return self.get_default_customers()
            
    def get_default_customers(self):
        """Return default sample customer data"""
        return [
            {"id": "CUST001", "name": "John Smith", "phone": "138-0000-1234", "address": "123 Main St, Anytown", "email": "john.s@example.com", "total_orders": 15, "total_amount": 1580.0},
            {"id": "CUST002", "name": "Jane Doe", "phone": "139-0000-5678", "address": "456 Oak Ave, Somecity", "email": "jane.d@example.com", "total_orders": 8, "total_amount": 890.0},
            {"id": "CUST003", "name": "Mike Johnson", "phone": "136-0000-9012", "address": "789 Pine Ln, Yourtown", "email": "mike.j@example.com", "total_orders": 12, "total_amount": 1250.0}
        ]

    def show(self):
        """Show the customer management module"""
        self.customer_data = self.load_customer_data()
        self.clear_frames()
        self.update_title()
        self.create_main_interface()

    def clear_frames(self):
        """Clear all widgets from the parent and title frames."""
        for widget in self.parent_frame.winfo_children():
            widget.destroy()
        for widget in self.title_frame.winfo_children():
            widget.destroy()

    def update_title(self):
        """Update the title bar."""
        title_frame = tk.Frame(self.title_frame, bg=self.colors['surface'])
        title_frame.pack(fill="both", expand=True)

        left_frame = tk.Frame(title_frame, bg=self.colors['surface'])
        left_frame.pack(side="left", padx=30, pady=20)

        tk.Label(left_frame, text="👥", font=('Segoe UI Emoji', 22), 
                 bg=self.colors['surface'], fg=self.colors['primary']).pack(side="left", padx=(0, 10))
        tk.Label(left_frame, text="Customer Management", font=self.fonts['title'], 
                 bg=self.colors['surface'], fg=self.colors['text_primary']).pack(side="left")

        right_frame = tk.Frame(title_frame, bg=self.colors['surface'])
        right_frame.pack(side="right", padx=30, pady=20)
        
        add_btn = tk.Button(right_frame, text="Add Customer", font=self.fonts['button'],
                            bg=self.colors['primary'], fg=self.colors['white'], bd=0,
                            cursor="hand2", padx=20, pady=8, command=self.add_customer)
        add_btn.pack(side='right', padx=5)

    def create_main_interface(self):
        """Create the main customer management interface"""
        self.main_frame = tk.Frame(self.parent_frame, bg=self.colors['background'])
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.create_customer_stats(self.main_frame)
        self.create_customer_list(self.main_frame)

    def create_customer_stats(self, parent):
        """Create the statistics cards area"""
        stats_frame = tk.Frame(parent, bg=self.colors['background'])
        stats_frame.pack(fill="x", pady=(0, 20))

        total_customers = len(self.customer_data)
        total_orders = sum(c.get('total_orders', 0) for c in self.customer_data)
        total_revenue = sum(c.get('total_amount', 0) for c in self.customer_data)
        avg_spend = total_revenue / total_customers if total_customers > 0 else 0

        stats = [
            {"title": "Total Customers", "value": f"{total_customers}", "icon": "👥"},
            {"title": "Total Orders", "value": f"{total_orders}", "icon": "🧾"},
            {"title": "Total Revenue", "value": f"${total_revenue:,.2f}", "icon": "💰"},
            {"title": "Avg. Spend", "value": f"${avg_spend:,.2f}", "icon": "💲"}
        ]

        for i, stat in enumerate(stats):
            stats_frame.grid_columnconfigure(i, weight=1)
            card = tk.Frame(stats_frame, bg=self.colors['surface'], relief="flat", bd=0)
            card.grid(row=0, column=i, padx=10, sticky="ew")

            icon_label = tk.Label(card, text=stat["icon"], font=('Segoe UI Emoji', 24),
                                  bg=self.colors['surface'], fg=self.colors['primary'])
            icon_label.pack(side="left", padx=20, pady=20)
            
            text_frame = tk.Frame(card, bg=self.colors['surface'])
            text_frame.pack(side="left", pady=20)
            
            value_label = tk.Label(text_frame, text=stat["value"], font=self.fonts['heading'],
                                   bg=self.colors['surface'], fg=self.colors['text_primary'])
            value_label.pack(anchor="w")
            
            title_label = tk.Label(text_frame, text=stat["title"], font=self.fonts['body'],
                                   bg=self.colors['surface'], fg=self.colors['text_secondary'])
            title_label.pack(anchor="w")
            self.stats_labels[stat['title']] = value_label

    def create_customer_list(self, parent):
        """Create the customer list view"""
        list_container = tk.Frame(parent, bg=self.colors['surface'])
        list_container.pack(fill="both", expand=True)

        list_header = tk.Frame(list_container, bg=self.colors['surface'])
        list_header.pack(fill="x", padx=20, pady=(15, 10))

        tk.Label(list_header, text="Customer List", font=self.fonts['heading'],
                 bg=self.colors['surface'], fg=self.colors['text_primary']).pack(side="left")
        
        refresh_btn = tk.Button(list_header, text="🔄 Refresh", font=self.fonts['small'],
                                bg=self.colors['secondary'], fg=self.colors['white'], bd=0,
                                cursor="hand2", padx=15, pady=5, command=self.refresh_customer_data)
        refresh_btn.pack(side="right")
        
        # Treeview
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background=self.colors['surface'], foreground=self.colors['text_primary'],
                        fieldbackground=self.colors['surface'], rowheight=30, font=self.fonts['body'])
        style.configure("Treeview.Heading", font=self.fonts['button'], background=self.colors['background'], 
                        foreground=self.colors['text_primary'], relief="flat")
        style.map("Treeview.Heading", background=[('active', self.colors['border'])])
        style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})]) # Remove borders

        cols = ("ID", "Name", "Phone", "Email", "Orders", "Total Spend")
        self.customer_tree = ttk.Treeview(list_container, columns=cols, show='headings', style="Treeview")

        for col in cols:
            self.customer_tree.heading(col, text=col)
            self.customer_tree.column(col, width=150, anchor='w')

        self.customer_tree.column("ID", width=80, anchor='center')
        self.customer_tree.column("Orders", width=80, anchor='center')
        self.customer_tree.column("Total Spend", width=120, anchor='e')

        self.customer_tree.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        self.customer_tree.bind("<Double-1>", lambda e: self.edit_customer())
        self.create_context_menu()
        self.refresh_customer_list()

    def create_context_menu(self):
        """Create a right-click context menu for the treeview."""
        self.context_menu = tk.Menu(self.customer_tree, tearoff=0, font=self.fonts['body'],
                                    bg=self.colors['surface'], fg=self.colors['text_primary'])
        self.context_menu.add_command(label="✏️ Edit Selected Customer", command=self.edit_customer)
        self.context_menu.add_command(label="🗑️ Delete Selected Customer", command=self.delete_customer)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="View Orders (Not Implemented)")

        self.customer_tree.bind("<Button-3>", self.show_context_menu)

    def show_context_menu(self, event):
        """Show the context menu on right-click."""
        row_id = self.customer_tree.identify_row(event.y)
        if row_id:
            self.customer_tree.selection_set(row_id)
            self.context_menu.post(event.x_root, event.y_root)

    def refresh_customer_data(self):
        """Refresh both data and UI display"""
        self.customer_data = self.load_customer_data()
        self.refresh_customer_list()
        self.update_stats()

    def update_stats(self):
        """Update statistics cards"""
        total_customers = len(self.customer_data)
        total_orders = sum(c.get('total_orders', 0) for c in self.customer_data)
        total_revenue = sum(c.get('total_amount', 0) for c in self.customer_data)
        avg_spend = total_revenue / total_customers if total_customers > 0 else 0
        
        self.stats_labels["Total Customers"].config(text=f"{total_customers}")
        self.stats_labels["Total Orders"].config(text=f"{total_orders}")
        self.stats_labels["Total Revenue"].config(text=f"${total_revenue:,.2f}")
        self.stats_labels["Avg. Spend"].config(text=f"${avg_spend:,.2f}")

    def refresh_customer_list(self):
        """Refresh only the customer list display"""
        if self.customer_tree:
            for item in self.customer_tree.get_children():
                self.customer_tree.delete(item)
            
            for customer in self.customer_data:
                values = (
                    customer.get('id', ''),
                    customer.get('name', ''),
                    customer.get('phone', ''),
                    customer.get('email', ''),
                    customer.get('total_orders', 0),
                    f"${customer.get('total_amount', 0):,.2f}"
                )
                self.customer_tree.insert("", "end", values=values, tags=(customer.get('id'),))
    
    def add_customer(self):
        """Add a new customer"""
        CustomerDialog(self.main_frame, "Add New Customer", colors=self.colors, fonts=self.fonts,
                       callback=self.refresh_customer_data)

    def edit_customer(self):
        """Edit the selected customer"""
        selected_item = self.customer_tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a customer to edit.", parent=self.main_frame)
            return
        
        customer_id = self.customer_tree.item(selected_item[0])['tags'][0]
        customer_data = next((c for c in self.customer_data if c['id'] == customer_id), None)
        
        if customer_data:
            CustomerDialog(self.main_frame, "Edit Customer", customer_data, self.colors, self.fonts,
                           callback=self.refresh_customer_data)

    def delete_customer(self):
        """Delete the selected customer"""
        selected_item = self.customer_tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a customer to delete.", parent=self.main_frame)
            return
            
        customer_id = self.customer_tree.item(selected_item[0])['tags'][0]
        customer_name = self.customer_tree.item(selected_item[0])['values'][1]

        if messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete customer '{customer_name}'?\nThis action cannot be undone.", parent=self.main_frame):
            try:
                if data_manager.delete_customer(customer_id):
                    messagebox.showinfo("Success", f"Customer '{customer_name}' deleted successfully.", parent=self.main_frame)
                    self.refresh_customer_data()
                else:
                    messagebox.showerror("Error", "Failed to delete customer. Please check logs.", parent=self.main_frame)
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}", parent=self.main_frame)
    
    def export_customers(self):
        """Export customer data (placeholder)"""
        messagebox.showinfo("Export", "Export functionality is not yet implemented.", parent=self.main_frame)

class CustomerDialog(tk.Toplevel):
    def __init__(self, parent, title, customer_data=None, colors=None, fonts=None, callback=None):
        super().__init__(parent)
        self.title(title)
        self.customer_data = customer_data
        self.colors = colors
        self.fonts = fonts
        self.callback = callback
        
        self.geometry("450x400")
        self.configure(bg=self.colors['background'])
        self.transient(parent)
        self.grab_set()
        
        self.create_widgets()
        self.load_data()
        self.center_window()
        
    def create_widgets(self):
        """Create widgets for the dialog"""
        main_frame = tk.Frame(self, bg=self.colors['background'], padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)

        tk.Label(main_frame, text=self.title(), font=self.fonts['heading'],
                 bg=self.colors['background'], fg=self.colors['text_primary']).pack(pady=(0, 15))

        self.entries = {}
        fields = ["Name", "Phone", "Email", "Address"]
        for field in fields:
            frame = tk.Frame(main_frame, bg=self.colors['background'])
            frame.pack(fill='x', pady=5)
            tk.Label(frame, text=f"{field}:", font=self.fonts['body'], 
                     bg=self.colors['background'], fg=self.colors['text_secondary'], width=8, anchor='w').pack(side='left')
            
            entry_var = tk.StringVar()
            entry = ttk.Entry(frame, textvariable=entry_var, font=self.fonts['body'], width=40)
            entry.pack(side='left', fill='x', expand=True)
            self.entries[field.lower()] = entry_var

        button_frame = tk.Frame(main_frame, bg=self.colors['background'])
        button_frame.pack(fill='x', pady=(20, 0))
        
        save_btn = tk.Button(button_frame, text="Save", font=self.fonts['button'],
                             bg=self.colors['success'], fg=self.colors['white'], bd=0,
                             padx=20, pady=8, cursor="hand2", command=self.save)
        save_btn.pack(side='right', padx=5)

        cancel_btn = tk.Button(button_frame, text="Cancel", font=self.fonts['button'],
                               bg=self.colors['text_secondary'], fg=self.colors['white'], bd=0,
                               padx=20, pady=8, cursor="hand2", command=self.destroy)
        cancel_btn.pack(side='right', padx=5)

    def load_data(self):
        """Load customer data into the form if editing"""
        if self.customer_data:
            self.entries['name'].set(self.customer_data.get('name', ''))
            self.entries['phone'].set(self.customer_data.get('phone', ''))
            self.entries['email'].set(self.customer_data.get('email', ''))
            self.entries['address'].set(self.customer_data.get('address', ''))

    def center_window(self):
        """Center the dialog on the parent window"""
        self.update_idletasks()
        parent_x = self.master.winfo_rootx()
        parent_y = self.master.winfo_rooty()
        parent_w = self.master.winfo_width()
        parent_h = self.master.winfo_height()
        dialog_w = self.winfo_width()
        dialog_h = self.winfo_height()
        x = parent_x + (parent_w - dialog_w) // 2
        y = parent_y + (parent_h - dialog_h) // 2
        self.geometry(f'+{x}+{y}')

    def save(self):
        """Save the customer data"""
        name = self.entries['name'].get().strip()
        phone = self.entries['phone'].get().strip()
        if not name or not phone:
            messagebox.showerror("Validation Error", "Name and Phone are required.", parent=self)
            return

        data = {
            'first_name': name.split(' ')[0] if ' ' in name else name,
            'last_name': ' '.join(name.split(' ')[1:]) if ' ' in name else '',
            'customer_phone': phone,
            'customer_email': self.entries['email'].get().strip(),
            'customer_address': self.entries['address'].get().strip()
        }
        
        try:
            if self.customer_data: # Update
                success = data_manager.update_customer(self.customer_data['id'], data)
                msg = f"Customer '{name}' updated successfully."
            else: # Add
                success = data_manager.add_customer(data)
                msg = f"Customer '{name}' added successfully."

            if success:
                messagebox.showinfo("Success", msg, parent=self)
                if self.callback:
                    self.callback()
                self.destroy()
            else:
                messagebox.showerror("Database Error", "Failed to save customer data.", parent=self)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}", parent=self)
