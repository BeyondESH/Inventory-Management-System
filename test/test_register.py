#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试注册功能和用户信息存储
"""

import sys
import os
import json

# 添加src路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from user_manager import UserManager

def test_register_functionality():
    """测试注册功能"""
    print("🧪 测试用户注册功能...")
    
    # 创建用户管理器
    um = UserManager()
    
    # 测试注册前的用户数量
    initial_count = len(um.users)
    print(f"📊 注册前用户数量: {initial_count}")
    
    # 测试注册新用户
    test_username = "testuser001"
    test_email = "test001@example.com"
    test_password = "testpass123"
    
    print(f"📝 尝试注册用户: {test_username}")
    success, message = um.register_user(test_username, test_email, test_password)
    
    if success:
        print(f"✅ 注册成功: {message}")
        
        # 检查用户是否已添加到内存中
        if test_username in um.users:
            print("✅ 用户已添加到内存中")
            user = um.users[test_username]
            print(f"   用户名: {user.username}")
            print(f"   邮箱: {user.email}")
            print(f"   创建时间: {user.created_at}")
            print(f"   密码已哈希: {len(user.password_hash) == 64}")
        else:
            print("❌ 用户未添加到内存中")
        
        # 检查用户是否保存到文件中
        try:
            with open(um.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if test_username in data:
                    print("✅ 用户已保存到JSON文件中")
                    print(f"   文件路径: {um.data_file}")
                    print(f"   当前文件中用户数量: {len(data)}")
                else:
                    print("❌ 用户未保存到JSON文件中")
        except Exception as e:
            print(f"❌ 读取用户文件失败: {e}")
    else:
        print(f"❌ 注册失败: {message}")
    
    # 测试重复注册
    print(f"\n🔄 测试重复注册相同用户名...")
    success2, message2 = um.register_user(test_username, "other@example.com", "otherpass")
    if not success2:
        print(f"✅ 正确阻止重复注册: {message2}")
    else:
        print(f"❌ 应该阻止重复注册但没有: {message2}")
    
    # 测试重复邮箱
    print(f"\n📧 测试重复邮箱...")
    success3, message3 = um.register_user("anotheruser", test_email, "anotherpass")
    if not success3:
        print(f"✅ 正确阻止重复邮箱: {message3}")
    else:
        print(f"❌ 应该阻止重复邮箱但没有: {message3}")
    
    print("\n📋 当前所有用户:")
    for username, user in um.users.items():
        print(f"  - {username} ({user.email}) - 创建于 {user.created_at}")

if __name__ == "__main__":
    test_register_functionality()
