# 智能餐厅管理系统打包说明

## 自动打包（推荐）

1. 运行打包脚本：
```bash
python build_exe.py
```

该脚本会自动：
- 安装PyInstaller（如果未安装）
- 创建PyInstaller配置文件
- 打包生成exe文件
- 创建便携版包

## 手动打包

### 1. 安装PyInstaller
```bash
pip install pyinstaller
```

### 2. 基本打包命令
```bash
# 单文件打包（推荐）
pyinstaller --onefile --windowed --name="SmartRestaurantSystem" main.py

# 包含数据文件的打包
pyinstaller --onefile --windowed --name="SmartRestaurantSystem" \
    --add-data="modern_system/data;modern_system/data" \
    --add-data="modern_system/modules;modern_system/modules" \
    --add-data="modern_system/core;modern_system/core" \
    main.py
```

### 3. 高级打包选项
```bash
pyinstaller --onefile --windowed \
    --name="SmartRestaurantSystem" \
    --icon="icon.ico" \
    --add-data="modern_system;modern_system" \
    --hidden-import="tkinter" \
    --hidden-import="json" \
    --hidden-import="datetime" \
    --exclude-module="matplotlib" \
    --exclude-module="numpy" \
    main.py
```

## 打包参数说明

- `--onefile`: 打包成单个exe文件
- `--windowed`: 隐藏控制台窗口（GUI应用）
- `--name`: 指定生成的exe文件名
- `--icon`: 指定程序图标
- `--add-data`: 添加数据文件到打包中
- `--hidden-import`: 手动指定需要导入的模块
- `--exclude-module`: 排除不需要的模块以减小文件大小

## 常见问题解决

### 1. 模块导入错误
如果出现模块导入错误，添加隐藏导入：
```bash
--hidden-import="missing_module_name"
```

### 2. 数据文件缺失
确保添加所有需要的数据文件：
```bash
--add-data="source_path;destination_path"
```

### 3. 文件过大
排除不必要的模块：
```bash
--exclude-module="matplotlib"
--exclude-module="pandas"
--exclude-module="numpy"
```

### 4. 启动慢
使用UPX压缩（可选）：
```bash
--upx-dir="path_to_upx"
```

## 生成的文件

打包完成后会生成：
- `dist/SmartRestaurantSystem.exe` - 主程序文件
- `build/` - 临时构建文件（可删除）
- `SmartRestaurantSystem.spec` - PyInstaller配置文件

## 部署说明

1. 将`dist/SmartRestaurantSystem.exe`复制到目标机器
2. 确保目标机器有必要的运行时库（通常Windows 10+自带）
3. 首次启动可能需要几秒钟初始化时间
4. 数据文件会自动创建在程序同目录的`modern_system/data/`中

## 性能优化

1. 使用`--optimize=2`进行Python字节码优化
2. 添加`--strip`移除调试信息
3. 使用`--upx`压缩可执行文件（需要UPX工具）

## 注意事项

1. 杀毒软件可能误报，需要添加信任
2. 第一次启动较慢是正常现象
3. 建议在干净的虚拟环境中打包
4. 打包后的exe文件较大（通常50-100MB）是正常的
