from flask import Blueprint, request, redirect, url_for, render_template, session, flash
from app.services import producto_service
from app.models.producto import Producto
from app import db
from functools import wraps
from datetime import datetime, timedelta

productos_bp = Blueprint('productos', __name__, template_folder='../templates/productos')

# ========================
# MIDDLEWARE AUTENTICACIÓN
# ========================
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

def solo_admin(f):
    @wraps(f)
    def decorador(*args, **kwargs):
        if session.get('usuario_rol') != 'admin':
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorador

# ========================
# RUTAS DE PRODUCTOS
# ========================

@productos_bp.route("/", methods=["GET"])
@login_requerido
def listar_productos():
    query = request.args.get("q", "").strip()
    if query:
        productos = producto_service.buscar_productos(query)
    else:
        productos = producto_service.obtener_todos_productos()
    return render_template("productos/listar.html", productos=productos)

@productos_bp.route("/registrar", methods=["GET", "POST"])
@login_requerido
@solo_admin
def registrar_producto():
    if request.method == "POST":
        producto_id = request.form.get('id')
        nombre = request.form['nombre']
        categoria = request.form['categoria']
        talla = request.form['talla']
        stock = int(request.form['stock'])
        precio = float(request.form['precio'])

        if producto_id:  # 🔄 EDICIÓN
            producto = Producto.query.get_or_404(producto_id)
            producto.nombre = nombre
            producto.categoria = categoria
            producto.talla = talla
            producto.stock = stock
            producto.precio = precio
            db.session.commit()
            flash("Producto actualizado correctamente", "success")
        else:  # ➕ CREACIÓN
            producto_service.crear_producto(nombre, categoria, talla, stock, precio)
            flash("Producto registrado exitosamente", "success")

        return redirect(url_for("productos.registrar_producto"))

    # GET: mostrar formulario vacío + lista
    productos = producto_service.obtener_todos_productos()
    return render_template("productos/registrar.html", productos=productos)


__all__ = ["productos_bp"]

@productos_bp.route('/editar/<int:id>', methods=["GET"])
def editar_producto(id):
    producto = Producto.query.get_or_404(id)
    productos = Producto.query.all()
    return render_template("productos/registrar.html", producto=producto, productos=productos)

@productos_bp.route('/eliminar/<int:id>', methods=["GET"])
def eliminar_producto(id):
    producto = Producto.query.get_or_404(id)
    db.session.delete(producto)
    db.session.commit()
    flash("Producto eliminado exitosamente.", "success")
    return redirect(url_for("productos.registrar_producto"))
