#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
客户管理模块
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from typing import Dict, List, Any, Union
import re

class CustomerModule:
    def __init__(self, parent_frame, title_frame):
        self.parent_frame = parent_frame
        self.title_frame = title_frame
        
        # 客户数据
        self.customer_data = [
            {"id": 1, "name": "张三", "phone": "13800138001", "email": "zhangsan@email.com", "address": "北京市朝阳区xxx街道", "type": "个人客户"},
            {"id": 2, "name": "李四", "phone": "13800138002", "email": "lisi@email.com", "address": "北京市海淀区xxx路", "type": "企业客户"},
            {"id": 3, "name": "王五", "phone": "13800138003", "email": "wangwu@email.com", "address": "北京市西城区xxx胡同", "type": "个人客户"},
            {"id": 4, "name": "赵六", "phone": "13800138004", "email": "zhaoliu@email.com", "address": "北京市东城区xxx大街", "type": "VIP客户"},
            {"id": 5, "name": "美食公司", "phone": "13900139001", "email": "info@food.com", "address": "北京市丰台区商业街88号", "type": "企业客户"},
        ]
        
    def show(self):
        """显示客户管理模块"""
        # 清空标题栏
        for widget in self.title_frame.winfo_children():
            widget.destroy()
            
        # 清空内容区域
        for widget in self.parent_frame.winfo_children():
            widget.destroy()
        
        # 标题
        title_label = tk.Label(self.title_frame, text="👥 客户管理", font=("微软雅黑", 16, "bold"),
                             bg="#ffffff", fg="#2c3e50")
        title_label.pack(side="left", padx=20, pady=15)
        
        # 状态提醒区域
        status_frame = tk.Frame(self.title_frame, bg="#ffffff")
        status_frame.pack(side="left", padx=(20, 0), pady=15)
        
        self.status_label = tk.Label(status_frame, text="💡 点击选择客户以启用修改功能", 
                                   font=("微软雅黑", 10),
                                   bg="#ffffff", fg="#7f8c8d")
        self.status_label.pack()
        
        # 工具栏
        toolbar_frame = tk.Frame(self.title_frame, bg="#ffffff")
        toolbar_frame.pack(side="right", padx=20, pady=15)
        
        # 修改客户按钮（初始禁用）
        self.edit_btn = tk.Button(toolbar_frame, text="🔧 修改客户", font=("微软雅黑", 10),
                                bg="#f39c12", fg="white", bd=0, padx=15, pady=5,
                                cursor="hand2", command=self.edit_selected_item,
                                state="disabled")
        self.edit_btn.pack(side="right", padx=(5,20))
        
        add_btn = tk.Button(toolbar_frame, text="➕ 添加客户", font=("微软雅黑", 10),
                          bg="#9b59b6", fg="white", bd=0, padx=15, pady=5,
                          cursor="hand2", command=self.add_customer_item)
        add_btn.pack(side="right", padx=5)
        
        # 主内容
        content_frame = tk.Frame(self.parent_frame, bg="#ffffff")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # 创建表格
        columns = ("ID", "客户姓名", "电话", "邮箱", "地址", "客户类型")
        tree = ttk.Treeview(content_frame, columns=columns, show="headings", height=15)
        
        # 设置列标题和宽度
        column_widths = [60, 120, 120, 180, 250, 100]
        for i, (col, width) in enumerate(zip(columns, column_widths)):
            tree.heading(col, text=col)
            tree.column(col, width=width, anchor="center")
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(content_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        # 填充数据
        for customer in self.customer_data:
            tree.insert("", "end", values=(
                customer["id"], customer["name"], customer["phone"], 
                customer["email"], customer["address"], customer["type"]
            ))
        
        # 布局
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # 保存tree引用以便后续使用
        self.tree = tree
        
        # 单击选择事件处理
        tree.bind("<<TreeviewSelect>>", self.on_item_select)
        
        # 双击编辑功能
        tree.bind("<Double-1>", lambda e: self.edit_customer_item(tree))
        
    def add_customer_item(self):
        """添加客户项目"""
        # 创建添加客户对话框
        dialog = tk.Toplevel()
        dialog.title("添加客户")
        dialog.geometry("450x400")
        dialog.configure(bg="#f8f9fa")
        dialog.resizable(False, False)
        dialog.grab_set()  # 模态对话框
        
        # 居中显示对话框
        dialog.transient(self.parent_frame.winfo_toplevel())
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (450 // 2)
        y = (dialog.winfo_screenheight() // 2) - (400 // 2)
        dialog.geometry(f"450x400+{x}+{y}")
        
        # 标题
        title_frame = tk.Frame(dialog, bg="#9b59b6", height=60)
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text="👥 添加客户", 
                              font=("微软雅黑", 16, "bold"),
                              bg="#9b59b6", fg="white")
        title_label.pack(pady=15)
        
        # 表单区域
        form_frame = tk.Frame(dialog, bg="#f8f9fa")
        form_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        # 输入字段配置
        fields = [
            ("客户姓名", "name", "text"),
            ("联系电话", "phone", "phone"),
            ("邮箱地址", "email", "email"),
            ("详细地址", "address", "text"),
            ("客户类型", "type", "select")
        ]
        
        # 存储输入控件的字典
        entries: Dict[str, Union[tk.Entry, ttk.Combobox]] = {}
        
        # 创建输入字段
        for i, (label_text, field_name, field_type) in enumerate(fields):
            # 标签
            label = tk.Label(form_frame, text=label_text, 
                           font=("微软雅黑", 11, "bold"),
                           bg="#f8f9fa", fg="#2c3e50")
            label.grid(row=i, column=0, sticky="w", pady=(10, 5))
            
            # 输入控件
            entry: Union[tk.Entry, ttk.Combobox, None] = None
            if field_type == "text":
                entry = tk.Entry(form_frame, font=("微软雅黑", 11),
                               width=30, relief="solid", bd=1)
                entry.grid(row=i, column=1, sticky="ew", pady=(0, 5))
                
            elif field_type == "phone":
                entry = tk.Entry(form_frame, font=("微软雅黑", 11),
                               width=30, relief="solid", bd=1)
                entry.grid(row=i, column=1, sticky="ew", pady=(0, 5))
                # 添加电话格式提示
                hint_label = tk.Label(form_frame, text="格式: 13800138000", 
                                    font=("微软雅黑", 9),
                                    bg="#f8f9fa", fg="#7f8c8d")
                hint_label.grid(row=i, column=2, sticky="w", padx=(10, 0))
                
            elif field_type == "email":
                entry = tk.Entry(form_frame, font=("微软雅黑", 11),
                               width=30, relief="solid", bd=1)
                entry.grid(row=i, column=1, sticky="ew", pady=(0, 5))
                # 添加邮箱格式提示
                hint_label = tk.Label(form_frame, text="格式: user@example.com", 
                                    font=("微软雅黑", 9),
                                    bg="#f8f9fa", fg="#7f8c8d")
                hint_label.grid(row=i, column=2, sticky="w", padx=(10, 0))
                
            elif field_type == "select":
                entry = ttk.Combobox(form_frame, font=("微软雅黑", 11),
                                   width=28, state="readonly")
                entry['values'] = ("个人客户", "企业客户", "VIP客户")
                entry.set("个人客户")  # 默认值
                entry.grid(row=i, column=1, sticky="ew", pady=(0, 5))
                
            if entry:
                entries[field_name] = entry
        
        # 设置第二列的权重，使输入框可以拉伸
        form_frame.columnconfigure(1, weight=1)
        
        # 按钮区域
        button_frame = tk.Frame(dialog, bg="#f8f9fa")
        button_frame.pack(fill="x", padx=30, pady=(0, 20))
        
        # 取消按钮
        cancel_btn = tk.Button(button_frame, text="取消", 
                             font=("微软雅黑", 11),
                             bg="#95a5a6", fg="white", bd=0,
                             padx=20, pady=8, cursor="hand2",
                             command=dialog.destroy)
        cancel_btn.pack(side="right", padx=(15, 40))
        
        # 确定按钮
        def save_item():
            try:
                # 验证输入
                name = entries["name"].get().strip()
                if not name:
                    messagebox.showerror("错误", "请输入客户姓名")
                    return
                
                phone = entries["phone"].get().strip()
                if not phone:
                    messagebox.showerror("错误", "请输入联系电话")
                    return
                
                # 验证电话号码格式
                if not re.match(r'^1[3-9]\d{9}$', phone):
                    messagebox.showerror("错误", "请输入正确的手机号码格式")
                    return
                
                email = entries["email"].get().strip()
                if not email:
                    messagebox.showerror("错误", "请输入邮箱地址")
                    return
                
                # 验证邮箱格式
                email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                if not re.match(email_pattern, email):
                    messagebox.showerror("错误", "请输入正确的邮箱格式")
                    return
                
                address = entries["address"].get().strip()
                if not address:
                    messagebox.showerror("错误", "请输入详细地址")
                    return
                
                customer_type = entries["type"].get()
                
                # 检查客户是否已存在
                for customer in self.customer_data:
                    if customer["phone"] == phone:
                        messagebox.showerror("错误", "该电话号码的客户已存在")
                        return
                    if customer["email"] == email:
                        messagebox.showerror("错误", "该邮箱地址的客户已存在")
                        return
                
                # 生成新ID
                new_id = max([customer["id"] for customer in self.customer_data]) + 1 if self.customer_data else 1
                
                # 创建新客户数据
                new_customer = {
                    "id": new_id,
                    "name": name,
                    "phone": phone,
                    "email": email,
                    "address": address,
                    "type": customer_type
                }
                
                # 添加到数据中
                self.customer_data.append(new_customer)
                
                messagebox.showinfo("成功", f"成功添加客户：{name}")
                dialog.destroy()
                
                # 刷新显示
                self.show()
                
            except Exception as e:
                messagebox.showerror("错误", f"添加失败：{str(e)}")
        
        save_btn = tk.Button(button_frame, text="💾 确定添加", 
                           font=("微软雅黑", 11, "bold"),
                           bg="#9b59b6", fg="white", bd=0,
                           padx=20, pady=8, cursor="hand2",
                           command=save_item)
        save_btn.pack(side="right", padx=(10, 0))
        
        # 设置焦点到第一个输入框
        entries["name"].focus()
        
        # 回车键提交
        dialog.bind('<Return>', lambda e: save_item())
    
    def edit_customer_item(self, tree):
        """编辑客户项目"""
        selected_items = tree.selection()
        if not selected_items:
            messagebox.showwarning("提示", "请先选择要编辑的客户")
            return
        
        # 获取选中的客户数据
        item_values = tree.item(selected_items[0])['values']
        customer_id = int(item_values[0])
        
        # 找到对应的客户数据
        current_customer = None
        for customer in self.customer_data:
            if customer["id"] == customer_id:
                current_customer = customer
                break
        
        if not current_customer:
            messagebox.showerror("错误", "未找到客户数据")
            return
        
        # 创建编辑客户对话框
        dialog = tk.Toplevel()
        dialog.title("编辑客户")
        dialog.geometry("450x400")
        dialog.configure(bg="#f8f9fa")
        dialog.resizable(False, False)
        dialog.grab_set()  # 模态对话框
        
        # 居中显示对话框
        dialog.transient(self.parent_frame.winfo_toplevel())
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (450 // 2)
        y = (dialog.winfo_screenheight() // 2) - (400 // 2)
        dialog.geometry(f"450x400+{x}+{y}")
        
        # 标题
        title_frame = tk.Frame(dialog, bg="#f39c12", height=60)
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text="🔧 编辑客户", 
                              font=("微软雅黑", 16, "bold"),
                              bg="#f39c12", fg="white")
        title_label.pack(pady=15)
        
        # 表单区域
        form_frame = tk.Frame(dialog, bg="#f8f9fa")
        form_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        # 输入字段配置
        fields = [
            ("客户姓名", "name", "text"),
            ("联系电话", "phone", "phone"),
            ("邮箱地址", "email", "email"),
            ("详细地址", "address", "text"),
            ("客户类型", "type", "select")
        ]
        
        # 存储输入控件的字典
        entries: Dict[str, Union[tk.Entry, ttk.Combobox]] = {}
        
        # 创建输入字段
        for i, (label_text, field_name, field_type) in enumerate(fields):
            # 标签
            label = tk.Label(form_frame, text=label_text, 
                           font=("微软雅黑", 11, "bold"),
                           bg="#f8f9fa", fg="#2c3e50")
            label.grid(row=i, column=0, sticky="w", pady=(10, 5))
            
            # 输入控件
            entry: Union[tk.Entry, ttk.Combobox, None] = None
            if field_type == "text":
                entry = tk.Entry(form_frame, font=("微软雅黑", 11),
                               width=30, relief="solid", bd=1)
                entry.grid(row=i, column=1, sticky="ew", pady=(0, 5))
                
            elif field_type == "phone":
                entry = tk.Entry(form_frame, font=("微软雅黑", 11),
                               width=30, relief="solid", bd=1)
                entry.grid(row=i, column=1, sticky="ew", pady=(0, 5))
                # 添加电话格式提示
                hint_label = tk.Label(form_frame, text="格式: 13800138000", 
                                    font=("微软雅黑", 9),
                                    bg="#f8f9fa", fg="#7f8c8d")
                hint_label.grid(row=i, column=2, sticky="w", padx=(10, 0))
                
            elif field_type == "email":
                entry = tk.Entry(form_frame, font=("微软雅黑", 11),
                               width=30, relief="solid", bd=1)
                entry.grid(row=i, column=1, sticky="ew", pady=(0, 5))
                # 添加邮箱格式提示
                hint_label = tk.Label(form_frame, text="格式: user@example.com", 
                                    font=("微软雅黑", 9),
                                    bg="#f8f9fa", fg="#7f8c8d")
                hint_label.grid(row=i, column=2, sticky="w", padx=(10, 0))
                
            elif field_type == "select":
                entry = ttk.Combobox(form_frame, font=("微软雅黑", 11),
                                   width=28, state="readonly")
                entry['values'] = ("个人客户", "企业客户", "VIP客户")
                entry.grid(row=i, column=1, sticky="ew", pady=(0, 5))
                
            if entry:
                # 填入当前数据
                if field_type == "select" and isinstance(entry, ttk.Combobox):
                    # 对于 Combobox，使用 set 方法
                    entry.set(current_customer[field_name])
                elif isinstance(entry, tk.Entry):
                    # 对于 Entry，使用 insert 方法
                    entry.insert(0, str(current_customer[field_name]))
                entries[field_name] = entry
        
        # 设置第二列的权重，使输入框可以拉伸
        form_frame.columnconfigure(1, weight=1)
        
        # 按钮区域
        button_frame = tk.Frame(dialog, bg="#f8f9fa")
        button_frame.pack(fill="x", padx=30, pady=(0, 20))
        
        # 删除按钮
        def delete_customer():
            result = messagebox.askyesno("确认删除", 
                                       f"确定要删除客户 '{current_customer['name']}' 吗？\n此操作不可撤销！")
            if result:
                # 从数据中删除
                self.customer_data.remove(current_customer)
                messagebox.showinfo("成功", f"已删除客户：{current_customer['name']}")
                dialog.destroy()
                # 刷新显示
                self.show()
        
        delete_btn = tk.Button(button_frame, text="🗑️ 删除", 
                             font=("微软雅黑", 11),
                             bg="#e74c3c", fg="white", bd=0,
                             padx=15, pady=8, cursor="hand2",
                             command=delete_customer)
        delete_btn.pack(side="left")
        
        # 取消按钮
        cancel_btn = tk.Button(button_frame, text="取消", 
                             font=("微软雅黑", 11),
                             bg="#95a5a6", fg="white", bd=0,
                             padx=20, pady=8, cursor="hand2",
                             command=dialog.destroy)
        cancel_btn.pack(side="right", padx=(10, 0))
        
        # 保存按钮
        def save_changes():
            try:
                # 验证输入
                name = entries["name"].get().strip()
                if not name:
                    messagebox.showerror("错误", "请输入客户姓名")
                    return
                
                phone = entries["phone"].get().strip()
                if not phone:
                    messagebox.showerror("错误", "请输入联系电话")
                    return
                
                # 验证电话号码格式
                if not re.match(r'^1[3-9]\d{9}$', phone):
                    messagebox.showerror("错误", "请输入正确的手机号码格式")
                    return
                
                email = entries["email"].get().strip()
                if not email:
                    messagebox.showerror("错误", "请输入邮箱地址")
                    return
                
                # 验证邮箱格式
                email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                if not re.match(email_pattern, email):
                    messagebox.showerror("错误", "请输入正确的邮箱格式")
                    return
                
                address = entries["address"].get().strip()
                if not address:
                    messagebox.showerror("错误", "请输入详细地址")
                    return
                
                customer_type = entries["type"].get()
                
                # 检查电话和邮箱是否被其他客户使用
                for customer in self.customer_data:
                    if customer["id"] != current_customer["id"]:
                        if customer["phone"] == phone:
                            messagebox.showerror("错误", "该电话号码已被其他客户使用")
                            return
                        if customer["email"] == email:
                            messagebox.showerror("错误", "该邮箱地址已被其他客户使用")
                            return
                
                # 更新客户数据
                current_customer["name"] = name
                current_customer["phone"] = phone
                current_customer["email"] = email
                current_customer["address"] = address
                current_customer["type"] = customer_type
                
                messagebox.showinfo("成功", f"成功更新客户：{name}")
                dialog.destroy()
                
                # 刷新显示
                self.show()
                
            except Exception as e:
                messagebox.showerror("错误", f"保存失败：{str(e)}")
        
        save_btn = tk.Button(button_frame, text="💾 保存修改", 
                           font=("微软雅黑", 11, "bold"),
                           bg="#f39c12", fg="white", bd=0,
                           padx=20, pady=8, cursor="hand2",
                           command=save_changes)
        save_btn.pack(side="right", padx=(10, 0))
        
        # 设置焦点到第一个输入框
        entries["name"].focus()
        entries["name"].selection_range(0, tk.END)  # 选中所有文本便于编辑
        
        # 回车键提交
        dialog.bind('<Return>', lambda e: save_changes())
        
    def on_item_select(self, event):
        """处理项目选择事件"""
        selected_items = self.tree.selection()
        if selected_items:
            # 获取选中的客户信息
            item_values = self.tree.item(selected_items[0])['values']
            if item_values:
                customer_name = item_values[1]  # 客户姓名在第二列
                customer_type = item_values[5]  # 客户类型在第六列
                
                # 更新状态提醒
                self.status_label.config(
                    text=f"✅ 已选中：{customer_name} ({customer_type})",
                    fg="#27ae60"
                )
            
            # 有选中项时启用修改按钮
            self.edit_btn.config(state="normal", bg="#f39c12")
        else:
            # 无选中项时禁用修改按钮和更新状态
            self.edit_btn.config(state="disabled", bg="#bdc3c7")
            self.status_label.config(
                text="💡 点击选择客户以启用修改功能",
                fg="#7f8c8d"
            )
    
    def edit_selected_item(self):
        """编辑选中的客户项目"""
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("提示", "请先选择要修改的客户")
            return
        
        # 调用编辑功能
        self.edit_customer_item(self.tree)
