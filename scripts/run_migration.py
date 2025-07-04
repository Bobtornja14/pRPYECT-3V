#!/usr/bin/env python3
"""
Script para ejecutar migraciones de base de datos
"""

import sqlite3
import os
import sys


def run_migration():
    """Ejecuta la migración para agregar usuario_id a tecnicos"""

    # Ruta a la base de datos
    db_path = 'servicio_tecnico.db'

    if not os.path.exists(db_path):
        print("Base de datos no encontrada. Creando nueva base de datos...")
        return

    try:
        # Conectar a la base de datos
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Verificar si la columna ya existe
        cursor.execute("PRAGMA table_info(tecnicos)")
        columns = [column[1] for column in cursor.fetchall()]

        if 'usuario_id' in columns:
            print("La columna usuario_id ya existe en la tabla tecnicos.")
            return

        print("Ejecutando migración: Agregando columna usuario_id a tecnicos...")

        # Agregar la columna usuario_id
        cursor.execute("ALTER TABLE tecnicos ADD COLUMN usuario_id INTEGER")

        # Crear índice
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_tecnicos_usuario_id ON tecnicos(usuario_id)")

        # Confirmar cambios
        conn.commit()

        print("Migración completada exitosamente.")

        # Mostrar estructura actualizada
        cursor.execute("PRAGMA table_info(tecnicos)")
        columns = cursor.fetchall()
        print("\nEstructura actualizada de la tabla tecnicos:")
        for column in columns:
            print(f"  {column[1]} ({column[2]})")

    except sqlite3.Error as e:
        print(f"Error durante la migración: {e}")
        conn.rollback()

    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    run_migration()
