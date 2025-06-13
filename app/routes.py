from flask import Blueprint, render_template, request, jsonify
from .models import Gastos
from .extensions import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def inicio():
    return render_template('index.html')

@main_bp.route('/gastos', methods=['GET', 'POST'])
def gastos():
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
            descripcion=descripcion)

        db.session.add(nuevo_gasto)
        db.session.commit()
        
        gastos = Gastos.query.all()
        return render_template('gastos.html', gastos=gastos)

    gastos = Gastos.query.all()
    return render_template('gastos.html', gastos=gastos)

