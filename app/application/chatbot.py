from app.infrastructure.landgGraph_orchestrator import LangraphOrchestrator
from app.infrastructure.qdrant import QdrantService
from app.config.bot_regulations import BotRegulations  # Importa BotRegulations
from app.configEnv import Config 
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configurar servicios de Qdrant
qdrant_url = Config.QDRANT_URL
qdrant_collection_name = Config.QDRANT_COLLECTION_NAME
qdrant_api_key = Config.QDRANT_API_KEY

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
    Función central del chatbot que maneja la conversación y extrae datos con LangGraph.
    """
    # Verificamos si ya tenemos datos del usuario
    if not BotRegulations.user_input.get("name") or not BotRegulations.user_input.get("phone"):
        # Ejecutamos LangGraph con el nodo extract_info
        response = orchestrator.run(user_input)

        # Si LangGraph extrajo info válida, la guardamos
        extracted = orchestrator.info_extractor.extract(user_input)
        if extracted.get("name") and extracted.get("phone"):
            BotRegulations.user_input = {
                "name": extracted["name"],
                "phone": extracted["phone"]
            }
            return f"✅ ¡Gracias, {extracted['name']}! Ahora dime, ¿en qué puedo ayudarte?"

        # Si no extrajo datos, usamos la respuesta de validación
        return response

    # Si ya tenemos los datos del usuario, usamos LangGraph completo
    return orchestrator.run(user_input)


def capture_user_data(user_input: str) -> str | None:
    """
    Intenta capturar el nombre y teléfono del usuario desde el mensaje.
    Si se captura correctamente, los guarda. Si no, no devuelve nada.
    """
    try:
        # Validar formato: "Mi nombre es X y mi numero de telefono es Y"
        lower_msg = user_input.lower()
        if "mi nombre es" in lower_msg and "mi numero de telefono es" in lower_msg:
            parts = user_input.split("y mi numero de telefono es")
            name = parts[0].replace("Mi nombre es", "").strip()
            phone = parts[1].strip()

            BotRegulations.user_input = {
                "name": name,
                "phone": phone
            }

            print("✅ Datos capturados:", BotRegulations.user_input)
            return None  

    except Exception as e:
        print(f"❌ Error capturando datos: {e}")

    return None 

