#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试水平滚动功能的脚本
"""

import tkinter as tk
from tkinter import ttk

def test_horizontal_scroll():
    """测试水平滚动功能"""
    
    root = tk.Tk()
    root.title("水平滚动测试")
    root.geometry("600x300")
    
    # 创建主框架
    main_frame = tk.Frame(root, bg='white')
    main_frame.pack(fill='both', expand=True, padx=20, pady=20)
    
    # 标题
    title_label = tk.Label(main_frame, text="可制作菜品 - 水平滚动测试", 
                          font=('Arial', 14, 'bold'), bg='white')
    title_label.pack(pady=(0, 10))
    
    # 创建容器框架
    container_frame = tk.Frame(main_frame, bg='white')
    container_frame.pack(fill='x')
    
    # 创建画布
    canvas = tk.Canvas(container_frame, bg='#f0f0f0', highlightthickness=0, height=150)
    
    # 创建水平滚动条
    scrollbar = ttk.Scrollbar(container_frame, orient="horizontal", command=canvas.xview)
    canvas.configure(xscrollcommand=scrollbar.set)
    
    # 打包组件
    canvas.pack(side="top", fill="both")
    scrollbar.pack(side="bottom", fill="x")
    
    # 创建内容框架
    content_frame = tk.Frame(canvas, bg='#f0f0f0')
    canvas_frame_id = canvas.create_window((0, 0), window=content_frame, anchor="nw")
    
    # 添加多个测试卡片
    dishes = [
        "🍜 西红柿牛肉面",
        "🍚 蛋炒饭", 
        "🍔 牛肉汉堡",
        "🍟 薯条",
        "🍣 三文鱼套餐",
        "🍗 家常鸡肉饭",
        "🦐 海鲜炒饭",
        "🍖 经典牛肉饭",
        "🥦 蔬菜套餐",
        "🌶️ 麻辣豆腐",
        "🍜 猪骨拉面",
        "🍱 日式照烧鸡肉饭",
        "🍝 蘑菇意面",
        "🥟 叉烧包",
        "🍛 泰式绿咖喱"
    ]
    
    for i, dish in enumerate(dishes):
        card = tk.Frame(content_frame, bg='white', bd=1, relief='solid', 
                       width=150, height=120)
        card.grid(row=0, column=i, padx=5, pady=10, sticky='ns')
        card.grid_propagate(False)
        
        # 菜品名称
        name_parts = dish.split(' ', 1)
        emoji = name_parts[0]
        name = name_parts[1] if len(name_parts) > 1 else dish
        
        tk.Label(card, text=emoji, font=('Segoe UI Emoji', 20), bg='white').pack(pady=(10,0))
        tk.Label(card, text=name, font=('Arial', 10), bg='white', 
                wraplength=130, justify='center').pack(pady=5)
        tk.Label(card, text=f"可制作 {i+1} 份", font=('Arial', 9, 'bold'), 
                bg='white', fg='green').pack(pady=(0,10))
    
    def on_canvas_configure(event):
        """处理画布大小变化"""
        canvas_width = event.width
        frame_width = content_frame.winfo_reqwidth()
        
        if frame_width > canvas_width:
            canvas.itemconfig(canvas_frame_id, width=frame_width)
        else:
            canvas.itemconfig(canvas_frame_id, width=canvas_width)
    
    def on_frame_configure(event):
        """处理框架大小变化"""
        canvas.configure(scrollregion=canvas.bbox("all"))
    
    def on_mousewheel(event):
        """处理鼠标滚轮"""
        bbox = canvas.bbox("all")
        if bbox and bbox[2] > canvas.winfo_width():
            if event.delta:
                canvas.xview_scroll(int(-1*(event.delta/120)), "units")
            else:
                if event.num == 4:
                    canvas.xview_scroll(-1, "units")
                elif event.num == 5:
                    canvas.xview_scroll(1, "units")
    
    # 绑定事件
    canvas.bind('<Configure>', on_canvas_configure)
    content_frame.bind('<Configure>', on_frame_configure)
    
    # 绑定鼠标滚轮事件
    canvas.bind("<Button-4>", on_mousewheel)
    canvas.bind("<Button-5>", on_mousewheel)
    canvas.bind("<MouseWheel>", on_mousewheel)
    content_frame.bind("<Button-4>", on_mousewheel)
    content_frame.bind("<Button-5>", on_mousewheel)
    content_frame.bind("<MouseWheel>", on_mousewheel)
    
    # 设置焦点以接收滚轮事件
    canvas.bind("<Enter>", lambda e: canvas.focus_set())
    content_frame.bind("<Enter>", lambda e: content_frame.focus_set())
    
    # 添加说明文本
    info_label = tk.Label(main_frame, 
                         text="测试说明：\n1. 拖拽下方滚动条来滚动\n2. 在卡片区域使用鼠标滚轮滚动\n3. 检查滚动条是否能正常拖拽",
                         font=('Arial', 10), bg='white', justify='left')
    info_label.pack(pady=(10, 0), anchor='w')
    
    # 强制更新并设置滚动区域
    def setup_scroll():
        content_frame.update_idletasks()
        canvas.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))
        
        # 检查是否需要滚动
        bbox = canvas.bbox("all")
        canvas_width = canvas.winfo_width()
        
        if bbox:
            frame_width = bbox[2] - bbox[0]
            print(f"Canvas width: {canvas_width}, Frame width: {frame_width}")
            if frame_width > canvas_width:
                print("✓ 滚动条应该是可用的")
                canvas.itemconfig(canvas_frame_id, width=frame_width)
            else:
                print("⚠ 内容宽度不足，可能不需要滚动")
    
    root.after(100, setup_scroll)  # 延迟执行以确保所有组件都已渲染
    
    root.mainloop()

if __name__ == "__main__":
    test_horizontal_scroll()
