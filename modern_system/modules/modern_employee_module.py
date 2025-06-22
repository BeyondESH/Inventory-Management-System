#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modern Employee Management Module
Based on modern takeout platform style employee management interface
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from typing import Dict, List, Any, Optional
import datetime
import json
import os

class ModernEmployeeModule:
    def __init__(self, parent_frame, title_frame):
        self.parent_frame = parent_frame
        self.title_frame = title_frame
        
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
        
        # Department color scheme
        self.department_colors = {
            'Front Office': '#3498DB',
            'Kitchen': '#E67E22',
            'Procurement': '#2ECC71',
            'Finance': '#9B59B6',
            'Management': '#E74C3C',
            'Delivery': '#1ABC9C'
        }
        
        # Employee status color scheme
        self.status_colors = {
            'Employed': '#2ECC71',
            'Probation': '#F39C12',
            'Resigned': '#95A5A6',
            'On Leave': '#3498DB'
        }
        
        # Employee data
        self.employee_data = [
            {
                "id": 1001,
                "name": "John Smith",
                "position": "Front Office Manager",
                "department": "Front Office",
                "phone": "138****1234",
                "email": "john.smith@company.com",
                "hire_date": "2023-01-15",
                "salary": 8000.0,
                "status": "Employed",
                "birthday": "1990-05-20",
                "address": "123 Main Street, Chaoyang District, Beijing",
                "emergency_contact": "Ms. Li 139****5678",
                "performance": 85
            },
            {
                "id": 1002,
                "name": "Jane Lee",
                "position": "Head Chef",
                "department": "Kitchen",
                "phone": "139****5678",
                "email": "jane.lee@company.com",
                "hire_date": "2022-08-20",
                "salary": 9500.0,
                "status": "Employed",
                "birthday": "1988-12-10",
                "address": "88 Business Road, Haidian District, Beijing",
                "emergency_contact": "Mr. Wang 137****9012",
                "performance": 92
            },
            {
                "id": 1003,
                "name": "Mike Wang",
                "position": "Waiter",
                "department": "Front Office",
                "phone": "136****9012",
                "email": "mike.wang@company.com",
                "hire_date": "2023-03-10",
                "salary": 4500.0,
                "status": "Employed",
                "birthday": "1995-08-15",
                "address": "66 Old Alley, Xicheng District, Beijing",
                "emergency_contact": "Ms. Zhang 135****1234",
                "performance": 78
            },
            {
                "id": 1004,
                "name": "Leo Zhao",
                "position": "Purchaser",
                "department": "Procurement",
                "phone": "137****3456",
                "email": "leo.zhao@company.com",
                "hire_date": "2023-05-22",
                "salary": 5500.0,
                "status": "Probation",
                "birthday": "1992-03-25",
                "address": "East Avenue, Dongcheng District, Beijing",
                "emergency_contact": "Mr. Qian 138****7890",
                "performance": 72
            },
            {
                "id": 1005,
                "name": "David Qian",
                "position": "Finance Specialist",
                "department": "Finance",
                "phone": "135****7890",
                "email": "david.qian@company.com",
                "hire_date": "2022-12-01",
                "salary": 6000.0,
                "status": "Resigned",
                "birthday": "1989-11-08",
                "address": "Fengtai Road, Fengtai District, Beijing",
                "emergency_contact": "Ms. Sun 132****4567",
                "performance": 65
            },
            {
                "id": 1006,
                "name": "Sunny Sun",
                "position": "Delivery Staff",
                "department": "Delivery",
                "phone": "132****4567",
                "email": "sunny.sun@company.com",
                "hire_date": "2023-06-01",
                "salary": 4000.0,
                "status": "Employed",
                "birthday": "1996-01-30",
                "address": "Daxing Community, Daxing District, Beijing",
                "emergency_contact": "Mr. Zhou 186****1234",
                "performance": 88
            }
        ]        # Department list
        self.departments = ["Front Office", "Kitchen", "Procurement", "Finance", "Management", "Delivery"]
        
        self.selected_employee = None
        self.current_filter = "All"
        self.search_keyword = ""
        self.stats_frame = None
    
    def create_stats_card(self, parent, title, value, subtitle, color):
        """Create statistics card"""
        # Outer container
        container_frame = tk.Frame(parent, bg=self.colors['background'])
        container_frame.pack(side='left', padx=10, pady=5, fill='both', expand=True)
        
        # Card body
        card_frame = tk.Frame(container_frame, bg=self.colors['card'], relief='flat', bd=1,
                             highlightbackground=self.colors['border'], highlightthickness=1)
        card_frame.pack(fill='both', expand=True)
        
        # Set card size
        card_frame.configure(height=120)
        container_frame.pack_propagate(False)
        
        # Icon/value area
        icon_frame = tk.Frame(card_frame, bg=color, width=80, height=80)
        icon_frame.pack(side='left', padx=15, pady=20)
        icon_frame.pack_propagate(False)
        
        # Value label
        value_label = tk.Label(icon_frame, text=str(value), 
                              font=('Segoe UI', 16, 'bold'),
                              bg=color, fg=self.colors['white'])
        value_label.place(relx=0.5, rely=0.5, anchor='center')
        
        # Info area
        info_frame = tk.Frame(card_frame, bg=self.colors['card'])
        info_frame.pack(side='left', padx=(10, 15), pady=20, fill='both', expand=True)
        
        # Title
        title_label = tk.Label(info_frame, text=title, 
                              font=('Segoe UI', 12, 'bold'),
                              bg=self.colors['card'], fg=self.colors['text'])
        title_label.pack(anchor='w', pady=(10, 5))
        
        # Subtitle
        subtitle_label = tk.Label(info_frame, text=subtitle, 
                                 font=('Segoe UI', 10),
                                 bg=self.colors['card'], fg=self.colors['text_light'])
        subtitle_label.pack(anchor='w')
        
        return card_frame
    
    def create_employee_card(self, parent, employee):
        """Create employee card"""
        card_frame = tk.Frame(parent, bg=self.colors['card'], relief='flat', bd=1,
                             highlightbackground=self.colors['border'], highlightthickness=1)
        card_frame.pack(fill='x', padx=5, pady=5)
        
        # Card header
        header_frame = tk.Frame(card_frame, bg=self.colors['card'])
        header_frame.pack(fill='x', padx=20, pady=(15, 10))
        
        # Employee basic information
        info_frame = tk.Frame(header_frame, bg=self.colors['card'])
        info_frame.pack(side='left', fill='both', expand=True)
        
        # Employee name and ID
        name_frame = tk.Frame(info_frame, bg=self.colors['card'])
        name_frame.pack(fill='x')
        
        name_label = tk.Label(name_frame, text=employee['name'], 
                             font=('Segoe UI', 14, 'bold'),
                             bg=self.colors['card'], fg=self.colors['text'])
        name_label.pack(side='left')
        
        id_label = tk.Label(name_frame, text=f"ID: {employee['id']}", 
                           font=('Segoe UI', 10),
                           bg=self.colors['card'], fg=self.colors['text_light'])
        id_label.pack(side='left', padx=(10, 0))
        
        # Position information
        position_frame = tk.Frame(info_frame, bg=self.colors['card'])
        position_frame.pack(fill='x', pady=(5, 0))
        
        position_label = tk.Label(position_frame, text=f"🎯 {employee['position']}", 
                                 font=('Segoe UI', 11, 'bold'),
                                 bg=self.colors['card'], fg=self.colors['primary'])
        position_label.pack(side='left')
        
        # Contact information
        contact_frame = tk.Frame(info_frame, bg=self.colors['card'])
        contact_frame.pack(fill='x', pady=(5, 0))
        
        phone_label = tk.Label(contact_frame, text=f"📞 {employee['phone']}", 
                              font=('Segoe UI', 10),
                              bg=self.colors['card'], fg=self.colors['text'])
        phone_label.pack(side='left')
        
        email_label = tk.Label(contact_frame, text=f"📧 {employee['email']}", 
                              font=('Segoe UI', 10),
                              bg=self.colors['card'], fg=self.colors['text'])
        email_label.pack(side='left', padx=(20, 0))
        
        # Right side status and department
        right_frame = tk.Frame(header_frame, bg=self.colors['card'])
        right_frame.pack(side='right')
        
        # Department label
        dept_color = self.department_colors.get(employee['department'], self.colors['info'])
        dept_frame = tk.Frame(right_frame, bg=dept_color, padx=10, pady=5)
        dept_frame.pack(pady=(0, 5))
        
        dept_label = tk.Label(dept_frame, text=employee['department'], 
                             font=('Segoe UI', 10, 'bold'),
                             bg=dept_color, fg=self.colors['white'])
        dept_label.pack()
        
        # Status label
        status_color = self.status_colors.get(employee['status'], self.colors['info'])
        status_frame = tk.Frame(right_frame, bg=status_color, padx=10, pady=5)
        status_frame.pack()
        
        status_label = tk.Label(status_frame, text=employee['status'], 
                               font=('Segoe UI', 10, 'bold'),
                               bg=status_color, fg=self.colors['white'])
        status_label.pack()
        
        # Employee detailed information
        details_frame = tk.Frame(card_frame, bg=self.colors['background'], padx=15, pady=10)
        details_frame.pack(fill='x', padx=20, pady=(0, 10))
        
        # Work information
        work_info_frame = tk.Frame(details_frame, bg=self.colors['background'])
        work_info_frame.pack(side='left', fill='x', expand=True)
        
        work_items = [
            ("Hire Date", employee['hire_date']),
            ("Salary", f"¥{employee['salary']:.0f}"),
            ("Performance", f"{employee['performance']} points")
        ]
        
        for i, (label, value) in enumerate(work_items):
            item_frame = tk.Frame(work_info_frame, bg=self.colors['background'])
            item_frame.pack(side='left', padx=(0, 20))
            
            tk.Label(item_frame, text=label, font=('Segoe UI', 9),
                    bg=self.colors['background'], fg=self.colors['text_light']).pack()
            
            tk.Label(item_frame, text=value, font=('Segoe UI', 11, 'bold'),
                    bg=self.colors['background'], fg=self.colors['text']).pack()
        
        # Performance bar
        performance_frame = tk.Frame(details_frame, bg=self.colors['background'])
        performance_frame.pack(side='right', padx=(20, 0))
        
        tk.Label(performance_frame, text="Performance", font=('Segoe UI', 9),
                bg=self.colors['background'], fg=self.colors['text_light']).pack()
        
        # Performance progress bar
        progress_bg = tk.Frame(performance_frame, bg=self.colors['light'], width=100, height=6)
        progress_bg.pack(pady=2)
        progress_bg.pack_propagate(False)
        
        performance_pct = employee['performance'] / 100
        progress_width = int(100 * performance_pct)
        
        # Select color based on performance score
        if employee['performance'] >= 90:
            progress_color = self.colors['success']
        elif employee['performance'] >= 80:
            progress_color = self.colors['info']
        elif employee['performance'] >= 70:
            progress_color = self.colors['warning']
        else:
            progress_color = self.colors['danger']
        
        progress_bar = tk.Frame(progress_bg, bg=progress_color, width=progress_width, height=6)
        progress_bar.place(x=0, y=0)
        
        # Action buttons
        actions_frame = tk.Frame(card_frame, bg=self.colors['card'])
        actions_frame.pack(fill='x', padx=20, pady=(0, 15))
        
        # View details button
        detail_btn = tk.Button(actions_frame, text="View Details", 
                              font=('Segoe UI', 9),
                              bg=self.colors['info'], fg=self.colors['white'],
                              bd=0, padx=15, pady=5, cursor='hand2',
                              command=lambda: self.show_employee_detail(employee))
        detail_btn.pack(side='right', padx=5)
        
        # Edit button
        edit_btn = tk.Button(actions_frame, text="Edit", 
                            font=('Segoe UI', 9),
                            bg=self.colors['warning'], fg=self.colors['white'],
                            bd=0, padx=15, pady=5, cursor='hand2',
                            command=lambda: self.edit_employee(employee))
        edit_btn.pack(side='right', padx=5)
        
        # Delete button (not shown for resigned employees)
        if employee['status'] != 'Resigned':
            delete_btn = tk.Button(actions_frame, text="Resign", 
                                  font=('Segoe UI', 9),
                                  bg=self.colors['danger'], fg=self.colors['white'],
                                  bd=0, padx=15, pady=5, cursor='hand2',
                                  command=lambda: self.resign_employee(employee['id']))
            delete_btn.pack(side='right', padx=5)
        
        return card_frame
    
    def show_employee_detail(self, employee):
        """Show employee details"""
        detail_window = tk.Toplevel()
        detail_window.title(f"Employee Details - {employee['name']}")
        detail_window.geometry("600x750")
        detail_window.configure(bg=self.colors['background'])
        detail_window.resizable(False, False)
        
        # Title
        title_frame = tk.Frame(detail_window, bg=self.colors['primary'], height=60)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text=f"Employee Details - {employee['name']}", 
                              font=('Segoe UI', 16, 'bold'),
                              bg=self.colors['primary'], fg=self.colors['white'])
        title_label.pack(expand=True)
        
        # Details content
        content_frame = tk.Frame(detail_window, bg=self.colors['background'])
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Basic information card
        basic_frame = tk.Frame(content_frame, bg=self.colors['card'], padx=20, pady=15)
        basic_frame.pack(fill='x', pady=(0, 15))
        
        tk.Label(basic_frame, text="Basic Information", font=('Segoe UI', 14, 'bold'),
                bg=self.colors['card'], fg=self.colors['text']).pack(anchor='w', pady=(0, 10))
        
        basic_info = [
            ("ID", employee['id']),
            ("Name", employee['name']),
            ("Birthday", employee['birthday']),
            ("Phone", employee['phone']),
            ("Email", employee['email']),
            ("Address", employee['address']),
            ("Emergency Contact", employee['emergency_contact'])
        ]
        
        for label, value in basic_info:
            info_row = tk.Frame(basic_frame, bg=self.colors['card'])
            info_row.pack(fill='x', pady=2)
            
            tk.Label(info_row, text=f"{label}:", font=('Segoe UI', 10),
                    bg=self.colors['card'], fg=self.colors['text_light'], width=12, anchor='w').pack(side='left')
            
            tk.Label(info_row, text=str(value), font=('Segoe UI', 10),
                    bg=self.colors['card'], fg=self.colors['text'], anchor='w').pack(side='left', fill='x', expand=True)
        
        # Work information card
        work_frame = tk.Frame(content_frame, bg=self.colors['card'], padx=20, pady=15)
        work_frame.pack(fill='x', pady=(0, 15))
        
        tk.Label(work_frame, text="Work Information", font=('Segoe UI', 14, 'bold'),
                bg=self.colors['card'], fg=self.colors['text']).pack(anchor='w', pady=(0, 10))
        
        work_info = [
            ("Position", employee['position']),
            ("Department", employee['department']),
            ("Hire Date", employee['hire_date']),
            ("Employee Status", employee['status']),
            ("Salary", f"¥{employee['salary']:.2f}"),
            ("Performance", f"{employee['performance']} points")
        ]
        
        for label, value in work_info:
            info_row = tk.Frame(work_frame, bg=self.colors['card'])
            info_row.pack(fill='x', pady=2)
            
            tk.Label(info_row, text=f"{label}:", font=('Segoe UI', 10),
                    bg=self.colors['card'], fg=self.colors['text_light'], width=12, anchor='w').pack(side='left')
            
            tk.Label(info_row, text=str(value), font=('Segoe UI', 10),
                    bg=self.colors['card'], fg=self.colors['text'], anchor='w').pack(side='left', fill='x', expand=True)
        
        # Performance details
        performance_frame = tk.Frame(content_frame, bg=self.colors['card'], padx=20, pady=15)
        performance_frame.pack(fill='x', pady=(0, 15))
        
        tk.Label(performance_frame, text="Performance Details", font=('Segoe UI', 14, 'bold'),
                bg=self.colors['card'], fg=self.colors['text']).pack(anchor='w', pady=(0, 10))
        
        # Work days calculation
        hire_date = datetime.datetime.strptime(employee['hire_date'], '%Y-%m-%d')
        work_days = (datetime.datetime.now() - hire_date).days
        
        # Performance visualization
        perf_visual_frame = tk.Frame(performance_frame, bg=self.colors['background'], padx=15, pady=10)
        perf_visual_frame.pack(fill='x')
        
        # Performance indicators
        perf_items = [
            ("Work Attitude", employee['performance'] - 5),
            ("Work Quality", employee['performance'] + 3),
            ("Team Collaboration", employee['performance'] - 2),
            ("Learning Ability", employee['performance'] + 1)
        ]
        
        for item_name, score in perf_items:
            item_frame = tk.Frame(perf_visual_frame, bg=self.colors['background'])
            item_frame.pack(fill='x', pady=5)
            
            tk.Label(item_frame, text=item_name, font=('Segoe UI', 10),
                    bg=self.colors['background'], fg=self.colors['text'], width=10, anchor='w').pack(side='left')
            
            # Score bar
            score_bg = tk.Frame(item_frame, bg=self.colors['light'], width=200, height=8)
            score_bg.pack(side='left', padx=(10, 0), anchor='w')
            score_bg.pack_propagate(False)
            
            score_pct = max(0, min(100, score)) / 100
            score_width = int(200 * score_pct)
            
            if score >= 90:
                score_color = self.colors['success']
            elif score >= 80:
                score_color = self.colors['info']
            elif score >= 70:
                score_color = self.colors['warning']
            else:
                score_color = self.colors['danger']
            
            score_bar = tk.Frame(score_bg, bg=score_color, width=score_width, height=8)
            score_bar.place(x=0, y=0)
            
            tk.Label(item_frame, text=f"{max(0, min(100, score))} points", font=('Segoe UI', 9),
                    bg=self.colors['background'], fg=self.colors['text']).pack(side='right')
        
        # Work statistics
        stats_text = f"""Employed Days: {work_days} days
Average Work Days per Month: {work_days // max(1, (datetime.datetime.now() - hire_date).days // 30)} days
Department Rank: Top {30}%
Overall Evaluation: {'Excellent' if employee['performance'] >= 90 else 'Good' if employee['performance'] >= 80 else 'Average' if employee['performance'] >= 70 else 'Needs Improvement'}"""
        
        tk.Label(performance_frame, text=stats_text, font=('Segoe UI', 10),
                bg=self.colors['card'], fg=self.colors['text'], justify='left').pack(anchor='w', pady=(10, 0))
        
        # Close button
        tk.Button(content_frame, text="Close", font=('Segoe UI', 10),
                 bg=self.colors['text_light'], fg=self.colors['white'],
                 bd=0, padx=30, pady=8, cursor='hand2',
                 command=detail_window.destroy).pack(pady=10)
    
    def edit_employee(self, employee):
        """Edit employee information"""
        edit_window = tk.Toplevel()
        edit_window.title(f"Edit Employee - {employee['name']}")
        edit_window.geometry("550x800")  # Increase height from 700 to 800
        edit_window.configure(bg=self.colors['background'])
        edit_window.resizable(False, False)
        
        # Title
        title_frame = tk.Frame(edit_window, bg=self.colors['primary'], height=60)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text="Edit Employee Information", 
                              font=('Segoe UI', 16, 'bold'),
                              bg=self.colors['primary'], fg=self.colors['white'])
        title_label.pack(expand=True)
        
        # Form content
        form_frame = tk.Frame(edit_window, bg=self.colors['background'])
        form_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Create scroll area
        canvas = tk.Canvas(form_frame, bg=self.colors['background'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(form_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['background'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Form card
        card_frame = tk.Frame(scrollable_frame, bg=self.colors['card'], padx=20, pady=20)
        card_frame.pack(fill='both', expand=True)
        
        # Form fields
        form_vars = {}
        
        # Basic information
        tk.Label(card_frame, text="Basic Information", font=('Segoe UI', 12, 'bold'),
                bg=self.colors['card'], fg=self.colors['text']).pack(anchor='w', pady=(0, 10))
        
        basic_fields = [
            ("Name", "name", employee['name']),
            ("Phone", "phone", employee['phone']),
            ("Email", "email", employee['email']),
            ("Birthday", "birthday", employee['birthday']),
            ("Address", "address", employee['address']),
            ("Emergency Contact", "emergency_contact", employee['emergency_contact'])
        ]
        
        for label, field, value in basic_fields:
            field_frame = tk.Frame(card_frame, bg=self.colors['card'])
            field_frame.pack(fill='x', pady=5)
            
            tk.Label(field_frame, text=f"{label}:", font=('Segoe UI', 10),
                    bg=self.colors['card'], fg=self.colors['text']).pack(anchor='w', pady=(0, 2))
            
            var = tk.StringVar(edit_window, value=value)
            form_vars[field] = var
            
            entry = tk.Entry(field_frame, textvariable=var, font=('Segoe UI', 10),
                           relief='flat', bd=5, bg=self.colors['light'])
            entry.pack(fill='x')
        
        # Separator
        separator = tk.Frame(card_frame, bg=self.colors['border'], height=1)
        separator.pack(fill='x', pady=20)
        
        # Work information
        tk.Label(card_frame, text="Work Information", font=('Segoe UI', 12, 'bold'),
                bg=self.colors['card'], fg=self.colors['text']).pack(anchor='w', pady=(0, 10))
        
        # Position
        pos_frame = tk.Frame(card_frame, bg=self.colors['card'])
        pos_frame.pack(fill='x', pady=5)
        tk.Label(pos_frame, text="Position:", font=('Segoe UI', 10),
                bg=self.colors['card'], fg=self.colors['text']).pack(anchor='w', pady=(0, 2))
        position_var = tk.StringVar(edit_window, value=employee['position'])
        form_vars['position'] = position_var
        position_entry = tk.Entry(pos_frame, textvariable=position_var, font=('Segoe UI', 10),
                                 relief='flat', bd=5, bg=self.colors['light'])
        position_entry.pack(fill='x')
        
        # Department
        dept_frame = tk.Frame(card_frame, bg=self.colors['card'])
        dept_frame.pack(fill='x', pady=5)
        tk.Label(dept_frame, text="Department:", font=('Segoe UI', 10),
                bg=self.colors['card'], fg=self.colors['text']).pack(anchor='w', pady=(0, 2))
        department_var = tk.StringVar(edit_window, value=employee['department'])
        form_vars['department'] = department_var
        dept_combo = ttk.Combobox(dept_frame, textvariable=department_var, 
                                 values=self.departments, state="readonly", font=('Segoe UI', 10))
        dept_combo.pack(fill='x')
        
        # Hire date
        hire_frame = tk.Frame(card_frame, bg=self.colors['card'])
        hire_frame.pack(fill='x', pady=5)
        tk.Label(hire_frame, text="Hire Date:", font=('Segoe UI', 10),
                bg=self.colors['card'], fg=self.colors['text']).pack(anchor='w', pady=(0, 2))
        hire_var = tk.StringVar(edit_window, value=employee['hire_date'])
        form_vars['hire_date'] = hire_var
        hire_entry = tk.Entry(hire_frame, textvariable=hire_var, font=('Segoe UI', 10),
                             relief='flat', bd=5, bg=self.colors['light'])
        hire_entry.pack(fill='x')
        
        # Salary
        salary_frame = tk.Frame(card_frame, bg=self.colors['card'])
        salary_frame.pack(fill='x', pady=5)
        tk.Label(salary_frame, text="Salary (¥):", font=('Segoe UI', 10),
                bg=self.colors['card'], fg=self.colors['text']).pack(anchor='w', pady=(0, 2))
        salary_var = tk.StringVar(edit_window, value=str(employee['salary']))
        form_vars['salary'] = salary_var
        salary_entry = tk.Entry(salary_frame, textvariable=salary_var, font=('Segoe UI', 10),
                               relief='flat', bd=5, bg=self.colors['light'])
        salary_entry.pack(fill='x')
        
        # Status
        status_frame = tk.Frame(card_frame, bg=self.colors['card'])
        status_frame.pack(fill='x', pady=5)
        tk.Label(status_frame, text="Status:", font=('Segoe UI', 10),
                bg=self.colors['card'], fg=self.colors['text']).pack(anchor='w', pady=(0, 2))
        status_var = tk.StringVar(edit_window, value=employee['status'])
        form_vars['status'] = status_var
        status_combo = ttk.Combobox(status_frame, textvariable=status_var, 
                                   values=["Employed", "Probation", "On Leave", "Resigned"], state="readonly", font=('Segoe UI', 10))
        status_combo.pack(fill='x')
        
        # Performance score
        perf_frame = tk.Frame(card_frame, bg=self.colors['card'])
        perf_frame.pack(fill='x', pady=5)
        tk.Label(perf_frame, text="Performance Score (0-100):", font=('Segoe UI', 10),
                bg=self.colors['card'], fg=self.colors['text']).pack(anchor='w', pady=(0, 2))
        performance_var = tk.StringVar(edit_window, value=str(employee['performance']))
        form_vars['performance'] = performance_var
        perf_entry = tk.Entry(perf_frame, textvariable=performance_var, font=('Segoe UI', 10),
                             relief='flat', bd=5, bg=self.colors['light'])
        perf_entry.pack(fill='x')
        
        # Button area
        button_frame = tk.Frame(card_frame, bg=self.colors['card'])
        button_frame.pack(fill='x', pady=20)
        
        def save_changes():
            try:
                # Verify input
                if not form_vars['name'].get() or not form_vars['phone'].get():
                    messagebox.showerror("Error", "Please fill in employee name and phone number")
                    return
                
                # Verify salary
                try:
                    salary = float(form_vars['salary'].get())
                    if salary < 0:
                        raise ValueError()
                except ValueError:
                    messagebox.showerror("Error", "Please enter a valid salary amount")
                    return
                
                # Verify performance score
                try:
                    performance = int(form_vars['performance'].get())
                    if not 0 <= performance <= 100:
                        raise ValueError()
                except ValueError:
                    messagebox.showerror("Error", "Performance score must be between 0-100")
                    return
                
                # Update employee information
                for i, emp in enumerate(self.employee_data):
                    if emp['id'] == employee['id']:
                        self.employee_data[i].update({
                            'name': form_vars['name'].get(),
                            'phone': form_vars['phone'].get(),
                            'email': form_vars['email'].get(),
                            'birthday': form_vars['birthday'].get(),
                            'address': form_vars['address'].get(),
                            'emergency_contact': form_vars['emergency_contact'].get(),
                            'position': form_vars['position'].get(),
                            'department': form_vars['department'].get(),
                            'hire_date': form_vars['hire_date'].get(),
                            'salary': salary,
                            'status': form_vars['status'].get(),
                            'performance': performance
                        })
                        break
                
                messagebox.showinfo("Success", "Employee information updated")
                edit_window.destroy()
                self.refresh_employee_list()
                
            except Exception as e:
                messagebox.showerror("Error", f"Save failed: {str(e)}")
        
        save_btn = tk.Button(button_frame, text="Save Changes", 
                           font=('Segoe UI', 10, 'bold'),
                           bg=self.colors['primary'], fg=self.colors['white'],
                           bd=0, padx=30, pady=8, cursor='hand2',
                           command=save_changes)
        save_btn.pack(side='right', padx=5)
        
        cancel_btn = tk.Button(button_frame, text="Cancel", 
                             font=('Segoe UI', 10),
                             bg=self.colors['text_light'], fg=self.colors['white'],
                             bd=0, padx=30, pady=8, cursor='hand2',
                             command=edit_window.destroy)
        cancel_btn.pack(side='right', padx=5)
        
        # Layout scroll area
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mouse wheel
        def on_mousewheel(event):
            if canvas.winfo_exists():
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        
        canvas.bind("<MouseWheel>", on_mousewheel)
        scrollable_frame.bind("<MouseWheel>", on_mousewheel)
    
    def resign_employee(self, employee_id):
        """Employee resign"""
        result = messagebox.askyesno("Confirm Resignation", "Are you sure you want to set this employee's status to Resigned?")
        if result:
            for employee in self.employee_data:
                if employee['id'] == employee_id:
                    employee['status'] = 'Resigned'
                    messagebox.showinfo("Success", f"Employee {employee['name']} set to Resigned status")
                    self.refresh_employee_list()
                    break
    
    def add_new_employee(self):
        """Add new employee"""
        add_window = tk.Toplevel()
        add_window.title("Add New Employee")
        add_window.geometry("550x800")  # Increase height from 700 to 800
        add_window.configure(bg=self.colors['background'])
        add_window.resizable(False, False)
        
        # Title
        title_frame = tk.Frame(add_window, bg=self.colors['primary'], height=60)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text="Add New Employee", 
                              font=('Segoe UI', 16, 'bold'),
                              bg=self.colors['primary'], fg=self.colors['white'])
        title_label.pack(expand=True)
        
        # Form content
        form_frame = tk.Frame(add_window, bg=self.colors['background'])
        form_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Create scroll area
        canvas = tk.Canvas(form_frame, bg=self.colors['background'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(form_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['background'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Form card
        card_frame = tk.Frame(scrollable_frame, bg=self.colors['card'], padx=20, pady=20)
        card_frame.pack(fill='both', expand=True)
        
        # Form fields
        form_vars = {}
        
        # Basic information
        tk.Label(card_frame, text="Basic Information", font=('Segoe UI', 12, 'bold'),
                bg=self.colors['card'], fg=self.colors['text']).pack(anchor='w', pady=(0, 10))
        
        basic_fields = [
            ("Name", "name", ""),
            ("Phone", "phone", ""),
            ("Email", "email", ""),
            ("Birthday", "birthday", ""),
            ("Address", "address", ""),
            ("Emergency Contact", "emergency_contact", "")
        ]
        
        for label, field, default in basic_fields:
            field_frame = tk.Frame(card_frame, bg=self.colors['card'])
            field_frame.pack(fill='x', pady=5)
            
            tk.Label(field_frame, text=f"{label}:", font=('Segoe UI', 10),
                    bg=self.colors['card'], fg=self.colors['text']).pack(anchor='w', pady=(0, 2))
            
            var = tk.StringVar(add_window, value=default)
            form_vars[field] = var
            
            entry = tk.Entry(field_frame, textvariable=var, font=('Segoe UI', 10),
                           relief='flat', bd=5, bg=self.colors['light'])
            entry.pack(fill='x')
        
        # Separator
        separator = tk.Frame(card_frame, bg=self.colors['border'], height=1)
        separator.pack(fill='x', pady=20)
        
        # Work information
        tk.Label(card_frame, text="Work Information", font=('Segoe UI', 12, 'bold'),
                bg=self.colors['card'], fg=self.colors['text']).pack(anchor='w', pady=(0, 10))
        
        # Position
        pos_frame = tk.Frame(card_frame, bg=self.colors['card'])
        pos_frame.pack(fill='x', pady=5)
        tk.Label(pos_frame, text="Position:", font=('Segoe UI', 10),
                bg=self.colors['card'], fg=self.colors['text']).pack(anchor='w', pady=(0, 2))
        position_var = tk.StringVar(add_window)
        form_vars['position'] = position_var
        position_entry = tk.Entry(pos_frame, textvariable=position_var, font=('Segoe UI', 10),
                                 relief='flat', bd=5, bg=self.colors['light'])
        position_entry.pack(fill='x')
        
        # Department
        dept_frame = tk.Frame(card_frame, bg=self.colors['card'])
        dept_frame.pack(fill='x', pady=5)
        tk.Label(dept_frame, text="Department:", font=('Segoe UI', 10),
                bg=self.colors['card'], fg=self.colors['text']).pack(anchor='w', pady=(0, 2))
        department_var = tk.StringVar(add_window, value=self.departments[0])
        form_vars['department'] = department_var
        dept_combo = ttk.Combobox(dept_frame, textvariable=department_var, 
                                 values=self.departments, state="readonly", font=('Segoe UI', 10))
        dept_combo.pack(fill='x')
        
        # Hire date
        hire_frame = tk.Frame(card_frame, bg=self.colors['card'])
        hire_frame.pack(fill='x', pady=5)
        tk.Label(hire_frame, text="Hire Date:", font=('Segoe UI', 10),
                bg=self.colors['card'], fg=self.colors['text']).pack(anchor='w', pady=(0, 2))
        hire_var = tk.StringVar(add_window, value=datetime.datetime.now().strftime("%Y-%m-%d"))
        form_vars['hire_date'] = hire_var
        hire_entry = tk.Entry(hire_frame, textvariable=hire_var, font=('Segoe UI', 10),
                             relief='flat', bd=5, bg=self.colors['light'])
        hire_entry.pack(fill='x')
        
        # Salary
        salary_frame = tk.Frame(card_frame, bg=self.colors['card'])
        salary_frame.pack(fill='x', pady=5)
        tk.Label(salary_frame, text="Salary (¥):", font=('Segoe UI', 10),
                bg=self.colors['card'], fg=self.colors['text']).pack(anchor='w', pady=(0, 2))
        salary_var = tk.StringVar(add_window, value="5000")
        form_vars['salary'] = salary_var
        salary_entry = tk.Entry(salary_frame, textvariable=salary_var, font=('Segoe UI', 10),
                               relief='flat', bd=5, bg=self.colors['light'])
        salary_entry.pack(fill='x')
        
        # Button area
        button_frame = tk.Frame(card_frame, bg=self.colors['card'])
        button_frame.pack(fill='x', pady=20)
        
        def save_employee():
            try:
                # Verify input
                if not form_vars['name'].get() or not form_vars['phone'].get():
                    messagebox.showerror("Error", "Please fill in employee name and phone number")
                    return
                
                # Verify salary
                try:
                    salary = float(form_vars['salary'].get())
                    if salary < 0:
                        raise ValueError()
                except ValueError:
                    messagebox.showerror("Error", "Please enter a valid salary amount")
                    return
                
                # Generate new employee ID
                new_id = max([emp['id'] for emp in self.employee_data]) + 1
                
                # Create new employee
                new_employee = {
                    "id": new_id,
                    "name": form_vars['name'].get(),
                    "phone": form_vars['phone'].get(),
                    "email": form_vars['email'].get(),
                    "birthday": form_vars['birthday'].get(),
                    "address": form_vars['address'].get(),
                    "emergency_contact": form_vars['emergency_contact'].get(),
                    "position": form_vars['position'].get(),
                    "department": form_vars['department'].get(),
                    "hire_date": form_vars['hire_date'].get(),
                    "salary": salary,
                    "status": "Probation",
                    "performance": 75
                }
                
                self.employee_data.append(new_employee)
                messagebox.showinfo("Success", f"Employee {new_employee['name']} added successfully")
                add_window.destroy()
                self.refresh_employee_list()
                
            except Exception as e:
                messagebox.showerror("Error", f"Add failed: {str(e)}")
        
        save_btn = tk.Button(button_frame, text="Add Employee", 
                           font=('Segoe UI', 10, 'bold'),
                           bg=self.colors['primary'], fg=self.colors['white'],
                           bd=0, padx=30, pady=8, cursor='hand2',
                           command=save_employee)
        save_btn.pack(side='right', padx=5)
        
        cancel_btn = tk.Button(button_frame, text="Cancel", 
                             font=('Segoe UI', 10),
                             bg=self.colors['text_light'], fg=self.colors['white'],
                             bd=0, padx=30, pady=8, cursor='hand2',                             command=add_window.destroy)
        cancel_btn.pack(side='right', padx=5)
        
        # Layout scroll area
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mouse wheel
        def on_mousewheel(event):
            if canvas.winfo_exists():
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        
        canvas.bind("<MouseWheel>", on_mousewheel)
        scrollable_frame.bind("<MouseWheel>", on_mousewheel)
    
    def search_employees(self, keyword):
        """Search employees"""
        self.search_keyword = keyword.lower()
        self.refresh_employee_list()
    
    def filter_employees(self, filter_type):
        """Filter employees"""
        self.current_filter = filter_type
        self.refresh_employee_list()
    
    def refresh_employee_list(self):
        """Refresh employee list"""
        # Clear list
        for widget in self.employees_container.winfo_children():
            widget.destroy()
        
        # Filter and search employees
        filtered_employees = self.employee_data
        
        # Apply department filter
        if self.current_filter != "All":
            if self.current_filter in self.departments:
                filtered_employees = [e for e in filtered_employees if e['department'] == self.current_filter]
            else:
                filtered_employees = [e for e in filtered_employees if e['status'] == self.current_filter]
        
        # Apply search
        if self.search_keyword:
            filtered_employees = [e for e in filtered_employees 
                                if self.search_keyword in e['name'].lower() 
                                or self.search_keyword in e['phone'].lower()
                                or self.search_keyword in e['position'].lower()]
        
        # Create employee card
        for employee in filtered_employees:
            self.create_employee_card(self.employees_container, employee)
        
        # Update statistics
        self.update_statistics()
    
    def update_statistics(self):
        """Update statistics display area"""
        if not self.stats_frame:
            return

        # Clear existing statistics cards
        for widget in self.stats_frame.winfo_children():
            widget.destroy()
        
        # Calculate statistics data
        total_employees = len(self.employee_data)
        active_employees = len([e for e in self.employee_data if e['status'] == 'Employed'])
        trial_employees = len([e for e in self.employee_data if e['status'] == 'Probation'])
        avg_salary = sum(e['salary'] for e in self.employee_data if e['status'] in ['Employed', 'Probation']) / max(1, len([e for e in self.employee_data if e['status'] in ['Employed', 'Probation']]))
        
        # Create statistics cards
        stats = [
            ("Total Employees", total_employees, "employees", self.colors['primary']),
            ("Employed Employees", active_employees, "employees", self.colors['success']),
            ("Probation Employees", trial_employees, "employees", self.colors['warning']),
            ("Average Salary", f"¥{avg_salary:.0f}", "¥/month", self.colors['info'])
        ]
        
        for title, value, subtitle, color in stats:
            self.create_stats_card(self.stats_frame, title, value, subtitle, color)
    
    def show(self):
        """Show employee management interface"""
        self.clear_frames()
        self.update_title()

        if hasattr(self, 'main_frame') and self.main_frame:
            self.main_frame.destroy()
            
        self.main_frame = tk.Frame(self.parent_frame, bg=self.colors['background'])
        self.main_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Create top statistics area
        self.stats_frame = tk.Frame(self.main_frame, bg=self.colors['background'])
        self.stats_frame.pack(fill='x', pady=(0, 10))
        
        self.create_statistics(self.stats_frame)
        
        # Create main content area
        content_frame = tk.Frame(self.main_frame, bg=self.colors['background'])
        content_frame.pack(fill='both', expand=True)
        
        # Create left filter/operation area
        left_panel = tk.Frame(content_frame, bg=self.colors['card'], width=250)
        left_panel.pack(side='left', fill='y', padx=(0, 10))
        left_panel.pack_propagate(False)
        
        self.create_filter_panel(left_panel)
        
        # Create right employee list area
        right_panel = tk.Frame(content_frame, bg=self.colors['background'])
        right_panel.pack(side='right', fill='both', expand=True)
        
        self.create_employee_list_panel(right_panel)
        
        # Initial data load
        self.refresh_employee_list()

    def clear_frames(self):
        """Clear the content and title frames."""
        for widget in self.parent_frame.winfo_children():
            widget.destroy()
        for widget in self.title_frame.winfo_children():
            widget.destroy()

    def update_title(self):
        """Update the module title bar."""
        title_frame = tk.Frame(self.title_frame, bg=self.colors['card'])
        title_frame.pack(fill="both", expand=True)

        left_frame = tk.Frame(title_frame, bg=self.colors['card'])
        left_frame.pack(side="left", padx=20, pady=15)

        tk.Label(left_frame, text="👥", font=('Segoe UI Emoji', 22), 
                 bg=self.colors['card'], fg=self.colors['primary']).pack(side="left", padx=(0, 10))
        tk.Label(left_frame, text="Employee Management", font=('Segoe UI', 18, 'bold'), 
                 bg=self.colors['card'], fg=self.colors['text']).pack(side="left")

        right_frame = tk.Frame(title_frame, bg=self.colors['card'])
        right_frame.pack(side="right", padx=20, pady=15)
        
        search_entry = tk.Entry(right_frame, font=('Segoe UI', 11), width=30,
                                bd=1, relief='solid', highlightthickness=1, highlightcolor=self.colors['border'])
        search_entry.insert(0, "Search by name, position...")
        search_entry.bind("<FocusIn>", lambda args: search_entry.delete('0', 'end'))
        search_entry.bind("<Return>", lambda event: self.search_employees(search_entry.get()))
        search_entry.pack(side='left', padx=(0, 10), ipady=5)

        search_btn = tk.Button(right_frame, text="Search", 
                               font=('Segoe UI', 10, 'bold'),
                               bg=self.colors['primary'], fg=self.colors['white'],
                               bd=0, pady=5, padx=15, cursor="hand2",
                               command=lambda: self.search_employees(search_entry.get()))
        search_btn.pack(side='left')

        add_btn = tk.Button(right_frame, text="Add Employee", 
                           font=('Segoe UI', 10, 'bold'),
                           bg=self.colors['success'], fg=self.colors['white'],
                           bd=0, pady=5, padx=15, cursor="hand2",
                           command=self.add_new_employee)
        add_btn.pack(side='left', padx=(10, 0))

    def create_filter_panel(self, parent):
        """Create the left panel for filtering and operations."""
        tk.Label(parent, text="Filter Options", font=('Segoe UI', 12, 'bold'), 
                 bg=self.colors['card'], fg=self.colors['text']).pack(pady=15, padx=20, anchor='w')

        # Department filters
        tk.Label(parent, text="Department", font=('Segoe UI', 10, 'bold'), 
                 bg=self.colors['card'], fg=self.colors['text_light']).pack(padx=20, anchor='w')
        
        departments = ["All"] + self.departments
        for dept in departments:
            btn = tk.Button(parent, text=dept, font=('Segoe UI', 10), 
                            bg=self.colors['card'], fg=self.colors['text'], bd=0, 
                            anchor='w', cursor="hand2",
                            command=lambda d=dept: self.filter_employees(d))
            btn.pack(fill='x', padx=20, pady=2)
            if dept == self.current_filter:
                btn.config(font=('Segoe UI', 10, 'bold'), fg=self.colors['primary'])

        # Status filters
        tk.Label(parent, text="Status", font=('Segoe UI', 10, 'bold'), 
                 bg=self.colors['card'], fg=self.colors['text_light']).pack(padx=20, pady=(10,0), anchor='w')
        
        statuses = ["Employed", "Probation", "Resigned"]
        for status in statuses:
            btn = tk.Button(parent, text=status, font=('Segoe UI', 10), 
                            bg=self.colors['card'], fg=self.colors['text'], bd=0, 
                            anchor='w', cursor="hand2",
                            command=lambda s=status: self.filter_employees(s))
            btn.pack(fill='x', padx=20, pady=2)
            if status == self.current_filter:
                btn.config(font=('Segoe UI', 10, 'bold'), fg=self.colors['primary'])

    def create_statistics(self, parent):
        """Create statistics display area"""
        self.update_statistics()

    def create_employee_list_panel(self, parent):
        """Create the right panel for displaying the employee list."""
        canvas = tk.Canvas(parent, bg=self.colors['background'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        self.employees_container = tk.Frame(canvas, bg=self.colors['background'])

        self.employees_container.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.employees_container, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        def on_mousewheel(event):
            if canvas.winfo_exists():
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind("<MouseWheel>", on_mousewheel)
        self.employees_container.bind("<MouseWheel>", on_mousewheel)
