# app/services/venta_service.py

from datetime import datetime, timedelta
from app import db
from app.models.venta import Venta
from app.models.detalle_venta import DetalleVenta
from app.models.producto import Producto


def registrar_venta_completa(cliente_id, carrito):
    total = sum(item['cantidad'] * item['precio'] for item in carrito)

    nueva_venta = Venta(
        cliente_id=cliente_id,
        total=total,
        fecha_venta=datetime.utcnow()
    )
    db.session.add(nueva_venta)
    db.session.flush()  # Para obtener venta_id antes del commit

    for item in carrito:
        # Agregar detalle de venta
        detalle = DetalleVenta(
            venta_id=nueva_venta.id,
            producto_id=item['id'],
            cantidad=item['cantidad'],
            precio_unitario=item['precio']
        )
        db.session.add(detalle)

        # Descontar stock
        producto = Producto.query.get(item['id'])
        if producto:
            if producto.stock >= item['cantidad']:
                producto.stock -= item['cantidad']
            else:
                raise Exception(f"Stock insuficiente para el producto: {producto.nombre}")
        else:
            raise Exception(f"Producto con ID {item['id']} no encontrado")

    db.session.commit()
    return nueva_venta


def obtener_todas_ventas(fecha_inicio=None):
    query = DetalleVenta.query.join(Venta).join(Venta.cliente)

    if fecha_inicio:
        try:
            fecha_dt = datetime.strptime(fecha_inicio, "%Y-%m-%d")
            siguiente_dia = fecha_dt + timedelta(days=1)
            query = query.filter(Venta.fecha_venta >= fecha_dt, Venta.fecha_venta < siguiente_dia)
        except ValueError:
            pass  # Si la fecha es inválida, ignora el filtro

    return query.all()


def obtener_total_ventas():
    ventas = Venta.query.all()
    return sum(venta.total for venta in ventas)
