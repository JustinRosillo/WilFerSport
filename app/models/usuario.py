from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)  # ← Añadido
    correo = db.Column(db.String(120), unique=True, nullable=False)
    contraseña_hash = db.Column(db.String(128), nullable=False)
    rol = db.Column(db.String(20), nullable=False)

    def set_password(self, password):
        self.contraseña_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.contraseña_hash, password)
