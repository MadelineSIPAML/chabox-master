"""Rutas para integración con WhatsApp usando Twilio."""

from flask import Blueprint, request, jsonify
import logging
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from model.assistant import generate_response
import os

logger = logging.getLogger(__name__)

whatsapp_bp = Blueprint('whatsapp', __name__, url_prefix='/api/whatsapp')

# Credenciales de Twilio (debes agregarlas a .env)
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID', '')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN', '')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER', 'whatsapp:+1234567890')

# Inicializar cliente de Twilio
if TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN:
    twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
else:
    twilio_client = None


@whatsapp_bp.route('/webhook', methods=['POST'])
def webhook():
    """
    Webhook para recibir mensajes de WhatsApp desde Twilio.
    Se configura en la consola de Twilio.
    """
    try:
        # Obtener datos del mensaje
        incoming_msg = request.values.get('Body', '').strip()
        sender = request.values.get('From', '')
        
        logger.info(f"Mensaje recibido de {sender}: {incoming_msg}")
        
        if not incoming_msg:
            return jsonify({"status": "ok"}), 200
        
        # Generar respuesta usando el asistente
        response_text = generate_response(incoming_msg)
        
        # Crear respuesta TwiML
        resp = MessagingResponse()
        resp.message(response_text)
        
        logger.info(f"Respuesta enviada a {sender}: {response_text}")
        
        return str(resp), 200
        
    except Exception as e:
        logger.error(f"Error en webhook de WhatsApp: {e}")
        resp = MessagingResponse()
        resp.message("Disculpa, ocurrió un error procesando tu mensaje.")
        return str(resp), 200


@whatsapp_bp.route('/send', methods=['POST'])
def send_message():
    """
    Endpoint para enviar un mensaje a WhatsApp desde tu aplicación.
    
    Body JSON:
    {
        "phone": "+34123456789",
        "message": "Tu mensaje aquí"
    }
    """
    if not twilio_client:
        return jsonify({"error": "Twilio no configurado"}), 400
    
    try:
        data = request.get_json()
        phone = data.get('phone')
        message = data.get('message')
        
        if not phone or not message:
            return jsonify({"error": "Falta 'phone' o 'message'"}), 400
        
        # Enviar mensaje
        msg = twilio_client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NUMBER,
            to=f'whatsapp:{phone}'
        )
        
        logger.info(f"Mensaje enviado a {phone}: SID={msg.sid}")
        
        return jsonify({
            "status": "enviado",
            "message_sid": msg.sid
        }), 200
        
    except Exception as e:
        logger.error(f"Error enviando mensaje por WhatsApp: {e}")
        return jsonify({"error": str(e)}), 500


@whatsapp_bp.route('/status', methods=['POST'])
def status_callback():
    """
    Webhook para recibir actualizaciones de estado de mensajes.
    Se configura en la consola de Twilio para recibir confirmaciones de entrega.
    """
    try:
        msg_sid = request.values.get('MessageSid')
        msg_status = request.values.get('MessageStatus')
        
        logger.info(f"Actualización de estado - SID: {msg_sid}, Estado: {msg_status}")
        
        return jsonify({"status": "ok"}), 200
    
    except Exception as e:
        logger.error(f"Error en callback de estado: {e}")
        return jsonify({"status": "ok"}), 200
