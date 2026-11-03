"""Fixed demo accounts and role permissions. No account table is required."""
from datetime import timedelta
import secrets

from flask import jsonify, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash

ACCOUNTS = {'admin': {'password_hash': 'scrypt:32768:8:1$A5u8aYQaI9rvfspy$1ba3de456362415916097c8a5e685134492b3b9a1929a98e6ebc35bf358e3228670c2e18fa7875a3f9cbb660ea140d1c1c34c366da907342e00c2ae4f822dc41', 'role': 'admin'}, 'inventory': {'password_hash': 'scrypt:32768:8:1$tYD9EvId2sHhOuPV$2d3ecfc234487492120d54f47d0c370c86ad95a378bbd9bf9ff2b71a9a3afbd35adc42836cc95bab112379cabc4a46f786c419d699017a123261d8ca329f015a', 'role': 'inventory'}, 'staff': {'password_hash': 'scrypt:32768:8:1$IwdD5fT0rv4lSOkW$7c0c1149db23cd4f476e011f6e0d92a636c29c93364d77b0c3b5c61023b4bd7b77c806fd1f4ab477b494c8f555eed01d97151dfb854f2440c3e080c3029f5afe', 'role': 'staff'}}
ROLE_NAMES = {'admin': 'Administrator', 'inventory': 'Inventory', 'staff': 'Order Staff'}
ALL_ACTIONS = ['view', 'add', 'update', 'delete']
RESOURCES = ['product', 'supplier', 'customer', 'employee', 'warehouse', 'order',
             'inventory', 'order-item', 'supplier-phone', 'supplier-address', 'supplies']
PERMISSIONS = {
    'admin': {name: ALL_ACTIONS for name in RESOURCES},
    'inventory': {
        'product': ['view'], 'warehouse': ['view'], 'inventory': ALL_ACTIONS,
        'supplier': ['view'], 'supplier-phone': ['view'],
        'supplier-address': ['view'], 'supplies': ['view']
    },
    'staff': {
        'product': ['view'], 'warehouse': ['view'], 'inventory': ['view'],
        'customer': ALL_ACTIONS, 'order': ALL_ACTIONS, 'order-item': ALL_ACTIONS
    }
}
# The list routes use plural names; the other routes use singular names.
RESOURCE_ALIASES = {
    'products': 'product', 'suppliers': 'supplier', 'customers': 'customer',
    'employees': 'employee', 'warehouses': 'warehouse', 'orders': 'order',
    'order-items': 'order-item', 'supplier-phones': 'supplier-phone',
    'supplier-addresses': 'supplier-address', 'supplies-product': 'supplies'
}


def current_account():
    return ACCOUNTS.get(session.get('username'))


def csrf_token():
    if 'csrf_token' not in session:
        session['csrf_token'] = secrets.token_hex(32)
    return session['csrf_token']


def valid_csrf():
    supplied = request.headers.get('X-CSRF-Token') or request.form.get('csrf_token', '')
    expected = session.get('csrf_token', '')
    return bool(expected and supplied and secrets.compare_digest(expected, supplied))


def route_permission(path):
    route = path.strip('/').split('/')[0]
    action, separator, resource = route.partition('-')
    if not separator or action not in ('get', 'view', 'add', 'update', 'delete'):
        return None, None
    return RESOURCE_ALIASES.get(resource, resource), 'view' if action == 'get' else action


def home_page():
    error = None
    if request.method == 'POST':
        if not valid_csrf():
            error = 'This login form has expired. Please try again.'
        else:
            username = request.form.get('username', '').strip()
            account = ACCOUNTS.get(username)
            # Use a real hash even for an unknown username.
            password_hash = (account or ACCOUNTS['admin'])['password_hash']
            valid_password = check_password_hash(password_hash, request.form.get('password', ''))
            if account and valid_password:
                session.clear()
                session['username'] = username
                session.permanent = True
                return redirect(url_for('dashboard'))
            error = 'Incorrect username or password.'
    account = current_account()
    role = account['role'] if account else None
    return render_template('index.html', username=session.get('username') if account else None,
                           role_name=ROLE_NAMES.get(role), permissions=PERMISSIONS.get(role, {}),
                           csrf_token=csrf_token(), login_error=error)


def dashboard_page():
    account = current_account()
    if account is None:
        return redirect(url_for('home'))
    role = account['role']
    return render_template('dashboard.html', username=session['username'],
                           role_name=ROLE_NAMES[role], permissions=PERMISSIONS[role],
                           csrf_token=csrf_token())


def initialize_auth(app):
    # A fresh key on startup logs everyone out after a server restart.
    app.secret_key = secrets.token_hex(32)
    app.config.update(SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE='Lax',
                      PERMANENT_SESSION_LIFETIME=timedelta(hours=8))

    @app.before_request
    def protect_operations():
        if request.endpoint in ('home', 'dashboard', 'static', 'logout') or request.endpoint is None:
            return None
        account = current_account()
        if account is None:
            return jsonify(success=False, message='Please sign in to the dashboard.'), 401
        resource, action = route_permission(request.path)
        if action not in PERMISSIONS[account['role']].get(resource, []):
            return jsonify(success=False, message='Your role does not have permission for this operation.'), 403
        if request.method in ('POST', 'PUT', 'DELETE', 'PATCH') and not valid_csrf():
            return jsonify(success=False, message='Your session has changed. Refresh the dashboard and try again.'), 403

    @app.after_request
    def prevent_cached_dashboard(response):
        if request.endpoint != 'static':
            response.headers['Cache-Control'] = 'no-store'
        return response

    @app.route('/logout', methods=['POST'])
    def logout():
        if not valid_csrf():
            return 'Session changed. Refresh the dashboard and try again.', 403
        session.clear()
        return redirect(url_for('home'))
