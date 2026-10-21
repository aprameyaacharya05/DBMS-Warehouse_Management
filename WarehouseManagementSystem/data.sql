-- Sample data for the current schema.sql. Run once after creating the tables.
-- Do not rerun on a populated database: the sample primary keys already exist.
-- Warehouses are created first with no manager, then employees are inserted,
-- then distinct managers are assigned to resolve the circular foreign keys.
USE WarehouseDB;


-- =====================================================
-- 1. WAREHOUSES
-- =====================================================

INSERT INTO Warehouse
(W_id, W_name, W_Area, W_City, W_State, W_Pincode, Capacity, Manager_id)
VALUES
(1, 'Central Warehouse', 'Peenya Industrial Area', 'Bengaluru', 'Karnataka', '560058', 5000, NULL),
(2, 'East Warehouse', 'Whitefield', 'Bengaluru', 'Karnataka', '560066', 3500, NULL);


-- =====================================================
-- 2. EMPLOYEES
-- =====================================================

INSERT INTO Employee
(E_id, E_name, Role, E_phone, W_id, Supervisor_id)
VALUES
(101, 'Rahul Sharma', 'Manager', '9876543210', 1, NULL),
(102, 'Priya Nair', 'Inventory Staff', '9876543211', 1, 101),
(103, 'Arjun Rao', 'Warehouse Staff', '9876543212', 1, 101),
(104, 'Meera Iyer', 'Manager', '9876543213', 2, NULL),
(105, 'Kiran Kumar', 'Inventory Staff', '9876543214', 2, 104);


-- =====================================================
-- 3. ASSIGN WAREHOUSE MANAGERS
-- =====================================================

UPDATE Warehouse
SET Manager_id = 101
WHERE W_id = 1;

UPDATE Warehouse
SET Manager_id = 104
WHERE W_id = 2;


-- =====================================================
-- 4. PRODUCTS
-- =====================================================

INSERT INTO Product
(P_id, P_name, P_price, Category)
VALUES
(201, 'Laptop', 55000.00, 'Electronics'),
(202, 'Wireless Mouse', 800.00, 'Electronics'),
(203, 'Keyboard', 1500.00, 'Electronics'),
(204, 'Office Chair', 7500.00, 'Furniture'),
(205, 'Notebook', 120.00, 'Stationery'),
(206, 'Water Bottle', 500.00, 'Accessories');


-- =====================================================
-- 5. SUPPLIERS
-- =====================================================

INSERT INTO Supplier
(S_id, S_name)
VALUES
(301, 'TechWorld Suppliers'),
(302, 'OfficeMart Distributors'),
(303, 'HomeStore Supplies');


-- =====================================================
-- 6. SUPPLIER PHONES
-- =====================================================

INSERT INTO Supplier_Phone
(S_id, S_phone)
VALUES
(301, '9988776655'),
(301, '9988776656'),
(302, '9977554433'),
(303, '9966443322');


-- =====================================================
-- 7. SUPPLIER ADDRESSES
-- =====================================================

INSERT INTO Supplier_Address
(S_id, Addr_no, S_Area, S_City, S_State, S_Pincode)
VALUES
(301, 1, 'Electronic City', 'Bengaluru', 'Karnataka', '560100'),
(302, 1, 'Rajajinagar', 'Bengaluru', 'Karnataka', '560010'),
(303, 1, 'Indiranagar', 'Bengaluru', 'Karnataka', '560038');


-- =====================================================
-- 8. CUSTOMERS
-- =====================================================

INSERT INTO Customer
(C_id, C_name, C_phone)
VALUES
(401, 'Ananya Menon', '9876500001'),
(402, 'Rohan Gupta', '9876500002'),
(403, 'Sneha Thomas', '9876500003'),
(404, 'Vikram Singh', '9876500004');


-- =====================================================
-- 9. INVENTORY
-- =====================================================

INSERT INTO Inventory
(W_id, P_id, P_quantity)
VALUES
(1, 201, 25),
(1, 202, 120),
(1, 203, 80),
(1, 204, 15),
(2, 205, 200),
(2, 206, 60),
(2, 202, 50);


-- =====================================================
-- 10. SUPPLIES
-- =====================================================

INSERT INTO Supplies
(S_id, P_id)
VALUES
(301, 201),
(301, 202),
(301, 203),
(302, 205),
(302, 206),
(303, 204);


-- =====================================================
-- 11. ORDERS
-- =====================================================

INSERT INTO `Order`
(O_id, O_date, Payment_Type, C_id)
VALUES
(501, '2026-09-20', 'UPI', 401),
(502, '2026-09-21', 'Card', 402),
(503, '2026-09-22', 'Cash', 403);


-- =====================================================
-- 12. ORDER ITEMS
-- =====================================================

INSERT INTO Order_Item
(O_id, Item_no, I_quantity, Sell_price, P_id)
VALUES
(501, 1, 1, 55000.00, 201),
(501, 2, 2, 800.00, 202),
(502, 1, 1, 7500.00, 204),
(502, 2, 3, 120.00, 205),
(503, 1, 2, 1500.00, 203),
(503, 2, 1, 500.00, 206);


-- =====================================================
-- 13. VERIFY DERIVED VALUES (not stored as extra columns)
-- =====================================================

-- Current stock is the total number of units in each warehouse.
SELECT W.W_id, W.W_name,
       COALESCE(SUM(I.P_quantity), 0) AS Cur_stock
FROM Warehouse AS W
LEFT JOIN Inventory AS I ON I.W_id = W.W_id
GROUP BY W.W_id, W.W_name;

-- Order total uses the item's selling price, not the current product price.
SELECT O.O_id,
       COALESCE(SUM(I.I_quantity * I.Sell_price), 0) AS Total_amt
FROM `Order` AS O
LEFT JOIN Order_Item AS I ON I.O_id = O.O_id
GROUP BY O.O_id;
