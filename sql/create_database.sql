-- 工厂后台综合管理系统数据库
-- SQLite数据库初始化脚本
-- 创建日期: 2025-06-21

-- 删除已存在的表（如果存在）
DROP TABLE IF EXISTS Total_income;
DROP TABLE IF EXISTS Fixed_cost;
DROP TABLE IF EXISTS Order_price;
DROP TABLE IF EXISTS "Order";
DROP TABLE IF EXISTS Employee_salary;
DROP TABLE IF EXISTS Employee;
DROP TABLE IF EXISTS Ingredient_batch_price;
DROP TABLE IF EXISTS Ingredient_supplier;
DROP TABLE IF EXISTS Ingredient_batch;
DROP TABLE IF EXISTS Ingredient;
DROP TABLE IF EXISTS Container_batch_price;
DROP TABLE IF EXISTS Container_supplier;
DROP TABLE IF EXISTS Container_batch;
DROP TABLE IF EXISTS Meal_container;
DROP TABLE IF EXISTS Container;
DROP TABLE IF EXISTS Meal;
DROP TABLE IF EXISTS Payment_method;
DROP TABLE IF EXISTS Customer;

-- 1. 支付方式表
CREATE TABLE Payment_method (
    payment_method_id INTEGER PRIMARY KEY AUTOINCREMENT,
    method_name TEXT NOT NULL UNIQUE
);

-- 2. 客户表
CREATE TABLE Customer (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    customer_phone TEXT,
    customer_email TEXT UNIQUE,
    customer_address TEXT,
    payment_method_id INTEGER,
    password_hash TEXT, -- 用于登录验证
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (payment_method_id) REFERENCES Payment_method(payment_method_id)
);

