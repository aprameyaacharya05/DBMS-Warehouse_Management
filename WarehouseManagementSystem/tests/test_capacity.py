import sqlite3
import unittest

from queries import add_record, update_composite_record, update_record


class Cursor:
    """Run the data checks against SQLite; MySQL row locks are not simulated."""
    def __init__(self, db):
        self.cursor = db.cursor()

    def execute(self, sql, values=()):
        self.cursor.execute(sql.replace('%s', '?').replace(' FOR UPDATE', ''), values)

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

    def commit(self):
        self.db.commit()

    def rollback(self):
        self.db.rollback()


class CapacityTests(unittest.TestCase):
    def setUp(self):
        self.c = Connection()
        self.c.db.executescript('''
            CREATE TABLE Warehouse (W_id INTEGER PRIMARY KEY, Capacity INTEGER);
            CREATE TABLE Inventory (W_id INTEGER, P_id INTEGER, P_quantity INTEGER,
                                    PRIMARY KEY (W_id, P_id));
            INSERT INTO Warehouse VALUES (1,100), (2,200), (3,NULL);
            INSERT INTO Inventory VALUES (1,201,60), (1,202,30), (2,201,150);
        ''')

    def tearDown(self):
        self.c.db.close()

    def stock(self):
        return self.c.db.execute('SELECT SUM(P_quantity) FROM Inventory WHERE W_id=1').fetchone()[0]

    def add(self, quantity, warehouse=1, product=203):
        add_record(self.c, 'Inventory', {'W_id':warehouse, 'P_id':product, 'P_quantity':quantity})

    def update(self, quantity, product=201):
        update_composite_record(self.c, 'Inventory', {'W_id':1, 'P_id':product}, {'P_quantity':quantity})

    def test_add_at_capacity_and_overflow(self):
        self.add('10')
        self.assertEqual(self.stock(), 100)
        with self.assertRaisesRegex(ValueError, 'capacity exceeded'):
            self.add(1, product=204)
        self.assertEqual(self.stock(), 100)

    def test_replacement_quantity_and_decrease(self):
        self.update(70)
        self.assertEqual(self.stock(), 100)
        with self.assertRaises(ValueError):
            self.update(71)
        self.assertEqual(self.stock(), 100)
        self.update(0)
        self.assertEqual(self.stock(), 30)

    def test_capacity_cannot_be_lower_than_stock(self):
        with self.assertRaises(ValueError):
            update_record(self.c, 'Warehouse', 'W_id', 1, {'Capacity':89})
        self.assertEqual(self.c.db.execute('SELECT Capacity FROM Warehouse WHERE W_id=1').fetchone()[0], 100)
        update_record(self.c, 'Warehouse', 'W_id', 1, {'Capacity':90})

    def test_missing_warehouse_item_and_capacity(self):
        for warehouse in (999, 3):
            with self.assertRaises(ValueError):
                self.add(1, warehouse=warehouse)
        with self.assertRaisesRegex(ValueError, 'No matching inventory'):
            self.update(1, product=999)
        self.assertEqual(self.stock(), 90)

    def test_duplicate_failure_rolls_back_and_connection_remains_usable(self):
        with self.assertRaises(sqlite3.IntegrityError):
            self.add(1, product=201)
        self.assertEqual(self.stock(), 90)
        self.add(5)
        self.assertEqual(self.stock(), 95)


if __name__ == '__main__':
    unittest.main()
