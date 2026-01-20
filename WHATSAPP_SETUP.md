# Integración WhatsApp con Chabox

## Configuración de Twilio

### 1. Crear cuenta en Twilio
- Ve a https://www.twilio.com/console
- Regístrate y verifica tu número de teléfono
- Obtén tu `ACCOUNT_SID` y `AUTH_TOKEN`

### 2. Configurar WhatsApp en Twilio
- En la consola, ve a **Messaging** > **Try it out** > **Send an SMS**
- Selecciona **WhatsApp** (en beta)
- Obtén tu número de teléfono de Twilio en formato `whatsapp:+1234567890`

### 3. Variables de entorno
Copia `.env.example` a `.env` y completa:
```
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxx
TWILIO_PHONE_NUMBER=whatsapp:+1234567890
GEMINI_API_KEY=tu_clave_aqui
```

### 4. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 5. Configurar Webhook en Twilio
- Ve a **Messaging** > **Services** > **Messaging Service**
- En **Inbound Settings**, configura:
  - **Inbound request URL**: `https://tudominio.com/api/whatsapp/webhook`
  - **HTTP method**: `POST`

### 6. Endpoints disponibles

#### Webhook (recibir mensajes)
```
POST /api/whatsapp/webhook
```
Twilio envía automáticamente los mensajes aquí.

#### Enviar mensaje
```bash
curl -X POST http://localhost:5000/api/whatsapp/send \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "+1234567890",
    "message": "Hola desde Python!"
  }'
```

#### Actualizar estado de entrega
```
POST /api/whatsapp/status
```
Twilio notifica el estado de los mensajes aquí.

## Flujo de funcionamiento

1. **Usuario envía mensaje en WhatsApp** → Twilio recibe
2. **Twilio envía POST a `/api/whatsapp/webhook`** 
3. **Tu chatbot procesa con el asistente (Gemini)**
4. **Respuesta automática se envía de vuelta** ✅

## Testing local (sin Twilio)
Para probar sin configurar Twilio, usa:
```bash
curl -X POST http://localhost:5000/api/whatsapp/webhook \
  -d "Body=Hola&From=whatsapp:+1234567890"
```

## Notas importantes
- Twilio tiene créditos de prueba iniciales
- La versión de WhatsApp en Twilio está en beta, puede haber límites
- Para producción en Heroku, configura las variables de entorno en Heroku Config Vars
