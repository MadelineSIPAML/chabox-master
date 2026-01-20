#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Script simple de validación para Chabox WhatsApp."""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Configurar encoding para Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("\n" + "="*70)
print("VALIDACION RAPIDA - CHABOX WHATSAPP")
print("="*70 + "\n")

# 1. Verificar dependencias
print("[1] Verificando dependencias...")
try:
    import flask
    import twilio
    import google.generativeai
    import pymysql
    import dotenv
    print("    OK: Todas las dependencias instaladas\n")
except ImportError as e:
    print(f"    ERROR: {e}\n")
    sys.exit(1)

# 2. Verificar archivo .env
print("[2] Verificando configuracion .env...")
if not Path('.env').exists():
    print("    ADVERTENCIA: .env no encontrado")
    print("    Copia .env.example a .env y completa los valores\n")
else:
    print("    OK: Archivo .env existe\n")

# Cargar variables de entorno
load_dotenv()

# 3. Verificar credenciales requeridas
print("[3] Verificando credenciales requeridas...")
required_vars = [
    'TWILIO_ACCOUNT_SID',
    'TWILIO_AUTH_TOKEN',
    'TWILIO_PHONE_NUMBER',
    'GOOGLE_GEMINI_API_KEY'
]

missing_vars = [var for var in required_vars if not os.getenv(var)]
if missing_vars:
    print(f"    ERROR: Faltan variables en .env: {', '.join(missing_vars)}")
    sys.exit(1)
else:
    print("    OK: Todas las credenciales están configuradas correctamente\n")

# 4. Verificar rutas WhatsApp
print("[4] Verificando rutas Flask...")
try:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from routes.whatsapp import whatsapp_bp
    print("    OK: Blueprint de WhatsApp importado\n")
except Exception as e:
    print(f"    ERROR: {e}\n")
    sys.exit(1)

# 5. Verificar asistente
print("[5] Verificando asistente...")
try:
    from model.assistant import generate_response
    test_response = generate_response("test")
    print(f"    OK: Asistente funciona\n")
except Exception as e:
    print(f"    ERROR: {e}\n")
    sys.exit(1)

print("="*70)
print("CHECKLIST DE SETUP:")
print("="*70)
print("""
[OK] Dependencias instaladas
[OK] Rutas WhatsApp cargadas
[OK] Asistente funcionando

PASOS SIGUIENTES:
=================
1. Registrate en https://www.twilio.com/console
2. Completa .env con tus credenciales:
   - TWILIO_ACCOUNT_SID
   - TWILIO_AUTH_TOKEN
   - TWILIO_PHONE_NUMBER=whatsapp:+1234567890
   - GEMINI_API_KEY=tu_clave_aqui

3. Ejecuta el servidor:
   $ python app.py
   o
   $ flask run

4. Configura webhook en Twilio:
   URL: https://tudominio.com/api/whatsapp/webhook

5. Prueba enviando un mensaje a tu numero de WhatsApp

ENDPOINTS DISPONIBLES:
======================
POST /api/whatsapp/webhook   -> Recibe mensajes
POST /api/whatsapp/send      -> Envia mensajes
POST /api/whatsapp/status    -> Actualizaciones de estado
""")
print("="*70 + "\n")
print(">>> Listo para usar! Completa la configuracion de Twilio.\n")

# Validación de configuración
print("Validando configuración...")
missing = [var for var in required_vars if not os.getenv(var)]

if missing:
    print(f"❌ Faltan variables: {', '.join(missing)}")
    exit(1)
else:
    print("✅ Todas las credenciales están configuradas")
