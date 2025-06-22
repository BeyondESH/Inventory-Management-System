#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modern Finance Management Module
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
        # Mock data manager
        class MockDataManager:
            def get_finance_records(self):
                return []
            def register_module(self, module_type, instance):
                pass
        data_manager = MockDataManager()

class ModernFinanceModule:
    def __init__(self, parent_frame, title_frame, order_module=None, employee_module=None):
        self.parent_frame = parent_frame
        self.title_frame = title_frame
        self.order_module = order_module
        self.employee_module = employee_module
        
        # Register to data management center
        data_manager.register_module('finance', self)
        
        # Fixed costs data file path
        self.fixed_costs_file = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), 
            'data', 
            'fixed_costs.json'
        )
        
        # Modern color scheme
        self.colors = {
            'primary': '#27AE60', 'secondary': '#2980B9', 'success': '#2ECC71',
            'warning': '#F1C40F', 'danger': '#E74C3C', 'info': '#3498DB',
            'background': '#F8F9FA', 'surface': '#FFFFFF', 'text_primary': '#2D3436',
            'text_secondary': '#636E72', 'border': '#E1E8ED', 'white': '#FFFFFF'
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
        self.finance_records = []
        self.fixed_costs = []
        self.stats_labels = {}
        self.notebook = None
        self.search_var = None
        self.date_filter_var = None
        self.type_filter_var = None

    def show(self):
        """Show the finance management interface."""
        self.clear_frames()
        self.update_title()

        if self.main_frame:
            self.main_frame.destroy()
        
        self.main_frame = tk.Frame(self.parent_frame, bg=self.colors['background'])
        self.main_frame.pack(fill="both", expand=True)
        
        self.search_var = tk.StringVar(self.main_frame)
        self.date_filter_var = tk.StringVar(self.main_frame, value="All")
        self.type_filter_var = tk.StringVar(self.main_frame, value="All")
        
        self.finance_records = self.load_finance_records()
        self.fixed_costs = self.load_fixed_costs()
        
        self.create_finance_overview()
        self.create_finance_tabs()
        self.update_overview_cards()
        self.refresh_records_list()
        self.refresh_fixed_costs_list()

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

        tk.Label(left_frame, text="💼", font=('Segoe UI Emoji', 22), 
                 bg=self.colors['surface'], fg=self.colors['primary']).pack(side="left", padx=(0, 10))
        tk.Label(left_frame, text="Finance Management", font=self.fonts['title'], 
                 bg=self.colors['surface'], fg=self.colors['text_primary']).pack(side="left")

        right_frame = tk.Frame(title_frame, bg=self.colors['surface'])
        right_frame.pack(side="right", padx=30, pady=20)
        
        export_btn = tk.Button(right_frame, text="Export Report", font=self.fonts['button'],
                               bg=self.colors['secondary'], fg=self.colors['white'], bd=0,
                               cursor="hand2", padx=20, pady=8, command=self.export_finance_report)
        export_btn.pack(side='right', padx=5)

    def create_finance_overview(self):
        """Create the overview statistics cards."""
        overview_frame = tk.Frame(self.main_frame, bg=self.colors['background'])
        overview_frame.pack(fill="x", pady=(0, 20))
        
        stats = [
            {"title": "Total Revenue", "icon": "💰", "color": self.colors['success']},
            {"title": "Total Expense", "icon": "💸", "color": self.colors['danger']},
            {"title": "Net Profit", "icon": "📈", "color": self.colors['primary']},
            {"title": "Avg. Daily Profit", "icon": "📅", "color": self.colors['info']}
        ]

        for i, stat in enumerate(stats):
            overview_frame.grid_columnconfigure(i, weight=1)
            card = tk.Frame(overview_frame, bg=self.colors['surface'])
            card.grid(row=0, column=i, padx=10, sticky="ew")
            
            tk.Label(card, text=stat['icon'], font=('Segoe UI Emoji', 24), bg=self.colors['surface'], fg=stat['color']).pack(side="left", padx=20, pady=20)
            text_frame = tk.Frame(card, bg=self.colors['surface'])
            text_frame.pack(side="left", pady=20, anchor='w')
            
            value_label = tk.Label(text_frame, text="$0.00", font=self.fonts['heading'], bg=self.colors['surface'], fg=self.colors['text_primary'])
            value_label.pack(anchor="w")
            tk.Label(text_frame, text=stat['title'], font=self.fonts['body'], bg=self.colors['surface'], fg=self.colors['text_secondary']).pack(anchor="w")
            self.stats_labels[stat['title']] = value_label

    def update_overview_cards(self):
        """Calculate and update the values on the overview cards."""
        total_revenue = sum(r['amount'] for r in self.finance_records if r['type'] == 'Income')
        total_expense = sum(r['amount'] for r in self.finance_records if r['type'] == 'Expense')
        net_profit = total_revenue - total_expense
        
        if self.finance_records:
            try:
                # 处理不同的日期格式
                start_dates = []
                for r in self.finance_records:
                    date_str = r['date']
                    try:
                        # 尝试解析 ISO 格式 (2025-06-22T14:39:22)
                        if 'T' in date_str:
                            date_obj = datetime.datetime.fromisoformat(date_str.split('T')[0])
                        else:
                            # 尝试解析简单日期格式 (2025-06-22)
                            date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d')
                        start_dates.append(date_obj)
                    except (ValueError, AttributeError):
                        # 如果解析失败，使用当前日期
                        start_dates.append(datetime.datetime.now())
                
                if start_dates:
                    start_date = min(start_dates)
                    days = (datetime.datetime.now() - start_date).days + 1
                    avg_daily_profit = net_profit / days if days > 0 else 0
                else:
                    avg_daily_profit = 0
            except Exception as e:
                print(f"计算平均日利润时出错: {e}")
                avg_daily_profit = 0
        else:
            avg_daily_profit = 0

        self.stats_labels["Total Revenue"].config(text=f"${total_revenue:,.2f}")
        self.stats_labels["Total Expense"].config(text=f"${total_expense:,.2f}")
        self.stats_labels["Net Profit"].config(text=f"${net_profit:,.2f}")
        self.stats_labels["Avg. Daily Profit"].config(text=f"${avg_daily_profit:,.2f}")

    def create_finance_tabs(self):
        """Create the notebook with tabs for different finance sections."""
        style = ttk.Style()
        style.configure('TNotebook.Tab', font=self.fonts['button'], padding=[20, 10], background=self.colors['background'], borderwidth=0)
        style.map('TNotebook.Tab', background=[('selected', self.colors['primary'])], foreground=[('selected', self.colors['white'])])
        style.configure('TNotebook', background=self.colors['background'], borderwidth=0)
        
        self.notebook = ttk.Notebook(self.main_frame, style='TNotebook')
        self.notebook.pack(fill="both", expand=True)
        
        self.records_frame = tk.Frame(self.notebook, bg=self.colors['surface'])
        self.fixed_costs_frame = tk.Frame(self.notebook, bg=self.colors['surface'])
        
        self.notebook.add(self.records_frame, text="Financial Records")
        self.notebook.add(self.fixed_costs_frame, text="Fixed Costs")
        
        self.create_finance_records_tab(self.records_frame)
        self.create_fixed_costs_tab(self.fixed_costs_frame)

    def create_finance_records_tab(self, parent):
        """Create the content for the 'Financial Records' tab."""
        tk.Label(parent, text="All Financial Records", font=self.fonts['heading'], bg=self.colors['surface'], fg=self.colors['text_primary']).pack(pady=20, padx=20, anchor='w')
        
        btn_frame = tk.Frame(parent, bg=self.colors['surface'])
        btn_frame.pack(fill='x', padx=20, pady=(0, 10))
        tk.Button(btn_frame, text="Add Income", command=self.add_income_record, font=self.fonts['button'], bg=self.colors['success'], fg='white', bd=0, padx=15, pady=8).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Add Expense", command=self.add_expense_record, font=self.fonts['button'], bg=self.colors['danger'], fg='white', bd=0, padx=15, pady=8).pack(side='left', padx=5)

        cols = ("Date", "Type", "Amount", "Category", "Description", "Recorded By")
        self.records_tree = self.create_treeview(parent, cols, [100, 80, 100, 120, 250, 120])
        self.records_tree.bind("<Double-1>", lambda e: self.edit_record(self.records_tree))
    
    def create_fixed_costs_tab(self, parent):
        """Create the content for the 'Fixed Costs' tab."""
        tk.Label(parent, text="Recurring Fixed Costs", font=self.fonts['heading'], bg=self.colors['surface'], fg=self.colors['text_primary']).pack(pady=20, padx=20, anchor='w')

        btn_frame = tk.Frame(parent, bg=self.colors['surface'])
        btn_frame.pack(fill='x', padx=20, pady=(0, 10))
        tk.Button(btn_frame, text="Add Fixed Cost", command=self.add_fixed_cost, font=self.fonts['button'], bg=self.colors['primary'], fg='white', bd=0, padx=15, pady=8).pack(side='left', padx=5)

        cols = ("Item", "Amount", "Category", "Frequency", "Next Due Date", "Status")
        self.costs_tree = self.create_treeview(parent, cols, [150, 100, 120, 100, 120, 100])
        self.costs_tree.bind("<Double-1>", lambda e: self.edit_record(self.costs_tree, is_fixed_cost=True))

    def create_treeview(self, parent, columns, widths):
        """Helper to create a styled Treeview."""
        style = ttk.Style()
        style.configure("Treeview", rowheight=30, font=self.fonts['body'], background=self.colors['surface'], fieldbackground=self.colors['surface'])
        style.configure("Treeview.Heading", font=self.fonts['button'], background=self.colors['background'], padding=5)
        style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])

        tree_frame = tk.Frame(parent)
        tree_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings')
        for i, col in enumerate(columns):
            tree.heading(col, text=col)
            tree.column(col, width=widths[i], anchor='w')
        
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        
        tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")
        return tree

    def refresh_records_list(self):
        """Refresh the financial records treeview."""
        for item in self.records_tree.get_children():
            self.records_tree.delete(item)
        for record in sorted(self.finance_records, key=lambda x: x['date'], reverse=True):
            values = (record['date'], record['type'], f"${record['amount']:.2f}", record['category'], record['description'], record.get('recorded_by', 'N/A'))
            tag = record['id']
            self.records_tree.insert("", "end", values=values, tags=(tag,))
            
    def refresh_fixed_costs_list(self):
        """Refresh the fixed costs treeview."""
        for item in self.costs_tree.get_children():
            self.costs_tree.delete(item)
        for cost in sorted(self.fixed_costs, key=lambda x: x['next_due_date']):
            values = (cost['item'], f"${cost['amount']:.2f}", cost['category'], cost['frequency'], cost['next_due_date'], cost['status'])
            tag = cost['id']
            self.costs_tree.insert("", "end", values=values, tags=(tag,))

    def load_finance_records(self):
        """Load financial records from data manager."""
        try:
            # 获取数据管理器中的财务记录
            raw_records = data_manager.get_financial_records() or []
            
            # 转换记录格式以匹配财务模块期望的格式
            converted_records = []
            for record in raw_records:
                converted_record = {
                    'id': record.get('id', ''),
                    'date': record.get('date', '').split('T')[0] if 'T' in record.get('date', '') else record.get('date', ''),
                    'type': 'Income' if record.get('type') == 'revenue' else 'Expense' if record.get('type') == 'cost' else record.get('type', ''),
                    'amount': abs(float(record.get('amount', 0))),  # 确保金额为正数
                    'category': 'Sales' if record.get('type') == 'revenue' else 'Cost' if record.get('type') == 'cost' else 'Other',
                    'description': record.get('description', ''),
                    'recorded_by': 'System'
                }
                converted_records.append(converted_record)
            
            return converted_records if converted_records else self.get_default_records()
        except Exception as e:
            print(f"Error loading finance records: {e}")
            return self.get_default_records()
            
    def get_default_records(self):
        """Get default financial records."""
        return [
            {'id': 'FIN001', 'date': '2023-10-26', 'type': 'Income', 'amount': 1500.0, 'category': 'Daily Sales', 'description': 'Restaurant sales', 'recorded_by': 'System'},
            {'id': 'FIN002', 'date': '2023-10-26', 'type': 'Expense', 'amount': 300.0, 'category': 'Ingredients', 'description': 'Vegetable purchase', 'recorded_by': 'Admin'},
        ]

    def load_fixed_costs(self):
        """Load fixed costs from JSON file."""
        try:
            if os.path.exists(self.fixed_costs_file):
                with open(self.fixed_costs_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return self.get_default_costs()
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error loading fixed costs file: {e}")
            return self.get_default_costs()
            
    def get_default_costs(self):
        """Get default fixed costs."""
        return [
            {'id': 'FC001', 'item': 'Rent', 'amount': 5000.0, 'category': 'Premises', 'frequency': 'Monthly', 'next_due_date': '2023-11-01', 'status': 'Upcoming'},
            {'id': 'FC002', 'item': 'Staff Salaries', 'amount': 15000.0, 'category': 'HR', 'frequency': 'Monthly', 'next_due_date': '2023-11-15', 'status': 'Upcoming'},
        ]

    def save_fixed_costs(self):
        """Save fixed costs to JSON file."""
        try:
            with open(self.fixed_costs_file, 'w', encoding='utf-8') as f:
                json.dump(self.fixed_costs, f, indent=4)
        except IOError as e:
            messagebox.showerror("Error", f"Failed to save fixed costs: {e}", parent=self.main_frame)
            
    def add_income_record(self):
        self.show_record_dialog("Add Income Record", is_income=True)
        
    def add_expense_record(self):
        self.show_record_dialog("Add Expense Record", is_income=False)
        
    def add_fixed_cost(self):
        self.show_record_dialog("Add Fixed Cost", is_fixed_cost=True)
        
    def edit_record(self, tree, is_fixed_cost=False):
        """Edit a selected record from a treeview."""
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select an item to edit.", parent=self.main_frame)
            return
        
        record_id = tree.item(selected_item[0])['tags'][0]
        
        if is_fixed_cost:
            record_data = next((c for c in self.fixed_costs if c['id'] == record_id), None)
            title = "Edit Fixed Cost"
        else:
            record_data = next((r for r in self.finance_records if r['id'] == record_id), None)
            title = "Edit Financial Record"
        
        if record_data:
            self.show_record_dialog(title, record_data, is_fixed_cost)
            
    def show_record_dialog(self, title, record_data=None, is_income=False, is_fixed_cost=False):
        """Generic dialog for adding/editing records."""
        FinanceDialog(self.main_frame, title, self.colors, self.fonts, self.refresh_all_data, 
                      record_data, is_income, is_fixed_cost)
                      
    def refresh_all_data(self):
        """Refresh all data and UI components."""
        self.finance_records = self.load_finance_records()
        self.fixed_costs = self.load_fixed_costs()
        self.update_overview_cards()
        self.refresh_records_list()
        self.refresh_fixed_costs_list()

    def refresh_data(self):
        """刷新财务数据（被数据管理器调用）"""
        try:
            self.refresh_all_data()
            print("✅ 财务模块数据已刷新")
        except Exception as e:
            print(f"❌ 财务模块数据刷新失败: {e}")

    def export_finance_report(self):
        """Placeholder for export functionality."""
        messagebox.showinfo("Export", "Export functionality not yet implemented.", parent=self.main_frame)

class FinanceDialog(tk.Toplevel):
    def __init__(self, parent, title, colors, fonts, callback, record_data=None, is_income=False, is_fixed_cost=False):
        super().__init__(parent)
        self.title(title)
        self.colors = colors
        self.fonts = fonts
        self.callback = callback
        self.record_data = record_data
        self.is_income = is_income
        self.is_fixed_cost = is_fixed_cost

        self.geometry("450x450")
        self.configure(bg=self.colors['background'])
        self.transient(parent)
        self.grab_set()

        self.create_widgets()
        if self.record_data:
            self.load_data()
        self.center_window()
        
    def create_widgets(self):
        main_frame = tk.Frame(self, bg=self.colors['background'], padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)
        tk.Label(main_frame, text=self.title(), font=self.fonts['heading'], bg=self.colors['background']).pack(pady=(0, 15))

        self.entries = {}
        if self.is_fixed_cost:
            fields = ["Item", "Amount", "Category", "Frequency", "Next Due Date"]
            categories = ["Premises", "HR", "Utilities", "Software", "Marketing", "Other"]
            frequencies = ["Daily", "Weekly", "Monthly", "Quarterly", "Annually"]
            self.create_form_field(main_frame, "Item")
            self.create_form_field(main_frame, "Amount")
            self.create_form_field(main_frame, "Category", "combobox", categories)
            self.create_form_field(main_frame, "Frequency", "combobox", frequencies)
            self.create_form_field(main_frame, "Next Due Date", "date")
        else:
            fields = ["Date", "Amount", "Category", "Description"]
            categories = ["Sales", "Service", "Other"] if self.is_income else ["Ingredients", "Wages", "Rent", "Utilities", "Marketing", "Other"]
            self.create_form_field(main_frame, "Date", "date")
            self.create_form_field(main_frame, "Amount")
            self.create_form_field(main_frame, "Category", "combobox", categories)
            self.create_form_field(main_frame, "Description")

        btn_frame = tk.Frame(main_frame, bg=self.colors['background'])
        btn_frame.pack(fill='x', pady=(20, 0))
        tk.Button(btn_frame, text="Save", command=self.save, font=self.fonts['button'], bg=self.colors['success'], fg='white', bd=0, padx=20, pady=8).pack(side='right')
        tk.Button(btn_frame, text="Cancel", command=self.destroy, font=self.fonts['button'], bg=self.colors['text_secondary'], fg='white', bd=0, padx=20, pady=8).pack(side='right', padx=10)

    def create_form_field(self, parent, label, field_type="entry", options=None):
        frame = tk.Frame(parent, bg=self.colors['background'])
        frame.pack(fill='x', pady=5)
        tk.Label(frame, text=f"{label}:", font=self.fonts['body'], bg=self.colors['background'], width=12, anchor='w').pack(side='left')
        
        var = tk.StringVar()
        if field_type == "combobox":
            widget = ttk.Combobox(frame, textvariable=var, values=options, font=self.fonts['body'], state="readonly")
        else: # entry or date
            widget = ttk.Entry(frame, textvariable=var, font=self.fonts['body'])
            if field_type == "date" and not self.record_data:
                var.set(datetime.date.today().strftime('%Y-%m-%d'))

        widget.pack(side='left', fill='x', expand=True)
        self.entries[label.lower().replace(" ", "_")] = var

    def load_data(self):
        """Load existing record data into the form."""
        for key, var in self.entries.items():
            if key in self.record_data:
                var.set(self.record_data[key])
    
    def center_window(self):
        self.update_idletasks()
        x = self.master.winfo_rootx() + (self.master.winfo_width() - self.winfo_width()) // 2
        y = self.master.winfo_rooty() + (self.master.winfo_height() - self.winfo_height()) // 2
        self.geometry(f'+{x}+{y}')

    def save(self):
        """Save the record data."""
        data = {key: var.get() for key, var in self.entries.items()}
        try:
            data['amount'] = float(data.get('amount', 0))
        except ValueError:
            messagebox.showerror("Validation Error", "Amount must be a valid number.", parent=self)
            return

        try:
            if self.is_fixed_cost:
                if self.record_data: # Update
                    index = next(i for i, c in enumerate(self.master.master.fixed_costs) if c['id'] == self.record_data['id'])
                    self.master.master.fixed_costs[index].update(data)
                else: # Add
                    data['id'] = f"FC{int(datetime.datetime.now().timestamp())}"
                    data['status'] = 'Upcoming'
                    self.master.master.fixed_costs.append(data)
                self.master.master.save_fixed_costs()
            else: # Financial Record
                data['type'] = 'Income' if self.is_income else 'Expense'
                if self.record_data: # Update
                    success = data_manager.update_finance_record(self.record_data['id'], data)
                else: # Add
                    data['recorded_by'] = 'Admin' # Placeholder
                    success = data_manager.add_finance_record(data)
                if not success:
                    raise Exception("Data manager failed to save the record.")

            messagebox.showinfo("Success", "Record saved successfully.", parent=self)
            if self.callback:
                self.callback()
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save record: {e}", parent=self)
