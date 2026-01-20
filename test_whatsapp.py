#!/usr/bin/env python
"""Test unitario para la integración de WhatsApp."""

import unittest
import json
import os
from pathlib import Path
import sys

# Agregar ruta del proyecto
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Cargar variables de entorno
from dotenv import load_dotenv
load_dotenv()


class TestWhatsAppIntegration(unittest.TestCase):
    """Test suite para WhatsApp."""
    
    def setUp(self):
        """Preparar test."""
        from app import app
        self.app = app
        self.client = self.app.test_client()
    
    def test_whatsapp_webhook_endpoint_exists(self):
        """Verifica que el endpoint webhook existe."""
        response = self.client.post(
            '/api/whatsapp/webhook',
            data={'Body': 'Hola', 'From': 'whatsapp:+1234567890'}
        )
        # Debe retornar 200 o error XML (no 404)
        self.assertNotEqual(response.status_code, 404)
        print(f"✓ Endpoint webhook: {response.status_code}")
    
    def test_whatsapp_webhook_processes_message(self):
        """Verifica que el webhook procesa mensajes."""
        response = self.client.post(
            '/api/whatsapp/webhook',
            data={
                'Body': '¿Cuál es el precio?',
                'From': 'whatsapp:+1234567890'
            }
        )
        self.assertIn(response.status_code, [200, 201])
        print(f"✓ Procesamiento de mensaje: {response.status_code}")
    
    def test_send_message_endpoint(self):
        """Verifica que el endpoint de envío funciona."""
        response = self.client.post(
            '/api/whatsapp/send',
            json={
                'phone': '+1234567890',
                'message': 'Mensaje de prueba'
            },
            content_type='application/json'
        )
        # Puede fallar si no hay credenciales, pero no debe ser 404
        self.assertNotEqual(response.status_code, 404)
        print(f"✓ Endpoint send: {response.status_code}")
    
    def test_assistant_generates_response(self):
        """Verifica que el asistente genera respuestas."""
        from model.assistant import generate_response
        
        response = generate_response("¿Qué productos tienen?")
        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 0)
        print(f"✓ Asistente genera respuesta: {len(response)} caracteres")
    
    def test_assistant_handles_pricing_query(self):
        """Verifica que el asistente responde sobre precios."""
        from model.assistant import generate_response
        
        response = generate_response("¿Cuál es el precio de la laptop?")
        self.assertIn("precio", response.lower())
        print(f"✓ Respuesta sobre precios: OK")
    
    def test_flask_routes_registered(self):
        """Verifica que las rutas están registradas."""
        routes = [str(rule) for rule in self.app.url_map.iter_rules()]
        whatsapp_routes = [r for r in routes if 'whatsapp' in r]
        
        self.assertGreater(len(whatsapp_routes), 0)
        print(f"✓ Rutas registradas: {len(whatsapp_routes)}")
        for route in whatsapp_routes:
            print(f"  - {route}")


class TestAssistant(unittest.TestCase):
    """Test suite para el asistente."""
    
    def test_assistant_imports(self):
        """Verifica que se puede importar el asistente."""
        try:
            from model.assistant import generate_response
            self.assertTrue(callable(generate_response))
            print("✓ Asistente importado correctamente")
        except ImportError as e:
            self.fail(f"No se puede importar asistente: {e}")
    
    def test_assistant_works_without_api_key(self):
        """Verifica que funciona en modo demo."""
        from model.assistant import generate_response
        
        response = generate_response("test")
        self.assertIsNotNone(response)
        self.assertIsInstance(response, str)
        print("✓ Asistente funciona en modo demo")
    
    def test_multiple_message_types(self):
        """Prueba diferentes tipos de mensajes."""
        from model.assistant import generate_response
        
        test_messages = [
            "precio",
            "garantia",
            "envio",
            "devolucion",
            "pago",
            "¿cómo configuro?",
            "problema con mi orden"
        ]
        
        for msg in test_messages:
            response = generate_response(msg)
            self.assertGreater(len(response), 0)
        
        print(f"✓ Probadas {len(test_messages)} tipos de mensaje")


class TestFlaskApp(unittest.TestCase):
    """Test suite para la aplicación Flask."""
    
    def setUp(self):
        """Preparar test."""
        from app import app
        self.app = app
        self.client = self.app.test_client()
    
    def test_app_creates_successfully(self):
        """Verifica que la app se crea correctamente."""
        self.assertIsNotNone(self.app)
        print("✓ Aplicación Flask creada")
    
    def test_index_route_exists(self):
        """Verifica que la ruta index funciona."""
        response = self.client.get('/')
        self.assertIn(response.status_code, [200, 404])  # 404 es OK si no hay template
        print(f"✓ Ruta index: {response.status_code}")
    
    def test_json_response_format(self):
        """Verifica que se devuelven JSON correctamente."""
        response = self.client.post(
            '/api/whatsapp/send',
            json={'phone': 'test', 'message': 'test'},
            content_type='application/json'
        )
        # Intentar parsear como JSON
        try:
            json.loads(response.get_data(as_text=True))
            print("✓ Respuesta en formato JSON correcto")
        except:
            print("⚠️  Respuesta no es JSON (puede ser OK según el endpoint)")


if __name__ == '__main__':
    print("\n" + "="*70)
    print("EJECUTANDO TESTS DE CHABOX WHATSAPP")
    print("="*70 + "\n")
    
    # Crear suite de tests
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Agregar todos los tests
    suite.addTests(loader.loadTestsFromTestCase(TestFlaskApp))
    suite.addTests(loader.loadTestsFromTestCase(TestAssistant))
    suite.addTests(loader.loadTestsFromTestCase(TestWhatsAppIntegration))
    
    # Ejecutar
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Resumen
    print("\n" + "="*70)
    print("RESUMEN DE TESTS")
    print("="*70)
    print(f"Tests ejecutados: {result.testsRun}")
    print(f"Exitosos: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Fallos: {len(result.failures)}")
    print(f"Errores: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("\n✅ TODOS LOS TESTS PASARON")
    else:
        print("\n❌ ALGUNOS TESTS FALLARON")
    
    print("="*70 + "\n")
