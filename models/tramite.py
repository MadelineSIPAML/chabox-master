from config.database import connectToMySQL

class Tramite:
    def __init__(self, datos):
        self.id = datos.get('id')
        self.nombre = datos.get('nombre')
        self.descripcion = datos.get('descripcion')
        self.estado = datos.get('estado', 'pendiente')
        self.usuario_whatsapp = datos.get('usuario_whatsapp')
        self.fecha_creacion = datos.get('fecha_creacion')
        self.fecha_actualizacion = datos.get('fecha_actualizacion')

    @classmethod
    def crear_tabla(cls):
        """Crear tabla en MySQL si no existe"""
        db = connectToMySQL('esquema_t')
        query = """
        CREATE TABLE IF NOT EXISTS tramites (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL,
            descripcion TEXT,
            estado VARCHAR(20) DEFAULT 'pendiente',
            usuario_whatsapp VARCHAR(20),
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
        """
        return db.query_db(query)

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'estado': self.estado,
            'usuario_whatsapp': self.usuario_whatsapp,
            'fecha_creacion': str(self.fecha_creacion),
            'fecha_actualizacion': str(self.fecha_actualizacion)
        }
