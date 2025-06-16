#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
客户管理模块测试脚本
"""

import sys
import os
import tkinter as tk

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.customer_module import CustomerModule

def test_customer_module():
    """测试客户管理模块"""
    print("=== 客户管理模块测试 ===")
    
    # 创建主窗口
    root = tk.Tk()
    root.title("客户管理模块测试")
    root.geometry("1000x700")
    root.configure(bg="#ffffff")
    
    # 创建标题框架
    title_frame = tk.Frame(root, bg="#ffffff", height=80)
    title_frame.pack(fill="x")
    title_frame.pack_propagate(False)
    
    # 创建内容框架
    content_frame = tk.Frame(root, bg="#ffffff")
    content_frame.pack(fill="both", expand=True)
    
    # 创建客户管理模块实例
    customer_module = CustomerModule(content_frame, title_frame)
    
    # 显示客户管理模块
    customer_module.show()
    
    print("\n测试功能说明：")
    print("1. ➕ 添加客户 - 点击添加新客户，填写客户信息")
    print("   - 支持客户姓名、电话、邮箱、地址、客户类型输入")
    print("   - 电话和邮箱格式验证")
    print("   - 重复客户检查")
    
    print("\n2. 🔧 修改客户 - 单击选择客户后启用此按钮")
    print("   - 点击客户行选择客户")
    print("   - 状态栏会显示选中的客户信息")
    print("   - '修改客户'按钮变为可用状态")
    
    print("\n3. ✏️ 编辑客户 - 双击客户行或使用修改按钮")
    print("   - 支持修改所有客户信息")
    print("   - 包含删除客户功能")
    print("   - 数据验证和重复检查")
    
    print("\n4. 客户类型分类：")
    print("   - 个人客户：普通个人用户")
    print("   - 企业客户：企业或组织客户")
    print("   - VIP客户：优质客户")
    
    print("\n5. 数据验证功能：")
    print("   - 手机号码：验证11位数字，1开头")
    print("   - 邮箱格式：标准邮箱格式验证")
    print("   - 唯一性检查：防止重复电话和邮箱")
    
    print("\n窗口已打开，请在界面中测试各项功能...")
    print("关闭窗口结束测试")
    
    # 启动GUI事件循环
    root.mainloop()
    
    print("客户管理模块测试完成")

def test_customer_data_operations():
    """测试客户数据操作"""
    print("\n=== 客户数据操作测试 ===")
    
    # 创建一个简单的测试实例
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    
    title_frame = tk.Frame(root)
    content_frame = tk.Frame(root)
    
    customer_module = CustomerModule(content_frame, title_frame)
    
    # 测试初始数据
    print(f"初始客户数量: {len(customer_module.customer_data)}")
    
    # 显示所有客户信息
    print("\n初始客户信息:")
    for i, customer in enumerate(customer_module.customer_data, 1):
        print(f"{i}. ID:{customer['id']} | 姓名:{customer['name']} | 电话:{customer['phone']} | 类型:{customer['type']}")
    
    # 测试添加新客户数据
    new_customer = {
        "id": 6,
        "name": "测试客户",
        "phone": "13912345678",
        "email": "test@example.com",
        "address": "测试地址123号",
        "type": "个人客户"
    }
    
    customer_module.customer_data.append(new_customer)
    print(f"\n添加测试客户后数量: {len(customer_module.customer_data)}")
    
    # 测试客户类型统计
    type_count = {}
    for customer in customer_module.customer_data:
        customer_type = customer['type']
        type_count[customer_type] = type_count.get(customer_type, 0) + 1
    
    print("\n客户类型统计:")
    for customer_type, count in type_count.items():
        print(f"  {customer_type}: {count}人")
    
    root.destroy()
    print("数据操作测试完成")

if __name__ == "__main__":
    try:
        # 首先进行数据操作测试
        test_customer_data_operations()
        
        # 然后进行UI测试
        test_customer_module()
        
    except Exception as e:
        print(f"测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