-- 3. 餐食表
CREATE TABLE Meal (
    meal_id INTEGER PRIMARY KEY AUTOINCREMENT,
    meal_name TEXT NOT NULL UNIQUE,
    meal_details TEXT,
    meal_price DECIMAL(10,2) NOT NULL,
    isActive BOOLEAN DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 4. 容器表
CREATE TABLE Container (
    container_id INTEGER PRIMARY KEY AUTOINCREMENT,
    container_type TEXT NOT NULL,
    container_unit_cost DECIMAL(10,2) NOT NULL,
    container_current_stock INTEGER DEFAULT 0,
    container_reorder_threshold INTEGER DEFAULT 10,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 5. 餐食-容器关联表（多对多关系）
CREATE TABLE Meal_container (
    meal_id INTEGER,
    container_id INTEGER,
    container_required_quantity INTEGER NOT NULL DEFAULT 1,
    PRIMARY KEY (meal_id, container_id),
    FOREIGN KEY (meal_id) REFERENCES Meal(meal_id) ON DELETE CASCADE,
    FOREIGN KEY (container_id) REFERENCES Container(container_id) ON DELETE CASCADE
);

-- 6. 容器供应商表
CREATE TABLE Container_supplier (
    container_supplier_id INTEGER PRIMARY KEY AUTOINCREMENT,
    container_supplier_name TEXT NOT NULL,
    container_supplier_contact_email TEXT,
    container_supplier_phone TEXT,
    container_supplier_address TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 7. 容器批次价格表
CREATE TABLE Container_batch_price (
    container_batch_price_id INTEGER PRIMARY KEY AUTOINCREMENT,
    container_batch_price DECIMAL(10,2) NOT NULL
);

-- 8. 容器批次表
CREATE TABLE Container_batch (
    container_batch_id INTEGER PRIMARY KEY AUTOINCREMENT,
    container_id INTEGER NOT NULL,
    container_supplier_id INTEGER NOT NULL,
    container_batch_price_id INTEGER NOT NULL,
    container_batch_purchase_date DATE NOT NULL,
    batch_quantity INTEGER NOT NULL DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (container_id) REFERENCES Container(container_id),
    FOREIGN KEY (container_supplier_id) REFERENCES Container_supplier(container_supplier_id),
    FOREIGN KEY (container_batch_price_id) REFERENCES Container_batch_price(container_batch_price_id)
);

-- 9. 原料表
CREATE TABLE Ingredient (
    ingredient_id INTEGER PRIMARY KEY AUTOINCREMENT,
    ingredient_name TEXT NOT NULL UNIQUE,
    ingredient_current_stock DECIMAL(10,2) DEFAULT 0,
    unit_measure TEXT NOT NULL, -- 如：kg, 升, 个
    ingredient_reorder_threshold DECIMAL(10,2) DEFAULT 10,
    ingredient_unit_cost DECIMAL(10,2) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 10. 原料供应商表
CREATE TABLE Ingredient_supplier (
    ingredient_supplier_id INTEGER PRIMARY KEY AUTOINCREMENT,
    ingredient_supplier_name TEXT NOT NULL,
    ingredient_supplier_email TEXT,
    ingredient_supplier_phone TEXT,
    ingredient_supplier_address TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 11. 原料批次价格表
CREATE TABLE Ingredient_batch_price (
    ingredient_batch_price_id INTEGER PRIMARY KEY AUTOINCREMENT,
    ingredient_batch_price DECIMAL(10,2) NOT NULL
);

-- 12. 原料批次表
CREATE TABLE Ingredient_batch (
    ingredient_batch_id INTEGER PRIMARY KEY AUTOINCREMENT,
    ingredient_id INTEGER NOT NULL,
    ingredient_batch_price_id INTEGER NOT NULL,
    ingredient_supplier_id INTEGER NOT NULL,
    expiration_date DATE,
    ingredient_purchase_date DATE NOT NULL,
    batch_quantity DECIMAL(10,2) NOT NULL DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ingredient_id) REFERENCES Ingredient(ingredient_id),
    FOREIGN KEY (ingredient_batch_price_id) REFERENCES Ingredient_batch_price(ingredient_batch_price_id),
    FOREIGN KEY (ingredient_supplier_id) REFERENCES Ingredient_supplier(ingredient_supplier_id)
);

-- 13. 员工薪资表
CREATE TABLE Employee_salary (
    employee_salary_id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_salary_amount DECIMAL(10,2) NOT NULL,
    pay_day INTEGER NOT NULL DEFAULT 1, -- 每月的发薪日
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 14. 员工表
CREATE TABLE Employee (
    employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_name TEXT NOT NULL,
    employee_address TEXT,
    employee_salary_id INTEGER,
    employee_phone TEXT,
    employee_email TEXT,
    hire_date DATE DEFAULT CURRENT_DATE,
    is_active BOOLEAN DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (employee_salary_id) REFERENCES Employee_salary(employee_salary_id)
);

-- 15. 订单价格表
CREATE TABLE Order_price (
    order_price_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_price DECIMAL(10,2) NOT NULL
);

-- 16. 订单表
CREATE TABLE "Order" (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    meal_id INTEGER NOT NULL,
    customer_id INTEGER NOT NULL,
    employee_id INTEGER,
    order_price_id INTEGER NOT NULL,
    payment_method_id INTEGER,
    order_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    delivery_date DATE,
    order_status TEXT DEFAULT '已接收' CHECK (order_status IN ('已接收', '进行中', '已完成')),
    order_note TEXT,
    meal_quantity INTEGER NOT NULL DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (meal_id) REFERENCES Meal(meal_id),
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id),
    FOREIGN KEY (employee_id) REFERENCES Employee(employee_id),
    FOREIGN KEY (order_price_id) REFERENCES Order_price(order_price_id),
    FOREIGN KEY (payment_method_id) REFERENCES Payment_method(payment_method_id)
);

-- 17. 固定成本表
CREATE TABLE Fixed_cost (
    fixed_cost_id INTEGER PRIMARY KEY AUTOINCREMENT,
    cost_type TEXT NOT NULL, -- 人力、租金、水电、杂费
    effective_date DATE NOT NULL,
    cost_amount DECIMAL(10,2) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 18. 总收入表
CREATE TABLE Total_income (
    total_income_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_price_id INTEGER,
    employee_salary_id INTEGER,
    container_batch_price_id INTEGER,
    ingredient_batch_price_id INTEGER,
    fixed_cost_id INTEGER,
    income_date DATE DEFAULT CURRENT_DATE,
    income_type TEXT NOT NULL, -- 'revenue', 'cost'
    amount DECIMAL(10,2) NOT NULL,
    description TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_price_id) REFERENCES Order_price(order_price_id),
    FOREIGN KEY (employee_salary_id) REFERENCES Employee_salary(employee_salary_id),
    FOREIGN KEY (container_batch_price_id) REFERENCES Container_batch_price(container_batch_price_id),
    FOREIGN KEY (ingredient_batch_price_id) REFERENCES Ingredient_batch_price(ingredient_batch_price_id),
    FOREIGN KEY (fixed_cost_id) REFERENCES Fixed_cost(fixed_cost_id)
);

-- 创建索引以提高查询性能
CREATE INDEX idx_customer_email ON Customer(customer_email);
CREATE INDEX idx_order_customer ON "Order"(customer_id);
CREATE INDEX idx_order_date ON "Order"(order_date);
CREATE INDEX idx_order_status ON "Order"(order_status);
CREATE INDEX idx_ingredient_stock ON Ingredient(ingredient_current_stock);
CREATE INDEX idx_container_stock ON Container(container_current_stock);
CREATE INDEX idx_ingredient_batch_expiration ON Ingredient_batch(expiration_date);
