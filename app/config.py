import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "secreto_por_defecto")
    PERMANENT_SESSION_LIFETIME = 1800  # 30 minutos
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "../wilfer.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
