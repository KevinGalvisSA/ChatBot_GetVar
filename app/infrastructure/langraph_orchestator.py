from langgraph.graph import StateGraph
from app.config.bot_regulations import BotRegulations  # Asegúrate de importar las reglas
from app.infrastructure.qdrant import QdrantService
from app.infrastructure.extract_info import InfoExtractor
from typing import Dict, Optional
from typing_extensions import TypedDict

class State(TypedDict):
    """
    Define la estructura del estado que se pasará entre los nodos.
    """
    question: str
    search_results: Optional[list[str]]  # Resultados de búsqueda de Qdrant
    response: Optional[str]  # Respuesta final que generará el bot
    extracted_info: Optional[dict]  # Información extraída del texto (por ejemplo, nombre, teléfono)
    validation_message: Optional[str]  # Mensaje de validación de la información extraída

class LangraphOrchestrator:
    def __init__(self, qdrant_url: str, qdrant_collection_name: str, qdrant_api_key: str):
        """
        Inicializa el orquestador Langgraph con el servicio de búsqueda en Qdrant y el extractor de información.
        
        Args:
        - qdrant_url (str): URL de Qdrant.
        - qdrant_collection_name (str): Nombre de la colección en Qdrant.
        - qdrant_api_key (str): La clave de API de Qdrant para autenticarse.
        """
        self.qdrant_service = QdrantService(
            url=qdrant_url,
            collection_name=qdrant_collection_name,
            api_key=qdrant_api_key
        )
        self.info_extractor = InfoExtractor()

        # Crear el grafo de estados
        self.graph_builder = StateGraph(State)
        self.graph_builder.add_node("search_node", self.search_node)
        self.graph_builder.add_node("response_node", self.response_node)
        self.graph_builder.add_node("extract_info_node", self.extract_info_node)

        # Añadir las conexiones entre nodos
        self.graph_builder.add_edge("search_node", "response_node")
        self.graph_builder.add_edge("response_node", "extract_info_node")

        # Establecer el punto de entrada y salida del grafo
        self.graph_builder.set_entry_point("search_node")
        self.graph_builder.set_finish_point("extract_info_node")

        # Compilar el grafo
        self.graph = self.graph_builder.compile()

    def run(self, message: str, context: Optional[Dict[str, str]] = None) -> str:
        """
        Ejecuta el flujo de trabajo de Langgraph basado en la entrada del usuario.
        
        Args:
        - user_input (str): Entrada del usuario.
        - context (dict, opcional): Información adicional que puede pasar entre nodos.
        
        Returns:
        - str: Respuesta generada para el usuario.
        """
        if context is None:
            context = {}

        # Crear el estado inicial con los datos proporcionados
        state = State(question=message, search_results=[], response="", extracted_info={}, validation_message="")

        print(f"📝 Estado inicial: {state}")

        try:
            # Ejecutar los nodos manualmente
            state = self.extract_info_node(state)
            print(f"📝 Después de extract_info_node: {state}")
            state = self.search_node(state)
            print(f"📝 Después de search_node: {state}")
            state = self.response_node(state)
            print(f"📝 Después de response_node: {state}")
        except Exception as e:
            return f"❌ Error en el flujo del chatbot: {str(e)}"

        # Verificación adicional antes de retornar la respuesta
        if not state.get("response"):
            return "❌ No se pudo generar una respuesta válida."
        
        return state['response'] # type: ignore

    def search_node(self, state: State) -> State:
        print(f"🌐 Ejecutando search_node con estado: {state}")
        search_results = self.qdrant_service.search(state['question'])
        state['search_results'] = search_results
        state['response'] = "Aquí están los resultados de tu búsqueda:"
        return state

    def response_node(self, state: State) -> State:
        print(f"📜 Ejecutando response_node con estado: {state}")
        if 'search_results' in state:
            search_results = state['search_results']
            state['response'] = "\n".join(search_results)  # type: ignore
        else:
            state['response'] = "No pude encontrar información relacionada con tu consulta."
        
        return state

    def extract_info_node(self, state: State) -> State:
        print(f"📝 Ejecutando extract_info_node con estado: {state}")
        extracted_info = self.info_extractor.extract(state['question'])
        validation_message = self.info_extractor.validate_extracted_info(extracted_info)
        state['extracted_info'] = extracted_info
        state['validation_message'] = validation_message
        state['response'] = validation_message
        return state
