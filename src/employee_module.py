#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
员工管理模块
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from typing import Dict, List, Any
import datetime
import json
import os

class EmployeeModule:
    def __init__(self, parent_frame, title_frame):
        self.parent_frame = parent_frame
        self.title_frame = title_frame
        
        # 员工数据存储
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
                "status": "在职"
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
                "status": "在职"
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
                "status": "在职"
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
                "status": "在职"
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
                "status": "离职"
            }
        ]
        
        # 部门列表
        self.departments = ["前厅部", "厨房部", "采购部", "财务部", "管理部"]
        
        # 职位列表
        self.positions = {
            "前厅部": ["前厅经理", "服务员", "收银员", "迎宾员"],
            "厨房部": ["厨师长", "主厨", "副厨", "洗菜工"],
            "采购部": ["采购经理", "采购员", "验收员"],
            "财务部": ["财务经理", "财务专员", "出纳"],
            "管理部": ["总经理", "副总经理", "人事专员", "行政专员"]
        }
    
    def show(self):
        """显示员工管理模块"""
        # 清空标题栏
        for widget in self.title_frame.winfo_children():
            widget.destroy()
            
        # 清空内容区域
        for widget in self.parent_frame.winfo_children():
            widget.destroy()
        
        # 标题
        title_label = tk.Label(self.title_frame, text="👥 员工管理", font=("微软雅黑", 16, "bold"),
                             bg="#ffffff", fg="#2c3e50")
        title_label.pack(side="left", padx=20, pady=15)
        
        # 工具栏
        toolbar_frame = tk.Frame(self.title_frame, bg="#ffffff")
        toolbar_frame.pack(side="right", padx=20, pady=15)
        
        # 添加员工按钮
        add_btn = tk.Button(toolbar_frame, text="➕ 添加员工", font=("微软雅黑", 10),
                          bg="#27ae60", fg="white", bd=0, padx=15, pady=5,
                          cursor="hand2", command=self.add_employee)
        add_btn.pack(side="right", padx=(5, 0))
        
        # 导出员工信息按钮
        export_btn = tk.Button(toolbar_frame, text="📊 导出信息", font=("微软雅黑", 10),
                             bg="#e67e22", fg="white", bd=0, padx=15, pady=5,
                             cursor="hand2", command=self.export_employee_info)
        export_btn.pack(side="right", padx=5)
        
        # 刷新按钮
        refresh_btn = tk.Button(toolbar_frame, text="🔄 刷新", font=("微软雅黑", 10),
                              bg="#3498db", fg="white", bd=0, padx=15, pady=5,
                              cursor="hand2", command=self.show)
        refresh_btn.pack(side="right", padx=5)
        
        # 搜索框
        search_frame = tk.Frame(toolbar_frame, bg="#ffffff")
        search_frame.pack(side="right", padx=10)
        
        tk.Label(search_frame, text="搜索:", font=("微软雅黑", 10),
               bg="#ffffff", fg="#2c3e50").pack(side="left")
        
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, 
                              font=("微软雅黑", 10), width=15)
        search_entry.pack(side="left", padx=(5, 0))
        search_entry.bind('<KeyRelease>', self.search_employees)
        
        # 创建主要内容区域
        self.create_main_content()
    
    def create_main_content(self):
        """创建主要内容区域"""
        # 主框架
        main_frame = tk.Frame(self.parent_frame, bg="#ffffff")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # 统计信息卡片
        self.create_statistics_cards(main_frame)
        
        # 员工列表
        self.create_employee_list(main_frame)
    
    def create_statistics_cards(self, parent):
        """创建统计信息卡片"""
        stats_frame = tk.Frame(parent, bg="#ffffff")
        stats_frame.pack(fill="x", pady=(0, 20))
        
        # 计算统计信息
        total_employees = len(self.employee_data)
        active_employees = len([emp for emp in self.employee_data if emp["status"] == "在职"])
        inactive_employees = total_employees - active_employees
        avg_salary = sum(emp["salary"] for emp in self.employee_data if emp["status"] == "在职") / max(active_employees, 1)
        
        # 总员工数卡片
        total_frame = tk.Frame(stats_frame, bg="#3498db", relief="raised", bd=2)
        total_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        tk.Label(total_frame, text="总员工数", font=("微软雅黑", 12, "bold"),
               bg="#3498db", fg="white").pack(pady=5)
        tk.Label(total_frame, text=str(total_employees), 
               font=("微软雅黑", 18, "bold"), bg="#3498db", fg="white").pack(pady=5)
        
        # 在职员工卡片
        active_frame = tk.Frame(stats_frame, bg="#27ae60", relief="raised", bd=2)
        active_frame.pack(side="left", fill="both", expand=True, padx=5)
        
        tk.Label(active_frame, text="在职员工", font=("微软雅黑", 12, "bold"),
               bg="#27ae60", fg="white").pack(pady=5)
        tk.Label(active_frame, text=str(active_employees),
               font=("微软雅黑", 18, "bold"), bg="#27ae60", fg="white").pack(pady=5)
        
        # 离职员工卡片
        inactive_frame = tk.Frame(stats_frame, bg="#e74c3c", relief="raised", bd=2)
        inactive_frame.pack(side="left", fill="both", expand=True, padx=5)
        
        tk.Label(inactive_frame, text="离职员工", font=("微软雅黑", 12, "bold"),
               bg="#e74c3c", fg="white").pack(pady=5)
        tk.Label(inactive_frame, text=str(inactive_employees),
               font=("微软雅黑", 18, "bold"), bg="#e74c3c", fg="white").pack(pady=5)
        
        # 平均薪资卡片
        salary_frame = tk.Frame(stats_frame, bg="#f39c12", relief="raised", bd=2)
        salary_frame.pack(side="right", fill="both", expand=True, padx=(5, 0))
        
        tk.Label(salary_frame, text="平均薪资", font=("微软雅黑", 12, "bold"),
               bg="#f39c12", fg="white").pack(pady=5)
        tk.Label(salary_frame, text=f"¥{avg_salary:,.0f}",
               font=("微软雅黑", 18, "bold"), bg="#f39c12", fg="white").pack(pady=5)
    
    def create_employee_list(self, parent):
        """创建员工列表"""
        # 列表标题
        list_title = tk.Label(parent, text="📋 员工信息列表", font=("微软雅黑", 14, "bold"),
                            bg="#ffffff", fg="#2c3e50")
        list_title.pack(anchor="w", pady=(0, 10))
        
        # 表格框架
        table_frame = tk.Frame(parent, bg="#ffffff")
        table_frame.pack(fill="both", expand=True)
        
        # 创建表格
        columns = ("ID", "姓名", "职位", "部门", "电话", "入职日期", "薪资", "状态")
        self.employee_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)
        
        # 设置列标题和宽度
        column_widths = [60, 80, 100, 80, 120, 100, 80, 60]
        for i, (col, width) in enumerate(zip(columns, column_widths)):
            self.employee_tree.heading(col, text=col)
            self.employee_tree.column(col, width=width, anchor="center")
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.employee_tree.yview)
        self.employee_tree.configure(yscrollcommand=scrollbar.set)
        
        # 填充数据
        self.refresh_employee_list()
        
        # 绑定双击事件
        self.employee_tree.bind("<Double-1>", self.edit_employee)
        
        # 绑定右键菜单
        self.employee_tree.bind("<Button-3>", self.show_context_menu)
        
        # 布局
        self.employee_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def refresh_employee_list(self, filtered_data=None):
        """刷新员工列表"""
        # 清空现有数据
        for item in self.employee_tree.get_children():
            self.employee_tree.delete(item)
        
        # 使用过滤数据或全部数据
        data_to_show = filtered_data if filtered_data is not None else self.employee_data
        
        # 填充数据
        for employee in data_to_show:
            status_color = "#27ae60" if employee["status"] == "在职" else "#e74c3c"
            values = (
                employee["id"],
                employee["name"],
                employee["position"],
                employee["department"],
                employee["phone"],
                employee["hire_date"],
                f"¥{employee['salary']:,.0f}",
                employee["status"]
            )
            
            item = self.employee_tree.insert("", "end", values=values)
            # 根据状态设置不同的标签颜色
            if employee["status"] == "离职":
                self.employee_tree.set(item, "状态", "🔴 离职")
            else:
                self.employee_tree.set(item, "状态", "🟢 在职")
    
    def search_employees(self, event=None):
        """搜索员工"""
        search_text = self.search_var.get().lower()
        if not search_text:
            self.refresh_employee_list()
            return
        
        # 过滤员工数据
        filtered_data = []
        for employee in self.employee_data:
            if (search_text in employee["name"].lower() or
                search_text in employee["position"].lower() or
                search_text in employee["department"].lower() or
                search_text in str(employee["id"])):
                filtered_data.append(employee)
        
        self.refresh_employee_list(filtered_data)
    
    def add_employee(self):
        """添加新员工"""
        dialog = EmployeeDialog(self.parent_frame, "添加员工", self.departments, self.positions)
        if dialog.result:
            # 生成新的员工ID
            max_id = max(emp["id"] for emp in self.employee_data) if self.employee_data else 1000
            new_employee = dialog.result
            new_employee["id"] = max_id + 1
            
            self.employee_data.append(new_employee)
            self.refresh_employee_list()
            self.show()  # 刷新统计信息
            messagebox.showinfo("成功", f"员工 {new_employee['name']} 添加成功！")
    
    def edit_employee(self, event=None):
        """编辑员工信息"""
        selection = self.employee_tree.selection()
        if not selection:
            messagebox.showwarning("提示", "请选择要编辑的员工！")
            return
        
        # 获取选中的员工信息
        item = selection[0]
        employee_id = int(self.employee_tree.item(item)["values"][0])
        
        # 找到对应的员工数据
        employee = next((emp for emp in self.employee_data if emp["id"] == employee_id), None)
        if not employee:
            messagebox.showerror("错误", "找不到员工信息！")
            return
        
        # 打开编辑对话框
        dialog = EmployeeDialog(self.parent_frame, "编辑员工", self.departments, self.positions, employee)
        if dialog.result:
            # 更新员工信息
            employee.update(dialog.result)
            self.refresh_employee_list()
            self.show()  # 刷新统计信息
            messagebox.showinfo("成功", f"员工 {employee['name']} 信息更新成功！")
    
    def show_context_menu(self, event):
        """显示右键菜单"""
        # 创建右键菜单
        context_menu = tk.Menu(self.parent_frame, tearoff=0)
        context_menu.add_command(label="📝 编辑", command=self.edit_employee)
        context_menu.add_command(label="🗑️ 删除", command=self.delete_employee)
        context_menu.add_separator()
        context_menu.add_command(label="📋 详细信息", command=self.show_employee_detail)
        
        # 显示菜单
        try:
            context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            context_menu.grab_release()
    
    def delete_employee(self):
        """删除员工"""
        selection = self.employee_tree.selection()
        if not selection:
            messagebox.showwarning("提示", "请选择要删除的员工！")
            return
        
        # 获取选中的员工信息
        item = selection[0]
        employee_id = int(self.employee_tree.item(item)["values"][0])
        employee_name = self.employee_tree.item(item)["values"][1]
        
        # 确认删除
        if messagebox.askyesno("确认删除", f"确定要删除员工 {employee_name} 吗？\n此操作不可撤销！"):
            # 从数据中删除
            self.employee_data = [emp for emp in self.employee_data if emp["id"] != employee_id]
            self.refresh_employee_list()
            self.show()  # 刷新统计信息
            messagebox.showinfo("成功", f"员工 {employee_name} 已删除！")
    
    def show_employee_detail(self):
        """显示员工详细信息"""
        selection = self.employee_tree.selection()
        if not selection:
            messagebox.showwarning("提示", "请选择要查看的员工！")
            return
        
        # 获取选中的员工信息
        item = selection[0]
        employee_id = int(self.employee_tree.item(item)["values"][0])
        employee = next((emp for emp in self.employee_data if emp["id"] == employee_id), None)
        
        if employee:
            EmployeeDetailDialog(self.parent_frame, employee)
    
    def export_employee_info(self):
        """导出员工信息"""
        try:
            # 创建导出内容
            export_content = "=== 员工信息导出 ===\n"
            export_content += f"导出时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            
            # 统计信息
            total_employees = len(self.employee_data)
            active_employees = len([emp for emp in self.employee_data if emp["status"] == "在职"])
            
            export_content += f"员工统计:\n"
            export_content += f"- 总员工数: {total_employees}\n"
            export_content += f"- 在职员工: {active_employees}\n"
            export_content += f"- 离职员工: {total_employees - active_employees}\n\n"
            
            # 员工详细信息
            export_content += "员工详细信息:\n"
            export_content += "-" * 80 + "\n"
            
            for employee in self.employee_data:
                export_content += f"员工ID: {employee['id']}\n"
                export_content += f"姓名: {employee['name']}\n"
                export_content += f"职位: {employee['position']}\n"
                export_content += f"部门: {employee['department']}\n"
                export_content += f"电话: {employee['phone']}\n"
                export_content += f"邮箱: {employee['email']}\n"
                export_content += f"入职日期: {employee['hire_date']}\n"
                export_content += f"薪资: ¥{employee['salary']:,.2f}\n"
                export_content += f"状态: {employee['status']}\n"
                export_content += "-" * 40 + "\n"
            
            # 保存到文件
            filename = f"员工信息_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            filepath = os.path.join(os.getcwd(), filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(export_content)
            
            messagebox.showinfo("导出成功", f"员工信息已导出到:\n{filepath}")
            
        except Exception as e:
            messagebox.showerror("导出失败", f"导出员工信息时出错：{str(e)}")


