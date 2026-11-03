import unittest
from unittest.mock import Mock, patch
from mysql.connector.errors import IntegrityError
from app import app
from queries import delete_record, delete_composite_record, DeletionError


class DeletionTests(unittest.TestCase):
    def test_referenced_record_rolls_back_and_closes_cursor(self):
        connection = Mock()
        cursor = connection.cursor.return_value
        cursor.execute.side_effect = IntegrityError('raw database details', errno=1451)
        with self.assertRaisesRegex(DeletionError, 'existing orders'):
            delete_record(connection, 'Customer', 'C_id', 401)
        connection.rollback.assert_called_once()
        connection.commit.assert_not_called()
        cursor.close.assert_called_once()

    def test_successful_composite_delete_keeps_both_keys(self):
        connection = Mock()
        delete_composite_record(connection, 'Inventory', {'W_id':1, 'P_id':201})
        sql, values = connection.cursor.return_value.execute.call_args.args
        self.assertIn('W_id = %s AND P_id = %s', sql)
        self.assertEqual(values, (1,201))
        connection.commit.assert_called_once()
        connection.rollback.assert_not_called()

    def test_other_errors_are_not_misreported_as_foreign_key_errors(self):
        connection = Mock()
        connection.cursor.return_value.execute.side_effect = RuntimeError('private detail')
        with self.assertRaises(DeletionError) as caught:
            delete_record(connection, 'Product', 'P_id', 201)
        self.assertEqual(caught.exception.status_code, 500)
        self.assertNotIn('private detail', str(caught.exception))

    def test_route_returns_json_and_closes_connection(self):
        client = app.test_client()
        with client.session_transaction() as session:
            session['username'] = 'admin'
            session['csrf_token'] = 'test-token'
        connection = Mock()
        connection.cursor.return_value.execute.side_effect = IntegrityError('raw details', errno=1451)
        with patch('app.get_connection', return_value=connection), patch('app.get_record', return_value={'C_id':401}):
            response = client.delete('/delete-customer/401', headers={'X-CSRF-Token':'test-token'})
        self.assertEqual(response.status_code, 409)
        self.assertFalse(response.json['success'])
        self.assertIn('existing orders', response.json['message'])
        self.assertNotIn('raw details', response.json['message'])
        connection.close.assert_called_once()


if __name__ == '__main__':
    unittest.main()
