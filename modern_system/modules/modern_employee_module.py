#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
现代化员工管理模块
基于现代化外卖平台风格的员工管理界面
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
        
        # 部门配色
        self.department_colors = {
            '前厅部': '#3498DB',
            '厨房部': '#E67E22',
            '采购部': '#2ECC71',
            '财务部': '#9B59B6',
            '管理部': '#E74C3C',
            '配送部': '#1ABC9C'
        }
        
        # 员工状态配色
        self.status_colors = {
            '在职': '#2ECC71',
            '试用': '#F39C12',
            '离职': '#95A5A6',
            '休假': '#3498DB'
        }
        
        # 员工数据
        self.employee_data = [
            {
                "id": 1001,
                "name": "张三",
                "position": "前厅经理",
                "department": "前厅部",
                "phone": "138****1234",
                "email": "zhangsan@company.com",
                "hire_date": "2023-01-15",
                "salary": 8000.0,
                "status": "在职",
                "birthday": "1990-05-20",
                "address": "北京市朝阳区xxx街道",
                "emergency_contact": "李女士 139****5678",
                "performance": 85
            },
            {
                "id": 1002,
                "name": "李四",
                "position": "厨师长",
                "department": "厨房部",
                "phone": "139****5678",
                "email": "lisi@company.com",
                "hire_date": "2022-08-20",
                "salary": 9500.0,
                "status": "在职",
                "birthday": "1988-12-10",
                "address": "北京市海淀区xxx路",
                "emergency_contact": "王先生 137****9012",
                "performance": 92
            },
            {
                "id": 1003,
                "name": "王五",
                "position": "服务员",
                "department": "前厅部",
                "phone": "136****9012",
                "email": "wangwu@company.com",
                "hire_date": "2023-03-10",
                "salary": 4500.0,
                "status": "在职",
                "birthday": "1995-08-15",
                "address": "北京市西城区xxx胡同",
                "emergency_contact": "张女士 135****1234",
                "performance": 78
            },
            {
                "id": 1004,
                "name": "赵六",
                "position": "采购员",
                "department": "采购部",
                "phone": "137****3456",
                "email": "zhaoliu@company.com",
                "hire_date": "2023-05-22",
                "salary": 5500.0,
                "status": "试用",
                "birthday": "1992-03-25",
                "address": "北京市东城区xxx大街",
                "emergency_contact": "钱先生 138****7890",
                "performance": 72
            },
            {
                "id": 1005,
                "name": "钱七",
                "position": "财务专员",
                "department": "财务部",
                "phone": "135****7890",
                "email": "qianqi@company.com",
                "hire_date": "2022-12-01",
                "salary": 6000.0,
                "status": "离职",
                "birthday": "1989-11-08",
                "address": "北京市丰台区xxx路",
                "emergency_contact": "孙女士 132****4567",
                "performance": 65
            },
            {
                "id": 1006,
                "name": "孙八",
                "position": "配送员",
                "department": "配送部",
                "phone": "132****4567",
                "email": "sunba@company.com",
                "hire_date": "2023-06-01",
                "salary": 4000.0,
                "status": "在职",
                "birthday": "1996-01-30",
                "address": "北京市大兴区xxx社区",
                "emergency_contact": "周先生 186****1234",
                "performance": 88
            }
        ]        # 部门列表
        self.departments = ["前厅部", "厨房部", "采购部", "财务部", "管理部", "配送部"]
        
        self.selected_employee = None
        self.current_filter = "全部"
        self.search_keyword = ""
    
    def create_stats_card(self, parent, title, value, subtitle, color):
        """创建统计卡片"""
        # 外层容器
        container_frame = tk.Frame(parent, bg=self.colors['background'])
        container_frame.pack(side='left', padx=10, pady=5, fill='both', expand=True)
        
        # 卡片主体
        card_frame = tk.Frame(container_frame, bg=self.colors['card'], relief='flat', bd=1,
                             highlightbackground=self.colors['border'], highlightthickness=1)
        card_frame.pack(fill='both', expand=True)
        
        # 设置卡片尺寸
        card_frame.configure(height=120)
        container_frame.pack_propagate(False)
        
        # 图标/数值区域
        icon_frame = tk.Frame(card_frame, bg=color, width=80, height=80)
        icon_frame.pack(side='left', padx=15, pady=20)
        icon_frame.pack_propagate(False)
        
        # 数值标签
        value_label = tk.Label(icon_frame, text=str(value), 
                              font=('Microsoft YaHei UI', 16, 'bold'),
                              bg=color, fg=self.colors['white'])
        value_label.place(relx=0.5, rely=0.5, anchor='center')
        
        # 信息区域
        info_frame = tk.Frame(card_frame, bg=self.colors['card'])
        info_frame.pack(side='left', padx=(10, 15), pady=20, fill='both', expand=True)
        
        # 标题
        title_label = tk.Label(info_frame, text=title, 
                              font=('Microsoft YaHei UI', 12, 'bold'),
                              bg=self.colors['card'], fg=self.colors['text'])
        title_label.pack(anchor='w', pady=(10, 5))
        
        # 副标题
        subtitle_label = tk.Label(info_frame, text=subtitle, 
                                 font=('Microsoft YaHei UI', 10),
                                 bg=self.colors['card'], fg=self.colors['text_light'])
        subtitle_label.pack(anchor='w')
        
        return card_frame
    
    def create_employee_card(self, parent, employee):
        """创建员工卡片"""
        card_frame = tk.Frame(parent, bg=self.colors['card'], relief='flat', bd=1,
                             highlightbackground=self.colors['border'], highlightthickness=1)
        card_frame.pack(fill='x', padx=5, pady=5)
        
        # 卡片头部
        header_frame = tk.Frame(card_frame, bg=self.colors['card'])
        header_frame.pack(fill='x', padx=20, pady=(15, 10))
        
        # 员工基本信息
        info_frame = tk.Frame(header_frame, bg=self.colors['card'])
        info_frame.pack(side='left', fill='both', expand=True)
        
        # 员工姓名和ID
        name_frame = tk.Frame(info_frame, bg=self.colors['card'])
        name_frame.pack(fill='x')
        
        name_label = tk.Label(name_frame, text=employee['name'], 
                             font=('Microsoft YaHei UI', 14, 'bold'),
                             bg=self.colors['card'], fg=self.colors['text'])
        name_label.pack(side='left')
        
        id_label = tk.Label(name_frame, text=f"工号: {employee['id']}", 
                           font=('Microsoft YaHei UI', 10),
                           bg=self.colors['card'], fg=self.colors['text_light'])
        id_label.pack(side='left', padx=(10, 0))
        
        # 职位信息
        position_frame = tk.Frame(info_frame, bg=self.colors['card'])
        position_frame.pack(fill='x', pady=(5, 0))
        
        position_label = tk.Label(position_frame, text=f"🎯 {employee['position']}", 
                                 font=('Microsoft YaHei UI', 11, 'bold'),
                                 bg=self.colors['card'], fg=self.colors['primary'])
        position_label.pack(side='left')
        
        # 联系信息
        contact_frame = tk.Frame(info_frame, bg=self.colors['card'])
        contact_frame.pack(fill='x', pady=(5, 0))
        
        phone_label = tk.Label(contact_frame, text=f"📞 {employee['phone']}", 
                              font=('Microsoft YaHei UI', 10),
                              bg=self.colors['card'], fg=self.colors['text'])
        phone_label.pack(side='left')
        
        email_label = tk.Label(contact_frame, text=f"📧 {employee['email']}", 
                              font=('Microsoft YaHei UI', 10),
                              bg=self.colors['card'], fg=self.colors['text'])
        email_label.pack(side='left', padx=(20, 0))
        
        # 右侧状态和部门
        right_frame = tk.Frame(header_frame, bg=self.colors['card'])
        right_frame.pack(side='right')
        
        # 部门标签
        dept_color = self.department_colors.get(employee['department'], self.colors['info'])
        dept_frame = tk.Frame(right_frame, bg=dept_color, padx=10, pady=5)
        dept_frame.pack(pady=(0, 5))
        
        dept_label = tk.Label(dept_frame, text=employee['department'], 
                             font=('Microsoft YaHei UI', 10, 'bold'),
                             bg=dept_color, fg=self.colors['white'])
        dept_label.pack()
        
        # 状态标签
        status_color = self.status_colors.get(employee['status'], self.colors['info'])
        status_frame = tk.Frame(right_frame, bg=status_color, padx=10, pady=5)
        status_frame.pack()
        
        status_label = tk.Label(status_frame, text=employee['status'], 
                               font=('Microsoft YaHei UI', 10, 'bold'),
                               bg=status_color, fg=self.colors['white'])
        status_label.pack()
        
        # 员工详细信息
        details_frame = tk.Frame(card_frame, bg=self.colors['background'], padx=15, pady=10)
        details_frame.pack(fill='x', padx=20, pady=(0, 10))
        
        # 工作信息
        work_info_frame = tk.Frame(details_frame, bg=self.colors['background'])
        work_info_frame.pack(side='left', fill='x', expand=True)
        
        work_items = [
            ("入职日期", employee['hire_date']),
            ("薪资待遇", f"¥{employee['salary']:.0f}"),
            ("绩效评分", f"{employee['performance']}分")
        ]
        
        for i, (label, value) in enumerate(work_items):
            item_frame = tk.Frame(work_info_frame, bg=self.colors['background'])
            item_frame.pack(side='left', padx=(0, 20))
            
            tk.Label(item_frame, text=label, font=('Microsoft YaHei UI', 9),
                    bg=self.colors['background'], fg=self.colors['text_light']).pack()
            
            tk.Label(item_frame, text=value, font=('Microsoft YaHei UI', 11, 'bold'),
                    bg=self.colors['background'], fg=self.colors['text']).pack()
        
        # 绩效条
        performance_frame = tk.Frame(details_frame, bg=self.colors['background'])
        performance_frame.pack(side='right', padx=(20, 0))
        
        tk.Label(performance_frame, text="绩效", font=('Microsoft YaHei UI', 9),
                bg=self.colors['background'], fg=self.colors['text_light']).pack()
        
        # 绩效进度条
        progress_bg = tk.Frame(performance_frame, bg=self.colors['light'], width=100, height=6)
        progress_bg.pack(pady=2)
        progress_bg.pack_propagate(False)
        
        performance_pct = employee['performance'] / 100
        progress_width = int(100 * performance_pct)
        
        # 根据绩效分数选择颜色
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
        
        # 操作按钮
        actions_frame = tk.Frame(card_frame, bg=self.colors['card'])
        actions_frame.pack(fill='x', padx=20, pady=(0, 15))
        
        # 查看详情按钮
        detail_btn = tk.Button(actions_frame, text="查看详情", 
                              font=('Microsoft YaHei UI', 9),
                              bg=self.colors['info'], fg=self.colors['white'],
                              bd=0, padx=15, pady=5, cursor='hand2',
                              command=lambda: self.show_employee_detail(employee))
        detail_btn.pack(side='right', padx=5)
        
        # 编辑按钮
        edit_btn = tk.Button(actions_frame, text="编辑", 
                            font=('Microsoft YaHei UI', 9),
                            bg=self.colors['warning'], fg=self.colors['white'],
                            bd=0, padx=15, pady=5, cursor='hand2',
                            command=lambda: self.edit_employee(employee))
        edit_btn.pack(side='right', padx=5)
        
        # 删除按钮（离职员工不显示）
        if employee['status'] != '离职':
            delete_btn = tk.Button(actions_frame, text="离职", 
                                  font=('Microsoft YaHei UI', 9),
                                  bg=self.colors['danger'], fg=self.colors['white'],
                                  bd=0, padx=15, pady=5, cursor='hand2',
                                  command=lambda: self.resign_employee(employee['id']))
            delete_btn.pack(side='right', padx=5)
        
        return card_frame
    
    def show_employee_detail(self, employee):
        """显示员工详情"""
        detail_window = tk.Toplevel()
        detail_window.title(f"员工详情 - {employee['name']}")
        detail_window.geometry("600x750")
        detail_window.configure(bg=self.colors['background'])
        detail_window.resizable(False, False)
        
        # 标题
        title_frame = tk.Frame(detail_window, bg=self.colors['primary'], height=60)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text=f"员工详情 - {employee['name']}", 
                              font=('Microsoft YaHei UI', 16, 'bold'),
                              bg=self.colors['primary'], fg=self.colors['white'])
        title_label.pack(expand=True)
        
        # 详情内容
        content_frame = tk.Frame(detail_window, bg=self.colors['background'])
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # 基本信息卡片
        basic_frame = tk.Frame(content_frame, bg=self.colors['card'], padx=20, pady=15)
        basic_frame.pack(fill='x', pady=(0, 15))
        
        tk.Label(basic_frame, text="基本信息", font=('Microsoft YaHei UI', 14, 'bold'),
                bg=self.colors['card'], fg=self.colors['text']).pack(anchor='w', pady=(0, 10))
        
        basic_info = [
            ("工号", employee['id']),
            ("姓名", employee['name']),
            ("生日", employee['birthday']),
            ("联系电话", employee['phone']),
            ("电子邮箱", employee['email']),
            ("家庭住址", employee['address']),
            ("紧急联系人", employee['emergency_contact'])
        ]
        
        for label, value in basic_info:
            info_row = tk.Frame(basic_frame, bg=self.colors['card'])
            info_row.pack(fill='x', pady=2)
            
            tk.Label(info_row, text=f"{label}:", font=('Microsoft YaHei UI', 10),
                    bg=self.colors['card'], fg=self.colors['text_light'], width=12, anchor='w').pack(side='left')
            
            tk.Label(info_row, text=str(value), font=('Microsoft YaHei UI', 10),
                    bg=self.colors['card'], fg=self.colors['text'], anchor='w').pack(side='left', fill='x', expand=True)
        
        # 工作信息卡片
        work_frame = tk.Frame(content_frame, bg=self.colors['card'], padx=20, pady=15)
        work_frame.pack(fill='x', pady=(0, 15))
        
        tk.Label(work_frame, text="工作信息", font=('Microsoft YaHei UI', 14, 'bold'),
                bg=self.colors['card'], fg=self.colors['text']).pack(anchor='w', pady=(0, 10))
        
        work_info = [
            ("职位", employee['position']),
            ("部门", employee['department']),
            ("入职日期", employee['hire_date']),
            ("员工状态", employee['status']),
            ("薪资待遇", f"¥{employee['salary']:.2f}"),
            ("绩效评分", f"{employee['performance']}分")
        ]
        
        for label, value in work_info:
            info_row = tk.Frame(work_frame, bg=self.colors['card'])
            info_row.pack(fill='x', pady=2)
            
            tk.Label(info_row, text=f"{label}:", font=('Microsoft YaHei UI', 10),
                    bg=self.colors['card'], fg=self.colors['text_light'], width=12, anchor='w').pack(side='left')
            
            tk.Label(info_row, text=str(value), font=('Microsoft YaHei UI', 10),
                    bg=self.colors['card'], fg=self.colors['text'], anchor='w').pack(side='left', fill='x', expand=True)
        
        # 绩效详情
        performance_frame = tk.Frame(content_frame, bg=self.colors['card'], padx=20, pady=15)
        performance_frame.pack(fill='x', pady=(0, 15))
        
        tk.Label(performance_frame, text="绩效详情", font=('Microsoft YaHei UI', 14, 'bold'),
                bg=self.colors['card'], fg=self.colors['text']).pack(anchor='w', pady=(0, 10))
        
        # 工作天数计算
        hire_date = datetime.datetime.strptime(employee['hire_date'], '%Y-%m-%d')
        work_days = (datetime.datetime.now() - hire_date).days
        
        # 绩效可视化
        perf_visual_frame = tk.Frame(performance_frame, bg=self.colors['background'], padx=15, pady=10)
        perf_visual_frame.pack(fill='x')
        
        # 绩效指标
        perf_items = [
            ("工作态度", employee['performance'] - 5),
            ("工作质量", employee['performance'] + 3),
            ("团队协作", employee['performance'] - 2),
            ("学习能力", employee['performance'] + 1)
        ]
        
        for item_name, score in perf_items:
            item_frame = tk.Frame(perf_visual_frame, bg=self.colors['background'])
            item_frame.pack(fill='x', pady=5)
            
            tk.Label(item_frame, text=item_name, font=('Microsoft YaHei UI', 10),
                    bg=self.colors['background'], fg=self.colors['text'], width=10, anchor='w').pack(side='left')
            
            # 评分条
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
            
            tk.Label(item_frame, text=f"{max(0, min(100, score))}分", font=('Microsoft YaHei UI', 9),
                    bg=self.colors['background'], fg=self.colors['text']).pack(side='right')
        
        # 工作统计
        stats_text = f"""在职天数：{work_days} 天
月均工作天数：{work_days // max(1, (datetime.datetime.now() - hire_date).days // 30)} 天
部门排名：前 {30}%
综合评价：{'优秀' if employee['performance'] >= 90 else '良好' if employee['performance'] >= 80 else '一般' if employee['performance'] >= 70 else '待改进'}"""
        
        tk.Label(performance_frame, text=stats_text, font=('Microsoft YaHei UI', 10),
                bg=self.colors['card'], fg=self.colors['text'], justify='left').pack(anchor='w', pady=(10, 0))
        
        # 关闭按钮
        tk.Button(content_frame, text="关闭", font=('Microsoft YaHei UI', 10),
                 bg=self.colors['text_light'], fg=self.colors['white'],
                 bd=0, padx=30, pady=8, cursor='hand2',
                 command=detail_window.destroy).pack(pady=10)
    
    def edit_employee(self, employee):
        """编辑员工信息"""
        edit_window = tk.Toplevel()
        edit_window.title(f"编辑员工 - {employee['name']}")
        edit_window.geometry("550x700")
        edit_window.configure(bg=self.colors['background'])
        edit_window.resizable(False, False)
        
        # 标题
        title_frame = tk.Frame(edit_window, bg=self.colors['primary'], height=60)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text="编辑员工信息", 
                              font=('Microsoft YaHei UI', 16, 'bold'),
                              bg=self.colors['primary'], fg=self.colors['white'])
        title_label.pack(expand=True)
        
        # 表单内容
        form_frame = tk.Frame(edit_window, bg=self.colors['background'])
        form_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # 创建滚动区域
        canvas = tk.Canvas(form_frame, bg=self.colors['background'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(form_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['background'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # 表单卡片
        card_frame = tk.Frame(scrollable_frame, bg=self.colors['card'], padx=20, pady=20)
        card_frame.pack(fill='both', expand=True)
        
        # 表单字段
        form_vars = {}
        
        # 基本信息
        tk.Label(card_frame, text="基本信息", font=('Microsoft YaHei UI', 12, 'bold'),
                bg=self.colors['card'], fg=self.colors['text']).pack(anchor='w', pady=(0, 10))
        
        basic_fields = [
            ("姓名", "name", employee['name']),
            ("联系电话", "phone", employee['phone']),
            ("电子邮箱", "email", employee['email']),
            ("生日", "birthday", employee['birthday']),
            ("家庭住址", "address", employee['address']),
            ("紧急联系人", "emergency_contact", employee['emergency_contact'])
        ]
        
        for label, field, value in basic_fields:
            field_frame = tk.Frame(card_frame, bg=self.colors['card'])
            field_frame.pack(fill='x', pady=5)
            
            tk.Label(field_frame, text=f"{label}:", font=('Microsoft YaHei UI', 10),
                    bg=self.colors['card'], fg=self.colors['text']).pack(anchor='w', pady=(0, 2))
            
            var = tk.StringVar(value=value)
            form_vars[field] = var
            
            entry = tk.Entry(field_frame, textvariable=var, font=('Microsoft YaHei UI', 10),
                           relief='flat', bd=5, bg=self.colors['light'])
            entry.pack(fill='x')
        
        # 分隔线
        separator = tk.Frame(card_frame, bg=self.colors['border'], height=1)
        separator.pack(fill='x', pady=20)
        
        # 工作信息
        tk.Label(card_frame, text="工作信息", font=('Microsoft YaHei UI', 12, 'bold'),
                bg=self.colors['card'], fg=self.colors['text']).pack(anchor='w', pady=(0, 10))
        
        # 职位
        pos_frame = tk.Frame(card_frame, bg=self.colors['card'])
        pos_frame.pack(fill='x', pady=5)
        tk.Label(pos_frame, text="职位:", font=('Microsoft YaHei UI', 10),
                bg=self.colors['card'], fg=self.colors['text']).pack(anchor='w', pady=(0, 2))
        position_var = tk.StringVar(value=employee['position'])
        form_vars['position'] = position_var
        position_entry = tk.Entry(pos_frame, textvariable=position_var, font=('Microsoft YaHei UI', 10),
                                 relief='flat', bd=5, bg=self.colors['light'])
        position_entry.pack(fill='x')
        
        # 部门
        dept_frame = tk.Frame(card_frame, bg=self.colors['card'])
        dept_frame.pack(fill='x', pady=5)
        tk.Label(dept_frame, text="部门:", font=('Microsoft YaHei UI', 10),
                bg=self.colors['card'], fg=self.colors['text']).pack(anchor='w', pady=(0, 2))
        department_var = tk.StringVar(value=employee['department'])
        form_vars['department'] = department_var
        dept_combo = ttk.Combobox(dept_frame, textvariable=department_var, 
                                 values=self.departments, state="readonly", font=('Microsoft YaHei UI', 10))
        dept_combo.pack(fill='x')
        
        # 入职日期
        hire_frame = tk.Frame(card_frame, bg=self.colors['card'])
        hire_frame.pack(fill='x', pady=5)
        tk.Label(hire_frame, text="入职日期:", font=('Microsoft YaHei UI', 10),
                bg=self.colors['card'], fg=self.colors['text']).pack(anchor='w', pady=(0, 2))
        hire_var = tk.StringVar(value=employee['hire_date'])
        form_vars['hire_date'] = hire_var
        hire_entry = tk.Entry(hire_frame, textvariable=hire_var, font=('Microsoft YaHei UI', 10),
                             relief='flat', bd=5, bg=self.colors['light'])
        hire_entry.pack(fill='x')
        
        # 薪资
        salary_frame = tk.Frame(card_frame, bg=self.colors['card'])
        salary_frame.pack(fill='x', pady=5)
        tk.Label(salary_frame, text="薪资 (元):", font=('Microsoft YaHei UI', 10),
                bg=self.colors['card'], fg=self.colors['text']).pack(anchor='w', pady=(0, 2))
        salary_var = tk.StringVar(value=str(employee['salary']))
        form_vars['salary'] = salary_var
        salary_entry = tk.Entry(salary_frame, textvariable=salary_var, font=('Microsoft YaHei UI', 10),
                               relief='flat', bd=5, bg=self.colors['light'])
        salary_entry.pack(fill='x')
        
        # 状态
        status_frame = tk.Frame(card_frame, bg=self.colors['card'])
        status_frame.pack(fill='x', pady=5)
        tk.Label(status_frame, text="状态:", font=('Microsoft YaHei UI', 10),
                bg=self.colors['card'], fg=self.colors['text']).pack(anchor='w', pady=(0, 2))
        status_var = tk.StringVar(value=employee['status'])
        form_vars['status'] = status_var
        status_combo = ttk.Combobox(status_frame, textvariable=status_var, 
                                   values=["在职", "试用", "休假", "离职"], state="readonly", font=('Microsoft YaHei UI', 10))
        status_combo.pack(fill='x')
        
        # 绩效评分
        perf_frame = tk.Frame(card_frame, bg=self.colors['card'])
        perf_frame.pack(fill='x', pady=5)
        tk.Label(perf_frame, text="绩效评分 (0-100):", font=('Microsoft YaHei UI', 10),
                bg=self.colors['card'], fg=self.colors['text']).pack(anchor='w', pady=(0, 2))
        performance_var = tk.StringVar(value=str(employee['performance']))
        form_vars['performance'] = performance_var
        perf_entry = tk.Entry(perf_frame, textvariable=performance_var, font=('Microsoft YaHei UI', 10),
                             relief='flat', bd=5, bg=self.colors['light'])
        perf_entry.pack(fill='x')
        
        # 按钮区域
        button_frame = tk.Frame(card_frame, bg=self.colors['card'])
        button_frame.pack(fill='x', pady=20)
        
        def save_changes():
            try:
                # 验证输入
                if not form_vars['name'].get() or not form_vars['phone'].get():
                    messagebox.showerror("错误", "请填写员工姓名和联系电话")
                    return
                
                # 验证薪资
                try:
                    salary = float(form_vars['salary'].get())
                    if salary < 0:
                        raise ValueError()
                except ValueError:
                    messagebox.showerror("错误", "请输入有效的薪资数额")
                    return
                
                # 验证绩效评分
                try:
                    performance = int(form_vars['performance'].get())
                    if not 0 <= performance <= 100:
                        raise ValueError()
                except ValueError:
                    messagebox.showerror("错误", "绩效评分必须是0-100之间的整数")
                    return
                
                # 更新员工信息
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
                
                messagebox.showinfo("成功", "员工信息已更新")
                edit_window.destroy()
                self.refresh_employee_list()
                
            except Exception as e:
                messagebox.showerror("错误", f"保存失败：{str(e)}")
        
        save_btn = tk.Button(button_frame, text="保存修改", 
                           font=('Microsoft YaHei UI', 10, 'bold'),
                           bg=self.colors['primary'], fg=self.colors['white'],
                           bd=0, padx=30, pady=8, cursor='hand2',
                           command=save_changes)
        save_btn.pack(side='right', padx=5)
        
        cancel_btn = tk.Button(button_frame, text="取消", 
                             font=('Microsoft YaHei UI', 10),
                             bg=self.colors['text_light'], fg=self.colors['white'],
                             bd=0, padx=30, pady=8, cursor='hand2',
                             command=edit_window.destroy)
        cancel_btn.pack(side='right', padx=5)
        
        # 布局滚动区域
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # 绑定鼠标滚轮
        def on_mousewheel(event):
            try:
                if canvas.winfo_exists():
                    canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            except tk.TclError:
                pass  # Widget已被销毁，忽略错误
        
        canvas.bind("<MouseWheel>", on_mousewheel)
        scrollable_frame.bind("<MouseWheel>", on_mousewheel)
    
    def resign_employee(self, employee_id):
        """员工离职"""
        result = messagebox.askyesno("确认离职", "确定要将该员工状态设置为离职吗？")
        if result:
            for employee in self.employee_data:
                if employee['id'] == employee_id:
                    employee['status'] = '离职'
                    messagebox.showinfo("成功", f"员工 {employee['name']} 已设置为离职状态")
                    self.refresh_employee_list()
                    break
    
    def add_new_employee(self):
        """添加新员工"""
        add_window = tk.Toplevel()
        add_window.title("添加新员工")
        add_window.geometry("550x700")
        add_window.configure(bg=self.colors['background'])
        add_window.resizable(False, False)
        
        # 标题
        title_frame = tk.Frame(add_window, bg=self.colors['primary'], height=60)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text="添加新员工", 
                              font=('Microsoft YaHei UI', 16, 'bold'),
                              bg=self.colors['primary'], fg=self.colors['white'])
        title_label.pack(expand=True)
        
        # 表单内容
        form_frame = tk.Frame(add_window, bg=self.colors['background'])
        form_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # 创建滚动区域
        canvas = tk.Canvas(form_frame, bg=self.colors['background'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(form_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['background'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # 表单卡片
        card_frame = tk.Frame(scrollable_frame, bg=self.colors['card'], padx=20, pady=20)
        card_frame.pack(fill='both', expand=True)
        
        # 表单字段
        form_vars = {}
        
        # 基本信息
        tk.Label(card_frame, text="基本信息", font=('Microsoft YaHei UI', 12, 'bold'),
                bg=self.colors['card'], fg=self.colors['text']).pack(anchor='w', pady=(0, 10))
        
        basic_fields = [
            ("姓名", "name", ""),
            ("联系电话", "phone", ""),
            ("电子邮箱", "email", ""),
            ("生日", "birthday", ""),
            ("家庭住址", "address", ""),
            ("紧急联系人", "emergency_contact", "")
        ]
        
        for label, field, default in basic_fields:
            field_frame = tk.Frame(card_frame, bg=self.colors['card'])
            field_frame.pack(fill='x', pady=5)
            
            tk.Label(field_frame, text=f"{label}:", font=('Microsoft YaHei UI', 10),
                    bg=self.colors['card'], fg=self.colors['text']).pack(anchor='w', pady=(0, 2))
            
            var = tk.StringVar(value=default)
            form_vars[field] = var
            
            entry = tk.Entry(field_frame, textvariable=var, font=('Microsoft YaHei UI', 10),
                           relief='flat', bd=5, bg=self.colors['light'])
            entry.pack(fill='x')
        
        # 分隔线
        separator = tk.Frame(card_frame, bg=self.colors['border'], height=1)
        separator.pack(fill='x', pady=20)
        
        # 工作信息
        tk.Label(card_frame, text="工作信息", font=('Microsoft YaHei UI', 12, 'bold'),
                bg=self.colors['card'], fg=self.colors['text']).pack(anchor='w', pady=(0, 10))
        
        # 职位
        pos_frame = tk.Frame(card_frame, bg=self.colors['card'])
        pos_frame.pack(fill='x', pady=5)
        tk.Label(pos_frame, text="职位:", font=('Microsoft YaHei UI', 10),
                bg=self.colors['card'], fg=self.colors['text']).pack(anchor='w', pady=(0, 2))
        position_var = tk.StringVar()
        form_vars['position'] = position_var
        position_entry = tk.Entry(pos_frame, textvariable=position_var, font=('Microsoft YaHei UI', 10),
                                 relief='flat', bd=5, bg=self.colors['light'])
        position_entry.pack(fill='x')
        
        # 部门
        dept_frame = tk.Frame(card_frame, bg=self.colors['card'])
        dept_frame.pack(fill='x', pady=5)
        tk.Label(dept_frame, text="部门:", font=('Microsoft YaHei UI', 10),
                bg=self.colors['card'], fg=self.colors['text']).pack(anchor='w', pady=(0, 2))
        department_var = tk.StringVar(value=self.departments[0])
        form_vars['department'] = department_var
        dept_combo = ttk.Combobox(dept_frame, textvariable=department_var, 
                                 values=self.departments, state="readonly", font=('Microsoft YaHei UI', 10))
        dept_combo.pack(fill='x')
        
        # 入职日期
        hire_frame = tk.Frame(card_frame, bg=self.colors['card'])
        hire_frame.pack(fill='x', pady=5)
        tk.Label(hire_frame, text="入职日期:", font=('Microsoft YaHei UI', 10),
                bg=self.colors['card'], fg=self.colors['text']).pack(anchor='w', pady=(0, 2))
        hire_var = tk.StringVar(value=datetime.datetime.now().strftime("%Y-%m-%d"))
        form_vars['hire_date'] = hire_var
        hire_entry = tk.Entry(hire_frame, textvariable=hire_var, font=('Microsoft YaHei UI', 10),
                             relief='flat', bd=5, bg=self.colors['light'])
        hire_entry.pack(fill='x')
        
        # 薪资
        salary_frame = tk.Frame(card_frame, bg=self.colors['card'])
        salary_frame.pack(fill='x', pady=5)
        tk.Label(salary_frame, text="薪资 (元):", font=('Microsoft YaHei UI', 10),
                bg=self.colors['card'], fg=self.colors['text']).pack(anchor='w', pady=(0, 2))
        salary_var = tk.StringVar(value="5000")
        form_vars['salary'] = salary_var
        salary_entry = tk.Entry(salary_frame, textvariable=salary_var, font=('Microsoft YaHei UI', 10),
                               relief='flat', bd=5, bg=self.colors['light'])
        salary_entry.pack(fill='x')
        
        # 按钮区域
        button_frame = tk.Frame(card_frame, bg=self.colors['card'])
        button_frame.pack(fill='x', pady=20)
        
        def save_employee():
            try:
                # 验证输入
                if not form_vars['name'].get() or not form_vars['phone'].get():
                    messagebox.showerror("错误", "请填写员工姓名和联系电话")
                    return
                
                # 验证薪资
                try:
                    salary = float(form_vars['salary'].get())
                    if salary < 0:
                        raise ValueError()
                except ValueError:
                    messagebox.showerror("错误", "请输入有效的薪资数额")
                    return
                
                # 生成新员工ID
                new_id = max([emp['id'] for emp in self.employee_data]) + 1
                
                # 创建新员工
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
                    "status": "试用",
                    "performance": 75
                }
                
                self.employee_data.append(new_employee)
                messagebox.showinfo("成功", f"员工 {new_employee['name']} 添加成功")
                add_window.destroy()
                self.refresh_employee_list()
                
            except Exception as e:
                messagebox.showerror("错误", f"添加失败：{str(e)}")
        
        save_btn = tk.Button(button_frame, text="添加员工", 
                           font=('Microsoft YaHei UI', 10, 'bold'),
                           bg=self.colors['primary'], fg=self.colors['white'],
                           bd=0, padx=30, pady=8, cursor='hand2',
                           command=save_employee)
        save_btn.pack(side='right', padx=5)
        
        cancel_btn = tk.Button(button_frame, text="取消", 
                             font=('Microsoft YaHei UI', 10),
                             bg=self.colors['text_light'], fg=self.colors['white'],
                             bd=0, padx=30, pady=8, cursor='hand2',                             command=add_window.destroy)
        cancel_btn.pack(side='right', padx=5)
        
        # 布局滚动区域
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # 绑定鼠标滚轮
        def on_mousewheel(event):
            try:
                if canvas.winfo_exists():
                    canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            except tk.TclError:
                pass  # Widget已被销毁，忽略错误
        
        canvas.bind("<MouseWheel>", on_mousewheel)
        scrollable_frame.bind("<MouseWheel>", on_mousewheel)
    
    def search_employees(self, keyword):
        """搜索员工"""
        self.search_keyword = keyword.lower()
        self.refresh_employee_list()
    
    def filter_employees(self, filter_type):
        """筛选员工"""
        self.current_filter = filter_type
        self.refresh_employee_list()
    
    def refresh_employee_list(self):
        """刷新员工列表"""
        # 清空列表
        for widget in self.employees_container.winfo_children():
            widget.destroy()
        
        # 筛选和搜索员工
        filtered_employees = self.employee_data
        
        # 应用部门筛选
        if self.current_filter != "全部":
            if self.current_filter in self.departments:
                filtered_employees = [e for e in filtered_employees if e['department'] == self.current_filter]
            else:
                filtered_employees = [e for e in filtered_employees if e['status'] == self.current_filter]
        
        # 应用搜索
        if self.search_keyword:
            filtered_employees = [e for e in filtered_employees 
                                if self.search_keyword in e['name'].lower() 
                                or self.search_keyword in e['phone'].lower()
                                or self.search_keyword in e['position'].lower()]
        
        # 创建员工卡片
        for employee in filtered_employees:
            self.create_employee_card(self.employees_container, employee)
        
        # 更新统计信息
        self.update_statistics()
    
    def update_statistics(self):
        """更新统计信息"""
        # 清空统计卡片
        for widget in self.stats_frame.winfo_children():
            widget.destroy()
        
        # 计算统计数据
        total_employees = len(self.employee_data)
        active_employees = len([e for e in self.employee_data if e['status'] == '在职'])
        trial_employees = len([e for e in self.employee_data if e['status'] == '试用'])
        avg_salary = sum(e['salary'] for e in self.employee_data if e['status'] in ['在职', '试用']) / max(1, len([e for e in self.employee_data if e['status'] in ['在职', '试用']]))
        
        # 创建统计卡片
        stats = [
            ("总员工数", total_employees, "位员工", self.colors['primary']),
            ("在职员工", active_employees, "位员工", self.colors['success']),
            ("试用员工", trial_employees, "位员工", self.colors['warning']),
            ("平均薪资", f"¥{avg_salary:.0f}", "元/月", self.colors['info'])
        ]
        
        for title, value, subtitle, color in stats:
            self.create_stats_card(self.stats_frame, title, value, subtitle, color)
    
    def show(self):
        """显示员工管理界面"""
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
        title_label = tk.Label(title_container, text="👨‍💼 员工管理", 
                              font=('Microsoft YaHei UI', 18, 'bold'),
                              bg=self.colors['white'], fg=self.colors['text'])
        title_label.pack(side='left', padx=20, pady=15)
        
        # 搜索框
        search_frame = tk.Frame(title_container, bg=self.colors['white'])
        search_frame.pack(side='left', padx=20, pady=15)
        
        search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=search_var, 
                               font=('Microsoft YaHei UI', 10),
                               width=20, relief='flat', bd=5, bg=self.colors['light'])
        search_entry.pack(side='left', padx=(0, 10))
        
        search_btn = tk.Button(search_frame, text="🔍 搜索", 
                              font=('Microsoft YaHei UI', 9),
                              bg=self.colors['info'], fg=self.colors['white'],
                              bd=0, padx=15, pady=5, cursor='hand2',
                              command=lambda: self.search_employees(search_var.get()))
        search_btn.pack(side='left')
        
        # 操作按钮
        actions_frame = tk.Frame(title_container, bg=self.colors['white'])
        actions_frame.pack(side='right', padx=20, pady=15)
        
        # 添加员工按钮
        add_btn = tk.Button(actions_frame, text="➕ 添加员工", 
                           font=('Microsoft YaHei UI', 10, 'bold'),
                           bg=self.colors['primary'], fg=self.colors['white'],
                           bd=0, padx=20, pady=8, cursor='hand2',
                           command=self.add_new_employee)
        add_btn.pack(side='right', padx=5)
        
        # 刷新按钮
        refresh_btn = tk.Button(actions_frame, text="🔄 刷新", 
                               font=('Microsoft YaHei UI', 10),
                               bg=self.colors['info'], fg=self.colors['white'],
                               bd=0, padx=20, pady=8, cursor='hand2',
                               command=self.refresh_employee_list)
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
        
        tk.Label(filter_frame, text="筛选员工：", font=('Microsoft YaHei UI', 12, 'bold'),
                bg=self.colors['background'], fg=self.colors['text']).pack(side='left')
        
        filter_buttons = ["全部"] + self.departments + ["在职", "试用", "离职"]
        for filter_name in filter_buttons:
            btn_color = self.colors['primary'] if filter_name == self.current_filter else self.colors['light']
            text_color = self.colors['white'] if filter_name == self.current_filter else self.colors['text']
            
            filter_btn = tk.Button(filter_frame, text=filter_name, 
                                  font=('Microsoft YaHei UI', 9),
                                  bg=btn_color, fg=text_color,
                                  bd=0, padx=12, pady=5, cursor='hand2',
                                  command=lambda f=filter_name: self.filter_employees(f))
            filter_btn.pack(side='left', padx=3)
        
        # 员工列表容器
        list_frame = tk.Frame(main_frame, bg=self.colors['background'])
        list_frame.pack(fill='both', expand=True)
        
        # 滚动区域
        canvas = tk.Canvas(list_frame, bg=self.colors['background'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=canvas.yview)
        self.employees_container = tk.Frame(canvas, bg=self.colors['background'])
        
        self.employees_container.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.employees_container, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # 初始化显示
        self.refresh_employee_list()
          # 绑定鼠标滚轮事件
        def on_mousewheel(event):
            try:
                if canvas.winfo_exists():
                    canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            except tk.TclError:
                pass  # Widget已被销毁，忽略错误
        
        canvas.bind("<MouseWheel>", on_mousewheel)
        self.employees_container.bind("<MouseWheel>", on_mousewheel)
