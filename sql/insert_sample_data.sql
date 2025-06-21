-- Database initial data insertion script
-- Add sample data for the comprehensive factory management system

-- Insert payment methods
INSERT INTO Payment_method (method_name) VALUES 
('Cash'),
('Credit Card'),
('Alipay'),
('WeChat Pay'),
('Bank Transfer');

-- Insert customer data
INSERT INTO Customer (first_name, last_name, customer_phone, customer_email, customer_address, payment_method_id, password_hash) VALUES 
('San', 'Zhang', '13800138001', 'zhangsan@email.com', '1 Jianguomenwai Avenue, Chaoyang District, Beijing', 1, 'hashed_password_123'),
('Si', 'Li', '13800138002', 'lisi@email.com', '100 Century Avenue, Pudong New Area, Shanghai', 2, 'hashed_password_456'),
('Wu', 'Wang', '13800138003', 'wangwu@email.com', '85 Huacheng Avenue, Zhujiang New Town, Tianhe District, Guangzhou', 3, 'hashed_password_789'),
('Liu', 'Zhao', '13800138004', 'zhaoliu@email.com', 'Block A, 10th Building, Shenzhen Bay Science and Technology Ecological Park, Nanshan District, Shenzhen', 4, 'hashed_password_101'),
('Meimei', 'Han', '13800138005', 'hanmeimei@email.com', 'No. 58, Nanshan Road, Hangzhou', 5, 'hashed_password_111'),
('Wei', 'Chen', '13800138006', 'chenwei@email.com', 'No. 123, Zhongshan Road, Nanjing', 1, 'hashed_password_222'),
('Admin', '', '13800138000', 'admin@company.com', 'Company Address', 1, 'admin_password_hash');

-- Insert employee salaries
INSERT INTO Employee_salary (employee_salary_amount, pay_day) VALUES 
(5000.00, 15),
(6000.00, 15),
(8000.00, 15),
(10000.00, 15),
(7500.00, 15);

-- Insert employee data
INSERT INTO Employee (employee_name, employee_address, employee_salary_id, employee_phone, employee_email) VALUES 
('Manager Chen', '27 Zhongguancun Street, Haidian District, Beijing', 4, '13900139001', 'chenmanager@company.com'),
('Chef Liu', '138 Wangfujing Street, Dongcheng District, Beijing', 3, '13900139002', 'liuchef@company.com'),
('Assistant Zhou', '35 Financial Street, Xicheng District, Beijing', 2, '13900139003', 'zhouassistant@company.com'),
('Deliveryman Wu', '128 West 4th Ring South Road, Fengtai District, Beijing', 1, '13900139004', 'wudelivery@company.com'),
('Accountant Sun', '99 Finance Street, Chaoyang District, Beijing', 5, '13900139005', 'sunaccountant@company.com');

-- Insert container suppliers
INSERT INTO Container_supplier (container_supplier_name, container_supplier_contact_email, container_supplier_phone, container_supplier_address) VALUES 
('Beijing Packaging Materials Co., Ltd.', 'info@bjpackaging.com', '010-12345678', 'Industrial Park, Daxing District Economic Development Zone, Beijing'),
('Shanghai Container Manufacturing Factory', 'sales@shcontainer.com', '021-87654321', '100 Songjiang Road, Songjiang Industrial Zone, Shanghai'),
('Guangdong Plastic Products Company', 'contact@gdplastic.com', '020-11111111', 'Industrial Zone, Houjie Town, Dongguan City, Guangdong Province');

-- Insert container types
INSERT INTO Container (container_type, container_unit_cost, container_current_stock, container_reorder_threshold) VALUES 
('Small Meal Box', 2.50, 500, 50),
('Medium Meal Box', 3.00, 300, 40),
('Large Meal Box', 3.50, 200, 30),
('Soup Box', 2.00, 400, 50),
('Beverage Cup', 1.50, 600, 80);

-- Insert container batch prices
INSERT INTO Container_batch_price (container_batch_price) VALUES 
(250.00),
(300.00),
(350.00),
(200.00),
(150.00);

-- Insert container batches
INSERT INTO Container_batch (container_id, container_supplier_id, container_batch_price_id, container_batch_purchase_date, batch_quantity) VALUES 
(1, 1, 1, '2025-06-01', 100),
(2, 1, 2, '2025-06-01', 100),
(3, 2, 3, '2025-06-05', 100),
(4, 2, 4, '2025-06-05', 100),
(5, 3, 5, '2025-06-10', 100);

