import re
import unittest
from unittest.mock import patch
from flask import jsonify
from app import app
from auth import ACCOUNTS, PERMISSIONS, route_permission


class LoginTests(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def token(self):
        with self.client.session_transaction() as session:
            return session['csrf_token']

    def login(self, name, password):
        self.client.get('/')
        return self.client.post('/', data={
            'username': name, 'password': password, 'csrf_token': self.token()})

    def test_public_index_and_login_form(self):
        self.assertEqual(self.client.get('/').status_code, 200)
        response = self.client.get('/')
        self.assertIn(b'class="home-login"', response.data)
        self.assertIn(b'class="features-section"', response.data)
        self.assertNotIn(b'Show Dashboard', response.data)
        self.assertEqual(self.client.get('/dashboard').location, '/')
        self.assertNotIn(b'class="table-menu"', response.data)
        self.assertEqual(response.headers['Cache-Control'], 'no-store')

    def test_invalid_credentials_and_token(self):
        self.assertIn(b'Incorrect username or password', self.login('admin','wrong').data)
        with self.client.session_transaction() as session:
            self.assertNotIn('username',session)
        response=self.client.post('/',data={'username':'admin','password':'ad123'})
        self.assertIn(b'login form has expired',response.data)

    def test_role_menus_and_logout(self):
        for name,password,expected in [
            ('admin','ad123',['product','supplier','customer','employee','warehouse','order']),
            ('inventory','in123',['product','supplier','warehouse']),
            ('staff','st123',['product','customer','warehouse','order'])
        ]:
            self.client=app.test_client()
            self.assertEqual(self.login(name,password).status_code,302)
            page=self.client.get('/dashboard').get_data(as_text=True)
            menu=page.split('<div class="table-menu">')[1].split('</div>')[0]
            for table in ['product','supplier','customer','employee','warehouse','order']:
                self.assertEqual("showTable('"+table+"')" in menu,table in expected,(name,table))
            self.assertNotIn(password,page)
            self.assertEqual(self.client.post('/logout').status_code,403)
            self.assertEqual(self.client.post('/logout',data={'csrf_token':self.token()}).status_code,302)
            self.assertEqual(self.client.get('/view-products').status_code,401)

    def routes(self):
        for rule in app.url_map.iter_rules():
            if rule.endpoint not in ('home','dashboard','static','logout'):
                path=re.sub(r'<[^>]+>','1',rule.rule)
                method=next(m for m in ('GET','POST','PUT','DELETE') if m in rule.methods)
                yield path,method

    def test_every_data_route_requires_login(self):
        with patch('app.get_connection') as connection:
            for path,method in self.routes():
                self.assertEqual(self.client.open(path,method=method,json={}).status_code,401,path)
            connection.assert_not_called()

    def test_every_role_and_route_permission(self):
        # Runs after the auth guard, so accepted requests need no real database.
        def probe():
            return jsonify(probe_reached=True)
        app.before_request_funcs[None].append(probe)
        try:
            for name,account in ACCOUNTS.items():
                with self.client.session_transaction() as session:
                    session['username']=name
                    session['csrf_token']='test-token'
                for path,method in self.routes():
                    resource,action=route_permission(path)
                    self.assertIsNotNone(resource,path)
                    expected=200 if action in PERMISSIONS[account['role']].get(resource,[]) else 403
                    result=self.client.open(path,method=method,json={},headers={'X-CSRF-Token':'test-token'})
                    self.assertEqual(result.status_code,expected,(name,path))
            self.assertEqual(self.client.post('/add-order',json={}).status_code,403)
        finally:
            app.before_request_funcs[None].remove(probe)


if __name__ == '__main__':
    unittest.main()
