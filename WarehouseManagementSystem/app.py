from flask import Flask, render_template, request, jsonify
from database import get_connection, prompt_database_password

from queries import (
    add_record,
    get_record,
    get_all_records,
    update_record,
    delete_record,
    get_composite_record,
    update_composite_record,
    delete_composite_record
)

app = Flask(__name__)

@app.route("/")
def home():
    return render_template(
        "index.html",
        message="Welcome to Warehouse Management System!"
    )

# --------------- PRODUCTS ---------------

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/add-product", methods=["POST"])
def add_product_route():
    data = request.json
    connection = get_connection()
    try:
        add_record(connection, "Product", {
            "P_id": data["p_id"],
            "P_name": data["p_name"],
            "P_price": data["p_price"],
            "Category": data["category"]
        })
        return jsonify({
            "success": True,
            "message": "Product added successfully!"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        })
    finally:
        connection.close()

@app.route("/get-product/<int:p_id>")
def get_product_route(p_id):
    connection = get_connection()
    product = get_record(
        connection,
        "Product",
        "P_id",
        p_id
    )
    connection.close()
    if product:
        return jsonify({
            "found": True,
            "product": product
        })
    return jsonify({
        "found": False,
        "message": "No such product exists."
    })

@app.route("/update-product", methods=["PUT"])
def update_product_route():
    data = request.json
    connection = get_connection()
    try:
        update_record(
            connection,
            "Product",
            "P_id",
            data["p_id"],
            {
                "P_name": data["p_name"],
                "P_price": data["p_price"],
                "Category": data["category"]
            }
        )
        return jsonify({
            "success": True,
            "message": "Product updated successfully!"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        })
    finally:
        connection.close()

@app.route("/delete-product/<int:p_id>", methods=["DELETE"])
def delete_product_route(p_id):
    connection = get_connection()
    try:
        product = get_record(
            connection,
            "Product",
            "P_id",
            p_id
        )
        if not product:
            return jsonify({
                "success": False,
                "message": "No such product exists."
            })
        delete_record(
            connection,
            "Product",
            "P_id",
            p_id
        )
        return jsonify({
            "success": True,
            "message": "Product deleted successfully!"
        })
    finally:
        connection.close()

@app.route("/view-products")
def view_products():
    connection = get_connection()
    products = get_all_records(connection, "Product")
    connection.close()
    return jsonify(products)

# --------------- SUPPLIER ---------------
@app.route("/add-supplier", methods=["POST"])
def add_supplier():
    data = request.json
    connection = get_connection()
    try:
        add_record(connection, "Supplier", {
            "S_id": data["s_id"],
            "S_name": data["s_name"]
        })
        return jsonify({
            "success": True,
            "message": "Supplier added successfully!"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        })
    finally:
        connection.close()

@app.route("/get-supplier/<int:s_id>")
def get_supplier(s_id):
    connection = get_connection()
    supplier = get_record(
        connection,
        "Supplier",
        "S_id",
        s_id
    )
    connection.close()
    if supplier:
        return jsonify({
            "found": True,
            "record": supplier
        })
    return jsonify({
        "found": False,
        "message": "No such supplier exists."
    })

@app.route("/update-supplier", methods=["PUT"])
def update_supplier():
    data = request.json
    connection = get_connection()
    try:
        update_record(
            connection,
            "Supplier",
            "S_id",
            data["s_id"],
            {
                "S_name": data["s_name"]
            }
        )
        return jsonify({
            "success": True,
            "message": "Supplier updated successfully!"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        })
    finally:
        connection.close()

@app.route("/delete-supplier/<int:s_id>", methods=["DELETE"])
def delete_supplier(s_id):
    connection = get_connection()
    try:
        supplier = get_record(
            connection,
            "Supplier",
            "S_id",
            s_id
        )
        if not supplier:
            return jsonify({
                "success": False,
                "message": "No such supplier exists."
            })
        delete_record(
            connection,
            "Supplier",
            "S_id",
            s_id
        )
        return jsonify({
            "success": True,
            "message": "Supplier deleted successfully!"
        })
    finally:
        connection.close()

@app.route("/view-suppliers")
def view_suppliers():
    connection = get_connection()
    records = get_all_records(
        connection,
        "Supplier"
    )
    connection.close()
    return jsonify(records)

