-- Complete current schema for a NEW database. Run this before data.sql.
-- Includes unique warehouse managers and required relationship references.
-- CREATE TABLE IF NOT EXISTS does not upgrade existing tables.
-- The existing project database has already received these constraint updates.
-- Cur_stock and Total_amt are calculated by SELECT queries, not stored columns.
CREATE DATABASE IF NOT EXISTS WarehouseDB;

USE WarehouseDB;

CREATE TABLE IF NOT EXISTS Warehouse (
    W_id INT PRIMARY KEY,
    W_name VARCHAR(100),
    W_Area VARCHAR(100),
    W_City VARCHAR(50),
    W_State VARCHAR(50),
    W_Pincode VARCHAR(10),
    Capacity INT,
    Manager_id INT,
    CONSTRAINT uq_warehouse_manager UNIQUE (Manager_id)
);

CREATE TABLE IF NOT EXISTS Product (
    P_id INT PRIMARY KEY,
    P_name VARCHAR(100),
    P_price DECIMAL(10, 2),
    Category VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS Supplier (
    S_id INT PRIMARY KEY,
    S_name VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS Customer (
    C_id INT PRIMARY KEY,
    C_name VARCHAR(100),
    C_phone VARCHAR(15)
);

CREATE TABLE IF NOT EXISTS Employee (
    E_id INT PRIMARY KEY,
    E_name VARCHAR(100),
    Role VARCHAR(50),
    E_phone VARCHAR(15),
    W_id INT NOT NULL,
    Supervisor_id INT,
    FOREIGN KEY (W_id) REFERENCES Warehouse(W_id),
    FOREIGN KEY (Supervisor_id) REFERENCES Employee(E_id)
);

CREATE TABLE IF NOT EXISTS Supplier_Phone (
    S_id INT,
    S_phone VARCHAR(15),
    PRIMARY KEY (S_id, S_phone),
    FOREIGN KEY (S_id) REFERENCES Supplier(S_id)
);

CREATE TABLE IF NOT EXISTS Supplier_Address (
    S_id INT,
    Addr_no INT,
    S_Area VARCHAR(100),
    S_City VARCHAR(50),
    S_State VARCHAR(50),
    S_Pincode VARCHAR(10),
    PRIMARY KEY (S_id, Addr_no),
    FOREIGN KEY (S_id) REFERENCES Supplier(S_id)
);

CREATE TABLE IF NOT EXISTS `Order` (
    O_id INT PRIMARY KEY,
    O_date DATE,
    Payment_Type VARCHAR(30),
    C_id INT NOT NULL,
    FOREIGN KEY (C_id) REFERENCES Customer(C_id)
);

CREATE TABLE IF NOT EXISTS Order_Item (
    O_id INT,
    Item_no INT,
    I_quantity INT,
    Sell_price DECIMAL(10,2),
    P_id INT NOT NULL,
    PRIMARY KEY (O_id, Item_no),
    FOREIGN KEY (O_id) REFERENCES `Order`(O_id),
    FOREIGN KEY (P_id) REFERENCES Product(P_id)
);

CREATE TABLE IF NOT EXISTS Inventory (
    W_id INT,
    P_id INT,
    P_quantity INT,
    PRIMARY KEY (W_id, P_id),
    FOREIGN KEY (W_id) REFERENCES Warehouse(W_id),
    FOREIGN KEY (P_id) REFERENCES Product(P_id)
);

CREATE TABLE IF NOT EXISTS Supplies (
    S_id INT,
    P_id INT,
    PRIMARY KEY (S_id, P_id),
    FOREIGN KEY (S_id) REFERENCES Supplier(S_id),
    FOREIGN KEY (P_id) REFERENCES Product(P_id)
);

SET @fk_exists = (
    SELECT COUNT(*)
    FROM information_schema.TABLE_CONSTRAINTS
    WHERE CONSTRAINT_SCHEMA = 'WarehouseDB'
      AND TABLE_NAME = 'Warehouse'
      AND CONSTRAINT_NAME = 'fk_wh_mgr'
      AND CONSTRAINT_TYPE = 'FOREIGN KEY'
);

SET @sql = IF(
    @fk_exists = 0,
    'ALTER TABLE Warehouse ADD CONSTRAINT fk_wh_mgr FOREIGN KEY (Manager_id) REFERENCES Employee(E_id)',
    'SET @dummy = 1'
);

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;
