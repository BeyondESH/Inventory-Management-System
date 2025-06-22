#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Data Management Center
Responsible for data linkage and unified management across modules
Stores data using JSON files
"""

import json
import os
import datetime
from typing import Dict, List, Any, Optional
from threading import Lock
from tkinter import TclError

class DataManager:
    def __init__(self):
        self.data_lock = Lock()
        self.modules = {}
        self.data_path = os.path.join(os.path.dirname(__file__), '..', 'data')
        self.ensure_data_directory()
        
        # 使用JSON文件存储
        print("✅ Using JSON file storage")
        # 数据存储（JSON模式）
        self.orders = self.load_orders()
        self.inventory = self.load_inventory()
        self.customers = self.load_customers()
        self.meals = self.load_meals()
        self.employees = self.load_employees()
        self.financial_records = self.load_financial_records()
        
        # 初始化仪表盘统计
        self.dashboard_stats = {
            'today_sales': 0,
            'order_count': 0,
            'low_stock_count': 0,
            'customer_count': 0,
            'last_update': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
    def ensure_data_directory(self):
        """Ensure data directory exists"""
        if not os.path.exists(self.data_path):
            os.makedirs(self.data_path)
    
    def register_module(self, module_type: str, instance):
        """注册模块实例"""
        self.modules[module_type] = instance
        
    def get_module(self, module_type: str):
        """获取模块实例"""
        return self.modules.get(module_type)

    # ==================== 数据加载方法 ====================
    def load_orders(self) -> List[Dict]:
        """Load orders data"""
        orders_file = os.path.join(self.data_path, 'orders.json')
        if os.path.exists(orders_file):
            try:
                with open(orders_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading orders data: {e}")
        return []
    
    def load_inventory(self) -> List[Dict]:
        """Load inventory data"""
        inventory_file = os.path.join(self.data_path, 'inventory.json')
        if os.path.exists(inventory_file):
            try:
                with open(inventory_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading inventory data: {e}")
        return []
    
    def load_customers(self) -> List[Dict]:
        """Load customers data"""
        customers_file = os.path.join(self.data_path, 'customers.json')
        if os.path.exists(customers_file):
            try:
                with open(customers_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading customers data: {e}")
        return []
    
    def load_meals(self) -> List[Dict]:
        """Load meals data"""
        meals_file = os.path.join(self.data_path, 'meals.json')
        if os.path.exists(meals_file):
            try:
                with open(meals_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading meals data: {e}")
        return []
    
    def load_employees(self) -> List[Dict]:
        """Load employees data"""
        employees_file = os.path.join(self.data_path, 'employees.json')
        if os.path.exists(employees_file):
            try:
                with open(employees_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading employees data: {e}")
        return []

    def load_financial_records(self) -> List[Dict]:
        """Load financial records"""
        finance_file = os.path.join(self.data_path, 'finance.json')
        if os.path.exists(finance_file):
            try:
                with open(finance_file, 'r', encoding='utf-8') as f:
                    records = json.load(f)
                    # 确保记录格式正确
                    processed_records = []
                    for record in records:
                        # 兼容不同的数据格式
                        if isinstance(record, dict):
                            # 数据类型转换
                            if record.get('type') == 'revenue':
                                record['type'] = 'Income'
                            elif record.get('type') == 'cost':
                                record['type'] = 'Expense'
                            
                            # 确保金额是数字类型
                            if 'amount' in record:
                                try:
                                    record['amount'] = float(record['amount'])
                                except (ValueError, TypeError):
                                    record['amount'] = 0.0
                            
                            # 确保有正确的时间字段
                            if 'date' in record and 'create_time' not in record:
                                record['create_time'] = record['date']
                                
                            processed_records.append(record)
                    return processed_records
            except Exception as e:
                print(f"Error loading financial records: {e}")
        return []
    
    def save_financial_records(self):
        """Save financial records"""
        finance_file = os.path.join(self.data_path, 'finance.json')
        try:
            # 处理浮点数精度问题
            records_to_save = []
            for record in self.financial_records:
                record_copy = record.copy()
                if 'amount' in record_copy:
                    record_copy['amount'] = round(float(record_copy['amount']), 2)
                records_to_save.append(record_copy)
            
            with open(finance_file, 'w', encoding='utf-8') as f:
                json.dump(records_to_save, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving financial records: {e}")
    
    # ==================== 财务管理 ====================
    def get_financial_records(self) -> List[Dict]:
        """Get financial records"""
        return self.financial_records.copy()
    
    def get_finance_records(self) -> List[Dict]:
        """获取财务记录（别名方法，兼容财务模块）"""
        return self.get_financial_records()

    # ==================== 数据获取方法 ====================
    def load_data(self, data_type: str):
        """Load specified data type (legacy interface compatibility)"""
        if data_type == 'orders':
            return self.get_orders()
        elif data_type == 'inventory':
            return self.get_inventory()
        elif data_type == 'customers':
            return self.get_customers()
        elif data_type == 'meals':
            return self.get_meals()
        elif data_type == 'employees':
            return self.get_employees()
        elif data_type == 'finance':
            return self.get_financial_records()
        elif data_type == 'recipes':
             # Load recipe data from recipes.json
            recipes_file = os.path.join(self.data_path, 'recipes.json')
            if os.path.exists(recipes_file):
                try:
                    with open(recipes_file, 'r', encoding='utf-8') as f:
                        return json.load(f)
                except Exception as e:
                    print(f"Error loading recipes data: {e}")
            return []
        else:
            print(f"Warning: Unsupported data type: {data_type}")
            return []
    
    def get_orders(self) -> List[Dict]:
        """获取订单数据"""
        return self.orders.copy()
    
    def get_inventory(self) -> List[Dict]:
        """获取库存数据"""
        return self.inventory.copy()
    
    def get_customers(self) -> List[Dict]:
        """获取客户数据"""
        return self.customers.copy()
    
    def get_meals(self) -> List[Dict]:
        """获取菜品数据"""
        return self.meals.copy()
    
    def get_employees(self) -> List[Dict]:
        """获取员工数据"""
        return self.employees.copy()

    # ==================== 数据保存方法 ====================
    def save_inventory(self):
        """Save inventory data"""
        inventory_file = os.path.join(self.data_path, 'inventory.json')
        try:
            with open(inventory_file, 'w', encoding='utf-8') as f:
                json.dump(self.inventory, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving inventory data: {e}")
    
    def save_customers(self):
        """Save customers data"""
        customers_file = os.path.join(self.data_path, 'customers.json')
        try:
            with open(customers_file, 'w', encoding='utf-8') as f:
                json.dump(self.customers, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving customers data: {e}")
    
    def save_meals(self):
        """Save meals data"""
        meals_file = os.path.join(self.data_path, 'meals.json')
        try:
            with open(meals_file, 'w', encoding='utf-8') as f:
                json.dump(self.meals, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving meals data: {e}")
    
    def save_employees(self):
        """Save employees data"""
        employees_file = os.path.join(self.data_path, 'employees.json')
        try:
            with open(employees_file, 'w', encoding='utf-8') as f:
                json.dump(self.employees, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving employees data: {e}")

    def save_orders(self):
        """Save orders data (JSON mode)"""
        try:
            orders_file = os.path.join(self.data_path, 'orders.json')
            with open(orders_file, 'w', encoding='utf-8') as f:
                json.dump(self.orders, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving orders data: {e}")

    # ==================== 订单管理 ====================
    def add_order(self, order_data: Dict) -> str:
        """添加订单（别名方法）"""
        return self.create_order(order_data)

    def create_order(self, order_data: Dict) -> Any:
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
                    'order_date': datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
                    'delivery_date': order_data.get('delivery_date', ''),
                    'created_at': datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
                    'updated_at': datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
                }                
                self.orders.append(new_order)
                self.save_orders()
                
                # 添加财务记录
                financial_record = {
                    'id': f"FIN{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}",
                    'type': 'revenue',
                    'amount': round(total_amount, 2),
                    'description': f"Order Income - {meal['name']} x{quantity}",
                    'order_id': order_id,
                    'date': datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
                    'create_time': datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
                }
                self.financial_records.append(financial_record)
                self.save_financial_records()
                
                # 扣减库存（基于菜品的食材需求）
                self.reduce_inventory_for_meal(meal, quantity)
                
                # 更新仪表盘统计
                self.update_dashboard_stats()
                
                # 通知各模块有新订单创建
                self.notify_modules_order_created(order_id)
                
                print(f"✅ 订单创建成功: {order_id}")
                return order_id
                
            except Exception as e:
                print(f"❌ 创建订单失败: {e}")
                return None

    # ==================== 模块通知和刷新 ====================
    def update_dashboard_stats(self):
        """更新仪表盘统计数据"""
        try:
            # 计算今日销售额
            today = datetime.datetime.now().strftime('%Y-%m-%d')
            today_sales = 0
            order_count = 0
            
            for record in self.financial_records:
                record_date = record.get('date', '')
                if record_date.startswith(today) and record.get('type') in ['revenue', 'Income']:
                    today_sales += record.get('amount', 0)
                    
            for order in self.orders:
                order_date = order.get('order_date', '')
                if order_date.startswith(today):
                    order_count += 1
            
            # 计算低库存项目
            low_stock_count = 0
            for item in self.inventory:
                current_stock = item.get('current_stock', 0)
                min_stock = item.get('min_stock', 10)  # 默认最小库存为10
                if current_stock < min_stock:
                    low_stock_count += 1
            
            # 客户数量
            customer_count = len(self.customers)
            
            # 保存统计数据
            self.dashboard_stats = {
                'today_sales': today_sales,
                'order_count': order_count,
                'low_stock_count': low_stock_count,
                'customer_count': customer_count,
                'last_update': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            print(f"✅ Dashboard statistics updated")
        except Exception as e:
            print(f"❌ 更新仪表盘统计失败: {e}")
            # 提供默认统计数据
            self.dashboard_stats = {
                'today_sales': 0,
                'order_count': 0,
                'low_stock_count': 0,
                'customer_count': 0,
                'last_update': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }

    def refresh_data(self):
        """刷新所有数据"""
        try:
            self.orders = self.load_orders()
            self.inventory = self.load_inventory() 
            self.customers = self.load_customers()
            self.meals = self.load_meals()
            self.employees = self.load_employees()
            self.financial_records = self.load_financial_records()
            print("✅ Data refreshed successfully")
        except Exception as e:
            print(f"❌ 数据刷新失败: {e}")

    def notify_modules_order_created(self, order_id: str):
        """Notify modules that an order has been created"""
        try:
            # Finance module
            finance_module = self.modules.get('finance')
            if finance_module and hasattr(finance_module, 'refresh_data'):
                try:
                    finance_module.refresh_data()
                    print(f"✅ Notified finance module to refresh data")
                except TclError:
                    print(f"⚠️ Finance UI not active, skipping refresh")
                except Exception as e:
                    print(f"⚠️ Skipped finance refresh: {e}")

            # Inventory module
            inventory_module = self.modules.get('inventory')
            if inventory_module and hasattr(inventory_module, 'refresh_data'):
                try:
                    inventory_module.refresh_data()
                    print(f"✅ Notified inventory module to refresh data")
                except TclError:
                    print(f"⚠️ Inventory UI not active, skipping refresh")
                except Exception as e:
                    print(f"⚠️ Skipped inventory refresh: {e}")

            # Charts module
            charts_module = self.modules.get('charts')
            if charts_module and hasattr(charts_module, 'refresh_charts'):
                try:
                    charts_module.refresh_charts()
                    print(f"✅ Notified charts module to refresh data")
                except TclError:
                    print(f"⚠️ Charts UI not active, skipping refresh")
                except Exception as e:
                    print(f"⚠️ Skipped charts refresh: {e}")

            # Sales module
            sales_module = self.modules.get('sales')
            if sales_module and hasattr(sales_module, 'refresh_data'):
                try:
                    sales_module.refresh_data()
                    print(f"✅ Notified sales module to refresh data")
                except TclError:
                    print(f"⚠️ Sales UI not active, skipping refresh")
                except Exception as e:
                    print(f"⚠️ Skipped sales refresh: {e}")
        except Exception as e:
            print(f"⚠️ Error notifying modules: {e}")
        # End of notifications

    def reduce_inventory_for_meal(self, meal: Dict, quantity: int) -> bool:
        """Reduce inventory for meal preparation"""
        try:
            # 获取菜品的食材需求
            ingredients = meal.get('ingredients', [])
            if not ingredients:
                print(f"⚠️ 菜品 {meal['name']} 没有配置食材信息")
                return True  # 没有食材需求，直接返回成功
            
            # 定义每份菜品的标准食材用量
            ingredient_consumption = {
                'Tomato': 0.2,     # 200g per dish
                'Beef': 0.15,      # 150g per dish
                'Noodles': 0.1,    # 100g per dish
                'Egg': 0.05,       # 50g per dish
                'Rice': 0.08,      # 80g per dish
                'Chicken': 0.15,   # 150g per dish
                'Pork': 0.15,      # 150g per dish
                'Fish': 0.2,       # 200g per dish
                'Potato': 0.1,     # 100g per dish
                'Onion': 0.05,     # 50g per dish
                'Carrot': 0.05,    # 50g per dish
                'Cabbage': 0.1,    # 100g per dish
                'Oil': 0.02,       # 20ml per dish
                'Salt': 0.005,     # 5g per dish
                'Soy Sauce': 0.01, # 10ml per dish
            }
            
            # 扣减库存
            reduced_items = []
            for ingredient_name in ingredients:
                # 查找库存中对应的食材
                for item in self.inventory:
                    if item['name'].lower() == ingredient_name.lower():
                        # 计算需要扣减的数量
                        required_quantity = ingredient_consumption.get(ingredient_name, 0.1) * quantity
                        
                        # 扣减库存
                        old_stock = item['current_stock']
                        item['current_stock'] = max(0, item['current_stock'] - required_quantity)
                        item['updated_at'] = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
                        
                        reduced_items.append({
                            'name': ingredient_name,
                            'reduced': min(required_quantity, old_stock),
                            'new_stock': item['current_stock']
                        })
                        
                        print(f"✅ Reduced inventory: {ingredient_name} -{min(required_quantity, old_stock):.2f} (Remaining: {item['current_stock']:.2f})")
                        break
            
            # 保存库存变更
            self.save_inventory()
            
            # 创建库存扣减的财务记录（成本记录）
            total_cost = 0
            for item_info in reduced_items:
                for inv_item in self.inventory:
                    if inv_item['name'] == item_info['name']:
                        item_cost = item_info['reduced'] * inv_item.get('price', 0)
                        total_cost += item_cost
                        break
            
            if total_cost > 0:
                cost_record = {
                    'id': f"COST{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}",
                    'type': 'cost',
                    'amount': round(-total_cost, 2),  # negative for expense
                    'description': f"Meal Cost - {meal['name']} x{quantity}",
                    'meal_id': meal['id'],
                    'date': datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
                    'create_time': datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
                }
                self.financial_records.append(cost_record)
                self.save_financial_records()
                print(f"✅ Meal cost recorded: ¥{total_cost:.2f}")
            
            return True
            
        except Exception as e:
            print(f"❌ Inventory reduction failed: {e}")
            return False

# 创建全局数据管理器实例
data_manager = DataManager()
