from flask import Blueprint, redirect, render_template, request, jsonify
from ..models.gastos import Gastos
from ..extensions import db
from ..utils.decorators import roles_required
from flask_jwt_extended import jwt_required, get_jwt_identity

gastos_bp = Blueprint('gastos', __name__)

@gastos_bp.route('/')
def inicio():
    return render_template('index.html')

@gastos_bp.route('/gastos', methods=['GET', 'POST', 'DELETE'])
@roles_required('admin')
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
    
    categoria_filtro = request.args.get('categoria')

    if categoria_filtro:
        gastos = Gastos.query.filter_by(usuario_id=current_user_id, categoria=categoria_filtro).all()
    else:
        gastos = Gastos.query.filter_by(usuario_id=current_user_id).all()
    
    return render_template('gastos.html', gastos=gastos)

@gastos_bp.route('/gastos/eliminar/<int:gasto_id>', methods=['POST'])
@jwt_required()
def eliminar_gasto(gasto_id):
    current_user_id = get_jwt_identity()
    gasto = Gastos.query.filter_by(id=gasto_id, usuario_id=current_user_id).first()

    if not gasto:
        return jsonify({'error': 'Gasto no encontrado o sin permiso'}), 404
    
    db.session.delete(gasto)
    db.session.commit()

    return redirect('/gastos')