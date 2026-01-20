#!/usr/bin/env python
"""Script de setup y validación para Chabox WhatsApp."""

import os
import sys
import json
from pathlib import Path

def check_requirements():
    """Verifica que todas las dependencias estén instaladas."""
    print("\n📦 Verificando dependencias...")
    
    required_packages = {
        'flask': 'Flask',
        'twilio': 'Twilio',
        'google.generativeai': 'Google Generative AI',
        'mysql': 'PyMySQL',
        'dotenv': 'python-dotenv'
    }
    
    missing = []
    for module, name in required_packages.items():
        try:
            __import__(module)
            print(f"  ✓ {name}")
        except ImportError:
            print(f"  ✗ {name} (faltante)")
            missing.append(name)
    
    if missing:
        print(f"\n⚠️  Faltan dependencias: {', '.join(missing)}")
        print("Ejecuta: pip install -r requirements.txt")
        return False
    
    print("  ✓ Todas las dependencias están instaladas\n")
    return True


def check_env_file():
    """Verifica que exista el archivo .env con las variables necesarias."""
    print("📋 Verificando variables de entorno...")
    
    env_file = Path('.env')
    
    if not env_file.exists():
        print("  ✗ Archivo .env no encontrado")
        print("  💡 Copia .env.example a .env y completa los valores")
        return False
    
    # Cargar .env
    env_vars = {}
    with open('.env', 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                if '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key.strip()] = value.strip()
    
    required_vars = {
        'TWILIO_ACCOUNT_SID': 'SID de tu cuenta Twilio',
        'TWILIO_AUTH_TOKEN': 'Token de autenticación de Twilio',
        'TWILIO_PHONE_NUMBER': 'Número de WhatsApp de Twilio (formato: whatsapp:+1234567890)',
        'GEMINI_API_KEY': 'Clave API de Google Gemini'
    }
    
    missing_vars = []
    for var, description in required_vars.items():
        if var in env_vars and env_vars[var]:
            print(f"  ✓ {var}")
        else:
            print(f"  ✗ {var} (faltante o vacío)")
            print(f"     → {description}")
            missing_vars.append(var)
    
    if missing_vars:
        print(f"\n⚠️  Faltan configurar: {', '.join(missing_vars)}")
        return False
    
    print("  ✓ Todas las variables están configuradas\n")
    return True


def check_twilio_connectivity():
    """Verifica que Twilio esté configurado correctamente."""
    print("🔗 Verificando conexión con Twilio...")
    
    try:
        from twilio.rest import Client
        
        account_sid = os.getenv('TWILIO_ACCOUNT_SID', '')
        auth_token = os.getenv('TWILIO_AUTH_TOKEN', '')
        
        if not account_sid or not auth_token:
            print("  ⚠️  Credenciales de Twilio no configuradas")
            return False
        
        # Intentar conectar
        client = Client(account_sid, auth_token)
        account = client.api.accounts(account_sid).fetch()
        
        print(f"  ✓ Conectado a Twilio")
        print(f"  ✓ Cuenta: {account.friendly_name}")
        print(f"  ✓ Estado: {account.status}\n")
        
        return True
    
    except Exception as e:
        print(f"  ✗ Error conectando a Twilio: {e}\n")
        return False


def test_assistant():
    """Prueba que el asistente funciona correctamente."""
    print("🤖 Probando asistente de IA...")
    
    try:
        from model.assistant import generate_response
        
        test_message = "¿Cuál es el precio?"
        response = generate_response(test_message)
        
        print(f"  Test input: '{test_message}'")
        print(f"  Test output: '{response}'")
        print("  ✓ Asistente funcionando correctamente\n")
        
        return True
    
    except Exception as e:
        print(f"  ✗ Error probando asistente: {e}\n")
        return False


def test_flask_routes():
    """Verifica que las rutas Flask estén registradas."""
    print("🛣️  Verificando rutas Flask...")
    
    try:
        from app import app
        
        routes = []
        for rule in app.url_map.iter_rules():
            if not rule.endpoint.startswith('static'):
                routes.append(str(rule))
        
        whatsapp_routes = [r for r in routes if 'whatsapp' in r]
        
        if whatsapp_routes:
            print("  ✓ Rutas de WhatsApp detectadas:")
            for route in whatsapp_routes:
                print(f"    - {route}")
        else:
            print("  ⚠️  No se encontraron rutas de WhatsApp")
            return False
        
        print()
        return True
    
    except Exception as e:
        print(f"  ✗ Error verificando rutas: {e}\n")
        return False


def create_setup_guide():
    """Crea un archivo de guía de setup."""
    guide = """
    
╔═══════════════════════════════════════════════════════════════════╗
║           GUÍA DE SETUP - CHABOX WHATSAPP INTEGRATION             ║
╚═══════════════════════════════════════════════════════════════════╝

1️⃣  REGISTRARSE EN TWILIO
   → https://www.twilio.com/console
   → Verificar número de teléfono
   → Obtener ACCOUNT_SID y AUTH_TOKEN

2️⃣  ACTIVAR WHATSAPP EN TWILIO
   → Console → Messaging → Try it out
   → Seleccionar WhatsApp (beta)
   → Obtener número de teléfono: whatsapp:+1234567890

3️⃣  CONFIGURAR VARIABLES DE ENTORNO
   → Copiar: cp .env.example .env
   → Editar: cat .env
   → Completar:
     • TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxx
     • TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxx
     • TWILIO_PHONE_NUMBER=whatsapp:+1234567890
     • GEMINI_API_KEY=tu_clave_api_aqui

4️⃣  INSTALAR DEPENDENCIAS
   $ pip install -r requirements.txt

5️⃣  PRUEBA LOCAL (sin webhook)
   $ python
   >>> from model.assistant import generate_response
   >>> generate_response("Hola")
   
6️⃣  CONFIGURAR WEBHOOK EN TWILIO
   → Console → Messaging → Services
   → Messaging Service → Inbound Settings
   → URL: https://tudominio.com/api/whatsapp/webhook
   → HTTP: POST
   
7️⃣  PROBAR ENVIANDO MENSAJE
   → Abre WhatsApp
   → Envía mensaje a tu número de Twilio
   → ¡Recibe respuesta automática!

═══════════════════════════════════════════════════════════════════

ENDPOINTS DISPONIBLES:
   POST /api/whatsapp/webhook    ← Recibe mensajes (Twilio)
   POST /api/whatsapp/send       ← Envía mensajes
   POST /api/whatsapp/status     ← Actualización de estado

PARA PRODUCCIÓN (HEROKU):
   $ heroku config:set TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxx
   $ heroku config:set TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxx
   $ heroku config:set TWILIO_PHONE_NUMBER=whatsapp:+1234567890
   $ heroku config:set GEMINI_API_KEY=tu_clave_api_aqui
   $ git push heroku main

═══════════════════════════════════════════════════════════════════
"""
    print(guide)


def main():
    """Ejecuta todas las verificaciones."""
    print("\n" + "="*70)
    print("INICIANDO VERIFICACIÓN DE CHABOX WHATSAPP")
    print("="*70)
    
    checks = [
        ("Dependencias", check_requirements),
        ("Variables de entorno", check_env_file),
        ("Asistente de IA", test_assistant),
        ("Rutas Flask", test_flask_routes),
        ("Conexión Twilio", check_twilio_connectivity),
    ]
    
    results = {}
    for check_name, check_func in checks:
        try:
            results[check_name] = check_func()
        except Exception as e:
            print(f"❌ Error en {check_name}: {e}\n")
            results[check_name] = False
    
    # Resumen
    print("="*70)
    print("📊 RESUMEN DE VERIFICACIÓN")
    print("="*70)
    
    for check_name, result in results.items():
        status = "✓" if result else "✗"
        print(f"  {status} {check_name}")
    
    all_passed = all(results.values())
    
    if all_passed:
        print("\n" + "🎉 " * 10)
        print("✅ TODOS LOS CHECKS PASARON - ¡LISTO PARA USAR!")
        print("🎉 " * 10)
        print("\nPara iniciar el servidor:")
        print("  $ flask run")
        print("  o")
        print("  $ python app.py")
    else:
        print("\n" + "⚠️  " * 10)
        print("❌ ALGUNOS CHECKS FALLARON")
        print("⚠️  " * 10)
        print("\nRevisa los errores arriba y completa la configuración.")
    
    create_setup_guide()


if __name__ == '__main__':
    main()
