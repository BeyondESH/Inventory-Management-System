#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
食品服务公司管理系统 - 功能演示脚本
"""

import sys
import os

def main():
    """主演示函数"""
    print("=" * 60)
    print("🎉 食品服务公司管理系统 - 完整功能演示")
    print("=" * 60)
    
    print("\n🎯 系统功能总览：")
    print("1. 🔐 用户登录注册系统")
    print("   - 完整的登录界面（logo + 标题同行）")
    print("   - 用户注册功能")
    print("   - 游客登录模式")
    print("   - 忘记密码功能")
    
    print("\n2. 📦 库存管理模块")
    print("   - ➕ 添加食材（完整表单验证）")
    print("   - ✏️ 双击编辑食材")
    print("   - 🔧 选中状态提醒 + 修改按钮")
    print("   - 🗑️ 删除功能（安全确认）")
    print("   - 📊 库存状态智能提醒")
    
    print("\n3. 📋 订单管理模块")
    print("   - ➕ 新建订单（完整表单）")
    print("   - ✏️ 双击编辑订单")
    print("   - 🔧 选中状态提醒 + 修改按钮")
    print("   - 🗑️ 删除功能（安全确认）")
    print("   - 📈 订单状态跟踪")
    
    print("\n4. 👥 客户管理模块")
    print("   - ➕ 添加客户（完整表单验证）")
    print("   - ✏️ 双击编辑客户")
    print("   - 🔧 选中状态提醒 + 修改按钮")
    print("   - 🗑️ 删除功能（安全确认）")
    print("   - 🏷️ 客户类型分类管理")
    
    print("\n✨ 统一功能特性：")
    print("   ✅ 所有模块界面风格完全统一")
    print("   ✅ 一致的交互逻辑和操作流程")
    print("   ✅ 完善的数据验证和错误处理")
    print("   ✅ 智能的状态提醒系统")
    print("   ✅ 双击快速编辑功能")
    print("   ✅ 选择后启用修改按钮")
    
    show_feature_comparison()
    
    print("\n" + "=" * 60)
    print("🚀 启动选项：")
    print("1. 启动完整系统")
    print("2. 运行测试脚本")
    print("3. 查看系统信息")
    print("4. 退出演示")
    
    choice = input("\n请选择 [1-4]: ").strip()
    
    if choice == "1":
        print("\n🚀 启动主系统...")
        os.system("python main.py")
        
    elif choice == "2":
        print("\n🧪 运行所有测试...")
        os.system("python test/run_tests.py")
        
    elif choice == "3":
        show_system_info()
        
    elif choice == "4":
        print("👋 感谢使用食品服务公司管理系统演示！")
        
    else:
        print("❌ 无效选择")

def show_feature_comparison():
    """显示功能对比表"""
    print("\n📊 三大模块功能对比:")
    print("+" + "-" * 58 + "+")
    print("| 功能特性     | 库存管理 | 订单管理 | 客户管理 |")
    print("+" + "-" * 58 + "+")
    print("| ➕ 添加功能   |    ✅    |    ✅    |    ✅    |")
    print("| ✏️ 编辑功能   |    ✅    |    ✅    |    ✅    |") 
    print("| 🗑️ 删除功能   |    ✅    |    ✅    |    ✅    |")
    print("| 💡 选择提醒   |    ✅    |    ✅    |    ✅    |")
    print("| ⚡ 双击编辑   |    ✅    |    ✅    |    ✅    |")
    print("| 🔧 修改按钮   |    ✅    |    ✅    |    ✅    |")
    print("| 🛡️ 数据验证   |    ✅    |    ✅    |    ✅    |")
    print("| 📊 状态反馈   |    ✅    |    ✅    |    ✅    |")
    print("+" + "-" * 58 + "+")

def show_system_info():
    """显示系统信息"""
    print("\n📋 系统信息:")
    print(f"   Python版本: {sys.version.split()[0]}")
    print(f"   当前目录: {os.getcwd()}")
    
    # 检查依赖
    try:
        import tkinter
        print("   ✅ Tkinter: 已安装")
    except ImportError:
        print("   ❌ Tkinter: 未安装")
    
    # 检查源码文件
    src_files = [
        "src/login_module.py",
        "src/user_manager.py", 
        "src/system_launcher.py",
        "src/inventory_system.py",
        "src/inventory_module.py",
        "src/order_module.py",
        "src/customer_module.py"
    ]
    
    print("\n📁 源码文件检查:")
    for file in src_files:
        if os.path.exists(file):
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file}")
    
    # 检查测试文件
    test_files = [
        "test/test_inventory_module.py",
        "test/test_order_module.py",
        "test/test_customer_module.py",
        "test/run_tests.py"
    ]
    
    print("\n🧪 测试文件检查:")
    for file in test_files:
        if os.path.exists(file):
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 用户中断，程序退出")
    except Exception as e:
        print(f"\n❌ 程序执行出错: {e}")
        import traceback
        traceback.print_exc()
