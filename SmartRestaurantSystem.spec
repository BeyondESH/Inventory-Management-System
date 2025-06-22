# -*- mode: python ; coding: utf-8 -*-

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
