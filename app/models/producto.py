from app import db

class Producto(db.Model):
    __tablename__ = 'productos'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    talla = db.Column(db.String(10), nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    precio = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<Producto {self.nombre} ({self.categoria})>"
