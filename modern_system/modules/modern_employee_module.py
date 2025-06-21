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
        self.employee_data = []
        # 部门列表
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
        # Note: We are assuming an EmployeeDialog class exists, similar to MealDialog
        # This part will need a proper dialog implementation for a full solution
        dialog = EmployeeDialog(self.parent_frame, f"编辑员工 - {employee['name']}", employee_data=employee, departments=self.departments)
        if dialog.result:
            try:
                data_manager.update_employee(employee['id'], dialog.result)
                messagebox.showinfo("成功", "员工信息更新成功！")
                self.refresh_employee_list()
            except Exception as e:
                messagebox.showerror("更新失败", f"更新员工信息时出错: {e}")
    
    def resign_employee(self, employee_id):
        """员工离职"""
        try:
            employee = next((e for e in self.employee_data if e['id'] == employee_id), None)
            if not employee:
                messagebox.showerror("错误", "未找到该员工。")
                return
            
            if messagebox.askyesno("确认离职", f"确定要将员工 {employee['name']} 的状态设置为离职吗？"):
                data_manager.delete_employee(employee_id) # delete_employee handles the logic
                messagebox.showinfo("成功", f"员工 {employee['name']} 已设置为离职状态")
                self.refresh_employee_list()
        except Exception as e:
            messagebox.showerror("操作失败", f"操作失败: {e}")
            
    def add_new_employee(self):
        """添加新员工"""
        # Note: We are assuming an EmployeeDialog class exists
        dialog = EmployeeDialog(self.parent_frame, "添加新员工", departments=self.departments)
        if dialog.result:
            try:
                data_manager.add_employee(dialog.result)
                messagebox.showinfo("成功", "新员工添加成功！")
                self.refresh_employee_list()
            except Exception as e:
                messagebox.showerror("添加失败", f"添加新员工失败: {e}")
    
    def search_employees(self, keyword):
        """搜索员工"""
        self.search_keyword = keyword.lower()
        self.refresh_employee_list()
    
    def filter_employees(self, filter_type):
        """筛选员工"""
        self.current_filter = filter_type
        self.refresh_employee_list()
    
    def refresh_employee_list(self):
        """从数据库重新加载并刷新员工列表和统计数据"""
        try:
            keyword = self.search_keyword if self.search_keyword else None
            # 注意: 搜索和筛选的逻辑需要后端支持，暂时简化处理
            self.employee_data = data_manager.get_employees()
            
            # 本地进行简单筛选
            if self.current_filter != "全部":
                filtered_data = [e for e in self.employee_data if e.get('department') == self.current_filter]
            else:
                filtered_data = self.employee_data

            if self.search_keyword:
                kw = self.search_keyword.lower()
                filtered_data = [
                    e for e in filtered_data 
                    if kw in e.get('name', '').lower() or 
                       kw in e.get('position', '').lower() or
                       str(e.get('id', '')) == kw
                ]

            # 清空并重新填充UI
            for widget in self.employees_container.winfo_children():
                widget.destroy()
            
            if not filtered_data:
                tk.Label(self.employees_container, text="未找到符合条件的员工。", bg=self.colors['background']).pack(pady=50)
            else:
                for emp in filtered_data:
                    self.create_employee_card(self.employees_container, emp)

            self.update_statistics()
        except Exception as e:
            messagebox.showerror("刷新失败", f"刷新员工列表时出错: {e}")
    
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

        # 从数据库加载数据
        try:
            self.employee_data = data_manager.get_employees()
        except Exception as e:
            messagebox.showerror("数据加载失败", f"无法从数据库加载员工信息: {e}")
            self.employee_data = []

        # 设置父框架背景
        self.parent_frame.configure(bg=self.colors['background'])
        
        # 创建主框架
        main_frame = tk.Frame(self.parent_frame, bg=self.colors['background'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # 创建标题和操作按钮
        # ... (UI creation code) ...

        # 最后刷新列表
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
