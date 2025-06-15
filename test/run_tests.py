#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试运行器 - 方便运行各种测试
"""

import os
import sys
import subprocess

def print_menu():
    """显示测试菜单"""
    print("🧪 食品服务公司管理系统 - 测试菜单")
    print("=" * 50)
    print()
    print("请选择要运行的测试:")
    print("1. 最终版本测试 (推荐)")
    print("2. 登录界面演示")
    print("3. 紧凑布局演示")
    print("4. 调试模式测试")
    print("5. 按钮功能测试")
    print("6. 运行主程序")
    print("0. 退出")
    print()

def run_test(choice):
    """运行选择的测试"""
    tests = {
        "1": "test\\final_test.py",
        "2": "test\\demo_login.py",
        "3": "test\\compact_login_demo.py",
        "4": "test\\debug_login.py", 
        "5": "test\\test_buttons.py",
        "6": "main.py"
    }
    
    if choice in tests:
        print(f"🚀 正在运行: {tests[choice]}")
        print("-" * 30)
        try:
            subprocess.run([sys.executable, tests[choice]], check=True)
        except subprocess.CalledProcessError as e:
            print(f"❌ 运行失败: {e}")
        except KeyboardInterrupt:
            print("⚠️ 用户中断")
        except Exception as e:
            print(f"❌ 运行错误: {e}")
    else:
        print("❌ 无效选择")

def main():
    """主函数"""
    # 确保在项目根目录运行
    project_root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_root)
    
    while True:
        print_menu()
        try:
            choice = input("请输入选择 (0-6): ").strip()
            
            if choice == "0":
                print("👋 再见!")
                break
            elif choice in ["1", "2", "3", "4", "5", "6"]:
                run_test(choice)
                print()
                input("按回车键继续...")
                print("\n" * 2)
            else:
                print("❌ 请输入有效数字 (0-6)")
                print()
                
        except KeyboardInterrupt:
            print("\n👋 再见!")
            break
        except Exception as e:
            print(f"❌ 错误: {e}")

if __name__ == "__main__":
    main()
