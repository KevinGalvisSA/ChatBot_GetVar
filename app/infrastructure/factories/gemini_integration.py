from app.configuration import Config
import google.generativeai as genai  # type: ignore
from app.models.context_chunk import ContextChunk
from app.config.bot_regulations import BotRegulations
from dotenv import load_dotenv

load_dotenv()

# Configuración de la API de Gemini
MY_GEMINI_API_KEY = Config.GEMINI_API_KEY
if not MY_GEMINI_API_KEY:
    raise ValueError("❌ API key de Gemini no configurada en .env")

genai.configure(api_key=MY_GEMINI_API_KEY)  # type: ignore

def answer_with_gemini(question: str, chunks: list[ContextChunk]) -> str:
    try:
        context = "\n".join([chunk.text for chunk in chunks])
        prompt = f"""
{BotRegulations.get_rule("intro")}

### CONTEXTO:
{context}

### PREGUNTA:
{question}

### RESPONDE CON ENFOQUE EN LA SOLUCIÓN:
Mantén la respuesta centrada en proporcionar soluciones claras y prácticas que ayuden al cliente a automatizar o mejorar su proceso.
        """

        response = genai.GenerativeModel("models/gemini-1.5-pro").generate_content(prompt)  # type: ignore
        return response.text or "❌ Gemini no devolvió contenido"

    except Exception as e:
        return f"❌ Error al usar Gemini: {str(e)}"