# --------------- CUSTOMER ---------------
@app.route("/add-customer", methods=["POST"])
def add_customer():
    data = request.json
    connection = get_connection()
    try:
        add_record(connection, "Customer", {
            "C_id": data["c_id"],
            "C_name": data["c_name"],
            "C_phone": data["c_phone"]
        })
        return jsonify({
            "success": True,
            "message": "Customer added successfully!"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        })
    finally:
        connection.close()

@app.route("/get-customer/<int:c_id>")
def get_customer(c_id):
    connection = get_connection()
    customer = get_record(
        connection,
        "Customer",
        "C_id",
        c_id
    )
    connection.close()
    if customer:
        return jsonify({
            "found": True,
            "record": customer
        })
    return jsonify({
        "found": False,
        "message": "No such customer exists."
    })

@app.route("/update-customer", methods=["PUT"])
def update_customer():
    data = request.json
    connection = get_connection()
    try:
        update_record(
            connection,
            "Customer",
            "C_id",
            data["c_id"],
            {
                "C_name": data["c_name"],
                "C_phone": data["c_phone"]
            }
        )
        return jsonify({
            "success": True,
            "message": "Customer updated successfully!"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        })
    finally:
        connection.close()

@app.route("/delete-customer/<int:c_id>", methods=["DELETE"])
def delete_customer(c_id):
    connection = get_connection()
    try:
        customer = get_record(
            connection,
            "Customer",
            "C_id",
            c_id
        )
        if not customer:
            return jsonify({
                "success": False,
                "message": "No such customer exists."
            })
        delete_record(
            connection,
            "Customer",
            "C_id",
            c_id
        )
        return jsonify({
            "success": True,
            "message": "Customer deleted successfully!"
        })
    finally:
        connection.close()

@app.route("/view-customers")
def view_customers():
    connection = get_connection()
    records = get_all_records(
        connection,
        "Customer"
    )
    connection.close()
    return jsonify(records)

# --------------- EMPLOYEE ---------------
@app.route("/add-employee", methods=["POST"])
def add_employee():
    data = request.json
    connection = get_connection()
    try:
        add_record(connection, "Employee", {
            "E_id": data["e_id"],
            "E_name": data["e_name"],
            "Role": data["role"],
            "E_phone": data["e_phone"],
            "W_id": data["w_id"],
            "Supervisor_id": data["supervisor_id"]
        })
        return jsonify({
            "success": True,
            "message": "Employee added successfully!"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        })
    finally:
        connection.close()

@app.route("/get-employee/<int:e_id>")
def get_employee(e_id):
    connection = get_connection()
    employee = get_record(
        connection,
        "Employee",
        "E_id",
        e_id
    )
    connection.close()
    if employee:
        return jsonify({
            "found": True,
            "record": employee
        })
    return jsonify({
        "found": False,
        "message": "No such employee exists."
    })

@app.route("/update-employee", methods=["PUT"])
def update_employee():
    data = request.json
    connection = get_connection()
    try:
        update_record(
            connection,
            "Employee",
            "E_id",
            data["e_id"],
            {
                "E_name": data["e_name"],
                "Role": data["role"],
                "E_phone": data["e_phone"],
                "W_id": data["w_id"],
                "Supervisor_id": data["supervisor_id"]
            }
        )
        return jsonify({
            "success": True,
            "message": "Employee updated successfully!"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        })
    finally:
        connection.close()

@app.route("/delete-employee/<int:e_id>", methods=["DELETE"])
def delete_employee(e_id):
    connection = get_connection()
    try:
        employee = get_record(
            connection,
            "Employee",
            "E_id",
            e_id
        )
        if not employee:
            return jsonify({
                "success": False,
                "message": "No such employee exists."
            })
        delete_record(
            connection,
            "Employee",
            "E_id",
            e_id
        )
        return jsonify({
            "success": True,
            "message": "Employee deleted successfully!"
        })
    finally:
        connection.close()

@app.route("/view-employees")
def view_employees():
    connection = get_connection()
    records = get_all_records(
        connection,
        "Employee"
    )
    connection.close()
    return jsonify(records)

# --------------- WAREHOUSE ---------------
@app.route("/add-warehouse", methods=["POST"])
def add_warehouse():
    data = request.json
    connection = get_connection()
    try:
        add_record(connection, "Warehouse", {
            "W_id": data["w_id"],
            "W_name": data["w_name"],
            "W_Area": data["w_area"],
            "W_City": data["w_city"],
            "W_State": data["w_state"],
            "W_Pincode": data["w_pincode"],
            "Capacity": data["capacity"],
            "Manager_id": data["manager_id"]
        })
        return jsonify({
            "success": True,
            "message": "Warehouse added successfully!"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        })
    finally:
        connection.close()

