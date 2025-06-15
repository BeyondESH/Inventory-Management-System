import tkinter as tk
from tkinter import ttk
from utils import show_info, show_error

class IngredientUI(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.ingredient_list = []
        self.selected_ingredient = None
        self.build_ui()
        self.refresh_list()

    def build_ui(self):
        self.columnconfigure(1, weight=1)
        # 左侧原料列表
        left = tk.Frame(self)
        left.grid(row=0, column=0, sticky="ns", padx=10, pady=10)
        tk.Label(left, text="原料列表", font=("微软雅黑", 12)).pack()
        self.listbox = tk.Listbox(left, width=20, activestyle='dotbox')
        self.listbox.pack(pady=5)
        self.listbox.bind('<<ListboxSelect>>', self.on_select)
        btns = tk.Frame(left)
        btns.pack(pady=5)
        tk.Button(btns, text="新增/清空", command=self.add_ingredient, width=10).pack(side=tk.LEFT, padx=2)
        tk.Button(btns, text="删除", command=self.delete_ingredient, width=10).pack(side=tk.LEFT, padx=2)
        # 右侧详情区
        right = tk.Frame(self)
        right.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        tk.Label(right, text="原料详情", font=("微软雅黑", 12)).grid(row=0, column=0, columnspan=2, pady=5)
        tk.Label(right, text="名称:").grid(row=1, column=0, sticky="e")
        self.name_var = tk.StringVar()
        tk.Entry(right, textvariable=self.name_var).grid(row=1, column=1, sticky="ew")
        tk.Label(right, text="单位:").grid(row=2, column=0, sticky="e")
        self.unit_var = tk.StringVar()
        tk.Entry(right, textvariable=self.unit_var).grid(row=2, column=1, sticky="ew")
        tk.Label(right, text="当前库存:").grid(row=3, column=0, sticky="e")
        self.stock_var = tk.DoubleVar()
        tk.Entry(right, textvariable=self.stock_var).grid(row=3, column=1, sticky="ew")
        tk.Label(right, text="安全库存:").grid(row=4, column=0, sticky="e")
        self.threshold_var = tk.DoubleVar()
        tk.Entry(right, textvariable=self.threshold_var).grid(row=4, column=1, sticky="ew")
        tk.Label(right, text="单价:").grid(row=5, column=0, sticky="e")
        self.price_var = tk.DoubleVar()
        tk.Entry(right, textvariable=self.price_var).grid(row=5, column=1, sticky="ew")
        # 下方操作按钮
        btn_frame = tk.Frame(right)
        btn_frame.grid(row=6, column=0, columnspan=2, pady=10)
        tk.Button(btn_frame, text="保存", command=self.save_ingredient, width=12).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="批次管理", command=self.batch_manage, width=12).pack(side=tk.LEFT, padx=5)

    def refresh_list(self):
        self.listbox.delete(0, tk.END)
        for ing in self.ingredient_list:
            self.listbox.insert(tk.END, ing['name'])
        if self.selected_ingredient and self.selected_ingredient in self.ingredient_list:
            idx = self.ingredient_list.index(self.selected_ingredient)
            self.listbox.selection_set(idx)
            self.listbox.activate(idx)
        else:
            self.listbox.selection_clear(0, tk.END)

    def on_select(self, event):
        idx = self.listbox.curselection()
        if idx:
            self.selected_ingredient = self.ingredient_list[idx[0]]
            self.load_ingredient(self.selected_ingredient)
        else:
            self.selected_ingredient = None

    def load_ingredient(self, ing):
        self.name_var.set(ing.get('name', ''))
        self.unit_var.set(ing.get('unit', ''))
        self.stock_var.set(ing.get('stock', 0.0))
        self.threshold_var.set(ing.get('threshold', 0.0))
        self.price_var.set(ing.get('price', 0.0))

    def add_ingredient(self):
        self.name_var.set("")
        self.unit_var.set("")
        self.stock_var.set(0.0)
        self.threshold_var.set(0.0)
        self.price_var.set(0.0)
        self.selected_ingredient = None
        self.listbox.selection_clear(0, tk.END)

    def save_ingredient(self):
        name = self.name_var.get().strip()
        if not name:
            show_error("错误", "原料名称不能为空")
            return
        try:
            stock = float(self.stock_var.get())
            threshold = float(self.threshold_var.get())
            price = float(self.price_var.get())
            if stock < 0 or threshold < 0 or price < 0:
                raise ValueError
        except:
            show_error("错误", "库存/安全库存/单价必须为非负数字")
            return
        ing = {
            'name': name,
            'unit': self.unit_var.get().strip(),
            'stock': stock,
            'threshold': threshold,
            'price': price
        }
        if self.selected_ingredient:
            idx = self.ingredient_list.index(self.selected_ingredient)
            self.ingredient_list[idx] = ing
            show_info("保存成功", "原料信息已更新")
        else:
            if any(x['name'] == name for x in self.ingredient_list):
                show_error("错误", "该原料名称已存在")
                return
            self.ingredient_list.append(ing)
            show_info("保存成功", "原料已添加")
        self.refresh_list()
        self.selected_ingredient = ing
        idx = self.ingredient_list.index(ing)
        self.listbox.selection_clear(0, tk.END)
        self.listbox.selection_set(idx)
        self.listbox.activate(idx)

    def delete_ingredient(self):
        idx = self.listbox.curselection()
        if idx:
            del self.ingredient_list[idx[0]]
            self.refresh_list()
            self.add_ingredient()
            show_info("删除成功", "原料已删除")
        else:
            show_error("错误", "请先选择要删除的原料")

    def batch_manage(self):
        show_info("批次管理", "批次管理功能待实现")

    # Getter/Setter
    def get_ingredient_list(self):
        return self.ingredient_list
    def set_ingredient_list(self, value):
        self.ingredient_list = value
    def get_selected_ingredient(self):
        return self.selected_ingredient
    def set_selected_ingredient(self, value):
        self.selected_ingredient = value
