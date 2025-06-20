#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
现代化登录模块 - 提供美观的用户登录界面
"""

import tkinter as tk
from tkinter import ttk, messagebox
import os
import math
import datetime
from PIL import Image, ImageTk
try:
    from ..core.user_manager import UserManager, User
except ImportError:
    import sys
    import os
    # 添加core目录到路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    core_dir = os.path.join(os.path.dirname(current_dir), 'core')
    sys.path.insert(0, core_dir)
    from user_manager import UserManager, User

class ModernLoginModule:
    def __init__(self, on_login_success=None):
        self.root = tk.Tk()
        self.root.title("智慧餐饮管理系统")
        self.root.geometry("900x600") 
        self.root.configure(bg="#ffffff")
        self.root.resizable(False, False)
        
        # 现代化颜色主题
        self.colors = {
            'primary': '#FF6B35',      # 主色调
            'secondary': '#F7931E',    # 次色调
            'accent': '#FFD23F',       # 强调色
            'background': '#F8F9FA',   # 背景色
            'surface': '#FFFFFF',      # 卡片背景
            'text_primary': '#2D3436', # 主文字
            'text_secondary': '#636E72', # 次文字
            'border': '#E0E0E0',       # 边框
            'hover': '#E17055',        # 悬停色
            'success': '#00B894',      # 成功色
            'error': '#E84393',        # 错误色
            'input_bg': '#F8F9FA',     # 输入框背景
            'input_focus': '#E8F4FD'   # 输入框焦点
        }
        
        # 字体配置
        self.fonts = {
            'title': ('Microsoft YaHei UI', 28, 'bold'),
            'heading': ('Microsoft YaHei UI', 18, 'bold'),
            'subheading': ('Microsoft YaHei UI', 14, 'bold'),
            'body': ('Microsoft YaHei UI', 12),
            'small': ('Microsoft YaHei UI', 10),
            'button': ('Microsoft YaHei UI', 12, 'bold'),
            'input': ('Microsoft YaHei UI', 11)
        }
        
        # 用户管理器
        self.user_manager = UserManager()
        
        # 登录成功回调
        self.on_login_success = on_login_success
        
        # 当前界面状态
        self.current_view = "login"  # login, register, forgot_password
          # 输入框变量
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.confirm_password_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.new_password_var = tk.StringVar()
        self.confirm_new_password_var = tk.StringVar()
        
        # 设置窗口图标
        self.set_window_icon()
        
        # 居中显示窗口
        self.center_window()
        
        # 创建界面
        self.create_modern_interface()
        
    def set_window_icon(self):
        """设置窗口图标"""
        try:
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
    
    def create_modern_interface(self):
        """创建现代化登录界面"""
        # 主容器
        main_container = tk.Frame(self.root, bg=self.colors['surface'])
        main_container.pack(fill="both", expand=True)
        
        # 左侧图片区域
        left_panel = tk.Frame(main_container, bg=self.colors['primary'], width=450)
        left_panel.pack(side="left", fill="y")
        left_panel.pack_propagate(False)
        
        # 右侧登录区域
        right_panel = tk.Frame(main_container, bg=self.colors['surface'], width=450)
        right_panel.pack(side="right", fill="both", expand=True)
        right_panel.pack_propagate(False)
        
        self.create_left_panel(left_panel)
        self.create_right_panel(right_panel)
    
    def create_left_panel(self, parent):
        """创建左侧面板"""
        # 简单的渐变背景
        canvas = tk.Canvas(parent, bg=self.colors['primary'], highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        
        # 渐变效果
        def create_gradient():
            width = canvas.winfo_width()
            height = canvas.winfo_height()
            if width > 1 and height > 1:
                for i in range(height):
                    alpha = i / height
                    r = int(255 * (1 - alpha * 0.3))
                    g = int(107 * (1 - alpha * 0.2))
                    b = int(53 * (1 - alpha * 0.1))
                    color = f"#{r:02x}{g:02x}{b:02x}"
                    canvas.create_line(0, i, width, i, fill=color, width=1)
        
        canvas.bind('<Configure>', lambda e: create_gradient())
        
        # 内容容器
        content_frame = tk.Frame(canvas, bg=self.colors['primary'])
        canvas.create_window(225, 300, window=content_frame, anchor="center")
        
        # 主图标
        icon_frame = tk.Frame(content_frame, bg=self.colors['primary'])
        icon_frame.pack(pady=(0, 20))
        
        # 大图标
        main_icon = tk.Label(icon_frame, text="🍽️", font=('Segoe UI Emoji', 64), 
                            bg=self.colors['primary'], fg="white")
        main_icon.pack()
          # 标题
        title_label = tk.Label(content_frame, text="智慧餐饮", font=self.fonts['title'], 
                              bg=self.colors['primary'], fg="white")
        title_label.pack(pady=(0, 8))
        
        # 副标题
        subtitle_label = tk.Label(content_frame, text="现代化管理系统", font=self.fonts['heading'], 
                                 bg=self.colors['primary'], fg="white")
        subtitle_label.pack(pady=(0, 30))
        
        # 特性列表
        features = [
            "🚀 高效的订单管理",
            "📊 智能数据分析", 
            "💰 精准财务控制",
            "👥 便捷客户管理"
        ]
        
        for feature in features:
            feature_label = tk.Label(content_frame, text=feature, font=self.fonts['body'], 
                                   bg=self.colors['primary'], fg="white", anchor="w")
            feature_label.pack(pady=8, padx=40, fill="x")
    
    def create_right_panel(self, parent):
        """创建右侧登录面板"""
        # 内容容器 - 增加高度以确保所有内容可见
        self.login_container = tk.Frame(parent, bg=self.colors['surface'])
        self.login_container.place(relx=0.5, rely=0.5, anchor="center", width=380, height=550)
        
        self.create_login_form()
    
    def create_login_form(self):
        """创建登录表单"""
        # 清空容器
        for widget in self.login_container.winfo_children():
            widget.destroy()
        
        # 欢迎标题
        welcome_label = tk.Label(self.login_container, text="欢迎回来", font=self.fonts['heading'], 
                                bg=self.colors['surface'], fg=self.colors['text_primary'])
        welcome_label.pack(pady=(0, 8))
        
        # 副标题
        subtitle_label = tk.Label(self.login_container, text="请登录您的账户", font=self.fonts['body'], 
                                 bg=self.colors['surface'], fg=self.colors['text_secondary'])
        subtitle_label.pack(pady=(0, 20))
        
        # 用户名输入
        self.username_entry = self.create_input_field(self.login_container, "用户名", self.username_var, "👤")
        
        # 密码输入
        self.password_entry = self.create_password_field(self.login_container, "密码", self.password_var)
        
        # 记住登录和忘记密码选项
        options_frame = tk.Frame(self.login_container, bg=self.colors['surface'])
        options_frame.pack(fill="x", pady=(0, 20))
        
        self.remember_var = tk.BooleanVar()
        remember_check = tk.Checkbutton(options_frame, text="记住登录", variable=self.remember_var,
                                       font=self.fonts['small'], bg=self.colors['surface'],
                                       fg=self.colors['text_secondary'], relief="flat")
        remember_check.pack(side="left")
        
        # 忘记密码链接
        forgot_link = tk.Label(options_frame, text="忘记密码?", font=self.fonts['small'],
                              bg=self.colors['surface'], fg=self.colors['primary'],
                              cursor="hand2")
        forgot_link.pack(side="right")
        forgot_link.bind("<Button-1>", lambda e: self.show_forgot_password())        
        # 登录按钮
        login_btn = self.create_modern_button(self.login_container, "登 录", self.handle_login, "primary", "normal")
        
        # 分割线
        divider_frame = tk.Frame(self.login_container, bg=self.colors['surface'], height=15)
        divider_frame.pack(fill="x", pady=12)
        divider_frame.pack_propagate(False)
        
        divider_line = tk.Frame(divider_frame, bg=self.colors['border'], height=1)
        divider_line.place(relx=0, rely=0.5, relwidth=0.35)
        
        divider_text = tk.Label(divider_frame, text="其他选项", font=self.fonts['small'],
                               bg=self.colors['surface'], fg=self.colors['text_secondary'])
        divider_text.place(relx=0.5, rely=0.5, anchor="center")
        
        divider_line2 = tk.Frame(divider_frame, bg=self.colors['border'], height=1)
        divider_line2.place(relx=0.65, rely=0.5, relwidth=0.35)
          # 并列按钮容器
        buttons_frame = tk.Frame(self.login_container, bg=self.colors['surface'])
        buttons_frame.pack(fill="x", pady=(5, 15))
        
        # 游客登录按钮 - 左侧
        guest_btn_frame = tk.Frame(buttons_frame, bg=self.colors['surface'])
        guest_btn_frame.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.create_modern_button(guest_btn_frame, "游客体验", self.guest_login, "secondary", "small")
        
        # 注册按钮 - 右侧
        register_btn_frame = tk.Frame(buttons_frame, bg=self.colors['surface'])
        register_btn_frame.pack(side="right", fill="x", expand=True, padx=(5, 0))
        self.create_modern_button(register_btn_frame, "注册账户", self.show_register, "tertiary", "small")
        
        # 绑定回车键
        self.root.bind('<Return>', lambda e: self.handle_login())
    
    def create_input_field(self, parent, label_text, variable, icon=""):
        """创建现代化输入框"""
        # 输入组容器
        input_group = tk.Frame(parent, bg=self.colors['surface'])
        input_group.pack(fill="x", pady=(0, 20))
        
        # 标签
        label = tk.Label(input_group, text=label_text, font=self.fonts['body'], 
                        bg=self.colors['surface'], fg=self.colors['text_primary'])
        label.pack(anchor="w", pady=(0, 5))
        
        # 输入框容器
        input_container = tk.Frame(input_group, bg=self.colors['input_bg'], 
                                  relief="solid", bd=1, highlightthickness=0)
        input_container.pack(fill="x", ipady=8)
        
        # 图标
        if icon:
            icon_label = tk.Label(input_container, text=icon, font=('Segoe UI Emoji', 14), 
                                bg=self.colors['input_bg'], fg=self.colors['text_secondary'])
            icon_label.pack(side="left", padx=(15, 5))
        
        # 输入框
        entry = tk.Entry(input_container, textvariable=variable, font=self.fonts['input'],
                        bg=self.colors['input_bg'], fg=self.colors['text_primary'],
                        relief="flat", bd=0, highlightthickness=0)
        entry.pack(side="left", fill="x", expand=True, padx=(0, 15))
        
        # 焦点事件
        def on_focus_in(event):
            input_container.configure(bg=self.colors['input_focus'], highlightbackground=self.colors['primary'])
            if icon:
                icon_label.configure(bg=self.colors['input_focus'])
            entry.configure(bg=self.colors['input_focus'])
            
        def on_focus_out(event):
            input_container.configure(bg=self.colors['input_bg'], highlightbackground=self.colors['border'])
            if icon:
                icon_label.configure(bg=self.colors['input_bg'])
            entry.configure(bg=self.colors['input_bg'])
        
        entry.bind('<FocusIn>', on_focus_in)
        entry.bind('<FocusOut>', on_focus_out)
        
        return entry

    def create_password_field(self, parent, label_text, variable):
        """创建密码输入框"""
        # 输入组容器
        input_group = tk.Frame(parent, bg=self.colors['surface'])
        input_group.pack(fill="x", pady=(0, 20))
        
        # 标签
        label = tk.Label(input_group, text=label_text, font=self.fonts['body'], 
                        bg=self.colors['surface'], fg=self.colors['text_primary'])
        label.pack(anchor="w", pady=(0, 5))
        
        # 输入框容器
        input_container = tk.Frame(input_group, bg=self.colors['input_bg'], 
                                  relief="solid", bd=1, highlightthickness=0)
        input_container.pack(fill="x", ipady=8)
        
        # 图标
        icon_label = tk.Label(input_container, text="🔒", font=('Segoe UI Emoji', 14), 
                            bg=self.colors['input_bg'], fg=self.colors['text_secondary'])
        icon_label.pack(side="left", padx=(15, 5))
        
        # 密码输入框
        entry = tk.Entry(input_container, textvariable=variable, font=self.fonts['input'],
                        bg=self.colors['input_bg'], fg=self.colors['text_primary'],
                        relief="flat", bd=0, highlightthickness=0, show="*")
        entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        # 显示/隐藏按钮
        show_password = tk.BooleanVar()
        def toggle_password():
            if show_password.get():
                entry.configure(show="")
                toggle_btn.configure(text="🙈")
            else:
                entry.configure(show="*")
                toggle_btn.configure(text="👁️")
            show_password.set(not show_password.get())
        
        toggle_btn = tk.Button(input_container, text="👁️", font=('Segoe UI Emoji', 12),
                              bg=self.colors['input_bg'], fg=self.colors['text_secondary'],
                              relief="flat", bd=0, cursor="hand2", 
                              command=toggle_password, width=2)
        toggle_btn.pack(side="right", padx=(0, 10))
        
        # 焦点事件
        def on_focus_in(event):
            input_container.configure(bg=self.colors['input_focus'])
            icon_label.configure(bg=self.colors['input_focus'])
            entry.configure(bg=self.colors['input_focus'])
            toggle_btn.configure(bg=self.colors['input_focus'])
            
        def on_focus_out(event):
            input_container.configure(bg=self.colors['input_bg'])
            icon_label.configure(bg=self.colors['input_bg'])
            entry.configure(bg=self.colors['input_bg'])
            toggle_btn.configure(bg=self.colors['input_bg'])
        
        entry.bind('<FocusIn>', on_focus_in)
        entry.bind('<FocusOut>', on_focus_out)
        
        return entry
    
    def create_modern_button(self, parent, text, command, style="primary", size="normal"):
        """创建现代化按钮"""
        if style == "primary":
            bg_color = self.colors['primary']
            hover_color = self.colors['hover']
            text_color = "white"
        elif style == "secondary":
            bg_color = self.colors['input_bg']
            hover_color = self.colors['border']
            text_color = self.colors['text_primary']
        elif style == "tertiary":
            bg_color = self.colors['secondary']
            hover_color = self.colors['accent']
            text_color = "white"
        else:
            bg_color = self.colors['input_bg']
            hover_color = self.colors['border']
            text_color = self.colors['text_primary']
        
        # 根据按钮大小设置不同的样式
        if size == "large":
            # 大按钮 - 用于主要操作（登录按钮）
            button_frame = tk.Frame(parent, bg=bg_color, cursor="hand2", height=45)
            button_frame.pack(fill="x", pady=8)
            button_frame.pack_propagate(False)
            button_label = tk.Label(button_frame, text=text, font=self.fonts['button'],
                                   bg=bg_color, fg=text_color)
            button_label.place(relx=0.5, rely=0.5, anchor="center")
        elif size == "small":
            # 小按钮 - 用于次要操作（游客、注册按钮）
            button_frame = tk.Frame(parent, bg=bg_color, cursor="hand2", height=35)
            button_frame.pack(fill="x", pady=3)
            button_frame.pack_propagate(False)
            button_label = tk.Label(button_frame, text=text, font=('Microsoft YaHei UI', 10, 'bold'),
                                   bg=bg_color, fg=text_color)
            button_label.place(relx=0.5, rely=0.5, anchor="center")
        else:
            # 正常按钮
            button_frame = tk.Frame(parent, bg=bg_color, cursor="hand2", height=40)
            button_frame.pack(fill="x", pady=5)
            button_frame.pack_propagate(False)
            button_label = tk.Label(button_frame, text=text, font=self.fonts['button'],
                                   bg=bg_color, fg=text_color)
            button_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # 悬停效果
        def on_enter(event):
            button_frame.configure(bg=hover_color)
            button_label.configure(bg=hover_color)
            
        def on_leave(event):
            button_frame.configure(bg=bg_color)
            button_label.configure(bg=bg_color)
            
        def on_click(event):
            command()
        
        button_frame.bind("<Enter>", on_enter)
        button_frame.bind("<Leave>", on_leave)
        button_frame.bind("<Button-1>", on_click)
        button_label.bind("<Enter>", on_enter)
        button_label.bind("<Leave>", on_leave)
        button_label.bind("<Button-1>", on_click)
        
        return button_frame
    
    def handle_login(self):
        """处理登录"""
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()
        
        if not username or not password:
            messagebox.showerror("错误", "请输入用户名和密码")
            return
        
        # 验证用户
        user = self.user_manager.validate_user(username, password)
        if user:
            messagebox.showinfo("成功", f"欢迎 {user.name}！")
            
            # 准备用户信息字典
            user_info = {
                'username': user.username,
                'name': user.name,
                'role': user.role,
                'email': getattr(user, 'email', ''),
                'phone': getattr(user, 'phone', ''),
                'login_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # 调用登录成功回调
            if self.on_login_success:                self.on_login_success(user_info)
            else:
                # 如果没有回调，直接关闭登录窗口
                self.root.destroy()
        else:
            messagebox.showerror("错误", "用户名或密码错误")
            self.password_var.set("")
    
    def show_register(self):
        """显示注册表单"""
        self.current_view = "register"
        self.create_register_form()
    
    def show_forgot_password(self):
        """显示忘记密码表单"""
        self.current_view = "forgot_password"
        self.create_forgot_password_form()
    
    def create_register_form(self):
        """创建注册表单"""
        # 清空容器
        for widget in self.login_container.winfo_children():
            widget.destroy()
        
        # 标题
        title_label = tk.Label(self.login_container, text="创建账户", font=self.fonts['heading'], 
                              bg=self.colors['surface'], fg=self.colors['text_primary'])
        title_label.pack(pady=(0, 10))
        
        # 副标题
        subtitle_label = tk.Label(self.login_container, text="请填写注册信息", font=self.fonts['body'], 
                                 bg=self.colors['surface'], fg=self.colors['text_secondary'])
        subtitle_label.pack(pady=(0, 20))
        
        # 输入字段
        self.create_input_field(self.login_container, "用户名", self.username_var, "👤")
        self.create_input_field(self.login_container, "邮箱", self.email_var, "📧")
        self.create_password_field(self.login_container, "密码", self.password_var)
        self.create_password_field(self.login_container, "确认密码", self.confirm_password_var)
        
        # 并列按钮容器
        buttons_frame = tk.Frame(self.login_container, bg=self.colors['surface'])
        buttons_frame.pack(fill="x", pady=(20, 15))
        
        # 返回按钮 - 左侧
        back_btn_frame = tk.Frame(buttons_frame, bg=self.colors['surface'])
        back_btn_frame.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.create_modern_button(back_btn_frame, "返回登录", self.show_login, "secondary", "large")
        
        # 注册按钮 - 右侧
        register_btn_frame = tk.Frame(buttons_frame, bg=self.colors['surface'])
        register_btn_frame.pack(side="right", fill="x", expand=True, padx=(10, 0))
        self.create_modern_button(register_btn_frame, "创建账户", self.handle_register, "primary", "large")
          # 提示文字
        tip_label = tk.Label(self.login_container, text="注册即表示您同意我们的服务条款",
                           font=self.fonts['small'], bg=self.colors['surface'], 
                           fg=self.colors['text_secondary'])
        tip_label.pack(pady=(10, 0))
    
    def create_forgot_password_form(self):
        """创建忘记密码表单"""
        # 清空容器
        for widget in self.login_container.winfo_children():
            widget.destroy()
        
        # 标题
        title_label = tk.Label(self.login_container, text="重置密码", font=self.fonts['heading'], 
                              bg=self.colors['surface'], fg=self.colors['text_primary'])
        title_label.pack(pady=(0, 10))
        
        # 副标题
        subtitle_label = tk.Label(self.login_container, text="请输入邮箱和新密码", font=self.fonts['body'], 
                                 bg=self.colors['surface'], fg=self.colors['text_secondary'])
        subtitle_label.pack(pady=(0, 20))
        
        # 邮箱输入
        self.create_input_field(self.login_container, "邮箱地址", self.email_var, "📧")
        
        # 新密码输入
        self.create_password_field(self.login_container, "新密码", self.new_password_var)
        
        # 确认新密码输入
        self.create_password_field(self.login_container, "确认新密码", self.confirm_new_password_var)
        
        # 并列按钮容器
        buttons_frame = tk.Frame(self.login_container, bg=self.colors['surface'])
        buttons_frame.pack(fill="x", pady=(20, 15))
        
        # 返回按钮 - 左侧
        back_btn_frame = tk.Frame(buttons_frame, bg=self.colors['surface'])
        back_btn_frame.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.create_modern_button(back_btn_frame, "返回登录", self.show_login, "secondary", "large")
          # 重置按钮 - 右侧
        reset_btn_frame = tk.Frame(buttons_frame, bg=self.colors['surface'])
        reset_btn_frame.pack(side="right", fill="x", expand=True, padx=(10, 0))
        self.create_modern_button(reset_btn_frame, "重置密码", self.handle_forgot_password, "primary", "large")
        
        # 提示文字
        tip_label = tk.Label(self.login_container, text="请确认邮箱地址正确，密码将直接重置",
                           font=self.fonts['small'], bg=self.colors['surface'], 
                           fg=self.colors['text_secondary'])
        tip_label.pack(pady=(10, 0))
    
    def show_login(self):
        """显示登录表单"""
        self.current_view = "login"
        self.create_login_form()
    
    def handle_register(self):
        """处理注册"""
        username = self.username_var.get().strip()
        email = self.email_var.get().strip()
        password = self.password_var.get().strip()
        confirm_password = self.confirm_password_var.get().strip()
        
        if not all([username, email, password, confirm_password]):
            messagebox.showerror("错误", "请填写所有字段")
            return
        
        if password != confirm_password:
            messagebox.showerror("错误", "密码不匹配")
            return
        
        if len(password) < 6:
            messagebox.showerror("错误", "密码至少需要6个字符")
            return
        
        # 检查用户是否已存在
        if self.user_manager.user_exists(username):
            messagebox.showerror("错误", "用户名已存在")
            return
        
        # 注册用户
        success, message = self.user_manager.register_user(username, email, password)
        if success:
            messagebox.showinfo("成功", "注册成功！请登录")
            self.show_login()
        else:
            messagebox.showerror("错误", message)
    
    def handle_forgot_password(self):
        """处理忘记密码 - 直接重置密码"""
        email = self.email_var.get().strip()
        new_password = self.new_password_var.get().strip()
        confirm_new_password = self.confirm_new_password_var.get().strip()
        
        # 验证输入
        if not email:
            messagebox.showerror("错误", "请输入邮箱地址")
            return
        
        if not new_password:
            messagebox.showerror("错误", "请输入新密码")
            return
        
        if not confirm_new_password:
            messagebox.showerror("错误", "请确认新密码")
            return
        
        if new_password != confirm_new_password:
            messagebox.showerror("错误", "两次输入的密码不一致")
            return
        
        if len(new_password) < 6:
            messagebox.showerror("错误", "密码长度至少6位")
            return
        
        # 验证邮箱格式
        import re
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            messagebox.showerror("错误", "邮箱格式不正确")
            return
        
        # 检查邮箱是否存在
        if not self.user_manager.email_exists(email):
            messagebox.showerror("错误", "该邮箱未注册")
            return
        
        # 重置密码
        if self.user_manager.reset_password_by_email(email, new_password):
            messagebox.showinfo("成功", "密码重置成功！请使用新密码登录")
            # 清空输入框
            self.email_var.set("")
            self.new_password_var.set("")
            self.confirm_new_password_var.set("")
            # 返回登录界面
            self.show_login()
        else:
            messagebox.showerror("错误", "密码重置失败，请稍后再试")
    
    def guest_login(self):
        """游客登录"""
        guest_info = {
            'username': 'guest',
            'name': '游客用户',
            'role': '游客',
            'email': '',
            'phone': '',
            'login_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # 调用登录成功回调
        if self.on_login_success:
            self.on_login_success(guest_info)
        else:
            # 如果没有回调，直接关闭登录窗口
            self.root.destroy()
    
    def run(self):
        """运行登录界面"""
        self.root.mainloop()

# 主程序入口
def main():
    def on_login_success(user):
        print(f"登录成功: {user['name']}")
        # 启动主系统
        try:
            # 尝试相对导入
            try:
                from ..core.modern_ui_system import ModernFoodServiceSystem
            except ImportError:
                # 尝试绝对导入
                import sys
                import os
                current_dir = os.path.dirname(os.path.abspath(__file__))
                core_dir = os.path.join(os.path.dirname(current_dir), 'core')
                sys.path.insert(0, core_dir)
                from modern_ui_system import ModernFoodServiceSystem
            
            # 创建并运行主系统
            app = ModernFoodServiceSystem()
            app.run()
        except ImportError as e:
            print(f"主系统模块导入失败: {e}")
            messagebox.showerror("错误", f"无法启动主系统: {e}")
        except Exception as e:
            print(f"启动主系统失败: {e}")
            messagebox.showerror("错误", f"启动主系统失败: {e}")
    
    login_app = ModernLoginModule(on_login_success)
    login_app.run()

if __name__ == "__main__":
    main()
