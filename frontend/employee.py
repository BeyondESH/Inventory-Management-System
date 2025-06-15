import tkinter as tk
from utils import show_info, show_error

class EmployeeUI(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.employee_list = []
        self.selected_employee = None
        self.build_ui()
        self.refresh_list()

    def build_ui(self):
        self.columnconfigure(1, weight=1)
        # 左侧员工列表
        left = tk.Frame(self)
        left.grid(row=0, column=0, sticky="ns", padx=10, pady=10)
        tk.Label(left, text="员工列表", font=("微软雅黑", 12)).pack()
        self.listbox = tk.Listbox(left, width=20, activestyle='dotbox')
        self.listbox.pack(pady=5)
        self.listbox.bind('<<ListboxSelect>>', self.on_select)
        btns = tk.Frame(left)
        btns.pack(pady=5)
        tk.Button(btns, text="新增/清空", command=self.add_employee, width=10).pack(side=tk.LEFT, padx=2)
        tk.Button(btns, text="删除", command=self.delete_employee, width=10).pack(side=tk.LEFT, padx=2)
        # 右侧详情区
        right = tk.Frame(self)
        right.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        tk.Label(right, text="员工详情", font=("微软雅黑", 12)).grid(row=0, column=0, columnspan=2, pady=5)
        tk.Label(right, text="姓名:").grid(row=1, column=0, sticky="e")
        self.name_var = tk.StringVar()
        tk.Entry(right, textvariable=self.name_var).grid(row=1, column=1, sticky="ew")
        tk.Label(right, text="地址:").grid(row=2, column=0, sticky="e")
        self.address_var = tk.StringVar()
        tk.Entry(right, textvariable=self.address_var).grid(row=2, column=1, sticky="ew")
        tk.Label(right, text="月薪:").grid(row=3, column=0, sticky="e")
        self.salary_var = tk.DoubleVar()
        tk.Entry(right, textvariable=self.salary_var).grid(row=3, column=1, sticky="ew")
        # 下方操作按钮
        btn_frame = tk.Frame(right)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=10)
        tk.Button(btn_frame, text="保存", command=self.save_employee, width=12).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="订单履历", command=self.show_orders, width=12).pack(side=tk.LEFT, padx=5)

    def refresh_list(self):
        self.listbox.delete(0, tk.END)
        for emp in self.employee_list:
            self.listbox.insert(tk.END, emp['name'])
        if self.selected_employee and self.selected_employee in self.employee_list:
            idx = self.employee_list.index(self.selected_employee)
            self.listbox.selection_set(idx)
            self.listbox.activate(idx)
        else:
            self.listbox.selection_clear(0, tk.END)

    def on_select(self, event):
        idx = self.listbox.curselection()
        if idx:
            self.selected_employee = self.employee_list[idx[0]]
            self.load_employee(self.selected_employee)
        else:
            self.selected_employee = None

    def load_employee(self, e):
        self.name_var.set(e.get('name', ''))
        self.address_var.set(e.get('address', ''))
        self.salary_var.set(e.get('salary', 0.0))

    def add_employee(self):
        self.name_var.set("")
        self.address_var.set("")
        self.salary_var.set(0.0)
        self.selected_employee = None
        self.listbox.selection_clear(0, tk.END)

    def save_employee(self):
        name = self.name_var.get().strip()
        if not name:
            show_error("错误", "员工姓名不能为空")
            return
        try:
            salary = float(self.salary_var.get())
            if salary < 0:
                raise ValueError
        except:
            show_error("错误", "月薪必须为非负数字")
            return
        emp = {
            'name': name,
            'address': self.address_var.get().strip(),
            'salary': salary
        }
        if self.selected_employee:
            idx = self.employee_list.index(self.selected_employee)
            self.employee_list[idx] = emp
            show_info("保存成功", "员工信息已更新")
        else:
            self.employee_list.append(emp)
            show_info("保存成功", "员工已添加")
        self.refresh_list()
        self.selected_employee = emp
        idx = self.employee_list.index(emp)
        self.listbox.selection_clear(0, tk.END)
        self.listbox.selection_set(idx)
        self.listbox.activate(idx)

    def delete_employee(self):
        idx = self.listbox.curselection()
        if idx:
            del self.employee_list[idx[0]]
            self.refresh_list()
            self.add_employee()
            show_info("删除成功", "员工已删除")
        else:
            show_error("错误", "请先选择要删除的员工")

    def show_orders(self):
        if self.selected_employee:
            show_info("订单履历", f"{self.selected_employee['name']} 的订单履历功能待实现")
        else:
            show_info("订单履历", "请先选择员工")

    # Getter/Setter
    def get_employee_list(self):
        return self.employee_list
    def set_employee_list(self, value):
        self.employee_list = value
    def get_selected_employee(self):
        return self.selected_employee
    def set_selected_employee(self, value):
        self.selected_employee = value
