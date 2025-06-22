#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
支付界面UI测试脚本
"""

import tkinter as tk
from tkinter import ttk

class PaymentUITest:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("支付界面UI测试")
        self.root.geometry("600x400")
        self.root.configure(bg="#F8F9FA")
        
        # 现代化颜色方案
        self.colors = {
            'primary': '#FF6B35',
            'background': '#F8F9FA',
            'surface': '#FFFFFF',
            'text_primary': '#2D3436',
            'white': '#FFFFFF'
        }
        
        self.fonts = {
            'title': ('Segoe UI', 16, 'bold'),
            'heading': ('Segoe UI', 14, 'bold'),
            'body': ('Segoe UI', 12)
        }
        
        self.create_payment_test()
    
    def create_payment_test(self):
        """创建支付测试界面"""
        # 标题
        title_frame = tk.Frame(self.root, bg=self.colors['primary'], height=60)
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text="支付界面UI测试",
                              font=self.fonts['title'],
                              bg=self.colors['primary'], fg=self.colors['white'])
        title_label.pack(pady=15)
        
        # 主内容
        main_frame = tk.Frame(self.root, bg=self.colors['background'], padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)
        
        # 左侧：订单详情
        left_frame = tk.Frame(main_frame, bg=self.colors['surface'], padx=15, pady=15)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        tk.Label(left_frame, text="订单详情", font=self.fonts['heading'],
                 bg=self.colors['surface'], fg=self.colors['text_primary']).pack(anchor="w", pady=(0, 10))
        
        # 示例订单项目
        order_items = [
            {"name": "牛肉汉堡", "quantity": 1, "price": 32.0},
            {"name": "薯条", "quantity": 2, "price": 12.0},
            {"name": "可乐", "quantity": 1, "price": 8.0}
        ]
        
        for item in order_items:
            item_row = tk.Frame(left_frame, bg=self.colors['surface'])
            item_row.pack(fill="x", pady=2)
            tk.Label(item_row, text=f"{item['name']} x{item['quantity']}",
                     bg=self.colors['surface'], font=self.fonts['body']).pack(side="left")
            tk.Label(item_row, text=f"¥{item['price'] * item['quantity']:.2f}",
                     bg=self.colors['surface'], font=self.fonts['body']).pack(side="right")
        
        ttk.Separator(left_frame, orient='horizontal').pack(fill='x', pady=10)
        
        # 右侧：支付方式
        right_frame = tk.Frame(main_frame, bg=self.colors['surface'], padx=15, pady=15)
        right_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        tk.Label(right_frame, text="支付方式", font=self.fonts['heading'],
                 bg=self.colors['surface'], fg=self.colors['text_primary']).pack(anchor="w", pady=(0, 10))
        
        # 支付按钮
        payment_methods = [
            ("信用卡", "💳", "#3498DB"),
            ("支付宝", "💰", "#1677FF"),  
            ("微信支付", "💬", "#07C160"),
            ("现金", "💵", "#F39C12")
        ]
        
        for method, icon, color in payment_methods:
            btn_frame = tk.Frame(right_frame, bg=self.colors['surface'])
            btn_frame.pack(fill="x", pady=5)
            
            btn = tk.Button(btn_frame, 
                           text=f"{icon}  {method}",
                           font=('Segoe UI', 12, 'bold'),
                           bg=color, 
                           fg="white",
                           activebackground=color,
                           activeforeground="white",
                           bd=0, 
                           relief="flat",
                           cursor="hand2", 
                           width=18,
                           height=2,
                           command=lambda m=method: self.test_payment(m))
            btn.pack(fill="x", ipady=8)
        
        # 底部：总金额
        bottom_frame = tk.Frame(self.root, bg=self.colors['background'], padx=20, pady=10)
        bottom_frame.pack(fill="x", side="bottom")
        
        total_amount = sum(item['price'] * item['quantity'] for item in order_items)
        total_label = tk.Label(bottom_frame, text=f"总计: ¥ {total_amount:.2f}",
                              font=self.fonts['title'],
                              bg=self.colors['background'], fg=self.colors['primary'])
        total_label.pack(side="left")
        
        close_btn = tk.Button(bottom_frame, text="关闭测试",
                             font=self.fonts['body'],
                             bg="#636E72", fg=self.colors['white'],
                             bd=0, cursor="hand2", command=self.root.destroy)
        close_btn.pack(side="right", padx=10, ipady=8)
    
    def test_payment(self, method):
        """测试支付方法"""
        print(f"测试支付方法: {method}")
        
        # 创建处理对话框
        processing_dialog = tk.Toplevel(self.root)
        processing_dialog.title("处理支付")
        processing_dialog.geometry("300x200")
        processing_dialog.transient(self.root)
        processing_dialog.grab_set()
        
        # 居中对话框
        processing_dialog.update_idletasks()
        x = (processing_dialog.winfo_screenwidth() // 2) - (300 // 2)
        y = (processing_dialog.winfo_screenheight() // 2) - (200 // 2)
        processing_dialog.geometry(f"300x200+{x}+{y}")
        
        # 处理内容
        processing_frame = tk.Frame(processing_dialog, bg="white")
        processing_frame.pack(expand=True, fill="both")
        
        tk.Label(processing_frame, text="💳", font=('Segoe UI', 48), bg="white").pack(pady=(30, 10))
        tk.Label(processing_frame, text=f"正在处理{method}支付...", 
                 font=('Segoe UI', 14), bg="white").pack()
        tk.Label(processing_frame, text="请稍候...", 
                 font=('Segoe UI', 12), bg="white", fg="#636E72").pack(pady=10)
        
        # 进度条
        progress = ttk.Progressbar(processing_frame, mode='indeterminate', length=200)
        progress.pack(pady=20)
        progress.start()
        
        # 2秒后关闭
        def close_processing():
            progress.stop()
            processing_dialog.destroy()
            print(f"✅ {method}支付测试完成")
        
        processing_dialog.after(2000, close_processing)
    
    def run(self):
        """运行测试"""
        self.root.mainloop()

if __name__ == "__main__":
    print("启动支付界面UI测试...")
    test = PaymentUITest()
    test.run()
