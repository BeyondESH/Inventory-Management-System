import tkinter as tk
from utils import show_info, show_error

class ContainerUI(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.container_list = []
        self.selected_container = None
        self.build_ui()
        self.refresh_list()

    def build_ui(self):
        self.columnconfigure(1, weight=1)
        # 左侧容器列表
        left = tk.Frame(self)
        left.grid(row=0, column=0, sticky="ns", padx=10, pady=10)
        tk.Label(left, text="容器列表", font=("微软雅黑", 12)).pack()
        self.listbox = tk.Listbox(left, width=20, activestyle='dotbox')
        self.listbox.pack(pady=5)
        self.listbox.bind('<<ListboxSelect>>', self.on_select)
        btns = tk.Frame(left)
        btns.pack(pady=5)
        tk.Button(btns, text="新增/清空", command=self.add_container, width=10).pack(side=tk.LEFT, padx=2)
        tk.Button(btns, text="删除", command=self.delete_container, width=10).pack(side=tk.LEFT, padx=2)
        # 右侧详情区
        right = tk.Frame(self)
        right.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        tk.Label(right, text="容器详情", font=("微软雅黑", 12)).grid(row=0, column=0, columnspan=2, pady=5)
        tk.Label(right, text="类型:").grid(row=1, column=0, sticky="e")
        self.type_var = tk.StringVar()
        tk.Entry(right, textvariable=self.type_var).grid(row=1, column=1, sticky="ew")
        tk.Label(right, text="单位成本:").grid(row=2, column=0, sticky="e")
        self.unit_cost_var = tk.DoubleVar()
        tk.Entry(right, textvariable=self.unit_cost_var).grid(row=2, column=1, sticky="ew")
        tk.Label(right, text="当前库存:").grid(row=3, column=0, sticky="e")
        self.stock_var = tk.DoubleVar()
        tk.Entry(right, textvariable=self.stock_var).grid(row=3, column=1, sticky="ew")
        tk.Label(right, text="安全库存:").grid(row=4, column=0, sticky="e")
        self.threshold_var = tk.DoubleVar()
        tk.Entry(right, textvariable=self.threshold_var).grid(row=4, column=1, sticky="ew")
        # 下方操作按钮
        btn_frame = tk.Frame(right)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=10)
        tk.Button(btn_frame, text="保存", command=self.save_container, width=12).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="批次管理", command=self.batch_manage, width=12).pack(side=tk.LEFT, padx=5)

    def refresh_list(self):
        self.listbox.delete(0, tk.END)
        for c in self.container_list:
            self.listbox.insert(tk.END, c['type'])
        if self.selected_container and self.selected_container in self.container_list:
            idx = self.container_list.index(self.selected_container)
            self.listbox.selection_set(idx)
            self.listbox.activate(idx)
        else:
            self.listbox.selection_clear(0, tk.END)

    def on_select(self, event):
        idx = self.listbox.curselection()
        if idx:
            self.selected_container = self.container_list[idx[0]]
            self.load_container(self.selected_container)
        else:
            self.selected_container = None

    def load_container(self, c):
        self.type_var.set(c.get('type', ''))
        self.unit_cost_var.set(c.get('unit_cost', 0.0))
        self.stock_var.set(c.get('stock', 0.0))
        self.threshold_var.set(c.get('threshold', 0.0))

    def add_container(self):
        self.type_var.set("")
        self.unit_cost_var.set(0.0)
        self.stock_var.set(0.0)
        self.threshold_var.set(0.0)
        self.selected_container = None
        self.listbox.selection_clear(0, tk.END)

    def save_container(self):
        ctype = self.type_var.get().strip()
        if not ctype:
            show_error("错误", "容器类型不能为空")
            return
        try:
            unit_cost = float(self.unit_cost_var.get())
            stock = float(self.stock_var.get())
            threshold = float(self.threshold_var.get())
            if unit_cost < 0 or stock < 0 or threshold < 0:
                raise ValueError
        except:
            show_error("错误", "单位成本/库存/安全库存必须为非负数字")
            return
        c = {
            'type': ctype,
            'unit_cost': unit_cost,
            'stock': stock,
            'threshold': threshold
        }
        if self.selected_container:
            idx = self.container_list.index(self.selected_container)
            self.container_list[idx] = c
            show_info("保存成功", "容器信息已更新")
        else:
            if any(x['type'] == ctype for x in self.container_list):
                show_error("错误", "该容器类型已存在")
                return
            self.container_list.append(c)
            show_info("保存成功", "容器已添加")
        self.refresh_list()
        self.selected_container = c
        idx = self.container_list.index(c)
        self.listbox.selection_clear(0, tk.END)
        self.listbox.selection_set(idx)
        self.listbox.activate(idx)

    def delete_container(self):
        idx = self.listbox.curselection()
        if idx:
            del self.container_list[idx[0]]
            self.refresh_list()
            self.add_container()
            show_info("删除成功", "容器已删除")
        else:
            show_error("错误", "请先选择要删除的容器")

    def batch_manage(self):
        show_info("批次管理", "批次管理功能待实现")

    # Getter/Setter
    def get_container_list(self):
        return self.container_list
    def set_container_list(self, value):
        self.container_list = value
    def get_selected_container(self):
        return self.selected_container
    def set_selected_container(self, value):
        self.selected_container = value
