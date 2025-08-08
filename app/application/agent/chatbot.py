# app/application/agent/chatbot.py

from app.domain.model.state import State
from app.application.agent.langgraph_flow import build_kai_graph
from app.infrastructure.sql.setupDB import get_formatted_history

# Inicializamos el flujo de LangGraph (solo una vez)
kai_graph = build_kai_graph()

async def chat_with_bot(user_input: str, session_id: str, name: str, phone:str) -> str:
    """
    Ejecuta el flujo de conversación del bot con el estado inicial.
    """
    initial_state = State(input=user_input, session_id=session_id, name=name, phone=phone) # type: ignore

    print("🧾 Initial state:", initial_state)
    print("Tipo initial state:", type(initial_state))

    final_state = await kai_graph.ainvoke(initial_state.model_dump())  # type: ignore # ✅ await + ainvoke

    print("🧾 Final state:", final_state)
    print("🔍 Tipo:", type(final_state))

    return final_state.get("response") # type: ignore

def generate_chat_summary(session_id: str) -> str:
    """
    Genera un resumen de la conversación para la sesión dada.
    """
    
    resumen = get_formatted_history(session_id=session_id)
    return resumen or "⚠️ No se encontró historial para esta sesión."
