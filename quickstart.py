#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
QUICK START - Chabox WhatsApp Integration
==========================================

Este script te guia paso a paso para activar WhatsApp.
"""

import os
import sys
import json
from pathlib import Path

def print_header(title):
    """Imprime encabezado."""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")

def check_env():
    """Verifica que .env exista."""
    if not Path('.env').exists():
        print("ERROR: No existe .env")
        print("Solución: Copia .env.example a .env")
        return False
    
    # Cargar .env
    env_vars = {}
    with open('.env', 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                env_vars[key.strip()] = value.strip()
    
    return env_vars

def main():
    print_header("CHABOX - AUTO RESPUESTA WHATSAPP")
    
    print("""
Este script te ayuda a configurar la integración WhatsApp en minutos.

REQUISITOS:
- Cuenta en Twilio (gratis): https://www.twilio.com
- Google Gemini API (gratis): https://aistudio.google.com
- Python 3.9+
    """)
    
    input("\nPresiona ENTER para continuar...")
    
    # Paso 1: Validar setup básico
    print_header("PASO 1: Validando Configuración")
    
    # Verificar dependencias
    print("[*] Verificando dependencias...")
    try:
        import flask, twilio, google.generativeai, pymysql, dotenv
        print("[OK] Todas las dependencias están instaladas")
    except ImportError as e:
        print(f"[ERROR] Falta instalar: {e}")
        print("Solución: pip install -r requirements.txt")
        return
    
    # Verificar .env
    print("[*] Verificando archivo .env...")
    env_vars = check_env()
    if not env_vars:
        print("[ERROR] .env no encontrado")
        return
    print("[OK] Archivo .env existe")
    
    # Paso 2: Obtener credenciales
    print_header("PASO 2: Configurar Twilio")
    
    print("""
INSTRUCCIONES:
1. Ve a https://www.twilio.com/console
2. En el dashboard, copia:
   - Account SID
   - Auth Token
3. Ve a Messaging > Services > WhatsApp
4. Obtén tu número: whatsapp:+1234567890

Completa tu .env con:
- TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxx
- TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxx
- TWILIO_PHONE_NUMBER=whatsapp:+1234567890
    """)
    
    twilio_ready = input("\n¿Ya tienes tus credenciales de Twilio? (s/n): ").lower() == 's'
    
    if not twilio_ready:
        print("\nPor favor, completa primero tu .env con credenciales Twilio.")
        return
    
    # Paso 3: Configurar Gemini
    print_header("PASO 3: Configurar Google Gemini")
    
    print("""
INSTRUCCIONES:
1. Ve a https://aistudio.google.com/apikey
2. Click en "Create API Key"
3. Copia la clave generada

Completa tu .env con:
- GEMINI_API_KEY=xxxxxxxxxxxxxxxx
    """)
    
    gemini_ready = input("\n¿Ya configuraste Google Gemini? (s/n): ").lower() == 's'
    
    if not gemini_ready:
        print("\nPor favor, completa primero tu .env con GEMINI_API_KEY.")
        return
    
    # Paso 4: Probar localmente
    print_header("PASO 4: Prueba Local")
    
    print("[*] Probando asistente de IA...")
    try:
        from model.assistant import generate_response
        response = generate_response("Hola, prueba")
        print(f"[OK] Asistente funcionando")
        print(f"\n    Respuesta de prueba: '{response[:80]}...'")
    except Exception as e:
        print(f"[ERROR] {e}")
        return
    
    # Paso 5: Iniciar servidor
    print_header("PASO 5: Iniciar Servidor")
    
    print("""
Tu servidor estará disponible en: http://localhost:5000

Para iniciar, ejecuta uno de estos comandos:
    
    flask run
    
o

    python app.py

El servidor debe estar corriendo para que Twilio envíe los mensajes.
    """)
    
    start_server = input("¿Deseas iniciar el servidor ahora? (s/n): ").lower() == 's'
    
    if start_server:
        print("\n[*] Iniciando servidor Flask...")
        print("    Servidor ejecutándose en http://localhost:5000")
        print("    Presiona CTRL+C para detener\n")
        
        try:
            os.system('flask run')
        except KeyboardInterrupt:
            print("\n\n[OK] Servidor detenido")
    
    # Paso 6: Configurar webhook
    print_header("PASO 6: Configurar Webhook en Twilio")
    
    print("""
PARA PRODUCCION:
1. Despliega tu app en Heroku, AWS, etc.
2. Obtén tu URL pública (ej: https://my-app.herokuapp.com)

PARA TESTING LOCAL:
1. Instala ngrok: https://ngrok.com/download
2. Ejecuta: ngrok http 5000
3. Copia la URL: https://xxxxxx.ngrok.io

EN TWILIO CONSOLE:
1. Ve a Messaging > Services > Tu servicio
2. Inbound Settings
3. Request URL: https://tu-url.com/api/whatsapp/webhook
4. HTTP Method: POST
5. Click Save

Luego, envía un mensaje a tu numero WhatsApp y recibira respuesta automatica!
    """)
    
    print_header("CONFIGURACION COMPLETA!")
    
    print("""
RESUMEN:
- Dependencias: OK
- .env: Configurado
- Asistente: Funcionando
- Servidor: Listo para iniciar
- Webhook: Pendiente (Configura en Twilio)

PRÓXIMOS PASOS:
1. Configura webhook en Twilio console
2. Envía un mensaje WhatsApp a tu numero Twilio
3. Recibe respuesta automatica!

ENDPOINTS DISPONIBLES:
- POST /api/whatsapp/webhook  -> Recibe mensajes
- POST /api/whatsapp/send     -> Envia mensajes
- POST /api/whatsapp/status   -> Estados

DOCUMENTACION COMPLETA:
- Lee: README_WHATSAPP.md

¿Preguntas? Consulta la documentacion oficial de Twilio:
https://www.twilio.com/docs/whatsapp
    """)
    
    print("="*70 + "\n")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[*] Operación cancelada por el usuario")
        sys.exit(0)
    except Exception as e:
        print(f"\n[ERROR] {e}")
        sys.exit(1)
