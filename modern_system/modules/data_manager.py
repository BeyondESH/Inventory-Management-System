#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据管理中心
负责各模块间的数据联动和统一管理
使用SQLite数据库替代JSON文件存储
"""

import json
import os
import datetime
from typing import Dict, List, Any, Optional
from threading import Lock

# 导入数据库管理器
try:
    from .database_manager import database_manager
except ImportError:
    try:
        from database_manager import database_manager
    except ImportError:
        print("❌ 无法导入数据库管理器，将使用JSON文件存储")
        database_manager = None

class DataManager:
    def __init__(self):
        self.data_lock = Lock()
        self.modules = {}
        self.data_path = os.path.join(os.path.dirname(__file__), '..', 'data')
        self.ensure_data_directory()
        
        # 检查是否使用数据库
        self.use_database = database_manager is not None
        
        if self.use_database:
            print("✅ 使用SQLite数据库存储")
        else:
            print("⚠️ 使用JSON文件存储（数据库不可用）")
            # 数据存储（JSON模式）
            self.orders = self.load_orders()
            self.inventory = self.load_inventory()
            self.customers = self.load_customers()
            self.meals = self.load_meals()
            self.employees = self.load_employees()
            self.financial_records = self.load_financial_records()
        
        # 统计数据缓存
        self.dashboard_stats = {
            'today_sales': 0,
            'order_count': 0,
            'low_stock_count': 0,
            'customer_count': 0,
            'last_update': None
        }
        
    def ensure_data_directory(self):
        """确保数据目录存在"""
        if not os.path.exists(self.data_path):
            os.makedirs(self.data_path)
    
    def register_module(self, module_type: str, instance):
        """注册模块实例"""
        self.modules[module_type] = instance
        
    def get_module(self, module_type: str):
        """获取模块实例"""
        return self.modules.get(module_type)
    
    def load_data(self, data_type: str):
        """通用数据加载方法"""
        if self.use_database:
            # 数据库模式
            if data_type == 'meals':
                return database_manager.get_meals()
            elif data_type == 'inventory':
                return database_manager.get_inventory()
            elif data_type == 'orders':
                return database_manager.get_orders()
            elif data_type == 'customers':
                return database_manager.get_customers()
            elif data_type == 'employees':
                return database_manager.get_employees()
            elif data_type == 'finance':
                return database_manager.get_financial_records()
            else:
                print(f"未知的数据类型: {data_type}")
                return []
        else:
            # JSON文件模式
            if data_type == 'meals':
                return self.load_meals()
            elif data_type == 'inventory':
                return self.load_inventory()
            elif data_type == 'orders':
                return self.load_orders()
            elif data_type == 'customers':
                return self.load_customers()
            elif data_type == 'employees':
                return self.load_employees()
            elif data_type == 'finance':
                return self.load_financial_records()
            else:
                print(f"未知的数据类型: {data_type}")
                return []
    
    # ==================== 订单管理 ====================
    def load_orders(self) -> List[Dict]:
        """加载订单数据（JSON模式）"""
        if self.use_database:
            return database_manager.get_orders()
        
        try:
            orders_file = os.path.join(self.data_path, 'orders.json')
            if os.path.exists(orders_file):
                with open(orders_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"加载订单数据失败: {e}")
        return self.get_default_orders()
    
    def save_orders(self):
        """保存订单数据（JSON模式）"""
        if self.use_database:
            return  # 数据库模式不需要手动保存
        
        try:
            orders_file = os.path.join(self.data_path, 'orders.json')
            with open(orders_file, 'w', encoding='utf-8') as f:
                json.dump(self.orders, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存订单数据失败: {e}")
    
    def add_order(self, order_data: Dict) -> int:
        """添加新订单并处理库存扣减 (数据库模式)"""
        if not self.use_database:
            # 此处可以保留或移除JSON模式的逻辑
            raise NotImplementedError("JSON模式下的订单创建已废弃")

        try:
            # 直接将订单数据传递给database_manager
            # database_manager现在负责事务、库存检查和扣减
            order_id = database_manager.create_order(order_data)
            
            # 通知模块（如果需要）
            self.notify_modules('order_added', {'order_id': order_id})
            
            return order_id
        except Exception as e:
            # 将数据库层的异常继续向上抛出，以便UI层可以捕获并显示给用户
            print(f"❌ DataManager创建订单失败: {e}")
            raise e
    
    def create_order(self, order_data: Dict) -> str:
        """创建新订单（add_order的别名）"""
        return self.add_order(order_data)
    
    def update_order_status(self, order_id: str, new_status: str) -> bool:
        """更新订单状态"""
        if self.use_database:
            # 数据库模式
            try:
                return database_manager.update_order_status(int(order_id), new_status)
            except Exception as e:
                print(f"❌ 数据库更新订单状态失败: {e}")
                return False
        
        # JSON文件模式
        with self.data_lock:
            for order in self.orders:
                if order['id'] == order_id:
                    old_status = order['status']
                    order['status'] = new_status
                    order['update_time'] = datetime.datetime.now().isoformat()
                    
                    # 如果订单被取消，恢复库存
                    if new_status == '已取消' and old_status != '已取消':
                        self.restore_inventory(order.get('items', []))
                        # 添加退款记录
                        self.add_financial_record({
                            'type': 'refund',
                            'category': '订单退款',
                            'amount': order.get('total_amount', 0),
                            'description': f"订单退款 - {order_id}",
                            'order_id': order_id
                        })
                    
                    self.save_orders()
                    self.update_dashboard_stats()
                    self.notify_modules('order_updated', order)
                    return True
            return False
    
    def get_orders(self, status_filter: Optional[str] = None) -> List[Dict]:
        """获取订单列表"""
        if self.use_database:
            return database_manager.get_orders(status_filter)
        
        if status_filter:
            return [order for order in self.orders if order.get('status') == status_filter]
        return self.orders.copy()
    
    # ==================== 库存管理 ====================
    def load_inventory(self) -> List[Dict]:
        """加载库存数据（JSON模式）"""
        if self.use_database:
            return database_manager.get_inventory()
        
        try:
            inventory_file = os.path.join(self.data_path, 'inventory.json')
            if os.path.exists(inventory_file):
                with open(inventory_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"加载库存数据失败: {e}")
        return self.get_default_inventory()
    
    def save_inventory(self):
        """保存库存数据（JSON模式）"""
        if self.use_database:
            return  # 数据库模式不需要手动保存
        
        try:
            inventory_file = os.path.join(self.data_path, 'inventory.json')
            with open(inventory_file, 'w', encoding='utf-8') as f:
                json.dump(self.inventory, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存库存数据失败: {e}")
    
    @property
    def inventory(self):
        """获取库存数据"""
        if self.use_database:
            return database_manager.get_inventory()
        return self._inventory if hasattr(self, '_inventory') else []
    
    @inventory.setter
    def inventory(self, value):
        """设置库存数据（JSON模式）"""
        if not self.use_database:
            self._inventory = value
    
    def check_and_reduce_inventory(self, order_items: List[Dict]) -> bool:
        """检查库存并扣减"""
        if self.use_database:
            # 数据库模式 - 这里需要根据餐食ID来扣减库存
            # 暂时返回True，实际扣减在create_order中处理
            return True
        
        # JSON文件模式
        print(f"开始检查库存，订单项目: {order_items}")
        
        # 先检查库存是否充足
        for item in order_items:
            product_id = item.get('product_id')
            quantity = item.get('quantity', 0)
            
            print(f"检查库存: {product_id}, 数量: {quantity}")
            
            inventory_item = self.find_inventory_item(product_id)
            if inventory_item:
                current_stock = inventory_item.get('stock', 0)
                print(f"找到库存项目: {inventory_item['name']}, 当前库存: {current_stock}")
                if current_stock < quantity:
                    print(f"库存不足: 需要{quantity}, 只有{current_stock}")
                    return False
            else:
                print(f"未找到库存项目: {product_id}, 跳过库存检查")
                # 对于堂食菜品，如果没有对应的库存项目，可以允许下单
                # 这是因为有些菜品可能不需要库存管理（如现做菜品）
                continue
        
        # 库存充足，执行扣减
        for item in order_items:
            product_id = item.get('product_id')
            quantity = item.get('quantity', 0)
            
            inventory_item = self.find_inventory_item(product_id)
            if inventory_item:
                old_stock = inventory_item['stock']
                inventory_item['stock'] -= quantity
                inventory_item['last_update'] = datetime.datetime.now().isoformat()
                print(f"库存扣减: {inventory_item['name']}, {old_stock} -> {inventory_item['stock']}")
        
        self.save_inventory()
        print("库存检查和扣减完成")
        return True
    
    def restore_inventory(self, order_items: List[Dict]):
        """恢复库存（订单取消时）"""
        if self.use_database:
            # 数据库模式 - 暂时不处理
            return
        
        # JSON文件模式
        for item in order_items:
            product_id = item.get('product_id')
            quantity = item.get('quantity', 0)
            
            inventory_item = self.find_inventory_item(product_id)
            if inventory_item:
                inventory_item['stock'] += quantity
                inventory_item['last_update'] = datetime.datetime.now().isoformat()
        
        self.save_inventory()
    
    def find_inventory_item(self, product_id: str) -> Optional[Dict]:
        """查找库存项目"""
        if not product_id:
            return None
            
        # 尝试多种匹配方式
        for item in self.inventory:
            # 精确匹配ID
            if item.get('id') == product_id:
                return item
            # 精确匹配名称
            if item.get('name') == product_id:
                return item
        
        # 模糊匹配（包含关系）
        for item in self.inventory:
            item_name = item.get('name', '').lower()
            if product_id.lower() in item_name:
                return item
        
        return None
    
    def get_low_stock_items(self, threshold: int = 10) -> List[Dict]:
        """获取低库存项目"""
        if self.use_database:
            return database_manager.get_low_stock_items(threshold)
        
        return [item for item in self.inventory if item.get('stock', 0) <= threshold]
    
    # ==================== 财务管理 ====================
    def load_financial_records(self) -> List[Dict]:
        """加载财务记录（JSON模式）"""
        if self.use_database:
            return database_manager.get_financial_records()
        
        try:
            finance_file = os.path.join(self.data_path, 'finance.json')
            if os.path.exists(finance_file):
                with open(finance_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"加载财务记录失败: {e}")
        return []
    
    def save_financial_records(self):
        """保存财务记录（JSON模式）"""
        if self.use_database:
            return  # 数据库模式不需要手动保存
        
        try:
            finance_file = os.path.join(self.data_path, 'finance.json')
            with open(finance_file, 'w', encoding='utf-8') as f:
                json.dump(self.financial_records, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存财务记录失败: {e}")
    
    def add_financial_record(self, record_data: Dict) -> str:
        """添加财务记录"""
        if self.use_database:
            # 数据库模式 - 财务记录在创建订单时自动添加
            return "DB_RECORD"
        
        # JSON文件模式
        record_id = f"FIN{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
        record_data['id'] = record_id
        record_data['create_time'] = datetime.datetime.now().isoformat()
        
        self.financial_records.append(record_data)
        self.save_financial_records()
        
        return record_id
    
    def get_financial_records(self, time_range: str = '全部', record_type: str = '全部') -> List[Dict]:
        """获取财务记录"""
        if self.use_database:
            return database_manager.get_financial_records(time_range, record_type)
        
        if record_type:
            return [record for record in self.financial_records if record.get('type') == record_type]
        return self.financial_records.copy()
    
    def update_dashboard_stats(self):
        """更新仪表盘统计数据"""
        if self.use_database:
            self.dashboard_stats = database_manager.get_dashboard_stats()
            return
        
        # JSON文件模式
        today = datetime.datetime.now().date()
        today_sales = 0
        order_count = 0
        
        # 计算今日销售额和订单数
        for order in self.orders:
            order_date = datetime.datetime.fromisoformat(order.get('create_time', '')).date()
            if order_date == today:
                order_count += 1
                today_sales += order.get('total_amount', 0)
        
        # 计算低库存项目数
        low_stock_count = len(self.get_low_stock_items())
        
        # 计算客户总数
        customer_count = len(self.customers)
        
        self.dashboard_stats = {
            'today_sales': today_sales,
            'order_count': order_count,
            'low_stock_count': low_stock_count,
            'customer_count': customer_count,
            'last_update': datetime.datetime.now().isoformat()
        }
    
    def get_dashboard_stats(self) -> Dict:
        """获取仪表盘统计数据"""
        if self.use_database:
            return database_manager.get_dashboard_stats()
        
        return self.dashboard_stats
    
    # ==================== 客户管理 ====================
    def load_customers(self) -> List[Dict]:
        """加载客户数据（JSON模式）"""
        if self.use_database:
            return database_manager.get_customers()
        
        try:
            customers_file = os.path.join(self.data_path, 'customers.json')
            if os.path.exists(customers_file):
                with open(customers_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"加载客户数据失败: {e}")
        return self.get_default_customers()
    
    def get_customers(self) -> List[Dict]:
        """获取客户列表"""
        if self.use_database:
            return database_manager.get_customers()
        return self.load_data('customers')
    
    def add_customer(self, data: Dict) -> int:
        """添加新客户"""
        if self.use_database:
            return database_manager.add_customer(data)
        raise NotImplementedError("JSON模式下不支持此操作")
    
    def update_customer(self, customer_id: int, data: Dict):
        """更新客户信息"""
        if self.use_database:
            return database_manager.update_customer(customer_id, data)
        raise NotImplementedError("JSON模式下不支持此操作")
    
    def delete_customer(self, customer_id: int):
        """删除客户"""
        if self.use_database:
            return database_manager.delete_customer(customer_id)
        raise NotImplementedError("JSON模式下不支持此操作")
    
    def save_customers(self):
        """保存客户数据（JSON模式）"""
        if self.use_database:
            return  # 数据库模式不需要手动保存
        
        try:
            customers_file = os.path.join(self.data_path, 'customers.json')
            with open(customers_file, 'w', encoding='utf-8') as f:
                json.dump(self.customers, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存客户数据失败: {e}")
    
    # ==================== 餐食管理 ====================
    def load_meals(self) -> List[Dict]:
        """加载餐食数据（JSON模式）"""
        if self.use_database:
            return database_manager.get_meals()
        
        try:
            meals_file = os.path.join(self.data_path, 'meals.json')
            if os.path.exists(meals_file):
                with open(meals_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"加载餐食数据失败: {e}")
        return self.get_default_meals()
    
    # ==================== 员工管理 ====================
    def load_employees(self) -> List[Dict]:
        """加载员工数据（JSON模式）"""
        if self.use_database:
            return database_manager.get_employees()
        
        try:
            employees_file = os.path.join(self.data_path, 'employees.json')
            if os.path.exists(employees_file):
                with open(employees_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"加载员工数据失败: {e}")
        return self.get_default_employees()
    
    def get_employees(self) -> List[Dict]:
        if self.use_database:
            return database_manager.get_employees()
        return []

    def add_employee(self, data: Dict):
        if self.use_database:
            return database_manager.add_employee(data)
        raise NotImplementedError("JSON模式下不支持此操作")

    def update_employee(self, employee_id: int, data: Dict):
        if self.use_database:
            return database_manager.update_employee(employee_id, data)
        raise NotImplementedError("JSON模式下不支持此操作")

    def delete_employee(self, employee_id: int):
        """逻辑删除"""
        if self.use_database:
            return database_manager.delete_employee(employee_id)
        raise NotImplementedError("JSON模式下不支持此操作")
    
    # ==================== 模块通知 ====================
    def notify_modules(self, event_type: str, data: Any):
        """通知相关模块"""
        for module_type, module_instance in self.modules.items():
            self._safe_notify_module(module_instance, event_type, data)
    
    def _safe_notify_module(self, module_instance, event_type: str, data: Any):
        """安全地通知模块"""
        try:
            if hasattr(module_instance, 'on_data_changed'):
                module_instance.on_data_changed(event_type, data)
        except Exception as e:
            print(f"通知模块 {type(module_instance).__name__} 失败: {e}")
    
    # ==================== 默认数据 ====================
    def get_default_orders(self) -> List[Dict]:
        """获取默认订单数据"""
        return []
    
    def get_default_inventory(self) -> List[Dict]:
        """获取默认库存数据"""
        return [
            {"id": "ING001", "name": "大米", "stock": 100, "unit": "kg", "price": 5.5},
            {"id": "ING002", "name": "鸡胸肉", "stock": 50, "unit": "kg", "price": 18.0},
            {"id": "ING003", "name": "牛肉", "stock": 30, "unit": "kg", "price": 35.0},
            {"id": "ING004", "name": "三文鱼", "stock": 15, "unit": "kg", "price": 45.0},
            {"id": "ING005", "name": "西兰花", "stock": 25, "unit": "kg", "price": 8.0},
            {"id": "ING006", "name": "胡萝卜", "stock": 20, "unit": "kg", "price": 4.0},
            {"id": "ING007", "name": "洋葱", "stock": 30, "unit": "kg", "price": 3.5},
            {"id": "ING008", "name": "大蒜", "stock": 10, "unit": "kg", "price": 12.0},
            {"id": "ING009", "name": "生抽", "stock": 20, "unit": "瓶", "price": 8.5},
            {"id": "ING010", "name": "香油", "stock": 15, "unit": "瓶", "price": 15.0}
        ]
    
    def get_default_customers(self) -> List[Dict]:
        """获取默认客户数据"""
        return []
    
    def get_default_meals(self) -> List[Dict]:
        """获取默认餐食数据"""
        return [
            {"id": "MEAL001", "name": "经典牛肉饭", "category": "面食", "price": 25.0, "image": "🍜"},
            {"id": "MEAL002", "name": "鸡蛋炒饭", "category": "炒饭", "price": 18.0, "image": "🍚"},
            {"id": "MEAL003", "name": "牛肉汉堡", "category": "西餐", "price": 32.0, "image": "🍔"},
            {"id": "MEAL004", "name": "薯条", "category": "小食", "price": 12.0, "image": "🍟"},
            {"id": "MEAL005", "name": "可乐", "category": "饮料", "price": 8.0, "image": "🥤"},
            {"id": "MEAL006", "name": "咖啡", "category": "饮料", "price": 15.0, "image": "☕"}
        ]
    
    def get_default_employees(self) -> List[Dict]:
        """获取默认员工数据"""
        return []

    def get_inventory(self) -> List[Dict]:
        """获取库存列表"""
        if self.use_database:
            return database_manager.get_inventory()
        # JSON模式的逻辑可以保留或删除
        return self.load_inventory()

    def add_ingredient(self, data: Dict) -> int:
        """添加新的库存原材料"""
        if self.use_database:
            return database_manager.add_ingredient(data)
        raise NotImplementedError("JSON模式下不支持此操作")

    def update_ingredient(self, ingredient_id: int, data: Dict):
        """更新库存原材料"""
        if self.use_database:
            return database_manager.update_ingredient(ingredient_id, data)
        raise NotImplementedError("JSON模式下不支持此操作")

    def delete_ingredient(self, ingredient_id: int):
        """删除库存原材料"""
        if self.use_database:
            return database_manager.delete_ingredient(ingredient_id)
        raise NotImplementedError("JSON模式下不支持此操作")

    def get_recipes(self) -> List[Dict]:
        """获取所有菜品的配方"""
        if self.use_database:
            return database_manager.get_recipes()
        raise NotImplementedError("JSON模式下不支持此操作")

    def get_meals(self, active_only=False) -> List[Dict]:
        """获取菜品列表"""
        if self.use_database:
            return database_manager.get_meals(active_only)
        return self.load_data('meals') # 保留JSON模式的兼容

    def add_meal(self, data: Dict) -> int:
        """添加新菜品"""
        if self.use_database:
            return database_manager.add_meal(data)
        raise NotImplementedError("JSON模式下不支持此操作")

    def update_meal(self, meal_id: int, data: Dict):
        """更新菜品信息"""
        if self.use_database:
            return database_manager.update_meal(meal_id, data)
        raise NotImplementedError("JSON模式下不支持此操作")

    def delete_meal(self, meal_id: int):
        """删除菜品"""
        if self.use_database:
            return database_manager.delete_meal(meal_id)
        raise NotImplementedError("JSON模式下不支持此操作")
        
    def update_meal_recipe(self, meal_id: int, ingredients: List[Dict]):
        """更新菜品配方"""
        if self.use_database:
            return database_manager.update_meal_recipe(meal_id, ingredients)
        raise NotImplementedError("JSON模式下不支持此操作")

    def get_fixed_costs(self) -> List[Dict]:
        if self.use_database:
            return database_manager.get_fixed_costs()
        return self.load_data('fixed_costs') # 假设JSON模式

    def add_fixed_cost(self, data: Dict):
        if self.use_database:
            return database_manager.add_fixed_cost(data)
        raise NotImplementedError("JSON模式下不支持此操作")

    def update_fixed_cost(self, cost_id: int, data: Dict):
        if self.use_database:
            return database_manager.update_fixed_cost(cost_id, data)
        raise NotImplementedError("JSON模式下不支持此操作")

    def delete_fixed_cost(self, cost_id: int):
        if self.use_database:
            return database_manager.delete_fixed_cost(cost_id)
        raise NotImplementedError("JSON模式下不支持此操作")
        
    def get_finance_summary(self) -> Dict:
        if self.use_database:
            return database_manager.get_finance_summary()
        return {} # JSON模式未实现

# 创建全局数据管理器实例
data_manager = DataManager()
