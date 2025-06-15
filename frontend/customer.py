import tkinter as tk
from utils import show_info, show_error

class CustomerUI(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.customer_list = []
        self.selected_customer = None
        self.build_ui()
        self.refresh_list()

    def build_ui(self):
        self.columnconfigure(1, weight=1)
        # 左侧客户列表
        left = tk.Frame(self)
        left.grid(row=0, column=0, sticky="ns", padx=10, pady=10)
        tk.Label(left, text="客户列表", font=("微软雅黑", 12)).pack()
        self.listbox = tk.Listbox(left, width=20, activestyle='dotbox')
        self.listbox.pack(pady=5)
        self.listbox.bind('<<ListboxSelect>>', self.on_select)
        btns = tk.Frame(left)
        btns.pack(pady=5)
        tk.Button(btns, text="新增/清空", command=self.add_customer, width=10).pack(side=tk.LEFT, padx=2)
        tk.Button(btns, text="删除", command=self.delete_customer, width=10).pack(side=tk.LEFT, padx=2)
        # 右侧详情区
        right = tk.Frame(self)
        right.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        tk.Label(right, text="客户详情", font=("微软雅黑", 12)).grid(row=0, column=0, columnspan=2, pady=5)
        tk.Label(right, text="姓名:").grid(row=1, column=0, sticky="e")
        self.name_var = tk.StringVar()
        tk.Entry(right, textvariable=self.name_var).grid(row=1, column=1, sticky="ew")
        tk.Label(right, text="邮箱:").grid(row=2, column=0, sticky="e")
        self.email_var = tk.StringVar()
        tk.Entry(right, textvariable=self.email_var).grid(row=2, column=1, sticky="ew")
        tk.Label(right, text="电话:").grid(row=3, column=0, sticky="e")
        self.phone_var = tk.StringVar()
        tk.Entry(right, textvariable=self.phone_var).grid(row=3, column=1, sticky="ew")
        tk.Label(right, text="地址:").grid(row=4, column=0, sticky="e")
        self.address_var = tk.StringVar()
        tk.Entry(right, textvariable=self.address_var).grid(row=4, column=1, sticky="ew")
        tk.Label(right, text="支付方式:").grid(row=5, column=0, sticky="e")
        self.payment_var = tk.StringVar()
        tk.Entry(right, textvariable=self.payment_var).grid(row=5, column=1, sticky="ew")
        # 下方操作按钮
        btn_frame = tk.Frame(right)
        btn_frame.grid(row=6, column=0, columnspan=2, pady=10)
        tk.Button(btn_frame, text="保存", command=self.save_customer, width=12).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="历史订单", command=self.show_orders, width=12).pack(side=tk.LEFT, padx=5)

    def refresh_list(self):
        self.listbox.delete(0, tk.END)
        for c in self.customer_list:
            self.listbox.insert(tk.END, c['name'])
        # 高亮选中项
        if self.selected_customer and self.selected_customer in self.customer_list:
            idx = self.customer_list.index(self.selected_customer)
            self.listbox.selection_set(idx)
            self.listbox.activate(idx)
        else:
            self.listbox.selection_clear(0, tk.END)

    def on_select(self, event):
        idx = self.listbox.curselection()
        if idx:
            self.selected_customer = self.customer_list[idx[0]]
            self.load_customer(self.selected_customer)
        else:
            self.selected_customer = None

    def load_customer(self, c):
        self.name_var.set(c.get('name', ''))
        self.email_var.set(c.get('email', ''))
        self.phone_var.set(c.get('phone', ''))
        self.address_var.set(c.get('address', ''))
        self.payment_var.set(c.get('payment', ''))

    def add_customer(self):
        self.name_var.set("")
        self.email_var.set("")
        self.phone_var.set("")
        self.address_var.set("")
        self.payment_var.set("")
        self.selected_customer = None
        self.listbox.selection_clear(0, tk.END)

    def save_customer(self):
        name = self.name_var.get().strip()
        email = self.email_var.get().strip()
        if not name or not email:
            show_error("错误", "客户姓名和邮箱不能为空")
            return
        if '@' not in email or '.' not in email:
            show_error("错误", "邮箱格式不正确")
            return
        c = {
            'name': name,
            'email': email,
            'phone': self.phone_var.get().strip(),
            'address': self.address_var.get().strip(),
            'payment': self.payment_var.get().strip()
        }
        if self.selected_customer:
            idx = self.customer_list.index(self.selected_customer)
            self.customer_list[idx] = c
            show_info("保存成功", "客户信息已更新")
        else:
            # 邮箱唯一性校验
            if any(x['email'] == email for x in self.customer_list):
                show_error("错误", "该邮箱已存在")
                return
            self.customer_list.append(c)
            show_info("保存成功", "客户已添加")
        self.refresh_list()
        self.selected_customer = c
        idx = self.customer_list.index(c)
        self.listbox.selection_clear(0, tk.END)
        self.listbox.selection_set(idx)
        self.listbox.activate(idx)

    def delete_customer(self):
        idx = self.listbox.curselection()
        if idx:
            del self.customer_list[idx[0]]
            self.refresh_list()
            self.add_customer()
            show_info("删除成功", "客户已删除")
        else:
            show_error("错误", "请先选择要删除的客户")

    def show_orders(self):
        if self.selected_customer:
            show_info("历史订单", f"{self.selected_customer['name']} 的历史订单功能待实现")
        else:
            show_info("历史订单", "请先选择客户")

    # Getter/Setter
    def get_customer_list(self):
        return self.customer_list
    def set_customer_list(self, value):
        self.customer_list = value
    def get_selected_customer(self):
        return self.selected_customer
    def set_selected_customer(self, value):
        self.selected_customer = value
