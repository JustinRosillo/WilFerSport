from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    # Importar y registrar Blueprints
    from app.routes.auth import auth_bp
    from app.routes.productos import productos_bp
    from app.routes.clientes import clientes_bp
    from app.routes.ventas import ventas_bp
    from app.routes.dashboard import dashboard_bp  # NUEVO

    app.register_blueprint(auth_bp, url_prefix="/")
    app.register_blueprint(productos_bp, url_prefix="/productos")
    app.register_blueprint(clientes_bp, url_prefix="/clientes")
    app.register_blueprint(ventas_bp, url_prefix="/ventas")
    app.register_blueprint(dashboard_bp, url_prefix="/dashboard")  # NUEVO

    with app.app_context():
        from . import models

    return app
