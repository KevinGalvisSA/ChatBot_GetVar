import os
from dotenv import load_dotenv

# Cargar las variables del archivo .env
load_dotenv()

class Config:
    """Clase para manejar la configuración del sistema."""

    # Configuración de Qdrant
    QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
    QDRANT_COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "knowledge_base")
    
    # Clave de API de Qdrant
    QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", "")

    # Configuración de Gemini (si es necesario)
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

    @staticmethod
    def print_config():
        """Imprimir las configuraciones actuales para depuración."""
        print(f"QDRANT_URL: {Config.QDRANT_URL}")
        print(f"QDRANT_COLLECTION_NAME: {Config.QDRANT_COLLECTION_NAME}")
        print(f"QDRANT_API_KEY: {Config.QDRANT_API_KEY}")
        print(f"GEMINI_API_KEY: {Config.GEMINI_API_KEY}")
