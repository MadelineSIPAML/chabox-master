from flask import Blueprint, request, jsonify
from controllers.tramite_controller import TramiteController

tramite_bp = Blueprint('tramites', __name__, url_prefix='/api/tramites')

@tramite_bp.route('', methods=['POST'])
def crear():
    """Crear nuevo trámite"""
    data = request.get_json()
    return TramiteController.crear_tramite(
        nombre=data.get('nombre'),
        descripcion=data.get('descripcion'),
        usuario_whatsapp=data.get('usuario_whatsapp')
    )

@tramite_bp.route('/<int:tramite_id>', methods=['GET'])
def obtener(tramite_id):
    """Obtener trámite por ID"""
    return TramiteController.obtener_tramite(tramite_id)

@tramite_bp.route('', methods=['GET'])
def obtener_todos():
    """Obtener todos los trámites"""
    return TramiteController.obtener_todos_tramites()

@tramite_bp.route('/<int:tramite_id>', methods=['PUT'])
def actualizar(tramite_id):
    """Actualizar trámite"""
    data = request.get_json()
    return TramiteController.actualizar_tramite(tramite_id, **data)

@tramite_bp.route('/<int:tramite_id>', methods=['DELETE'])
def eliminar(tramite_id):
    """Eliminar trámite"""
    return TramiteController.eliminar_tramite(tramite_id)
