from flask import redirect, url_for, session, flash
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Por favor inicia sesión para acceder a esta página.', 'warning')
            return redirect(url_for('auth_controller.login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_rol' not in session or session['user_rol'] != 'admin':
            flash('No tienes permisos para acceder a esta página.', 'error')
            return redirect(url_for('dashboard_controller.index'))
        return f(*args, **kwargs)
    return decorated_function