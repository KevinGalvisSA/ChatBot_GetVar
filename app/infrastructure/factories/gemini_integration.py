import os
import google.generativeai as genai  # type: ignore
from dotenv import load_dotenv
from app.models.context_chunk import ContextChunk
from app.config.bot_regulations import BotRegulations

# Cargar variables de entorno
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configurar Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Instancia del modelo Gemini
model = genai.GenerativeModel("gemini-pro")

def answer_with_gemini(user_input: str, context_chunks: list[ContextChunk]) -> str:
    try:
        # Reglas del bot
        rules = BotRegulations.RULES["intro"]

        # Construir contexto a partir de los chunks
        context = "\n".join([f"- {chunk.content}" for chunk in context_chunks])

        prompt = f"""
{rules}

## CONTEXTO RELACIONADO
{context}

## PREGUNTA DEL USUARIO
{user_input}
        """.strip()

        # Generar respuesta
        response = model.generate_content(prompt)

        # ✅ Manejo seguro del tipo de respuesta
        if isinstance(response, str):
            return response
        elif hasattr(response, "text"):
            return response.text
        else:
            raise Exception(f"Respuesta inesperada de Gemini: {type(response)}")

    except Exception as e:
        return f"❌ Error al usar Gemini: {str(e)}"
