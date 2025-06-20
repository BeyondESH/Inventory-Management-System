#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整系统测试脚本
测试所有模块的基本功能和UI显示
"""

import sys
import os
import traceback

# 添加路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

def test_imports():
    """测试所有模块的导入"""
    print("=" * 50)
    print("测试模块导入...")
    print("=" * 50)
    
    modules_to_test = [
        ("登录模块", "modern_system.modules.modern_login_module", "ModernLoginModule"),
        ("UI系统", "modern_system.core.modern_ui_system", "ModernFoodServiceSystem"),
        ("销售模块", "modern_system.modules.modern_sales_module", "ModernSalesModule"),
        ("库存模块", "modern_system.modules.modern_inventory_module", "ModernInventoryModule"),
        ("订单模块", "modern_system.modules.modern_order_module", "ModernOrderModule"),
        ("客户模块", "modern_system.modules.modern_customer_module", "ModernCustomerModule"),
        ("员工模块", "modern_system.modules.modern_employee_module", "ModernEmployeeModule"),
        ("财务模块", "modern_system.modules.modern_finance_module", "ModernFinanceModule"),
        ("菜品模块", "modern_system.modules.modern_meal_module", "ModernMealModule"),
        ("图表模块", "modern_system.ui.meituan_charts_module", "ModernChartsModule"),
        ("数据管理", "modern_system.utils.data_manager", "data_manager")
    ]
    
    success_count = 0
    total_count = len(modules_to_test)
    
    for module_name, module_path, class_name in modules_to_test:
        try:
            if class_name == "data_manager":
                exec(f"from {module_path} import {class_name}")
            else:
                exec(f"from {module_path} import {class_name}")
            print(f"✓ {module_name}: 导入成功")
            success_count += 1
        except Exception as e:
            print(f"✗ {module_name}: 导入失败 - {e}")
    
    print(f"\n导入测试结果: {success_count}/{total_count} 成功")
    return success_count == total_count

def test_syntax():
    """测试Python文件语法"""
    print("=" * 50)
    print("测试Python文件语法...")
    print("=" * 50)
    
    files_to_test = [
        "main.py",
        "main_modern.py", 
        "launch_system.py",
        "modern_system/core/modern_ui_system.py",
        "modern_system/modules/modern_login_module.py",
        "modern_system/modules/modern_sales_module.py",
        "modern_system/modules/modern_inventory_module.py",
        "modern_system/modules/modern_order_module.py",
        "modern_system/modules/modern_customer_module.py",
        "modern_system/modules/modern_employee_module.py",
        "modern_system/modules/modern_finance_module.py",
        "modern_system/modules/modern_meal_module.py",
        "modern_system/ui/meituan_charts_module.py",
        "modern_system/utils/data_manager.py"
    ]
    
    success_count = 0
    total_count = len(files_to_test)
    
    for file_path in files_to_test:
        full_path = os.path.join(current_dir, file_path)
        if not os.path.exists(full_path):
            print(f"✗ {file_path}: 文件不存在")
            continue
        
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                source = f.read()
            compile(source, full_path, 'exec')
            print(f"✓ {file_path}: 语法正确")
            success_count += 1
        except SyntaxError as e:
            print(f"✗ {file_path}: 语法错误 - 行{e.lineno}: {e.msg}")
        except Exception as e:
            print(f"✗ {file_path}: 其他错误 - {e}")
    
    print(f"\n语法测试结果: {success_count}/{total_count} 成功")
    return success_count == total_count

def test_ui_creation():
    """测试UI创建（不显示窗口）"""
    print("=" * 50)
    print("测试UI组件创建...")
    print("=" * 50)
    
    try:
        import tkinter as tk
        # 创建测试用的根窗口
        test_root = tk.Tk()
        test_root.withdraw()  # 隐藏窗口
        
        print("✓ Tkinter根窗口创建成功")
        
        # 测试基本组件
        test_frame = tk.Frame(test_root)
        test_label = tk.Label(test_frame, text="测试")
        test_button = tk.Button(test_frame, text="测试按钮")
        
        print("✓ 基本Tkinter组件创建成功")
        
        # 清理
        test_root.destroy()
        
        return True
    except Exception as e:
        print(f"✗ UI组件创建失败: {e}")
        return False

def test_data_manager():
    """测试数据管理器"""
    print("=" * 50)
    print("测试数据管理器...")
    print("=" * 50)
    
    try:
        from modern_system.utils.data_manager import data_manager
        
        # 测试基本方法
        stats = data_manager.get_dashboard_stats()
        print(f"✓ 获取仪表盘数据成功: {len(stats)} 项")
        
        # 测试添加数据
        test_order = {
            "id": "test_001",
            "table": "T001",
            "items": [{"name": "测试菜品", "price": 10.0, "quantity": 1}],
            "total": 10.0,
            "status": "completed"
        }
        
        data_manager.add_order(test_order)
        print("✓ 添加订单数据成功")
        
        orders = data_manager.get_orders()
        print(f"✓ 获取订单数据成功: {len(orders)} 条")
        
        return True
    except Exception as e:
        print(f"✗ 数据管理器测试失败: {e}")
        traceback.print_exc()
        return False

def main():
    """主测试函数"""
    print("智慧餐饮管理系统 - 完整测试")
    print("=" * 60)
    
    # 运行所有测试
    tests = [
        ("语法检查", test_syntax),
        ("模块导入", test_imports),
        ("UI组件", test_ui_creation),
        ("数据管理", test_data_manager)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n开始 {test_name} 测试...")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ {test_name} 测试异常: {e}")
            results.append((test_name, False))
        print(f"{test_name} 测试完成\n")
    
    # 输出总结果
    print("=" * 60)
    print("测试总结:")
    print("=" * 60)
    
    success_count = 0
    for test_name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"{test_name}: {status}")
        if result:
            success_count += 1
    
    print(f"\n总体结果: {success_count}/{len(results)} 测试通过")
    
    if success_count == len(results):
        print("🎉 所有测试都通过了！系统状态良好。")
    else:
        print("⚠️ 部分测试失败，请检查相关模块。")
    
    return success_count == len(results)

if __name__ == "__main__":
    main()
