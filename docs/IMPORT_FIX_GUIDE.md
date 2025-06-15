# 导入问题修复说明

## 问题描述
main.py 文件出现 "无法解析导入system_launcher" 的 Pylance 错误。

## 解决方案

### 1. 修改了项目结构
- 在 `src/` 目录下添加了 `__init__.py` 文件，使其成为一个 Python 包
- 修改了 `main.py` 使用包导入方式：`from src.system_launcher import SystemLauncher`

### 2. 修复了相对导入
- 修改了 `src/` 目录中所有文件的导入方式，支持两种模式：
  - 作为包导入时使用相对导入（`from .module import Class`）
  - 直接运行时使用绝对导入（`from module import Class`）

### 3. 添加了IDE配置
- 创建了 `.vscode/settings.json` 配置文件，帮助 VS Code 正确识别 Python 路径
- 创建了 `pyrightconfig.json` 配置文件，优化类型检查

### 4. 运行方式
现在支持两种运行方式：

```bash
# 方式1：从项目根目录运行（推荐）
python main.py

# 方式2：从src目录运行
cd src
python system_launcher.py
```

### 5. 文件更改清单
- `main.py` - 修改导入方式
- `src/__init__.py` - 新增包初始化文件
- `src/system_launcher.py` - 修改导入方式，支持双模式
- `src/login_module.py` - 修改导入方式，支持双模式
- `src/inventory_system.py` - 修改导入方式，支持双模式
- `.vscode/settings.json` - 新增VS Code配置
- `pyrightconfig.json` - 新增类型检查配置

## 技术细节

使用了条件导入的方式：
```python
try:
    from .module import Class  # 包导入
except ImportError:
    from module import Class   # 直接导入
```

这样确保了无论是作为包使用还是直接运行都能正常工作。
