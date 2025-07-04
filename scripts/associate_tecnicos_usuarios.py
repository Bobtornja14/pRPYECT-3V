#!/usr/bin/env python3
"""
Script para activar el administrador y verificar usuarios
"""

import sys
import os
import sqlite3


def activate_admin():
    """Activa el usuario administrador"""

    db_path = 'servicio_tecnico.db'

    if not os.path.exists(db_path):
        print("❌ Base de datos no encontrada.")
        print("Ejecute primero: python app.py")
        return False

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Verificar si existe la tabla usuarios
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='usuarios'")
        if not cursor.fetchone():
            print("❌ Tabla usuarios no existe.")
            conn.close()
            return False

        # Verificar usuarios existentes
        cursor.execute("SELECT id, nombre, email, rol, activo FROM usuarios")
        usuarios = cursor.fetchall()

        print("=== USUARIOS ACTUALES ===")
        for usuario in usuarios:
            id_user, nombre, email, rol, activo = usuario
            estado = "✅ Activo" if activo else "❌ Inactivo"
            print(f"ID: {id_user} | {nombre} | {email} | {rol} | {estado}")

        # Activar todos los usuarios
        cursor.execute("UPDATE usuarios SET activo = 1")
        rows_affected = cursor.rowcount

        conn.commit()

        print(f"\n✅ {rows_affected} usuarios activados")

        # Mostrar usuarios después de la actualización
        cursor.execute("SELECT id, nombre, email, rol, activo FROM usuarios")
        usuarios = cursor.fetchall()

        print("\n=== USUARIOS DESPUÉS DE ACTIVAR ===")
        for usuario in usuarios:
            id_user, nombre, email, rol, activo = usuario
            estado = "✅ Activo" if activo else "❌ Inactivo"
            print(f"ID: {id_user} | {nombre} | {email} | {rol} | {estado}")

        print("\n🔑 CREDENCIALES PARA LOGIN:")
        print("   Admin: admin@servicio.com / admin123")
        print("   Técnico: tecnico@servicio.com / tecnico123")
        print("   Usuario: usuario@servicio.com / usuario123")

        conn.close()
        return True

    except sqlite3.Error as e:
        print(f"❌ Error: {e}")
        if conn:
            conn.rollback()
            conn.close()
        return False


if __name__ == "__main__":
    print("🔧 Activando usuarios...")
    if activate_admin():
        print("✅ Usuarios activados correctamente")
    else:
        print("❌ Error al activar usuarios")