@app.route("/get-warehouse/<int:w_id>")
def get_warehouse(w_id):
    connection = get_connection()
    warehouse = get_record(
        connection,
        "Warehouse",
        "W_id",
        w_id
    )
    connection.close()
    if warehouse:
        return jsonify({
            "found": True,
            "record": warehouse
        })
    return jsonify({
        "found": False,
        "message": "No such warehouse exists."
    })

@app.route("/update-warehouse", methods=["PUT"])
def update_warehouse():
    data = request.json
    connection = get_connection()
    try:
        update_record(
            connection,
            "Warehouse",
            "W_id",
            data["w_id"],
            {
                "W_name": data["w_name"],
                "W_Area": data["w_area"],
                "W_City": data["w_city"],
                "W_State": data["w_state"],
                "W_Pincode": data["w_pincode"],
                "Capacity": data["capacity"],
                "Manager_id": data["manager_id"]
            }
        )
        return jsonify({
            "success": True,
            "message": "Warehouse updated successfully!"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        })
    finally:
        connection.close()

@app.route("/delete-warehouse/<int:w_id>", methods=["DELETE"])
def delete_warehouse(w_id):
    connection = get_connection()
    try:
        warehouse = get_record(
            connection,
            "Warehouse",
            "W_id",
            w_id
        )
        if not warehouse:
            return jsonify({
                "success": False,
                "message": "No such warehouse exists."
            })
        delete_record(
            connection,
            "Warehouse",
            "W_id",
            w_id
        )
        return jsonify({
            "success": True,
            "message": "Warehouse deleted successfully!"
        })
    finally:
        connection.close()

@app.route("/view-warehouses")
def view_warehouses():
    connection = get_connection()
    records = get_all_records(
        connection,
        "Warehouse"
    )
    connection.close()
    return jsonify(records)

# --------------- ORDER ---------------

@app.route("/add-order", methods=["POST"])
def add_order():
    data = request.json
    connection = get_connection()

    try:
        add_record(connection, "Order", {
            "O_id": data["o_id"],
            "O_date": data["o_date"],
            "Payment_Type": data["payment_type"],
            "C_id": data["c_id"]
        })

        return jsonify({
            "success": True,
            "message": "Order added successfully!"
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        })

    finally:
        connection.close()


@app.route("/get-order/<int:o_id>")
def get_order(o_id):
    connection = get_connection()

    order = get_record(
        connection,
        "Order",
        "O_id",
        o_id
    )

    connection.close()

    if order:
        return jsonify({
            "found": True,
            "record": order
        })

    return jsonify({
        "found": False,
        "message": "No such order exists."
    })


@app.route("/update-order", methods=["PUT"])
def update_order():
    data = request.json
    connection = get_connection()

    try:
        update_record(
            connection,
            "Order",
            "O_id",
            data["o_id"],
            {
                "O_date": data["o_date"],
                "Payment_Type": data["payment_type"],
                "C_id": data["c_id"]
            }
        )

        return jsonify({
            "success": True,
            "message": "Order updated successfully!"
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        })

    finally:
        connection.close()


@app.route("/delete-order/<int:o_id>", methods=["DELETE"])
def delete_order(o_id):
    connection = get_connection()

    try:
        order = get_record(
            connection,
            "Order",
            "O_id",
            o_id
        )

        if not order:
            return jsonify({
                "success": False,
                "message": "No such order exists."
            })

        delete_record(
            connection,
            "Order",
            "O_id",
            o_id
        )

        return jsonify({
            "success": True,
            "message": "Order deleted successfully!"
        })

    finally:
        connection.close()


@app.route("/view-orders")
def view_orders():
    connection = get_connection()

    records = get_all_records(
        connection,
        "Order"
    )

    connection.close()

    return jsonify(records)

# --------------- INVENTORY ---------------

@app.route("/add-inventory", methods=["POST"])
def add_inventory():
    data = request.json
    connection = get_connection()

    try:
        add_record(connection, "Inventory", {
            "W_id": data["w_id"],
            "P_id": data["p_id"],
            "P_quantity": data["p_quantity"]
        })

        return jsonify({
            "success": True,
            "message": "Inventory added successfully!"
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        })

    finally:
        connection.close()


