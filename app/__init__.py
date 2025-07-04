from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

# Inicializar extensiones
db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar extensiones con la app
    db.init_app(app)
    login_manager.init_app(app)

    # Configurar Flask-Login
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Debe iniciar sesión para acceder a esta página.'
    login_manager.login_message_category = 'info'

    @login_manager.user_loader
    def load_user(user_id):
        from app.models.models import Usuario
        return Usuario.query.get(int(user_id))

    # Registrar blueprints
    from app.controllers.main import main_bp
    from app.controllers.auth import auth_bp
    from app.controllers.clientes import clientes_bp
    from app.controllers.solicitudes import solicitudes_bp
    from app.controllers.asignaciones import asignaciones_bp
    from app.controllers.facturas import facturas_bp
    from app.controllers.servicios import servicios_bp
    from app.controllers.tecnicos import tecnicos_bp
   
    from app.controllers.partes import partes_bp
    from app.controllers.reportes import reportes_bp
    from app.controllers.tecnico import tecnico_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(clientes_bp, url_prefix='/clientes')
    app.register_blueprint(solicitudes_bp, url_prefix='/solicitudes')
    app.register_blueprint(asignaciones_bp, url_prefix='/asignaciones')
    app.register_blueprint(facturas_bp, url_prefix='/facturas')
    app.register_blueprint(servicios_bp, url_prefix='/servicios')
    app.register_blueprint(tecnicos_bp, url_prefix='/tecnicos')
    
    app.register_blueprint(partes_bp, url_prefix='/partes')
    app.register_blueprint(reportes_bp, url_prefix='/reportes')
    app.register_blueprint(tecnico_bp, url_prefix='/tecnico')

    # Crear tablas y datos iniciales
    with app.app_context():
        db.create_all()
        create_initial_data()

    return app


def create_initial_data():
    """Crea datos iniciales si no existen"""
    from app.models.models import Usuario, Cliente, Servicio, Tecnico, Parte

    try:
        # Crear usuario administrador si no existe
        admin = Usuario.query.filter_by(email='admin@servicio.com').first()
        if not admin:
            admin = Usuario(
                nombre='Administrador Sistema',
                email='admin@servicio.com',
                telefono='1111111111',
                rol='administrador'
            )
            admin.set_password('admin123')
            db.session.add(admin)

        # Crear usuario técnico si no existe
        tecnico_user = Usuario.query.filter_by(email='tecnico@servicio.com').first()
        if not tecnico_user:
            tecnico_user = Usuario(
                nombre='Juan Técnico',
                email='tecnico@servicio.com',
                telefono='2222222222',
                rol='tecnico'
            )
            tecnico_user.set_password('tecnico123')
            db.session.add(tecnico_user)

        # Crear usuario normal si no existe
        usuario_normal = Usuario.query.filter_by(email='usuario@servicio.com').first()
        if not usuario_normal:
            usuario_normal = Usuario(
                nombre='María Usuario',
                email='usuario@servicio.com',
                telefono='3333333333',
                rol='usuario'
            )
            usuario_normal.set_password('usuario123')
            db.session.add(usuario_normal)

        db.session.commit()

        # Crear perfil de técnico si no existe
        perfil_tecnico = Tecnico.query.filter_by(email='tecnico@servicio.com').first()
        if not perfil_tecnico:
            perfil_tecnico = Tecnico(
                usuario_id=tecnico_user.id,
                nombre='Juan Técnico',
                email='tecnico@servicio.com',
                telefono='2222222222',
                especialidad='Hardware y Software',
                nivel_experiencia='senior'
            )
            db.session.add(perfil_tecnico)

        # Crear algunos clientes de ejemplo si no existen
        if Cliente.query.count() == 0:
            clientes_ejemplo = [
                Cliente(nombre='Juan Pérez', email='juan@email.com', telefono='3001234567',
                        direccion='Calle 123 #45-67', tipo_cliente='particular'),
                Cliente(nombre='Empresa ABC S.A.S.', email='contacto@abc.com', telefono='3012345678',
                        direccion='Carrera 45 #12-34', tipo_cliente='empresa')
            ]
            for cliente in clientes_ejemplo:
                db.session.add(cliente)

        # Crear algunos servicios de ejemplo si no existen
        if Servicio.query.count() == 0:
            servicios_ejemplo = [
                Servicio(nombre='Reparación de Computadores', descripcion='Diagnóstico y reparación de equipos',
                         precio_base=80000, categoria='Hardware'),
                Servicio(nombre='Instalación de Software', descripcion='Instalación y configuración de programas',
                         precio_base=50000, categoria='Software'),
                Servicio(nombre='Mantenimiento Preventivo', descripcion='Limpieza y optimización de equipos',
                         precio_base=60000, categoria='Mantenimiento')
            ]
            for servicio in servicios_ejemplo:
                db.session.add(servicio)

        # Crear algunas partes de ejemplo si no existen
        if Parte.query.count() == 0:
            partes_ejemplo = [
                Parte(nombre='Memoria RAM DDR4 8GB', codigo='RAM-DDR4-8GB',
                      descripcion='Memoria RAM DDR4 de 8GB', precio=180000, stock=25,
                      stock_minimo=5, proveedor='TechSupply'),
                Parte(nombre='Disco SSD 240GB', codigo='SSD-240GB',
                      descripcion='Disco de estado sólido 240GB', precio=220000, stock=15,
                      stock_minimo=3, proveedor='StoragePro')
            ]
            for parte in partes_ejemplo:
                db.session.add(parte)

        db.session.commit()
        print("✅ Datos iniciales creados correctamente")

    except Exception as e:
        print(f"❌ Error creando datos iniciales: {e}")
        db.session.rollback()
