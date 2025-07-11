import os
import google.generativeai as genai  # type: ignore
from app.models.context_chunk import ContextChunk
from app.config.bot_regulations import BotRegulations  # Importamos las reglas
from dotenv import load_dotenv  # Para cargar las variables de entorno

# Cargar variables de entorno
load_dotenv()

# Configuración de la API de Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Verificar si la clave de API está configurada correctamente
if not GEMINI_API_KEY:
    raise Exception("La clave de API de Gemini no está configurada correctamente. Asegúrate de definirla en el archivo .env")

# Imprimir la clave para depuración
print(f"GEMINI_API_KEY: {GEMINI_API_KEY}")  # Para verificar si la clave de API se ha cargado correctamente

# Configuración de la API de Gemini
genai.configure(api_key=GEMINI_API_KEY)  # type: ignore

def answer_with_gemini(question: str, chunks: list[ContextChunk]) -> str:
    """
    Genera una respuesta utilizando Gemini basada en el contexto y la consulta.
    
    Args:
    - question (str): La pregunta o consulta del usuario.
    - chunks (list): Los fragmentos de contexto extraídos de la base de datos.

    Returns:
    - str: La respuesta generada por Gemini.
    """
    try:
        # Crear el contexto a partir de los fragmentos
        context = "\n".join([chunk.text for chunk in chunks])

        # Obtener el reglamento del bot
        bot_intro = BotRegulations.get_rule("intro")  # Se puede modificar para obtener otras reglas

        # Crear el prompt para enviar a Gemini usando f-string para interpolar las variables
        prompt = f"""
        {bot_intro}

        ### CONTEXTO:
        {context}

        ### PREGUNTA:
        {question}

        ### RESPONDE CON ENFOQUE EN LA SOLUCIÓN:
        Mantén la respuesta centrada en proporcionar soluciones claras y prácticas que ayuden al cliente a automatizar o mejorar su proceso, sin desviarte a temas irrelevantes. Usa un lenguaje sencillo y directo. 
        """

        # Llamar a la API de Gemini para generar la respuesta
        response = genai.GenerativeModel("models/gemini-1.5-pro").generate_content(prompt)  # type: ignore
        
        # Si la respuesta no tiene texto, lanzamos un error
        if not response or not response.text:
            raise Exception("Gemini no respondió correctamente.")
        
        return response.text
    
    except Exception as e:
        return f"❌ Error al usar Gemini: {str(e)}"
