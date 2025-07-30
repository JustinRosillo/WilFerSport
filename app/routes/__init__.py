# app/routes/__init__.py

from flask import Blueprint

# Importar blueprints individuales
from .auth import auth_bp
from .productos import productos_bp
from .clientes import clientes_bp
from .ventas import ventas_bp
# crea otro si deseas para dashboard

def register_routes(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(productos_bp, url_prefix="/productos")
    app.register_blueprint(clientes_bp, url_prefix="/clientes")
    app.register_blueprint(ventas_bp, url_prefix="/ventas")
