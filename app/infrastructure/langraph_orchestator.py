from langgraph.graph import StateGraph
from app.infrastructure.qdrant import QdrantService
from app.infrastructure.extract_info import InfoExtractor
from typing import Dict, Optional
from typing_extensions import TypedDict
from app.infrastructure.gemini_integration import answer_with_gemini
from app.models.context_chunk import ContextChunk
from app.config.bot_regulations import BotRegulations

class State(TypedDict):
    """
    Define la estructura del estado que se pasará entre los nodos.
    """
    question: str
    search_results: Optional[list[str]]  # Resultados de búsqueda de Qdrant
    response: Optional[str]              # Respuesta final del bot
    extracted_info: Optional[dict]       # Info extraída del usuario (nombre, teléfono)
    validation_message: Optional[str]    # Mensaje si falta info importante

class LangraphOrchestrator:
    def __init__(self, qdrant_url: str, qdrant_collection_name: str, qdrant_api_key: str):
        self.qdrant_service = QdrantService(
            url=qdrant_url,
            collection_name=qdrant_collection_name,
            api_key=qdrant_api_key
        )
        self.info_extractor = InfoExtractor()

        # Construir el grafo de estados
        self.graph_builder = StateGraph(State)
        self.graph_builder.add_node("extract_info_node", self.extract_info_node)
        self.graph_builder.add_node("search_node", self.search_node)
        self.graph_builder.add_node("response_node", self.response_node)

        self.graph_builder.add_edge("extract_info_node", "search_node")
        self.graph_builder.add_edge("search_node", "response_node")

        self.graph_builder.set_entry_point("extract_info_node")
        self.graph_builder.set_finish_point("response_node")

        self.graph = self.graph_builder.compile()

    def run(self, message: str) -> str:
        """
        Ejecuta el flujo LangGraph completo para una consulta del usuario.
        """
        initial_state = State(
            question=message,
            search_results=[],
            response="",
            extracted_info={},
            validation_message=""
        )

        try:
            final_state = self.graph.invoke(initial_state)
            return final_state.get("response", "❌ No se pudo generar una respuesta válida.")
        except Exception as e:
            return f"❌ Error en el flujo del chatbot: {str(e)}"

    def extract_info_node(self, state: State) -> State:
        print(f"📝 Ejecutando extract_info_node con estado: {state}")
        extracted_info = self.info_extractor.extract(state["question"])
        validation_message = self.info_extractor.validate_extracted_info(extracted_info)

        state["extracted_info"] = extracted_info
        state["validation_message"] = validation_message

        # Si falta información importante, no continuar aún con búsqueda/respuesta
        if not extracted_info.get("name") or not extracted_info.get("phone"):
            state["response"] = validation_message
            return state

        return state

    def search_node(self, state: State) -> State:
        print(f"🌐 Ejecutando search_node con estado: {state}")
        search_results = self.qdrant_service.search(state["question"])
        state["search_results"] = search_results
        return state

    def response_node(self, state: State) -> State:
        print(f"📜 Ejecutando response_node con estado: {state}")
        search_results = state.get("search_results", [])

        if not search_results:
            state["response"] = "Lo siento, no encontré información relevante para tu consulta."
            return state

        context_chunks = [ContextChunk(text=chunk, score=0.9) for chunk in search_results]
        response = answer_with_gemini(
            question=state["question"],
            chunks=context_chunks
        )

        state["response"] = response
        return state