@app.route("/get-inventory/<int:w_id>/<int:p_id>")
def get_inventory(w_id, p_id):
    connection = get_connection()

    record = get_composite_record(
        connection,
        "Inventory",
        {
            "W_id": w_id,
            "P_id": p_id
        }
    )

    connection.close()

    if record:
        return jsonify({
            "found": True,
            "record": record
        })

    return jsonify({
        "found": False,
        "message": "No such inventory record exists."
    })


@app.route("/update-inventory", methods=["PUT"])
def update_inventory():
    data = request.json
    connection = get_connection()

    try:
        update_composite_record(
            connection,
            "Inventory",
            {
                "W_id": data["w_id"],
                "P_id": data["p_id"]
            },
            {
                "P_quantity": data["p_quantity"]
            }
        )

        return jsonify({
            "success": True,
            "message": "Inventory updated successfully!"
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        })

    finally:
        connection.close()


@app.route(
    "/delete-inventory/<int:w_id>/<int:p_id>",
    methods=["DELETE"]
)
def delete_inventory(w_id, p_id):
    connection = get_connection()

    try:
        record = get_composite_record(
            connection,
            "Inventory",
            {
                "W_id": w_id,
                "P_id": p_id
            }
        )

        if not record:
            return jsonify({
                "success": False,
                "message": "No such inventory record exists."
            })

        delete_composite_record(
            connection,
            "Inventory",
            {
                "W_id": w_id,
                "P_id": p_id
            }
        )

        return jsonify({
            "success": True,
            "message": "Inventory deleted successfully!"
        })

    finally:
        connection.close()


@app.route("/view-inventory")
def view_inventory():
    connection = get_connection()

    records = get_all_records(
        connection,
        "Inventory"
    )

    connection.close()

    return jsonify(records)

@app.route("/view-inventory/<int:w_id>")
def view_inventory_by_warehouse(w_id):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT *
        FROM Inventory
        WHERE W_id = %s
        """,
        (w_id,)
    )

    records = cursor.fetchall()
    cursor.close()
    connection.close()

    return jsonify(records)
# --------------- ORDER ITEM ---------------

@app.route("/add-order-item", methods=["POST"])
def add_order_item():
    data = request.json
    connection = get_connection()

    try:
        add_record(connection, "Order_Item", {
            "O_id": data["o_id"],
            "Item_no": data["item_no"],
            "I_quantity": data["i_quantity"],
            "Sell_price": data["sell_price"],
            "P_id": data["p_id"]
        })

        return jsonify({
            "success": True,
            "message": "Order item added successfully!"
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        })

    finally:
        connection.close()


@app.route("/get-order-item/<int:o_id>/<int:item_no>")
def get_order_item(o_id, item_no):
    connection = get_connection()

    record = get_composite_record(
        connection,
        "Order_Item",
        {
            "O_id": o_id,
            "Item_no": item_no
        }
    )

    connection.close()

    if record:
        return jsonify({
            "found": True,
            "record": record
        })

    return jsonify({
        "found": False,
        "message": "No such order item exists."
    })


@app.route("/update-order-item", methods=["PUT"])
def update_order_item():
    data = request.json
    connection = get_connection()

    try:
        update_composite_record(
            connection,
            "Order_Item",
            {
                "O_id": data["o_id"],
                "Item_no": data["item_no"]
            },
            {
                "I_quantity": data["i_quantity"],
                "Sell_price": data["sell_price"],
                "P_id": data["p_id"]
            }
        )

        return jsonify({
            "success": True,
            "message": "Order item updated successfully!"
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        })

    finally:
        connection.close()


@app.route(
    "/delete-order-item/<int:o_id>/<int:item_no>",
    methods=["DELETE"]
)
def delete_order_item(o_id, item_no):
    connection = get_connection()

    try:
        record = get_composite_record(
            connection,
            "Order_Item",
            {
                "O_id": o_id,
                "Item_no": item_no
            }
        )

        if not record:
            return jsonify({
                "success": False,
                "message": "No such order item exists."
            })

        delete_composite_record(
            connection,
            "Order_Item",
            {
                "O_id": o_id,
                "Item_no": item_no
            }
        )

        return jsonify({
            "success": True,
            "message": "Order item deleted successfully!"
        })

    finally:
        connection.close()


@app.route("/view-order-items")
def view_order_items():
    connection = get_connection()

    records = get_all_records(
        connection,
        "Order_Item"
    )

    connection.close()

    return jsonify(records)

@app.route("/view-order-items/<int:o_id>")
def view_order_items_by_order(o_id):
    connection = get_connection()

    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT *
        FROM Order_Item
        WHERE O_id = %s
        """,
        (o_id,)
    )

    records = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(records)

