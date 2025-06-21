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
    def get_meals(self, active_only: bool = True) -> List[Dict]:
        """获取餐食列表"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            if active_only:
                cursor.execute("SELECT * FROM Meal WHERE isActive = 1 ORDER BY meal_name")
            else:
                cursor.execute("SELECT * FROM Meal ORDER BY meal_name")
            
            return [dict(row) for row in cursor.fetchall()]
            
        except Exception as e:
            print(f"❌ 获取餐食列表失败: {e}")
            return []
    
    def create_meal(self, meal_data: Dict) -> int:
        """创建新餐食"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO Meal (meal_name, meal_details, meal_price, isActive)
                VALUES (?, ?, ?, ?)
            """, (
                meal_data.get('name'),
                meal_data.get('details', ''),
                meal_data.get('price', 0),
                meal_data.get('isActive', True)
            ))
            
            meal_id = cursor.lastrowid
            
            # 添加餐食容器关联
            containers = meal_data.get('containers', [])
            for container in containers:
                cursor.execute("""
                    INSERT INTO Meal_container (meal_id, container_id, container_required_quantity)
                    VALUES (?, ?, ?)
                """, (meal_id, container['container_id'], container['quantity']))
            
            conn.commit()
            return meal_id
            
        except Exception as e:
            print(f"❌ 创建餐食失败: {e}")
            raise
    
    def update_meal(self, meal_id: int, meal_data: Dict) -> bool:
        """更新餐食信息"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE Meal 
                SET meal_name = ?, meal_details = ?, meal_price = ?, isActive = ?, updated_at = CURRENT_TIMESTAMP
                WHERE meal_id = ?
            """, (
                meal_data.get('name'),
                meal_data.get('details', ''),
                meal_data.get('price', 0),
                meal_data.get('isActive', True),
                meal_id
            ))
            
            conn.commit()
            return cursor.rowcount > 0
            
        except Exception as e:
            print(f"❌ 更新餐食失败: {e}")
            return False
    
    def delete_meal(self, meal_id: int) -> bool:
        """删除餐食"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM Meal WHERE meal_id = ?", (meal_id,))
            conn.commit()
            
            return cursor.rowcount > 0
            
        except Exception as e:
            print(f"❌ 删除餐食失败: {e}")
            return False
    
    # ==================== 库存管理 ====================
    def get_inventory(self) -> List[Dict]:
        """获取库存列表"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM Ingredient 
                ORDER BY ingredient_name
            """)
            
            return [dict(row) for row in cursor.fetchall()]
            
        except Exception as e:
            print(f"❌ 获取库存列表失败: {e}")
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
        """创建新订单"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # 验证餐食ID
            meal_id = order_data.get('meal_id')
            if not meal_id:
                raise ValueError("餐食ID不能为空")
            
            # 如果餐食ID是字符串，尝试转换为整数
            if isinstance(meal_id, str):
                try:
                    meal_id = int(meal_id)
                except ValueError:
                    # 如果不是数字，尝试通过名称查找
                    cursor.execute("SELECT meal_id FROM Meal WHERE meal_name = ?", (meal_id,))
                    result = cursor.fetchone()
                    if result:
                        meal_id = result['meal_id']
                    else:
                        raise ValueError(f"未找到餐食: {meal_id}")
            
            # 验证餐食是否存在
            cursor.execute("SELECT meal_id FROM Meal WHERE meal_id = ?", (meal_id,))
            if not cursor.fetchone():
                raise ValueError(f"餐食ID {meal_id} 不存在")
            
            # 创建订单价格记录
            cursor.execute("""
                INSERT INTO Order_price (order_price)
                VALUES (?)
            """, (order_data.get('total_amount', 0),))
            
            order_price_id = cursor.lastrowid
            
            # 创建订单记录
            cursor.execute("""
                INSERT INTO "Order" (meal_id, customer_id, employee_id, order_price_id, 
                                   payment_method_id, delivery_date, order_status, order_note, meal_quantity)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                meal_id,
                order_data.get('customer_id', 1),
                order_data.get('employee_id', 1),
                order_price_id,
                order_data.get('payment_method_id', 1),
                order_data.get('delivery_date'),
                order_data.get('order_status', '已接收'),
                order_data.get('note', ''),
                order_data.get('quantity', 1)
            ))
            
            order_id = cursor.lastrowid
            
            # 扣减库存
            if not self.reduce_inventory_for_order(meal_id, order_data.get('quantity', 1)):
                # 如果库存扣减失败，回滚订单
                conn.rollback()
                raise ValueError("库存不足，无法创建订单")
            
            # 添加收入记录
            cursor.execute("""
                INSERT INTO Total_income (order_price_id, income_date, income_type, amount, description)
                VALUES (?, CURRENT_DATE, 'revenue', ?, ?)
            """, (order_price_id, order_data.get('total_amount', 0), f"订单 {order_id} 收入"))
            
            conn.commit()
            return order_id
            
        except Exception as e:
            print(f"❌ 创建订单失败: {e}")
            raise
    
    def get_orders(self, status_filter: str = None) -> List[Dict]:
        """获取订单列表"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            if status_filter:
                cursor.execute("""
                    SELECT o.*, m.meal_name, c.first_name || ' ' || c.last_name as customer_name,
                           e.employee_name, pm.method_name as payment_method
                    FROM "Order" o
                    LEFT JOIN Meal m ON o.meal_id = m.meal_id
                    LEFT JOIN Customer c ON o.customer_id = c.customer_id
                    LEFT JOIN Employee e ON o.employee_id = e.employee_id
                    LEFT JOIN Payment_method pm ON o.payment_method_id = pm.payment_method_id
                    WHERE o.order_status = ?
                    ORDER BY o.order_date DESC
                """, (status_filter,))
            else:
                cursor.execute("""
                    SELECT o.*, m.meal_name, c.first_name || ' ' || c.last_name as customer_name,
                           e.employee_name, pm.method_name as payment_method
                    FROM "Order" o
                    LEFT JOIN Meal m ON o.meal_id = m.meal_id
                    LEFT JOIN Customer c ON o.customer_id = c.customer_id
                    LEFT JOIN Employee e ON o.employee_id = e.employee_id
                    LEFT JOIN Payment_method pm ON o.payment_method_id = pm.payment_method_id
                    ORDER BY o.order_date DESC
                """)
            
            return [dict(row) for row in cursor.fetchall()]
            
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
    
    def reduce_inventory_for_order(self, meal_id: int, quantity: int) -> bool:
        """为订单扣减库存（容器+原料）"""
        try:
            import os, json
            conn = self.get_connection()
            cursor = conn.cursor()

            # 1. 扣减容器库存（原有逻辑）
            cursor.execute("""
                SELECT mc.container_id, mc.container_required_quantity
                FROM Meal_container mc
                WHERE mc.meal_id = ?
            """, (meal_id,))
            containers = cursor.fetchall()
            for container in containers:
                cursor.execute("""
                    SELECT container_current_stock 
                    FROM Container 
                    WHERE container_id = ?
                """, (container['container_id'],))
                current_stock = cursor.fetchone()['container_current_stock']
                required = container['container_required_quantity'] * quantity
                if current_stock < required:
                    return False
            for container in containers:
                required = container['container_required_quantity'] * quantity
                cursor.execute("""
                    UPDATE Container 
                    SET container_current_stock = container_current_stock - ?
                    WHERE container_id = ?
                """, (required, container['container_id']))

            # 2. 扣减原料库存（新逻辑）
            # 读取recipes.json
            recipes_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'recipes.json')
            with open(recipes_path, 'r', encoding='utf-8') as f:
                recipes = json.load(f)
            # meal_id可能是int，recipes里是str，需统一
            meal_id_str = str(meal_id)
            recipe = None
            for r in recipes:
                if str(r.get('meal_id')) == meal_id_str:
                    recipe = r
                    break
            if not recipe:
                # 没有配方，视为无需扣减原料
                return True
            # 检查所有原料库存是否充足
            insufficient = []
            for ing in recipe.get('ingredients', []):
                ing_name = ing['ingredient_name']
                qty_per = ing['quantity_per_serving']
                total_need = qty_per * quantity
                # 查找Ingredient表
                cursor.execute("""
                    SELECT ingredient_id, ingredient_current_stock FROM Ingredient WHERE ingredient_name = ?
                """, (ing_name,))
                row = cursor.fetchone()
                if not row or row['ingredient_current_stock'] < total_need:
                    insufficient.append(ing_name)
            if insufficient:
                print(f"❌ 原料库存不足: {insufficient}")
                return False
            # 扣减原料库存
            for ing in recipe.get('ingredients', []):
                ing_name = ing['ingredient_name']
                qty_per = ing['quantity_per_serving']
                total_need = qty_per * quantity
                cursor.execute("""
                    UPDATE Ingredient SET ingredient_current_stock = ingredient_current_stock - ? WHERE ingredient_name = ?
                """, (total_need, ing_name))
            return True
        except Exception as e:
            print(f"❌ 扣减库存失败: {e}")
            return False
    
    # ==================== 客户管理 ====================
    def get_customers(self) -> List[Dict]:
        """获取客户列表"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT c.*, pm.method_name as payment_method_name
                FROM Customer c
                LEFT JOIN Payment_method pm ON c.payment_method_id = pm.payment_method_id
                ORDER BY c.first_name, c.last_name
            """)
            
            return [dict(row) for row in cursor.fetchall()]
            
        except Exception as e:
            print(f"❌ 获取客户列表失败: {e}")
            return []
    
    def create_customer(self, customer_data: Dict) -> int:
        """创建新客户"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO Customer (first_name, last_name, customer_phone, customer_email, 
                                    customer_address, payment_method_id)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                customer_data.get('first_name', ''),
                customer_data.get('last_name', ''),
                customer_data.get('phone', ''),
                customer_data.get('email', ''),
                customer_data.get('address', ''),
                customer_data.get('payment_method_id')
            ))
            
            conn.commit()
            return cursor.lastrowid
            
        except Exception as e:
            print(f"❌ 创建客户失败: {e}")
            raise
    
    def update_customer(self, customer_id: int, customer_data: Dict) -> bool:
        """更新客户信息"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE Customer 
                SET first_name = ?, last_name = ?, customer_phone = ?, 
                    customer_email = ?, customer_address = ?, payment_method_id = ?
                WHERE customer_id = ?
            """, (
                customer_data.get('first_name', ''),
                customer_data.get('last_name', ''),
                customer_data.get('phone', ''),
                customer_data.get('email', ''),
                customer_data.get('address', ''),
                customer_data.get('payment_method_id'),
                customer_id
            ))
            
            conn.commit()
            return cursor.rowcount > 0
            
        except Exception as e:
            print(f"❌ 更新客户失败: {e}")
            return False
    
    def delete_customer(self, customer_id: int) -> bool:
        """删除客户"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # 检查是否有相关订单
            cursor.execute("""
                SELECT COUNT(*) as order_count
                FROM "Order"
                WHERE customer_id = ?
            """, (customer_id,))
            
            order_count = cursor.fetchone()['order_count']
            if order_count > 0:
                print(f"⚠️ 客户有 {order_count} 个相关订单，无法删除")
                return False
            
            cursor.execute("""
                DELETE FROM Customer
                WHERE customer_id = ?
            """, (customer_id,))
            
            conn.commit()
            return cursor.rowcount > 0
            
        except Exception as e:
            print(f"❌ 删除客户失败: {e}")
            return False
    
    # ==================== 财务管理 ====================
    def get_financial_records(self, record_type: str = None) -> List[Dict]:
        """获取财务记录"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            if record_type:
                cursor.execute("""
                    SELECT * FROM Total_income 
                    WHERE income_type = ?
                    ORDER BY income_date DESC
                """, (record_type,))
            else:
                cursor.execute("""
                    SELECT * FROM Total_income 
                    ORDER BY income_date DESC
                """)
            
            return [dict(row) for row in cursor.fetchall()]
            
        except Exception as e:
            print(f"❌ 获取财务记录失败: {e}")
            return []
    
    def get_dashboard_stats(self) -> Dict:
        """获取仪表盘统计数据"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # 今日销售额
            cursor.execute("""
                SELECT COALESCE(SUM(ti.amount), 0) as today_sales
                FROM Total_income ti
                WHERE ti.income_type = 'revenue' 
                AND ti.income_date = CURRENT_DATE
            """)
            today_sales = cursor.fetchone()['today_sales']
            
            # 今日订单数
            cursor.execute("""
                SELECT COUNT(*) as order_count
                FROM "Order"
                WHERE DATE(order_date) = CURRENT_DATE
            """)
            order_count = cursor.fetchone()['order_count']
            
            # 低库存项目数
            cursor.execute("""
                SELECT COUNT(*) as low_stock_count
                FROM Ingredient
                WHERE ingredient_current_stock <= ingredient_reorder_threshold
            """)
            low_stock_count = cursor.fetchone()['low_stock_count']
            
            # 客户总数
            cursor.execute("SELECT COUNT(*) as customer_count FROM Customer")
            customer_count = cursor.fetchone()['customer_count']
            
            return {
                'today_sales': today_sales,
                'order_count': order_count,
                'low_stock_count': low_stock_count,
                'customer_count': customer_count,
                'last_update': datetime.datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"❌ 获取仪表盘统计失败: {e}")
            return {
                'today_sales': 0,
                'order_count': 0,
                'low_stock_count': 0,
                'customer_count': 0,
                'last_update': datetime.datetime.now().isoformat()
            }
    
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
            
            cursor.execute("""
                SELECT e.*, es.employee_salary_amount
                FROM Employee e
                LEFT JOIN Employee_salary es ON e.employee_salary_id = es.employee_salary_id
                WHERE e.is_active = 1
                ORDER BY e.employee_name
            """)
            
            return [dict(row) for row in cursor.fetchall()]
            
        except Exception as e:
            print(f"❌ 获取员工列表失败: {e}")
            return []

# 创建全局数据库管理器实例
database_manager = DatabaseManager()
