#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
重新优化的登录界面 - 紧凑布局
"""

import tkinter as tk
from tkinter import messagebox

def create_compact_login():
    """创建紧凑布局的登录界面"""
    root = tk.Tk()
    root.title("食品服务公司管理系统 - 登录")
    root.geometry("420x550")  # 进一步减小高度
    root.configure(bg="#f5f5f5")
    root.resizable(True, True)
    
    # 居中显示
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    # 主容器
    main_frame = tk.Frame(root, bg="#f5f5f5")
    main_frame.pack(fill="both", expand=True, padx=25, pady=20)
    
    # Logo区域
    logo_frame = tk.Frame(main_frame, bg="#f5f5f5")
    logo_frame.pack(pady=(0, 20))
    
    # 系统Logo
    logo_label = tk.Label(logo_frame, text="🍽️", font=("微软雅黑", 40), 
                         bg="#f5f5f5", fg="#07c160")
    logo_label.pack()
    
    title_label = tk.Label(logo_frame, text="食品服务管理系统", 
                          font=("微软雅黑", 18, "bold"), 
                          bg="#f5f5f5", fg="#2c3e50")
    title_label.pack(pady=(8, 0))
    
    # 登录表单容器
    form_frame = tk.Frame(main_frame, bg="#ffffff", relief="solid", bd=1)
    form_frame.pack(fill="x", pady=(0, 15))
    
    # 用户名输入
    username_frame = tk.Frame(form_frame, bg="#ffffff")
    username_frame.pack(fill="x", padx=20, pady=(20, 10))
    
    tk.Label(username_frame, text="用户名", font=("微软雅黑", 11), 
            bg="#ffffff", fg="#666666").pack(anchor="w")
    
    username_entry = tk.Entry(username_frame, font=("微软雅黑", 13), 
                             relief="flat", bd=5, bg="#f8f8f8")
    username_entry.pack(fill="x", pady=(5, 0), ipady=6)
    
    # 密码输入
    password_frame = tk.Frame(form_frame, bg="#ffffff")
    password_frame.pack(fill="x", padx=20, pady=(10, 15))
    
    tk.Label(password_frame, text="密码", font=("微软雅黑", 11), 
            bg="#ffffff", fg="#666666").pack(anchor="w")
    
    password_entry = tk.Entry(password_frame, font=("微软雅黑", 13), 
                             show="*", relief="flat", bd=5, bg="#f8f8f8")
    password_entry.pack(fill="x", pady=(5, 0), ipady=6)
    
    # 登录按钮 - 更小更精致
    def login_click():
        messagebox.showinfo("登录", "点击了登录按钮")
    
    login_btn = tk.Button(form_frame, text="🔐 立即登录", 
                         font=("微软雅黑", 12, "bold"),
                         bg="#07c160", fg="white", relief="flat", bd=0,
                         cursor="hand2", command=login_click,
                         width=12, height=1)
    login_btn.pack(padx=20, pady=(10, 15), ipady=4)
    
    # 功能按钮区域 - 在表单框内，水平排列
    action_frame = tk.Frame(form_frame, bg="#ffffff")
    action_frame.pack(fill="x", padx=20, pady=(0, 15))
    
    # 按钮容器 - 水平排列
    btn_container = tk.Frame(action_frame, bg="#ffffff")
    btn_container.pack(fill="x", pady=(5, 0))
    
    # 注册按钮
    def register_click():
        messagebox.showinfo("注册", "点击了注册按钮")
    
    register_btn = tk.Button(btn_container, text="📝 注册", 
                           font=("微软雅黑", 10), bg="#1485ee", fg="white",
                           relief="flat", bd=0, cursor="hand2", width=6,
                           command=register_click)
    register_btn.pack(side="left", padx=(0, 8), ipady=3)
    
    # 游客体验按钮
    def guest_click():
        messagebox.showinfo("游客", "点击了游客体验按钮 - 将直接进入主界面！")
    
    guest_btn = tk.Button(btn_container, text="👤 游客", 
                        font=("微软雅黑", 10), bg="#fa9d3b", fg="white",
                        relief="flat", bd=0, cursor="hand2", width=6,
                        command=guest_click)
    guest_btn.pack(side="left", padx=(0, 8), ipady=3)
    
    # 测试模式按钮
    def test_click():
        messagebox.showinfo("测试", "点击了测试模式按钮")
    
    test_btn = tk.Button(btn_container, text="🧪 测试", 
                       font=("微软雅黑", 10), bg="#ff6b6b", fg="white",
                       relief="flat", bd=0, cursor="hand2", width=6,
                       command=test_click)
    test_btn.pack(side="left", ipady=3)
    
    # 忘记密码链接 - 居中显示
    def forgot_click():
        messagebox.showinfo("忘记密码", "点击了忘记密码链接")
    
    forgot_btn = tk.Button(action_frame, text="忘记密码？", 
                         font=("微软雅黑", 9), bg="#ffffff", fg="#576b95",
                         relief="flat", bd=0, cursor="hand2",
                         command=forgot_click)
    forgot_btn.pack(pady=(8, 0))
    
    print("🎨 紧凑布局登录界面已创建:")
    print("   ✅ 窗口大小: 420x550")
    print("   ✅ 登录按钮: 更小更精致 (12宽度)")
    print("   ✅ 功能按钮: 都在表单框内，水平排列")
    print("   ✅ 按钮尺寸: 紧凑 (6宽度)")
    print("   ✅ 布局: 所有按钮都在黑框内")
    print("")
    print("📝 按钮布局:")
    print("   [🔐 立即登录]     <- 大一点的主按钮")
    print("   [📝 注册] [👤 游客] [🧪 测试]  <- 水平排列")
    print("   忘记密码？        <- 小链接")
    
    root.mainloop()

if __name__ == "__main__":
    create_compact_login()
