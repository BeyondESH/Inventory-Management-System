# 食品服务公司管理系统

一个基于Python Tkinter的食品服务公司综合管理系统，包含用户登录注册、库存管理、餐食配置、订单管理、客户信息管理和财务管理等功能模块。

## 项目结构

```
Inventory-Management-System/
├── main.py                 # 主启动文件
├── requirements.txt        # 项目依赖
├── README.md              # 项目说明
├── src/                   # 源代码目录
│   ├── system_launcher.py  # 系统启动器
│   ├── login_module.py     # 登录注册模块
│   ├── user_manager.py     # 用户管理类
│   ├── inventory_system.py # 主系统界面
│   ├── inventory_module.py # 库存管理模块
│   ├── meal_module.py      # 餐食配置模块
│   ├── order_module.py     # 订单管理模块
│   ├── customer_module.py  # 客户信息管理模块
│   └── finance_module.py   # 财务管理模块
├── data/                  # 数据文件目录
│   └── users.json         # 用户数据
├── config/                # 配置文件目录
│   └── settings.json      # 系统配置
├── docs/                  # 文档目录
│   ├── README.md          # 详细文档
│   ├── MODULE_ARCHITECTURE.md # 模块架构说明
│   ├── MANAGEMENT_SYSTEM_README.md # 管理系统说明
│   └── QUICK_START.md     # 快速开始指南
└── image/                 # 图片资源目录
    ├── icon/              # 图标文件
    ├── png/               # PNG图片
    └── svg/               # SVG图片
```

## 快速开始

### 1. 环境要求
- Python 3.6+
- Tkinter (通常随Python安装)

### 2. 运行系统
从项目根目录运行：
```bash
python main.py
```

或者从src目录运行：
```bash
cd src
python system_launcher.py
```

### 3. 登录系统
- 使用默认管理员账户：admin / admin@company.com
- 或者注册新用户
- 支持游客模式快速体验

## 功能模块

### 用户系统
- 用户注册登录
- 密码重置
- 游客模式
- 用户信息管理

### 业务模块
1. **库存管理** - 商品库存的增删改查
2. **餐食配置** - 餐食菜单和配置管理
3. **订单管理** - 订单创建、处理和跟踪
4. **客户信息管理** - 客户资料维护
5. **财务管理** - 财务数据统计和分析

## 开发说明

项目采用模块化设计，每个业务功能都是独立的类和文件，便于维护和扩展。

- `src/` - 所有Python源代码
- `data/` - 数据存储文件
- `config/` - 配置文件
- `docs/` - 项目文档
- `image/` - 界面图标和图片资源

## 许可证

MIT License
