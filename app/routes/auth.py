from flask import Blueprint, jsonify, request, render_template, make_response, redirect
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity,
    get_jwt, set_access_cookies
)
from ..extensions import jwt
from ..models.usuario import Usuario
from app import db
from datetime import datetime, timezone
from ..utils.validators import validate_email, validate_password

auth_bp = Blueprint('auth', __name__)

# Lista negra de tokens revocados (en producción usar Redis)
BLACKLIST = set()

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.form

        username = data.get('username')
        password = data.get('password')

        # Validaciones
        if not username or not password:
            return render_template('register.html', error='Todos los campos son obligatorios')
        
        if not validate_password(password):
            return render_template('register.html', error='Contraseña muy corta')

        if Usuario.query.filter_by(username=username).first():
            return render_template('register.html', error='Usuario ya existe')

        # Crear nuevo usuario
        usuario = Usuario(username=username)
        usuario.set_password(password)

        db.session.add(usuario)
        db.session.commit()

        return render_template('register.html')
    else:
        return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form

        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return render_template('login.html', error='Usuario y contraseña requeridos')
        
        # Buscar usuario por username o email
        usuario = Usuario.query.filter_by(username=username).first()

        if not usuario or not usuario.check_password(password):
            return render_template('login.html', error='Credenciales inválidas')

        # Crear token JWT
        access_token = create_access_token(identity=str(usuario.id))
        response = make_response(render_template('dashboard.html', usuario=usuario, token=access_token))
        set_access_cookies(response, access_token)

        return response
    else:
        return render_template('login.html')

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()['jti'] 
    print(jti)
    BLACKLIST.add(jti)
    return jsonify({'mensaje': 'Sesión cerrada exitosamente'})

# Middleware de protección
@jwt.token_in_blocklist_loader
def is_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    print(f"Verificando si el token está en BLACKLIST: {jti}")
    return jti in BLACKLIST

@jwt.revoked_token_loader
def revoked_token_response(jwt_header, jwt_payload):
    return jsonify({'msg': 'Token ha sido revocado'}), 401
############


# Endpoint protegido de ejemplo
@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    current_user_id = get_jwt_identity()
    usuario = Usuario.query.get(current_user_id)
    if not usuario:
        return jsonify({'error': 'Usuario no encontrado'}), 404
    return jsonify(usuario.to_dict())