# --------------- SUPPLIER PHONE ---------------

@app.route("/add-supplier-phone", methods=["POST"])
def add_supplier_phone():
    data = request.json
    connection = get_connection()

    try:
        add_record(connection, "Supplier_Phone", {
            "S_id": data["s_id"],
            "S_phone": data["s_phone"]
        })

        return jsonify({
            "success": True,
            "message": "Supplier phone added successfully!"
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        })

    finally:
        connection.close()


@app.route("/get-supplier-phone/<int:s_id>/<s_phone>")
def get_supplier_phone(s_id, s_phone):
    connection = get_connection()

    record = get_composite_record(
        connection,
        "Supplier_Phone",
        {
            "S_id": s_id,
            "S_phone": s_phone
        }
    )

    connection.close()

    if record:
        return jsonify({
            "found": True,
            "record": record
        })

    return jsonify({
        "found": False,
        "message": "No such supplier phone exists."
    })


@app.route("/update-supplier-phone", methods=["PUT"])
def update_supplier_phone():
    data = request.json
    connection = get_connection()

    try:
        update_composite_record(
            connection,
            "Supplier_Phone",
            {
                "S_id": data["s_id"],
                "S_phone": data["old_phone"]
            },
            {
                "S_phone": data["s_phone"]
            }
        )

        return jsonify({
            "success": True,
            "message": "Supplier phone updated successfully!"
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        })

    finally:
        connection.close()


@app.route(
    "/delete-supplier-phone/<int:s_id>/<s_phone>",
    methods=["DELETE"]
)
def delete_supplier_phone(s_id, s_phone):
    connection = get_connection()

    try:
        record = get_composite_record(
            connection,
            "Supplier_Phone",
            {
                "S_id": s_id,
                "S_phone": s_phone
            }
        )

        if not record:
            return jsonify({
                "success": False,
                "message": "No such supplier phone exists."
            })

        delete_composite_record(
            connection,
            "Supplier_Phone",
            {
                "S_id": s_id,
                "S_phone": s_phone
            }
        )

        return jsonify({
            "success": True,
            "message": "Supplier phone deleted successfully!"
        })

    finally:
        connection.close()


@app.route("/view-supplier-phones")
def view_supplier_phones():
    connection = get_connection()

    records = get_all_records(
        connection,
        "Supplier_Phone"
    )

    connection.close()

    return jsonify(records)

