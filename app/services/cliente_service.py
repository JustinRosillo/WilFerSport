from app import db
from app.models.cliente import Cliente

def crear_cliente(data):
    cliente = Cliente(
        nombre=data["nombre"],
        correo=data["correo"],
        telefono=data.get("telefono"),
        direccion=data.get("direccion")
    )
    db.session.add(cliente)
    db.session.commit()
    return cliente

def obtener_todos_clientes():
    return Cliente.query.all()

def obtener_cliente_por_id(cliente_id):
    return Cliente.query.get(cliente_id)
