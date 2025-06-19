from flask import Blueprint, redirect, render_template, request, jsonify
from ..models.ingresos import Ingresos
from ..models.usuario import Usuario
from ..extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity

ingresos_bp = Blueprint('ingresos', __name__)

@ingresos_bp.route('/')
def inicio():
    return render_template('index.html')

@ingresos_bp.route('/ingresos', methods=['GET', 'POST'])
@jwt_required()
def ingresos():
    current_user_id = get_jwt_identity()
    usuario = Usuario.query.get(current_user_id)

    if request.method == 'POST':
        data = request.form
        categoria = data.get('categoria')
        total = data.get('total')
        pago = data.get('pago')

        if not categoria or total is None or not pago:
            return jsonify({'error': 'Faltan campos obligatorios'}), 400
        
        fecha = data.get('fecha')
        descripcion = data.get('descripcion')

        nuevo_gasto = Ingresos(
            categoria=categoria,
            total=float(total),
            pago=pago,
            fecha=fecha,
            descripcion=descripcion,
            usuario_id=current_user_id)

        db.session.add(nuevo_gasto)
        db.session.commit()
        
        ingresos = Ingresos.query.filter_by(usuario_id=current_user_id).all()
        return render_template('ingresos.html', ingresos=ingresos, usuario=usuario)
    
    categoria_filtro = request.args.get('categoria')

    if categoria_filtro:
        ingresos = Ingresos.query.filter_by(usuario_id=current_user_id, categoria=categoria_filtro).all()
    else:
        ingresos = Ingresos.query.filter_by(usuario_id=current_user_id).all()
    
    return render_template('ingresos.html', ingresos=ingresos, usuario=usuario)

@ingresos_bp.route('/ingresos/eliminar/<int:ingreso_id>', methods=['POST'])
@jwt_required()
def eliminar_ingreso(ingreso_id):
    current_user_id = get_jwt_identity()
    ingreso = Ingresos.query.filter_by(id=ingreso_id, usuario_id=current_user_id).first()

    if not ingreso:
        return jsonify({'error': 'Gasto no encontrado o sin permiso'}), 404
    
    db.session.delete(ingreso)
    db.session.commit()

    return redirect('/ingresos')