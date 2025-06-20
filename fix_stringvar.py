#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速修复StringVar初始化问题
将所有模块初始化时的StringVar改为延迟初始化
"""

import os
import re

def fix_stringvar_in_file(file_path):
    """修复文件中的StringVar初始化问题"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 在__init__方法中找到StringVar初始化并注释掉
        # 模式：查找类似 self.xxx_var = tk.StringVar(value="xxx") 的行
        pattern = r'(\s+)(self\.\w+_var\s*=\s*tk\.StringVar\(value=.*?\))'
        
        def replace_func(match):
            indent = match.group(1)
            assignment = match.group(2)
            var_name = assignment.split('=')[0].strip()
            return f"{indent}# {assignment}  # 延迟初始化\n{indent}{var_name} = None"
        
        new_content = re.sub(pattern, replace_func, content)
        
        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"✓ 修复了 {file_path}")
            return True
        else:
            print(f"- 无需修复 {file_path}")
            return False
            
    except Exception as e:
        print(f"✗ 修复失败 {file_path}: {e}")
        return False

def main():
    """主函数"""
    print("🔧 开始修复StringVar初始化问题...")
    
    # 需要修复的模块文件
    module_files = [
        "modern_system/modules/modern_meal_module.py",
        "modern_system/modules/modern_inventory_module.py",
        "modern_system/modules/modern_employee_module.py",
        "modern_system/modules/modern_order_module.py",
        "modern_system/modules/modern_customer_module.py",
        "modern_system/modules/modern_finance_module.py"
    ]
    
    fixed_count = 0
    for file_path in module_files:
        if os.path.exists(file_path):
            if fix_stringvar_in_file(file_path):
                fixed_count += 1
        else:
            print(f"⚠️ 文件不存在: {file_path}")
    
    print(f"\n🎉 修复完成！共修复了 {fixed_count} 个文件")

if __name__ == "__main__":
    main()
