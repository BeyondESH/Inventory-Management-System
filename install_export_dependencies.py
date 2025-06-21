#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
导出功能依赖库安装脚本
用于安装导出Excel、CSV、PDF功能所需的第三方库
"""

import subprocess
import sys
import os

def install_package(package):
    """安装Python包"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ 成功安装 {package}")
        return True
    except subprocess.CalledProcessError:
        print(f"❌ 安装 {package} 失败")
        return False

def main():
    """主函数"""
    print("=" * 50)
    print("智慧餐饮管理系统 - 导出功能依赖库安装")
    print("=" * 50)
    
    # 需要安装的包列表
    packages = [
        "openpyxl",      # Excel文件处理
        "reportlab",     # PDF文件生成
        "Pillow",        # 图像处理（reportlab依赖）
    ]
    
    print("正在安装导出功能所需的依赖库...")
    print()
    
    success_count = 0
    total_count = len(packages)
    
    for package in packages:
        print(f"正在安装 {package}...")
        if install_package(package):
            success_count += 1
        print()
    
    print("=" * 50)
    print(f"安装完成！成功安装 {success_count}/{total_count} 个包")
    
    if success_count == total_count:
        print("✅ 所有依赖库安装成功，导出功能已可用！")
        print()
        print("支持的导出格式：")
        print("  📊 Excel (.xlsx) - 支持样式和格式化")
        print("  📄 CSV (.csv) - 通用表格格式")
        print("  📋 PDF (.pdf) - 文档格式")
        print()
        print("各模块导出功能：")
        print("  💰 财务管理 - 收支记录、固定成本、财务概览")
        print("  📦 订单管理 - 订单列表（支持状态筛选）")
        print("  📦 库存管理 - 库存数据（支持类型筛选）")
        print("  👥 客户管理 - 客户信息（支持类型筛选）")
        print("  🍽️ 菜品管理 - 菜品数据（支持状态筛选）")
    else:
        print("⚠️ 部分依赖库安装失败，某些导出功能可能不可用")
        print("请手动安装失败的包：")
        for package in packages:
            print(f"  pip install {package}")
    
    print("=" * 50)
    
    # 等待用户按键
    input("按回车键退出...")

if __name__ == "__main__":
    main() 