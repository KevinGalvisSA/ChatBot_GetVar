# app/application/agent/langgraph_flow.py

from langgraph.graph import StateGraph, END
from typing import Callable
from app.domain.model.state import State

# Importa todas tus tools
from app.application.tools.tool_save_message import save_message_tool, get_history_tool
from app.application.tools.tool_qdrant import retrieve_context_tool
from app.application.tools.tool_prompt import build_prompt_tool
from app.application.tools.tool_gemini import call_gemini_tool
from app.application.tools.tool_check_sent import check_already_sent_tool
from app.application.tools.tool_check_AB import check_AB_tool
from app.application.tools.tool_state import get_state_tool, save_state_tool
from app.application.tools.tool_update_name import update_name_tool
from app.application.tools.tool_update_company import update_company_tool
from app.application.tools.tool_update_role import update_role_tool
from app.application.tools.tool_create_user import create_user_tool

TOOLS = {
    "save_message": save_message_tool,
    "get_history": get_history_tool,
    "retrieve_context": retrieve_context_tool,
    "build_prompt": build_prompt_tool,
    "call_gemini": call_gemini_tool,
    "check_sent": check_already_sent_tool,
    "check_AB": check_AB_tool,
    "get_state": get_state_tool,
    "save_state": save_state_tool,
    "update_name": update_name_tool,
    "update_company": update_company_tool,
    "update_role": update_role_tool,
    "create_user": create_user_tool,
}

def merge_state_preserving_values(old: dict, new: dict) -> dict:
    merged = old.copy()
    for k, v in new.items():
        if v is not None:
            merged[k] = v
    return merged

# Wrapper general para tools que esperan {"state": {...}}
def wrap_tool_dict_input(tool_func: Callable[[dict], dict], name: str) -> Callable[[State], State]:
    def wrapped(state: State) -> State:
        print(f"\n🚀 Ejecutando nodo: {name}")
        print(f"📥 Entrada State para {name}: {state}")
        result_dict = tool_func({"state": state.model_dump()})
        print(f"✅ Resultado nodo {name}: {result_dict}")
        if not isinstance(result_dict, dict):
            raise TypeError(f"❌ Nodo {name} devolvió {type(result_dict)} en vez de dict")
        merged = merge_state_preserving_values(state.model_dump(), result_dict)
        return State(**merged)
    return wrapped

# Wrapper específico para create_user, también envuelve en "state"
def wrap_create_user_tool(name: str = "create_user") -> Callable[[State], State]:
    def wrapped(state: State) -> State:
        print(f"\n🚀 Ejecutando nodo: {name}")
        print(f"📥 Entrada State para {name}: {state}")
        result_dict = TOOLS[name]({"state": state.model_dump()})
        print(f"✅ Resultado nodo {name}: {result_dict}")
        if not isinstance(result_dict, dict):
            raise TypeError(f"❌ Nodo {name} devolvió {type(result_dict)} en vez de dict")
        merged = merge_state_preserving_values(state.model_dump(), result_dict)
        return State(**merged)
    return wrapped

# Wrapper especial para call_gemini_tool, que espera dict con "state"
def wrap_call_gemini_tool(tool_func: Callable[[dict], dict], name: str = "call_gemini") -> Callable[[State], State]:
    def wrapped(state: State) -> State:
        print(f"\n🚀 Ejecutando nodo: {name}")
        print(f"📥 Entrada State para {name}: {state}")
        result_dict = tool_func({"state": state.model_dump()})
        print(f"✅ Resultado nodo {name}: {result_dict}")
        if not isinstance(result_dict, dict):
            raise TypeError(f"❌ Nodo {name} devolvió {type(result_dict)} en vez de dict")
        merged = merge_state_preserving_values(state.model_dump(), result_dict)
        return State(**merged)
    return wrapped

def wrap_save_message_tool(name: str = "save_message") -> Callable[[State], State]:
    def wrapped(state: State) -> State:
        print(f"\n🚀 Ejecutando nodo: {name}")
        print(f"📥 Entrada State para {name}: {state}")

        input_to_tool = {
            "state": state.model_dump(),
            "message_content": getattr(state, "input", "") or "",
            "message_type": getattr(state, "message_type", "human"),
        }

        result_dict = TOOLS["save_message"](input_to_tool)
        print(f"✅ Resultado nodo {name}: {result_dict}")

        if not isinstance(result_dict, dict):
            raise TypeError(f"❌ Nodo {name} devolvió {type(result_dict)} en vez de dict")

        merged = merge_state_preserving_values(state.model_dump(), result_dict)
        return State(**merged)
    return wrapped

def wrap_save_bot_message_tool(name: str = "save_bot_message") -> Callable[[State], State]:
    def wrapped(state: State) -> State:
        print(f"\n🚀 Ejecutando nodo: {name}")
        print(f"📥 Entrada State para {name}: {state}")

        input_to_tool = {
            "state": state.model_dump(),
            "message_content": getattr(state, "response", "") or "",
            "message_type": "ai",
        }

        result_dict = TOOLS["save_message"](input_to_tool)
        print(f"✅ Resultado nodo {name}: {result_dict}")

        if not isinstance(result_dict, dict):
            raise TypeError(f"❌ Nodo {name} devolvió {type(result_dict)} en vez de dict")

        merged = merge_state_preserving_values(state.model_dump(), result_dict)
        return State(**merged)
    return wrapped

def build_kai_graph():
    print("🧠 Entrando a build_kai_graph()")

    graph = StateGraph(State)

    print("🔧 Añadiendo nodos...")

    simple_tools = [
        "get_state",
        "create_user",    # create_user va con wrapper específico
        "save_state",
        "get_history",
        "retrieve_context",
        "build_prompt",
        "check_sent",
        "call_gemini",
        "check_AB",
        "update_name",
        "update_company",
        "update_role",
    ]

    # Agregar nodos con wrapper general o específico
    for name in simple_tools:
        if name == "create_user":
            graph.add_node(name, wrap_create_user_tool(name))
        elif name == "call_gemini":
            graph.add_node(name, wrap_call_gemini_tool(TOOLS[name], name))
        else:
            graph.add_node(name, wrap_tool_dict_input(TOOLS[name], name))

    graph.add_node("save_message", wrap_save_message_tool())
    graph.add_node("save_bot_message", wrap_save_bot_message_tool())

    graph.add_node("end", lambda state: (
        print("🏁 Nodo final alcanzado"),
        state
    )[1])

    graph.set_entry_point("get_state")

    graph.add_edge("get_state", "create_user")
    graph.add_edge("create_user", "save_message")
    graph.add_edge("save_message", "get_history")
    graph.add_edge("get_history", "retrieve_context")
    graph.add_edge("retrieve_context", "build_prompt")
    graph.add_edge("build_prompt", "check_sent")

    def after_check_sent(state: State) -> str:
        return "end" if state.already_sent_solution else "call_gemini"

    graph.add_conditional_edges("check_sent", after_check_sent)

    graph.add_edge("call_gemini", "update_name")
    graph.add_edge("update_name", "update_company")
    graph.add_edge("update_company", "update_role")
    graph.add_edge("update_role", "save_bot_message")

    graph.add_edge("save_bot_message", "check_AB")
    graph.add_edge("check_AB", "save_state")
    graph.add_edge("save_state", "end")
    graph.add_edge("end", END)

    print("✅ Grafo construido correctamente\n")
    return graph.compile()
