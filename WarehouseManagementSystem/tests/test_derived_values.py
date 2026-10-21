import sqlite3
import unittest

from queries import get_all_records, get_record


class Cursor:
    def __init__(self, connection):
        self.cursor = connection.cursor()

    def execute(self, sql, values=()):
        self.cursor.execute(sql.replace('%s', '?'), values)

    def fetchone(self):
        row = self.cursor.fetchone()
        return dict(row) if row else None

    def fetchall(self):
        return [dict(row) for row in self.cursor.fetchall()]

    def close(self):
        self.cursor.close()


class Connection:
    def __init__(self):
        self.db = sqlite3.connect(':memory:')
        self.db.row_factory = sqlite3.Row

    def cursor(self, **kwargs):
        return Cursor(self.db)


class DerivedValuesTests(unittest.TestCase):
    def setUp(self):
        self.connection = Connection()
        self.connection.db.executescript('''
            CREATE TABLE Warehouse (W_id INTEGER PRIMARY KEY);
            CREATE TABLE Inventory (W_id INTEGER, P_id INTEGER, P_quantity INTEGER);
            CREATE TABLE `Order` (O_id INTEGER PRIMARY KEY);
            CREATE TABLE Order_Item (O_id INTEGER, Item_no INTEGER,
                I_quantity INTEGER, Sell_price DECIMAL);
            INSERT INTO Warehouse VALUES (1), (2), (3);
            INSERT INTO Inventory VALUES (1,201,5), (1,202,8), (2,201,10);
            INSERT INTO `Order` VALUES (501), (502), (503);
            INSERT INTO Order_Item VALUES (501,1,2,12.50), (501,2,3,4), (502,1,1,7);
        ''')

    def tearDown(self):
        self.connection.db.close()

    def test_stock_is_separate_per_warehouse_and_empty_is_zero(self):
        rows = get_all_records(self.connection, 'Warehouse')
        self.assertEqual({r['W_id']: r['Cur_stock'] for r in rows}, {1:13, 2:10, 3:0})

    def test_totals_are_separate_per_order_and_empty_is_zero(self):
        rows = get_all_records(self.connection, 'Order')
        self.assertEqual({r['O_id']: r['Total_amt'] for r in rows}, {501:37, 502:7, 503:0})

    def test_totals_recalculate_after_edit_and_delete(self):
        db = self.connection.db
        db.execute('UPDATE Order_Item SET I_quantity=4 WHERE O_id=501 AND Item_no=1')
        self.assertEqual(get_record(self.connection, 'Order', 'O_id', 501)['Total_amt'], 62)
        db.execute('DELETE FROM Order_Item WHERE O_id=501')
        self.assertEqual(get_record(self.connection, 'Order', 'O_id', 501)['Total_amt'], 0)
        db.execute('UPDATE Inventory SET P_quantity=0 WHERE W_id=1')
        self.assertEqual(get_record(self.connection, 'Warehouse', 'W_id', 1)['Cur_stock'], 0)


if __name__ == '__main__':
    unittest.main()
