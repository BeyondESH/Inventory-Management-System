#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Modern Login Module - Provides beautiful user login interface
"""

import tkinter as tk
from tkinter import ttk, messagebox
import os
import math
import datetime
# PIL is an optional dependency, skip if not installed
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("⚠️ PIL library not installed, will use basic interface (does not affect functionality)")

try:
    from ..core.user_manager import UserManager, User
except ImportError:
    import sys
    import os
    # Add core directory to path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    core_dir = os.path.join(os.path.dirname(current_dir), 'core')
    sys.path.insert(0, core_dir)
    from user_manager import UserManager, User

class ModernLoginModule:
    def __init__(self, on_login_success=None):
        self.root = tk.Tk()
        self.root.title("Smart Restaurant Management System")
        self.root.geometry("900x600") 
        self.root.configure(bg="#ffffff")
        self.root.resizable(False, False)
        
        # Modern color theme
        self.colors = {
            'primary': '#FF6B35',      # Primary
            'secondary': '#F7931E',    # Secondary
            'accent': '#FFD23F',       # Accent
            'background': '#F8F9FA',   # Background
            'surface': '#FFFFFF',      # Card background
            'text_primary': '#2D3436', # Main text
            'text_secondary': '#636E72', # Secondary text
            'border': '#E0E0E0',       # Border
            'hover': '#E17055',        # Hover
            'success': '#00B894',      # Success
            'error': '#E84393',        # Error
            'input_bg': '#F8F9FA',     # Input background
            'input_focus': '#E8F4FD'   # Input focus
        }
        
        # Font configuration
        self.fonts = {
            'title': ('Segoe UI', 28, 'bold'),
            'heading': ('Segoe UI', 18, 'bold'),
            'subheading': ('Segoe UI', 14, 'bold'),
            'body': ('Segoe UI', 12),
            'small': ('Segoe UI', 10),
            'button': ('Segoe UI', 12, 'bold'),
            'input': ('Segoe UI', 11)
        }
        
        # User manager
        self.user_manager = UserManager()
        
        # Login success callback
        self.on_login_success = on_login_success
        
        # Current interface state
        self.current_view = "login"  # login, register, forgot_password
        # Input field variables
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.confirm_password_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.new_password_var = tk.StringVar()
        self.confirm_new_password_var = tk.StringVar()
        
        # Set window icon
        self.set_window_icon()
        
        # Center window
        self.center_window()
        
        # Create interface
        self.create_modern_interface()
        
    def set_window_icon(self):
        """Set window icon"""
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(current_dir)
            icon_path = os.path.join(project_root, "image", "icon", "main.ico")
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except:
            pass
    
    def center_window(self):
        """Center window display"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_modern_interface(self):
        """Create modern login interface"""
        # Main container
        main_container = tk.Frame(self.root, bg=self.colors['surface'])
        main_container.pack(fill="both", expand=True)
        
        # Left image area
        left_panel = tk.Frame(main_container, bg=self.colors['primary'], width=450)
        left_panel.pack(side="left", fill="y")
        left_panel.pack_propagate(False)
        
        # Right login area
        right_panel = tk.Frame(main_container, bg=self.colors['surface'], width=450)
        right_panel.pack(side="right", fill="both", expand=True)
        right_panel.pack_propagate(False)
        
        self.create_left_panel(left_panel)
        self.create_right_panel(right_panel)
    
    def create_left_panel(self, parent):
        """Create left panel"""
        # Simple gradient background
        canvas = tk.Canvas(parent, bg=self.colors['primary'], highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        
        # Gradient effect
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
        
        # Content container
        content_frame = tk.Frame(canvas, bg=self.colors['primary'])
        canvas.create_window(225, 300, window=content_frame, anchor="center")
        
        # Main icon
        icon_frame = tk.Frame(content_frame, bg=self.colors['primary'])
        icon_frame.pack(pady=(0, 20))
        
        # Large icon
        main_icon = tk.Label(icon_frame, text="🍽️", font=('Segoe UI Emoji', 64), 
                            bg=self.colors['primary'], fg="white")
        main_icon.pack()
        # Title
        title_label = tk.Label(content_frame, text="Smart Restaurant", font=self.fonts['title'], 
                              bg=self.colors['primary'], fg="white")
        title_label.pack(pady=(0, 8))
        
        # Subtitle
        subtitle_label = tk.Label(content_frame, text="Modern Management System", font=self.fonts['heading'], 
                                 bg=self.colors['primary'], fg="white")
        subtitle_label.pack(pady=(0, 30))
        
        # Feature list
        features = [
            "🚀 Efficient Order Management",
            "📊 Smart Data Analysis", 
            "💰 Precise Financial Control",
            "👥 Convenient Customer Management"
        ]
        
        for feature in features:
            feature_label = tk.Label(content_frame, text=feature, font=self.fonts['body'], 
                                   bg=self.colors['primary'], fg="white", anchor="w")
            feature_label.pack(pady=8, padx=40, fill="x")
    
    def create_right_panel(self, parent):
        """Create right login panel"""
        # Content container - increase height to ensure all content is visible
        self.login_container = tk.Frame(parent, bg=self.colors['surface'])
        self.login_container.place(relx=0.5, rely=0.5, anchor="center", width=380, height=580)
        
        self.create_login_form()
    
    def create_login_form(self):
        """Create login form"""
        # Clear container
        for widget in self.login_container.winfo_children():
            widget.destroy()
        
        # Welcome title
        welcome_label = tk.Label(self.login_container, text="Welcome back", font=self.fonts['heading'], 
                                bg=self.colors['surface'], fg=self.colors['text_primary'])
        welcome_label.pack(pady=(0, 8))
        
        # Subtitle
        subtitle_label = tk.Label(self.login_container, text="Please login to your account", font=self.fonts['body'], 
                                 bg=self.colors['surface'], fg=self.colors['text_secondary'])
        subtitle_label.pack(pady=(0, 20))
        
        # Username input
        self.username_entry = self.create_input_field(self.login_container, "Username", self.username_var, "👤")
        
        # Password input
        self.password_entry = self.create_password_field(self.login_container, "Password", self.password_var)
        
        # Remember login and forgot password options
        options_frame = tk.Frame(self.login_container, bg=self.colors['surface'])
        options_frame.pack(fill="x", pady=(0, 20))
        
        self.remember_var = tk.BooleanVar()
        remember_check = tk.Checkbutton(options_frame, text="Remember login", variable=self.remember_var,
                                       font=self.fonts['small'], bg=self.colors['surface'],
                                       fg=self.colors['text_secondary'], relief="flat")
        remember_check.pack(side="left")
        
        # Forgot password link
        forgot_link = tk.Label(options_frame, text="Forgot password?", font=self.fonts['small'],
                              bg=self.colors['surface'], fg=self.colors['primary'],
                              cursor="hand2")
        forgot_link.pack(side="right")
        forgot_link.bind("<Button-1>", lambda e: self.show_forgot_password())        
        # Login button
        login_btn = self.create_modern_button(self.login_container, "Login", self.handle_login, "primary", "normal")
        
        # Divider
        divider_frame = tk.Frame(self.login_container, bg=self.colors['surface'], height=15)
        divider_frame.pack(fill="x", pady=12)
        divider_frame.pack_propagate(False)
        
        divider_line = tk.Frame(divider_frame, bg=self.colors['border'], height=1)
        divider_line.place(relx=0, rely=0.5, relwidth=0.35)
        
        divider_text = tk.Label(divider_frame, text="Other options", font=self.fonts['small'],
                               bg=self.colors['surface'], fg=self.colors['text_secondary'])
        divider_text.place(relx=0.5, rely=0.5, anchor="center")
        
        divider_line2 = tk.Frame(divider_frame, bg=self.colors['border'], height=1)
        divider_line2.place(relx=0.65, rely=0.5, relwidth=0.35)
        # Parallel button container
        buttons_frame = tk.Frame(self.login_container, bg=self.colors['surface'])
        buttons_frame.pack(fill="x", pady=(5, 15))
        
        # Guest login button - left
        guest_btn_frame = tk.Frame(buttons_frame, bg=self.colors['surface'])
        guest_btn_frame.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.create_modern_button(guest_btn_frame, "Guest experience", self.guest_login, "secondary", "small")
        
        # Register button - right
        register_btn_frame = tk.Frame(buttons_frame, bg=self.colors['surface'])
        register_btn_frame.pack(side="right", fill="x", expand=True, padx=(5, 0))
        self.create_modern_button(register_btn_frame, "Register account", self.show_register, "tertiary", "small")
        
        # Bind enter key
        self.root.bind('<Return>', lambda e: self.handle_login())
    
    def create_input_field(self, parent, label_text, variable, icon=""):
        """Create modern input field"""
        # Input group container
        input_group = tk.Frame(parent, bg=self.colors['surface'])
        input_group.pack(fill="x", pady=(0, 20))
        
        # Label
        label = tk.Label(input_group, text=label_text, font=self.fonts['body'], 
                        bg=self.colors['surface'], fg=self.colors['text_primary'])
        label.pack(anchor="w", pady=(0, 5))
        
        # Input field container
        input_container = tk.Frame(input_group, bg=self.colors['input_bg'], 
                                  relief="solid", bd=1, highlightthickness=0)
        input_container.pack(fill="x", ipady=8)
        
        # Icon
        if icon:
            icon_label = tk.Label(input_container, text=icon, font=('Segoe UI Emoji', 14), 
                                bg=self.colors['input_bg'], fg=self.colors['text_secondary'])
            icon_label.pack(side="left", padx=(15, 5))
        
        # Input field
        entry = tk.Entry(input_container, textvariable=variable, font=self.fonts['input'],
                        bg=self.colors['input_bg'], fg=self.colors['text_primary'],
                        relief="flat", bd=0, highlightthickness=0)
        entry.pack(side="left", fill="x", expand=True, padx=(0, 15))
        
        # Focus event
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
        """Create password input field"""
        # Input group container
        input_group = tk.Frame(parent, bg=self.colors['surface'])
        input_group.pack(fill="x", pady=(0, 20))
        
        # Label
        label = tk.Label(input_group, text=label_text, font=self.fonts['body'], 
                        bg=self.colors['surface'], fg=self.colors['text_primary'])
        label.pack(anchor="w", pady=(0, 5))
        
        # Input field container
        input_container = tk.Frame(input_group, bg=self.colors['input_bg'], 
                                  relief="solid", bd=1, highlightthickness=0)
        input_container.pack(fill="x", ipady=8)
        
        # Icon
        icon_label = tk.Label(input_container, text="🔒", font=('Segoe UI Emoji', 14), 
                            bg=self.colors['input_bg'], fg=self.colors['text_secondary'])
        icon_label.pack(side="left", padx=(15, 5))
        
        # Password input field
        entry = tk.Entry(input_container, textvariable=variable, font=self.fonts['input'],
                        bg=self.colors['input_bg'], fg=self.colors['text_primary'],
                        relief="flat", bd=0, highlightthickness=0, show="*")
        entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        # Show/hide button
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
        
        # Focus event
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
        """Create modern button"""
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
        
        # According to button size, set different styles
        if size == "large":
            # Large button - used for main operations (login button)
            button_frame = tk.Frame(parent, bg=bg_color, cursor="hand2", height=45)
            button_frame.pack(fill="x", pady=8)
            button_frame.pack_propagate(False)
            button_label = tk.Label(button_frame, text=text, font=self.fonts['button'],
                                   bg=bg_color, fg=text_color)
            button_label.place(relx=0.5, rely=0.5, anchor="center")
        elif size == "small":
            # Small button - used for secondary operations (guest, register buttons)
            button_frame = tk.Frame(parent, bg=bg_color, cursor="hand2", height=35)
            button_frame.pack(fill="x", pady=3)
            button_frame.pack_propagate(False)
            button_label = tk.Label(button_frame, text=text, font=('Segoe UI', 10, 'bold'),
                                   bg=bg_color, fg=text_color)
            button_label.place(relx=0.5, rely=0.5, anchor="center")
        else:
            # Normal button
            button_frame = tk.Frame(parent, bg=bg_color, cursor="hand2", height=40)
            button_frame.pack(fill="x", pady=5)
            button_frame.pack_propagate(False)
            button_label = tk.Label(button_frame, text=text, font=self.fonts['button'],
                                   bg=bg_color, fg=text_color)
            button_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # Hover effect
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
        """Handle login"""
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter username and password")
            return
        
        # Validate user
        user = self.user_manager.validate_user(username, password)
        if user:
            messagebox.showinfo("Success", f"Welcome {user.name}!")
            # Prepare user information dictionary
            user_info = {
                'username': user.username,
                'name': user.name,
                'role': user.role,
                'email': getattr(user, 'email', ''),
                'phone': getattr(user, 'phone', ''),
                'login_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Call login success callback
            if self.on_login_success:
                self.on_login_success(user_info, self.root)
            else:
                # If no callback, just close login window
                self.root.destroy()
        else:
            messagebox.showerror("Error", "Invalid username or password")
            self.password_var.set("")
    
    def show_register(self):
        """Show register form"""
        self.current_view = "register"
        self.create_register_form()
    
    def show_forgot_password(self):
        """Show forgot password form"""
        self.current_view = "forgot_password"
        self.create_forgot_password_form()
    
    def create_register_form(self):
        """Create register form"""
        # Clear container
        for widget in self.login_container.winfo_children():
            widget.destroy()
        
        # Fixed at bottom button container - first create, ensure displayed at bottom
        bottom_frame = tk.Frame(self.login_container, bg=self.colors['surface'], height=70)
        bottom_frame.pack(side="bottom", fill="x", pady=(10, 0))
        bottom_frame.pack_propagate(False)
        
        # Parallel button container
        buttons_frame = tk.Frame(bottom_frame, bg=self.colors['surface'])
        buttons_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Back button - left
        back_btn_frame = tk.Frame(buttons_frame, bg=self.colors['surface'])
        back_btn_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))
        self.create_modern_button(back_btn_frame, "Back to login", self.show_login, "secondary", "large")
        
        # Register button - right
        register_btn_frame = tk.Frame(buttons_frame, bg=self.colors['surface'])
        register_btn_frame.pack(side="right", fill="both", expand=True, padx=(5, 0))
        self.create_modern_button(register_btn_frame, "Create account", self.handle_register, "primary", "large")
        
        # Content area - use remaining space
        content_frame = tk.Frame(self.login_container, bg=self.colors['surface'])
        content_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        # Use Canvas to ensure content scrollable
        canvas = tk.Canvas(content_frame, bg=self.colors['surface'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(content_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['surface'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Title
        title_label = tk.Label(scrollable_frame, text="Create account", font=self.fonts['heading'], 
                              bg=self.colors['surface'], fg=self.colors['text_primary'])
        title_label.pack(pady=(0, 10))
        
        # Subtitle
        subtitle_label = tk.Label(scrollable_frame, text="Please fill in registration information", font=self.fonts['body'], 
                                 bg=self.colors['surface'], fg=self.colors['text_secondary'])
        subtitle_label.pack(pady=(0, 20))
        
        # Input fields
        self.create_input_field(scrollable_frame, "Username", self.username_var, "👤")
        self.create_input_field(scrollable_frame, "Email", self.email_var, "📧")
        self.create_password_field(scrollable_frame, "Password", self.password_var)
        self.create_password_field(scrollable_frame, "Confirm password", self.confirm_password_var)
        
        # Tip text
        tip_label = tk.Label(scrollable_frame, text="Registering means you agree to our service terms",
                           font=self.fonts['small'], bg=self.colors['surface'], 
                           fg=self.colors['text_secondary'])
        tip_label.pack(pady=(10, 20))
        # Layout Canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def create_forgot_password_form(self):
        """Create forgot password form"""
        # Clear container
        for widget in self.login_container.winfo_children():
            widget.destroy()
        
        # Fixed at bottom button container - first create, ensure displayed at bottom
        bottom_frame = tk.Frame(self.login_container, bg=self.colors['surface'], height=70)
        bottom_frame.pack(side="bottom", fill="x", pady=(10, 0))
        bottom_frame.pack_propagate(False)
        
        # Parallel button container
        buttons_frame = tk.Frame(bottom_frame, bg=self.colors['surface'])
        buttons_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Back button - left
        back_btn_frame = tk.Frame(buttons_frame, bg=self.colors['surface'])
        back_btn_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))
        self.create_modern_button(back_btn_frame, "Back to login", self.show_login, "secondary", "large")
        
        # Reset button - right
        reset_btn_frame = tk.Frame(buttons_frame, bg=self.colors['surface'])
        reset_btn_frame.pack(side="right", fill="both", expand=True, padx=(5, 0))
        self.create_modern_button(reset_btn_frame, "Reset password", self.handle_forgot_password, "primary", "large")
        
        # Content area - use remaining space
        content_frame = tk.Frame(self.login_container, bg=self.colors['surface'])
        content_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        # Use Canvas to ensure content scrollable
        canvas = tk.Canvas(content_frame, bg=self.colors['surface'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(content_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['surface'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Title
        title_label = tk.Label(scrollable_frame, text="Reset password", font=self.fonts['heading'], 
                              bg=self.colors['surface'], fg=self.colors['text_primary'])
        title_label.pack(pady=(0, 10))
        
        # Subtitle
        subtitle_label = tk.Label(scrollable_frame, text="Please enter email and new password", font=self.fonts['body'], 
                                 bg=self.colors['surface'], fg=self.colors['text_secondary'])
        subtitle_label.pack(pady=(0, 20))
        
        # Email input
        self.create_input_field(scrollable_frame, "Email address", self.email_var, "📧")
        
        # New password input
        self.create_password_field(scrollable_frame, "New password", self.new_password_var)
        
        # Confirm new password input
        self.create_password_field(scrollable_frame, "Confirm new password", self.confirm_new_password_var)
        
        # Tip text
        tip_label = tk.Label(scrollable_frame, text="Please confirm email address is correct, password will be reset directly",
                           font=self.fonts['small'], bg=self.colors['surface'], 
                           fg=self.colors['text_secondary'])
        tip_label.pack(pady=(10, 20))
        
        # Layout Canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def show_login(self):
        """Show login form"""
        self.current_view = "login"
        self.create_login_form()
    
    def handle_register(self):
        """Handle register"""
        username = self.username_var.get().strip()
        email = self.email_var.get().strip()
        password = self.password_var.get().strip()
        confirm_password = self.confirm_password_var.get().strip()
        
        if not all([username, email, password, confirm_password]):
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return
        
        if len(password) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters long")
            return
        
        # Check if user already exists
        if self.user_manager.user_exists(username):
            messagebox.showerror("Error", "Username already exists")
            return
        
        # Register user
        success, message = self.user_manager.register_user(username, email, password)
        if success:
            messagebox.showinfo("Success", "Registration successful! Please login")
            self.show_login()
        else:
            messagebox.showerror("Error", message)
    
    def handle_forgot_password(self):
        """Handle forgot password - directly reset password"""
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
            self.on_login_success(guest_info, self.root)
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
