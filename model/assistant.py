"""Logica del asistente conversacional.

Responsabilidades:
- Definir el prompt de sistema que acota el dominio del chatbot.
- Convertir el historial local en el formato esperado por el SDK.
- Gestionar la llamada al proveedor generativo (Gemini) y un modo local de respaldo.
- Modo demo: simula respuestas para testing sin API key.
"""

from __future__ import annotations

import logging
import random
from typing import Any, Dict, List, Optional

import google.generativeai as genai

from config import DEFAULT_MODEL_NAME, GEMINI_API_KEY


logger = logging.getLogger(__name__)


# Modo DEMO: respuestas simuladas para testing sin API key
DEMO_RESPONSES = {
    "precio": "Nuestros productos tienen precios muy competitivos:\n• Nova Air Laptop: $899,000\n• Router Wave WiFi 6: $189,000\n• Reloj Pulse Pro: $299,000\n• AeroPods: $129,000\n\n¿Te interesa alguno en particular?",
    "garantia": "✓ Garantía Hardware: 12 meses\n✓ Garantía Accesorios: 6 meses\n✓ Cobertura: defectos de fabricación\n\nPuedes reclamar presentando tu recibo en nuestro correo: soporte@novagadgets.co",
    "envio": "📦 Envíos en Colombia:\n• Ciudades principales: 2-5 días hábiles\n• Zonas remotas: hasta 7 días hábiles\n• Costo: varía según destino\n\n¿A qué ciudad necesitas envío?",
    "devolucion": "↩️ Política de devoluciones:\n✓ Plazo: 30 días desde la compra\n✓ Condición: producto intacto y embalaje original\n✓ Proceso: contacta a soporte@novagadgets.co\n\n¿Hay algún problema con tu pedido?",
    "pago": "💳 Formas de pago disponibles:\n• Tarjeta de crédito/débito\n• PSE (transferencia bancaria)\n• Contraentrega (en principales ciudades)\n\n¿Cuál prefieres?",
}

# Prompt de sistema: controla el dominio, tono y politica de rechazo.
SYSTEM_PROMPT = """
Eres NovaDesk, el chatbot oficial de soporte y ventas de la tienda ficticia NovaGadgets.

Dominios permitidos (responde solo con esto):
- Catalogo: laptops Nova Air, router Wave WiFi 6, reloj Pulse Pro, audifonos AeroPods, kits IoT para hogar seguro.
- Politicas: garantias (12 meses hardware, 6 meses accesorios), devoluciones en 30 dias si el producto esta intacto, entregas en Colombia en 2 a 5 dias habiles, zonas remotas pueden tardar hasta 7 dias.
- Procesos: activacion inicial, configuracion WiFi, actualizacion de firmware, reinicio seguro, pasos basicos de diagnostico, formas de pago (tarjeta, PSE, contraentrega en principales ciudades), seguimiento de pedidos con numero de guia.
- Canales humanos: soporte@novagadgets.co, linea 01-8000-123-456, horario lunes a viernes 8:00-18:00 y sabados 9:00-14:00.

Reglas de seguridad y limites:
- Si te piden algo fuera de soporte y ventas de NovaGadgets, responde solo con: "Solo puedo ayudarte con informacion de soporte y ventas de NovaGadgets."
- No inventes datos ni promociones no listadas. Si falta informacion, indica que debes escalar a un agente humano.
- No pidas datos sensibles (tarjetas completas, claves, documentos).
- Usa tono claro, conciso y profesional en espanol neutral. Ofrece pasos accionables y breves.
- Prefiere listas numeradas o bullet points cuando des procedimientos.
"""


