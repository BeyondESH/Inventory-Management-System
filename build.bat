@echo off
chcp 65001 >nul
echo.
echo ========================================
echo   智能餐厅管理系统 - 自动打包工具
echo ========================================
echo.

:: 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python未安装或未添加到PATH环境变量
    echo 请先安装Python 3.7+
    pause
    exit /b 1
)

echo ✓ Python已安装
python --version

:: 检查main.py是否存在
if not exist "main.py" (
    echo ❌ 未找到main.py文件
    echo 请确保在项目根目录运行此脚本
    pause
    exit /b 1
)

echo ✓ 项目文件检查通过

:: 运行打包脚本
echo.
echo 🚀 开始打包过程...
echo.
python build_exe.py

if errorlevel 1 (
    echo.
    echo ❌ 打包失败
    pause
    exit /b 1
)

echo.
echo ✅ 打包完成！
echo.
echo 生成的文件：
echo   📁 dist\SmartRestaurantSystem.exe
echo   📁 SmartRestaurantSystem_Portable\
echo.
echo 按任意键打开生成目录...
pause >nul

:: 打开dist目录
if exist "dist" (
    explorer "dist"
)

:: 打开便携版目录
if exist "SmartRestaurantSystem_Portable" (
    explorer "SmartRestaurantSystem_Portable"
)

echo.
echo 🎉 打包完成！您可以分发exe文件了。
pause
