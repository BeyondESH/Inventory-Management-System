#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk, messagebox
import os
from turtle import title
try:
    from .user_manager import UserManager, User
except ImportError:
    from user_manager import UserManager, User

class LoginModule:
    def __init__(self, on_login_success=None):
        self.root = tk.Tk()
        self.root.title("管理系统 - 登录")
        self.root.geometry("420x500") 
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
        self.root.geometry("420x500")
        self.clear_frame()
        self.current_view = "login"
        # 主容器 - 减小边距让界面更紧凑
        main_frame = tk.Frame(self.root, bg="#f5f5f5")
        main_frame.pack(fill="both", expand=True, padx=25, pady=20)
        # 标题区域
        title = tk.Frame(main_frame, bg="#f5f5f5")
        title.pack(pady=(10, 10))

        title_label = tk.Label(title, text="食品服务管理系统",
                              font=("微软雅黑", 18, "bold"),
                              bg="#f5f5f5", fg="#2c3e50")
        title_label.pack(pady=(10, 10))

        # 登录表单容器
        form_frame = tk.Frame(main_frame, bg="#ffffff", relief="solid", bd=1)
        form_frame.pack(fill="x", pady=(0, 15))
        
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
        login_btn = tk.Button(form_frame, text="🔐 立即登录", 
                             font=("微软雅黑", 12, "bold"),
                             bg="#07c160", fg="white", relief="flat", bd=0,
                             cursor="hand2", command=self.handle_login,
                             width=12, height=1)
        login_btn.pack(padx=20, pady=(10, 15), ipady=4)

        # 功能按钮区域 - 在表单框内，水平排列
        action_frame = tk.Frame(form_frame, bg="#ffffff")
        action_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        # 按钮容器 - 水平排列
        btn_container = tk.Frame(action_frame, bg="#ffffff")
        btn_container.pack(fill="x", pady=(5, 0))
        
        # 注册按钮
        register_btn = tk.Button(btn_container, text="📝注册", 
                               font=("微软雅黑", 8, "bold"), bg="#1485ee", fg="white",
                               relief="flat", bd=0, cursor="hand2", width=10,height=1,
                               command=self.create_register_interface)
        register_btn.pack(side="left", padx=(0, 8), ipady=4)
        
        # 忘记密码按钮
        forgot_btn = tk.Button(btn_container, text="忘记密码", 
                             font=("微软雅黑", 8, "bold"), bg="#9dda11", fg="white",
                             relief="flat", bd=0, cursor="hand2",width=10,height=1,
                             command=self.create_forgot_password_interface)
        forgot_btn.pack(side="left", padx=(0, 8), ipady=4)

        # 游客体验按钮
        guest_btn = tk.Button(btn_container, text="👤游客", 
                            font=("微软雅黑", 8, "bold"), bg="#fa9d3b", fg="white",
                            relief="flat", bd=0, cursor="hand2", width=10,height=1,
                            command=self.handle_guest_login)
        guest_btn.pack(side="left", padx=(0, 8), ipady=4)
        
        # 测试模式按钮
        test_btn = tk.Button(btn_container, text="🧪测试", 
                           font=("微软雅黑", 8, "bold"), bg="#ff6b6b", fg="white",
                           relief="flat", bd=0, cursor="hand2", width=10,height=1,
                           command=self.handle_test_login)
        test_btn.pack(side="left", padx=(0, 8) ,ipady=4)

        # 设置回车键登录
        self.root.bind('<Return>', lambda e: self.handle_login())
        
        # 默认焦点
        self.username_entry.focus()
    
    def create_register_interface(self):
        """创建注册界面"""
        self.clear_frame()
        self.current_view = "register"
        self.root.geometry("420x670") 
        # 主容器
        main_frame = tk.Frame(self.root, bg="#f5f5f5")
        main_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        # 标题区域
        title_frame = tk.Frame(main_frame, bg="#f5f5f5")
        title_frame.pack(pady=(10, 10))
        
        title_label = tk.Label(title_frame, text="📝 注册新账户", 
                              font=("微软雅黑", 18, "bold"), 
                              bg="#f5f5f5", fg="#2c3e50")
        title_label.pack(pady=(10, 10))
        
        # 注册表单容器
        form_frame = tk.Frame(main_frame, bg="#ffffff", relief="solid", bd=1)
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
        register_btn = tk.Button(form_frame, text="✅ 立即注册", 
                               font=("微软雅黑", 12, "bold"),
                               bg="#1485ee", fg="white", relief="flat", bd=0,
                               cursor="hand2", command=self.handle_register,
                               width=12, height=1)
        register_btn.pack(side="left", padx=(30, 20), pady=(10, 15), ipady=4)
        
        # 返回登录按钮
        login_btn = tk.Button(form_frame, text="🔙 返回登录",
                            font=("微软雅黑", 13), bg="#95a5a6", fg="white",
                            relief="flat", bd=0, cursor="hand2", width=12,
                            command=self.create_login_interface)
        login_btn.pack(side="left",padx=(20, 30), pady=(10, 15), ipady=4)
        
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
        
        back_btn = tk.Button(title_frame, text="← 返回登录", 
                           font=("微软雅黑", 12), bg="#f5f5f5", fg="#576b95",
                           relief="flat", bd=0, cursor="hand2",
                           command=self.create_login_interface)
        back_btn.pack(anchor="w")
        
        title_label = tk.Label(title_frame, text="🔑 找回密码", 
                              font=("微软雅黑", 20, "bold"), 
                              bg="#f5f5f5", fg="#2c3e50")
        title_label.pack(pady=(10, 0))
        
        # 提示信息
        tip_label = tk.Label(main_frame, text="请输入您的注册邮箱，我们将发送重置链接", 
                           font=("微软雅黑", 12), bg="#f5f5f5", fg="#7f8c8d")
        tip_label.pack(pady=(0, 20))
        
        # 重置表单容器
        form_frame = tk.Frame(main_frame, bg="#ffffff", relief="solid", bd=1)
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
        reset_btn = tk.Button(form_frame, text="📧 发送重置链接", 
                             font=("微软雅黑", 16, "bold"),
                             bg="#e67e22", fg="white", relief="flat", bd=0,
                             cursor="hand2", command=self.handle_password_reset,
                             width=20, height=2)
        reset_btn.pack(padx=20, pady=(10, 25), ipady=15)
        
        # 功能按钮区域
        btn_container = tk.Frame(main_frame, bg="#f5f5f5")
        btn_container.pack(fill="x", pady=(0, 20))
        
        # 游客体验按钮
        guest_btn = tk.Button(btn_container, text="👤 游客体验", 
                            font=("微软雅黑", 13), bg="#fa9d3b", fg="white",
                            relief="flat", bd=0, cursor="hand2", width=12,
                            command=self.handle_guest_login)
        guest_btn.pack(side="left", padx=(0, 10), ipady=10)
        
        # 返回登录按钮
        login_btn = tk.Button(btn_container, text="🔙 返回登录", 
                            font=("微软雅黑", 13), bg="#95a5a6", fg="white",
                            relief="flat", bd=0, cursor="hand2", width=12,
                            command=self.create_login_interface)
        login_btn.pack(side="left", ipady=10)
        
        # 默认焦点
        self.reset_email_entry.focus()
    
    def handle_login(self):
        """处理登录"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username:
            messagebox.showerror("错误", "请输入用户名")
            return
        
        if not password:
            messagebox.showerror("错误", "请输入密码")
            return
          # 验证登录
        success, message = self.user_manager.login_user(username, password)
        if success:
            messagebox.showinfo("登录成功", f"欢迎回来，{username}！")
            self.close_and_start_main()
        else:
            messagebox.showerror("登录失败", message)
    
    def handle_register(self):
        """处理注册"""
        username = self.reg_username_entry.get().strip()
        email = self.reg_email_entry.get().strip()
        password = self.reg_password_entry.get().strip()
        confirm = self.reg_confirm_entry.get().strip()
        
        if not username:
            messagebox.showerror("错误", "请输入用户名")
            return
        
        if not email:
            messagebox.showerror("错误", "请输入邮箱")
            return
        
        if not password:
            messagebox.showerror("错误", "请输入密码")
            return
        
        if password != confirm:
            messagebox.showerror("错误", "两次输入的密码不一致")
            return
          # 注册用户
        success, message = self.user_manager.register_user(username, email, password)
        if success:
            messagebox.showinfo("注册成功", "账户创建成功！请登录。")
            self.create_login_interface()
        else:
            messagebox.showerror("注册失败", message)
    
    def handle_password_reset(self):
        """处理密码重置"""
        email = self.reset_email_entry.get().strip()
        
        if not email:
            messagebox.showerror("错误", "请输入注册邮箱")
            return
        
        # 模拟发送重置邮件
        messagebox.showinfo("重置链接已发送", 
                          f"密码重置链接已发送到 {email}，请检查您的邮箱。")
        self.create_login_interface()
    
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
        self.user_manager.current_user = User(
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
