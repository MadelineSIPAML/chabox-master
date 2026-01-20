"""Configuración de la aplicación."""

import os
from dotenv import load_dotenv

load_dotenv()

# Google Gemini API
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
DEFAULT_MODEL_NAME = 'gemini-pro'

# Twilio
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID', '')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN', '')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER', '')

__all__ = [
    'GEMINI_API_KEY',
    'DEFAULT_MODEL_NAME',
    'TWILIO_ACCOUNT_SID',
    'TWILIO_AUTH_TOKEN',
    'TWILIO_PHONE_NUMBER'
]
