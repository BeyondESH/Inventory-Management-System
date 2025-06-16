#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
餐食配置模块
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from typing import Dict, List, Any, Union
import re

class MealModule:
    def __init__(self, parent_frame, title_frame):
        self.parent_frame = parent_frame
        self.title_frame = title_frame
        
        # 餐食配置数据
        self.meal_data = [
            {"id": 1, "name": "番茄牛肉面", "price": 25.0, "active": True, "description": "经典番茄牛肉面", "category": "面食", "cook_time": 15},
            {"id": 2, "name": "鸡蛋炒饭", "price": 18.0, "active": True, "description": "香滑鸡蛋炒饭", "category": "米饭", "cook_time": 10},
            {"id": 3, "name": "蒸蛋羹", "price": 12.0, "active": True, "description": "嫩滑蒸蛋羹", "category": "汤品", "cook_time": 8},
            {"id": 4, "name": "牛肉汉堡", "price": 32.0, "active": True, "description": "美式牛肉汉堡", "category": "西式", "cook_time": 12},
            {"id": 5, "name": "素食沙拉", "price": 22.0, "active": False, "description": "健康素食沙拉", "category": "沙拉", "cook_time": 5},
            {"id": 6, "name": "红烧肉", "price": 35.0, "active": True, "description": "传统红烧肉", "category": "中式", "cook_time": 25},
        ]
        
        # 当前选中的项目
        self.selected_item = None
    
    def show(self):
        """显示餐食配置模块"""
        # 清空标题栏
        for widget in self.title_frame.winfo_children():
            widget.destroy()
            
        # 清空内容区域
        for widget in self.parent_frame.winfo_children():
            widget.destroy()
        
        # 标题
        title_label = tk.Label(self.title_frame, text="🍜 餐食配置", font=("微软雅黑", 16, "bold"),
                             bg="#ffffff", fg="#2c3e50")
        title_label.pack(side="left", padx=20, pady=15)
        
        # 状态提醒区域
        status_frame = tk.Frame(self.title_frame, bg="#ffffff")
        status_frame.pack(side="left", padx=(20, 0), pady=15)
        
        self.status_label = tk.Label(status_frame, text="💡 点击选择餐食以启用修改功能", 
                                   font=("微软雅黑", 10),
                                   bg="#ffffff", fg="#7f8c8d")
        self.status_label.pack()
        
        # 工具栏
        toolbar_frame = tk.Frame(self.title_frame, bg="#ffffff")
        toolbar_frame.pack(side="right", padx=20, pady=15)
        
        # 修改餐食按钮（初始禁用）
        self.edit_btn = tk.Button(toolbar_frame, text="🔧 修改餐食", font=("微软雅黑", 10),
                                bg="#f39c12", fg="white", bd=0, padx=15, pady=5,
                                cursor="hand2", command=self.edit_selected_item,
                                state="disabled")
        self.edit_btn.pack(side="right", padx=(5,20))
        
        add_btn = tk.Button(toolbar_frame, text="➕ 添加餐食", font=("微软雅黑", 10),
                          bg="#e67e22", fg="white", bd=0, padx=15, pady=5,
                          cursor="hand2", command=self.add_meal_item)
        add_btn.pack(side="right", padx=5)
        
        # 主内容
        content_frame = tk.Frame(self.parent_frame, bg="#ffffff")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # 创建表格
        columns = ("ID", "餐食名称", "价格", "分类", "制作时间", "描述", "状态")
        tree = ttk.Treeview(content_frame, columns=columns, show="headings", height=15)
        
        # 设置列标题和宽度
        column_widths = [60, 120, 80, 80, 90, 200, 80]
        for i, (col, width) in enumerate(zip(columns, column_widths)):
            tree.heading(col, text=col)
            tree.column(col, width=width, anchor="center")
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(content_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        # 填充数据
        for meal in self.meal_data:
            status = "✅ 启用中" if meal["active"] else "❌ 已停用"
            tree.insert("", "end", values=(
                meal["id"], meal["name"], f"¥{meal['price']}", meal["category"],
                f"{meal['cook_time']}分钟", meal["description"], status
            ))
        
        # 布局
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # 保存tree引用以便后续使用
        self.tree = tree
        
        # 单击选择事件处理
        tree.bind("<<TreeviewSelect>>", self.on_item_select)
        
        # 双击编辑功能
        tree.bind("<Double-1>", lambda e: self.edit_selected_item())
        
    def on_item_select(self, event):
        """处理项目选择事件"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            meal_id = int(item['values'][0])
            self.selected_item = next((meal for meal in self.meal_data if meal['id'] == meal_id), None)
            
            if self.selected_item:
                # 更新状态提醒
                self.status_label.config(
                    text=f"📋 已选择餐食: {self.selected_item['name']} (点击修改餐食按钮编辑)",
                    fg="#2980b9"
                )
                # 启用修改按钮
                self.edit_btn.config(state="normal", bg="#3498db")
            else:
                self.clear_selection()
        else:
            self.clear_selection()
    
    def clear_selection(self):
        """清除选择状态"""
        self.selected_item = None
        self.status_label.config(
            text="💡 点击选择餐食以启用修改功能",
            fg="#7f8c8d"
        )
        self.edit_btn.config(state="disabled", bg="#bdc3c7")
    
    def edit_selected_item(self):
        """编辑选中的餐食"""
        if not self.selected_item:
            messagebox.showwarning("提示", "请先选择要编辑的餐食！")
            return
        
        self.show_meal_dialog(self.selected_item)
    
    def add_meal_item(self):
        """添加餐食项目"""
        self.show_meal_dialog()
    
    def show_meal_dialog(self, meal=None):
        """显示餐食编辑对话框"""
        dialog = tk.Toplevel()
        dialog.title("编辑餐食" if meal else "添加餐食")
        dialog.geometry("480x520")
        dialog.configure(bg="#f8f9fa")
        dialog.resizable(False, False)
        dialog.grab_set()  # 模态对话框
        
        # 居中显示对话框
        dialog.transient(self.parent_frame.winfo_toplevel())
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (480 // 2)
        y = (dialog.winfo_screenheight() // 2) - (520 // 2)
        dialog.geometry(f"480x520+{x}+{y}")
        
        # 标题栏
        title_frame = tk.Frame(dialog, bg="#e67e22", height=60)
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)
        
        title_text = "🍜 编辑餐食" if meal else "🍜 添加餐食"
        title_label = tk.Label(title_frame, text=title_text, 
                              font=("微软雅黑", 16, "bold"),
                              bg="#e67e22", fg="white")
        title_label.pack(pady=15)
        
        # 表单区域
        form_frame = tk.Frame(dialog, bg="#f8f9fa")
        form_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        # 餐食名称
        name_label = tk.Label(form_frame, text="餐食名称", 
                           font=("微软雅黑", 11, "bold"),
                           bg="#f8f9fa", fg="#2c3e50")
        name_label.grid(row=0, column=0, sticky="w", pady=(10, 5))
        name_entry = tk.Entry(form_frame, font=("微软雅黑", 11),
                            width=30, relief="solid", bd=1)
        name_entry.grid(row=0, column=1, sticky="ew", pady=(0, 5))
        
        # 价格
        price_label = tk.Label(form_frame, text="价格(元)", 
                            font=("微软雅黑", 11, "bold"),
                            bg="#f8f9fa", fg="#2c3e50")
        price_label.grid(row=1, column=0, sticky="w", pady=(10, 5))
        price_entry = tk.Entry(form_frame, font=("微软雅黑", 11),
                             width=30, relief="solid", bd=1)
        price_entry.grid(row=1, column=1, sticky="ew", pady=(0, 5))
        # 价格格式提示
        price_hint = tk.Label(form_frame, text="格式: 25.50", 
                            font=("微软雅黑", 9),
                            bg="#f8f9fa", fg="#7f8c8d")
        price_hint.grid(row=1, column=2, sticky="w", padx=(10, 0))
        
        # 分类
        category_label = tk.Label(form_frame, text="分类", 
                               font=("微软雅黑", 11, "bold"),
                               bg="#f8f9fa", fg="#2c3e50")
        category_label.grid(row=2, column=0, sticky="w", pady=(10, 5))
        category_var = tk.StringVar()
        category_combo = ttk.Combobox(form_frame, textvariable=category_var, 
                                    font=("微软雅黑", 11), width=28, state="readonly")
        category_combo['values'] = ["面食", "米饭", "汤品", "西式", "沙拉", "中式", "小食", "饮品"]
        category_combo.set("面食")  # 默认值
        category_combo.grid(row=2, column=1, sticky="ew", pady=(0, 5))
        
        # 制作时间
        cook_time_label = tk.Label(form_frame, text="制作时间(分钟)", 
                                 font=("微软雅黑", 11, "bold"),
                                 bg="#f8f9fa", fg="#2c3e50")
        cook_time_label.grid(row=3, column=0, sticky="w", pady=(10, 5))
        cook_time_entry = tk.Entry(form_frame, font=("微软雅黑", 11),
                                 width=30, relief="solid", bd=1)
        cook_time_entry.grid(row=3, column=1, sticky="ew", pady=(0, 5))
        # 时间格式提示
        time_hint = tk.Label(form_frame, text="格式: 15", 
                           font=("微软雅黑", 9),
                           bg="#f8f9fa", fg="#7f8c8d")
        time_hint.grid(row=3, column=2, sticky="w", padx=(10, 0))
        
        # 描述
        desc_label = tk.Label(form_frame, text="描述", 
                            font=("微软雅黑", 11, "bold"),
                            bg="#f8f9fa", fg="#2c3e50")
        desc_label.grid(row=4, column=0, sticky="w", pady=(10, 5))
        desc_text = tk.Text(form_frame, font=("微软雅黑", 11), 
                          width=30, height=4, relief="solid", bd=1)
        desc_text.grid(row=4, column=1, sticky="ew", pady=(0, 5))
        
        # 状态
        status_label = tk.Label(form_frame, text="状态", 
                              font=("微软雅黑", 11, "bold"),
                              bg="#f8f9fa", fg="#2c3e50")
        status_label.grid(row=5, column=0, sticky="w", pady=(10, 5))
        active_var = tk.BooleanVar(value=True)
        active_check = tk.Checkbutton(form_frame, text="启用此餐食", variable=active_var,
                                    font=("微软雅黑", 11), bg="#f8f9fa")
        active_check.grid(row=5, column=1, sticky="w", pady=(0, 5))
        
        # 如果是编辑模式，填充现有数据
        if meal:
            name_entry.insert(0, meal["name"])
            price_entry.insert(0, str(meal["price"]))
            category_var.set(meal["category"])
            cook_time_entry.insert(0, str(meal["cook_time"]))
            desc_text.insert("1.0", meal["description"])
            active_var.set(meal["active"])
        
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
        def save_meal():
            """保存餐食"""
            # 验证输入
            name = name_entry.get().strip()
            if not name:
                messagebox.showerror("错误", "请输入餐食名称")
                return
            
            try:
                price = float(price_entry.get().strip())
                if price <= 0:
                    raise ValueError()
            except ValueError:
                messagebox.showerror("错误", "请输入有效的价格")
                return
            
            category = category_var.get().strip()
            if not category:
                messagebox.showerror("错误", "请选择餐食分类")
                return
            
            try:
                cook_time = int(cook_time_entry.get().strip())
                if cook_time <= 0:
                    raise ValueError()
            except ValueError:
                messagebox.showerror("错误", "请输入有效的制作时间")
                return
            
            description = desc_text.get("1.0", "end-1c").strip()
            if not description:
                messagebox.showerror("错误", "请输入餐食描述")
                return
            
            # 保存数据
            if meal:  # 编辑模式
                meal["name"] = name
                meal["price"] = price
                meal["category"] = category
                meal["cook_time"] = cook_time
                meal["description"] = description
                meal["active"] = active_var.get()
                messagebox.showinfo("成功", "餐食修改成功！")
            else:  # 添加模式
                new_id = max([m["id"] for m in self.meal_data]) + 1 if self.meal_data else 1
                new_meal = {
                    "id": new_id,
                    "name": name,
                    "price": price,
                    "category": category,
                    "cook_time": cook_time,
                    "description": description,
                    "active": active_var.get()
                }
                self.meal_data.append(new_meal)
                messagebox.showinfo("成功", "餐食添加成功！")
            
            dialog.destroy()
            self.refresh_view()
        
        # 确定按钮
        save_btn = tk.Button(button_frame, text="确定", 
                           font=("微软雅黑", 11),
                           bg="#27ae60", fg="white", bd=0,
                           padx=20, pady=8, cursor="hand2",
                           command=save_meal)
        save_btn.pack(side="right", padx=(0, 15))
        
        # 删除按钮（仅编辑模式显示）
        if meal:
            def delete_meal():
                """删除餐食"""
                if messagebox.askyesno("确认删除", f"确定要删除餐食 '{meal['name']}' 吗？\n此操作不可撤销！"):
                    self.meal_data.remove(meal)
                    messagebox.showinfo("成功", "餐食删除成功！")
                    dialog.destroy()
                    self.refresh_view()
            
            delete_btn = tk.Button(button_frame, text="删除", 
                                 font=("微软雅黑", 11),
                                 bg="#e74c3c", fg="white", bd=0,
                                 padx=20, pady=8, cursor="hand2",
                                 command=delete_meal)
            delete_btn.pack(side="right", padx=(0, 15))
    
    def refresh_view(self):
        """刷新视图"""
        self.clear_selection()
        self.show()
    
    def toggle_meal_status(self, meal):
        """切换餐食状态"""
        meal["active"] = not meal["active"]
        status = "启用" if meal["active"] else "停用"
        messagebox.showinfo("状态更新", f"餐食 '{meal['name']}' 已{status}！")
        self.refresh_view()
