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

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

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
    
    # Definir rutas DENTRO de create_app
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
            reply_text = response.text[:160]  # Limitar a 160 caracteres
            
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
    
    try:
        # Importar modelos y utilidades
        from models.tramite import Tramite
        
        # Crear tabla al iniciar
        logger.info("Creando tabla de trámites...")
        Tramite.crear_tabla()
        logger.info("Tabla de trámites lista")
        
        # Registrar blueprints
        from routes import main_bp, tramite_bp, whatsapp_bp
        app.register_blueprint(main_bp)
        app.register_blueprint(tramite_bp)
        app.register_blueprint(whatsapp_bp)
        
        logger.info("Rutas registradas correctamente")
    except Exception as e:
        logger.error(f"Error durante la inicialización: {e}")
        raise
    
    return app


# Crear la aplicación para el servidor WSGI
app = create_app()

if __name__ == '__main__':
    try:
        print("\n" + "="*50)
        print("ChaBox iniciando...")
        print("="*50)
        print("Servidor: http://localhost:5000")
        print("Webhook: http://localhost:5000/webhook")
        print("Test: http://localhost:5000/test")
        print("="*50 + "\n")
        
        # En producción, usar puerto de la variable de entorno
        port = int(os.getenv('PORT', 5000))
        debug = os.getenv('FLASK_ENV', 'development') == 'development'
        app.run(debug=debug, host='0.0.0.0', port=port)
    except Exception as e:
        logger.critical(f"No se pudo iniciar la aplicación: {e}")
        sys.exit(1)
