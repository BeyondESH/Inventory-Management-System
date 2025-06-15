#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
食品服务公司管理系统主启动文件
项目入口点
"""

import sys
import os


current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)


from src.system_launcher import SystemLauncher

def main():
    """主函数，启动系统"""
    print("正在启动食品服务公司管理系统...")
    launcher = SystemLauncher()
    launcher.run()

if __name__ == "__main__":
    main()
