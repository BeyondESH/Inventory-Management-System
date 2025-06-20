#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据管理中心 - 负责各模块间的数据同步和联动
实现订单、库存、财务等模块的数据交互
"""

import json
import os
import datetime
from typing import Dict, List, Any, Optional
from threading import Lock
import uuid

class DataManager:
    """数据管理中心单例类"""
    
    _instance = None
    _lock = Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if hasattr(self, '_initialized'):
            return
        
        self._initialized = True
        self.data_dir = self._get_data_dir()
        self.modules = {}
        self.registered_modules = {}  # 存储注册的模块实例
        self.event_listeners = {}
        
        # 初始化数据文件
        self.data_files = {
            'orders': 'orders.json',
            'inventory': 'inventory.json',
            'meals': 'meals.json',
            'customers': 'customers.json',
            'employees': 'employees.json',
            'finance': 'finance.json',
            'sales': 'sales.json'
        }
        
        # 确保数据文件存在
        self._init_data_files()
    
    def _get_data_dir(self):
        """获取数据目录"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        data_dir = os.path.join(project_root, 'modern_system', 'data')
        
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        
        return data_dir
    
    def _init_data_files(self):
        """初始化数据文件"""
        default_data = {
            'orders': [],
            'inventory': [
                {"id": "INV001", "name": "番茄", "category": "蔬菜", "quantity": 50, "unit": "kg", "price": 8.0, "min_stock": 10},
                {"id": "INV002", "name": "牛肉", "category": "肉类", "quantity": 20, "unit": "kg", "price": 68.0, "min_stock": 5},
                {"id": "INV003", "name": "面条", "category": "主食", "quantity": 100, "unit": "包", "price": 3.5, "min_stock": 20},
                {"id": "INV004", "name": "可乐", "category": "饮料", "quantity": 80, "unit": "瓶", "price": 5.0, "min_stock": 30}
            ],
            'meals': [
                {"id": "MEAL001", "name": "番茄牛肉面", "category": "面食", "price": 25.0, "cost": 15.0, "ingredients": ["番茄", "牛肉", "面条"]},
                {"id": "MEAL002", "name": "鸡蛋炒饭", "category": "炒饭", "price": 18.0, "cost": 10.0, "ingredients": ["鸡蛋", "米饭"]},
                {"id": "MEAL003", "name": "牛肉汉堡", "category": "西餐", "price": 32.0, "cost": 20.0, "ingredients": ["牛肉", "面包", "生菜"]},
                {"id": "MEAL004", "name": "薯条", "category": "小食", "price": 12.0, "cost": 6.0, "ingredients": ["土豆"]}
            ],
            'customers': [
                {"id": "CUST001", "name": "张三", "phone": "138****1234", "address": "北京市朝阳区xxx街道1号", "total_orders": 15, "total_amount": 1580.0},
                {"id": "CUST002", "name": "李四", "phone": "139****5678", "address": "北京市海淀区xxx路88号", "total_orders": 8, "total_amount": 890.0},
                {"id": "CUST003", "name": "王五", "phone": "136****9012", "address": "北京市西城区xxx胡同66号", "total_orders": 12, "total_amount": 1250.0}
            ],
            'employees': [
                {"id": "EMP001", "name": "管理员", "position": "经理", "department": "管理部", "phone": "188****0001", "salary": 8000, "hire_date": "2023-01-01"},
                {"id": "EMP002", "name": "小王", "position": "厨师", "department": "厨房", "phone": "188****0002", "salary": 6000, "hire_date": "2023-03-15"},
                {"id": "EMP003", "name": "小李", "position": "服务员", "department": "前厅", "phone": "188****0003", "salary": 4500, "hire_date": "2023-06-01"}
            ],
            'finance': [],
            'sales': []
        }
        
        for data_type, filename in self.data_files.items():
            file_path = os.path.join(self.data_dir, filename)
            if not os.path.exists(file_path):
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(default_data[data_type], f, ensure_ascii=False, indent=2)
    def register_module(self, module_type: str, instance):
        """注册模块"""
        self.modules[module_type] = instance
        # 同时保存到registered_modules
        if not hasattr(self, 'registered_modules'):
            self.registered_modules = {}
        self.registered_modules[module_type] = instance
        print(f"注册模块: {module_type}")
    
    def notify_modules(self, event_type: str):
        """通知已注册的模块"""
        if hasattr(self, 'registered_modules'):
            for module_type, module_instance in self.registered_modules.items():
                if event_type == 'meals_updated' and hasattr(module_instance, 'refresh_meals_data'):
                    try:
                        module_instance.refresh_meals_data()
                        print(f"已通知 {module_type} 模块刷新菜品数据")
                    except Exception as e:
                        print(f"通知 {module_type} 模块失败: {e}")
    
    def subscribe_event(self, event_type: str, callback):
        """订阅事件"""
        if event_type not in self.event_listeners:
            self.event_listeners[event_type] = []
        self.event_listeners[event_type].append(callback)
    
    def emit_event(self, event_type: str, data: Any):
        """触发事件"""
        if event_type in self.event_listeners:
            for callback in self.event_listeners[event_type]:
                try:
                    callback(data)
                except Exception as e:
                    print(f"事件处理错误 {event_type}: {e}")
    
    def load_data(self, data_type: str) -> List[Dict]:
        """加载数据"""
        if data_type not in self.data_files:
            return []
        
        file_path = os.path.join(self.data_dir, self.data_files[data_type])
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"加载数据失败 {data_type}: {e}")
            return []
    
    def save_data(self, data_type: str, data: List[Dict]):
        """保存数据"""
        if data_type not in self.data_files:
            return False
        
        file_path = os.path.join(self.data_dir, self.data_files[data_type])
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"保存数据失败 {data_type}: {e}")
            return False
    
    # 订单相关方法
    def get_orders(self, status_filter: Optional[str] = None) -> List[Dict]:
        """获取订单列表"""
        orders = self.load_data('orders')
        if status_filter:
            orders = [order for order in orders if order.get('status') == status_filter]
        return orders
    
    def add_order(self, order_data: Dict) -> str:
        """添加订单"""
        orders = self.load_data('orders')
        
        # 生成订单ID
        order_id = f"ORD{datetime.datetime.now().strftime('%Y%m%d')}{len(orders)+1:04d}"
        order_data['id'] = order_id
        order_data['create_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        orders.append(order_data)
        self.save_data('orders', orders)
        
        # 扣减库存
        self._deduct_inventory(order_data.get('items', []))
        
        # 记录销售数据
        self._record_sale(order_data)
        
        # 记录财务数据
        self._record_finance(order_data)
        
        # 触发事件
        self.emit_event('order_added', order_data)
        
        return order_id
    
    def update_order_status(self, order_id: str, new_status: str) -> bool:
        """更新订单状态"""
        orders = self.load_data('orders')
        
        for order in orders:
            if order.get('id') == order_id:
                old_status = order.get('status')
                order['status'] = new_status
                order['update_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                self.save_data('orders', orders)
                
                # 触发事件
                self.emit_event('order_status_changed', {
                    'order_id': order_id,
                    'old_status': old_status,
                    'new_status': new_status,
                    'order': order
                })
                
                return True
        
        return False
    
    def _deduct_inventory(self, order_items: List[Dict]):
        """扣减库存"""
        inventory = self.load_data('inventory')
        meals = self.load_data('meals')
        
        # 创建库存查找字典
        inventory_dict = {item['name']: item for item in inventory}
        meals_dict = {meal['name']: meal for meal in meals}
        
        for order_item in order_items:
            meal_name = order_item.get('name')
            quantity = order_item.get('quantity', 1)
            
            if meal_name in meals_dict:
                meal = meals_dict[meal_name]
                ingredients = meal.get('ingredients', [])
                
                # 扣减原料库存
                for ingredient in ingredients:
                    if ingredient in inventory_dict:
                        inventory_dict[ingredient]['quantity'] -= quantity
                        if inventory_dict[ingredient]['quantity'] < 0:
                            inventory_dict[ingredient]['quantity'] = 0
        
        # 保存更新后的库存
        updated_inventory = list(inventory_dict.values())
        self.save_data('inventory', updated_inventory)
        
        # 触发库存更新事件
        self.emit_event('inventory_updated', updated_inventory)
    
    def _record_sale(self, order_data: Dict):
        """记录销售数据"""
        sales = self.load_data('sales')
        
        sale_record = {
            'id': f"SALE{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}",
            'order_id': order_data.get('id'),
            'customer_name': order_data.get('customer_name'),
            'total_amount': order_data.get('total_amount', 0),
            'items': order_data.get('items', []),
            'sale_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'payment_method': order_data.get('payment_method', '现金')
        }
        
        sales.append(sale_record)
        self.save_data('sales', sales)
        
        # 触发事件
        self.emit_event('sale_recorded', sale_record)
    
    def _record_finance(self, order_data: Dict):
        """记录财务数据"""
        finance = self.load_data('finance')
        
        finance_record = {
            'id': f"FIN{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}",
            'type': 'income',
            'order_id': order_data.get('id'),
            'amount': order_data.get('total_amount', 0),
            'description': f"订单收入 - {order_data.get('customer_name', '未知客户')}",
            'date': datetime.datetime.now().strftime('%Y-%m-%d'),
            'time': datetime.datetime.now().strftime('%H:%M:%S'),
            'payment_method': order_data.get('payment_method', '现金')
        }
        
        finance.append(finance_record)
        self.save_data('finance', finance)
        
        # 触发事件
        self.emit_event('finance_recorded', finance_record)
    
    # 库存相关方法
    def get_inventory(self) -> List[Dict]:
        """获取库存列表"""
        return self.load_data('inventory')
    
    def update_inventory(self, item_id: str, quantity: int) -> bool:
        """更新库存数量"""
        inventory = self.load_data('inventory')
        
        for item in inventory:
            if item.get('id') == item_id:
                item['quantity'] = quantity
                item['update_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                self.save_data('inventory', inventory)
                self.emit_event('inventory_updated', inventory)
                
                return True
        
        return False
    
    def get_low_stock_items(self) -> List[Dict]:
        """获取低库存物品"""
        inventory = self.load_data('inventory')
        return [item for item in inventory if item.get('quantity', 0) <= item.get('min_stock', 0)]
    
    # 财务相关方法
    def get_finance_records(self, date_filter: Optional[str] = None) -> List[Dict]:
        """获取财务记录"""
        finance = self.load_data('finance')
        if date_filter:
            finance = [record for record in finance if record.get('date') == date_filter]
        return finance
    
    def get_daily_revenue(self, date: str = None) -> float:
        """获取日营收"""
        if not date:
            date = datetime.datetime.now().strftime('%Y-%m-%d')
        
        finance = self.get_finance_records(date)
        revenue = sum(record.get('amount', 0) for record in finance if record.get('type') == 'income')
        return revenue
    
    # 统计相关方法
    def get_dashboard_stats(self) -> Dict:
        """获取仪表盘统计数据"""
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        
        # 今日销售额
        today_revenue = self.get_daily_revenue(today)
        
        # 今日订单数
        orders = self.get_orders()
        today_orders = [order for order in orders if order.get('create_time', '').startswith(today)]
        
        # 库存预警
        low_stock_items = self.get_low_stock_items()
        
        # 客户总数
        customers = self.load_data('customers')
        
        return {
            'today_revenue': today_revenue,
            'today_orders': len(today_orders),
            'low_stock_count': len(low_stock_items),
            'total_customers': len(customers)
        }

# 创建全局单例实例
data_manager = DataManager()
