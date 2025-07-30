# app/routes/clientes.py

from flask import Blueprint, request, redirect, url_for, render_template, session, flash
from app.services import cliente_service
from functools import wraps
from datetime import datetime, timedelta

clientes_bp = Blueprint('clientes', __name__, template_folder='../templates/clientes')

# ================================
# MIDDLEWARE DE AUTENTICACIÓN
# ================================

def login_requerido(f):
    @wraps(f)
    def decorador(*args, **kwargs):
        usuario_id = session.get('usuario_id')
        expiracion = session.get('expira_en')

        if not usuario_id or not expiracion:
            return redirect(url_for('auth.login'))

        if datetime.utcnow() > datetime.strptime(expiracion, "%Y-%m-%d %H:%M:%S"):
            session.clear()
            return redirect(url_for('auth.login'))

        session['expira_en'] = (datetime.utcnow() + timedelta(minutes=30)).strftime("%Y-%m-%d %H:%M:%S")
        return f(*args, **kwargs)
    return decorador

# ================================
# RUTAS DE CLIENTES
# ================================

@clientes_bp.route("/registrar", methods=["GET", "POST"])
@login_requerido
def registrar_cliente():
    if request.method == "POST":
        data = {
            "nombre": request.form["nombre"],
            "correo": request.form["correo"],
            "telefono": request.form.get("telefono"),
            "direccion": request.form.get("direccion")
        }

        try:
            cliente_service.crear_cliente(data)
            flash("Cliente registrado exitosamente", "success")
            return redirect(url_for("clientes.registrar_cliente"))
        except Exception as e:
            flash("Error: El correo ya está registrado o hubo un problema al guardar", "danger")
            return render_template("clientes/registrar.html")

    return render_template("clientes/registrar.html")
