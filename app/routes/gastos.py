from flask import Blueprint, render_template, request, jsonify
from ..models.gastos import Gastos
from ..extensions import db, jwt
from instance.config import Config
from flask_jwt_extended import jwt_required, get_jwt_identity

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def inicio():
    return render_template('index.html')

@main_bp.route('/gastos', methods=['GET', 'POST'])
@jwt_required()
def gastos():
    current_user_id = get_jwt_identity()

    if request.method == 'POST':
        data = request.form
        categoria = data.get('categoria')
        total = data.get('total')
        pago = data.get('pago')

        if not categoria or total is None or not pago:
            return jsonify({'error': 'Faltan campos obligatorios'}), 400
        
        fecha = data.get('fecha')
        descripcion = data.get('descripcion')

        nuevo_gasto = Gastos(
            categoria=categoria,
            total=float(total),
            pago=pago,
            fecha=fecha,
            descripcion=descripcion,
            usuario_id=current_user_id)

        db.session.add(nuevo_gasto)
        db.session.commit()
        
        gastos = Gastos.query.filter_by(usuario_id=current_user_id).all()
        return render_template('gastos.html', gastos=gastos)

    gastos = Gastos.query.filter_by(usuario_id=current_user_id).all()
    return render_template('gastos.html', gastos=gastos)

