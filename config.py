import os
from datetime import timedelta


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-servicio-tecnico-2024'

    # Base de datos SQLite en el directorio principal
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL') or f'sqlite:///{os.path.join(basedir, "instance/servicio_tecnico.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configuración de sesiones
    PERMANENT_SESSION_LIFETIME = timedelta(hours=8)

    # Configuración de paginación
    POSTS_PER_PAGE = 10

    # Configuración de archivos
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
