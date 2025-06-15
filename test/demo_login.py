#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
直接测试登录界面 - 强制显示所有按钮
"""

import tkinter as tk
from tkinter import messagebox

def create_demo_login():
    """创建演示登录界面"""
    root = tk.Tk()
    root.title("食品服务公司管理系统 - 登录")
    root.geometry("400x600")
    root.configure(bg="#f5f5f5")
    root.resizable(False, False)
    
    # 居中显示
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    # 主容器
    main_frame = tk.Frame(root, bg="#f5f5f5")
    main_frame.pack(fill="both", expand=True, padx=30, pady=30)
    
    # Logo区域
    logo_frame = tk.Frame(main_frame, bg="#f5f5f5")
    logo_frame.pack(pady=(0, 40))
    
    # 系统Logo
    logo_label = tk.Label(logo_frame, text="🍽️", font=("微软雅黑", 48), 
                         bg="#f5f5f5", fg="#07c160")
    logo_label.pack()
    
    title_label = tk.Label(logo_frame, text="食品服务管理系统", 
                          font=("微软雅黑", 20, "bold"), 
                          bg="#f5f5f5", fg="#2c3e50")
    title_label.pack(pady=(10, 0))
    
    # 登录表单容器
    form_frame = tk.Frame(main_frame, bg="#ffffff", relief="solid", bd=1)
    form_frame.pack(fill="x", pady=(0, 20))
    
    # 用户名输入
    username_frame = tk.Frame(form_frame, bg="#ffffff")
    username_frame.pack(fill="x", padx=20, pady=(20, 10))
    
    tk.Label(username_frame, text="用户名", font=("微软雅黑", 12), 
            bg="#ffffff", fg="#666666").pack(anchor="w")
    
    username_entry = tk.Entry(username_frame, font=("微软雅黑", 14), 
                             relief="flat", bd=5, bg="#f8f8f8")
    username_entry.pack(fill="x", pady=(5, 0), ipady=8)
    
    # 密码输入
    password_frame = tk.Frame(form_frame, bg="#ffffff")
    password_frame.pack(fill="x", padx=20, pady=(10, 20))
    
    tk.Label(password_frame, text="密码", font=("微软雅黑", 12), 
            bg="#ffffff", fg="#666666").pack(anchor="w")
    
    password_entry = tk.Entry(password_frame, font=("微软雅黑", 14), 
                             show="*", relief="flat", bd=5, bg="#f8f8f8")
    password_entry.pack(fill="x", pady=(5, 0), ipady=8)
    
    # 登录按钮
    def login_click():
        messagebox.showinfo("登录", "点击了登录按钮")
    
    login_btn = tk.Button(form_frame, text="🔐 立即登录", 
                         font=("微软雅黑", 16, "bold"),
                         bg="#07c160", fg="white", relief="flat", bd=0,
                         cursor="hand2", command=login_click,
                         width=20, height=2)
    login_btn.pack(padx=20, pady=(10, 25), ipady=15)
    
    # 功能按钮区域
    action_frame = tk.Frame(main_frame, bg="#f5f5f5")
    action_frame.pack(fill="x", pady=(0, 20))
    
    # 第一行按钮容器
    top_btn_frame = tk.Frame(action_frame, bg="#f5f5f5")
    top_btn_frame.pack(pady=(10, 15))
    
    # 注册按钮
    def register_click():
        messagebox.showinfo("注册", "点击了注册按钮")
    
    register_btn = tk.Button(top_btn_frame, text="📝 注册账户", 
                           font=("微软雅黑", 13), bg="#1485ee", fg="white",
                           relief="flat", bd=0, cursor="hand2", width=12,
                           command=register_click)
    register_btn.pack(side="left", padx=(0, 10), ipady=10)
    
    # 游客登录按钮
    def guest_click():
        messagebox.showinfo("游客", "点击了游客体验按钮")
    
    guest_btn = tk.Button(top_btn_frame, text="👤 游客体验", 
                        font=("微软雅黑", 13), bg="#fa9d3b", fg="white",
                        relief="flat", bd=0, cursor="hand2", width=12,
                        command=guest_click)
    guest_btn.pack(side="left", ipady=10)
    
    # 第二行按钮容器
    bottom_btn_frame = tk.Frame(action_frame, bg="#f5f5f5")
    bottom_btn_frame.pack(pady=(0, 15))
    
    # 测试按钮
    def test_click():
        messagebox.showinfo("测试", "点击了测试模式按钮")
    
    test_btn = tk.Button(bottom_btn_frame, text="🧪 测试模式", 
                       font=("微软雅黑", 13), bg="#ff6b6b", fg="white",
                       relief="flat", bd=0, cursor="hand2", width=25,
                       command=test_click)
    test_btn.pack(ipady=10)
    
    # 忘记密码链接
    def forgot_click():
        messagebox.showinfo("忘记密码", "点击了忘记密码按钮")
    
    forgot_btn = tk.Button(action_frame, text="忘记密码？", 
                         font=("微软雅黑", 11), bg="#f5f5f5", fg="#576b95",
                         relief="flat", bd=0, cursor="hand2",
                         command=forgot_click)
    forgot_btn.pack(pady=(10, 0))
    
    print("演示登录界面已创建，应该显示以下按钮:")
    print("✅ 🔐 立即登录 (绿色大按钮)")
    print("✅ 📝 注册账户 (蓝色按钮，左侧)")
    print("✅ 👤 游客体验 (橙色按钮，右侧)")
    print("✅ 🧪 测试模式 (红色按钮，居中)")
    print("✅ 忘记密码？ (文字链接)")
    
    root.mainloop()

if __name__ == "__main__":
    create_demo_login()