@app.route("/view-supplier-phones/<int:s_id>")
def view_supplier_phones_by_supplier(s_id):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT *
        FROM Supplier_Phone
        WHERE S_id = %s
        """,
        (s_id,)
    )

    records = cursor.fetchall()
    cursor.close()
    connection.close()

    return jsonify(records)
# --------------- SUPPLIER ADDRESS ---------------

@app.route("/add-supplier-address", methods=["POST"])
def add_supplier_address():
    data = request.json
    connection = get_connection()

    try:
        add_record(connection, "Supplier_Address", {
            "S_id": data["s_id"],
            "Addr_no": data["addr_no"],
            "S_Area": data["s_area"],
            "S_City": data["s_city"],
            "S_State": data["s_state"],
            "S_Pincode": data["s_pincode"]
        })

        return jsonify({
            "success": True,
            "message": "Supplier address added successfully!"
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        })

    finally:
        connection.close()


@app.route("/get-supplier-address/<int:s_id>/<int:addr_no>")
def get_supplier_address(s_id, addr_no):
    connection = get_connection()

    record = get_composite_record(
        connection,
        "Supplier_Address",
        {
            "S_id": s_id,
            "Addr_no": addr_no
        }
    )

    connection.close()

    if record:
        return jsonify({
            "found": True,
            "record": record
        })

    return jsonify({
        "found": False,
        "message": "No such supplier address exists."
    })


@app.route("/update-supplier-address", methods=["PUT"])
def update_supplier_address():
    data = request.json
    connection = get_connection()

    try:
        update_composite_record(
            connection,
            "Supplier_Address",
            {
                "S_id": data["s_id"],
                "Addr_no": data["addr_no"]
            },
            {
                "S_Area": data["s_area"],
                "S_City": data["s_city"],
                "S_State": data["s_state"],
                "S_Pincode": data["s_pincode"]
            }
        )

        return jsonify({
            "success": True,
            "message": "Supplier address updated successfully!"
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        })

    finally:
        connection.close()


@app.route(
    "/delete-supplier-address/<int:s_id>/<int:addr_no>",
    methods=["DELETE"]
)
def delete_supplier_address(s_id, addr_no):
    connection = get_connection()

    try:
        record = get_composite_record(
            connection,
            "Supplier_Address",
            {
                "S_id": s_id,
                "Addr_no": addr_no
            }
        )

        if not record:
            return jsonify({
                "success": False,
                "message": "No such supplier address exists."
            })

        delete_composite_record(
            connection,
            "Supplier_Address",
            {
                "S_id": s_id,
                "Addr_no": addr_no
            }
        )

        return jsonify({
            "success": True,
            "message": "Supplier address deleted successfully!"
        })

    finally:
        connection.close()


@app.route("/view-supplier-addresses")
def view_supplier_addresses():
    connection = get_connection()

    records = get_all_records(
        connection,
        "Supplier_Address"
    )

    connection.close()

    return jsonify(records)

@app.route("/view-supplier-addresses/<int:s_id>")
def view_supplier_addresses_by_supplier(s_id):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT *
        FROM Supplier_Address
        WHERE S_id = %s
        """,
        (s_id,)
    )

    records = cursor.fetchall()
    cursor.close()
    connection.close()

    return jsonify(records)

# --------------- SUPPLIES ---------------

@app.route("/add-supplies", methods=["POST"])
def add_supplies():
    data = request.json
    connection = get_connection()

    try:
        add_record(connection, "Supplies", {
            "S_id": data["s_id"],
            "P_id": data["p_id"]
        })

        return jsonify({
            "success": True,
            "message": "Supply record added successfully!"
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        })

    finally:
        connection.close()


@app.route("/get-supplies/<int:s_id>/<int:p_id>")
def get_supplies(s_id, p_id):
    connection = get_connection()

    record = get_composite_record(
        connection,
        "Supplies",
        {
            "S_id": s_id,
            "P_id": p_id
        }
    )

    connection.close()

    if record:
        return jsonify({
            "found": True,
            "record": record
        })

    return jsonify({
        "found": False,
        "message": "No such supply record exists."
    })


@app.route("/update-supplies", methods=["PUT"])
def update_supplies():
    data = request.json
    connection = get_connection()
    try:
        update_composite_record(
            connection, "Supplies",
            {"S_id": data["old_s_id"], "P_id": data["old_p_id"]},
            {"S_id": data["s_id"], "P_id": data["p_id"]}
        )
        return jsonify(success=True, message="Supply record updated successfully!")
    except Exception as e:
        return jsonify(success=False, message=str(e))
    finally:
        connection.close()


@app.route("/delete-supplies/<int:s_id>/<int:p_id>", methods=["DELETE"])
def delete_supplies(s_id, p_id):
    connection = get_connection()

    try:
        record = get_composite_record(
            connection,
            "Supplies",
            {
                "S_id": s_id,
                "P_id": p_id
            }
        )

        if not record:
            return jsonify({
                "success": False,
                "message": "No such supply record exists."
            })

        delete_composite_record(
            connection,
            "Supplies",
            {
                "S_id": s_id,
                "P_id": p_id
            }
        )

        return jsonify({
            "success": True,
            "message": "Supply record deleted successfully!"
        })

    finally:
        connection.close()


@app.route("/view-supplies")
def view_supplies():
    connection = get_connection()

    records = get_all_records(
        connection,
        "Supplies"
    )

    connection.close()

    return jsonify(records)

@app.route("/view-supplies-product/<int:p_id>")
def view_supplies_by_product(p_id):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT *
        FROM Supplies
        WHERE P_id = %s
        """,
        (p_id,)
    )

    records = cursor.fetchall()
    cursor.close()
    connection.close()

    return jsonify(records)

if __name__ == "__main__":
    prompt_database_password()
    # Check credentials before starting the server.
    connection = get_connection()
    connection.close()
    # The reloader starts a second process, which would prompt again.
    app.run(debug=True, use_reloader=False)
