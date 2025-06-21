-- 数据库初始数据插入脚本
-- 为工厂后台综合管理系统添加示例数据

-- 插入支付方式
INSERT INTO Payment_method (method_name) VALUES 
('现金'),
('信用卡'),
('支付宝'),
('微信支付'),
('银行转账');

-- 插入客户数据
INSERT INTO Customer (first_name, last_name, customer_phone, customer_email, customer_address, payment_method_id, password_hash) VALUES 
('张', '三', '13800138001', 'zhangsan@email.com', '北京市朝阳区建国门外大街1号', 1, 'hashed_password_123'),
('李', '四', '13800138002', 'lisi@email.com', '上海市浦东新区世纪大道100号', 2, 'hashed_password_456'),
('王', '五', '13800138003', 'wangwu@email.com', '广州市天河区珠江新城花城大道85号', 3, 'hashed_password_789'),
('赵', '六', '13800138004', 'zhaoliu@email.com', '深圳市南山区深圳湾科技生态园10栋A座', 4, 'hashed_password_101'),
('管理员', '', '13800138000', 'admin@company.com', '公司地址', 1, 'admin_password_hash');

-- 插入员工薪资
INSERT INTO Employee_salary (employee_salary_amount, pay_day) VALUES 
(5000.00, 15),
(6000.00, 15),
(8000.00, 15),
(10000.00, 15);

-- 插入员工数据
INSERT INTO Employee (employee_name, employee_address, employee_salary_id, employee_phone, employee_email) VALUES 
('陈经理', '北京市海淀区中关村大街27号', 4, '13900139001', 'chenmanager@company.com'),
('刘厨师', '北京市东城区王府井大街138号', 3, '13900139002', 'liuchef@company.com'),
('周助理', '北京市西城区金融街35号', 2, '13900139003', 'zhouassistant@company.com'),
('吴配送员', '北京市丰台区南四环西路128号', 1, '13900139004', 'wudelivery@company.com');

-- 插入容器供应商
INSERT INTO Container_supplier (container_supplier_name, container_supplier_contact_email, container_supplier_phone, container_supplier_address) VALUES 
('北京包装材料有限公司', 'info@bjpackaging.com', '010-12345678', '北京市大兴区经济开发区工业园'),
('上海容器制造厂', 'sales@shcontainer.com', '021-87654321', '上海市松江区工业区松江路100号'),
('广东塑料制品公司', 'contact@gdplastic.com', '020-11111111', '广东省东莞市厚街镇工业区');

-- 插入容器类型
INSERT INTO Container (container_type, container_unit_cost, container_current_stock, container_reorder_threshold) VALUES 
('小号餐盒', 2.50, 500, 50),
('中号餐盒', 3.00, 300, 40),
('大号餐盒', 3.50, 200, 30),
('汤盒', 2.00, 400, 50),
('饮料杯', 1.50, 600, 80);

-- 插入容器批次价格
INSERT INTO Container_batch_price (container_batch_price) VALUES 
(250.00),
(300.00),
(350.00),
(200.00),
(150.00);

-- 插入容器批次
INSERT INTO Container_batch (container_id, container_supplier_id, container_batch_price_id, container_batch_purchase_date, batch_quantity) VALUES 
(1, 1, 1, '2025-06-01', 100),
(2, 1, 2, '2025-06-01', 100),
(3, 2, 3, '2025-06-05', 100),
(4, 2, 4, '2025-06-05', 100),
(5, 3, 5, '2025-06-10', 100);

-- 插入原料供应商
INSERT INTO Ingredient_supplier (ingredient_supplier_name, ingredient_supplier_email, ingredient_supplier_phone, ingredient_supplier_address) VALUES 
('新鲜农场有限公司', 'fresh@farm.com', '010-22222222', '北京市房山区农业示范园'),
('海鲜批发市场', 'seafood@market.com', '021-33333333', '上海市浦东新区海鲜批发市场'),
('优质肉类供应商', 'meat@supplier.com', '020-44444444', '广州市白云区肉类批发市场'),
('调料香料公司', 'spice@company.com', '0755-55555555', '深圳市宝安区调料市场');