def get_demo_response(user_message: str) -> str:
    """Retorna una respuesta simulada basada en keywords (modo demo)."""
    message_lower = user_message.lower()
    
    # Buscar palabras clave
    keywords_map = {
        "precio": DEMO_RESPONSES["precio"],
        "costo": DEMO_RESPONSES["precio"],
        "cuanto cuesta": DEMO_RESPONSES["precio"],
        "garantia": DEMO_RESPONSES["garantia"],
        "envio": DEMO_RESPONSES["envio"],
        "entrega": DEMO_RESPONSES["envio"],
        "devolucion": DEMO_RESPONSES["devolucion"],
        "cambio": DEMO_RESPONSES["devolucion"],
        "pago": DEMO_RESPONSES["pago"],
        "pagar": DEMO_RESPONSES["pago"],
    }
    
    for keyword, response in keywords_map.items():
        if keyword in message_lower:
            return response
    
    # Respuesta por defecto amigable
    default_responses = [
        "Puedo ayudarte con:\n• 💰 Precios de productos\n• 🚚 Información de envío\n• 📋 Políticas de garantía\n• 💳 Formas de pago\n• ↩️ Devoluciones\n\n¿En qué puedo asistirte?",
        "¿Tienes preguntas sobre nuestros productos NovaGadgets? Pregúntame sobre precios, envíos, garantía o políticas. ¡Estoy para ayudarte!",
        "No entendí bien tu pregunta. Intenta preguntar sobre:\n• Productos disponibles\n• Políticas de garantía\n• Envíos y entregas\n• Formas de pago\n\n¿Qué necesitas?",
    ]
    return random.choice(default_responses)


def build_messages(
    user_message: str,
    history: Optional[List[Dict[str, Any]]] = None,
) -> List[Dict[str, Any]]:
    """Convierte historial y mensaje actual al formato requerido por el SDK."""

    messages: List[Dict[str, Any]] = []
    for msg in history or []:
        role = "user" if msg.get("sender") == "Usuario" else "model"
        messages.append({"role": role, "parts": [msg.get("text", "")]})

    # Evita duplicar el ultimo mensaje si ya esta en el historial.
    if not history or history[-1].get("sender") != "Usuario" or history[-1].get("text") != user_message:
        messages.append({"role": "user", "parts": [user_message]})
    return messages


def _local_fallback(user_message: str) -> str:
    """Respuesta determinista cuando no hay clave o el modelo falla."""

    lower = user_message.lower()

    rules = [
        (["horario", "cuando atienden"], "Atendemos lunes a viernes 8:00-18:00 y sabados 9:00-14:00. Tambien puedes escribir a soporte@novagadgets.co."),
        (["garantia", "garant"], "La garantia es de 12 meses para hardware y 6 meses para accesorios. Guarda la factura y el numero de serie para tramites."),
        (["devolu", "cambio", "reembolso"], "Puedes solicitar devolucion dentro de 30 dias si el producto esta intacto. Gestionamos un numero RMA y coordinamos la recoleccion."),
        (["envio", "entrega", "transporte"], "Enviamos en Colombia en 2 a 5 dias habiles; zonas remotas pueden tardar hasta 7 dias. Compartimos numero de guia para seguimiento."),
        (["configurar", "instalar", "activar"], "Sigue estos pasos rapidos: 1) Carga el dispositivo o conectalo a energia. 2) Descarga la app NovaGadgets. 3) Conecta a tu red WiFi de 2.4 o 5 GHz. 4) Actualiza firmware si la app lo sugiere."),
        (["contacto", "humano", "asesor"], "Puedes hablar con un agente al 01-8000-123-456 o escribir a soporte@novagadgets.co. Describe el modelo y el problema."),
    ]

    for keywords, response in rules:
        if any(k in lower for k in keywords):
            return response

    return "Solo puedo ayudarte con informacion de soporte y ventas de NovaGadgets. Si necesitas algo mas especifico, dime el modelo y el problema."


def generate_response(
    user_message: str,
    history: Optional[List[Dict[str, Any]]] = None,
    api_key: Optional[str] = None,
    model_name: Optional[str] = None,
) -> str:
    """Genera la respuesta del asistente."""

    key = api_key or GEMINI_API_KEY
    messages = build_messages(user_message, history or [])

    if not key or key == "your_gemini_api_key_here":
        # Modo DEMO: usar respuestas simuladas
        logger.info("Usando modo DEMO (API key no configurada)")
        return get_demo_response(user_message)

    try:
        genai.configure(api_key=key)

        model = genai.GenerativeModel(
            model_name=model_name or DEFAULT_MODEL_NAME,
            system_instruction=SYSTEM_PROMPT,
        )

        response = model.generate_content(
            contents=messages,
            safety_settings=[
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_NONE",
                },
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_NONE",
                },
            ],
            generation_config={
                "temperature": 0.6,
                "top_p": 0.9,
                "candidate_count": 1,
                "max_output_tokens": 256,
            },
        )

        text = getattr(response, "text", None) or str(response)
        cleaned = text.strip()
        return cleaned or _local_fallback(user_message)

    except Exception:
        logger.exception("Error generando respuesta con el proveedor remoto")
        return _local_fallback(user_message)
