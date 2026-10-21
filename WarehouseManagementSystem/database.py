from getpass import getpass

import mysql.connector


_db_password = None


def prompt_database_password():
    """Read the password once without displaying or saving it to a file."""
    global _db_password
    _db_password = getpass("MySQL password for root: ")


def get_connection():
    if _db_password is None:
        raise RuntimeError("Start the application with python app.py to enter the MySQL password.")
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password=_db_password,
        database="WarehouseDB"
    )
