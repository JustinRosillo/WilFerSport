from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.usuario import Usuario
from app import db
from datetime import datetime, timedelta

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        correo = request.form.get("correo")
        contraseña = request.form.get("contraseña")
        usuario = Usuario.query.filter_by(correo=correo).first()

        if usuario and usuario.check_password(contraseña):
            session["usuario_id"] = usuario.id
            session["usuario_rol"] = usuario.rol
            session["usuario_correo"] = usuario.correo
            session["usuario_nombre"] = usuario.nombre  # ← nuevo
            session["expira_en"] = (datetime.utcnow() + timedelta(minutes=30)).strftime("%Y-%m-%d %H:%M:%S")
            return redirect(url_for("dashboard.mostrar_dashboard"))

        flash("Correo o contraseña incorrectos.", "danger")

    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))
