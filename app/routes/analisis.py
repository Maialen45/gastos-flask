from ..utils.decorators import roles_required
from flask import Blueprint, render_template
from flask_jwt_extended import jwt_required, get_jwt

analisis_bp = Blueprint('analisis', __name__)

@analisis_bp.route('/analisis', methods=['GET'])
@roles_required('admin', 'user')
@jwt_required()
def mostrar_analisis():
    claims = get_jwt()
    role = claims.get('role')
    return render_template('analisis.html', role=role)