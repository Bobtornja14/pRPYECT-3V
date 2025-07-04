#!/usr/bin/env python3
"""
Script para verificar el estado de la base de datos
"""

import sys
import os
import sqlite3

# Agregar el directorio padre al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models.models import Usuario, Tecnico


def check_database():
    """Verifica el estado de la base de datos"""

    app = create_app()

    with app.app_context():
        try:
            print("=== VERIFICACIÓN DE BASE DE DATOS ===\n")

            # Verificar usuarios
            usuarios = Usuario.query.all()
            print(f"Total de usuarios: {len(usuarios)}")

            if usuarios:
                print("\nUsuarios encontrados:")
                for usuario in usuarios:
                    print(f"  - {usuario.nombre}")
                    print(f"    Email: {usuario.email}")
                    print(f"    Rol: {usuario.rol}")
                    print(f"    Activo: {'✅' if usuario.activo else '❌'}")
                    print(f"    ID: {usuario.id}")
                    print()
            else:
                print("❌ No hay usuarios en la base de datos")
                print("Ejecute: python scripts/reset_users.py")

            # Verificar técnicos
            tecnicos = Tecnico.query.all()
            print(f"Total de técnicos: {len(tecnicos)}")

            if tecnicos:
                print("\nTécnicos encontrados:")
                for tecnico in tecnicos:
                    print(f"  - {tecnico.nombre}")
                    print(f"    Email: {tecnico.email}")
                    print(f"    Usuario ID: {tecnico.usuario_id}")
                    print(f"    Activo: {'✅' if tecnico.activo else '❌'}")
                    print()

            # Verificar estructura de tablas
            print("=== ESTRUCTURA DE TABLAS ===")
            db_path = 'servicio_tecnico.db'
            if os.path.exists(db_path):
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()

                # Verificar tabla usuarios
                cursor.execute("PRAGMA table_info(usuarios)")
                columns = cursor.fetchall()
                print(f"\nTabla 'usuarios' - {len(columns)} columnas:")
                for col in columns:
                    print(f"  {col[1]} ({col[2]})")

                # Verificar tabla tecnicos
                cursor.execute("PRAGMA table_info(tecnicos)")
                columns = cursor.fetchall()
                print(f"\nTabla 'tecnicos' - {len(columns)} columnas:")
                for col in columns:
                    print(f"  {col[1]} ({col[2]})")

                conn.close()

        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    check_database()
