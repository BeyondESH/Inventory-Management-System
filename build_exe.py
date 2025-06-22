#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Smart Restaurant Management System - EXE Builder
使用PyInstaller将项目打包为可执行文件
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def install_pyinstaller():
    """安装PyInstaller"""
    try:
        import PyInstaller
        print("✓ PyInstaller already installed")
        return True
    except ImportError:
        print("Installing PyInstaller...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print("✓ PyInstaller installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to install PyInstaller: {e}")
            return False

def create_spec_file():
    """创建PyInstaller规格文件"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

import os
import sys
from pathlib import Path

# 获取项目根目录
project_root = os.getcwd()
modern_system_path = os.path.join(project_root, 'modern_system')

# 数据文件和目录
datas = [
    (os.path.join(modern_system_path, 'data'), 'modern_system/data'),
    (os.path.join(modern_system_path, 'modules'), 'modern_system/modules'),
    (os.path.join(modern_system_path, 'core'), 'modern_system/core'),
    (os.path.join(modern_system_path, 'ui'), 'modern_system/ui'),
    (os.path.join(modern_system_path, 'utils'), 'modern_system/utils'),
]

# 过滤存在的目录
filtered_datas = []
for src, dst in datas:
    if os.path.exists(src):
        filtered_datas.append((src, dst))
        print(f"Adding: {src} -> {dst}")
    else:
        print(f"Skipping missing: {src}")

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[project_root],
    binaries=[],
    datas=filtered_datas,
    hiddenimports=[
        'tkinter',
        'tkinter.ttk',
        'tkinter.messagebox',
        'tkinter.simpledialog',
        'json',
        'datetime',
        'threading',
        'sqlite3',
        'csv',
        'os',
        'sys',
        'typing',
        'pathlib',
        'modern_system.modules.data_manager',
        'modern_system.modules.modern_login_module',
        'modern_system.modules.modern_inventory_module',
        'modern_system.modules.modern_finance_module',
        'modern_system.modules.modern_sales_module',
        'modern_system.modules.modern_meal_module',
        'modern_system.modules.modern_customer_module',
        'modern_system.modules.modern_employee_module',
        'modern_system.modules.modern_order_module',
        'modern_system.core.modern_ui_system',
        'modern_system.core.system_launcher',
        'modern_system.core.user_manager',
        'modern_system.ui.meituan_charts_module',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'numpy',
        'pandas',
        'PIL',
        'cv2',
        'torch',
        'tensorflow',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='SmartRestaurantSystem',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # 设置为False隐藏控制台窗口
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # 可以添加图标文件路径
    version_info=None,
)
'''
    
    with open('SmartRestaurantSystem.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    print("✓ Created PyInstaller spec file: SmartRestaurantSystem.spec")

def build_exe():
    """构建可执行文件"""
    try:
        print("Building executable file...")
        
        # 运行PyInstaller
        cmd = [sys.executable, "-m", "PyInstaller", "--clean", "SmartRestaurantSystem.spec"]
        
        print(f"Running command: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✓ Build completed successfully!")
            print(f"Executable created at: dist/SmartRestaurantSystem.exe")
            
            # 检查文件是否存在
            exe_path = "dist/SmartRestaurantSystem.exe"
            if os.path.exists(exe_path):
                file_size = os.path.getsize(exe_path) / (1024 * 1024)  # MB
                print(f"✓ File size: {file_size:.1f} MB")
            
            return True
        else:
            print("✗ Build failed!")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False
            
    except Exception as e:
        print(f"✗ Build error: {e}")
        return False

def create_portable_package():
    """创建便携版包"""
    try:
        print("Creating portable package...")
        
        # 创建便携版目录
        portable_dir = "SmartRestaurantSystem_Portable"
        if os.path.exists(portable_dir):
            shutil.rmtree(portable_dir)
        os.makedirs(portable_dir)
        
        # 复制可执行文件
        if os.path.exists("dist/SmartRestaurantSystem.exe"):
            shutil.copy2("dist/SmartRestaurantSystem.exe", portable_dir)
            print("✓ Copied executable file")
        
        # 复制数据目录
        data_src = "modern_system/data"
        if os.path.exists(data_src):
            data_dst = os.path.join(portable_dir, "modern_system", "data")
            shutil.copytree(data_src, data_dst)
            print("✓ Copied data directory")
        
        # 创建启动脚本
        batch_content = '''@echo off
echo Smart Restaurant Management System
echo Starting application...
SmartRestaurantSystem.exe
pause
'''
        with open(os.path.join(portable_dir, "启动餐厅管理系统.bat"), 'w', encoding='gbk') as f:
            f.write(batch_content)
        
        # 创建说明文件
        readme_content = '''智能餐厅管理系统 - 便携版

系统特性：
- 现代化UI设计
- 菜品管理
- 库存管理
- 订单管理
- 财务管理
- 销售管理
- 员工管理
- 客户管理

使用方法：
1. 双击"启动餐厅管理系统.bat"启动程序
2. 或者直接运行"SmartRestaurantSystem.exe"

注意事项：
- 首次运行可能需要几秒钟启动时间
- 所有数据保存在modern_system/data目录中
- 建议定期备份data目录

版本：v2.0
构建时间：''' + str(Path(__file__).stat().st_mtime) + '''
'''
        
        with open(os.path.join(portable_dir, "使用说明.txt"), 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        print(f"✓ Portable package created: {portable_dir}/")
        return True
        
    except Exception as e:
        print(f"✗ Failed to create portable package: {e}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("Smart Restaurant Management System - EXE Builder")
    print("=" * 60)
    
    # 检查是否在正确的目录
    if not os.path.exists("main.py"):
        print("✗ main.py not found. Please run this script from the project root directory.")
        return False
    
    # 安装PyInstaller
    if not install_pyinstaller():
        return False
    
    # 创建规格文件
    create_spec_file()
    
    # 构建可执行文件
    if not build_exe():
        return False
    
    # 创建便携版包
    create_portable_package()
    
    print("\n" + "=" * 60)
    print("✓ Build process completed successfully!")
    print("Files created:")
    print("  - dist/SmartRestaurantSystem.exe (单文件版本)")
    print("  - SmartRestaurantSystem_Portable/ (便携版包)")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        input("Press Enter to exit...")
        sys.exit(1)
