from app.configuration import Config
import google.generativeai as genai  # type: ignore
from app.models.context_chunk import ContextChunk
from app.config.bot_regulations import BotRegulations
from dotenv import load_dotenv

load_dotenv()

MY_GEMINI_API_KEY = Config.GEMINI_API_KEY
if not MY_GEMINI_API_KEY:
    raise ValueError("❌ API key de Gemini no configurada en .env")

genai.configure(api_key=MY_GEMINI_API_KEY)  # type: ignore

def answer_with_gemini(question: str, chunks: list[ContextChunk]) -> str:
    try:
        # Los chunks pueden ser dicts o ContextChunk, convertir a texto seguro
        context_texts = []
        for c in chunks:
            # Si es dict con 'text' lo toma, si es ContextChunk también
            if isinstance(c, dict):
                context_texts.append(c.get("text", ""))
            elif hasattr(c, "text"):
                context_texts.append(c.text)
            else:
                context_texts.append(str(c))

        context = "\n".join(context_texts).strip()

        prompt = f"""
{BotRegulations.get_rule("intro")}

### CONTEXTO:
{context if context else 'No hay contexto disponible.'}

### PREGUNTA:
{question}

### RESPONDE CON ENFOQUE EN LA SOLUCIÓN:
Mantén la respuesta centrada en proporcionar soluciones claras y prácticas que ayuden al cliente a automatizar o mejorar su proceso.
        """

        response = genai.GenerativeModel("models/gemini-1.5-pro").generate_content(prompt)  # type: ignore
        return response.text or "❌ Gemini no devolvió contenido"

    except Exception as e:
        return f"❌ Error al usar Gemini: {str(e)}"
