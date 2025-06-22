#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Data Management Center - Responsible for data synchronization and linkage between modules
Implements data interaction between orders, inventory, finance and other modules
"""

import json
import os
import datetime
from typing import Dict, List, Any, Optional
from threading import Lock
import uuid

class DataManager:
    """Data Management Center Singleton Class"""
    
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
        self.registered_modules = {}  # Store registered module instances
        self.event_listeners = {}
        
        # Initialize data files
        self.data_files = {
            'orders': 'orders.json',
            'inventory': 'inventory.json',
            'meals': 'meals.json',
            'customers': 'customers.json',
            'employees': 'employees.json',
            'finance': 'finance.json',
            'sales': 'sales.json'
        }
        
        # Ensure data files exist
        self._init_data_files()
    
    def _get_data_dir(self):
        """Get data directory"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        data_dir = os.path.join(project_root, 'modern_system', 'data')
        
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        
        return data_dir
    
    def _init_data_files(self):
        """Initialize data files"""
        default_data = {
            'orders': [],
            'inventory': [
                {"id": "INV001", "name": "Tomato", "category": "Vegetables", "quantity": 50, "unit": "kg", "price": 8.0, "min_stock": 10},
                {"id": "INV002", "name": "Beef", "category": "Meat", "quantity": 20, "unit": "kg", "price": 68.0, "min_stock": 5},
                {"id": "INV003", "name": "Noodles", "category": "Staple Food", "quantity": 100, "unit": "pack", "price": 3.5, "min_stock": 20},
                {"id": "INV004", "name": "Cola", "category": "Beverages", "quantity": 80, "unit": "bottle", "price": 5.0, "min_stock": 30}
            ],
            'meals': [
                {"id": "MEAL001", "name": "Tomato Beef Noodles", "category": "Noodles", "price": 25.0, "cost": 15.0, "ingredients": ["Tomato", "Beef", "Noodles"]},
                {"id": "MEAL002", "name": "Egg Fried Rice", "category": "Fried Rice", "price": 18.0, "cost": 10.0, "ingredients": ["Egg", "Rice"]},
                {"id": "MEAL003", "name": "Beef Burger", "category": "Western", "price": 32.0, "cost": 20.0, "ingredients": ["Beef", "Bread", "Lettuce"]},
                {"id": "MEAL004", "name": "French Fries", "category": "Snacks", "price": 12.0, "cost": 6.0, "ingredients": ["Potato"]}
            ],
            'customers': [
                {"id": "CUST001", "name": "Zhang San", "phone": "138****1234", "address": "No.1 Street, Chaoyang District, Beijing", "total_orders": 15, "total_amount": 1580.0},
                {"id": "CUST002", "name": "Li Si", "phone": "139****5678", "address": "No.88 Road, Haidian District, Beijing", "total_orders": 8, "total_amount": 890.0},
                {"id": "CUST003", "name": "Wang Wu", "phone": "136****9012", "address": "No.66 Alley, Xicheng District, Beijing", "total_orders": 12, "total_amount": 1250.0}
            ],
            'employees': [
                {"id": "EMP001", "name": "Administrator", "position": "Manager", "department": "Management", "phone": "188****0001", "salary": 8000, "hire_date": "2023-01-01"},
                {"id": "EMP002", "name": "Chef Wang", "position": "Chef", "department": "Kitchen", "phone": "188****0002", "salary": 6000, "hire_date": "2023-03-15"},
                {"id": "EMP003", "name": "Server Li", "position": "Waiter", "department": "Front Desk", "phone": "188****0003", "salary": 4500, "hire_date": "2023-06-01"}
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
        """Register module"""
        self.modules[module_type] = instance
        # Also save to registered_modules
        if not hasattr(self, 'registered_modules'):
            self.registered_modules = {}
        self.registered_modules[module_type] = instance
        print(f"Registered module: {module_type}")
    
    def notify_modules(self, event_type: str):
        """Notify registered modules"""
        if hasattr(self, 'registered_modules'):
            for module_type, module_instance in self.registered_modules.items():
                if event_type == 'meals_updated' and hasattr(module_instance, 'refresh_meals_data'):
                    try:
                        module_instance.refresh_meals_data()
                        print(f"Notified {module_type} module to refresh meal data")
                    except Exception as e:
                        print(f"Failed to notify {module_type} module: {e}")
    
    def subscribe_event(self, event_type: str, callback):
        """Subscribe to event"""
        if event_type not in self.event_listeners:
            self.event_listeners[event_type] = []
        self.event_listeners[event_type].append(callback)
    
    def emit_event(self, event_type: str, data: Any):
        """Emit event"""
        if event_type in self.event_listeners:
            for callback in self.event_listeners[event_type]:
                try:
                    callback(data)
                except Exception as e:
                    print(f"Event handling error {event_type}: {e}")
    
    def load_data(self, data_type: str) -> List[Dict]:
        """Load data"""
        if data_type not in self.data_files:
            return []
        
        file_path = os.path.join(self.data_dir, self.data_files[data_type])
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Failed to load data {data_type}: {e}")
            return []
    
    def save_data(self, data_type: str, data: List[Dict]):
        """Save data"""
        if data_type not in self.data_files:
            return False
        
        file_path = os.path.join(self.data_dir, self.data_files[data_type])
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Failed to save data {data_type}: {e}")
            return False
    
    # Order related methods
    def get_orders(self, status_filter: Optional[str] = None) -> List[Dict]:
        """Get order list"""
        orders = self.load_data('orders')
        if status_filter:
            orders = [order for order in orders if order.get('status') == status_filter]
        return orders
    
    def add_order(self, order_data: Dict) -> str:
        """Add order"""
        orders = self.load_data('orders')
        
        # Generate order ID
        order_id = f"ORD{datetime.datetime.now().strftime('%Y%m%d')}{len(orders)+1:04d}"
        order_data['id'] = order_id
        order_data['create_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        orders.append(order_data)
        self.save_data('orders', orders)
        
        # Deduct inventory
        self._deduct_inventory(order_data.get('items', []))
        
        # Record sales data
        self._record_sale(order_data)
        
        # Record finance data
        self._record_finance(order_data)
        
        # Emit event
        self.emit_event('order_added', order_data)
        
        return order_id
    
    def update_order_status(self, order_id: str, new_status: str) -> bool:
        """Update order status"""
        orders = self.load_data('orders')
        
        for order in orders:
            if order.get('id') == order_id:
                old_status = order.get('status')
                order['status'] = new_status
                order['update_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                self.save_data('orders', orders)
                
                # Emit event
                self.emit_event('order_status_changed', {
                    'order_id': order_id,
                    'old_status': old_status,
                    'new_status': new_status,
                    'order': order
                })
                
                return True
        
        return False
    
    def _deduct_inventory(self, order_items: List[Dict]):
        """Deduct inventory"""
        inventory = self.load_data('inventory')
        meals = self.load_data('meals')
        
        # Create inventory lookup dictionary
        inventory_dict = {item['name']: item for item in inventory}
        meals_dict = {meal['name']: meal for meal in meals}
        
        for order_item in order_items:
            meal_name = order_item.get('name')
            quantity = order_item.get('quantity', 1)
            
            if meal_name in meals_dict:
                meal = meals_dict[meal_name]
                ingredients = meal.get('ingredients', [])
                
                # Deduct ingredient inventory
                for ingredient in ingredients:
                    if ingredient in inventory_dict:
                        inventory_dict[ingredient]['quantity'] -= quantity
                        if inventory_dict[ingredient]['quantity'] < 0:
                            inventory_dict[ingredient]['quantity'] = 0
        
        # Save updated inventory
        updated_inventory = list(inventory_dict.values())
        self.save_data('inventory', updated_inventory)
        
        # Emit inventory update event
        self.emit_event('inventory_updated', updated_inventory)
    
    def _record_sale(self, order_data: Dict):
        """Record sales data"""
        sales = self.load_data('sales')
        
        sale_record = {
            'order_id': order_data.get('id'),
            'sale_time': order_data.get('create_time'),
            'total_amount': order_data.get('total_amount'),
            'items': order_data.get('items')
        }
        
        sales.append(sale_record)
        self.save_data('sales', sales)
    
    def _record_finance(self, order_data: Dict):
        """Record financial data"""
        finance = self.load_data('finance')
        
        finance_record = {
            'id': f"FIN-{order_data.get('id')}",
            'date': datetime.datetime.now().strftime('%Y-%m-%d'),
            'type': 'Income',
            'amount': order_data.get('total_amount', 0),
            'category': 'Sales',
            'description': f"Order {order_data.get('id')}",
            'recorded_by': 'System'
        }
        
        finance.append(finance_record)
        self.save_data('finance', finance)
    
    # Inventory related methods
    def get_inventory(self) -> List[Dict]:
        """Get full inventory list"""
        return self.load_data('inventory')
    
    def update_inventory(self, item_id: str, new_data: Dict) -> bool:
        """Update a specific inventory item"""
        inventory = self.load_data('inventory')
        for item in inventory:
            if item.get('id') == item_id:
                item.update(new_data)
                item['update_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                return self.save_data('inventory', inventory)
        return False
    
    def add_inventory_item(self, item_data: Dict) -> bool:
        """Add a new item to inventory"""
        inventory = self.load_data('inventory')
        item_data['id'] = f"INV{int(datetime.datetime.now().timestamp())}"
        inventory.append(item_data)
        return self.save_data('inventory', inventory)
    
    def delete_inventory_item(self, item_id: str) -> bool:
        """Delete an item from inventory"""
        inventory = self.load_data('inventory')
        original_length = len(inventory)
        inventory = [item for item in inventory if item.get('id') != item_id]
        if len(inventory) < original_length:
            return self.save_data('inventory', inventory)
        return False
    
    # Customer related methods
    def get_customers(self) -> List[Dict]:
        """Get customer list"""
        return self.load_data('customers')
    
    def add_customer(self, customer_data: Dict) -> bool:
        """Add a new customer"""
        customers = self.load_data('customers')
        customer_data['id'] = f"CUST{int(datetime.datetime.now().timestamp())}"
        customers.append(customer_data)
        return self.save_data('customers', customers)
    
    def update_customer(self, customer_id: str, customer_data: Dict) -> bool:
        """Update customer information"""
        customers = self.load_data('customers')
        for customer in customers:
            if customer.get('id') == customer_id:
                customer.update(customer_data)
                return self.save_data('customers', customers)
        return False
    
    def delete_customer(self, customer_id: str) -> bool:
        """Delete a customer"""
        customers = self.load_data('customers')
        original_length = len(customers)
        customers = [c for c in customers if c.get('id') != customer_id]
        if len(customers) < original_length:
            return self.save_data('customers', customers)
        return False
    
    # Finance related methods
    def get_finance_records(self) -> List[Dict]:
        """Get all finance records"""
        return self.load_data('finance')
    
    def add_finance_record(self, record_data: Dict) -> bool:
        """Add a new finance record"""
        finance_records = self.load_data('finance')
        record_data['id'] = f"FIN{int(datetime.datetime.now().timestamp())}"
        finance_records.append(record_data)
        return self.save_data('finance', finance_records)
    
    def update_finance_record(self, record_id: str, record_data: Dict) -> bool:
        """Update a finance record"""
        finance_records = self.load_data('finance')
        for record in finance_records:
            if record.get('id') == record_id:
                record.update(record_data)
                return self.save_data('finance', finance_records)
        return False
    
    def delete_finance_record(self, record_id: str) -> bool:
        """Delete a finance record"""
        finance_records = self.load_data('finance')
        original_length = len(finance_records)
        finance_records = [r for r in finance_records if r.get('id') != record_id]
        if len(finance_records) < original_length:
            return self.save_data('finance', finance_records)
        return False
    
    # Statistics related methods
    def get_low_stock_items(self) -> List[Dict]:
        """Get items with low stock"""
        inventory = self.load_data('inventory')
        return [item for item in inventory if item.get('quantity', 0) <= item.get('min_stock', 0)]
    
    def get_daily_revenue(self, date: str = None) -> float:
        """Get daily revenue"""
        if date is None:
            date = datetime.datetime.now().strftime('%Y-%m-%d')
        
        orders = self.load_data('orders')
        total = sum(o.get('total_amount', 0) for o in orders if o.get('create_time', '').startswith(date))
        return total
    
    def get_dashboard_stats(self) -> Dict:
        """Get key statistics for the dashboard"""
        orders = self.load_data('orders')
        today_str = datetime.datetime.now().strftime('%Y-%m-%d')
        
        today_orders = [o for o in orders if o.get('create_time', '').startswith(today_str)]
        
        stats = {
            "today_revenue": sum(o.get('total_amount', 0) for o in today_orders),
            "today_orders": len(today_orders),
            "total_customers": len(self.load_data('customers')),
            "low_stock_items": len(self.get_low_stock_items())
        }
        return stats

# Create global singleton instance
data_manager = DataManager()
