# Deployment a Heroku - Chabox WhatsApp

Guía para desplegar tu aplicación en Heroku.

## Requisitos

- Cuenta en Heroku (https://heroku.com)
- Git instalado
- Heroku CLI instalado (https://devcenter.heroku.com/articles/heroku-cli)

## Pasos de Deployment

### 1. Preparar la aplicación

Asegúrate de que tengas estos archivos en el root del proyecto:

```
Procfile              # Define cómo ejecutar la app
runtime.txt           # Versión de Python
requirements.txt      # Dependencias (ya existe)
.gitignore            # Archivos a ignorar
```

#### Crear Procfile

```bash
echo "web: gunicorn app:app" > Procfile
```

#### Crear runtime.txt

```bash
echo "python-3.11.5" > runtime.txt
```

#### Verificar .gitignore

```bash
cat > .gitignore << 'EOF'
.env
*.pyc
__pycache__/
.venv/
venv/
.DS_Store
*.db
EOF
```

### 2. Configurar Git

```bash
# Inicializar git (si no está inicializado)
git init

# Agregar archivos
git add .

# Commit inicial
git commit -m "Add WhatsApp integration"
```

### 3. Crear y configurar app en Heroku

```bash
# Loguеarse en Heroku
heroku login

# Crear nueva app
heroku create nombre-de-tu-app

# O si ya existe:
# heroku git:remote -a nombre-de-tu-app
```

### 4. Configurar variables de entorno en Heroku

```bash
# Asegúrate de que .env NO esté en git
echo ".env" >> .gitignore

# Configurar variables en Heroku
heroku config:set TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxx
heroku config:set TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxx
heroku config:set TWILIO_PHONE_NUMBER=whatsapp:+1234567890
heroku config:set GEMINI_API_KEY=xxxxxxxxxxxxxxxx
heroku config:set SECRET_KEY=tu_clave_secreta_aqui
heroku config:set FLASK_ENV=production
```

Verificar:
```bash
heroku config
```

### 5. Desplegar

```bash
# Push a Heroku
git push heroku main
# o si usas master:
# git push heroku master
```

Ver logs:
```bash
heroku logs --tail
```

### 6. Abrir la app

```bash
heroku open
```

O visita: `https://nombre-de-tu-app.herokuapp.com`

## Configurar Webhook en Twilio

Una vez que tu app esté en Heroku:

1. Ve a Twilio Console
2. Messaging > Services > Tu servicio
3. Inbound Settings
4. **Request URL:** `https://nombre-de-tu-app.herokuapp.com/api/whatsapp/webhook`
5. HTTP Method: `POST`
6. Click **Save**

### Status Callback (opcional)

Para rastrear entregas:
- **Status Callback URL:** `https://nombre-de-tu-app.herokuapp.com/api/whatsapp/status`

## Verificar Deployment

```bash
# Test del webhook
curl -X POST https://nombre-de-tu-app.herokuapp.com/api/whatsapp/webhook \
  -d "Body=Hola&From=whatsapp:+1234567890"

# Ver logs
heroku logs --tail

# Test del endpoint de envío
curl -X POST https://nombre-de-tu-app.herokuapp.com/api/whatsapp/send \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "+1234567890",
    "message": "Mensaje de prueba desde Heroku!"
  }'
```

## Problemas Comunes

### Error: "No web processes running"

```bash
heroku ps:scale web=1
```

### Error: "ImportError: No module named..."

Asegúrate de que `requirements.txt` esté actualizado:
```bash
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update requirements"
git push heroku main
```

### Error: "Application error"

Ver logs detallados:
```bash
heroku logs --tail -n 50
```

### Webhook no recibe mensajes

1. Verifica la URL en Twilio console (sin trailing slash)
2. Revisa logs: `heroku logs --tail`
3. Prueba manualmente con curl

## Mantenimiento

### Actualizar código

```bash
# Hacer cambios localmente
git add .
git commit -m "Descripción de cambios"

# Desplegar
git push heroku main
```

### Ver estado de la app

```bash
heroku ps
```

### Reiniciar app

```bash
heroku restart
```

### Acceder a bash en Heroku

```bash
heroku run bash
```

## Monitoreo

### Ver logs en tiempo real

```bash
heroku logs --tail
```

### Configurar alertas

En el dashboard de Heroku, ve a Settings > Add-ons para agregar monitoreo.

## Escalar (si necesario)

```bash
# Aumentar dyno a Standard (costo)
heroku dyos:type Standard-1x web

# O mantener Free (default)
heroku dyos:type free web
```

## Backup y Datos

Si usas MySQL:

```bash
# Backup manual
heroku pg:backups:capture

# Descargar
heroku pg:backups:download

# Ver backups
heroku pg:backups
```

## Eliminar app

```bash
heroku apps:destroy --app nombre-de-tu-app --confirm nombre-de-tu-app
```

## Variables de Entorno Importantes

Asegúrate de configurar todas estas:

| Variable | Descripción |
|----------|-------------|
| `TWILIO_ACCOUNT_SID` | SID de tu cuenta Twilio |
| `TWILIO_AUTH_TOKEN` | Token de autenticación |
| `TWILIO_PHONE_NUMBER` | Número WhatsApp de Twilio |
| `GEMINI_API_KEY` | API key de Google Gemini |
| `SECRET_KEY` | Clave secreta de Flask |
| `FLASK_ENV` | production |

## Próximos Pasos

1. Desplegar a Heroku ✓
2. Configurar webhook en Twilio ✓
3. Probar enviando mensaje WhatsApp
4. Monitorear logs
5. Escalar si necesario (después)

## Ayuda

- Heroku Docs: https://devcenter.heroku.com
- Twilio Docs: https://www.twilio.com/docs/whatsapp
- Python en Heroku: https://devcenter.heroku.com/articles/python-support

---

¿Problemas? Revisa los logs:
```bash
heroku logs --tail
```

¡Listo para producción!
