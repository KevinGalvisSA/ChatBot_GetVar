from app.infrastructure.langraph_orchestator import LangraphOrchestrator
from app.infrastructure.qdrant import QdrantService
from app.infrastructure.gemini_integration import answer_with_gemini
from app.models.context_chunk import ContextChunk
from app.config.bot_regulations import BotRegulations  # Importa BotRegulations
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configurar servicios de Qdrant
qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6333")
qdrant_collection_name = os.getenv("QDRANT_COLLECTION_NAME", "asesorias")
qdrant_api_key = os.getenv("QDRANT_API_KEY", "")

if not qdrant_url or not qdrant_collection_name or not qdrant_api_key:
    raise ValueError("Faltan variables de entorno. Asegúrate de definir QDRANT_URL, QDRANT_COLLECTION_NAME y QDRANT_API_KEY en el archivo .env")

# Crear el servicio de Qdrant
qdrant_service = QdrantService(
    url=qdrant_url,
    collection_name=qdrant_collection_name,
    api_key=qdrant_api_key
)

# Crear el orquestador de Langraph
orchestrator = LangraphOrchestrator(
    qdrant_url=qdrant_url,
    qdrant_collection_name=qdrant_collection_name,
    qdrant_api_key=qdrant_api_key
)

def chat_with_bot(user_input: str) -> str:
    """
    Maneja la consulta del usuario, solicita el nombre y teléfono si es necesario,
    guarda esos datos, y luego genera la respuesta del chatbot con Gemini.
    
    Args:
    - user_input (str): El mensaje o consulta del usuario.
    
    Returns:
    - str: Respuesta generada por el chatbot.
    """
    try:
        # Comprobar si el nombre y teléfono ya han sido guardados
        if not BotRegulations.user_input.get("name") or not BotRegulations.user_input.get("phone"):
            # Si no están guardados, solicitar al usuario
            return "¡Hola! Un placer en conocerte, ¿podrías indicarme por favor tu nombre y número de teléfono? Estos datos son importantes para poder ofrecerte mejor asistencia."

        # Si ya se tiene la información, procesar la consulta
        print(f"🔍 Procesando mensaje: {user_input}")

        # Realizar la búsqueda explícita en Qdrant usando el servicio
        search_results = qdrant_service.search(user_input)
        
        if not search_results:
            return "Lo siento, no pude encontrar información relevante para tu consulta."

        # Usar el orquestador para procesar la entrada del usuario y combinar la búsqueda
        context_chunks = [ContextChunk(text=result, score=0.9) for result in search_results]  # type: ignore
        response = answer_with_gemini(user_input, context_chunks)
        
        return response
    except Exception as e:
        return f"❌ Ocurrió un error al procesar tu consulta: {str(e)}"

def capture_user_data(user_input: str) -> str:
    """
    Función para capturar el nombre y el teléfono del usuario.
    
    Args:
    - user_input (str): El mensaje que contiene el nombre y teléfono.
    
    Returns:
    - str: Respuesta para confirmar la captura de los datos.
    """
    # Suponemos que el usuario proporciona el nombre y teléfono de esta manera: "Mi nombre es Juan y mi número de teléfono es 123456789"
    if "mi nombre es" in user_input.lower() and "mi numero de telefono es" in user_input.lower():
        try:
            # Extraemos el nombre y teléfono usando expresiones regulares o dividiendo el texto
            parts = user_input.split("y mi numero de telefono es")
            name = parts[0].replace("Mi nombre es", "").strip()
            phone = parts[1].strip()

            # Guardar los datos en la variable interna user_input
            BotRegulations.user_input = {
                "name": name,
                "phone": phone
            }

            return f"Muchas gracias por la información, {name}! Ahora, cuéntame, ¿en qué puedo ayudarte?"

        except Exception as e:
            return "Lo siento, no pude entender la información. Por favor, intenta de nuevo con tu nombre y número de teléfono."

    return "Para poder ofrecerte una mejor asistencia, ¿podrías indicarme tu nombre y número de teléfono?"
