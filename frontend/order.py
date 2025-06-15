import tkinter as tk
from tkinter import ttk
from utils import show_info, show_error

class OrderUI(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.order_list = []
        self.selected_order = None
        self.build_ui()
        self.refresh_list()

    def build_ui(self):
        tk.Label(self, text="订单管理", font=("微软雅黑", 14)).pack(pady=10)
        form = tk.Frame(self)
        form.pack(pady=5)
        tk.Label(form, text="客户:").grid(row=0, column=0, sticky="e")
        self.customer_var = tk.StringVar()
        tk.Entry(form, textvariable=self.customer_var).grid(row=0, column=1, padx=5)
        tk.Label(form, text="员工:").grid(row=0, column=2, sticky="e")
        self.employee_var = tk.StringVar()
        tk.Entry(form, textvariable=self.employee_var).grid(row=0, column=3, padx=5)
        tk.Label(form, text="配送日期:").grid(row=1, column=0, sticky="e")
        self.date_var = tk.StringVar()
        tk.Entry(form, textvariable=self.date_var).grid(row=1, column=1, padx=5)
        tk.Label(form, text="订单状态:").grid(row=1, column=2, sticky="e")
        self.status_var = tk.StringVar(value="已接收")
        ttk.Combobox(form, textvariable=self.status_var, values=["已接收", "进行中", "已完成"]).grid(row=1, column=3, padx=5)
        # 订单列表
        tk.Label(self, text="订单列表", font=("微软雅黑", 12)).pack(pady=5)
        self.listbox = tk.Listbox(self, width=60, activestyle='dotbox')
        self.listbox.pack(pady=5)
        self.listbox.bind('<<ListboxSelect>>', self.on_select)
        btns = tk.Frame(self)
        btns.pack(pady=5)
        tk.Button(btns, text="新增/清空", command=self.add_order, width=10).pack(side=tk.LEFT, padx=2)
        tk.Button(btns, text="删除", command=self.delete_order, width=10).pack(side=tk.LEFT, padx=2)
        # 餐品明细
        tk.Label(self, text="餐品明细（示例）", font=("微软雅黑", 12)).pack(pady=5)
        self.meal_table = ttk.Treeview(self, columns=("name", "qty", "price"), show="headings", height=5)
        self.meal_table.heading("name", text="餐食名称")
        self.meal_table.heading("qty", text="数量")
        self.meal_table.heading("price", text="单价")
        self.meal_table.pack(pady=5)
        # 操作按钮
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="保存订单", command=self.save_order, width=12).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="订单履历", command=self.show_history, width=12).pack(side=tk.LEFT, padx=5)

    def refresh_list(self):
        self.listbox.delete(0, tk.END)
        for order in self.order_list:
            summary = f"客户:{order['customer']} 员工:{order['employee']} 日期:{order['date']} 状态:{order['status']}"
            self.listbox.insert(tk.END, summary)
        if self.selected_order and self.selected_order in self.order_list:
            idx = self.order_list.index(self.selected_order)
            self.listbox.selection_set(idx)
            self.listbox.activate(idx)
        else:
            self.listbox.selection_clear(0, tk.END)

    def on_select(self, event):
        idx = self.listbox.curselection()
        if idx:
            self.selected_order = self.order_list[idx[0]]
            self.load_order(self.selected_order)
        else:
            self.selected_order = None

    def load_order(self, order):
        self.customer_var.set(order.get('customer', ''))
        self.employee_var.set(order.get('employee', ''))
        self.date_var.set(order.get('date', ''))
        self.status_var.set(order.get('status', '已接收'))
        self.meal_table.delete(*self.meal_table.get_children())
        for meal in order.get('meals', []):
            self.meal_table.insert('', tk.END, values=(meal['name'], meal['qty'], meal['price']))

    def add_order(self):
        self.customer_var.set("")
        self.employee_var.set("")
        self.date_var.set("")
        self.status_var.set("已接收")
        self.selected_order = None
        self.listbox.selection_clear(0, tk.END)
        self.meal_table.delete(*self.meal_table.get_children())

    def save_order(self):
        customer = self.customer_var.get().strip()
        employee = self.employee_var.get().strip()
        date = self.date_var.get().strip()
        status = self.status_var.get().strip()
        if not customer or not date:
            show_error("错误", "客户和配送日期不能为空")
            return
        order = {
            'customer': customer,
            'employee': employee,
            'date': date,
            'status': status,
            'meals': []
        }
        if self.selected_order:
            idx = self.order_list.index(self.selected_order)
            self.order_list[idx] = order
            show_info("保存成功", "订单信息已更新")
        else:
            self.order_list.append(order)
            show_info("保存成功", "订单已添加")
        self.refresh_list()
        self.selected_order = order
        idx = self.order_list.index(order)
        self.listbox.selection_clear(0, tk.END)
        self.listbox.selection_set(idx)
        self.listbox.activate(idx)

    def delete_order(self):
        idx = self.listbox.curselection()
        if idx:
            del self.order_list[idx[0]]
            self.refresh_list()
            self.add_order()
            show_info("删除成功", "订单已删除")
        else:
            show_error("错误", "请先选择要删除的订单")

    def show_history(self):
        if self.selected_order:
            show_info("订单履历", f"{self.selected_order['customer']} 的订单履历功能待实现")
        else:
            show_info("订单履历", "请先选择订单")

    # Getter/Setter
    def get_order_list(self):
        return self.order_list
    def set_order_list(self, value):
        self.order_list = value
    def get_selected_order(self):
        return self.selected_order
    def set_selected_order(self, value):
        self.selected_order = value
