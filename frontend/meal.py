import tkinter as tk
from tkinter import ttk
from utils import show_info, show_error

class MealUI(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.meal_list = []  # 餐食列表
        self.selected_meal = None
        self.build_ui()
        self.refresh_list()

    def build_ui(self):
        self.columnconfigure(1, weight=1)
        # 左侧餐食列表
        left = tk.Frame(self)
        left.grid(row=0, column=0, sticky="ns", padx=10, pady=10)
        tk.Label(left, text="餐食列表", font=("微软雅黑", 12)).pack()
        self.listbox = tk.Listbox(left, width=20, activestyle='dotbox')
        self.listbox.pack(pady=5)
        self.listbox.bind('<<ListboxSelect>>', self.on_select)
        btns = tk.Frame(left)
        btns.pack(pady=5)
        tk.Button(btns, text="新增/清空", command=self.add_meal, width=10).pack(side=tk.LEFT, padx=2)
        tk.Button(btns, text="删除", command=self.delete_meal, width=10).pack(side=tk.LEFT, padx=2)
        # 中间详情区
        center = tk.Frame(self)
        center.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        tk.Label(center, text="餐食详情", font=("微软雅黑", 12)).grid(row=0, column=0, columnspan=2, pady=5)
        tk.Label(center, text="名称:").grid(row=1, column=0, sticky="e")
        self.name_var = tk.StringVar()
        tk.Entry(center, textvariable=self.name_var).grid(row=1, column=1, sticky="ew")
        tk.Label(center, text="描述:").grid(row=2, column=0, sticky="e")
        self.detail_var = tk.StringVar()
        tk.Entry(center, textvariable=self.detail_var).grid(row=2, column=1, sticky="ew")
        tk.Label(center, text="价格:").grid(row=3, column=0, sticky="e")
        self.price_var = tk.DoubleVar()
        tk.Entry(center, textvariable=self.price_var).grid(row=3, column=1, sticky="ew")
        tk.Label(center, text="状态:").grid(row=4, column=0, sticky="e")
        self.active_var = tk.BooleanVar()
        tk.Checkbutton(center, text="激活", variable=self.active_var).grid(row=4, column=1, sticky="w")
        # 下方操作按钮
        btn_frame = tk.Frame(center)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=10)
        tk.Button(btn_frame, text="保存", command=self.save_meal, width=12).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="配置原料与容器", command=self.config_meal, width=16).pack(side=tk.LEFT, padx=5)

    def refresh_list(self):
        self.listbox.delete(0, tk.END)
        for meal in self.meal_list:
            self.listbox.insert(tk.END, meal['name'])
        # 高亮选中项
        if self.selected_meal and self.selected_meal in self.meal_list:
            idx = self.meal_list.index(self.selected_meal)
            self.listbox.selection_set(idx)
            self.listbox.activate(idx)
        else:
            self.listbox.selection_clear(0, tk.END)

    def on_select(self, event):
        idx = self.listbox.curselection()
        if idx:
            self.selected_meal = self.meal_list[idx[0]]
            self.load_meal(self.selected_meal)
        else:
            self.selected_meal = None

    def load_meal(self, meal):
        self.name_var.set(meal.get('name', ''))
        self.detail_var.set(meal.get('detail', ''))
        self.price_var.set(meal.get('price', 0.0))
        self.active_var.set(meal.get('active', True))

    def add_meal(self):
        self.name_var.set("")
        self.detail_var.set("")
        self.price_var.set(0.0)
        self.active_var.set(True)
        self.selected_meal = None
        self.listbox.selection_clear(0, tk.END)

    def save_meal(self):
        name = self.name_var.get().strip()
        if not name:
            show_error("错误", "餐食名称不能为空")
            return
        try:
            price = float(self.price_var.get())
            if price < 0:
                raise ValueError
        except:
            show_error("错误", "价格必须为非负数字")
            return
        meal = {
            'name': name,
            'detail': self.detail_var.get().strip(),
            'price': price,
            'active': self.active_var.get()
        }
        if self.selected_meal:
            idx = self.meal_list.index(self.selected_meal)
            self.meal_list[idx] = meal
            show_info("保存成功", "餐食信息已更新")
        else:
            # 名称唯一性校验
            if any(x['name'] == name for x in self.meal_list):
                show_error("错误", "该餐食名称已存在")
                return
            self.meal_list.append(meal)
            show_info("保存成功", "餐食已添加")
        self.refresh_list()
        self.selected_meal = meal
        idx = self.meal_list.index(meal)
        self.listbox.selection_clear(0, tk.END)
        self.listbox.selection_set(idx)
        self.listbox.activate(idx)

    def delete_meal(self):
        idx = self.listbox.curselection()
        if idx:
            del self.meal_list[idx[0]]
            self.refresh_list()
            self.add_meal()
            show_info("删除成功", "餐食已删除")
        else:
            show_error("错误", "请先选择要删除的餐食")

    def config_meal(self):
        show_info("配置", "配置原料与容器功能待实现")

    # Getter/Setter
    def get_meal_list(self):
        return self.meal_list
    def set_meal_list(self, value):
        self.meal_list = value
    def get_selected_meal(self):
        return self.selected_meal
    def set_selected_meal(self, value):
        self.selected_meal = value
