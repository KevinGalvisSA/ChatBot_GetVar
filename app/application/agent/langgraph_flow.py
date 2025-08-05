# app/application/agent/langgraph_flow.py

from langgraph.graph import StateGraph, END
from app.domain.model.state import State

from app.application.tools.tool_extractor import extract_user_info_tool
from app.application.tools.tool_save_user import save_user_tool
from app.application.tools.tool_qdrant import retrieve_context_tool
from app.application.tools.tool_prompt import build_prompt_tool
from app.application.tools.tool_gemini import call_gemini_tool
from app.application.tools.tool_check_sent import check_already_sent_tool
from app.application.tools.tool_check_AB import check_AB_tool

from typing import Callable, Any


# 🔧 Wrapper para hacer trazables los nodos
def wrap_tool(tool_func: Callable[[State], dict], name: str) -> Callable[[Any], dict]:
    def wrapped(state: State) -> dict:
        print(f"\n🚀 Ejecutando nodo: {name}")
        print(f"📥 State recibido por {name}: {state}")
        result = tool_func(state)
        print(f"✅ Resultado nodo {name}: {result}")
        if not isinstance(result, dict):
            raise TypeError(f"❌ Nodo {name} devolvió {type(result)} en vez de dict")
        return result
    return wrapped



def build_kai_graph():
    print("🧠 Entrando a build_kai_graph()")

    graph = StateGraph(State)

    print("🔧 Añadiendo nodos...")
    print("Holas graph:", graph)
    print("Muerte Judia:", extract_user_info_tool)

    graph.add_node("extract_info", wrap_tool(extract_user_info_tool, "extract_info"))
    graph.add_node("save_user", wrap_tool(save_user_tool, "save_user"))
    graph.add_node("retrieve_context", wrap_tool(retrieve_context_tool, "retrieve_context"))
    graph.add_node("build_prompt", wrap_tool(build_prompt_tool, "build_prompt"))
    graph.add_node("check_sent", wrap_tool(check_already_sent_tool, "check_sent"))
    graph.add_node("call_gemini", wrap_tool(call_gemini_tool, "call_gemini"))
    graph.add_node("check_AB", wrap_tool(check_AB_tool, "check_AB"))

    # 🔚 Nodo final con print de cierre
    graph.add_node("end", lambda state: (
        print("🏁 Nodo final alcanzado"),
        state.model_dump()
    )[1])  # 👈 truco para ejecutar print y devolver dict

    print("🔗 Definiendo flujo de ejecución...")

    graph.set_entry_point("extract_info")

    def after_extract_info(state: State) -> str:
        next_node = "save_user" if state.user and not state.user_saved else "retrieve_context"
        print(f"➡️ after_extract_info ➜ {next_node}")
        return next_node
    graph.add_conditional_edges("extract_info", after_extract_info)

    graph.add_edge("save_user", "retrieve_context")
    graph.add_edge("retrieve_context", "build_prompt")
    graph.add_edge("build_prompt", "check_sent")

    def after_check_sent(state: State) -> str:
        next_node = "end" if state.already_sent_solution else "call_gemini"
        print(f"➡️ after_check_sent ➜ {next_node}")
        return next_node
    graph.add_conditional_edges("check_sent", after_check_sent)

    def after_call_gemini(state: State) -> str:
        next_node = "end" if state.already_sent else "check_AB"
        print(f"➡️ after_call_gemini ➜ {next_node}")
        return next_node
    graph.add_conditional_edges("call_gemini", after_call_gemini)

    def after_check_AB(state: State) -> str:
        print("➡️ after_check_AB ➜ end")
        return "end"
    graph.add_conditional_edges("check_AB", after_check_AB)

    graph.add_edge("end", END)

    print("✅ Grafo construido correctamente\n")
    return graph.compile()
