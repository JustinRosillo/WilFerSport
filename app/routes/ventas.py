# app/routes/ventas.py

from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.services import cliente_service, producto_service, venta_service
from app.routes.productos import login_requerido
import json

ventas_bp = Blueprint("ventas", __name__, template_folder="../templates/ventas")


@ventas_bp.route("/registrar", methods=["GET", "POST"])
@login_requerido
def registrar_venta():
    if request.method == "POST":
        cliente_id = request.form.get("cliente_id")
        carrito_json = request.form.get("carrito")

        if not cliente_id or not carrito_json:
            flash("Faltan datos para registrar la venta", "danger")
            return redirect(url_for("ventas.registrar_venta"))

        try:
            carrito = json.loads(carrito_json)
            venta_service.registrar_venta_completa(cliente_id, carrito)
            flash("Venta registrada correctamente", "success")
        except Exception as e:
            flash(f"Error al registrar la venta: {str(e)}", "danger")

        return redirect(url_for("ventas.registrar_venta"))

    clientes = cliente_service.obtener_todos_clientes()
    productos = producto_service.obtener_todos_productos()
    return render_template("ventas/registrar.html", clientes=clientes, productos=productos)


@ventas_bp.route("/reportes", methods=["GET"])
@login_requerido
def reporte_ventas():
    fecha_inicio = request.args.get("fecha_inicio")
    ventas = venta_service.obtener_todas_ventas(fecha_inicio)
    return render_template("reportes/index.html", ventas=ventas)

