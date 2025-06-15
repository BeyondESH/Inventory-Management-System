# 食品服务公司管理系统 - 模块化架构

## 项目结构

### 主文件
- `system_launcher.py` - 系统启动器，整合登录和主系统
- `inventory_system.py` - 主程序文件，负责界面框架和模块调度
- `main.py` - 备用主程序（如果存在）

### 核心模块文件
- `login_module.py` - 🔐 登录注册模块

### 业务模块文件
- `inventory_module.py` - 📦 库存管理模块
- `meal_module.py` - 🍜 餐食配置模块  
- `order_module.py` - 📋 订单管理模块
- `customer_module.py` - 👥 客户管理模块
- `finance_module.py` - 💰 财务管理模块

## 模块说明

### 0. 登录注册模块 (LoginModule)
**文件**: `login_module.py`
**功能**:
- 微信风格的登录界面设计
- 用户邮箱+密码登录验证
- 新用户注册功能
- 测试模式快速进入（无需登录）
- 密码加密存储和验证
- 记住密码和忘记密码功能

### 1. 库存管理模块 (InventoryModule)
**文件**: `inventory_module.py`
**功能**:
- 显示食材库存列表
- 库存状态监控（正常/库存不足）
- 支持添加和编辑库存项目
- 包含过期日期管理

### 2. 餐食配置模块 (MealModule)
**文件**: `meal_module.py`
**功能**:
- 卡片式餐食展示
- 餐食价格和描述管理
- 餐食启用/停用状态切换
- 支持添加和编辑餐食

### 3. 订单管理模块 (OrderModule)
**文件**: `order_module.py`
**功能**:
- 订单列表展示
- 订单状态追踪
- 支持新建和编辑订单
- 客户和餐食关联管理

### 4. 客户管理模块 (CustomerModule)
**文件**: `customer_module.py`
**功能**:
- 客户信息管理
- 联系方式维护
- 地址信息管理  
- 支持添加和编辑客户

### 5. 财务管理模块 (FinanceModule)
**文件**: `finance_module.py`
**功能**:
- 月度收入统计
- 固定成本和可变成本分析
- 利润计算和展示
- 可视化财务报表

## 架构特点

### 模块化设计
- 每个业务模块独立成文件
- 低耦合、高内聚的设计原则
- 便于维护和扩展

### 统一接口
- 所有模块都实现 `show()` 方法
- 统一的初始化参数 `(parent_frame, title_frame)`
- 一致的用户交互体验

### 数据封装
- 每个模块管理自己的数据
- 示例数据内置在各模块中
- 便于后续数据持久化改造

## 运行方式

```bash
# 推荐：使用系统启动器（包含登录功能）
python system_launcher.py

# 直接启动主系统（跳过登录）
python inventory_system.py

# 仅测试登录模块
python login_module.py
```

## 扩展方式

### 添加新模块
1. 创建新的模块文件 `new_module.py`
2. 实现类似其他模块的结构：
   ```python
   class NewModule:
       def __init__(self, parent_frame, title_frame):
           # 初始化
       
       def show(self):
           # 显示界面
   ```
3. 在 `inventory_system.py` 中导入并初始化新模块
4. 在导航栏中添加对应按钮

### 数据持久化
- 可以为每个模块添加数据库或文件存储
- 在各模块的 `__init__` 方法中加载数据
- 在相应操作中保存数据

## 技术栈
- **UI框架**: tkinter + ttk
- **语言**: Python 3.x
- **架构**: 模块化MVC模式
- **数据**: 当前使用内存数据，可扩展为数据库

## 开发团队
食品服务公司IT部门
