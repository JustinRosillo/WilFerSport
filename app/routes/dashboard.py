# app/routes/dashboard.py

from flask import Blueprint, render_template, session, redirect, url_for
from app.utils.auth_utils import login_requerido
from app.services import venta_service, producto_service
from datetime import date

# Este blueprint se registrará con: url_prefix="/dashboard"
dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/")
@login_requerido
def mostrar_dashboard():
    rol = session.get("usuario_rol")

    if rol not in ["admin", "vendedor"]:
        return redirect(url_for("auth.logout"))

    total_ventas_dia = 0.0
    total_ventas = 0.0
    stock_critico = []

    if rol == "admin":
        # Ventas del día (suma total por día)
        detalles_hoy = venta_service.obtener_todas_ventas(fecha_inicio=str(date.today()))
        total_ventas_dia = sum(d.cantidad * d.precio_unitario for d in detalles_hoy)

        # Total acumulado de todas las ventas
        total_ventas = venta_service.obtener_total_ventas()

        # Productos con stock menor a 5
        stock_critico = producto_service.obtener_productos_stock_bajo()

    return render_template(
        "dashboard.html",
        rol=rol,
        total_ventas_dia=total_ventas_dia,
        total_ventas=total_ventas,
        stock_critico=stock_critico
    )
