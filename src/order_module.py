#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
订单管理模块
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from typing import Dict, List, Any

class OrderModule:
    def __init__(self, parent_frame, title_frame):
        self.parent_frame = parent_frame
        self.title_frame = title_frame
        
        # 订单数据
        self.order_data = [
            {"id": 1001, "customer": "张三", "meal": "番茄牛肉面", "quantity": 2, "total": 50.0, "date": "2024-06-15", "status": "已完成"},
            {"id": 1002, "customer": "李四", "meal": "鸡蛋炒饭", "quantity": 1, "total": 18.0, "date": "2024-06-15", "status": "进行中"},
            {"id": 1003, "customer": "王五", "meal": "牛肉汉堡", "quantity": 3, "total": 96.0, "date": "2024-06-14", "status": "已接收"},
            {"id": 1004, "customer": "赵六", "meal": "蒸蛋羹", "quantity": 4, "total": 48.0, "date": "2024-06-14", "status": "已完成"},
        ]
        
    def show(self):
        """显示订单管理模块"""
        # 清空标题栏
        for widget in self.title_frame.winfo_children():
            widget.destroy()
            
        # 清空内容区域
        for widget in self.parent_frame.winfo_children():
            widget.destroy()
          # 标题
        title_label = tk.Label(self.title_frame, text="📋 订单管理", font=("微软雅黑", 16, "bold"),
                             bg="#ffffff", fg="#2c3e50")
        title_label.pack(side="left", padx=20, pady=15)
        
        # 状态提醒区域
        status_frame = tk.Frame(self.title_frame, bg="#ffffff")
        status_frame.pack(side="left", padx=(20, 0), pady=15)
        
        self.status_label = tk.Label(status_frame, text="💡 点击选择订单以启用修改功能", 
                                   font=("微软雅黑", 10),
                                   bg="#ffffff", fg="#7f8c8d")
        self.status_label.pack()
        
        # 工具栏
        toolbar_frame = tk.Frame(self.title_frame, bg="#ffffff")
        toolbar_frame.pack(side="right", padx=20, pady=15)
        
        # 修改订单按钮（初始禁用）
        self.edit_btn = tk.Button(toolbar_frame, text="🔧修改订单", font=("微软雅黑", 10),
                                bg="#f39c12", fg="white", bd=0, padx=15, pady=5,
                                cursor="hand2", command=self.edit_selected_item,
                                state="disabled")
        self.edit_btn.pack(side="right", padx=(5,20))
        
        add_btn = tk.Button(toolbar_frame, text="➕ 新建订单", font=("微软雅黑", 10),
                          bg="#3498db", fg="white", bd=0, padx=15, pady=5,
                          cursor="hand2", command=self.add_order_item)
        add_btn.pack(side="right", padx=5)
        
        # 主内容
        content_frame = tk.Frame(self.parent_frame, bg="#ffffff")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # 创建表格
        columns = ("订单号", "客户", "餐食", "数量", "总金额", "下单日期", "状态")
        tree = ttk.Treeview(content_frame, columns=columns, show="headings", height=15)
        
        # 设置列标题和宽度
        column_widths = [80, 100, 150, 60, 80, 100, 80]
        for i, (col, width) in enumerate(zip(columns, column_widths)):
            tree.heading(col, text=col)
            tree.column(col, width=width, anchor="center")
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(content_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        # 填充数据
        for order in self.order_data:
            tree.insert("", "end", values=(
                order["id"], order["customer"], order["meal"], order["quantity"],
                f"¥{order['total']}", order["date"], order["status"]
            ))
          # 布局
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # 保存tree引用以便后续使用
        self.tree = tree
        
        # 单击选择事件处理
        tree.bind("<<TreeviewSelect>>", self.on_item_select)
          # 双击编辑功能
        tree.bind("<Double-1>", lambda e: self.edit_order_item(tree))
        
    def add_order_item(self):
        """添加订单项目"""
        # 创建新建订单对话框
        dialog = tk.Toplevel()
        dialog.title("新建订单")
        dialog.geometry("450x450")
        dialog.configure(bg="#f8f9fa")
        dialog.resizable(False, False)
        dialog.grab_set()  # 模态对话框
        
        # 居中显示对话框
        dialog.transient(self.parent_frame.winfo_toplevel())
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (450 // 2)
        y = (dialog.winfo_screenheight() // 2) - (450 // 2)
        dialog.geometry(f"450x450+{x}+{y}")
        
        # 标题
        title_frame = tk.Frame(dialog, bg="#3498db", height=60)
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text="📋 新建订单", 
                              font=("微软雅黑", 16, "bold"),
                              bg="#3498db", fg="white")
        title_label.pack(pady=15)
        
        # 表单区域
        form_frame = tk.Frame(dialog, bg="#f8f9fa")
        form_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        # 输入字段配置
        fields = [
            ("客户姓名", "customer", "text"),
            ("餐食名称", "meal", "combo"),
            ("订单数量", "quantity", "number"),
            ("单价 (¥)", "unit_price", "number"),
            ("下单日期", "date", "date"),
            ("订单状态", "status", "combo_status")
        ]
        
        # 存储输入控件的字典
        entries = {}
        
        # 预定义的餐食选项
        meal_options = ["番茄牛肉面", "鸡蛋炒饭", "牛肉汉堡", "蒸蛋羹", "青椒肉丝", "宫保鸡丁", "麻婆豆腐", "红烧肉"]
        status_options = ["已接收", "进行中", "已完成", "已取消"]
        
        # 创建输入字段
        for i, (label_text, field_name, field_type) in enumerate(fields):
            # 标签
            label = tk.Label(form_frame, text=label_text, 
                           font=("微软雅黑", 11, "bold"),
                           bg="#f8f9fa", fg="#2c3e50")
            label.grid(row=i, column=0, sticky="w", pady=(10, 5))
            
            # 输入框
            entry = None
            if field_type == "text":
                entry = tk.Entry(form_frame, font=("微软雅黑", 11),
                               width=28, relief="solid", bd=1)
                entry.grid(row=i, column=1, sticky="ew", pady=(0, 5))
                
            elif field_type == "number":
                entry = tk.Entry(form_frame, font=("微软雅黑", 11),
                               width=28, relief="solid", bd=1)
                entry.grid(row=i, column=1, sticky="ew", pady=(0, 5))
                
            elif field_type == "combo":
                entry = ttk.Combobox(form_frame, font=("微软雅黑", 11),
                                   width=26, values=meal_options, state="normal")
                entry.grid(row=i, column=1, sticky="ew", pady=(0, 5))
                
            elif field_type == "combo_status":
                entry = ttk.Combobox(form_frame, font=("微软雅黑", 11),
                                   width=26, values=status_options, state="readonly")
                entry.set("已接收")  # 默认状态
                entry.grid(row=i, column=1, sticky="ew", pady=(0, 5))
                
            elif field_type == "date":
                entry = tk.Entry(form_frame, font=("微软雅黑", 11),
                               width=28, relief="solid", bd=1)
                entry.grid(row=i, column=1, sticky="ew", pady=(0, 5))
                # 添加日期格式提示
                hint_label = tk.Label(form_frame, text="格式: YYYY-MM-DD", 
                                    font=("微软雅黑", 9),
                                    bg="#f8f9fa", fg="#7f8c8d")
                hint_label.grid(row=i, column=2, sticky="w", padx=(10, 0))
                
                # 设置默认日期为今天
                import datetime
                today = datetime.date.today().strftime("%Y-%m-%d")
                entry.insert(0, today)
                
            if entry:
                entries[field_name] = entry
        
        # 自动计算总金额的功能
        def calculate_total():
            try:
                quantity = float(entries["quantity"].get() or 0)
                unit_price = float(entries["unit_price"].get() or 0)
                total = quantity * unit_price
                total_label.config(text=f"总金额: ¥{total:.2f}")
            except ValueError:
                total_label.config(text="总金额: ¥0.00")
        
        # 总金额显示
        total_frame = tk.Frame(form_frame, bg="#f8f9fa")
        total_frame.grid(row=len(fields), column=0, columnspan=2, pady=(15, 10))
        
        total_label = tk.Label(total_frame, text="总金额: ¥0.00", 
                             font=("微软雅黑", 12, "bold"),
                             bg="#f8f9fa", fg="#e74c3c")
        total_label.pack()
        
        # 绑定计算事件
        entries["quantity"].bind("<KeyRelease>", lambda e: calculate_total())
        entries["unit_price"].bind("<KeyRelease>", lambda e: calculate_total())
        
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
        cancel_btn.pack(side="right", padx=(10, 0))
        
        # 确定按钮
        def save_order():
            try:
                # 验证输入
                customer = entries["customer"].get().strip()
                if not customer:
                    messagebox.showerror("错误", "请输入客户姓名")
                    return
                
                meal = entries["meal"].get().strip()
                if not meal:
                    messagebox.showerror("错误", "请选择或输入餐食名称")
                    return
                
                quantity = float(entries["quantity"].get())
                if quantity <= 0:
                    messagebox.showerror("错误", "订单数量必须大于0")
                    return
                
                unit_price = float(entries["unit_price"].get())
                if unit_price <= 0:
                    messagebox.showerror("错误", "单价必须大于0")
                    return
                
                date = entries["date"].get().strip()
                if not date:
                    messagebox.showerror("错误", "请输入下单日期")
                    return
                
                status = entries["status"].get()
                
                # 验证日期格式
                import datetime
                try:
                    datetime.datetime.strptime(date, "%Y-%m-%d")
                except ValueError:
                    messagebox.showerror("错误", "日期格式不正确，请使用 YYYY-MM-DD 格式")
                    return
                
                # 计算总金额
                total = quantity * unit_price
                
                # 生成新订单号
                new_id = max([order["id"] for order in self.order_data]) + 1 if self.order_data else 1001
                
                # 创建新订单数据
                new_order = {
                    "id": new_id,
                    "customer": customer,
                    "meal": meal,
                    "quantity": int(quantity),
                    "total": total,
                    "date": date,
                    "status": status
                }
                
                # 添加到数据中
                self.order_data.append(new_order)
                
                messagebox.showinfo("成功", f"成功创建订单：#{new_id}")
                dialog.destroy()
                
                # 刷新显示
                self.show()
                
            except ValueError:
                messagebox.showerror("错误", "请输入正确的数字格式")
            except Exception as e:
                messagebox.showerror("错误", f"创建失败：{str(e)}")
        
        confirm_btn = tk.Button(button_frame, text="创建订单", 
                              font=("微软雅黑", 11, "bold"),
                              bg="#3498db", fg="white", bd=0,
                              padx=20, pady=8, cursor="hand2",
                              command=save_order)
        confirm_btn.pack(side="right")
        
        # 设置焦点到第一个输入框
        entries["customer"].focus()
        
        # 回车键提交
        dialog.bind('<Return>', lambda e: save_order())
    
    def edit_order_item(self, tree):
        """编辑订单项目"""
        # 获取选中的项目
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("提示", "请选择要编辑的订单")
            return
        
        # 获取选中项目的数据
        item_values = tree.item(selected_item[0])['values']
        if not item_values:
            return
        
        # 根据ID找到对应的订单数据
        order_id = int(item_values[0])
        current_order = None
        for order in self.order_data:
            if order["id"] == order_id:
                current_order = order
                break
        
        if not current_order:
            messagebox.showerror("错误", "未找到对应的订单数据")
            return
        
        # 创建编辑订单对话框
        dialog = tk.Toplevel()
        dialog.title("编辑订单")
        dialog.geometry("450x500")
        dialog.configure(bg="#f8f9fa")
        dialog.resizable(False, False)
        dialog.grab_set()  # 模态对话框
        
        # 居中显示对话框
        dialog.transient(self.parent_frame.winfo_toplevel())
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (450 // 2)
        y = (dialog.winfo_screenheight() // 2) - (500 // 2)
        dialog.geometry(f"450x500+{x}+{y}")
        
        # 标题
        title_frame = tk.Frame(dialog, bg="#e67e22", height=60)
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text="🔧编辑订单", 
                              font=("微软雅黑", 16, "bold"),
                              bg="#e67e22", fg="white")
        title_label.pack(pady=15)
        
        # 表单区域
        form_frame = tk.Frame(dialog, bg="#f8f9fa")
        form_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        # 输入字段配置
        fields = [
            ("订单号", "id", "readonly"),
            ("客户姓名", "customer", "text"),
            ("餐食名称", "meal", "combo"),
            ("订单数量", "quantity", "number"),
            ("单价 (¥)", "unit_price", "number"),
            ("下单日期", "date", "date"),
            ("订单状态", "status", "combo_status")
        ]
        
        # 存储输入控件的字典
        entries = {}
        
        # 预定义的餐食选项
        meal_options = ["番茄牛肉面", "鸡蛋炒饭", "牛肉汉堡", "蒸蛋羹", "青椒肉丝", "宫保鸡丁", "麻婆豆腐", "红烧肉"]
        status_options = ["已接收", "进行中", "已完成", "已取消"]
        
        # 创建输入字段并填入当前数据
        for i, (label_text, field_name, field_type) in enumerate(fields):
            # 标签
            label = tk.Label(form_frame, text=label_text, 
                           font=("微软雅黑", 11, "bold"),
                           bg="#f8f9fa", fg="#2c3e50")
            label.grid(row=i, column=0, sticky="w", pady=(10, 5))
            
            # 输入框
            entry = None
            if field_type == "readonly":
                entry = tk.Entry(form_frame, font=("微软雅黑", 11),
                               width=28, relief="solid", bd=1, state="readonly")
                entry.grid(row=i, column=1, sticky="ew", pady=(0, 5))
                
            elif field_type == "text":
                entry = tk.Entry(form_frame, font=("微软雅黑", 11),
                               width=28, relief="solid", bd=1)
                entry.grid(row=i, column=1, sticky="ew", pady=(0, 5))
                
            elif field_type == "number":
                entry = tk.Entry(form_frame, font=("微软雅黑", 11),
                               width=28, relief="solid", bd=1)
                entry.grid(row=i, column=1, sticky="ew", pady=(0, 5))
                
            elif field_type == "combo":
                entry = ttk.Combobox(form_frame, font=("微软雅黑", 11),
                                   width=26, values=meal_options, state="normal")
                entry.grid(row=i, column=1, sticky="ew", pady=(0, 5))
                
            elif field_type == "combo_status":
                entry = ttk.Combobox(form_frame, font=("微软雅黑", 11),
                                   width=26, values=status_options, state="readonly")
                entry.grid(row=i, column=1, sticky="ew", pady=(0, 5))
                
            elif field_type == "date":
                entry = tk.Entry(form_frame, font=("微软雅黑", 11),
                               width=28, relief="solid", bd=1)
                entry.grid(row=i, column=1, sticky="ew", pady=(0, 5))
                # 添加日期格式提示
                hint_label = tk.Label(form_frame, text="格式: YYYY-MM-DD", 
                                    font=("微软雅黑", 9),
                                    bg="#f8f9fa", fg="#7f8c8d")
                hint_label.grid(row=i, column=2, sticky="w", padx=(10, 0))
                
            if entry:
                # 填入当前数据
                if field_name == "unit_price":
                    # 计算单价
                    unit_price = current_order["total"] / current_order["quantity"]
                    entry.insert(0, f"{unit_price:.2f}")
                else:
                    if field_name in current_order:
                        entry.insert(0, str(current_order[field_name]))
                entries[field_name] = entry
        
        # 自动计算总金额的功能
        def calculate_total():
            try:
                quantity = float(entries["quantity"].get() or 0)
                unit_price = float(entries["unit_price"].get() or 0)
                total = quantity * unit_price
                total_label.config(text=f"总金额: ¥{total:.2f}")
            except ValueError:
                total_label.config(text=f"总金额: ¥{current_order['total']:.2f}")
        
        # 总金额显示
        total_frame = tk.Frame(form_frame, bg="#f8f9fa")
        total_frame.grid(row=len(fields), column=0, columnspan=2, pady=(15, 10))
        
        total_label = tk.Label(total_frame, text=f"总金额: ¥{current_order['total']:.2f}", 
                             font=("微软雅黑", 12, "bold"),
                             bg="#f8f9fa", fg="#e74c3c")
        total_label.pack()
        
        # 绑定计算事件
        entries["quantity"].bind("<KeyRelease>", lambda e: calculate_total())
        entries["unit_price"].bind("<KeyRelease>", lambda e: calculate_total())
        
        # 设置第二列的权重，使输入框可以拉伸
        form_frame.columnconfigure(1, weight=1)
        
        # 按钮区域
        button_frame = tk.Frame(dialog, bg="#f8f9fa")
        button_frame.pack(fill="x", padx=30, pady=(0, 20))
        
        # 删除按钮
        def delete_order():
            result = messagebox.askyesno("确认删除", 
                                       f"确定要删除订单 #{current_order['id']} 吗？\n此操作不可撤销！")
            if result:
                # 从数据中删除
                self.order_data.remove(current_order)
                messagebox.showinfo("成功", f"已删除订单：#{current_order['id']}")
                dialog.destroy()
                # 刷新显示
                self.show()
        
        delete_btn = tk.Button(button_frame, text="🗑️ 删除", 
                             font=("微软雅黑", 11),
                             bg="#e74c3c", fg="white", bd=0,
                             padx=15, pady=8, cursor="hand2",
                             command=delete_order)
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
                customer = entries["customer"].get().strip()
                if not customer:
                    messagebox.showerror("错误", "请输入客户姓名")
                    return
                
                meal = entries["meal"].get().strip()
                if not meal:
                    messagebox.showerror("错误", "请选择或输入餐食名称")
                    return
                
                quantity = float(entries["quantity"].get())
                if quantity <= 0:
                    messagebox.showerror("错误", "订单数量必须大于0")
                    return
                
                unit_price = float(entries["unit_price"].get())
                if unit_price <= 0:
                    messagebox.showerror("错误", "单价必须大于0")
                    return
                
                date = entries["date"].get().strip()
                if not date:
                    messagebox.showerror("错误", "请输入下单日期")
                    return
                
                status = entries["status"].get()
                
                # 验证日期格式
                import datetime
                try:
                    datetime.datetime.strptime(date, "%Y-%m-%d")
                except ValueError:
                    messagebox.showerror("错误", "日期格式不正确，请使用 YYYY-MM-DD 格式")
                    return
                
                # 计算总金额
                total = quantity * unit_price
                
                # 更新订单数据
                current_order["customer"] = customer
                current_order["meal"] = meal
                current_order["quantity"] = int(quantity)
                current_order["total"] = total
                current_order["date"] = date
                current_order["status"] = status
                
                messagebox.showinfo("成功", f"成功更新订单：#{current_order['id']}")
                dialog.destroy()
                
                # 刷新显示
                self.show()
                
            except ValueError:
                messagebox.showerror("错误", "请输入正确的数字格式")
            except Exception as e:
                messagebox.showerror("错误", f"保存失败：{str(e)}")
        
        save_btn = tk.Button(button_frame, text="💾 保存修改", 
                           font=("微软雅黑", 11, "bold"),
                           bg="#f39c12", fg="white", bd=0,
                           padx=20, pady=8, cursor="hand2",
                           command=save_changes)
        save_btn.pack(side="right", padx=(10, 0))
        
        # 设置焦点到第一个可编辑输入框
        entries["customer"].focus()
        entries["customer"].selection_range(0, tk.END)  # 选中所有文本便于编辑
        
        # 回车键提交
        dialog.bind('<Return>', lambda e: save_changes())
    
    def on_item_select(self, event):
        """处理项目选择事件"""
        selected_items = self.tree.selection()
        if selected_items:
            # 获取选中的订单信息
            item_values = self.tree.item(selected_items[0])['values']
            if item_values:
                order_id = item_values[0]  # 订单号在第一列
                customer = item_values[1]  # 客户在第二列
                meal = item_values[2]  # 餐食在第三列
                status = item_values[6]  # 状态在第七列
                
                # 更新状态提醒
                self.status_label.config(
                    text=f"✅ 已选中：#{order_id} {customer} - {meal} ({status})",
                    fg="#27ae60"
                )
            
            # 有选中项时启用修改按钮
            self.edit_btn.config(state="normal", bg="#f39c12")
        else:
            # 无选中项时禁用修改按钮和更新状态
            self.edit_btn.config(state="disabled", bg="#bdc3c7")
            self.status_label.config(
                text="💡 点击选择订单以启用修改功能",
                fg="#7f8c8d"
            )
    
    def edit_selected_item(self):
        """编辑选中的订单项目"""
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("提示", "请先选择要修改的订单")
            return
        
        # 调用编辑功能
        self.edit_order_item(self.tree)
