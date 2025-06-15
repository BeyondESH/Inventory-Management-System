# 项目安装和构建指南

## 🛠️ 环境准备

### 1. 安装构建依赖
```bash
pip install setuptools wheel
```

### 2. 安装项目依赖
```bash
pip install -r requirements.txt
```

## 📦 项目安装

### 开发模式安装（推荐）
```bash
# 在项目根目录执行
pip install -e .
```
这种方式安装后，代码修改会立即生效，适合开发时使用。

### 正式安装
```bash
# 在项目根目录执行
pip install .
```

## 🚀 运行系统

### 方式1：使用命令行工具（推荐）
安装后可以直接使用命令：
```bash
inventory-system
```

### 方式2：直接运行Python文件
```bash
# 从项目根目录
python main.py

# 或从src目录
cd src
python system_launcher.py
```

## 📦 构建分发包

### 创建源码分发包
```bash
python setup.py sdist
```
生成的文件：`dist/inventory-management-system-2.0.0.tar.gz`

### 创建Wheel分发包
```bash
python setup.py bdist_wheel
```
生成的文件：`dist/inventory_management_system-2.0.0-py3-none-any.whl`

### 同时创建两种分发包
```bash
python setup.py sdist bdist_wheel
```

## 🔧 开发工具

### 检查项目信息
```bash
python setup.py --name           # 显示项目名称
python setup.py --version        # 显示版本号
python setup.py --description    # 显示描述
python setup.py --author         # 显示作者
```

### 验证setup.py配置
```bash
python setup.py check
```

### 清理构建文件
```bash
python setup.py clean --all
```

## 📂 生成的文件结构

运行构建命令后，会生成以下目录：
```
project/
├── build/              # 构建临时文件
├── dist/               # 分发包
├── *.egg-info/         # 包信息
└── __pycache__/        # Python缓存
```

## ⚠️ 常见问题

### 1. setuptools未安装
```
ModuleNotFoundError: No module named 'setuptools'
```
解决：`pip install setuptools`

### 2. 权限问题
如果安装时出现权限错误，可以：
```bash
pip install --user .    # 安装到用户目录
```

### 3. 虚拟环境推荐
建议在虚拟环境中开发：
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

## 🎯 最佳实践

1. **开发时**：使用 `pip install -e .` 进行可编辑安装
2. **分发时**：使用 `python setup.py sdist bdist_wheel` 创建分发包
3. **部署时**：使用 `pip install package_name.whl` 安装wheel包

## 📋 版本更新流程

1. 修改 `setup.py` 中的 `version`
2. 更新 `README.md` 和文档
3. 运行测试确保功能正常
4. 构建新的分发包
5. 分发或上传到PyPI
