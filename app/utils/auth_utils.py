from functools import wraps
from flask import session, redirect, url_for
from datetime import datetime, timedelta

def login_requerido(f):
    @wraps(f)
    def decorador(*args, **kwargs):
        usuario_id = session.get("usuario_id")
        expiracion = session.get("expira_en")

        if not usuario_id or not expiracion:
            return redirect(url_for("auth.login"))

        if datetime.utcnow() > datetime.strptime(expiracion, "%Y-%m-%d %H:%M:%S"):
            session.clear()
            return redirect(url_for("auth.login"))

        # Renovar sesión
        session["expira_en"] = (datetime.utcnow() + timedelta(minutes=30)).strftime("%Y-%m-%d %H:%M:%S")
        return f(*args, **kwargs)
    return decorador
