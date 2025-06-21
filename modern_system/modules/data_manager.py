#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据管理中心
负责各模块间的数据联动和统一管理
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
        
        # 数据存储
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
    
    # ==================== 订单管理 ====================
    def load_orders(self) -> List[Dict]:
        """加载订单数据"""
        try:
            orders_file = os.path.join(self.data_path, 'orders.json')
            if os.path.exists(orders_file):
                with open(orders_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"加载订单数据失败: {e}")
        return self.get_default_orders()
    
    def save_orders(self):
        """保存订单数据"""
        try:
            orders_file = os.path.join(self.data_path, 'orders.json')
            with open(orders_file, 'w', encoding='utf-8') as f:
                json.dump(self.orders, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存订单数据失败: {e}")
    
    def add_order(self, order_data: Dict) -> str:
        """添加新订单并处理库存扣减"""
        with self.data_lock:
            # 生成订单ID
            order_id = f"ORD{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
            order_data['id'] = order_id
            order_data['create_time'] = datetime.datetime.now().isoformat()
            order_data['status'] = '待处理'
            
            # 检查库存并扣减
            if self.check_and_reduce_inventory(order_data.get('items', [])):
                self.orders.append(order_data)
                self.save_orders()
                
                # 添加财务记录
                self.add_financial_record({
                    'type': 'income',
                    'category': '销售收入',
                    'amount': order_data.get('total_amount', 0),
                    'description': f"订单收入 - {order_id}",
                    'order_id': order_id
                })
                
                # 更新统计数据
                self.update_dashboard_stats()
                
                # 通知相关模块
                self.notify_modules('order_added', order_data)
                
                return order_id
            else:
                raise ValueError("库存不足，无法创建订单")
    
    def create_order(self, order_data: Dict) -> str:
        """创建新订单（add_order的别名）"""
        return self.add_order(order_data)
    
    def update_order_status(self, order_id: str, new_status: str) -> bool:
        """更新订单状态"""
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
        if status_filter:
            return [order for order in self.orders if order.get('status') == status_filter]
        return self.orders.copy()
    
    # ==================== 库存管理 ====================
    def load_inventory(self) -> List[Dict]:
        """加载库存数据"""
        try:
            inventory_file = os.path.join(self.data_path, 'inventory.json')
            if os.path.exists(inventory_file):
                with open(inventory_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"加载库存数据失败: {e}")
        return self.get_default_inventory()
    
    def save_inventory(self):
        """保存库存数据"""
        try:
            inventory_file = os.path.join(self.data_path, 'inventory.json')
            with open(inventory_file, 'w', encoding='utf-8') as f:
                json.dump(self.inventory, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存库存数据失败: {e}")
    
    def check_and_reduce_inventory(self, order_items: List[Dict]) -> bool:
        """检查库存并扣减"""
        # 先检查库存是否充足
        for item in order_items:
            product_id = item.get('product_id')
            quantity = item.get('quantity', 0)
            
            inventory_item = self.find_inventory_item(product_id)
            if not inventory_item or inventory_item.get('stock', 0) < quantity:
                return False
        
        # 库存充足，执行扣减
        for item in order_items:
            product_id = item.get('product_id')
            quantity = item.get('quantity', 0)
            
            inventory_item = self.find_inventory_item(product_id)
            if inventory_item:
                inventory_item['stock'] -= quantity
                inventory_item['last_update'] = datetime.datetime.now().isoformat()
        
        self.save_inventory()
        return True
    
    def restore_inventory(self, order_items: List[Dict]):
        """恢复库存（订单取消时）"""
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
        for item in self.inventory:
            if item.get('id') == product_id or item.get('name') == product_id:
                return item
        return None
    
    def get_low_stock_items(self, threshold: int = 10) -> List[Dict]:
        """获取低库存商品"""
        return [item for item in self.inventory if item.get('stock', 0) <= threshold]
    
    # ==================== 财务管理 ====================
    def load_financial_records(self) -> List[Dict]:
        """加载财务记录"""
        try:
            finance_file = os.path.join(self.data_path, 'finance.json')
            if os.path.exists(finance_file):
                with open(finance_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"加载财务数据失败: {e}")
        return []
    
    def save_financial_records(self):
        """保存财务记录"""
        try:
            finance_file = os.path.join(self.data_path, 'finance.json')
            with open(finance_file, 'w', encoding='utf-8') as f:
                json.dump(self.financial_records, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存财务数据失败: {e}")
    
    def add_financial_record(self, record_data: Dict) -> str:
        """添加财务记录"""
        with self.data_lock:
            record_id = f"FIN{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
            record_data['id'] = record_id
            record_data['create_time'] = datetime.datetime.now().isoformat()
            
            self.financial_records.append(record_data)
            self.save_financial_records()
            
            # 通知财务模块
            self.notify_modules('financial_record_added', record_data)
            
            return record_id
    
    def get_financial_records(self, record_type: Optional[str] = None) -> List[Dict]:
        """获取财务记录"""
        if record_type:
            return [record for record in self.financial_records if record.get('type') == record_type]
        return self.financial_records.copy()
    
    # ==================== 统计数据 ====================
    def update_dashboard_stats(self):
        """更新仪表盘统计数据"""
        today = datetime.date.today()
        today_str = today.isoformat()
        
        # 今日销售额
        today_sales = 0
        today_orders = 0
        
        for order in self.orders:
            order_date = order.get('create_time', '')[:10]  # 取日期部分
            if order_date == today_str and order.get('status') != '已取消':
                today_sales += order.get('total_amount', 0)
                today_orders += 1
        
        # 库存预警数量
        low_stock_count = len(self.get_low_stock_items())
        
        # 客户总数
        customer_count = len(self.customers)
        
        self.dashboard_stats = {
            'today_sales': today_sales,
            'order_count': today_orders,
            'low_stock_count': low_stock_count,
            'customer_count': customer_count,
            'last_update': datetime.datetime.now().isoformat()
        }
    
    def get_dashboard_stats(self) -> Dict:
        """获取仪表盘统计数据"""
        # 如果数据太旧，重新计算
        if (not self.dashboard_stats.get('last_update') or 
            datetime.datetime.now() - datetime.datetime.fromisoformat(self.dashboard_stats['last_update']) > 
            datetime.timedelta(minutes=5)):
            self.update_dashboard_stats()
        
        return self.dashboard_stats.copy()
    
    # ==================== 其他数据管理 ====================
    def load_customers(self) -> List[Dict]:
        """加载客户数据"""
        try:
            customers_file = os.path.join(self.data_path, 'customers.json')
            if os.path.exists(customers_file):
                with open(customers_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"加载客户数据失败: {e}")
        return self.get_default_customers()
    
    def load_meals(self) -> List[Dict]:
        """加载菜品数据"""
        try:
            meals_file = os.path.join(self.data_path, 'meals.json')
            if os.path.exists(meals_file):
                with open(meals_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"加载菜品数据失败: {e}")
        return self.get_default_meals()
    
    def load_employees(self) -> List[Dict]:
        """加载员工数据"""
        try:
            employees_file = os.path.join(self.data_path, 'employees.json')
            if os.path.exists(employees_file):
                with open(employees_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"加载员工数据失败: {e}")
        return self.get_default_employees()
    
    # ==================== 模块通知 ====================
    def notify_modules(self, event_type: str, data: Any):
        """通知相关模块数据变更"""
        for module_type, module_instance in self.modules.items():
            if hasattr(module_instance, 'on_data_changed'):
                try:
                    module_instance.on_data_changed(event_type, data)
                except Exception as e:
                    print(f"通知模块 {module_type} 失败: {e}")
    
    # ==================== 默认数据 ====================
    def get_default_orders(self) -> List[Dict]:
        """获取默认订单数据"""
        return [
            {
                'id': 'ORD20240615001',
                'customer_name': '张三',
                'customer_phone': '138****1234',
                'delivery_address': '北京市朝阳区xxx街道1号',
                'items': [
                    {'product_id': '番茄牛肉面', 'name': '番茄牛肉面', 'quantity': 2, 'price': 25.0},
                    {'product_id': '可乐', 'name': '可乐', 'quantity': 1, 'price': 5.0}
                ],
                'total_amount': 55.0,
                'status': '已完成',
                'order_type': '外卖',
                'payment_method': '微信支付',
                'note': '少放辣椒',
                'create_time': '2024-06-15T12:30:00',
                'update_time': '2024-06-15T12:45:00'
            },
            {
                'id': 'ORD20240615002',
                'customer_name': '李四',
                'customer_phone': '139****5678',
                'delivery_address': '北京市海淀区xxx路88号',
                'items': [
                    {'product_id': '鸡蛋炒饭', 'name': '鸡蛋炒饭', 'quantity': 1, 'price': 18.0}
                ],
                'total_amount': 18.0,
                'status': '制作中',
                'order_type': '外卖',
                'payment_method': '支付宝',
                'note': '',
                'create_time': '2024-06-15T12:45:00',
                'update_time': '2024-06-15T12:45:00'
            },
            {
                'id': 'ORD20240615003',
                'customer_name': '王五',
                'customer_phone': '136****9012',
                'delivery_address': '北京市西城区xxx胡同66号',
                'items': [
                    {'product_id': '牛肉汉堡', 'name': '牛肉汉堡', 'quantity': 3, 'price': 32.0},
                    {'product_id': '薯条', 'name': '薯条', 'quantity': 2, 'price': 12.0}
                ],
                'total_amount': 120.0,
                'status': '待接单',
                'order_type': '外卖',
                'payment_method': '现金',
                'note': '汉堡不要洋葱',
                'create_time': '2024-06-15T11:20:00',
                'update_time': '2024-06-15T11:20:00'
            },
            {
                'id': 'ORD20240615004',
                'customer_name': '赵六',
                'customer_phone': '137****3456',
                'delivery_address': '堂食',
                'items': [
                    {'product_id': '红烧肉', 'name': '红烧肉', 'quantity': 1, 'price': 35.0},
                    {'product_id': '米饭', 'name': '米饭', 'quantity': 2, 'price': 3.0}
                ],
                'total_amount': 41.0,
                'status': '配送中',
                'order_type': '堂食',
                'payment_method': '微信支付',
                'note': '',
                'create_time': '2024-06-15T13:15:00',
                'update_time': '2024-06-15T13:15:00'
            },
            {
                'id': 'ORD20240615005',
                'customer_name': '钱七',
                'customer_phone': '135****7890',
                'delivery_address': '上海市浦东新区xxx路99号',
                'items': [
                    {'product_id': '宫保鸡丁', 'name': '宫保鸡丁', 'quantity': 1, 'price': 28.0},
                    {'product_id': '白米饭', 'name': '白米饭', 'quantity': 1, 'price': 3.0}
                ],
                'total_amount': 31.0,
                'status': '已完成',
                'order_type': '外卖',
                'payment_method': '现金',
                'note': '不要太辣',
                'create_time': '2024-06-15T14:20:00',
                'update_time': '2024-06-15T14:50:00'
            }
        ]
    
    def get_default_inventory(self) -> List[Dict]:
        """获取默认库存数据"""
        return [
            {'id': 'INV001', 'name': '鸡肉', 'category': '肉类', 'stock': 50, 'unit': '斤', 'price': 15.0, 'min_stock': 10},
            {'id': 'INV002', 'name': '豆腐', 'category': '豆制品', 'stock': 30, 'unit': '块', 'price': 3.0, 'min_stock': 5},
            {'id': 'INV003', 'name': '大米', 'category': '主食', 'stock': 100, 'unit': '斤', 'price': 5.0, 'min_stock': 20},
            {'id': 'INV004', 'name': '青菜', 'category': '蔬菜', 'stock': 8, 'unit': '斤', 'price': 4.0, 'min_stock': 10}  # 低库存示例
        ]
    
    def get_default_customers(self) -> List[Dict]:
        """获取默认客户数据"""
        return [
            {'id': 'CUS001', 'name': '张三', 'phone': '13800138001', 'address': '北京市朝阳区', 'level': 'VIP'},
            {'id': 'CUS002', 'name': '李四', 'phone': '13800138002', 'address': '北京市海淀区', 'level': '普通'},
            {'id': 'CUS003', 'name': '王五', 'phone': '13800138003', 'address': '北京市西城区', 'level': '普通'}
        ]
    
    def get_default_meals(self) -> List[Dict]:
        """获取默认菜品数据"""
        return [
            {'id': 'MEAL001', 'name': '宫保鸡丁', 'category': '川菜', 'price': 28.0, 'cost': 18.0, 'description': '经典川菜'},
            {'id': 'MEAL002', 'name': '麻婆豆腐', 'category': '川菜', 'price': 18.0, 'cost': 12.0, 'description': '麻辣可口'},
            {'id': 'MEAL003', 'name': '红烧肉', 'category': '家常菜', 'price': 35.0, 'cost': 25.0, 'description': '肥而不腻'}
        ]
    
    def get_default_employees(self) -> List[Dict]:
        """获取默认员工数据"""
        return [
            {'id': 'EMP001', 'name': '管理员', 'position': '经理', 'department': '管理部', 'salary': 8000, 'phone': '13900139001'},
            {'id': 'EMP002', 'name': '小王', 'position': '服务员', 'department': '服务部', 'salary': 4000, 'phone': '13900139002'},
            {'id': 'EMP003', 'name': '小李', 'position': '厨师', 'department': '厨房', 'salary': 6000, 'phone': '13900139003'}
        ]

# 创建全局数据管理器实例
data_manager = DataManager()