-- Insert ingredient suppliers
INSERT INTO Ingredient_supplier (ingredient_supplier_name, ingredient_supplier_email, ingredient_supplier_phone, ingredient_supplier_address) VALUES 
('Fresh Farm Co., Ltd.', 'fresh@farm.com', '010-22222222', 'Agricultural Demonstration Park, Fangshan District, Beijing'),
('Seafood Wholesale Market', 'seafood@market.com', '021-33333333', 'Seafood Wholesale Market, Pudong New Area, Shanghai'),
('Quality Meat Supplier', 'meat@supplier.com', '020-44444444', 'Meat Wholesale Market, Baiyun District, Guangzhou'),
('Spice & Condiment Company', 'spice@company.com', '0755-55555555', 'Condiment Market, Baoan District, Shenzhen');

-- Insert ingredients
INSERT INTO Ingredient (ingredient_name, ingredient_current_stock, unit_measure, ingredient_reorder_threshold, ingredient_unit_cost) VALUES 
('Rice', 100.00, 'kg', 20.00, 5.50),
('Chicken Breast', 50.00, 'kg', 10.00, 18.00),
('Beef', 30.00, 'kg', 8.00, 35.00),
('Salmon', 15.00, 'kg', 5.00, 45.00),
('Broccoli', 25.00, 'kg', 5.00, 8.00),
('Carrot', 20.00, 'kg', 5.00, 4.00),
('Onion', 30.00, 'kg', 8.00, 3.50),
('Garlic', 10.00, 'kg', 2.00, 12.00),
('Soy Sauce', 20.00, 'bottle', 5.00, 8.50),
('Sesame Oil', 15.00, 'bottle', 3.00, 15.00),
('Tofu', 40.00, 'kg', 10.00, 6.00),
('Shrimp', 20.00, 'kg', 5.00, 55.00),
('Chili', 10.00, 'kg', 2.00, 25.00),
('Egg', 200.00, 'pcs', 50.00, 1.20);

-- Insert ingredient batch prices
INSERT INTO Ingredient_batch_price (ingredient_batch_price) VALUES 
(550.00),
(900.00),
(1050.00),
(675.00),
(200.00),
(120.00),
(105.00),
(240.00),
(170.00),
(225.00),
(1100.00),
(250.00),
(240.00);

-- Insert ingredient batches
INSERT INTO Ingredient_batch (ingredient_id, ingredient_batch_price_id, ingredient_supplier_id, expiration_date, ingredient_purchase_date, batch_quantity) VALUES 
(1, 1, 1, '2025-12-31', '2025-06-01', 100.00),
(2, 2, 3, '2025-06-30', '2025-06-01', 50.00),
(3, 3, 3, '2025-06-25', '2025-06-01', 30.00),
(4, 4, 2, '2025-06-23', '2025-06-01', 15.00),
(5, 5, 1, '2025-06-28', '2025-06-01', 25.00),
(6, 6, 1, '2025-07-15', '2025-06-01', 30.00),
(7, 7, 1, '2025-07-20', '2025-06-01', 30.00),
(8, 8, 4, '2025-12-31', '2025-06-01', 20.00),
(9, 9, 4, '2026-06-01', '2025-06-01', 20.00),
(10, 10, 4, '2026-06-01', '2025-06-01', 15.00),
(11, 11, 1, '2025-07-10', '2025-06-15', 40.00),
(12, 12, 2, '2025-06-25', '2025-06-15', 20.00),
(13, 13, 4, '2025-08-01', '2025-06-15', 10.00),
(14, 14, 1, '2025-07-05', '2025-06-15', 200.00);

-- Insert meals
INSERT INTO Meal (meal_name, meal_details, meal_price, isActive) VALUES 
('Classic Beef Rice', 'Tender beef with rice and seasonal vegetables, a balanced meal.', 28.00, 1),
('Salmon Set', 'Fresh salmon sashimi with special sauce, served with a vegetable salad.', 45.00, 1),
('Homestyle Chicken Rice', 'Tender chicken breast with fragrant rice, a healthy low-fat choice.', 22.00, 1),
('Vegetarian Set', 'A mix of seasonal vegetables, the top choice for vegetarians.', 18.00, 1),
('Seafood Fried Rice', 'Fresh seafood with fried rice, rich in flavor.', 32.00, 1),
('Spicy Tofu Rice', 'Classic Sichuan Mapo Tofu, spicy and savory, served with rice.', 16.00, 1),
('Shrimp and Egg Rice', 'Stir-fried shrimp with fluffy eggs, a delicious and nutritious meal.', 25.00, 1);

