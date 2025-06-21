#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
财务模块功能验证脚本
快速验证所有实现的功能
"""

import sys
import os
import json

# 添加项目路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, 'modern_system'))
sys.path.insert(0, os.path.join(project_root, 'modern_system', 'modules'))

def verify_finance_features():
    """验证财务模块功能"""
    print("🔍 开始验证财务模块功能...")
    print("-" * 50)
    
    results = {
        "module_import": False,
        "data_file": False,
        "methods": {},
        "data_integrity": False
    }
    
    try:
        # 1. 验证模块导入
        print("1. 检查模块导入...")
        from modern_finance_module import ModernFinanceModule
        results["module_import"] = True
        print("   ✅ 财务模块导入成功")
        
        # 2. 验证数据文件
        print("2. 检查数据文件...")
        data_file = os.path.join(project_root, 'modern_system', 'data', 'fixed_costs.json')
        if os.path.exists(data_file):
            results["data_file"] = True
            print(f"   ✅ 数据文件存在: {data_file}")
            
            # 验证数据内容
            with open(data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            if isinstance(data, list) and len(data) > 0:
                results["data_integrity"] = True
                print(f"   ✅ 数据完整性验证通过，包含 {len(data)} 条记录")
            else:
                print("   ❌ 数据文件格式或内容异常")
        else:
            print(f"   ❌ 数据文件不存在: {data_file}")
        
        # 3. 验证方法实现
        print("3. 检查方法实现...")
        
        # 创建模拟的tkinter环境进行测试
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()  # 隐藏窗口
        
        try:
            main_frame = tk.Frame(root)
            title_frame = tk.Frame(root)
            
            module = ModernFinanceModule(main_frame, title_frame)
            
            # 检查关键方法
            methods_to_check = [
                'load_fixed_costs',
                'save_fixed_costs', 
                'add_fixed_cost',
                'edit_fixed_cost',
                'delete_fixed_cost',
                'calculate_fixed_cost_stats',
                'convert_to_monthly',
                'get_costs_from_tree',
                'add_income_record',
                'add_expense_record'
            ]
            
            for method in methods_to_check:
                if hasattr(module, method):
                    results["methods"][method] = True
                    print(f"   ✅ {method}")
                else:
                    results["methods"][method] = False
                    print(f"   ❌ {method}")
            
            # 测试数据加载功能
            print("4. 测试数据加载功能...")
            try:
                costs_data = module.load_fixed_costs()
                if isinstance(costs_data, list):
                    print(f"   ✅ 数据加载成功，{len(costs_data)} 条记录")
                else:
                    print("   ❌ 数据加载返回格式异常")
            except Exception as e:
                print(f"   ❌ 数据加载失败: {e}")
            
            # 测试统计计算功能
            print("5. 测试统计计算功能...")
            try:
                stats = module.calculate_fixed_cost_stats()
                if isinstance(stats, list) and len(stats) > 0:
                    print(f"   ✅ 统计计算成功，{len(stats)} 个统计项")
                    for stat in stats:
                        print(f"      • {stat['title']}: {stat['value']}")
                else:
                    print("   ❌ 统计计算返回格式异常")
            except Exception as e:
                print(f"   ❌ 统计计算失败: {e}")
            
        finally:
            root.destroy()
        
    except ImportError as e:
        print(f"   ❌ 模块导入失败: {e}")
    except Exception as e:
        print(f"   ❌ 验证过程出错: {e}")
    
    # 输出验证结果摘要
    print("\n" + "=" * 50)
    print("📊 验证结果摘要:")
    print(f"   模块导入: {'✅' if results['module_import'] else '❌'}")
    print(f"   数据文件: {'✅' if results['data_file'] else '❌'}")
    print(f"   数据完整性: {'✅' if results['data_integrity'] else '❌'}")
    
    implemented_methods = sum(1 for v in results['methods'].values() if v)
    total_methods = len(results['methods'])
    print(f"   方法实现: {implemented_methods}/{total_methods} {'✅' if implemented_methods == total_methods else '⚠️'}")
    
    # 功能完成度评估
    completion_rate = (
        (1 if results['module_import'] else 0) +
        (1 if results['data_file'] else 0) +
        (1 if results['data_integrity'] else 0) +
        (implemented_methods / total_methods)
    ) / 4 * 100
    
    print(f"\n🎯 功能完成度: {completion_rate:.1f}%")
    
    if completion_rate >= 90:
        print("🎉 财务模块功能实现优秀！")
    elif completion_rate >= 80:
        print("👍 财务模块功能实现良好！")
    elif completion_rate >= 70:
        print("⚠️ 财务模块功能基本实现，需要改进")
    else:
        print("❌ 财务模块功能实现不完整，需要重点修复")
    
    print("=" * 50)
    
    return completion_rate >= 80

if __name__ == "__main__":
    success = verify_finance_features()
    
    if success:
        print("\n✅ 验证通过 - 财务模块符合要求")
    else:
        print("\n❌ 验证失败 - 财务模块需要进一步完善")
