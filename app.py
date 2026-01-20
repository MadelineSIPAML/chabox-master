"""Aplicacion Flask para el chatbot ChaBox."""

from __future__ import annotations
import logging
import os
import sys
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from twilio.rest import Client
import google.generativeai as genai

# Cargar variables de entorno
load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s - %(message)s",
)

logger = logging.getLogger(__name__)

# Twilio setup
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')

try:
    twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    logger.info("✅ Twilio inicializado correctamente")
except Exception as e:
    logger.error(f"❌ Error al inicializar Twilio: {e}")
    twilio_client = None

# Google Gemini setup
try:
    genai.configure(api_key=os.getenv('GOOGLE_GEMINI_API_KEY'))
    model = genai.GenerativeModel('gemini-pro')
    logger.info("✅ Google Gemini inicializado correctamente")
except Exception as e:
    logger.error(f"❌ Error al inicializar Gemini: {e}")
    model = None


def create_app():
    """Crear y configurar la aplicación Flask."""
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    app.config['JSON_AS_ASCII'] = False
    
    @app.route('/', methods=['GET'])
    def health():
        return jsonify({'status': 'ok', 'message': 'ChaBox running'}), 200

    @app.route('/webhook', methods=['POST'])
    def webhook():
        try:
            incoming_msg = request.values.get('Body', '').strip()
            sender = request.values.get('From')
            
            logger.info(f"📨 Mensaje recibido de {sender}: {incoming_msg}")
            
            if not incoming_msg:
                return jsonify({'error': 'Mensaje vacío'}), 400
            
            if not model:
                return jsonify({'error': 'Gemini no configurado'}), 500
            
            # Generar respuesta con Gemini
            response = model.generate_content(incoming_msg)
            reply_text = response.text[:160]
            
            logger.info(f"🤖 Respuesta Gemini: {reply_text}")
            
            if not twilio_client:
                return jsonify({'error': 'Twilio no configurado'}), 500
            
            # Enviar respuesta por WhatsApp
            twilio_msg = twilio_client.messages.create(
                body=reply_text,
                from_=f"whatsapp:{TWILIO_PHONE_NUMBER}",
                to=sender
            )
            
            logger.info(f"✅ Mensaje enviado: {twilio_msg.sid}")
            return jsonify({'status': 'sent', 'sid': twilio_msg.sid}), 200
            
        except Exception as e:
            logger.error(f"❌ Error en webhook: {e}")
            return jsonify({'error': str(e)}), 500

    @app.route('/test', methods=['GET'])
    def test():
        return jsonify({
            'twilio': 'configurado' if TWILIO_ACCOUNT_SID else 'falta',
            'gemini': 'configurado' if os.getenv('GOOGLE_GEMINI_API_KEY') else 'falta',
            'mensaje': 'Sistema listo'
        }), 200
    
    # ❌ COMENTADO: No usar MySQL en Render (sin base de datos)
    # try:
    #     from models.tramite import Tramite
    #     logger.info("Creando tabla de trámites...")
    #     Tramite.crear_tabla()
    #     logger.info("Tabla de trámites lista")
    #     
    #     from routes import main_bp, tramite_bp, whatsapp_bp
    #     app.register_blueprint(main_bp)
    #     app.register_blueprint(tramite_bp)
    #     app.register_blueprint(whatsapp_bp)
    #     logger.info("Rutas registradas correctamente")
    # except Exception as e:
    #     logger.error(f"Error durante la inicialización: {e}")
    
    return app


app = create_app()

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000))
    app.run(debug=False, host='0.0.0.0', port=port)
