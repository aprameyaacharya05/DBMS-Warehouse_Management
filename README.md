# Warehouse Management System

A web-based Warehouse Management System developed as a DBMS mini-project using Python, Flask, and MySQL.

## Features
- Product and inventory management
- Supplier and customer management
- Employee and order management
- CRUD operations
- Database integration and data validation

## Tech Stack
- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python, Flask
- **Database:** MySQL

## About
This project demonstrates the practical application of relational database concepts through a warehouse management system.


## Fixed demo logins

Sign in using the login block on the home page; successful login opens the dashboard. These are demonstration credentials, not private accounts.

| Username | Password | Role |
|---|---|---|
| admin | ad123 | Administrator: all operations |
| inventory | in123 | Manage inventory; view products, warehouses and supplier details |
| staff | st123 | Manage customers, orders and items; view products and stock |

Accounts and password hashes are defined in `WarehouseManagementSystem/auth.py`.
There is no user table, registration page, or password-change page. Permissions
are enforced in Flask as well as in dashboard controls. Logout clears the session;
restarting the server also requires users to sign in again.

The MySQL password entered when running `python app.py` is separate from these
website logins. No database schema change is required for login.