-- Insert meal-container associations (containers required for each meal)
INSERT INTO Meal_container (meal_id, container_id, container_required_quantity) VALUES 
(1, 2, 1), -- Classic Beef Rice - Medium Meal Box
(1, 4, 1), -- Classic Beef Rice - Soup Box
(2, 3, 1), -- Salmon Set - Large Meal Box
(2, 1, 1), -- Salmon Set - Small Meal Box (for salad)
(3, 2, 1), -- Homestyle Chicken Rice - Medium Meal Box
(4, 2, 1), -- Vegetarian Set - Medium Meal Box
(5, 3, 1), -- Seafood Fried Rice - Large Meal Box
(6, 2, 1), -- Spicy Tofu Rice - Medium Meal Box
(7, 2, 1); -- Shrimp and Egg Rice - Medium Meal Box

-- Insert order prices
INSERT INTO Order_price (order_price) VALUES 
(28.00),
(45.00),
(22.00),
(18.00),
(32.00),
(56.00),
(90.00),
(16.00),
(25.00);

-- Insert order data
INSERT INTO "Order" (meal_id, customer_id, employee_id, order_price_id, payment_method_id, order_date, delivery_date, order_status, order_note, meal_quantity) VALUES 
(1, 1, 1, 1, 1, '2025-06-20 12:00:00', '2025-06-20', 'Completed', 'Not spicy', 1),
(2, 2, 1, 2, 2, '2025-06-20 13:30:00', '2025-06-20', 'Completed', 'Extra sauce', 1),
(3, 3, 2, 3, 3, '2025-06-21 11:45:00', '2025-06-21', 'In Progress', '', 1),
(4, 4, 2, 4, 4, '2025-06-21 12:15:00', '2025-06-21', 'Received', 'Vegetarian request', 1),
(1, 1, 1, 6, 1, '2025-06-21 14:00:00', '2025-06-21', 'Received', 'Double portion', 2),
(2, 2, 1, 7, 2, '2025-06-21 15:00:00', '2025-06-22', 'Received', 'Deliver tomorrow', 2),
(6, 5, 3, 8, 5, '2025-06-22 10:00:00', '2025-06-22', 'In Progress', 'More spicy', 1),
(7, 6, 4, 9, 1, '2025-06-22 11:00:00', '2025-06-22', 'Received', '', 1);

-- Insert fixed costs
INSERT INTO Fixed_cost (cost_type, effective_date, cost_amount) VALUES 
('Labor Cost', '2025-06-01', 10000.00),
('Rent', '2025-06-01', 3500.00),
('Utilities', '2025-06-01', 2000.00),
('Miscellaneous Fees', '2025-06-01', 1000.00);

-- Insert total income records (example)
INSERT INTO Total_income (order_price_id, income_date, income_type, amount, description) VALUES 
(1, '2025-06-20', 'revenue', 28.00, 'Revenue from Classic Beef Rice order'),
(2, '2025-06-20', 'revenue', 45.00, 'Revenue from Salmon Set order'),
(3, '2025-06-21', 'revenue', 22.00, 'Revenue from Homestyle Chicken Rice order'),
(6, '2025-06-21', 'revenue', 56.00, 'Revenue from Classic Beef Rice order (double)'),
(7, '2025-06-21', 'revenue', 90.00, 'Revenue from Salmon Set order (double)'),
(8, '2025-06-22', 'revenue', 16.00, 'Revenue from Spicy Tofu Rice order'),
(9, '2025-06-22', 'revenue', 25.00, 'Revenue from Shrimp and Egg Rice order');

INSERT INTO Total_income (fixed_cost_id, income_date, income_type, amount, description) VALUES 
(1, '2025-06-01', 'cost', 10000.00, 'June Labor Cost'),
(2, '2025-06-01', 'cost', 3500.00, 'June Rent'),
(3, '2025-06-01', 'cost', 2000.00, 'June Utilities'),
(4, '2025-06-01', 'cost', 1000.00, 'June Miscellaneous Fees');
