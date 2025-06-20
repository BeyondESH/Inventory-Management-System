#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
直接启动主界面 - 用于调试和测试
跳过登录界面，直接进入主系统
"""

import sys
import os

# 添加项目路径
current_dir = os.path.dirname(os.path.abspath(__file__))
modern_system_dir = os.path.join(current_dir, 'modern_system')
sys.path.insert(0, current_dir)
sys.path.insert(0, modern_system_dir)

def main():
    """直接启动主界面"""
    try:
        print("🚀 直接启动主界面...")
        
        # 导入主界面系统
        from modern_system.core.modern_ui_system import ModernFoodServiceSystem
        
        print("✓ 主界面系统导入成功")
        
        # 创建并启动主系统
        app = ModernFoodServiceSystem()
        print("✓ 主系统创建成功，正在启动...")
        
        app.run()
        
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        import traceback
        traceback.print_exc()
        
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
