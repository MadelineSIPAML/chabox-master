-- Crear base de datos
CREATE DATABASE IF NOT EXISTS esquema_t CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Usar la base de datos
USE esquema_t;

-- Tabla de trámites
CREATE TABLE IF NOT EXISTS tramites (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    estado VARCHAR(20) DEFAULT 'pendiente',
    usuario_whatsapp VARCHAR(20),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_estado (estado),
    INDEX idx_usuario_whatsapp (usuario_whatsapp)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Verificar que todo fue creado correctamente
SHOW DATABASES LIKE 'esquema_t';
SHOW TABLES IN esquema_t;
DESCRIBE tramites;
