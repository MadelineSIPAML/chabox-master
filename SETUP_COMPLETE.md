# SETUP COMPLETO - CHABOX WHATSAPP

## ✅ LO QUE SE HIZO

### 1. Integración con Twilio WhatsApp
- **Archivo:** `routes/whatsapp.py`
- **Endpoints:**
  - `POST /api/whatsapp/webhook` - Recibe mensajes de WhatsApp
  - `POST /api/whatsapp/send` - Envía mensajes
  - `POST /api/whatsapp/status` - Notificaciones de estado

### 2. Configuración
- **Archivo:** `config/__init__.py` (NUEVO)
- **Variables de entorno:** TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER, GEMINI_API_KEY
- **Archivo .env.example** con todas las variables necesarias

### 3. Scripts de Ayuda
- **validate_setup.py** - Valida que todo esté configurado
- **quickstart.py** - Guía interactiva de setup
- **test_whatsapp.py** - Suite de tests

### 4. Documentación Completa
- **README_WHATSAPP.md** - Guía completa en español
- **WHATSAPP_SETUP.md** - Setup step-by-step
- **DEPLOYMENT.md** - Deploy a Heroku

### 5. Dependencias Instaladas
```
twilio==8.10.0
google-generativeai==0.8.6
```

### 6. Archivos para Heroku
- **Procfile** - Define cómo ejecutar en Heroku
- **runtime.txt** - Versión de Python

## 🚀 INICIO RÁPIDO

### Paso 1: Instalar dependencias
```bash
pip install -r requirements.txt
```

### Paso 2: Configurar .env
```bash
cp .env.example .env
# Edita .env con tus credenciales Twilio y Gemini
```

### Paso 3: Validar setup
```bash
python validate_setup.py
```

### Paso 4: Iniciar servidor
```bash
flask run
# o
python app.py
```

### Paso 5: Configurar webhook en Twilio Console
- URL: `https://tu-dominio.com/api/whatsapp/webhook`
- HTTP: POST

### Paso 6: Prueba
- Envía un mensaje WhatsApp a tu número Twilio
- Recibe respuesta automática 🎉

## 📁 ARCHIVOS NUEVOS/MODIFICADOS

```
✅ NUEVOS:
  - routes/whatsapp.py              (Integración WhatsApp)
  - config/__init__.py              (Configuración centralizada)
  - .env.example                    (Template de variables)
  - validate_setup.py               (Script de validación)
  - quickstart.py                   (Guía interactiva)
  - test_whatsapp.py                (Tests)
  - README_WHATSAPP.md              (Documentación completa)
  - WHATSAPP_SETUP.md               (Setup detallado)
  - DEPLOYMENT.md                   (Deploy a Heroku)
  - Procfile                        (Heroku)
  - runtime.txt                     (Heroku)

✅ MODIFICADOS:
  - routes/__init__.py              (Agregado blueprint whatsapp)
  - app.py                          (Agregado blueprint whatsapp)
  - requirements.txt                (Agregadas dependencias)
```

## 🔧 CONFIGURACIÓN NECESARIA

### 1. Twilio (Gratis)
- Registrate: https://www.twilio.com/console
- Obtén: ACCOUNT_SID, AUTH_TOKEN
- Activa WhatsApp beta
- Obtén número: whatsapp:+1234567890

### 2. Google Gemini (Gratis)
- Ve a: https://aistudio.google.com/apikey
- Crea API Key
- Copia en .env

### 3. Variables de Entorno (.env)
```env
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxx
TWILIO_PHONE_NUMBER=whatsapp:+1234567890
GEMINI_API_KEY=xxxxxxxxxxxxxxxx
SECRET_KEY=tu_clave_secreta
```

## 📊 ENDPOINTS

### Webhook (Automático)
```
POST /api/whatsapp/webhook
```
Twilio envía automáticamente los mensajes aquí.

### Enviar Mensaje
```bash
curl -X POST http://localhost:5000/api/whatsapp/send \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "+1234567890",
    "message": "Hola!"
  }'
```

### Status Callback
```
POST /api/whatsapp/status
```
Twilio notifica estado de entregas.

## ✨ CARACTERÍSTICAS

- ✅ Auto respuesta en WhatsApp
- ✅ Respuestas potenciadas por Google Gemini
- ✅ Respuestas por defecto en modo demo (sin API key)
- ✅ Manejo de errores robusto
- ✅ Logging completo
- ✅ Compatible con Heroku
- ✅ Tests unitarios incluidos
- ✅ Documentación completa en español

## 🧪 TESTING

### Local sin Twilio
```bash
curl -X POST http://localhost:5000/api/whatsapp/webhook \
  -d "Body=¿Cuál es el precio?&From=whatsapp:+1234567890"
```

### Con Python
```python
from model.assistant import generate_response
response = generate_response("Hola")
print(response)
```

## 🚢 DEPLOYMENT A HEROKU

```bash
# 1. Agregar Procfile y runtime.txt (YA ESTÁN)

# 2. Git setup
git add .
git commit -m "Add WhatsApp integration"
heroku login
heroku create tu-app-name

# 3. Configurar variables
heroku config:set TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxx
heroku config:set TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxx
heroku config:set TWILIO_PHONE_NUMBER=whatsapp:+1234567890
heroku config:set GEMINI_API_KEY=xxxxxxxxxxxxxxxx

# 4. Deploy
git push heroku main

# 5. Configurar webhook en Twilio
# URL: https://tu-app.herokuapp.com/api/whatsapp/webhook
```

Ver logs:
```bash
heroku logs --tail
```

## 🐛 TROUBLESHOOTING

### Error: "Module not found"
```bash
pip install -r requirements.txt
```

### Error: "Invalid credentials"
- Verifica .env tiene credenciales correctas
- Copia exactamente desde Twilio (sin espacios)

### No recibe mensajes
1. Verifica URL webhook en Twilio es correcta
2. Ver logs: `heroku logs --tail`
3. Test local: `curl -X POST http://localhost:5000/api/whatsapp/webhook ...`

### Error de encoding (Windows)
```bash
python validate_setup.py
```

## 📚 DOCUMENTACIÓN

- **README_WHATSAPP.md** - Guía completa
- **WHATSAPP_SETUP.md** - Setup paso a paso
- **DEPLOYMENT.md** - Deploy a Heroku
- **validate_setup.py** - Revisa automáticamente

## 🎯 PRÓXIMOS PASOS

1. ✅ Setup técnico completado
2. [ ] Registrate en Twilio
3. [ ] Obtén API key de Gemini
4. [ ] Edita .env con credenciales
5. [ ] Ejecuta `python validate_setup.py`
6. [ ] Ejecuta `flask run`
7. [ ] Configura webhook en Twilio
8. [ ] Prueba enviando mensaje WhatsApp
9. [ ] Deploy a Heroku (opcional)

## 📞 SOPORTE

- Twilio: https://www.twilio.com/docs/whatsapp
- Gemini: https://ai.google.dev
- Flask: https://flask.palletsprojects.com
- Heroku: https://devcenter.heroku.com

---

## ¡LISTO!

Tu aplicación está 100% lista para usar WhatsApp. Solo completa:

1. Credenciales Twilio ← **TODO AHORA**
2. API key Gemini ← **TODO AHORA**
3. Inicia el servidor
4. Configura webhook
5. ¡Prueba! 🚀

```bash
# Validar todo
python validate_setup.py

# Iniciar
flask run
```

**¡Que disfrutes de tu auto respuesta en WhatsApp! 📱**

---

Creado: 19 de Enero, 2026
Sistema: Chabox WhatsApp Integration v1.0
