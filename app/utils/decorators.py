from functools import wraps
from flask import flash, redirect, url_for
from flask_jwt_extended import get_jwt, jwt_required

def roles_required(*roles):
    def wrapper(fn):
        @wraps(fn)
        @jwt_required()
        def decorated_function(*args, **kwargs):
            claims = get_jwt()
            user_role = claims.get('role')

            if user_role not in roles:
                flash('No tiene permiso para acceder a esta página', 'danger')
                return redirect(url_for('ingresos.inicio'))
            return fn(*args, **kwargs)
        
        return decorated_function
    return wrapper
            