#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
库存管理模块
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from typing import Dict, List, Any

class InventoryModule:
    def __init__(self, parent_frame, title_frame):
        self.parent_frame = parent_frame
        self.title_frame = title_frame
        
        # 库存数据
        self.inventory_data = [
            {"id": 1, "name": "面粉", "current_stock": 50, "unit": "kg", "threshold": 10, "unit_cost": 3.5, "expiry": "2024-12-30"},
            {"id": 2, "name": "鸡蛋", "current_stock": 200, "unit": "个", "threshold": 50, "unit_cost": 0.8, "expiry": "2024-07-15"},
            {"id": 3, "name": "牛肉", "current_stock": 25, "unit": "kg", "threshold": 5, "unit_cost": 35.0, "expiry": "2024-07-01"},
            {"id": 4, "name": "番茄", "current_stock": 80, "unit": "kg", "threshold": 15, "unit_cost": 4.2, "expiry": "2024-06-25"},
            {"id": 5, "name": "一次性餐盒", "current_stock": 500, "unit": "个", "threshold": 100, "unit_cost": 0.5, "expiry": "2025-06-01"},
        ]
        
        # 菜品配方数据 - 定义每个菜品需要的原材料及其用量
        self.recipe_data = {
            "番茄牛肉面": {
                "面粉": 0.2,     # kg
                "牛肉": 0.15,    # kg  
                "番茄": 0.1,     # kg
                "鸡蛋": 1,       # 个
                "一次性餐盒": 1   # 个
            },
            "鸡蛋炒饭": {
                "鸡蛋": 2,       # 个
                "一次性餐盒": 1   # 个
            },
            "蒸蛋羹": {
                "鸡蛋": 3,       # 个
                "一次性餐盒": 1   # 个
            },
            "牛肉汉堡": {
                "面粉": 0.1,     # kg
                "牛肉": 0.2,     # kg
                "番茄": 0.05,    # kg
                "一次性餐盒": 1   # 个
            },
            "素食沙拉": {
                "番茄": 0.15,    # kg
                "一次性餐盒": 1   # 个
            },
            "红烧肉": {
                "牛肉": 0.25,    # kg
                "一次性餐盒": 1   # 个
            }
        }
        
    def show(self):
        """显示库存管理模块"""
        # 清空标题栏
        for widget in self.title_frame.winfo_children():
            widget.destroy()
            
        # 清空内容区域
        for widget in self.parent_frame.winfo_children():
            widget.destroy()
          # 标题
        title_label = tk.Label(self.title_frame, text="📦 库存管理", font=("微软雅黑", 16, "bold"),
                             bg="#ffffff", fg="#2c3e50")
        title_label.pack(side="left", padx=20, pady=15)
        
        # 状态提醒区域
        status_frame = tk.Frame(self.title_frame, bg="#ffffff")
        status_frame.pack(side="left", padx=(20, 0), pady=15)
        
        self.status_label = tk.Label(status_frame, text="💡 点击选择食材以启用修改功能", 
                                   font=("微软雅黑", 10),
                                   bg="#ffffff", fg="#7f8c8d")
        self.status_label.pack()
        
        # 工具栏
        toolbar_frame = tk.Frame(self.title_frame, bg="#ffffff")
        toolbar_frame.pack(side="right", padx=20, pady=15)
        
        # 修改库存按钮（初始禁用）
        self.edit_btn = tk.Button(toolbar_frame, text="🔧 修改库存", font=("微软雅黑", 10),
                                bg="#f39c12", fg="white", bd=0, padx=15, pady=5,
                                cursor="hand2", command=self.edit_selected_item,
                                state="disabled")
        self.edit_btn.pack(side="right", padx=(5,20))
        
        # 库存预警按钮
        warning_btn = tk.Button(toolbar_frame, text="⚠️ 库存预警", font=("微软雅黑", 10),
                              bg="#e74c3c", fg="white", bd=0, padx=15, pady=5,
                              cursor="hand2", command=self.show_stock_warnings)
        warning_btn.pack(side="right", padx=5)
        
        add_btn = tk.Button(toolbar_frame, text="➕ 添加食材", font=("微软雅黑", 10),
                          bg="#27ae60", fg="white", bd=0, padx=15, pady=5,
                          cursor="hand2", command=self.add_inventory_item)
        add_btn.pack(side="right", padx=5)
        
        # 主内容
        content_frame = tk.Frame(self.parent_frame, bg="#ffffff")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # 创建表格
        columns = ("ID", "食材名称", "当前库存", "单位", "安全库存", "单价", "过期日期", "状态")
        tree = ttk.Treeview(content_frame, columns=columns, show="headings", height=15)
        
        # 设置列标题和宽度
        column_widths = [60, 120, 100, 60, 100, 80, 120, 80]
        for i, (col, width) in enumerate(zip(columns, column_widths)):
            tree.heading(col, text=col)
            tree.column(col, width=width, anchor="center")
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(content_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        # 填充数据
        for item in self.inventory_data:
            status = "⚠️ 库存不足" if item["current_stock"] <= item["threshold"] else "✅ 正常"
            tree.insert("", "end", values=(
                item["id"], item["name"], item["current_stock"], item["unit"],
                item["threshold"], f"¥{item['unit_cost']}", item["expiry"], status
            ))
          # 布局
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # 保存tree引用以便后续使用
        self.tree = tree
        
        # 单击选择事件处理
        tree.bind("<<TreeviewSelect>>", self.on_item_select)
        
        # 双击编辑功能
        tree.bind("<Double-1>", lambda e: self.edit_inventory_item(tree))
        
    def add_inventory_item(self):
        """添加库存项目"""
        # 创建添加库存对话框
        dialog = tk.Toplevel()
        dialog.title("添加库存")
        dialog.geometry("400x400")
        dialog.configure(bg="#f8f9fa")
        dialog.resizable(False, False)
        dialog.grab_set()  # 模态对话框
        
        # 居中显示对话框
        dialog.transient(self.parent_frame.winfo_toplevel())
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (dialog.winfo_screenheight() // 2) - (500 // 2)
        dialog.geometry(f"400x400+{x}+{y}")
        
        # 标题
        title_frame = tk.Frame(dialog, bg="#3498db", height=60)
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text="📦 添加库存", 
                              font=("微软雅黑", 16, "bold"),
                              bg="#3498db", fg="white")
        title_label.pack(pady=15)
        
        # 表单区域
        form_frame = tk.Frame(dialog, bg="#f8f9fa")
        form_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        # 输入字段配置
        fields = [
            ("食材名称", "name", "text"),
            ("当前库存", "current_stock", "number"),
            ("单位", "unit", "text"),
            ("安全库存阈值", "threshold", "number"),
            ("单价 (¥)", "unit_cost", "number"),
            ("过期日期", "expiry", "date")
        ]
        
        # 存储输入控件的字典
        entries = {}
        
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
                               width=25, relief="solid", bd=1)
                entry.grid(row=i, column=1, sticky="ew", pady=(0, 5))
                
            elif field_type == "number":
                entry = tk.Entry(form_frame, font=("微软雅黑", 11),
                               width=25, relief="solid", bd=1)
                entry.grid(row=i, column=1, sticky="ew", pady=(0, 5))
                
            elif field_type == "date":
                entry = tk.Entry(form_frame, font=("微软雅黑", 11),
                               width=25, relief="solid", bd=1)
                entry.grid(row=i, column=1, sticky="ew", pady=(0, 5))
                # 添加日期格式提示
                hint_label = tk.Label(form_frame, text="格式: YYYY-MM-DD", 
                                    font=("微软雅黑", 9),
                                    bg="#f8f9fa", fg="#7f8c8d")
                hint_label.grid(row=i, column=2, sticky="w", padx=(10, 0))
                
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
                    messagebox.showerror("错误", "请输入食材名称")
                    return
                
                current_stock = float(entries["current_stock"].get())
                if current_stock < 0:
                    messagebox.showerror("错误", "当前库存不能为负数")
                    return
                    
                unit = entries["unit"].get().strip()
                if not unit:
                    messagebox.showerror("错误", "请输入单位")
                    return
                
                threshold = float(entries["threshold"].get())
                if threshold < 0:
                    messagebox.showerror("错误", "安全库存阈值不能为负数")
                    return
                
                unit_cost = float(entries["unit_cost"].get())
                if unit_cost < 0:
                    messagebox.showerror("错误", "单价不能为负数")
                    return
                
                expiry = entries["expiry"].get().strip()
                if not expiry:
                    messagebox.showerror("错误", "请输入过期日期")
                    return
                
                # 验证日期格式
                import datetime
                try:
                    datetime.datetime.strptime(expiry, "%Y-%m-%d")
                except ValueError:
                    messagebox.showerror("错误", "日期格式不正确，请使用 YYYY-MM-DD 格式")
                    return
                
                # 生成新ID
                new_id = max([item["id"] for item in self.inventory_data]) + 1 if self.inventory_data else 1
                
                # 创建新食材数据
                new_item = {
                    "id": new_id,
                    "name": name,
                    "current_stock": current_stock,
                    "unit": unit,
                    "threshold": threshold,
                    "unit_cost": unit_cost,
                    "expiry": expiry
                }
                
                # 添加到数据中
                self.inventory_data.append(new_item)
                
                messagebox.showinfo("成功", f"成功添加食材：{name}")
                dialog.destroy()
                
                # 刷新显示
                self.show()
                
            except ValueError:
                messagebox.showerror("错误", "请输入正确的数字格式")
            except Exception as e:
                messagebox.showerror("错误", f"添加失败：{str(e)}")
        
        confirm_btn = tk.Button(button_frame, text="确定添加", 
                              font=("微软雅黑", 11, "bold"),
                              bg="#27ae60", fg="white", bd=0,
                              padx=20, pady=8, cursor="hand2",
                              command=save_item)
        confirm_btn.pack(side="right")
        
        # 设置焦点到第一个输入框
        entries["name"].focus()
          # 回车键提交
        dialog.bind('<Return>', lambda e: save_item())
        
    def edit_inventory_item(self, tree):
        """编辑库存项目"""
        # 获取选中的项目
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("提示", "请选择要编辑的食材")
            return
        
        # 获取选中项目的数据
        item_values = tree.item(selected_item[0])['values']
        if not item_values:
            return
        
        # 根据ID找到对应的食材数据
        item_id = int(item_values[0])
        current_item = None
        for item in self.inventory_data:
            if item["id"] == item_id:
                current_item = item
                break
        
        if not current_item:
            messagebox.showerror("错误", "未找到对应的食材数据")
            return
        
        # 创建修改库存对话框
        dialog = tk.Toplevel()
        dialog.title("修改库存")
        dialog.geometry("400x400")
        dialog.configure(bg="#f8f9fa")
        dialog.resizable(False, False)
        dialog.grab_set()  # 模态对话框
        
        # 居中显示对话框
        dialog.transient(self.parent_frame.winfo_toplevel())
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (dialog.winfo_screenheight() // 2) - (400 // 2)
        dialog.geometry(f"400x400+{x}+{y}")
        
        # 标题
        title_frame = tk.Frame(dialog, bg="#e67e22", height=60)
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text="🔧修改库存", 
                              font=("微软雅黑", 16, "bold"),
                              bg="#e67e22", fg="white")
        title_label.pack(pady=15)
        
        # 表单区域
        form_frame = tk.Frame(dialog, bg="#f8f9fa")
        form_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        # 输入字段配置
        fields = [
            ("食材名称", "name", "text"),
            ("当前库存", "current_stock", "number"),
            ("单位", "unit", "text"),
            ("安全库存阈值", "threshold", "number"),
            ("单价 (¥)", "unit_cost", "number"),
            ("过期日期", "expiry", "date")
        ]
        
        # 存储输入控件的字典
        entries = {}
        
        # 创建输入字段并填入当前数据
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
                               width=25, relief="solid", bd=1)
                entry.grid(row=i, column=1, sticky="ew", pady=(0, 5))
                
            elif field_type == "number":
                entry = tk.Entry(form_frame, font=("微软雅黑", 11),
                               width=25, relief="solid", bd=1)
                entry.grid(row=i, column=1, sticky="ew", pady=(0, 5))
                
            elif field_type == "date":
                entry = tk.Entry(form_frame, font=("微软雅黑", 11),
                               width=25, relief="solid", bd=1)
                entry.grid(row=i, column=1, sticky="ew", pady=(0, 5))
                # 添加日期格式提示
                hint_label = tk.Label(form_frame, text="格式: YYYY-MM-DD", 
                                    font=("微软雅黑", 9),
                                    bg="#f8f9fa", fg="#7f8c8d")
                hint_label.grid(row=i, column=2, sticky="w", padx=(10, 0))
                
            if entry:
                # 填入当前数据
                entry.insert(0, str(current_item[field_name]))
                entries[field_name] = entry
        
        # 设置第二列的权重，使输入框可以拉伸
        form_frame.columnconfigure(1, weight=1)
        
        # 按钮区域
        button_frame = tk.Frame(dialog, bg="#f8f9fa")
        button_frame.pack(fill="x", padx=30, pady=(0, 20))
        
        # 删除按钮
        def delete_item():
            result = messagebox.askyesno("确认删除", 
                                       f"确定要删除食材 '{current_item['name']}' 吗？\n此操作不可撤销！")
            if result:
                # 从数据中删除
                self.inventory_data.remove(current_item)
                messagebox.showinfo("成功", f"已删除食材：{current_item['name']}")
                dialog.destroy()
                # 刷新显示
                self.show()
        
        delete_btn = tk.Button(button_frame, text="🗑️ 删除", 
                             font=("微软雅黑", 11),
                             bg="#e74c3c", fg="white", bd=0,
                             padx=15, pady=8, cursor="hand2",
                             command=delete_item)
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
                    messagebox.showerror("错误", "请输入食材名称")
                    return
                
                current_stock = float(entries["current_stock"].get())
                if current_stock < 0:
                    messagebox.showerror("错误", "当前库存不能为负数")
                    return
                    
                unit = entries["unit"].get().strip()
                if not unit:
                    messagebox.showerror("错误", "请输入单位")
                    return
                
                threshold = float(entries["threshold"].get())
                if threshold < 0:
                    messagebox.showerror("错误", "安全库存阈值不能为负数")
                    return
                
                unit_cost = float(entries["unit_cost"].get())
                if unit_cost < 0:
                    messagebox.showerror("错误", "单价不能为负数")
                    return
                
                expiry = entries["expiry"].get().strip()
                if not expiry:
                    messagebox.showerror("错误", "请输入过期日期")
                    return
                
                # 验证日期格式
                import datetime
                try:
                    datetime.datetime.strptime(expiry, "%Y-%m-%d")
                except ValueError:
                    messagebox.showerror("错误", "日期格式不正确，请使用 YYYY-MM-DD 格式")
                    return
                
                # 更新食材数据
                current_item["name"] = name
                current_item["current_stock"] = current_stock
                current_item["unit"] = unit
                current_item["threshold"] = threshold
                current_item["unit_cost"] = unit_cost
                current_item["expiry"] = expiry
                
                messagebox.showinfo("成功", f"成功更新食材：{name}")
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
        
        # 设置焦点到第一个输入框
        entries["name"].focus()
        entries["name"].selection_range(0, tk.END)  # 选中所有文本便于编辑
          # 回车键提交
        dialog.bind('<Return>', lambda e: save_changes())
        
    def on_item_select(self, event):
        """处理项目选择事件"""
        selected_items = self.tree.selection()
        if selected_items:
            # 获取选中的食材信息
            item_values = self.tree.item(selected_items[0])['values']
            if item_values:
                food_name = item_values[1]  # 食材名称在第二列
                current_stock = item_values[2]  # 当前库存在第三列
                unit = item_values[3]  # 单位在第四列
                
                # 更新状态提醒
                self.status_label.config(
                    text=f"✅ 已选中：{food_name} (库存: {current_stock} {unit})",
                    fg="#27ae60"
                )
            
            # 有选中项时启用修改按钮
            self.edit_btn.config(state="normal", bg="#f39c12")
        else:
            # 无选中项时禁用修改按钮和更新状态
            self.edit_btn.config(state="disabled", bg="#bdc3c7")
            self.status_label.config(
                text="💡 点击选择食材以启用修改功能",
                fg="#7f8c8d"
            )
    
    def edit_selected_item(self):
        """编辑选中的库存项目"""
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("提示", "请先选择要修改的食材")
            return
        
        # 调用编辑功能
        self.edit_inventory_item(self.tree)

    def check_ingredients_availability(self, meal_name, quantity):
        """检查制作指定数量菜品的原材料是否充足"""
        if meal_name not in self.recipe_data:
            return True, "该菜品未配置配方"
        
        recipe = self.recipe_data[meal_name]
        insufficient_ingredients = []
        
        for ingredient_name, required_amount in recipe.items():
            # 查找对应的库存项目
            ingredient_item = None
            for item in self.inventory_data:
                if item["name"] == ingredient_name:
                    ingredient_item = item
                    break
            
            if ingredient_item is None:
                insufficient_ingredients.append(f"{ingredient_name}: 库存中未找到")
                continue
            
            total_required = required_amount * quantity
            if ingredient_item["current_stock"] < total_required:
                insufficient_ingredients.append(
                    f"{ingredient_name}: 需要 {total_required} {ingredient_item['unit']}, "
                    f"但只有 {ingredient_item['current_stock']} {ingredient_item['unit']}"
                )
        
        if insufficient_ingredients:
            return False, "原材料不足:\n" + "\n".join(insufficient_ingredients)
        
        return True, "原材料充足"
    
    def consume_ingredients(self, meal_name, quantity):
        """消耗制作指定数量菜品的原材料"""
        if meal_name not in self.recipe_data:
            return False, "该菜品未配置配方"
        
        # 先检查原材料是否充足
        is_sufficient, message = self.check_ingredients_availability(meal_name, quantity)
        if not is_sufficient:
            return False, message
        
        recipe = self.recipe_data[meal_name]
        consumed_items = []
        
        # 扣减库存
        for ingredient_name, required_amount in recipe.items():
            for item in self.inventory_data:
                if item["name"] == ingredient_name:
                    total_required = required_amount * quantity
                    item["current_stock"] -= total_required
                    consumed_items.append(f"{ingredient_name}: -{total_required} {item['unit']}")
                    break
        
        return True, f"成功消耗原材料:\n" + "\n".join(consumed_items)
    
    def get_recipe_info(self, meal_name):
        """获取菜品配方信息"""
        if meal_name not in self.recipe_data:
            return None
        
        recipe = self.recipe_data[meal_name]
        recipe_info = []
        
        for ingredient_name, required_amount in recipe.items():
            # 查找对应的库存项目获取单位
            for item in self.inventory_data:
                if item["name"] == ingredient_name:
                    recipe_info.append(f"{ingredient_name}: {required_amount} {item['unit']}")
                    break
        
        return recipe_info

    def show_stock_warnings(self):
        """显示库存预警信息"""
        # 创建预警信息对话框
        dialog = tk.Toplevel()
        dialog.title("库存预警")
        dialog.geometry("700x600")
        dialog.configure(bg="#f8f9fa")
        dialog.resizable(False, False)
        dialog.grab_set()
        
        # 居中显示对话框
        dialog.transient(self.parent_frame.winfo_toplevel())
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (700 // 2)
        y = (dialog.winfo_screenheight() // 2) - (600 // 2)
        dialog.geometry(f"700x600+{x}+{y}")
        
        # 标题
        title_frame = tk.Frame(dialog, bg="#e74c3c", height=60)
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text="⚠️ 库存预警", 
                              font=("微软雅黑", 16, "bold"),
                              bg="#e74c3c", fg="white")
        title_label.pack(pady=15)
        
        # 内容区域
        content_frame = tk.Frame(dialog, bg="#f9f9fa")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # 创建文本显示区域
        text_frame = tk.Frame(content_frame)
        text_frame.pack(fill="both", expand=True)
        
        text_widget = tk.Text(text_frame, font=("微软雅黑", 11),
                            wrap=tk.WORD, bg="#ffffff", fg="#2c3e50")
        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        # 生成预警信息
        warning_content = "📊 库存预警报告\n\n"
        
        # 1. 库存不足预警
        low_stock_items = []
        for item in self.inventory_data:
            if item["current_stock"] <= item["threshold"]:
                low_stock_items.append(item)
        
        if low_stock_items:
            warning_content += "🔴 库存不足预警:\n"
            for item in low_stock_items:
                warning_content += f"   • {item['name']}: 当前 {item['current_stock']} {item['unit']}, "
                warning_content += f"安全库存 {item['threshold']} {item['unit']}\n"
        else:
            warning_content += "✅ 所有物品库存充足\n"
        
        warning_content += "\n"
        
        # 2. 可制作菜品分析
        warning_content += "🍽️ 可制作菜品分析:\n"
        for meal_name, recipe in self.recipe_data.items():
            can_make = True
            max_quantity = float('inf')
            limiting_ingredient = ""
            
            for ingredient_name, required_amount in recipe.items():
                ingredient_item = None
                for item in self.inventory_data:
                    if item["name"] == ingredient_name:
                        ingredient_item = item
                        break
                
                if ingredient_item is None:
                    can_make = False
                    limiting_ingredient = f"{ingredient_name}(库存中未找到)"
                    max_quantity = 0
                    break
                
                possible_quantity = int(ingredient_item["current_stock"] / required_amount)
                if possible_quantity < max_quantity:
                    max_quantity = possible_quantity
                    limiting_ingredient = ingredient_name
            
            if can_make and max_quantity > 0:
                warning_content += f"   ✅ {meal_name}: 最多可制作 {max_quantity} 份"
                if max_quantity < 10:
                    warning_content += f" (受限于 {limiting_ingredient})"
                warning_content += "\n"
            else:
                warning_content += f"   ❌ {meal_name}: 无法制作 (缺少 {limiting_ingredient})\n"
        
        warning_content += "\n"
        
        # 3. 补货建议
        warning_content += "📋 补货建议:\n"
        for item in low_stock_items:
            suggested_order = item["threshold"] * 3  # 建议补货到安全库存的3倍
            needed_quantity = suggested_order - item["current_stock"]
            estimated_cost = needed_quantity * item["unit_cost"]
            warning_content += f"   • {item['name']}: 建议补货 {needed_quantity} {item['unit']}, "
            warning_content += f"预计成本 ¥{estimated_cost:.2f}\n"
        
        text_widget.insert(tk.END, warning_content)
        text_widget.config(state=tk.DISABLED)  # 设为只读
        
        text_widget.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # 关闭按钮
        close_btn = tk.Button(content_frame, text="关闭", 
                            font=("微软雅黑", 11),
                            bg="#95a5a6", fg="white", bd=0,
                            padx=20, pady=8, cursor="hand2",
                            command=dialog.destroy)
        close_btn.pack(pady=(10, 0))
