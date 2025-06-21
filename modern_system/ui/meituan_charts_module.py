#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modern Charts Module - Data Visualization
"""

import tkinter as tk
from tkinter import ttk
from typing import Dict, List, Any
import datetime

# Import data management center
try:
    from ..utils.data_manager import data_manager
except ImportError:
    try:
        from data_manager import data_manager
    except ImportError:
        # Mock data manager
        class MockDataManager:
            def get_dashboard_stats(self):
                return {'today_revenue': 2580, 'today_orders': 25, 'low_stock_count': 3, 'total_customers': 156}
            def get_daily_revenue(self, date_str):
                return 1000 + int(date_str.split('-')[2]) * 100 # Mock data
            def get_orders(self):
                return []
        data_manager = MockDataManager()

class ModernChartsModule:
    def __init__(self, parent_frame, title_frame):
        self.parent_frame = parent_frame
        self.title_frame = title_frame
        
        self.colors = {
            'primary': '#3498DB', 'secondary': '#2ECC71', 'success': '#27AE60',
            'warning': '#F1C40F', 'danger': '#E74C3C', 'info': '#3498DB',
            'background': '#F8F9FA', 'surface': '#FFFFFF', 'text_primary': '#2D3436',
            'text_secondary': '#636E72', 'border': '#E1E8ED', 'white': '#FFFFFF'
        }
        self.fonts = {
            'title': ('Segoe UI', 20, 'bold'), 'heading': ('Segoe UI', 16, 'bold'),
            'body': ('Segoe UI', 12), 'small': ('Segoe UI', 10),
            'button': ('Segoe UI', 11, 'bold')
        }
        
        self.main_frame = None
        
    def show(self):
        """Show the charts interface."""
        self.clear_frames()
        self.update_title()
        
        self.main_frame = tk.Frame(self.parent_frame, bg=self.colors['background'])
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.create_charts_area()

    def clear_frames(self):
        """Clear all widgets from the main frames."""
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
        tk.Label(left_frame, text="📊", font=('Segoe UI Emoji', 22), 
                 bg=self.colors['surface'], fg=self.colors['primary']).pack(side="left", padx=(0, 10))
        tk.Label(left_frame, text="Dashboard", font=self.fonts['title'], 
                 bg=self.colors['surface'], fg=self.colors['text_primary']).pack(side="left")
        
        right_frame = tk.Frame(title_frame, bg=self.colors['surface'])
        right_frame.pack(side="right", padx=30, pady=20)
        
        refresh_btn = tk.Button(right_frame, text="Refresh", font=self.fonts['button'],
                               bg=self.colors['secondary'], fg=self.colors['white'], bd=0,
                               cursor="hand2", padx=20, pady=8, command=self.refresh_charts)
        refresh_btn.pack(side='right', padx=5)

    def create_charts_area(self):
        """Create the area for displaying charts."""
        charts_container = tk.Frame(self.main_frame, bg=self.colors['background'])
        charts_container.pack(fill="both", expand=True)
        
        top_frame = tk.Frame(charts_container, bg=self.colors['background'])
        top_frame.pack(fill="x", expand=True, pady=(0, 10))

        left_frame = tk.Frame(top_frame, bg=self.colors['surface'])
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        right_frame = tk.Frame(top_frame, bg=self.colors['surface'])
        right_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        self.create_sales_chart(left_frame)
        self.create_product_chart(right_frame)

        bottom_frame = tk.Frame(charts_container, bg=self.colors['surface'])
        bottom_frame.pack(fill="both", expand=True, pady=(10, 0))
        self.create_revenue_chart(bottom_frame)
        
    def create_sales_chart(self, parent):
        """Create the sales trend chart."""
        tk.Label(parent, text="Weekly Sales Trend", font=self.fonts['heading'], bg=self.colors['surface'], fg=self.colors['text_primary']).pack(pady=10, padx=20, anchor='w')
        
        chart_frame = tk.Frame(parent, bg=self.colors['surface'])
        chart_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        chart_data = self.get_real_sales_data()
        max_sales = max(item[2] for item in chart_data) if chart_data else 1

        for day, amount_str, amount_val in chart_data:
            row_frame = tk.Frame(chart_frame, bg=self.colors['surface'])
            row_frame.pack(fill="x", pady=4)
            
            tk.Label(row_frame, text=day, width=10, font=self.fonts['body'], bg=self.colors['surface'], fg=self.colors['text_primary'], anchor='w').pack(side="left")
            
            progress_container = tk.Frame(row_frame, bg='#ECF0F1', height=20)
            progress_container.pack(side="left", fill="x", expand=True, padx=10)
            
            percentage = amount_val / max_sales if max_sales > 0 else 0
            bar = tk.Frame(progress_container, bg=self.colors['primary'], height=20)
            bar.place(relwidth=percentage, relheight=1)

            tk.Label(row_frame, text=amount_str, width=10, font=self.fonts['body'], bg=self.colors['surface'], fg=self.colors['text_secondary'], anchor='e').pack(side="right")
            
    def create_product_chart(self, parent):
        """Create the product analysis chart (pie chart style)."""
        tk.Label(parent, text="Hot Selling Products", font=self.fonts['heading'], bg=self.colors['surface'], fg=self.colors['text_primary']).pack(pady=10, padx=20, anchor='w')
        
        chart_frame = tk.Frame(parent, bg=self.colors['surface'])
        chart_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        product_data = self.get_real_product_data()
        
        colors = ['#2ECC71', '#3498DB', '#9B59B6', '#E67E22', '#F1C40F']
        
        for i, (product, count, percentage) in enumerate(product_data):
            color = colors[i % len(colors)]
            row_frame = tk.Frame(chart_frame, bg=self.colors['surface'])
            row_frame.pack(fill="x", pady=4)
            
            tk.Label(row_frame, text="●", font=('Segoe UI', 16), bg=self.colors['surface'], fg=color).pack(side="left", padx=(0, 10))
            tk.Label(row_frame, text=f"{product}", font=self.fonts['body'], bg=self.colors['surface'], fg=self.colors['text_primary'], anchor='w').pack(side="left", fill='x', expand=True)
            tk.Label(row_frame, text=f"{count} orders ({percentage:.0f}%)", font=self.fonts['body'], bg=self.colors['surface'], fg=self.colors['text_secondary']).pack(side="right")
            
    def create_revenue_chart(self, parent):
        """Create the monthly revenue bar chart."""
        tk.Label(parent, text="Monthly Revenue Statistics", font=self.fonts['heading'], bg=self.colors['surface'], fg=self.colors['text_primary']).pack(pady=10, padx=20, anchor='w')
        
        chart_frame = tk.Frame(parent, bg=self.colors['surface'])
        chart_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        revenue_data = self.get_real_revenue_data()
        max_revenue = max(rev for _, rev in revenue_data) if revenue_data else 1
        
        for i, (month, revenue) in enumerate(revenue_data):
            chart_frame.grid_columnconfigure(i, weight=1)
            month_frame = tk.Frame(chart_frame, bg=self.colors['surface'])
            month_frame.grid(row=0, column=i, sticky="nswe", padx=5)
            
            bar_height_percentage = revenue / max_revenue if max_revenue > 0 else 0
            
            tk.Label(month_frame, text=f"${revenue/1000:.1f}K", font=self.fonts['small'], bg=self.colors['surface'], fg=self.colors['text_secondary']).pack(side="top", pady=2)
            
            bar_container = tk.Frame(month_frame, bg='#ECF0F1', height=100)
            bar_container.pack(side="top", fill='x', expand=True)
            bar = tk.Frame(bar_container, bg=self.colors['secondary'])
            bar.place(relwidth=1, relheight=bar_height_percentage, rely=1.0, anchor='sw')

            tk.Label(month_frame, text=month, font=self.fonts['body'], bg=self.colors['surface'], fg=self.colors['text_primary']).pack(side="bottom", pady=5)
    
    def get_real_sales_data(self):
        """Get sales data for the last 7 days from financial records."""
        try:
            today = datetime.datetime.now()
            daily_revenue = { (today - datetime.timedelta(days=i)).strftime('%Y-%m-%d'): 0 for i in range(7) }

            finance_records = data_manager.get_finance_records()
            for record in finance_records:
                if record.get('type') == 'Income' and record.get('date') in daily_revenue:
                    daily_revenue[record['date']] += record.get('amount', 0)
            
            chart_data = []
            for i in range(6, -1, -1):
                date = today - datetime.timedelta(days=i)
                date_str = date.strftime('%Y-%m-%d')
                revenue = daily_revenue.get(date_str, 0)
                weekday = date.strftime('%A')
                chart_data.append((weekday, f"${revenue:,.2f}", revenue))
            return chart_data
        except Exception as e:
            print(f"Error getting sales data: {e}")
            return [("Mon", "$0", 0), ("Tue", "$0", 0), ("Wed", "$0", 0),
                    ("Thu", "$0", 0), ("Fri", "$0", 0), ("Sat", "$0", 0), ("Sun", "$0", 0)]
            
    def get_real_product_data(self):
        """Get hot product data from the data manager."""
        try:
            orders = data_manager.get_orders()
            product_sales = {}
            total_items = 0
            for order in orders:
                for item in order.get('items', []):
                    name = item.get('name')
                    quantity = item.get('quantity', 1)
                    product_sales[name] = product_sales.get(name, 0) + quantity
                    total_items += quantity
            
            if not product_sales: return []
            
            # Sort by sales count and take top 5
            sorted_products = sorted(product_sales.items(), key=lambda x: x[1], reverse=True)[:5]
            
            chart_data = []
            for name, count in sorted_products:
                percentage = (count / total_items) * 100 if total_items > 0 else 0
                chart_data.append((name, count, percentage))
            return chart_data
        except Exception as e:
            print(f"Error getting product data: {e}")
            return [("Beef Noodles", 50, 40), ("Fried Rice", 30, 24), ("Burger", 20, 16), ("Fries", 15, 12), ("Coke", 10, 8)]

    def get_real_revenue_data(self):
        """Get monthly revenue data for the last 6 months from financial records."""
        try:
            today = datetime.date.today()
            
            # Correctly determine the last 6 months
            first_month = (today.replace(day=1) - datetime.timedelta(days=5*30)).replace(day=1)
            monthly_revenue = {}
            current_month = first_month
            for _ in range(12): # Iterate over a year to be safe
                if current_month > today:
                    break
                month_key = current_month.strftime('%Y-%m')
                monthly_revenue[month_key] = 0
                next_month = (current_month.replace(day=28) + datetime.timedelta(days=4)).replace(day=1)
                current_month = next_month

            finance_records = data_manager.get_finance_records()
            for record in finance_records:
                if record.get('type') == 'Income':
                    record_date_str = record.get('date')
                    if record_date_str:
                        record_month_key = datetime.datetime.strptime(record_date_str, '%Y-%m-%d').strftime('%Y-%m')
                        if record_month_key in monthly_revenue:
                            monthly_revenue[record_month_key] += record.get('amount', 0)

            # Get the last 6 months from the calculated data
            sorted_months = sorted(monthly_revenue.keys())[-6:]
            
            chart_data = []
            for month_key in sorted_months:
                month_name = datetime.datetime.strptime(month_key, '%Y-%m').strftime('%b')
                revenue = monthly_revenue.get(month_key, 0)
                chart_data.append((month_name, revenue))

            return chart_data
        except Exception as e:
            print(f"Error getting revenue data: {e}")
            return [('Jan', 0), ('Feb', 0), ('Mar', 0), ('Apr', 0), ('May', 0), ('Jun', 0)]
            
    def refresh_charts(self):
        """Refresh all charts with the latest data."""
        if self.main_frame:
            for widget in self.main_frame.winfo_children():
                widget.destroy()
            self.create_charts_area()
