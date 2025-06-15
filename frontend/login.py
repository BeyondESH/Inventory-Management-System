import tkinter as tk
from tkinter import ttk
from utils import show_info, show_error

class LoginUI(tk.Frame):
    def __init__(self, master, login_callback):
        super().__init__(master)
        self.login_callback = login_callback
        self.email = tk.StringVar()
        self.password = tk.StringVar()
        self.build_ui()

    def build_ui(self):
        self.columnconfigure(0, weight=1)
        tk.Label(self, text="欢迎登录", font=("微软雅黑", 20)).grid(row=0, column=0, pady=30)
        tk.Label(self, text="邮箱:").grid(row=1, column=0, sticky="w", padx=100)
        tk.Entry(self, textvariable=self.email).grid(row=2, column=0, padx=100, pady=5, sticky="ew")
        tk.Label(self, text="密码:").grid(row=3, column=0, sticky="w", padx=100)
        tk.Entry(self, textvariable=self.password, show="*").grid(row=4, column=0, padx=100, pady=5, sticky="ew")
        tk.Button(self, text="登录", command=self.login).grid(row=5, column=0, pady=15)
        tk.Button(self, text="注册新用户", command=self.register).grid(row=6, column=0)

    def login(self):
        # 这里应接入数据库校验
        if self.email.get() and self.password.get():
            # 假设登录成功
            user_info = {"email": self.email.get(), "role": "admin"}
            self.login_callback(user_info)
        else:
            show_error("登录失败", "请输入邮箱和密码")

    def register(self):
        RegisterWindow(self)

class RegisterWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("用户注册")
        self.geometry("350x350")
        self.resizable(False, False)
        self.parent = parent
        self.name = tk.StringVar()
        self.email = tk.StringVar()
        self.phone = tk.StringVar()
        self.password = tk.StringVar()
        self.confirm = tk.StringVar()
        self.build_ui()

    def build_ui(self):
        tk.Label(self, text="用户注册", font=("微软雅黑", 16)).pack(pady=15)
        form = tk.Frame(self)
        form.pack(pady=5)
        tk.Label(form, text="姓名:").grid(row=0, column=0, sticky="e", pady=5)
        tk.Entry(form, textvariable=self.name).grid(row=0, column=1, pady=5)
        tk.Label(form, text="邮箱:").grid(row=1, column=0, sticky="e", pady=5)
        tk.Entry(form, textvariable=self.email).grid(row=1, column=1, pady=5)
        tk.Label(form, text="电话:").grid(row=2, column=0, sticky="e", pady=5)
        tk.Entry(form, textvariable=self.phone).grid(row=2, column=1, pady=5)
        tk.Label(form, text="密码:").grid(row=3, column=0, sticky="e", pady=5)
        tk.Entry(form, textvariable=self.password, show="*").grid(row=3, column=1, pady=5)
        tk.Label(form, text="确认密码:").grid(row=4, column=0, sticky="e", pady=5)
        tk.Entry(form, textvariable=self.confirm, show="*").grid(row=4, column=1, pady=5)
        tk.Button(self, text="注册", command=self.do_register).pack(pady=15)

    def do_register(self):
        name = self.name.get().strip()
        email = self.email.get().strip()
        phone = self.phone.get().strip()
        pwd = self.password.get()
        confirm = self.confirm.get()
        if not name or not email or not pwd:
            show_error("注册失败", "姓名、邮箱和密码不能为空")
            return
        if '@' not in email or '.' not in email:
            show_error("注册失败", "邮箱格式不正确")
            return
        if pwd != confirm:
            show_error("注册失败", "两次输入的密码不一致")
            return
        # 简单模拟唯一性校验和保存（可用文件或数据库，现用内存）
        if hasattr(self.parent, 'registered_users'):
            users = self.parent.registered_users
        else:
            users = {}
            self.parent.registered_users = users
        if email in users:
            show_error("注册失败", "该邮箱已注册")
            return
        users[email] = {"name": name, "phone": phone, "password": pwd}
        show_info("注册成功", "注册成功，正在自动登录……")
        self.destroy()
        # 自动登录
        user_info = {"email": email, "name": name, "role": "user"}
        self.parent.login_callback(user_info)

    # Getter/Setter
    def get_email(self):
        return self.email.get()
    def set_email(self, value):
        self.email.set(value)
    def get_password(self):
        return self.password.get()
    def set_password(self, value):
        self.password.set(value)
