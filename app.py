import os
from app import create_app, db

app = create_app()

with app.app_context():
    # Crear directorio instance si no existe
    os.makedirs(app.instance_path, exist_ok=True)
    # Ejecutar migración para agregar usuario_id a tecnicos si falta
    from app.migrations import add_usuario_id_to_tecnicos
    add_usuario_id_to_tecnicos()
    # Crear las tablas si no existen
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
