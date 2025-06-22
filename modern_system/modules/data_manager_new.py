#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据管理中心
负责各模块间的数据联动和统一管理
使用JSON文件存储数据
"""

import json
import os
import datetime
from typing import Dict, List, Any, Optional
from threading import Lock

class DataManager:
    def __init__(self):
        self.data_lock = Lock()
        self.modules = {}
        self.data_path = os.path.join(os.path.dirname(__file__), '..', 'data')
        self.ensure_data_directory()
        
        # 使用JSON文件存储
        print("✅ 使用JSON文件存储")
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
        elif data_type == 'financial':
            return self.load_financial_records()
        return []

    # ==================== 订单管理 ====================
    def get_orders(self, status_filter: Optional[str] = None) -> List[Dict]:
        """获取订单列表"""
        if status_filter:
            return [order for order in self.orders if order.get('status') == status_filter]
        return self.orders.copy()

    def load_orders(self) -> List[Dict]:
        """加载订单数据（JSON模式）"""
        try:
            orders_file = os.path.join(self.data_path, 'orders.json')
            if os.path.exists(orders_file):
                with open(orders_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"加载订单数据失败: {e}")
        return []

    def create_order(self, order_data: Dict) -> str:
        """创建新订单"""
        with self.data_lock:
            try:
                # 生成订单ID
                order_id = f"ORD{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
                
                # 获取菜品信息
                meal = None
                for m in self.meals:
                    if m['id'] == order_data.get('meal_id'):
                        meal = m
                        break
                
                if not meal:
                    print(f"⚠️ 菜品不存在: {order_data.get('meal_id')}")
                    return None
                
                # 计算总金额
                quantity = order_data.get('quantity', 1)
                total_amount = meal['price'] * quantity
                
                # 创建订单记录
                new_order = {
                    'id': order_id,
                    'meal_id': order_data.get('meal_id'),
                    'meal_name': meal['name'],
                    'customer_id': order_data.get('customer_id', 'GUEST'),
                    'quantity': quantity,
                    'price': meal['price'],
                    'total_amount': total_amount,
                    'status': order_data.get('status', 'Received'),
                    'note': order_data.get('note', ''),
                    'order_date': datetime.datetime.now().isoformat(),
                    'delivery_date': order_data.get('delivery_date', ''),
                    'created_at': datetime.datetime.now().isoformat(),
                    'updated_at': datetime.datetime.now().isoformat()
                }
                
                self.orders.append(new_order)
                self.save_orders()
                
                # 添加财务记录
                financial_record = {
                    'id': f"FIN{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}",
                    'type': 'revenue',
                    'amount': total_amount,
                    'description': f"订单收入 - {meal['name']} x{quantity}",
                    'order_id': order_id,
                    'date': datetime.datetime.now().isoformat(),
                    'create_time': datetime.datetime.now().isoformat()
                }
                self.financial_records.append(financial_record)
                self.save_financial_records()
                
                print(f"✅ 订单创建成功: {order_id}")
                return order_id
                
            except Exception as e:
                print(f"❌ 创建订单失败: {e}")
                return None

    def update_order_status(self, order_id: str, new_status: str) -> bool:
        """更新订单状态"""
        with self.data_lock:
            for order in self.orders:
                if order['id'] == order_id:
                    order['status'] = new_status
                    order['updated_at'] = datetime.datetime.now().isoformat()
                    self.save_orders()
                    return True
            return False

    def save_orders(self):
        """保存订单数据（JSON模式）"""
        try:
            orders_file = os.path.join(self.data_path, 'orders.json')
            with open(orders_file, 'w', encoding='utf-8') as f:
                json.dump(self.orders, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存订单数据失败: {e}")

    # ==================== 库存管理 ====================
    def get_inventory(self) -> List[Dict]:
        """获取库存列表"""
        return self.inventory.copy()

    def load_inventory(self) -> List[Dict]:
        """加载库存数据（JSON模式）"""
        try:
            inventory_file = os.path.join(self.data_path, 'inventory.json')
            if os.path.exists(inventory_file):
                with open(inventory_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"加载库存数据失败: {e}")
        return self.get_default_inventory()

    def update_inventory_stock(self, item_id: str, quantity_change: float) -> bool:
        """更新库存数量"""
        with self.data_lock:
            for item in self.inventory:
                if item['id'] == item_id:
                    item['current_stock'] += quantity_change
                    item['updated_at'] = datetime.datetime.now().isoformat()
                    self.save_inventory()
                    return True
            return False

    def save_inventory(self):
        """保存库存数据（JSON模式）"""
        try:
            inventory_file = os.path.join(self.data_path, 'inventory.json')
            with open(inventory_file, 'w', encoding='utf-8') as f:
                json.dump(self.inventory, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存库存数据失败: {e}")

    def get_low_stock_items(self, threshold: int = 10) -> List[Dict]:
        """获取低库存项目"""
        return [item for item in self.inventory if item.get('current_stock', 0) <= threshold]

    # ==================== 财务管理 ====================
    def get_financial_records(self) -> List[Dict]:
        """获取财务记录"""
        return self.financial_records.copy()

    def load_financial_records(self) -> List[Dict]:
        """加载财务记录（JSON模式）"""
        try:
            finance_file = os.path.join(self.data_path, 'finance.json')
            if os.path.exists(finance_file):
                with open(finance_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"加载财务数据失败: {e}")
        return []

    def add_financial_record(self, record_data: Dict) -> str:
        """添加财务记录"""
        record_id = f"FIN{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
        record_data['id'] = record_id
        record_data['create_time'] = datetime.datetime.now().isoformat()
        self.financial_records.append(record_data)
        self.save_financial_records()
        return record_id

    def get_financial_records_by_type(self, record_type: Optional[str] = None) -> List[Dict]:
        """获取财务记录"""
        if record_type:
            return [record for record in self.financial_records if record.get('type') == record_type]
        return self.financial_records.copy()

    def save_financial_records(self):
        """保存财务记录（JSON模式）"""
        try:
            finance_file = os.path.join(self.data_path, 'finance.json')
            with open(finance_file, 'w', encoding='utf-8') as f:
                json.dump(self.financial_records, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存财务数据失败: {e}")

    def update_dashboard_stats(self):
        """更新仪表盘统计数据"""
        # JSON文件模式
        today = datetime.datetime.now().date()
        today_sales = 0
        order_count = 0
        
        for order in self.orders:
            try:
                order_date = datetime.datetime.fromisoformat(order['order_date']).date()
                if order_date == today:
                    order_count += 1
                    today_sales += order.get('total_amount', 0)
            except:
                continue
        
        low_stock_count = len(self.get_low_stock_items())
        customer_count = len(self.customers)
        
        self.dashboard_stats = {
            'today_sales': today_sales,
            'order_count': order_count,
            'low_stock_count': low_stock_count,
            'customer_count': customer_count,
            'last_update': datetime.datetime.now().isoformat()
        }

    # ==================== 客户管理 ====================
    def get_customers(self) -> List[Dict]:
        """获取客户列表"""
        return self.customers.copy()

    def load_customers(self) -> List[Dict]:
        """加载客户数据（JSON模式）"""
        try:
            customers_file = os.path.join(self.data_path, 'customers.json')
            if os.path.exists(customers_file):
                with open(customers_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"加载客户数据失败: {e}")
        return self.get_default_customers()

    def add_customer(self, customer_data: Dict) -> str:
        """添加客户"""
        with self.data_lock:
            customer_id = f"CUST{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
            customer_data['id'] = customer_id
            customer_data['created_at'] = datetime.datetime.now().isoformat()
            customer_data['updated_at'] = datetime.datetime.now().isoformat()
            self.customers.append(customer_data)
            self.save_customers()
            return customer_id

    def update_customer(self, customer_id: str, customer_data: Dict) -> bool:
        """更新客户信息"""
        with self.data_lock:
            for customer in self.customers:
                if customer['id'] == customer_id:
                    customer.update(customer_data)
                    customer['updated_at'] = datetime.datetime.now().isoformat()
                    self.save_customers()
                    return True
            return False

    def delete_customer(self, customer_id: str) -> bool:
        """删除客户"""
        with self.data_lock:
            for i, customer in enumerate(self.customers):
                if customer['id'] == customer_id:
                    del self.customers[i]
                    self.save_customers()
                    return True
            return False

    def save_customers(self):
        """保存客户数据（JSON模式）"""
        try:
            customers_file = os.path.join(self.data_path, 'customers.json')
            with open(customers_file, 'w', encoding='utf-8') as f:
                json.dump(self.customers, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存客户数据失败: {e}")

    # ==================== 餐食管理 ====================
    def load_meals(self) -> List[Dict]:
        """加载餐食数据（JSON模式）"""
        try:
            meals_file = os.path.join(self.data_path, 'meals.json')
            if os.path.exists(meals_file):
                with open(meals_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"加载餐食数据失败: {e}")
        return self.get_default_meals()

    def get_meals(self, active_only: bool = True) -> List[Dict]:
        """获取餐食列表"""
        if active_only:
            return [meal for meal in self.meals if meal.get('isActive', True)]
        return self.meals.copy()

    def add_meal(self, meal_data: Dict) -> str:
        """添加餐食"""
        with self.data_lock:
            meal_id = f"MEAL{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
            meal_data['id'] = meal_id
            meal_data['created_at'] = datetime.datetime.now().isoformat()
            meal_data['updated_at'] = datetime.datetime.now().isoformat()
            self.meals.append(meal_data)
            self.save_meals()
            return meal_id

    def update_meal(self, meal_id: str, meal_data: Dict) -> bool:
        """更新餐食信息"""
        with self.data_lock:
            for meal in self.meals:
                if meal['id'] == meal_id:
                    meal.update(meal_data)
                    meal['updated_at'] = datetime.datetime.now().isoformat()
                    self.save_meals()
                    return True
            return False

    def delete_meal(self, meal_id: str) -> bool:
        """删除餐食"""
        with self.data_lock:
            for i, meal in enumerate(self.meals):
                if meal['id'] == meal_id:
                    del self.meals[i]
                    self.save_meals()
                    return True
            return False

    def save_meals(self):
        """保存餐食数据（JSON模式）"""
        try:
            meals_file = os.path.join(self.data_path, 'meals.json')
            with open(meals_file, 'w', encoding='utf-8') as f:
                json.dump(self.meals, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存餐食数据失败: {e}")

    # ==================== 员工管理 ====================
    def load_employees(self) -> List[Dict]:
        """加载员工数据（JSON模式）"""
        try:
            employees_file = os.path.join(self.data_path, 'employees.json')
            if os.path.exists(employees_file):
                with open(employees_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"加载员工数据失败: {e}")
        return self.get_default_employees()

    def get_employees(self) -> List[Dict]:
        """获取员工列表"""
        return self.employees.copy()

    def add_employee(self, employee_data: Dict) -> str:
        """添加员工"""
        with self.data_lock:
            employee_id = f"EMP{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
            employee_data['id'] = employee_id
            employee_data['created_at'] = datetime.datetime.now().isoformat()
            employee_data['updated_at'] = datetime.datetime.now().isoformat()
            self.employees.append(employee_data)
            self.save_employees()
            return employee_id

    def update_employee(self, employee_id: str, employee_data: Dict) -> bool:
        """更新员工信息"""
        with self.data_lock:
            for employee in self.employees:
                if employee['id'] == employee_id:
                    employee.update(employee_data)
                    employee['updated_at'] = datetime.datetime.now().isoformat()
                    self.save_employees()
                    return True
            return False

    def delete_employee(self, employee_id: str) -> bool:
        """删除员工"""
        with self.data_lock:
            for i, employee in enumerate(self.employees):
                if employee['id'] == employee_id:
                    del self.employees[i]
                    self.save_employees()
                    return True
            return False

    def save_employees(self):
        """保存员工数据（JSON模式）"""
        try:
            employees_file = os.path.join(self.data_path, 'employees.json')
            with open(employees_file, 'w', encoding='utf-8') as f:
                json.dump(self.employees, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存员工数据失败: {e}")

    # ==================== 默认数据 ====================
    def get_default_meals(self) -> List[Dict]:
        """获取默认餐食数据"""
        return [
            {
                'id': 'MEAL001',
                'name': '宫保鸡丁',
                'price': 28.0,
                'category': '川菜',
                'description': '经典川菜，麻辣鲜香',
                'isActive': True,
                'created_at': datetime.datetime.now().isoformat(),
                'updated_at': datetime.datetime.now().isoformat()
            },
            {
                'id': 'MEAL002',
                'name': '麻婆豆腐',
                'price': 18.0,
                'category': '川菜',
                'description': '嫩滑豆腐，麻辣鲜香',
                'isActive': True,
                'created_at': datetime.datetime.now().isoformat(),
                'updated_at': datetime.datetime.now().isoformat()
            },
            {
                'id': 'MEAL003',
                'name': '红烧肉',
                'price': 35.0,
                'category': '家常菜',
                'description': '肥而不腻，入口即化',
                'isActive': True,
                'created_at': datetime.datetime.now().isoformat(),
                'updated_at': datetime.datetime.now().isoformat()
            },
            {
                'id': 'MEAL004',
                'name': '糖醋排骨',
                'price': 32.0,
                'category': '家常菜',
                'description': '酸甜可口，老少皆宜',
                'isActive': True,
                'created_at': datetime.datetime.now().isoformat(),
                'updated_at': datetime.datetime.now().isoformat()
            },
            {
                'id': 'MEAL005',
                'name': '清蒸鱼',
                'price': 45.0,
                'category': '海鲜',
                'description': '新鲜鱼类，原汁原味',
                'isActive': True,
                'created_at': datetime.datetime.now().isoformat(),
                'updated_at': datetime.datetime.now().isoformat()
            }
        ]

    def get_default_inventory(self) -> List[Dict]:
        """获取默认库存数据"""
        return [
            {
                'id': 'INV001',
                'name': '鸡肉',
                'category': '肉类',
                'unit': '公斤',
                'current_stock': 50.0,
                'min_stock': 10.0,
                'price': 15.0,
                'supplier': '新鲜食材供应商',
                'updated_at': datetime.datetime.now().isoformat()
            },
            {
                'id': 'INV002',
                'name': '豆腐',
                'category': '豆制品',
                'unit': '块',
                'current_stock': 30.0,
                'min_stock': 5.0,
                'price': 3.0,
                'supplier': '豆制品厂',
                'updated_at': datetime.datetime.now().isoformat()
            },
            {
                'id': 'INV003',
                'name': '猪肉',
                'category': '肉类',
                'unit': '公斤',
                'current_stock': 40.0,
                'min_stock': 8.0,
                'price': 25.0,
                'supplier': '肉类批发市场',
                'updated_at': datetime.datetime.now().isoformat()
            },
            {
                'id': 'INV004',
                'name': '排骨',
                'category': '肉类',
                'unit': '公斤',
                'current_stock': 25.0,
                'min_stock': 5.0,
                'price': 35.0,
                'supplier': '肉类批发市场',
                'updated_at': datetime.datetime.now().isoformat()
            },
            {
                'id': 'INV005',
                'name': '鲫鱼',
                'category': '海鲜',
                'unit': '条',
                'current_stock': 20.0,
                'min_stock': 3.0,
                'price': 12.0,
                'supplier': '海鲜市场',
                'updated_at': datetime.datetime.now().isoformat()
            }
        ]

    def get_default_customers(self) -> List[Dict]:
        """获取默认客户数据"""
        return [
            {
                'id': 'CUST001',
                'name': '张三',
                'phone': '13800138001',
                'email': 'zhangsan@example.com',
                'address': '北京市朝阳区建国门外大街1号',
                'created_at': datetime.datetime.now().isoformat(),
                'updated_at': datetime.datetime.now().isoformat()
            },
            {
                'id': 'CUST002',
                'name': '李四',
                'phone': '13800138002',
                'email': 'lisi@example.com',
                'address': '上海市浦东新区世纪大道100号',
                'created_at': datetime.datetime.now().isoformat(),
                'updated_at': datetime.datetime.now().isoformat()
            }
        ]

    def get_default_employees(self) -> List[Dict]:
        """获取默认员工数据"""
        return [
            {
                'id': 'EMP001',
                'name': '王厨师',
                'position': '主厨',
                'department': '厨房',
                'salary': 8000.0,
                'phone': '13900139001',
                'email': 'chef.wang@restaurant.com',
                'created_at': datetime.datetime.now().isoformat(),
                'updated_at': datetime.datetime.now().isoformat()
            },
            {
                'id': 'EMP002',
                'name': '刘服务员',
                'position': '服务员',
                'department': '前厅',
                'salary': 4500.0,
                'phone': '13900139002',
                'email': 'service.liu@restaurant.com',
                'created_at': datetime.datetime.now().isoformat(),
                'updated_at': datetime.datetime.now().isoformat()
            }
        ]

# 创建全局数据管理器实例
data_manager = DataManager()
