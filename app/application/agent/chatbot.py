# app/application/agent/chatbot.py

from app.domain.model.state import State
from app.application.agent.langgraph_flow import build_kai_graph
from app.infrastructure.sql.setupDB import get_formatted_history
from app.infrastructure.factories.gemini_integration import answer_with_gemini
from app.models.context_chunk import ContextChunk

# Inicializamos el flujo de LangGraph (solo una vez)
kai_graph = build_kai_graph()

async def chat_with_bot(user_input: str, session_id: str, name: str, phone:str) -> str:
    """
    Ejecuta el flujo de conversación del bot con el estado inicial.
    """
    initial_state = State(input=user_input, session_id=session_id, name=name, phone=phone) # type: ignore

    print("🧾 Initial state:", initial_state)
    # print("Tipo initial state:", type(initial_state))

    final_state = await kai_graph.ainvoke(initial_state.model_dump())  # type: ignore # ✅ await + ainvoke

    # print("🧾 Final state:", final_state)
    # print("🔍 Tipo:", type(final_state))

    return final_state.get("response") # type: ignore

def generate_chat_summary(session_id: str) -> str:
    """
    Genera un resumen de la conversación para la sesión dada.
    """
    resumen = get_formatted_history(session_id=session_id)

    summary = answer_with_gemini(
        question=f"Genera un resumen no tan detallado de la conversación,lo importante es que indique los puntos clave como cuál fue la problemática y qué decía esta, soluciones, acciones tomadas, conclusiones y puntos a mejorar. Que sea un resumen detallado pero no muy largo y que sea entendible:\n{resumen}",
        chunks=list[ContextChunk]
    )


    return summary or "⚠️ No se encontró historial para esta sesión."
