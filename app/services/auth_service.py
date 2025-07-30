from app.models.usuario import Usuario
from werkzeug.security import check_password_hash
from flask import session
from datetime import datetime, timedelta

def login_usuario(correo, contraseña):
    usuario = Usuario.query.filter_by(correo=correo).first()
    if usuario and check_password_hash(usuario.contraseña, contraseña):
        session['usuario_id'] = usuario.id
        session['usuario_nombre'] = usuario.nombre  # 👈 para mostrar en la navbar
        session['rol'] = usuario.rol
        session['expira_en'] = (datetime.utcnow() + timedelta(minutes=30)).strftime("%Y-%m-%d %H:%M:%S")
        return True
    return False

def logout_usuario():
    session.clear()

def usuario_actual():
    return session.get('usuario_id')

def rol_actual():
    return session.get('rol')
