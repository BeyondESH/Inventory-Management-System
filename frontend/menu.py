import tkinter as tk
from meal import MealUI
from ingredient import IngredientUI
from container import ContainerUI
from order import OrderUI
from customer import CustomerUI
from employee import EmployeeUI
from report import ReportUI
from utils import show_info

class MainMenuUI(tk.Frame):
    def __init__(self, master, user_info):
        super().__init__(master)
        self.user_info = user_info
        self.master = master
        self.current_frame = None
        self.build_ui()

    def build_ui(self):
        for widget in self.winfo_children():
            widget.destroy()
        tk.Label(self, text=f"欢迎，{self.user_info.get('email', '用户')}！", font=("微软雅黑", 16)).pack(pady=20)
        tk.Label(self, text="请选择功能模块：", font=("微软雅黑", 12)).pack(pady=10)
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)
        modules = [
            ("餐食管理", self.open_meal),
            ("原料管理", self.open_ingredient),
            ("容器管理", self.open_container),
            ("订单管理", self.open_order),
            ("客户管理", self.open_customer),
            ("员工管理", self.open_employee),
            ("报表财务", self.open_report)
        ]
        for i, (text, cmd) in enumerate(modules):
            tk.Button(btn_frame, text=text, width=12, command=cmd).grid(row=i//3, column=i%3, padx=10, pady=10)
        tk.Label(self, text="系统版本：v1.0", fg="#888").pack(side=tk.BOTTOM, pady=10)

    def show_module(self, module_class):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = module_class(self)
        self.current_frame.pack(fill=tk.BOTH, expand=True)
        # 添加返回主菜单按钮
        btn = tk.Button(self.current_frame, text="返回主菜单", command=self.back_to_menu)
        btn.pack(side=tk.BOTTOM, pady=10)

    def back_to_menu(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = None
        self.build_ui()

    def open_meal(self):
        self.show_module(MealUI)
    def open_ingredient(self):
        self.show_module(IngredientUI)
    def open_container(self):
        self.show_module(ContainerUI)
    def open_order(self):
        self.show_module(OrderUI)
    def open_customer(self):
        self.show_module(CustomerUI)
    def open_employee(self):
        self.show_module(EmployeeUI)
    def open_report(self):
        self.show_module(ReportUI)

    # Getter/Setter
    def get_user_info(self):
        return self.user_info
    def set_user_info(self, value):
        self.user_info = value
