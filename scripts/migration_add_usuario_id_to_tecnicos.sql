-- Migración: Agregar columna usuario_id a la tabla tecnicos
-- Fecha: 2024-01-07

-- Agregar la columna usuario_id a la tabla tecnicos
ALTER TABLE tecnicos ADD COLUMN usuario_id INTEGER;

-- Crear índice para mejorar el rendimiento
CREATE INDEX IF NOT EXISTS idx_tecnicos_usuario_id ON tecnicos(usuario_id);

-- Actualizar datos existentes (opcional)
-- Si ya tienes técnicos y quieres asociarlos con usuarios existentes
-- UPDATE tecnicos SET usuario_id = (SELECT id FROM usuarios WHERE email = tecnicos.email AND rol = 'tecnico') WHERE tecnicos.email IS NOT NULL;

-- Verificar la estructura actualizada
-- SELECT sql FROM sqlite_master WHERE type='table' AND name='tecnicos';