-- 插入原料
INSERT INTO Ingredient (ingredient_name, ingredient_current_stock, unit_measure, ingredient_reorder_threshold, ingredient_unit_cost) VALUES 
('大米', 100.00, 'kg', 20.00, 5.50),
('鸡胸肉', 50.00, 'kg', 10.00, 18.00),
('牛肉', 30.00, 'kg', 8.00, 35.00),
('三文鱼', 15.00, 'kg', 5.00, 45.00),
('西兰花', 25.00, 'kg', 5.00, 8.00),
('胡萝卜', 20.00, 'kg', 5.00, 4.00),
('洋葱', 30.00, 'kg', 8.00, 3.50),
('大蒜', 10.00, 'kg', 2.00, 12.00),
('生抽', 20.00, '瓶', 5.00, 8.50),
('香油', 15.00, '瓶', 3.00, 15.00);

-- 插入原料批次价格
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
(225.00);

-- 插入原料批次
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
(10, 10, 4, '2026-06-01', '2025-06-01', 15.00);

-- 插入餐食
INSERT INTO Meal (meal_name, meal_details, meal_price, isActive) VALUES 
('经典牛肉饭', '香嫩牛肉配米饭，搭配时令蔬菜，营养均衡', 28.00, 1),
('三文鱼套餐', '新鲜三文鱼刺身配特制酱汁，附赠蔬菜沙拉', 45.00, 1),
('家常鸡肉饭', '嫩滑鸡胸肉配香米，健康低脂选择', 22.00, 1),
('蔬菜素食套餐', '时令蔬菜搭配，健康素食主义者首选', 18.00, 1),
('海鲜炒饭', '新鲜海鲜配炒米饭，口感丰富', 32.00, 1);

-- 插入餐食-容器关联（每个餐食需要的容器）
INSERT INTO Meal_container (meal_id, container_id, container_required_quantity) VALUES 
(1, 2, 1), -- 经典牛肉饭 - 中号餐盒
(1, 4, 1), -- 经典牛肉饭 - 汤盒
(2, 3, 1), -- 三文鱼套餐 - 大号餐盒
(2, 1, 1), -- 三文鱼套餐 - 小号餐盒（沙拉）
(3, 2, 1), -- 家常鸡肉饭 - 中号餐盒
(4, 2, 1), -- 蔬菜素食套餐 - 中号餐盒
(5, 3, 1); -- 海鲜炒饭 - 大号餐盒

-- 插入订单价格
INSERT INTO Order_price (order_price) VALUES 
(28.00),
(45.00),
(22.00),
(18.00),
(32.00),
(56.00),
(90.00);

-- 插入订单数据
INSERT INTO "Order" (meal_id, customer_id, employee_id, order_price_id, payment_method_id, order_date, delivery_date, order_status, order_note, meal_quantity) VALUES 
(1, 1, 1, 1, 1, '2025-06-20 12:00:00', '2025-06-20', '已完成', '不要辣', 1),
(2, 2, 1, 2, 2, '2025-06-20 13:30:00', '2025-06-20', '已完成', '要酱汁', 1),
(3, 3, 2, 3, 3, '2025-06-21 11:45:00', '2025-06-21', '进行中', '', 1),
(4, 4, 2, 4, 4, '2025-06-21 12:15:00', '2025-06-21', '已接收', '素食要求', 1),
(1, 1, 1, 6, 1, '2025-06-21 14:00:00', '2025-06-21', '已接收', '双份', 2),
(2, 2, 1, 7, 2, '2025-06-21 15:00:00', '2025-06-22', '已接收', '明天送达', 2);

-- 插入固定成本
INSERT INTO Fixed_cost (cost_type, effective_date, cost_amount) VALUES 
('人力成本', '2025-06-01', 10000.00),
('租金', '2025-06-01', 3500.00),
('水电费', '2025-06-01', 2000.00),
('杂费', '2025-06-01', 1000.00);

-- 插入总收入记录（示例）
INSERT INTO Total_income (order_price_id, income_date, income_type, amount, description) VALUES 
(1, '2025-06-20', 'revenue', 28.00, '经典牛肉饭订单收入'),
(2, '2025-06-20', 'revenue', 45.00, '三文鱼套餐订单收入'),
(3, '2025-06-21', 'revenue', 22.00, '家常鸡肉饭订单收入');

INSERT INTO Total_income (fixed_cost_id, income_date, income_type, amount, description) VALUES 
(1, '2025-06-01', 'cost', 10000.00, '6月人力成本'),
(2, '2025-06-01', 'cost', 3500.00, '6月租金'),
(3, '2025-06-01', 'cost', 2000.00, '6月水电费'),
(4, '2025-06-01', 'cost', 1000.00, '6月杂费');
