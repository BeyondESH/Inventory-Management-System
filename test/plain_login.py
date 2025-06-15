#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
纯文字版登录界面 - 不使用emoji，确保兼容性
"""

import tkinter as tk
from tkinter import messagebox

def create_text_login():
    """创建纯文字版登录界面"""
    root = tk.Tk()
    root.title("食品服务公司管理系统 - 登录")
    root.geometry("450x650")  # 增加高度确保所有按钮可见
    root.configure(bg="#f5f5f5")
    root.resizable(True, True)  # 允许调整大小
    
    # 居中显示
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    # 添加滚动条
    canvas = tk.Canvas(root, bg="#f5f5f5")
    scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#f5f5f5")
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    # 主容器
    main_frame = tk.Frame(scrollable_frame, bg="#f5f5f5")
    main_frame.pack(fill="both", expand=True, padx=30, pady=30)
    
    # Logo区域
    logo_frame = tk.Frame(main_frame, bg="#f5f5f5")
    logo_frame.pack(pady=(0, 40))
    
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
    
    login_btn = tk.Button(form_frame, text="立即登录", 
                         font=("微软雅黑", 16, "bold"),
                         bg="#07c160", fg="white", relief="flat", bd=0,
                         cursor="hand2", command=login_click,
                         width=20, height=2)
    login_btn.pack(padx=20, pady=(10, 25), ipady=15)
    
    # 功能按钮区域
    action_frame = tk.Frame(main_frame, bg="#f5f5f5")
    action_frame.pack(fill="x", pady=(0, 20))
    
    # 添加分隔线
    separator = tk.Frame(action_frame, bg="#ddd", height=1)
    separator.pack(fill="x", pady=(10, 15))
    
    # 按钮说明
    label = tk.Label(action_frame, text="其他登录选项:", font=("微软雅黑", 12, "bold"), 
                    bg="#f5f5f5", fg="#2c3e50")
    label.pack(pady=(0, 10))
    
    # 第一行按钮容器
    top_btn_frame = tk.Frame(action_frame, bg="#f5f5f5")
    top_btn_frame.pack(pady=(10, 15), fill="x")
    
    # 注册按钮
    def register_click():
        messagebox.showinfo("注册", "点击了注册按钮")
    
    register_btn = tk.Button(top_btn_frame, text="注册新账户", 
                           font=("微软雅黑", 13, "bold"), bg="#1485ee", fg="white",
                           relief="flat", bd=0, cursor="hand2", width=15,
                           command=register_click, height=2)
    register_btn.pack(side="left", padx=(0, 10), ipady=10, fill="x", expand=True)
    
    # 游客登录按钮
    def guest_click():
        messagebox.showinfo("游客", "点击了游客体验按钮 - 将直接进入主界面！")
    
    guest_btn = tk.Button(top_btn_frame, text="游客体验", 
                        font=("微软雅黑", 13, "bold"), bg="#fa9d3b", fg="white",
                        relief="flat", bd=0, cursor="hand2", width=15,
                        command=guest_click, height=2)
    guest_btn.pack(side="left", ipady=10, fill="x", expand=True)
    
    # 第二行按钮容器
    bottom_btn_frame = tk.Frame(action_frame, bg="#f5f5f5")
    bottom_btn_frame.pack(pady=(0, 15), fill="x")
    
    # 测试按钮
    def test_click():
        messagebox.showinfo("测试", "点击了测试模式按钮")
    
    test_btn = tk.Button(bottom_btn_frame, text="测试模式", 
                       font=("微软雅黑", 13, "bold"), bg="#ff6b6b", fg="white",
                       relief="flat", bd=0, cursor="hand2", 
                       command=test_click, height=2)
    test_btn.pack(ipady=10, fill="x", padx=20)
    
    # 忘记密码链接
    def forgot_click():
        messagebox.showinfo("忘记密码", "点击了忘记密码按钮")
    
    forgot_btn = tk.Button(action_frame, text="忘记密码？", 
                         font=("微软雅黑", 11, "underline"), bg="#f5f5f5", fg="#576b95",
                         relief="flat", bd=0, cursor="hand2",
                         command=forgot_click)
    forgot_btn.pack(pady=(15, 0))
    
    # 布局画布和滚动条
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    print("✅ 纯文字版登录界面已创建，包含以下按钮:")
    print("   1. [立即登录] - 绿色大按钮")
    print("   2. [注册新账户] - 蓝色按钮")
    print("   3. [游客体验] - 橙色按钮 (点击直接进入主界面)")
    print("   4. [测试模式] - 红色按钮")
    print("   5. [忘记密码？] - 下划线文字链接")
    print("")
    print("📝 如果你只看到登录按钮，请尝试:")
    print("   - 向下滚动查看更多按钮")
    print("   - 调整窗口大小")
    print("   - 检查是否有显示问题")
    
    root.mainloop()

if __name__ == "__main__":
    create_text_login()
