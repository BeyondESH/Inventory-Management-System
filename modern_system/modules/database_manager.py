#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SQLite数据库管理器
替代JSON文件存储，提供完整的数据库操作接口
"""

import sqlite3
import os
import datetime
from typing import Dict, List, Any, Optional, Tuple
import hashlib
import json

class DatabaseManager:
    def __init__(self, db_path: str = None):
        """初始化数据库管理器"""
        if db_path is None:
            # 默认数据库路径
            current_dir = os.path.dirname(os.path.abspath(__file__))
            data_dir = os.path.join(os.path.dirname(current_dir), 'data')
            if not os.path.exists(data_dir):
                os.makedirs(data_dir)
            db_path = os.path.join(data_dir, 'factory_management.db')
        
        self.db_path = db_path
        self.connection = None
        self.init_database()
    
    def get_connection(self):
        """获取数据库连接"""
        if self.connection is None:
            self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
            self.connection.row_factory = sqlite3.Row  # 使查询结果可以通过列名访问
        return self.connection
    
    def close_connection(self):
        """关闭数据库连接"""
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def init_database(self):
        """初始化数据库，创建表结构"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # 读取SQL创建脚本
            sql_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(self.db_path))), 'sql', 'create_database.sql')
            
            if os.path.exists(sql_file_path):
                with open(sql_file_path, 'r', encoding='utf-8') as f:
                    sql_script = f.read()
                
                # 执行SQL脚本
                cursor.executescript(sql_script)
                conn.commit()
                print("✅ 数据库表结构创建成功")
                
                # 检查是否需要插入示例数据
                cursor.execute("SELECT COUNT(*) FROM Customer")
                if cursor.fetchone()[0] == 0:
                    self.insert_sample_data()
            else:
                print("⚠️ SQL脚本文件不存在，使用默认表结构")
                self.create_default_tables(cursor)
                conn.commit()
                
        except Exception as e:
            print(f"❌ 数据库初始化失败: {e}")
            raise
    
    def create_default_tables(self, cursor):
        """创建默认表结构（如果SQL文件不存在）"""
        # 这里可以添加基本的表结构创建代码
        pass
    
    def insert_sample_data(self):
        """插入示例数据"""
        try:
            sql_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(self.db_path))), 'sql', 'insert_sample_data.sql')
            
            if os.path.exists(sql_file_path):
                conn = self.get_connection()
                cursor = conn.cursor()
                
                with open(sql_file_path, 'r', encoding='utf-8') as f:
                    sql_script = f.read()
                
                cursor.executescript(sql_script)
                conn.commit()
                print("✅ 示例数据插入成功")
            else:
                print("⚠️ 示例数据文件不存在")
                
        except Exception as e:
            print(f"❌ 插入示例数据失败: {e}")
    
    # ==================== 用户管理 ====================
    def create_user(self, user_data: Dict) -> int:
        """创建新用户"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # 密码哈希
            password_hash = hashlib.sha256(user_data.get('password', '').encode()).hexdigest()
            
            cursor.execute("""
                INSERT INTO Customer (first_name, last_name, customer_phone, customer_email, 
                                    customer_address, payment_method_id, password_hash)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                user_data.get('first_name', ''),
                user_data.get('last_name', ''),
                user_data.get('phone', ''),
                user_data.get('email', ''),
                user_data.get('address', ''),
                user_data.get('payment_method_id'),
                password_hash
            ))
            
            conn.commit()
            return cursor.lastrowid
            
        except Exception as e:
            print(f"❌ 创建用户失败: {e}")
            raise
    
    def verify_user(self, email: str, password: str) -> Optional[Dict]:
        """验证用户登录"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            
            cursor.execute("""
                SELECT customer_id, first_name, last_name, customer_email, customer_phone, 
                       customer_address, payment_method_id
                FROM Customer 
                WHERE customer_email = ? AND password_hash = ?
            """, (email, password_hash))
            
            row = cursor.fetchone()
            if row:
                return dict(row)
            return None
            
        except Exception as e:
            print(f"❌ 用户验证失败: {e}")
            return None
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict]:
        """根据ID获取用户信息"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT customer_id, first_name, last_name, customer_email, customer_phone, 
                       customer_address, payment_method_id
                FROM Customer 
                WHERE customer_id = ?
            """, (user_id,))
            
            row = cursor.fetchone()
            return dict(row) if row else None
            
        except Exception as e:
            print(f"❌ 获取用户信息失败: {e}")
            return None
    
    # ==================== 餐食管理 ====================
    def get_meals(self, active_only=False) -> List[Dict]:
        """获取菜品列表"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            query = "SELECT * FROM Meal"
            params = []

            if active_only:
                query += " WHERE isActive = 1"

            cursor.execute(query)
            meals = [dict(row) for row in cursor.fetchall()]

            # 兼容UI字段
            for meal in meals:
                meal['id'] = meal.get('meal_id')
                meal['name'] = meal.get('meal_name')
                meal['is_available'] = meal.get('isActive')

            return meals
        except Exception as e:
            print(f"❌ 获取菜品列表失败: {e}")
            return []

    def add_meal(self, data: Dict) -> int:
        """添加新菜品"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Meal (meal_name, meal_category, meal_price, meal_cost, meal_details, isActive)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                data['name'], data['category'], data['price'], data['cost'],
                data['description'], data.get('is_available', True)
            ))
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"❌ 添加菜品失败: {e}")
            raise e

    def update_meal(self, meal_id: int, data: Dict):
        """更新菜品信息"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            db_data = {
                'meal_name': data.get('name'),
                'meal_category': data.get('category'),
                'meal_price': data.get('price'),
                'meal_cost': data.get('cost'),
                'meal_details': data.get('description'),
                'isActive': data.get('is_available')
            }
            
            set_clause = ", ".join([f"{key} = ?" for key, val in db_data.items() if val is not None])
            values = [val for val in db_data.values() if val is not None]

            if not set_clause:
                return

            values.append(meal_id)
            query = f"UPDATE Meal SET {set_clause} WHERE meal_id = ?"
            cursor.execute(query, values)
            conn.commit()
        except Exception as e:
            print(f"❌ 更新菜品失败: {e}")
            raise e

    def delete_meal(self, meal_id: int):
        """删除菜品"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            # 检查是否有关联的订单项
            cursor.execute("SELECT COUNT(*) FROM OrderItem WHERE meal_id = ?", (meal_id,))
            if cursor.fetchone()[0] > 0:
                raise ValueError("无法删除，该菜品已被用于订单中")
            
            # 删除关联的配方
            cursor.execute("DELETE FROM RecipeIngredient WHERE meal_id = ?", (meal_id,))
            # 删除菜品
            cursor.execute("DELETE FROM Meal WHERE meal_id = ?", (meal_id,))
            conn.commit()
        except Exception as e:
            print(f"❌ 删除菜品失败: {e}")
            raise e
            
    def update_meal_recipe(self, meal_id: int, ingredients: List[Dict]):
        """更新菜品的配方"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            conn.execute("BEGIN")
            
            # 1. 删除旧配方
            cursor.execute("DELETE FROM RecipeIngredient WHERE meal_id = ?", (meal_id,))
            
            # 2. 插入新配方
            for ing in ingredients:
                # 'id' 是 ingredient_id
                cursor.execute("""
                    INSERT INTO RecipeIngredient (meal_id, ingredient_id, quantity_required)
                    VALUES (?, ?, ?)
                """, (meal_id, ing['id'], ing['quantity']))
            
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(f"❌ 更新配方失败: {e}")
            raise e
    
    # ==================== 库存管理 ====================
    def get_inventory(self) -> List[Dict]:
        """获取所有库存原材料"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Ingredient ORDER BY ingredient_name")
            # 在返回前，为UI兼容性统一字段名
            inventory = []
            for row in cursor.fetchall():
                item = dict(row)
                item['id'] = item['ingredient_id']
                item['name'] = item['ingredient_name']
                item['quantity'] = item['current_stock']
                item['update_time'] = item['last_updated']
                inventory.append(item)
            return inventory
        except Exception as e:
            print(f"❌ 获取库存列表失败: {e}")
            return []

    def add_ingredient(self, data: Dict) -> int:
        """添加新的库存原材料"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Ingredient (ingredient_name, category, current_stock, min_stock, max_stock, unit, price, supplier)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                data['name'], data['category'], data['current_stock'],
                data['min_stock'], data['max_stock'], data['unit'],
                data['price'], data['supplier']
            ))
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"❌ 添加原材料失败: {e}")
            raise e

    def update_ingredient(self, ingredient_id: int, data: Dict):
        """更新原材料信息"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            # 从data字典中安全地获取值，如果键不存在则不更新该字段
            fields = ['ingredient_name', 'category', 'current_stock', 'min_stock', 'max_stock', 'unit', 'price', 'supplier', 'last_updated']
            
            # 为了UI兼容性，将name和current_stock等UI字段名转为数据库字段名
            db_data = {
                'ingredient_name': data.get('name'),
                'category': data.get('category'),
                'current_stock': data.get('current_stock'),
                'min_stock': data.get('min_stock'),
                'max_stock': data.get('max_stock'),
                'unit': data.get('unit'),
                'price': data.get('price'),
                'supplier': data.get('supplier'),
                'last_updated': datetime.date.today().isoformat() # 总是更新为今天
            }

            set_clause = ", ".join([f"{key} = ?" for key, val in db_data.items() if val is not None])
            values = [val for val in db_data.values() if val is not None]
            
            if not set_clause:
                print("⚠️ 无可更新字段")
                return

            values.append(ingredient_id)
            query = f"UPDATE Ingredient SET {set_clause} WHERE ingredient_id = ?"
            
            cursor.execute(query, values)
            conn.commit()
        except Exception as e:
            print(f"❌ 更新原材料失败: {e}")
            raise e

    def delete_ingredient(self, ingredient_id: int):
        """删除原材料"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            # 检查是否有关联的配方
            cursor.execute("SELECT COUNT(*) FROM RecipeIngredient WHERE ingredient_id = ?", (ingredient_id,))
            if cursor.fetchone()[0] > 0:
                raise ValueError("无法删除，该原材料已被用于配方中")
            
            cursor.execute("DELETE FROM Ingredient WHERE ingredient_id = ?", (ingredient_id,))
            conn.commit()
        except Exception as e:
            print(f"❌ 删除原材料失败: {e}")
            raise e
    
    def get_recipes(self) -> List[Dict]:
        """获取所有菜品的配方"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            # 获取所有菜品
            cursor.execute("SELECT meal_id, meal_name FROM Meal")
            meals = cursor.fetchall()
            
            recipes = []
            for meal in meals:
                cursor.execute("""
                    SELECT i.ingredient_name, ri.quantity_required, i.unit
                    FROM RecipeIngredient ri
                    JOIN Ingredient i ON ri.ingredient_id = i.ingredient_id
                    WHERE ri.meal_id = ?
                """, (meal['meal_id'],))
                ingredients = [dict(row) for row in cursor.fetchall()]
                
                # 兼容旧格式，转换字段名
                formatted_ingredients = [
                    {'ingredient_name': ing['ingredient_name'], 'quantity_per_serving': ing['quantity_required'], 'unit': ing['unit']}
                    for ing in ingredients
                ]

                if formatted_ingredients:
                    recipes.append({
                        'meal_id': meal['meal_id'],
                        'meal_name': meal['meal_name'],
                        'ingredients': formatted_ingredients
                    })
            return recipes
        except Exception as e:
            print(f"❌ 获取配方列表失败: {e}")
            return []
    
    def get_containers(self) -> List[Dict]:
        """获取容器列表"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM Container 
                ORDER BY container_type
            """)
            
            return [dict(row) for row in cursor.fetchall()]
            
        except Exception as e:
            print(f"❌ 获取容器列表失败: {e}")
            return []
    
    def update_inventory_stock(self, ingredient_id: int, quantity_change: float) -> bool:
        """更新库存数量"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE Ingredient 
                SET ingredient_current_stock = ingredient_current_stock + ?
                WHERE ingredient_id = ?
            """, (quantity_change, ingredient_id))
            
            conn.commit()
            return cursor.rowcount > 0
            
        except Exception as e:
            print(f"❌ 更新库存失败: {e}")
            return False
    
    def update_container_stock(self, container_id: int, quantity_change: int) -> bool:
        """更新容器库存"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE Container 
                SET container_current_stock = container_current_stock + ?
                WHERE container_id = ?
            """, (quantity_change, container_id))
            
            conn.commit()
            return cursor.rowcount > 0
            
        except Exception as e:
            print(f"❌ 更新容器库存失败: {e}")
            return False
    
    def get_low_stock_items(self, threshold: float = 10) -> List[Dict]:
        """获取低库存项目"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM Ingredient 
                WHERE ingredient_current_stock <= ingredient_reorder_threshold
                ORDER BY ingredient_current_stock
            """)
            
            return [dict(row) for row in cursor.fetchall()]
            
        except Exception as e:
            print(f"❌ 获取低库存项目失败: {e}")
            return []
    
    # ==================== 订单管理 ====================
    def create_order(self, order_data: Dict) -> int:
        """
        创建新订单（包含多个订单项），并自动扣减库存。
        使用事务确保操作的原子性。
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            conn.execute("BEGIN")

            # 1. 检查所有菜品的库存是否充足
            for item in order_data['items']:
                is_sufficient = self.check_inventory_for_meal(item['id'], item['quantity'], cursor)
                if not is_sufficient:
                    raise ValueError(f"库存不足，无法制作菜品: {item['name']}")

            # 2. 创建主订单 (Order)
            cursor.execute("""
                INSERT INTO "Order" (customer_id, employee_id, payment_method_id, delivery_date, order_status, note, total_amount)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                order_data.get('customer_id', 1),
                order_data.get('employee_id', 1),
                order_data.get('payment_method_id', 1),
                order_data.get('delivery_date', datetime.date.today().isoformat()),
                order_data.get('order_status', '待接单'),
                order_data.get('note', ''),
                order_data.get('total_amount', 0)
            ))
            order_id = cursor.lastrowid

            # 3. 创建订单项 (OrderItem) 并扣减库存
            for item in order_data['items']:
                # 创建订单项
                cursor.execute("""
                    INSERT INTO OrderItem (order_id, meal_id, quantity, price)
                    VALUES (?, ?, ?, ?)
                """, (order_id, item['id'], item['quantity'], item['price']))
                
                # 扣减库存
                self.reduce_inventory_for_meal(item['id'], item['quantity'], cursor)

            conn.commit()
            print(f"✅ 订单 {order_id} 创建成功，并已扣减库存。")
            return order_id

        except Exception as e:
            conn.rollback()
            print(f"❌ 创建订单失败，事务已回滚: {e}")
            # 抛出异常，以便上层可以捕获
            raise e

    def check_inventory_for_meal(self, meal_id: int, quantity: int, cursor) -> bool:
        """(在事务中)检查单个菜品的所有原料库存是否充足"""
        # 获取菜品的配方
        cursor.execute("""
            SELECT i.ingredient_id, i.ingredient_name, ri.quantity_required
            FROM RecipeIngredient ri
            JOIN Ingredient i ON ri.ingredient_id = i.ingredient_id
            WHERE ri.meal_id = ?
        """, (meal_id,))
        ingredients = cursor.fetchall()
        
        if not ingredients:
            # 如果没有配方，默认认为库存充足
            return True
            
        for ingredient in ingredients:
            required_qty = ingredient['quantity_required'] * quantity
            # 检查库存
            cursor.execute("SELECT current_stock FROM Inventory WHERE ingredient_id = ?", (ingredient['ingredient_id'],))
            stock_row = cursor.fetchone()
            if not stock_row or stock_row['current_stock'] < required_qty:
                return False
        return True

    def reduce_inventory_for_meal(self, meal_id: int, quantity: int, cursor):
        """(在事务中)根据配方扣减单个菜品的原料库存"""
        cursor.execute("""
            SELECT i.ingredient_id, ri.quantity_required
            FROM RecipeIngredient ri
            JOIN Ingredient i ON ri.ingredient_id = i.ingredient_id
            WHERE ri.meal_id = ?
        """, (meal_id,))
        ingredients = cursor.fetchall()
        
        for ingredient in ingredients:
            quantity_to_reduce = ingredient['quantity_required'] * quantity
            cursor.execute("""
                UPDATE Inventory SET current_stock = current_stock - ? 
                WHERE ingredient_id = ?
            """, (quantity_to_reduce, ingredient['ingredient_id']))

    def get_orders(self, status_filter: str = None) -> List[Dict]:
        """获取订单列表，并附带订单项"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            query = 'SELECT * FROM "Order"'
            params = []
            
            if status_filter and status_filter != '全部':
                query += " WHERE order_status = ?"
                params.append(status_filter)
            
            query += " ORDER BY order_date DESC"
            
            cursor.execute(query, params)
            orders = [dict(row) for row in cursor.fetchall()]
            
            # 为每个订单获取其订单项
            for order in orders:
                cursor.execute("""
                    SELECT oi.quantity, oi.price, m.meal_name, m.image 
                    FROM OrderItem oi
                    JOIN Meal m ON oi.meal_id = m.meal_id
                    WHERE oi.order_id = ?
                """, (order['order_id'],))
                order['items'] = [dict(row) for row in cursor.fetchall()]
                # 兼容旧UI的字段
                order['id'] = order['order_id']
                order['status'] = order['order_status']
                order['create_time'] = order['order_date']
                order['total'] = order['total_amount']
                order['customer'] = f"客户ID: {order['customer_id']}"
                order['phone'] = "" # 数据库中没有存，暂时为空
                order['address'] = "" # 数据库中没有存，暂时为空
                order['meals'] = [{
                    'name': item['meal_name'],
                    'quantity': item['quantity'],
                    'price': item['price']
                } for item in order['items']]


            return orders
            
        except Exception as e:
            print(f"❌ 获取订单列表失败: {e}")
            return []
    
    def update_order_status(self, order_id: int, new_status: str) -> bool:
        """更新订单状态"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE "Order" 
                SET order_status = ?, updated_at = CURRENT_TIMESTAMP
                WHERE order_id = ?
            """, (new_status, order_id))
            
            conn.commit()
            return cursor.rowcount > 0
            
        except Exception as e:
            print(f"❌ 更新订单状态失败: {e}")
            return False
    
    # ==================== 客户管理 ====================
    def get_customers(self) -> List[Dict]:
        """获取客户列表，并聚合订单信息"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    c.customer_id, c.first_name, c.last_name, c.customer_phone, c.customer_address,
                    COUNT(o.order_id) as total_orders,
                    SUM(o.total_amount) as total_amount
                FROM Customer c
                LEFT JOIN "Order" o ON c.customer_id = o.customer_id
                GROUP BY c.customer_id
                ORDER BY total_amount DESC
            """)
            customers = []
            for row in cursor.fetchall():
                item = dict(row)
                item['id'] = item.get('customer_id')
                item['name'] = f"{item.get('first_name', '')} {item.get('last_name', '')}".strip()
                item['phone'] = item.get('customer_phone')
                item['address'] = item.get('customer_address')
                item['total_amount'] = item.get('total_amount') or 0
                customers.append(item)
            return customers
        except Exception as e:
            print(f"❌ 获取客户列表失败: {e}")
            return []

    def add_customer(self, data: Dict) -> int:
        """添加新客户"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Customer (first_name, last_name, customer_phone, customer_address)
                VALUES (?, ?, ?, ?)
            """, (data.get('first_name', ''), data.get('last_name', ''), data.get('phone'), data.get('address')))
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"❌ 添加客户失败: {e}")
            raise e

    def update_customer(self, customer_id: int, data: Dict):
        """更新客户信息"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE Customer SET first_name=?, last_name=?, customer_phone=?, customer_address=?
                WHERE customer_id = ?
            """, (
                data.get('first_name', ''), data.get('last_name', ''),
                data.get('phone'), data.get('address'), customer_id
            ))
            conn.commit()
        except Exception as e:
            print(f"❌ 更新客户失败: {e}")
            raise e

    def delete_customer(self, customer_id: int):
        """删除客户"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            # 检查关联订单
            cursor.execute("SELECT COUNT(*) FROM \"Order\" WHERE customer_id = ?", (customer_id,))
            if cursor.fetchone()[0] > 0:
                raise ValueError("无法删除，该客户已有订单记录。请先处理相关订单。")
            cursor.execute("DELETE FROM Customer WHERE customer_id = ?", (customer_id,))
            conn.commit()
        except Exception as e:
            print(f"❌ 删除客户失败: {e}")
            raise e
    
    # ==================== 财务管理 ====================
    def get_financial_records(self, time_range: str = '全部', record_type: str = '全部') -> List[Dict]:
        """获取财务记录"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            query = "SELECT * FROM FinancialRecord WHERE 1=1"
            params = []

            if time_range == '今日':
                query += " AND DATE(record_date) = DATE('now')"
            elif time_range == '本周':
                query += " AND DATE(record_date) >= DATE('now', '-7 days')"
            elif time_range == '本月':
                query += " AND STRFTIME('%Y-%m', record_date) = STRFTIME('%Y-%m', 'now')"

            if record_type != '全部':
                query += " AND record_type = ?"
                params.append(record_type)
            
            query += " ORDER BY record_date DESC"
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            print(f"❌ 获取财务记录失败: {e}")
            return []

    def add_financial_record(self, data: Dict):
        """添加财务记录"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO FinancialRecord (record_type, amount, description, record_date)
                VALUES (?, ?, ?, ?)
            """, (data['type'], data['amount'], data['description'], data.get('date', datetime.datetime.now())))
            conn.commit()
        except Exception as e:
            print(f"❌ 添加财务记录失败: {e}")
            raise e

    def get_fixed_costs(self) -> List[Dict]:
        """获取所有固定成本"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM FixedCost ORDER BY cost_name")
            return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            print(f"❌ 获取固定成本失败: {e}")
            return []
            
    def add_fixed_cost(self, data: Dict):
        """添加固定成本"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO FixedCost (cost_name, cost_category, amount, payment_cycle, next_payment_date, status, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                data['name'], data['category'], data['amount'], data['cycle'],
                data['next_date'], data.get('status', '未支付'), data.get('notes', '')
            ))
            conn.commit()
        except Exception as e:
            print(f"❌ 添加固定成本失败: {e}")
            raise e

    def update_fixed_cost(self, cost_id: int, data: Dict):
        """更新固定成本"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE FixedCost SET 
                    cost_name = ?, cost_category = ?, amount = ?, 
                    payment_cycle = ?, next_payment_date = ?, status = ?, notes = ?
                WHERE cost_id = ?
            """, (
                data['name'], data['category'], data['amount'], data['cycle'],
                data['next_date'], data.get('status', '未支付'), data.get('notes', ''),
                cost_id
            ))
            conn.commit()
        except Exception as e:
            print(f"❌ 更新固定成本失败: {e}")
            raise e

    def delete_fixed_cost(self, cost_id: int):
        """删除固定成本"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM FixedCost WHERE cost_id = ?", (cost_id,))
            conn.commit()
        except Exception as e:
            print(f"❌ 删除固定成本失败: {e}")
            raise e
        
    def get_finance_summary(self) -> Dict:
        """获取财务概览统计"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            summary = {
                'today_income': 0, 'today_expense': 0,
                'month_income': 0, 'month_expense': 0,
            }

            # 今日
            cursor.execute("SELECT record_type, SUM(amount) FROM FinancialRecord WHERE DATE(record_date) = DATE('now') GROUP BY record_type")
            for row in cursor.fetchall():
                if row['record_type'] == '收入':
                    summary['today_income'] = row[1]
                else:
                    summary['today_expense'] = row[1]
            
            # 本月
            cursor.execute("SELECT record_type, SUM(amount) FROM FinancialRecord WHERE STRFTIME('%Y-%m', record_date) = STRFTIME('%Y-%m', 'now') GROUP BY record_type")
            for row in cursor.fetchall():
                if row['record_type'] == '收入':
                    summary['month_income'] = row[1]
                else:
                    summary['month_expense'] = row[1]
            
            summary['today_profit'] = summary['today_income'] - summary['today_expense']
            summary['month_profit'] = summary['month_income'] - summary['month_expense']
            
            return summary
        except Exception as e:
            print(f"❌ 获取财务概览失败: {e}")
            return {}
    
    # ==================== 支付方式管理 ====================
    def get_payment_methods(self) -> List[Dict]:
        """获取支付方式列表"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM Payment_method ORDER BY method_name")
            return [dict(row) for row in cursor.fetchall()]
            
        except Exception as e:
            print(f"❌ 获取支付方式失败: {e}")
            return []
    
    # ==================== 员工管理 ====================
    def get_employees(self) -> List[Dict]:
        """获取员工列表"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Employee ORDER BY first_name, last_name")
            employees = []
            for row in cursor.fetchall():
                item = dict(row)
                item['id'] = item['employee_id']
                item['name'] = f"{item.get('first_name', '')} {item.get('last_name', '')}".strip()
                employees.append(item)
            return employees
        except Exception as e:
            print(f"❌ 获取员工列表失败: {e}")
            return []

    def add_employee(self, data: Dict):
        """添加新员工"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Employee (first_name, last_name, position, department, phone, email, hire_date, salary, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                data.get('first_name'), data.get('last_name'), data.get('position'),
                data.get('department'), data.get('phone'), data.get('email'),
                data.get('hire_date'), data.get('salary'), data.get('status', '在职')
            ))
            conn.commit()
        except Exception as e:
            print(f"❌ 添加员工失败: {e}")
            raise e

    def update_employee(self, employee_id: int, data: Dict):
        """更新员工信息"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            # 动态构建SET子句
            set_clause = ", ".join([f"{key} = ?" for key in data.keys()])
            values = list(data.values())
            values.append(employee_id)
            
            query = f"UPDATE Employee SET {set_clause} WHERE employee_id = ?"
            cursor.execute(query, values)
            conn.commit()
        except Exception as e:
            print(f"❌ 更新员工失败: {e}")
            raise e

    def delete_employee(self, employee_id: int):
        """删除员工(逻辑删除，标记为离职)"""
        try:
            self.update_employee(employee_id, {'status': '离职'})
        except Exception as e:
            print(f"❌ 逻辑删除员工失败: {e}")
            raise e

# 创建全局数据库管理器实例
database_manager = DatabaseManager()
