#!/usr/bin/env python3
"""
Script para reparar la base de datos y ejecutar migraciones
"""

import sqlite3
import os
import sys


def fix_database():
    """Repara la base de datos agregando columnas faltantes"""

    db_path = 'servicio_tecnico.db'

    if not os.path.exists(db_path):
        print("Base de datos no encontrada.")
        return False

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Verificar si la tabla tecnicos existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='tecnicos'")
        if not cursor.fetchone():
            print("Tabla tecnicos no existe.")
            conn.close()
            return False

        # Verificar si la columna usuario_id existe
        cursor.execute("PRAGMA table_info(tecnicos)")
        columns = [column[1] for column in cursor.fetchall()]

        if 'usuario_id' not in columns:
            print("Agregando columna usuario_id a tecnicos...")
            cursor.execute("ALTER TABLE tecnicos ADD COLUMN usuario_id INTEGER")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_tecnicos_usuario_id ON tecnicos(usuario_id)")
            conn.commit()
            print("Columna usuario_id agregada exitosamente")
        else:
            print("Columna usuario_id ya existe")

        # Mostrar estructura actualizada
        cursor.execute("PRAGMA table_info(tecnicos)")
        columns = cursor.fetchall()
        print("\nEstructura de la tabla tecnicos:")
        for column in columns:
            print(f"  {column[1]} ({column[2]})")

        conn.close()
        return True

    except sqlite3.Error as e:
        print(f"Error: {e}")
        if conn:
            conn.rollback()
            conn.close()
        return False


if __name__ == "__main__":
    print("Reparando base de datos...")
    if fix_database():
        print("Base de datos reparada exitosamente")
    else:
        print("Error al reparar la base de datos")
