#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
登录注册模块
类似微信登录界面的设计风格
"""

import tkinter as tk
from tkinter import ttk, messagebox
import os
try:
    from .user_manager import UserManager
except ImportError:
    from user_manager import UserManager

class LoginModule:
    def __init__(self, on_login_success=None):
        self.root = tk.Tk()
        self.root.title("食品服务公司管理系统 - 登录")
        self.root.geometry("400x600")
        self.root.configure(bg="#f5f5f5")
        self.root.resizable(False, False)
        
        # 用户管理器
        self.user_manager = UserManager()
        
        # 登录成功回调
        self.on_login_success = on_login_success
        
        # 当前界面状态
        self.current_view = "login"  # login, register, forgot_password
        
        # 设置窗口图标
        self.set_window_icon()
        
        # 居中显示窗口
        self.center_window()        
        # 创建界面
        self.create_login_interface()
        
    def set_window_icon(self):
        """设置窗口图标"""
        try:
            # 获取项目根目录的image文件夹路径
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(current_dir)
            icon_path = os.path.join(project_root, "image", "icon", "main.ico")
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except:
            pass
    
    def center_window(self):
        """窗口居中显示"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def clear_frame(self):
        """清空当前界面"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def create_login_interface(self):
        """创建登录界面"""
        self.clear_frame()
        self.current_view = "login"
        
        # 主容器
        main_frame = tk.Frame(self.root, bg="#f5f5f5")
        main_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Logo区域
        logo_frame = tk.Frame(main_frame, bg="#f5f5f5")
        logo_frame.pack(pady=(0, 40))
        
        # 系统Logo（使用文字替代图片）
        logo_label = tk.Label(logo_frame, text="🍽️", font=("Arial", 48), bg="#f5f5f5")
        logo_label.pack()
        
        title_label = tk.Label(logo_frame, text="食品服务管理系统", 
                              font=("微软雅黑", 16, "bold"), 
                              bg="#f5f5f5", fg="#333333")
        title_label.pack(pady=(10, 0))
        
        # 登录表单区域
        form_frame = tk.Frame(main_frame, bg="#ffffff", relief="flat", bd=1)
        form_frame.pack(fill="x", pady=(0, 20))
        
        # 用户名输入
        username_frame = tk.Frame(form_frame, bg="#ffffff")
        username_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        tk.Label(username_frame, text="用户名", font=("微软雅黑", 12), 
                bg="#ffffff", fg="#666666").pack(anchor="w")
        
        self.username_entry = tk.Entry(username_frame, font=("微软雅黑", 14), 
                                      relief="flat", bd=5, bg="#f8f8f8")
        self.username_entry.pack(fill="x", pady=(5, 0), ipady=8)
        
        # 密码输入
        password_frame = tk.Frame(form_frame, bg="#ffffff")
        password_frame.pack(fill="x", padx=20, pady=(10, 20))
        
        tk.Label(password_frame, text="密码", font=("微软雅黑", 12), 
                bg="#ffffff", fg="#666666").pack(anchor="w")
        
        self.password_entry = tk.Entry(password_frame, font=("微软雅黑", 14), 
                                      show="*", relief="flat", bd=5, bg="#f8f8f8")
        self.password_entry.pack(fill="x", pady=(5, 0), ipady=8)
        
        # 登录按钮
        login_btn = tk.Button(form_frame, text="登录", font=("微软雅黑", 14, "bold"),
                             bg="#07c160", fg="white", relief="flat", bd=0,
                             cursor="hand2", command=self.handle_login)
        login_btn.pack(fill="x", padx=20, pady=(0, 20), ipady=10)
          # 功能按钮区域
        action_frame = tk.Frame(main_frame, bg="#f5f5f5")
        action_frame.pack(fill="x", pady=(0, 20))
        
        # 注册按钮
        register_btn = tk.Button(action_frame, text="注册新账户", 
                               font=("微软雅黑", 12), bg="#1485ee", fg="white",
                               relief="flat", bd=0, cursor="hand2",
                               command=self.create_register_interface)
        register_btn.pack(fill="x", pady=(0, 12), ipady=10)
        
        # 游客登录按钮
        guest_btn = tk.Button(action_frame, text="游客登录", 
                            font=("微软雅黑", 12), bg="#fa9d3b", fg="white",
                            relief="flat", bd=0, cursor="hand2",
                            command=self.handle_guest_login)
        guest_btn.pack(fill="x", pady=(0, 12), ipady=10)
        
        # 测试按钮
        test_btn = tk.Button(action_frame, text="🧪 测试模式（直接进入）", 
                           font=("微软雅黑", 12), bg="#ff6b6b", fg="white",
                           relief="flat", bd=0, cursor="hand2",
                           command=self.handle_test_login)
        test_btn.pack(fill="x", pady=(0, 20), ipady=10)
        
        # 忘记密码链接
        forgot_btn = tk.Button(action_frame, text="忘记密码？", 
                             font=("微软雅黑", 10), bg="#f5f5f5", fg="#576b95",
                             relief="flat", bd=0, cursor="hand2",
                             command=self.create_forgot_password_interface)
        forgot_btn.pack()
        
        # 设置回车键登录
        self.root.bind('<Return>', lambda e: self.handle_login())
        
        # 默认焦点
        self.username_entry.focus()
    
    def create_register_interface(self):
        """创建注册界面"""
        self.clear_frame()
        self.current_view = "register"
        
        # 主容器
        main_frame = tk.Frame(self.root, bg="#f5f5f5")
        main_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        # 标题区域
        title_frame = tk.Frame(main_frame, bg="#f5f5f5")
        title_frame.pack(pady=(0, 30))
        
        # 返回按钮
        back_btn = tk.Button(title_frame, text="← 返回登录", 
                           font=("微软雅黑", 12), bg="#f5f5f5", fg="#576b95",
                           relief="flat", bd=0, cursor="hand2",
                           command=self.create_login_interface)
        back_btn.pack(anchor="w")
        
        title_label = tk.Label(title_frame, text="注册新账户", 
                              font=("微软雅黑", 18, "bold"), 
                              bg="#f5f5f5", fg="#333333")
        title_label.pack(pady=(10, 0))
        
        # 注册表单区域
        form_frame = tk.Frame(main_frame, bg="#ffffff", relief="flat", bd=1)
        form_frame.pack(fill="x", pady=(0, 20))
        
        # 用户名输入
        username_frame = tk.Frame(form_frame, bg="#ffffff")
        username_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        tk.Label(username_frame, text="用户名", font=("微软雅黑", 12), 
                bg="#ffffff", fg="#666666").pack(anchor="w")
        
        self.reg_username_entry = tk.Entry(username_frame, font=("微软雅黑", 14), 
                                          relief="flat", bd=5, bg="#f8f8f8")
        self.reg_username_entry.pack(fill="x", pady=(5, 0), ipady=8)
        
        # 邮箱输入
        email_frame = tk.Frame(form_frame, bg="#ffffff")
        email_frame.pack(fill="x", padx=20, pady=(10, 10))
        
        tk.Label(email_frame, text="邮箱", font=("微软雅黑", 12), 
                bg="#ffffff", fg="#666666").pack(anchor="w")
        
        self.reg_email_entry = tk.Entry(email_frame, font=("微软雅黑", 14), 
                                       relief="flat", bd=5, bg="#f8f8f8")
        self.reg_email_entry.pack(fill="x", pady=(5, 0), ipady=8)
        
        # 密码输入
        password_frame = tk.Frame(form_frame, bg="#ffffff")
        password_frame.pack(fill="x", padx=20, pady=(10, 10))
        
        tk.Label(password_frame, text="密码", font=("微软雅黑", 12), 
                bg="#ffffff", fg="#666666").pack(anchor="w")
        
        self.reg_password_entry = tk.Entry(password_frame, font=("微软雅黑", 14), 
                                          show="*", relief="flat", bd=5, bg="#f8f8f8")
        self.reg_password_entry.pack(fill="x", pady=(5, 0), ipady=8)
          # 确认密码输入
        confirm_frame = tk.Frame(form_frame, bg="#ffffff")
        confirm_frame.pack(fill="x", padx=20, pady=(10, 20))
        
        tk.Label(confirm_frame, text="确认密码", font=("微软雅黑", 12), 
                bg="#ffffff", fg="#666666").pack(anchor="w")
        
        self.reg_confirm_entry = tk.Entry(confirm_frame, font=("微软雅黑", 14), 
                                         show="*", relief="flat", bd=5, bg="#f8f8f8")
        self.reg_confirm_entry.pack(fill="x", pady=(5, 0), ipady=8)
        
        # 注册按钮
        register_btn = tk.Button(form_frame, text="注册新用户", font=("微软雅黑", 14, "bold"),
                               bg="#1485ee", fg="white", relief="flat", bd=0,
                               cursor="hand2", command=self.handle_register)
        register_btn.pack(fill="x", padx=20, pady=(10, 20), ipady=12)
        
        # 功能按钮区域
        action_frame = tk.Frame(main_frame, bg="#f5f5f5")
        action_frame.pack(fill="x", pady=(10, 20))
        
        # 游客登录按钮
        guest_btn = tk.Button(action_frame, text="游客登录", 
                            font=("微软雅黑", 12), bg="#fa9d3b", fg="white",
                            relief="flat", bd=0, cursor="hand2",
                            command=self.handle_guest_login)
        guest_btn.pack(fill="x", pady=(0, 10), ipady=8)
        
        # 测试按钮
        test_btn = tk.Button(action_frame, text="🧪 测试模式（直接进入）", 
                           font=("微软雅黑", 12), bg="#ff6b6b", fg="white",
                           relief="flat", bd=0, cursor="hand2",
                           command=self.handle_test_login)
        test_btn.pack(fill="x", ipady=8)
        
        # 密码要求提示
        tip_label = tk.Label(main_frame, 
                           text="密码要求：长度6-20位，包含字母和数字", 
                           font=("微软雅黑", 10), bg="#f5f5f5", fg="#999999")
        tip_label.pack(pady=(10, 0))
        
        # 设置回车键注册
        self.root.bind('<Return>', lambda e: self.handle_register())
        
        # 默认焦点
        self.reg_username_entry.focus()
    
    def create_forgot_password_interface(self):
        """创建忘记密码界面"""
        self.clear_frame()
        self.current_view = "forgot_password"
        
        # 主容器
        main_frame = tk.Frame(self.root, bg="#f5f5f5")
        main_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        # 标题区域
        title_frame = tk.Frame(main_frame, bg="#f5f5f5")
        title_frame.pack(pady=(0, 30))
        
        # 返回按钮
        back_btn = tk.Button(title_frame, text="← 返回登录", 
                           font=("微软雅黑", 12), bg="#f5f5f5", fg="#576b95",
                           relief="flat", bd=0, cursor="hand2",
                           command=self.create_login_interface)
        back_btn.pack(anchor="w")
        
        title_label = tk.Label(title_frame, text="重置密码", 
                              font=("微软雅黑", 18, "bold"), 
                              bg="#f5f5f5", fg="#333333")
        title_label.pack(pady=(10, 0))
        
        # 说明文字
        desc_label = tk.Label(main_frame, 
                            text="请输入您的注册邮箱，我们将向您发送临时密码", 
                            font=("微软雅黑", 12), bg="#f5f5f5", fg="#666666",
                            wraplength=300)
        desc_label.pack(pady=(0, 20))
        
        # 重置表单区域
        form_frame = tk.Frame(main_frame, bg="#ffffff", relief="flat", bd=1)
        form_frame.pack(fill="x", pady=(0, 20))
        
        # 邮箱输入
        email_frame = tk.Frame(form_frame, bg="#ffffff")
        email_frame.pack(fill="x", padx=20, pady=(20, 20))
        
        tk.Label(email_frame, text="注册邮箱", font=("微软雅黑", 12), 
                bg="#ffffff", fg="#666666").pack(anchor="w")
        
        self.reset_email_entry = tk.Entry(email_frame, font=("微软雅黑", 14), 
                                         relief="flat", bd=5, bg="#f8f8f8")
        self.reset_email_entry.pack(fill="x", pady=(5, 0), ipady=8)
          # 重置按钮
        reset_btn = tk.Button(form_frame, text="发送临时密码", font=("微软雅黑", 14, "bold"),
                            bg="#fa9d3b", fg="white", relief="flat", bd=0,
                            cursor="hand2", command=self.handle_reset_password)
        reset_btn.pack(fill="x", padx=20, pady=(10, 20), ipady=12)
        
        # 功能按钮区域
        action_frame = tk.Frame(main_frame, bg="#f5f5f5")
        action_frame.pack(fill="x", pady=(10, 20))
        
        # 游客登录按钮
        guest_btn = tk.Button(action_frame, text="游客登录", 
                            font=("微软雅黑", 12), bg="#fa9d3b", fg="white",
                            relief="flat", bd=0, cursor="hand2",
                            command=self.handle_guest_login)
        guest_btn.pack(fill="x", pady=(0, 10), ipady=8)
        
        # 测试按钮
        test_btn = tk.Button(action_frame, text="🧪 测试模式（直接进入）", 
                           font=("微软雅黑", 12), bg="#ff6b6b", fg="white",
                           relief="flat", bd=0, cursor="hand2",
                           command=self.handle_test_login)
        test_btn.pack(fill="x", ipady=8)
        
        # 设置回车键重置
        self.root.bind('<Return>', lambda e: self.handle_reset_password())
        
        # 默认焦点
        self.reset_email_entry.focus()
    
    def handle_login(self):
        """处理登录"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("错误", "请输入用户名和密码")
            return
        
        success, message = self.user_manager.login_user(username, password)
        
        if success:
            messagebox.showinfo("成功", message)
            self.close_and_start_main()
        else:
            messagebox.showerror("登录失败", message)
    
    def handle_register(self):
        """处理注册"""
        username = self.reg_username_entry.get().strip()
        email = self.reg_email_entry.get().strip()
        password = self.reg_password_entry.get()
        confirm_password = self.reg_confirm_entry.get()
        
        if not username or not email or not password or not confirm_password:
            messagebox.showerror("错误", "请填写所有字段")
            return
        
        if password != confirm_password:
            messagebox.showerror("错误", "两次输入的密码不一致")
            return
        
        success, message = self.user_manager.register_user(username, email, password)
        
        if success:
            messagebox.showinfo("成功", message + "\n请使用新账户登录")
            self.create_login_interface()
        else:
            messagebox.showerror("注册失败", message)
    
    def handle_reset_password(self):
        """处理重置密码"""
        email = self.reset_email_entry.get().strip()
        
        if not email:
            messagebox.showerror("错误", "请输入邮箱地址")
            return
        
        success, message = self.user_manager.reset_password(email)
        
        if success:
            messagebox.showinfo("密码重置成功", message)
            self.create_login_interface()
        else:
            messagebox.showerror("重置失败", message)
    
    def handle_guest_login(self):
        """处理游客登录"""
        success, message = self.user_manager.guest_login()
        if success:
            messagebox.showinfo("游客登录", "您正在以游客身份使用系统")
            self.close_and_start_main()
    
    def handle_test_login(self):
        """处理测试登录"""
        # 创建测试用户
        test_user_name = "测试用户"
        self.user_manager.current_user = self.user_manager.User(
            test_user_name, "test@test.com", ""
        )
        messagebox.showinfo("测试模式", "已进入测试模式，直接访问系统")
        self.close_and_start_main()
    
    def close_and_start_main(self):
        """关闭登录窗口并启动主系统"""
        if self.on_login_success:
            self.root.destroy()
            self.on_login_success(self.user_manager)
        else:
            self.root.destroy()
    
    def run(self):
        """运行登录界面"""
        self.root.mainloop()
        return self.user_manager
