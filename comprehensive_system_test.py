#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智慧餐饮管理系统综合测试脚本
测试所有核心功能和模块联动
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

# 添加项目路径
current_dir = os.path.dirname(os.path.abspath(__file__))
modern_system_dir = os.path.join(current_dir, 'modern_system')
sys.path.insert(0, current_dir)
sys.path.insert(0, modern_system_dir)

def test_data_manager():
    """测试数据管理中心"""
    print("🔍 测试数据管理中心...")
    
    try:
        from modern_system.utils.data_manager import data_manager
        
        # 测试获取统计数据
        stats = data_manager.get_dashboard_stats()
        print(f"✓ 获取统计数据成功: {stats}")
        
        # 测试获取订单数据
        orders = data_manager.get_orders()
        print(f"✓ 获取订单数据成功，共 {len(orders)} 条订单")
        
        # 测试获取库存数据
        inventory = data_manager.get_inventory()
        print(f"✓ 获取库存数据成功，共 {len(inventory)} 个商品")
        
        # 测试低库存预警
        low_stock = data_manager.get_low_stock_items()
        print(f"✓ 低库存商品: {len(low_stock)} 个")
        
        # 测试添加订单
        test_order = {
            'customer_name': '测试客户',
            'phone': '138****0000',
            'address': '测试地址',
            'items': [
                {'name': '番茄牛肉面', 'quantity': 1, 'price': 25.0}
            ],
            'total_amount': 25.0,
            'payment_method': '微信支付'
        }
        
        order_id = data_manager.add_order(test_order)
        print(f"✓ 添加测试订单成功: {order_id}")
        
        return True
        
    except Exception as e:
        print(f"✗ 数据管理中心测试失败: {e}")
        return False

def test_login_module():
    """测试登录模块"""
    print("🔍 测试登录模块...")
    
    try:
        from modern_system.modules.modern_login_module import ModernLoginModule
        print("✓ 登录模块导入成功")
        return True
    except Exception as e:
        print(f"✗ 登录模块测试失败: {e}")
        return False

def test_ui_system():
    """测试UI系统"""
    print("🔍 测试UI系统...")
    
    try:
        from modern_system.core.modern_ui_system import ModernFoodServiceSystem
        print("✓ UI系统导入成功")
        return True
    except Exception as e:
        print(f"✗ UI系统测试失败: {e}")
        return False

def test_business_modules():
    """测试业务模块"""
    print("🔍 测试业务模块...")
    
    modules_to_test = [
        'modern_order_module',
        'modern_inventory_module', 
        'modern_employee_module',
        'modern_meal_module'
    ]
    
    success_count = 0
    
    for module_name in modules_to_test:
        try:
            module = __import__(f'modern_system.modules.{module_name}', fromlist=[module_name])
            print(f"✓ {module_name} 导入成功")
            success_count += 1
        except Exception as e:
            print(f"✗ {module_name} 导入失败: {e}")
    
    return success_count == len(modules_to_test)

def run_visual_test():
    """运行可视化测试"""
    print("🚀 启动可视化测试...")
    
    try:
        # 创建测试窗口
        root = tk.Tk()
        root.title("智慧餐饮管理系统 - 测试")
        root.geometry("600x400")
        root.configure(bg="#F8F9FA")
        
        # 测试结果显示
        title_label = tk.Label(root, text="🧪 系统测试结果", 
                              font=('Microsoft YaHei UI', 16, 'bold'),
                              bg="#F8F9FA", fg="#2D3436")
        title_label.pack(pady=20)
        
        # 测试各个组件
        tests = [
            ("数据管理中心", test_data_manager),
            ("登录模块", test_login_module), 
            ("UI系统", test_ui_system),
            ("业务模块", test_business_modules)
        ]
        
        results_frame = tk.Frame(root, bg="#F8F9FA")
        results_frame.pack(fill="both", expand=True, padx=40, pady=20)
        
        all_passed = True
        
        for test_name, test_func in tests:
            result = test_func()
            status = "✅ 通过" if result else "❌ 失败"
            color = "#00B894" if result else "#E84393"
            
            result_label = tk.Label(results_frame, 
                                  text=f"{test_name}: {status}",
                                  font=('Microsoft YaHei UI', 12),
                                  bg="#F8F9FA", fg=color)
            result_label.pack(anchor="w", pady=5)
            
            if not result:
                all_passed = False
        
        # 总结
        summary = "🎉 所有测试通过！" if all_passed else "⚠️ 部分测试失败"
        summary_color = "#00B894" if all_passed else "#F39C12"
        
        summary_label = tk.Label(results_frame, text=summary,
                               font=('Microsoft YaHei UI', 14, 'bold'),
                               bg="#F8F9FA", fg=summary_color)
        summary_label.pack(pady=20)
        
        # 操作按钮
        btn_frame = tk.Frame(root, bg="#F8F9FA")
        btn_frame.pack(fill="x", padx=40, pady=20)
        
        if all_passed:
            launch_btn = tk.Button(btn_frame, text="🚀 启动系统",
                                 font=('Microsoft YaHei UI', 12, 'bold'),
                                 bg="#FF6B35", fg="white",
                                 bd=0, pady=10, padx=20,
                                 command=lambda: launch_system(root))
            launch_btn.pack(side="left", padx=(0, 10))
        
        close_btn = tk.Button(btn_frame, text="关闭测试",
                             font=('Microsoft YaHei UI', 12),
                             bg="#636E72", fg="white",
                             bd=0, pady=10, padx=20,
                             command=root.destroy)
        close_btn.pack(side="left")
        
        root.mainloop()
        
    except Exception as e:
        print(f"✗ 可视化测试失败: {e}")

def launch_system(test_window):
    """启动系统"""
    try:
        test_window.destroy()
        
        # 导入并启动登录系统
        from modern_system.modules.modern_login_module import ModernLoginModule
        login_app = ModernLoginModule()
        login_app.run()
        
    except Exception as e:
        messagebox.showerror("启动错误", f"无法启动系统: {e}")

def main():
    """主函数"""
    print("=" * 60)
    print("🧪 智慧餐饮管理系统 - 综合测试")
    print("=" * 60)
    
    # 运行可视化测试
    run_visual_test()

if __name__ == "__main__":
    main()
