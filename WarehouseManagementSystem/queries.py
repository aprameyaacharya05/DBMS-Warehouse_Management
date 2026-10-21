from validation import validate_values


def capacity_checked_write(connection, warehouse_id, query, values,
                           product_id=None, quantity=None, capacity=None,
                           updating_inventory=False):
    """Check stock and write in one transaction; serialize edits per warehouse."""
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT Capacity FROM Warehouse WHERE W_id = %s FOR UPDATE",
                       (warehouse_id,))
        warehouse = cursor.fetchone()
        if warehouse is None:
            raise ValueError("No such warehouse exists.")

        # Locking reads see the latest committed stock, even after another read.
        cursor.execute("SELECT P_id, P_quantity FROM Inventory WHERE W_id = %s FOR UPDATE",
                       (warehouse_id,))
        inventory = cursor.fetchall()
        stock = sum(row['P_quantity'] or 0 for row in inventory)
        limit = warehouse['Capacity'] if capacity is None else capacity
        if limit is None:
            raise ValueError("Set this warehouse's capacity before changing its inventory.")
        limit = int(limit)
        projected_stock = stock
        if quantity is not None:
            old_quantity = 0
            if updating_inventory:
                record = next((row for row in inventory
                               if row['P_id'] == int(product_id)), None)
                if record is None:
                    raise ValueError("No matching inventory record exists.")
                old_quantity = record['P_quantity'] or 0
            projected_stock = stock - old_quantity + int(quantity)
        if projected_stock > limit:
            raise ValueError(
                f"Warehouse capacity exceeded: this operation would leave "
                f"{projected_stock} units, but capacity is {limit}. "
                f"Current stock is {stock} units."
            )
        cursor.execute(query, values)
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        cursor.close()


def get_table_name(table):
    if table == "Order":
        return "`Order`"
    return table


def select_records_sql(table):
    # Derived attributes are calculated from the current rows, never stored.
    if table == "Warehouse":
        return """SELECT Warehouse.*,
            (SELECT COALESCE(SUM(P_quantity), 0) FROM Inventory
             WHERE Inventory.W_id = Warehouse.W_id) AS Cur_stock
            FROM Warehouse"""
    if table == "Order":
        return """SELECT `Order`.*,
            (SELECT COALESCE(SUM(I_quantity * Sell_price), 0) FROM Order_Item
             WHERE Order_Item.O_id = `Order`.O_id) AS Total_amt
            FROM `Order`"""
    return f"SELECT * FROM {get_table_name(table)}"

def add_record(connection, table, data):
    validate_values(data)
    columns = ", ".join(data.keys())
    placeholders = ", ".join(["%s"] * len(data))
    query = f"""
        INSERT INTO {get_table_name(table)} ({columns})
        VALUES ({placeholders})
    """
    if table == "Inventory":
        if data.get('P_quantity') is None:
            raise ValueError("Inventory Quantity is required.")
        return capacity_checked_write(
            connection, data['W_id'], query, tuple(data.values()),
            product_id=data['P_id'], quantity=data['P_quantity'])
    cursor = connection.cursor()
    cursor.execute(query, tuple(data.values()))
    connection.commit()
    cursor.close()

def get_record(connection, table, pk_column, pk_value):
    cursor = connection.cursor(dictionary=True)
    query = f"""
        {select_records_sql(table)}
        WHERE {pk_column} = %s
    """
    cursor.execute(query, (pk_value,))
    record = cursor.fetchone()
    cursor.close()
    return record

def get_all_records(connection, table):
    cursor = connection.cursor(dictionary=True)
    cursor.execute(select_records_sql(table))
    records = cursor.fetchall()
    cursor.close()
    return records

def update_record(connection, table, pk_column, pk_value, data):
    validate_values({pk_column: pk_value, **data})
    set_clause = ", ".join(
        f"{column} = %s" for column in data.keys()
    )
    query = f"""
        UPDATE {get_table_name(table)}
        SET {set_clause}
        WHERE {pk_column} = %s
    """
    if table == "Warehouse" and 'Capacity' in data:
        if data['Capacity'] is None:
            raise ValueError("Warehouse Capacity is required.")
        return capacity_checked_write(
            connection, pk_value, query, tuple(data.values()) + (pk_value,),
            capacity=data['Capacity'])
    cursor = connection.cursor()
    cursor.execute(
        query,
        tuple(data.values()) + (pk_value,)
    )
    connection.commit()
    cursor.close()

def delete_record(connection, table, pk_column, pk_value):
    cursor = connection.cursor()
    query = f"""
        DELETE FROM {get_table_name(table)}
        WHERE {pk_column} = %s
    """
    cursor.execute(query, (pk_value,))
    connection.commit()
    cursor.close()

def get_composite_record(connection, table, conditions):
    cursor = connection.cursor(dictionary=True)

    where_clause = " AND ".join(
        f"{column} = %s" for column in conditions.keys()
    )

    query = f"""
        SELECT * FROM {get_table_name(table)}
        WHERE {where_clause}
    """

    cursor.execute(
        query,
        tuple(conditions.values())
    )

    record = cursor.fetchone()

    cursor.close()

    return record


def update_composite_record(
    connection,
    table,
    conditions,
    data
):
    validate_values(conditions)
    validate_values(data)
    if not conditions or any(value is None or str(value).strip() == "" for value in conditions.values()):
        raise ValueError("Both key values are required.")
    if table == "Inventory":
        if set(conditions) != {'W_id', 'P_id'} or set(data) != {'P_quantity'}:
            raise ValueError("Inventory updates require both IDs and a replacement quantity.")
        if data['P_quantity'] is None:
            raise ValueError("Inventory Quantity is required.")
        return capacity_checked_write(
            connection, conditions['W_id'],
            "UPDATE Inventory SET P_quantity = %s WHERE W_id = %s AND P_id = %s",
            (data['P_quantity'], conditions['W_id'], conditions['P_id']),
            product_id=conditions['P_id'], quantity=data['P_quantity'],
            updating_inventory=True)
    if not get_composite_record(connection, table, conditions):
        raise ValueError("No matching record exists for these key values.")
    cursor = connection.cursor()

    set_clause = ", ".join(
        f"{column} = %s" for column in data.keys()
    )

    where_clause = " AND ".join(
        f"{column} = %s"
        for column in conditions.keys()
    )

    query = f"""
        UPDATE {get_table_name(table)}
        SET {set_clause}
        WHERE {where_clause}
    """

    cursor.execute(
        query,
        tuple(data.values()) +
        tuple(conditions.values())
    )

    connection.commit()

    cursor.close()


def delete_composite_record(
    connection,
    table,
    conditions
):
    cursor = connection.cursor()

    where_clause = " AND ".join(
        f"{column} = %s"
        for column in conditions.keys()
    )

    query = f"""
        DELETE FROM {get_table_name(table)}
        WHERE {where_clause}
    """

    cursor.execute(
        query,
        tuple(conditions.values())
    )

    connection.commit()

    cursor.close()
