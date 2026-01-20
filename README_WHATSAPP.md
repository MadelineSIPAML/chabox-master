# Chabox - Integración WhatsApp con Twilio

Auto respuesta automática en WhatsApp usando Twilio y Google Gemini.

## Resumen Rápido ⚡

Tu chatbot ahora responde automáticamente en WhatsApp. Solo necesitas:

1. Crear cuenta en Twilio
2. Completar variables de entorno
3. Ejecutar el servidor
4. Configurar webhook en Twilio
5. ¡Listo! Recibe respuestas automáticas

## Instalación

### 1. Instalar Dependencias

```bash
pip install -r requirements.txt
```

Verify con:
```bash
python validate_setup.py
```

### 2. Configurar Credenciales

**Copia el archivo de ejemplo:**
```bash
cp .env.example .env
```

**Edita `.env` con tus credenciales:**

```env
# Google Gemini
GEMINI_API_KEY=tu_clave_de_api_google_gemini

# Twilio WhatsApp
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxxxx
TWILIO_PHONE_NUMBER=whatsapp:+1234567890

# Flask
SECRET_KEY=tu_clave_secreta_aqui
```

## Obtener Credenciales de Twilio

### Paso 1: Crear Cuenta
1. Ve a https://www.twilio.com/console
2. Regístrate con tu email
3. Verifica tu número de teléfono
4. En el dashboard, copia:
   - **ACCOUNT_SID**
   - **AUTH TOKEN**

### Paso 2: Activar WhatsApp
1. Ve a **Messaging** → **Services** (o **Try it out**)
2. Selecciona **Whatsapp** (beta)
3. Verifica tu número
4. Obtén tu número de Twilio en formato: `whatsapp:+1234567890`

### Paso 3: Obtener API Key de Google Gemini
1. Ve a https://aistudio.google.com/apikey
2. Click "Create API Key"
3. Copia la clave generada

## Ejecutar el Servidor

```bash
# Opción 1: Con Flask
flask run

# Opción 2: Con Python
python app.py

# Opción 3: Producción (Gunicorn)
gunicorn app:app
```

El servidor estará disponible en `http://localhost:5000`

## Configurar Webhook en Twilio

1. **Obtén tu URL pública:**
   - Local: `https://localhost:5000/api/whatsapp/webhook` (no funciona local)
   - Producción: `https://tudominio.com/api/whatsapp/webhook`
   - Testing: Usa `ngrok` para exponer local: `ngrok http 5000`

2. **Configura en Twilio Console:**
   - Ve a **Messaging** → **Services** → Tu servicio
   - Sección **Inbound Settings**
   - **Request URL:** `https://tu-url.com/api/whatsapp/webhook`
   - **HTTP Method:** `POST`
   - Click **Save**

3. **Status Callback (opcional):**
   - **Status Callback URL:** `https://tu-url.com/api/whatsapp/status`

## Endpoints Disponibles

### Webhook (Recibe Mensajes)
```
POST /api/whatsapp/webhook
```
Twilio envía los mensajes aquí automáticamente. **No necesitas llamarlo manualmente.**

Ejemplo de datos que recibe:
```
Body: "Hola, ¿cuál es el precio?"
From: "whatsapp:+1234567890"
MessageSid: "SMxxxxxxxxxxxxxxxx"
```

### Enviar Mensaje
```
POST /api/whatsapp/send
Content-Type: application/json

{
  "phone": "+1234567890",
  "message": "Hola! Este es un mensaje de prueba"
}
```

Respuesta:
```json
{
  "status": "enviado",
  "message_sid": "SMxxxxxxxxxxxxxxxx"
}
```

**Ejemplo con curl:**
```bash
curl -X POST http://localhost:5000/api/whatsapp/send \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "+1234567890",
    "message": "Hola desde Python!"
  }'
```

### Status Callback
```
POST /api/whatsapp/status
```
Twilio notifica el estado de los mensajes (delivered, read, failed, etc).

## Testing Local

### Test sin Twilio (webhook local)
```bash
curl -X POST http://localhost:5000/api/whatsapp/webhook \
  -d "Body=Hola&From=whatsapp:+1234567890"
```

### Test con Python
```python
from model.assistant import generate_response

# Test simple
response = generate_response("¿Cuál es el precio?")
print(response)
```

