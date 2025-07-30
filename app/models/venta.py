# app/models/venta.py

from app import db
from datetime import datetime

class Venta(db.Model):
    __tablename__ = 'ventas'

    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    total = db.Column(db.Float, nullable=False)
    fecha_venta = db.Column(db.DateTime, default=datetime.utcnow)

    # Relaciones
    cliente = db.relationship('Cliente', backref='ventas')
    detalles = db.relationship('DetalleVenta', backref='venta', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Venta ID {self.id} - Cliente {self.cliente_id}>"