class EmployeeDialog:
    """员工信息对话框"""
    def __init__(self, parent, title, departments, positions, employee_data=None):
        self.result = None
        self.departments = departments
        self.positions = positions
        
        # 创建对话框
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("500x600")
        self.dialog.configure(bg="#f8f9fa")
        self.dialog.resizable(False, False)
        self.dialog.grab_set()
        
        # 居中显示
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (600 // 2)
        self.dialog.geometry(f"500x600+{x}+{y}")
        
        self.create_form(employee_data)
        
        # 等待对话框关闭
        self.dialog.wait_window()
    
    def create_form(self, employee_data):
        """创建表单"""
        # 标题栏
        title_frame = tk.Frame(self.dialog, bg="#34495e", height=60)
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text="👤 员工信息", 
                              font=("微软雅黑", 16, "bold"),
                              bg="#34495e", fg="white")
        title_label.pack(pady=15)
        
        # 表单区域
        form_frame = tk.Frame(self.dialog, bg="#f8f9fa")
        form_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        # 表单字段
        fields = [
            ("姓名", "name", "entry"),
            ("部门", "department", "combobox"),
            ("职位", "position", "combobox"),
            ("电话", "phone", "entry"),
            ("邮箱", "email", "entry"),
            ("入职日期", "hire_date", "entry"),
            ("薪资", "salary", "entry"),
            ("状态", "status", "combobox")
        ]
        
        self.form_vars = {}
        self.position_combo = None
        
        row = 0
        for field_name, field_key, field_type in fields:
            # 标签
            label = tk.Label(form_frame, text=f"{field_name}:", 
                           font=("微软雅黑", 11, "bold"),
                           bg="#f8f9fa", fg="#2c3e50")
            label.grid(row=row, column=0, sticky="w", pady=8)
            
            # 输入控件
            if field_type == "entry":
                var = tk.StringVar()
                entry = tk.Entry(form_frame, textvariable=var, font=("微软雅黑", 11),
                               width=25, relief="solid", bd=1)
                entry.grid(row=row, column=1, sticky="ew", pady=8, padx=(10, 0))
                self.form_vars[field_key] = var
                
            elif field_type == "combobox":
                var = tk.StringVar()
                if field_key == "department":
                    combo = ttk.Combobox(form_frame, textvariable=var, 
                                       values=self.departments, font=("微软雅黑", 11),
                                       width=23, state="readonly")
                    combo.bind('<<ComboboxSelected>>', self.on_department_change)
                elif field_key == "position":
                    combo = ttk.Combobox(form_frame, textvariable=var, 
                                       values=[], font=("微软雅黑", 11),
                                       width=23, state="readonly")
                    self.position_combo = combo
                elif field_key == "status":
                    combo = ttk.Combobox(form_frame, textvariable=var, 
                                       values=["在职", "离职"], font=("微软雅黑", 11),
                                       width=23, state="readonly")
                
                combo.grid(row=row, column=1, sticky="ew", pady=8, padx=(10, 0))
                self.form_vars[field_key] = var
            
            row += 1
        
        # 如果是编辑模式，填充现有数据
        if employee_data:
            for key, var in self.form_vars.items():
                if key in employee_data:
                    var.set(str(employee_data[key]))
            
            # 更新职位选项
            if employee_data.get("department"):
                self.update_positions(employee_data["department"])
        
        # 设置列权重
        form_frame.columnconfigure(1, weight=1)
        
        # 按钮区域
        button_frame = tk.Frame(self.dialog, bg="#f8f9fa")
        button_frame.pack(fill="x", padx=30, pady=(0, 20))
        
        # 取消按钮
        cancel_btn = tk.Button(button_frame, text="取消", 
                             font=("微软雅黑", 11),
                             bg="#95a5a6", fg="white", bd=0,
                             padx=20, pady=8, cursor="hand2",
                             command=self.dialog.destroy)
        cancel_btn.pack(side="right", padx=(15, 40))
        
        # 保存按钮
        save_btn = tk.Button(button_frame, text="保存", 
                           font=("微软雅黑", 11),
                           bg="#27ae60", fg="white", bd=0,
                           padx=20, pady=8, cursor="hand2",
                           command=self.save_employee)
        save_btn.pack(side="right", padx=(0, 15))
    
    def on_department_change(self, event=None):
        """部门选择改变时更新职位选项"""
        department = self.form_vars["department"].get()
        self.update_positions(department)
    
    def update_positions(self, department):
        """更新职位选项"""
        if department in self.positions and self.position_combo:
            self.position_combo.configure(values=self.positions[department])
            self.form_vars["position"].set("")  # 清空职位选择
    
    def save_employee(self):
        """保存员工信息"""
        try:
            # 验证必填字段
            required_fields = ["name", "department", "position", "phone", "hire_date", "salary", "status"]
            for field in required_fields:
                if not self.form_vars[field].get().strip():
                    messagebox.showerror("错误", f"请填写{field}！")
                    return
            
            # 验证薪资格式
            try:
                salary = float(self.form_vars["salary"].get())
                if salary < 0:
                    raise ValueError("薪资不能为负数")
            except ValueError:
                messagebox.showerror("错误", "请输入有效的薪资金额！")
                return
            
            # 验证日期格式
            hire_date = self.form_vars["hire_date"].get()
            try:
                datetime.datetime.strptime(hire_date, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("错误", "请输入正确的日期格式（YYYY-MM-DD）！")
                return
            
            # 构建结果数据
            self.result = {
                "name": self.form_vars["name"].get().strip(),
                "department": self.form_vars["department"].get(),
                "position": self.form_vars["position"].get(),
                "phone": self.form_vars["phone"].get().strip(),
                "email": self.form_vars["email"].get().strip(),
                "hire_date": hire_date,
                "salary": salary,
                "status": self.form_vars["status"].get()
            }
            
            self.dialog.destroy()
            
        except Exception as e:
            messagebox.showerror("错误", f"保存员工信息时出错：{str(e)}")


class EmployeeDetailDialog:
    """员工详细信息查看对话框"""
    def __init__(self, parent, employee_data):
        # 创建对话框
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("员工详细信息")
        self.dialog.geometry("400x500")
        self.dialog.configure(bg="#f8f9fa")
        self.dialog.resizable(False, False)
        self.dialog.grab_set()
        
        # 居中显示
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (500 // 2)
        self.dialog.geometry(f"400x500+{x}+{y}")
        
        self.create_detail_view(employee_data)
    
    def create_detail_view(self, employee_data):
        """创建详细信息视图"""
        # 标题栏
        title_frame = tk.Frame(self.dialog, bg="#34495e", height=60)
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text=f"👤 {employee_data['name']}", 
                              font=("微软雅黑", 16, "bold"),
                              bg="#34495e", fg="white")
        title_label.pack(pady=15)
        
        # 内容区域
        content_frame = tk.Frame(self.dialog, bg="#ffffff")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # 员工信息
        info_items = [
            ("员工ID", str(employee_data["id"])),
            ("姓名", employee_data["name"]),
            ("职位", employee_data["position"]),
            ("部门", employee_data["department"]),
            ("电话", employee_data["phone"]),
            ("邮箱", employee_data["email"]),
            ("入职日期", employee_data["hire_date"]),
            ("薪资", f"¥{employee_data['salary']:,.2f}"),
            ("状态", employee_data["status"])
        ]
        
        for i, (label, value) in enumerate(info_items):
            # 标签
            label_widget = tk.Label(content_frame, text=f"{label}:", 
                                  font=("微软雅黑", 11, "bold"),
                                  bg="#ffffff", fg="#2c3e50")
            label_widget.grid(row=i, column=0, sticky="w", pady=8)
            
            # 值
            value_widget = tk.Label(content_frame, text=value, 
                                  font=("微软雅黑", 11),
                                  bg="#ffffff", fg="#34495e")
            value_widget.grid(row=i, column=1, sticky="w", pady=8, padx=(20, 0))
        
        # 关闭按钮
        close_btn = tk.Button(content_frame, text="关闭", 
                            font=("微软雅黑", 11),
                            bg="#3498db", fg="white", bd=0,
                            padx=30, pady=8, cursor="hand2",
                            command=self.dialog.destroy)
        close_btn.grid(row=len(info_items), column=0, columnspan=2, pady=20)