## Flujo de Funcionamiento

```
Usuario en WhatsApp
        |
        | Envía mensaje
        v
   Servidor Twilio
        |
        | POST a webhook
        v
   /api/whatsapp/webhook
        |
        | Procesa con Gemini
        v
   generate_response()
        |
        | Devuelve TwiML
        v
   Twilio envía respuesta
        |
        v
  Usuario recibe respuesta
```

## Respuestas del Chatbot

El asistente está configurado para responder sobre:

### Dominios Permitidos
- **Catálogo:** Laptops, routers, relojes, audífonos
- **Garantía:** 12 meses hardware, 6 meses accesorios
- **Entregas:** 2-5 días hábiles en Colombia
- **Devoluciones:** 30 días con producto intacto
- **Pago:** Tarjeta, PSE, contraentrega

### Ejemplo de Preguntas

| Pregunta | Respuesta |
|----------|-----------|
| "¿Cuál es el precio?" | Devuelve lista de precios |
| "¿Cuánto tarda la entrega?" | Información de envío |
| "¿Qué es la garantía?" | Detalles de cobertura |
| "¿Cómo pago?" | Formas de pago disponibles |
| "Fuera de soporte" | "Solo puedo ayudarte con NovaGadgets" |

## Producción en Heroku

### 1. Configurar Variables
```bash
heroku config:set TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxx
heroku config:set TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxx
heroku config:set TWILIO_PHONE_NUMBER=whatsapp:+1234567890
heroku config:set GEMINI_API_KEY=xxxxxxxxxxxxxxxx
heroku config:set SECRET_KEY=tu_clave_secreta
```

### 2. Deploy
```bash
git add .
git commit -m "Add WhatsApp integration"
git push heroku main
```

### 3. Actualizar URL en Twilio
Usa tu URL de Heroku: `https://tu-app.herokuapp.com/api/whatsapp/webhook`

## Solución de Problemas

### Error: "Module not found"
```bash
pip install -r requirements.txt
```

### Error: "Invalid credentials"
- Verifica que `.env` tenga credenciales correctas
- Copia exactamente desde Twilio console (sin espacios)

### No recibe mensajes
1. Verifica que el webhook URL es correcto en Twilio
2. Revisa los logs del servidor con:
   ```bash
   python app.py  # Ver logs en console
   ```
3. En Twilio console, ve a **Logs** para ver requests

### Error de encoding (Windows)
Esto está solucionado. Si lo ves aún, ejecuta:
```bash
python validate_setup.py
```

## Estructura de Archivos

```
chabox-master/
├── app.py                    # App Flask principal
├── requirements.txt          # Dependencias
├── .env                      # Variables (CREAR)
├── .env.example              # Template
├── validate_setup.py         # Script de validación
├── routes/
│   ├── __init__.py
│   ├── main.py
│   ├── tramite.py
│   └── whatsapp.py          # NUEVO: Integración WhatsApp
├── model/
│   └── assistant.py          # Lógica de IA
├── config/
│   ├── __init__.py           # NUEVO
│   ├── database.py
│   └── mysqlconnections.py
└── ...
```

## Límites y Consideraciones

### Twilio
- Versión WhatsApp está en **beta** (cambios posibles)
- Créditos de prueba limitados ($5-15 iniciales)
- Rate limit: 1000 mensajes/día (trial)

### Gemini
- Free: 60 requests/minuto
- Cambios a `google-genai` en futuro

### WhatsApp
- Números de Twilio deben verificarse
- Primeros mensajes deben ser plantillas
- No permitir texto abusivo automáticamente

## Ayuda y Recursos

- **Twilio Docs:** https://www.twilio.com/docs/whatsapp
- **Gemini Docs:** https://ai.google.dev
- **Flask Docs:** https://flask.palletsprojects.com
- **Ngrok (Testing Local):** https://ngrok.com

## Licencia

Este proyecto es parte de Chabox.

---

**¿Preguntas?** Revisa el archivo `WHATSAPP_SETUP.md` para más detalles.

**¿Listo?** Ejecuta:
```bash
python validate_setup.py
flask run
```

¡Disfruta de tu auto respuesta en WhatsApp! 📱
