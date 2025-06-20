#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UI模块切换测试脚本
测试各个模块的显示和切换功能
"""

import sys
import os
import tkinter as tk
from tkinter import ttk
import threading
import time

# 添加路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

def test_ui_modules():
    """测试UI模块切换"""
    print("=" * 50)
    print("启动UI模块切换测试...")
    print("=" * 50)
    
    try:
        from modern_system.core.modern_ui_system import ModernFoodServiceSystem
        
        # 创建应用实例
        app = ModernFoodServiceSystem()
        
        # 测试各个模块切换
        modules_to_test = ["sales", "inventory", "meal", "order", "customer", "employee", "finance", "charts"]
        
        def auto_test():
            """自动测试各模块切换"""
            time.sleep(2)  # 等待界面完全加载
            
            for i, module in enumerate(modules_to_test):
                print(f"测试切换到: {module}")
                try:
                    # 切换模块
                    app.switch_module(module)
                    app.root.update()  # 更新界面
                    time.sleep(1)  # 等待1秒
                    print(f"✓ {module} 模块显示成功")
                except Exception as e:
                    print(f"✗ {module} 模块显示失败: {e}")
            
            print("\n所有模块测试完成，程序将在5秒后自动关闭...")
            time.sleep(5)
            app.root.quit()
        
        # 在单独线程中运行自动测试
        test_thread = threading.Thread(target=auto_test, daemon=True)
        test_thread.start()
        
        print("UI测试窗口已启动，将自动测试各个模块...")
        print("观察窗口中各模块的切换情况...")
        
        # 运行主循环
        app.run()
        
        return True
    
    except Exception as e:
        print(f"UI模块测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_login_module():
    """测试登录模块"""
    print("=" * 50)
    print("测试登录模块UI...")
    print("=" * 50)
    
    try:
        from modern_system.modules.modern_login_module import ModernLoginModule
        
        # 创建测试窗口
        root = tk.Tk()
        root.withdraw()  # 隐藏主窗口
        
        # 创建登录模块
        login_module = ModernLoginModule()
        
        def auto_close():
            """3秒后自动关闭"""
            time.sleep(3)
            login_module.root.quit()
        
        # 启动自动关闭线程
        close_thread = threading.Thread(target=auto_close, daemon=True)
        close_thread.start()
        
        print("登录界面已启动，将在3秒后自动关闭...")
        login_module.run()
        
        print("✓ 登录模块测试完成")
        return True
        
    except Exception as e:
        print(f"✗ 登录模块测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("智慧餐饮管理系统 - UI功能测试")
    print("=" * 60)
    
    # 选择测试类型
    print("请选择测试类型:")
    print("1. 登录模块测试（快速）")
    print("2. 主UI模块切换测试（完整）")
    print("3. 跳过UI测试")
    
    try:
        choice = input("请输入选择 (1-3): ").strip()
        
        if choice == "1":
            print("\n开始登录模块测试...")
            result = test_login_module()
        elif choice == "2":
            print("\n开始主UI模块切换测试...")
            result = test_ui_modules()
        elif choice == "3":
            print("\n跳过UI测试")
            result = True
        else:
            print("无效选择，跳过UI测试")
            result = True
            
        if result:
            print("\n🎉 UI测试完成！")
        else:
            print("\n⚠️ UI测试中出现错误")
            
    except KeyboardInterrupt:
        print("\n用户中断测试")
    except Exception as e:
        print(f"\n测试异常: {e}")

if __name__ == "__main__":
    main()
