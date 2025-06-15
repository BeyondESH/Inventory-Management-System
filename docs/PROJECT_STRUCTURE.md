# 项目文件夹结构说明

## 文件夹组织

```
Inventory-Management-System/
├── src/                    # Python源代码文件
│   ├── system_launcher.py  # 系统启动器
│   ├── login_module.py     # 登录注册模块
│   ├── user_manager.py     # 用户管理类
│   ├── inventory_system.py # 主系统界面
│   ├── inventory_module.py # 库存管理模块
│   ├── meal_module.py      # 餐食配置模块
│   ├── order_module.py     # 订单管理模块
│   ├── customer_module.py  # 客户信息管理模块
│   └── finance_module.py   # 财务管理模块
├── docs/                   # 文档文件
│   ├── README.md           # 项目说明文档
│   ├── QUICK_START.md      # 快速开始指南
│   ├── MODULE_ARCHITECTURE.md # 模块架构说明
│   └── MANAGEMENT_SYSTEM_README.md # 管理系统详细说明
├── data/                   # 数据文件
│   └── users.json          # 用户数据
├── config/                 # 配置文件
│   └── settings.json       # 系统配置
├── image/                  # 图像资源
│   ├── icon/               # 图标文件
│   ├── png/                # PNG图片
│   └── svg/                # SVG矢量图
├── main.py                 # 主启动入口
├── requirements.txt        # Python依赖包
└── README.md               # 项目根目录说明
```

## 运行方式

### 方法1：从项目根目录运行
```bash
python main.py
```

### 方法2：从src目录运行
```bash
cd src
python system_launcher.py
```

## 文件夹说明

- **src/**: 存放所有Python源代码文件，模块化设计
- **docs/**: 存放所有Markdown文档和说明文件
- **data/**: 存放应用程序数据文件（如用户数据）
- **config/**: 存放配置文件
- **image/**: 存放所有图像资源文件

## 优势

1. **清晰的文件组织**: 不同类型的文件分类存放
2. **易于维护**: 代码、文档、数据分离
3. **模块化设计**: 每个功能模块独立文件
4. **便于扩展**: 新功能可以轻松添加到对应文件夹
