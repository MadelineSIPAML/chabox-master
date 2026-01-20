from gtts import gTTS
import os

def generar_audio_chileno(texto, nombre_archivo="respuesta.mp3"):
    """
    Genera audio con acento chileno (es-CL) usando Google Text-to-Speech
    
    Args:
        texto: Texto a convertir a audio
        nombre_archivo: Nombre del archivo MP3 a guardar
    
    Returns:
        Ruta del archivo generado
    """
    try:
        # es-CL para acento chileno
        tts = gTTS(text=texto, lang='es', tld='cl', slow=False)
        
        # Guardar en carpeta static
        ruta_audio = os.path.join('static', 'audio', nombre_archivo)
        
        # Crear carpeta si no existe
        os.makedirs(os.path.dirname(ruta_audio), exist_ok=True)
        
        tts.save(ruta_audio)
        
        print(f"✓ Audio chileno generado: {ruta_audio}")
        return ruta_audio
        
    except Exception as e:
        print(f"✗ Error generando audio: {e}")
        return None

generar_audio_chileno("Hola, bienvenido a BarneBT-Plus")
