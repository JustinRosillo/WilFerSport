from app import db
from app.models.producto import Producto
from sqlalchemy import or_

def crear_producto(nombre, categoria, talla, stock, precio):
    producto = Producto(
        nombre=nombre,
        categoria=categoria,
        talla=talla,
        stock=stock,
        precio=precio
    )
    db.session.add(producto)
    db.session.commit()
    return producto

def obtener_todos_productos():
    return Producto.query.all()

def buscar_productos(termino):
    return Producto.query.filter(
        or_(
            Producto.nombre.ilike(f"%{termino}%"),
            Producto.categoria.ilike(f"%{termino}%"),
            Producto.talla.ilike(f"%{termino}%")
        )
    ).all()

def obtener_producto_por_id(producto_id):
    return Producto.query.get(producto_id)

def actualizar_producto(producto_id, data):
    producto = Producto.query.get(producto_id)
    if not producto:
        return None
    producto.nombre = data["nombre"]
    producto.categoria = data["categoria"]
    producto.talla = data["talla"]
    producto.stock = data["stock"]
    producto.precio = data["precio"]
    db.session.commit()
    return producto

def eliminar_producto(producto_id):
    producto = Producto.query.get(producto_id)
    if not producto:
        return None
    db.session.delete(producto)
    db.session.commit()
    return True

def obtener_productos_stock_bajo():
    return Producto.query.filter(Producto.stock < 5).all()
