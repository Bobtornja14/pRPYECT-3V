-- Script para crear datos de ejemplo en el sistema

-- Insertar clientes de ejemplo
INSERT INTO clientes (nombre, email, telefono, direccion, tipo_cliente, activo) VALUES
('Juan Pérez', 'juan.perez@email.com', '3001234567', 'Calle 123 #45-67, Bogotá', 'particular', 1),
('María García', 'maria.garcia@email.com', '3007654321', 'Carrera 45 #12-34, Medellín', 'particular', 1),
('Empresa ABC S.A.S.', 'contacto@empresaabc.com', '3012345678', 'Avenida 68 #23-45, Bogotá', 'empresa', 1),
('Carlos Rodríguez', 'carlos.rodriguez@email.com', '3009876543', 'Calle 67 #89-12, Cali', 'particular', 1),
('Tecnología XYZ Ltda.', 'info@tecnologiaxyz.com', '3015678901', 'Carrera 15 #34-56, Barranquilla', 'empresa', 1);

-- Insertar servicios de ejemplo
INSERT INTO servicios (nombre, descripcion, precio_base, categoria, activo) VALUES
('Reparación de Computadores', 'Diagnóstico y reparación de equipos de cómputo', 80000, 'Hardware', 1),
('Instalación de Software', 'Instalación y configuración de programas', 50000, 'Software', 1),
('Mantenimiento Preventivo', 'Limpieza y optimización de equipos', 60000, 'Mantenimiento', 1),
('Recuperación de Datos', 'Recuperación de información perdida', 150000, 'Datos', 1),
('Configuración de Redes', 'Instalación y configuración de redes', 120000, 'Redes', 1),
('Soporte Técnico Remoto', 'Asistencia técnica a distancia', 40000, 'Soporte', 1),
('Actualización de Hardware', 'Mejora de componentes del equipo', 100000, 'Hardware', 1),
('Instalación de Antivirus', 'Instalación y configuración de antivirus', 35000, 'Seguridad', 1);

-- Insertar técnicos de ejemplo
INSERT INTO tecnicos (nombre, email, telefono, especialidad, nivel_experiencia, activo) VALUES
('Andrés Martínez', 'andres.martinez@servicio.com', '3201234567', 'Hardware y Reparaciones', 'senior', 1),
('Laura Sánchez', 'laura.sanchez@servicio.com', '3207654321', 'Redes y Comunicaciones', 'experto', 1),
('Diego Morales', 'diego.morales@servicio.com', '3212345678', 'Software y Sistemas', 'senior', 1),
('Ana Jiménez', 'ana.jimenez@servicio.com', '3209876543', 'Seguridad Informática', 'junior', 1),
('Roberto Silva', 'roberto.silva@servicio.com', '3215678901', 'Soporte Técnico', 'senior', 1);

-- Insertar partes de ejemplo
INSERT INTO partes (nombre, codigo, descripcion, precio, stock, stock_minimo, proveedor, activo) VALUES
('Memoria RAM DDR4 8GB', 'RAM-DDR4-8GB', 'Memoria RAM DDR4 de 8GB para computadores', 180000, 25, 5, 'TechSupply S.A.', 1),
('Disco Duro SSD 240GB', 'SSD-240GB', 'Disco de estado sólido de 240GB', 220000, 15, 3, 'StoragePro Ltda.', 1),
('Fuente de Poder 500W', 'PSU-500W', 'Fuente de alimentación de 500W certificada', 150000, 10, 2, 'PowerTech', 1),
('Tarjeta de Red WiFi', 'WIFI-CARD', 'Tarjeta de red inalámbrica USB', 45000, 30, 8, 'NetworkPlus', 1),
('Cable HDMI 2m', 'HDMI-2M', 'Cable HDMI de 2 metros de longitud', 25000, 50, 10, 'CableTech', 1),
('Teclado USB', 'KB-USB', 'Teclado estándar con conexión USB', 35000, 20, 5, 'PeripheralPro', 1),
('Mouse Óptico', 'MOUSE-OPT', 'Mouse óptico con conexión USB', 20000, 25, 5, 'PeripheralPro', 1),
('Ventilador CPU', 'FAN-CPU', 'Ventilador para procesador', 60000, 12, 3, 'CoolingTech', 1);

-- Insertar solicitudes de ejemplo
INSERT INTO solicitudes (cliente_id, servicio_id, descripcion_problema, prioridad, estado, fecha_solicitud) VALUES
(1, 1, 'El computador no enciende después de una tormenta eléctrica', 'alta', 'pendiente', datetime('now', '-2 days')),
(2, 3, 'El equipo está muy lento y hace mucho ruido', 'media', 'pendiente', datetime('now', '-1 day')),
(3, 5, 'Necesitan configurar la red de la oficina nueva', 'alta', 'asignada', datetime('now', '-3 days')),
(4, 2, 'Requiere instalación de software contable', 'media', 'en_proceso', datetime('now', '-5 days')),
(5, 4, 'Se perdieron archivos importantes del servidor', 'urgente', 'asignada', datetime('now', '-1 day')),
(1, 6, 'Problemas con el correo electrónico', 'baja', 'completada', datetime('now', '-7 days')),
(2, 8, 'Instalación de antivirus en varios equipos', 'media', 'pendiente', datetime('now'));

-- Insertar asignaciones de ejemplo
INSERT INTO asignaciones (solicitud_id, tecnico_id, fecha_asignacion, estado, observaciones, tiempo_estimado) VALUES
(3, 2, datetime('now', '-3 days'), 'en_proceso', 'Configuración de red empresarial con 20 equipos', 8),
(4, 3, datetime('now', '-5 days'), 'en_proceso', 'Instalación de software contable y capacitación', 4),
(5, 1, datetime('now', '-1 day'), 'asignada', 'Recuperación urgente de base de datos', 6),
(6, 5, datetime('now', '-7 days'), 'completada', 'Configuración de Outlook completada', 2);

-- Insertar facturas de ejemplo
INSERT INTO facturas (numero_factura, cliente_id, solicitud_id, fecha_emision, subtotal, impuestos, total, estado, observaciones) VALUES
('FAC-001', 1, 6, datetime('now', '-6 days'), 40000, 7600, 47600, 'pagada', 'Soporte técnico remoto - Configuración email'),
('FAC-002', 3, NULL, datetime('now', '-4 days'), 120000, 22800, 142800, 'pendiente', 'Configuración de red empresarial - Pendiente de pago'),
('FAC-003', 2, NULL, datetime('now', '-2 days'), 60000, 11400, 71400, 'pendiente', 'Mantenimiento preventivo programado');
