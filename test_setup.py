import os
from dotenv import load_dotenv
from twilio.rest import Client
import google.generativeai as genai

load_dotenv()

print("\n🔍 Verificando configuración...\n")

# Test 1: Variables de entorno
print("1️⃣  Variables de entorno:")
required_vars = [
    'TWILIO_ACCOUNT_SID',
    'TWILIO_AUTH_TOKEN',
    'TWILIO_PHONE_NUMBER',
    'GOOGLE_GEMINI_API_KEY'
]

for var in required_vars:
    value = os.getenv(var)
    if value and value != f'your_{var.lower()}':
        print(f"   ✅ {var}")
    else:
        print(f"   ❌ {var} - Falta o no configurado")

# Test 2: Conexión Twilio
print("\n2️⃣  Twilio Connection:")
try:
    client = Client(os.getenv('TWILIO_ACCOUNT_SID'), os.getenv('TWILIO_AUTH_TOKEN'))
    account = client.api.accounts(os.getenv('TWILIO_ACCOUNT_SID')).fetch()
    print(f"   ✅ Cuenta Twilio: {account.friendly_name}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 3: Google Gemini
print("\n3️⃣  Google Gemini API:")
try:
    genai.configure(api_key=os.getenv('GOOGLE_GEMINI_API_KEY'))
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content("Hola, ¿cómo estás?")
    print(f"   ✅ Respuesta: {response.text[:50]}...")
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n✨ Verificación completada\n")
