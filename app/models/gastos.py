from ..extensions import db
from sqlalchemy.dialects.postgresql import NUMERIC

class Gastos(db.Model):
    __tablename__ = 'gastos'
    
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, nullable=True)
    categoria = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    total = db.Column(NUMERIC(10, 2), nullable=False)
    pago = db.Column(db.String(30), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)
    
    usuarios = db.Relationship('Usuario', back_populates='gastos')
