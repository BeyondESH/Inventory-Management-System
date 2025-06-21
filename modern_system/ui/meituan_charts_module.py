#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
现代化图表模块 - 数据可视化
"""

import tkinter as tk
from tkinter import ttk
from typing import Dict, List, Any
import datetime

# 导入数据管理中心
try:
    from ..utils.data_manager import data_manager
except ImportError:
    try:
        from data_manager import data_manager
    except ImportError:
        # 模拟数据管理器
        class MockDataManager:
            def get_dashboard_stats(self):
                return {'today_revenue': 2580, 'today_orders': 25, 'low_stock_count': 3, 'total_customers': 156}
        data_manager = MockDataManager()

class ModernChartsModule:
    def __init__(self, parent_frame, title_frame):
        self.parent_frame = parent_frame
        self.title_frame = title_frame
        
        # 现代化配色方案
        self.colors = {
            'primary': '#FF6B35',
            'secondary': '#F7931E',
            'success': '#00B894',
            'warning': '#FDCB6E',
            'danger': '#E74C3C',
            'info': '#3498DB',
            'background': '#F8F9FA',
            'surface': '#FFFFFF',
            'text_primary': '#2D3436',
            'text_secondary': '#636E72',
            'border': '#E1E8ED'
        }
        
        # 字体配置
        self.fonts = {
            'title': ('Microsoft YaHei UI', 16, 'bold'),
            'heading': ('Microsoft YaHei UI', 14, 'bold'),
            'body': ('Microsoft YaHei UI', 12),
            'small': ('Microsoft YaHei UI', 10)
        }
        
        self.main_frame = None
        
    def show(self):
        """显示图表界面"""
        if self.main_frame:
            self.main_frame.destroy()
        
        self.main_frame = tk.Frame(self.parent_frame, bg=self.colors['background'])
        self.main_frame.pack(fill="both", expand=True)
        
        # 标题
        title_label = tk.Label(self.main_frame, text="📈 数据图表", 
                              font=self.fonts['title'],
                              bg=self.colors['background'], 
                              fg=self.colors['text_primary'])
        title_label.pack(pady=(0, 20))
        
        # 创建图表区域
        self.create_charts_area()
        
    def create_charts_area(self):
        """创建图表区域"""
        # 主容器
        charts_container = tk.Frame(self.main_frame, bg=self.colors['background'])
        charts_container.pack(fill="both", expand=True)
        
        # 左侧图表
        left_frame = tk.Frame(charts_container, bg=self.colors['surface'], relief="flat", bd=1)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # 右侧图表
        right_frame = tk.Frame(charts_container, bg=self.colors['surface'], relief="flat", bd=1)
        right_frame.pack(side="right", fill="both", expand=True)
        
        # 销售趋势图
        self.create_sales_chart(left_frame)
        
        # 产品分析图
        self.create_product_chart(right_frame)
          # 底部图表
        bottom_frame = tk.Frame(self.main_frame, bg=self.colors['surface'], relief="flat", bd=1)
        bottom_frame.pack(fill="x", pady=(20, 0))
        
        self.create_revenue_chart(bottom_frame)
        
    def create_sales_chart(self, parent):
        """创建销售趋势图"""
        chart_title = tk.Label(parent, text="📊 销售趋势", 
                              font=self.fonts['heading'],
                              bg=self.colors['surface'], 
                              fg=self.colors['text_primary'])
        chart_title.pack(pady=10)
        
        # 获取真实销售数据
        chart_frame = tk.Frame(parent, bg=self.colors['surface'])
        chart_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # 使用真实数据
        chart_data = self.get_real_sales_data()
        
        for day, amount, percentage in chart_data:
            row_frame = tk.Frame(chart_frame, bg=self.colors['surface'])
            row_frame.pack(fill="x", pady=2)
            
            # 日期
            day_label = tk.Label(row_frame, text=day, width=8,
                               font=self.fonts['body'], bg=self.colors['surface'],
                               fg=self.colors['text_primary'])
            day_label.pack(side="left")
            
            # 进度条
            progress_frame = tk.Frame(row_frame, bg=self.colors['background'], height=20)
            progress_frame.pack(side="left", fill="x", expand=True, padx=5)
            
            bar_width = int(percentage * 2)  # 最大宽度200px
            bar = tk.Frame(progress_frame, bg=self.colors['primary'], height=15, width=bar_width)
            bar.pack(side="left", anchor="w", pady=2)
              # 金额
            amount_label = tk.Label(row_frame, text=amount, width=10,
                                  font=self.fonts['body'], bg=self.colors['surface'],
                                  fg=self.colors['text_secondary'])
            amount_label.pack(side="right")
            
    def create_product_chart(self, parent):
        """创建产品分析图"""
        chart_title = tk.Label(parent, text="🍽️ 热销产品", 
                              font=self.fonts['heading'],
                              bg=self.colors['surface'], 
                              fg=self.colors['text_primary'])
        chart_title.pack(pady=10)
        
        # 获取真实产品数据
        chart_frame = tk.Frame(parent, bg=self.colors['surface'])
        chart_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # 使用真实数据
        product_data = self.get_real_product_data()
        
        # 颜色列表
        colors = [self.colors['success'], self.colors['primary'], self.colors['info'], 
                 self.colors['warning'], self.colors['secondary']]
        
        for i, (product, count, percentage) in enumerate(product_data):
            color = colors[i % len(colors)]
            row_frame = tk.Frame(chart_frame, bg=self.colors['surface'])
            row_frame.pack(fill="x", pady=3)
            
            # 产品名
            product_label = tk.Label(row_frame, text=product, width=12,
                                   font=self.fonts['body'], bg=self.colors['surface'],
                                   fg=self.colors['text_primary'])
            product_label.pack(side="left")
            
            # 圆点指示器
            dot = tk.Label(row_frame, text="●", font=('Segoe UI', 16),
                         bg=self.colors['surface'], fg=color)
            dot.pack(side="left", padx=5)
              # 数量
            count_label = tk.Label(row_frame, text=f"{count}份", width=8,
                                 font=self.fonts['body'], bg=self.colors['surface'],
                                 fg=self.colors['text_secondary'])
            count_label.pack(side="right")
            
    def create_revenue_chart(self, parent):
        """创建收入图表"""
        chart_title = tk.Label(parent, text="💰 月度收入统计", 
                              font=self.fonts['heading'],
                              bg=self.colors['surface'], 
                              fg=self.colors['text_primary'])
        chart_title.pack(pady=10)
        
        # 获取真实收入数据
        chart_frame = tk.Frame(parent, bg=self.colors['surface'])
        chart_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # 使用真实数据
        revenue_data = self.get_real_revenue_data()
        max_revenue = max([rev for _, rev in revenue_data]) if revenue_data else 1
        
        # 创建月度收入条形图
        bars_frame = tk.Frame(chart_frame, bg=self.colors['surface'])
        bars_frame.pack(fill="both", expand=True)
        
        for month, revenue in revenue_data:
            month_frame = tk.Frame(bars_frame, bg=self.colors['surface'])
            month_frame.pack(side="left", fill="both", expand=True, padx=5)
            
            # 收入金额
            amount_label = tk.Label(month_frame, text=f"￥{revenue/1000:.0f}K" if revenue > 0 else "￥0K",
                                  font=self.fonts['small'], bg=self.colors['surface'],
                                  fg=self.colors['text_secondary'])
            amount_label.pack(side="top", pady=2)
            
            # 条形图
            bar_height = int((revenue / max_revenue) * 80) if max_revenue > 0 else 0  # 最大高度80px
            bar = tk.Frame(month_frame, bg=self.colors['primary'], 
                         width=40, height=bar_height)
            bar.pack(side="top", pady=2)
            bar.pack_propagate(False)
            
            # 月份标签
            month_label = tk.Label(month_frame, text=month,
                                 font=self.fonts['body'], bg=self.colors['surface'],
                                 fg=self.colors['text_primary'])
            month_label.pack(side="bottom", pady=5)
    
    def get_real_sales_data(self):
        """从数据管理器获取真实销售数据"""
        try:
            # 获取最近7天的销售数据
            from datetime import datetime, timedelta
            today = datetime.now()
            
            # 从数据管理器获取销售数据
            daily_sales = {}
            for i in range(7):
                date = today - timedelta(days=i)
                date_str = date.strftime('%Y-%m-%d')
                revenue = data_manager.get_daily_revenue(date_str)
                daily_sales[date_str] = revenue
            
            # 构建图表数据
            chart_data = []
            for i in range(6, -1, -1):  # 从6天前到今天
                date = today - timedelta(days=i)
                date_str = date.strftime('%Y-%m-%d')
                weekday = ['周一', '周二', '周三', '周四', '周五', '周六', '周日'][date.weekday()]
                
                sales_amount = daily_sales.get(date_str, 0)
                # 计算相对百分比（以最大值为100%）
                max_sales = max(daily_sales.values()) if daily_sales else 1
                percentage = int((sales_amount / max_sales) * 100) if max_sales > 0 else 0
                
                chart_data.append((weekday, f"￥{sales_amount:,.0f}", percentage))
            
            return chart_data
            
        except Exception as e:
            print(f"获取销售数据失败: {e}")
            # 返回默认数据
            return [
                ("周一", "￥0", 0),
                ("周二", "￥0", 0),
                ("周三", "￥0", 0),
                ("周四", "￥0", 0),
                ("周五", "￥0", 0),
                ("周六", "￥0", 0),
                ("周日", "￥0", 0)
            ]
    
    def get_real_product_data(self):
        """从数据管理器获取真实产品数据"""
        try:
            # 获取销售记录
            sales_records = data_manager.load_data('sales')
            
            # 统计产品销量
            product_sales = {}
            for record in sales_records:
                items = record.get('items', [])
                for item in items:
                    product_name = item.get('name', '未知产品')
                    quantity = item.get('quantity', 0)
                    
                    if product_name not in product_sales:
                        product_sales[product_name] = 0
                    product_sales[product_name] += quantity
            
            # 按销量排序，取前5名
            sorted_products = sorted(product_sales.items(), key=lambda x: x[1], reverse=True)[:5]
            
            # 计算百分比
            max_quantity = max([qty for _, qty in sorted_products]) if sorted_products else 1
            chart_data = []
            
            for product, quantity in sorted_products:
                percentage = int((quantity / max_quantity) * 100) if max_quantity > 0 else 0
                chart_data.append((product, str(quantity), percentage))
            
            # 如果没有数据，返回默认数据
            if not chart_data:
                chart_data = [
                    ("暂无数据", "0", 0),
                ]
            
            return chart_data
            
        except Exception as e:
            print(f"获取产品数据失败: {e}")
            # 返回默认数据
            return [
                ("暂无数据", "0", 0),            ]
    
    def refresh_charts(self):
        """刷新图表数据"""
        if self.main_frame:
            # 重新创建图表
            for widget in self.main_frame.winfo_children():
                if widget != self.main_frame.winfo_children()[0]:  # 保留标题
                    widget.destroy()
            
            # 重新创建图表区域
            self.create_charts_area()
