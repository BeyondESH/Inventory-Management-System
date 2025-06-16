#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试system_launcher.py修复效果
"""

import sys
import os

# 添加src路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_system_launcher_import():
    """测试system_launcher模块导入"""
    print("🧪 测试SystemLauncher导入和基本功能...")
    
    try:
        from system_launcher import SystemLauncher
        print("✅ SystemLauncher导入成功")
        
        # 测试创建实例
        launcher = SystemLauncher()
        print("✅ SystemLauncher实例创建成功")
        
        # 检查方法是否存在
        if hasattr(launcher, 'start_main_system'):
            print("✅ start_main_system方法存在")
        else:
            print("❌ start_main_system方法不存在")
        
        if hasattr(launcher, 'run'):
            print("✅ run方法存在")
        else:
            print("❌ run方法不存在")
        
        print("✅ SystemLauncher所有基本功能正常")
        
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
    except Exception as e:
        print(f"❌ 其他错误: {e}")
    
    print("\n🏁 测试完成")

if __name__ == "__main__":
    test_system_launcher_import()
