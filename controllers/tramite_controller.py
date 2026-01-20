from models.tramite import Tramite
from config.database import connectToMySQL

class TramiteController:
    
    @staticmethod
    def crear_tramite(nombre, descripcion, usuario_whatsapp):
        """CREATE - Crear nuevo trámite"""
        try:
            db = connectToMySQL('esquema_t')
            query = """
            INSERT INTO tramites (nombre, descripcion, usuario_whatsapp, estado)
            VALUES (%s, %s, %s, %s)
            """
            tramite_id = db.query_db(query, (nombre, descripcion, usuario_whatsapp, 'pendiente'))
            
            if tramite_id:
                return {
                    'success': True,
                    'mensaje': 'Trámite creado exitosamente',
                    'tramite_id': tramite_id
                }, 201
            else:
                return {'success': False, 'error': 'Error al crear trámite'}, 400
        except Exception as e:
            return {'success': False, 'error': str(e)}, 400

    @staticmethod
    def obtener_tramite(tramite_id):
        """READ - Obtener un trámite por ID"""
        try:
            db = connectToMySQL('esquema_t')
            query = "SELECT * FROM tramites WHERE id = %s"
            resultado = db.query_db(query, (tramite_id,))
            
            if resultado:
                tramite = Tramite(resultado[0])
                return {'success': True, 'tramite': tramite.to_dict()}, 200
            else:
                return {'success': False, 'error': 'Trámite no encontrado'}, 404
        except Exception as e:
            return {'success': False, 'error': str(e)}, 400

    @staticmethod
    def obtener_todos_tramites():
        """READ - Obtener todos los trámites"""
        try:
            db = connectToMySQL('esquema_t')
            query = "SELECT * FROM tramites ORDER BY fecha_creacion DESC"
            resultados = db.query_db(query)
            
            tramites = [Tramite(t).to_dict() for t in resultados] if resultados else []
            return {
                'success': True,
                'tramites': tramites,
                'total': len(tramites)
            }, 200
        except Exception as e:
            return {'success': False, 'error': str(e)}, 400

    @staticmethod
    def actualizar_tramite(tramite_id, **kwargs):
        """UPDATE - Actualizar un trámite"""
        try:
            db = connectToMySQL('esquema_t')
            
            # Verificar que el trámite existe
            query_check = "SELECT * FROM tramites WHERE id = %s"
            existe = db.query_db(query_check, (tramite_id,))
            
            if not existe:
                return {'success': False, 'error': 'Trámite no encontrado'}, 404
            
            # Construir dinámicamente la consulta UPDATE
            campos = []
            valores = []
            for key, value in kwargs.items():
                if key in ['nombre', 'descripcion', 'estado', 'usuario_whatsapp']:
                    campos.append(f"{key} = %s")
                    valores.append(value)
            
            if not campos:
                return {'success': False, 'error': 'No hay campos para actualizar'}, 400
            
            valores.append(tramite_id)
            query = f"UPDATE tramites SET {', '.join(campos)} WHERE id = %s"
            
            db.query_db(query, tuple(valores))
            
            # Retornar el trámite actualizado
            resultado = db.query_db(query_check, (tramite_id,))
            tramite = Tramite(resultado[0])
            return {'success': True, 'tramite': tramite.to_dict()}, 200
        except Exception as e:
            return {'success': False, 'error': str(e)}, 400

    @staticmethod
    def eliminar_tramite(tramite_id):
        """DELETE - Eliminar un trámite"""
        try:
            db = connectToMySQL('esquema_t')
            
            # Verificar que existe
            query_check = "SELECT * FROM tramites WHERE id = %s"
            existe = db.query_db(query_check, (tramite_id,))
            
            if not existe:
                return {'success': False, 'error': 'Trámite no encontrado'}, 404
            
            query = "DELETE FROM tramites WHERE id = %s"
            db.query_db(query, (tramite_id,))
            
            return {'success': True, 'mensaje': 'Trámite eliminado exitosamente'}, 200
        except Exception as e:
            return {'success': False, 'error': str(e)}, 400
