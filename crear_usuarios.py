# crear_usuarios.py

from app import create_app, db
from app.models.usuario import Usuario
from werkzeug.security import generate_password_hash

app = create_app()

usuarios_predefinidos = [
    {"nombre": "Administrador",   "correo": "admin@wfsport.com",     "password": "admin123", "rol": "admin"},
    {"nombre": "Vendedor Uno",    "correo": "vendedor1@wfsport.com", "password": "vend123",  "rol": "vendedor"},
    {"nombre": "Vendedor Dos",    "correo": "vendedor2@wfsport.com", "password": "vend456",  "rol": "vendedor"},
    {"nombre": "Vendedor Tres",   "correo": "vendedor3@wfsport.com", "password": "vend789",  "rol": "vendedor"},
]

with app.app_context():
    # Crear las tablas si no existen
    db.create_all()

    for u in usuarios_predefinidos:
        existe = Usuario.query.filter_by(correo=u["correo"]).first()
        if not existe:
            nuevo = Usuario(
                nombre=u["nombre"],  # ← Incluido para cumplir con NOT NULL
                correo=u["correo"],
                contraseña_hash=generate_password_hash(u["password"]),
                rol=u["rol"]
            )
            db.session.add(nuevo)
            print(f"✔ Usuario creado: {u['correo']} ({u['rol']})")
        else:
            print(f"⚠ Usuario ya existe: {u['correo']}")
    db.session.commit()
    print("✅ Usuarios cargados correctamente.")
