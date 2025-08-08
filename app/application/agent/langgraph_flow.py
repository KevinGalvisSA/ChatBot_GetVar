from langgraph.graph import StateGraph, END
from typing import Callable

from app.domain.model.state import State
from app.application.tools.tool_extractor import extract_user_info_tool
from app.application.tools.tool_save_user import save_user_tool
from app.application.tools.tool_qdrant import retrieve_context_tool
from app.application.tools.tool_save_message import get_history_tool, save_message_tool
from app.application.tools.tool_prompt import build_prompt_tool
from app.application.tools.tool_gemini import call_gemini_tool
from app.application.tools.tool_check_sent import check_already_sent_tool
from app.application.tools.tool_check_AB import check_AB_tool
from app.application.tools.tool_state import get_state_tool, save_state_tool


def wrap_tool(tool_func: Callable[[State], dict], name: str) -> Callable[[State], State]:
    def wrapped(state: State) -> State:  # type: ignore
        print(f"\n🚀 Ejecutando nodo: {name}")
        print(f"📥 Entrada State para {name}: {state}")
        result_dict = tool_func(state)
        print(f"✅ Resultado nodo {name}: {result_dict}")
        if not isinstance(result_dict, dict):
            raise TypeError(f"❌ Nodo {name} devolvió {type(result_dict)} en vez de dict")
        merged = {**state.model_dump(), **result_dict}
        return State(**merged)
    return wrapped


def wrap_tool_dict_input(tool_func: Callable[[dict], dict], name: str) -> Callable[[State], State]:
    def wrapped(state: State) -> State:
        print(f"\n🚀 Ejecutando nodo: {name}")
        print(f"📥 Entrada State para {name}: {state}")
        result_dict = tool_func(state.model_dump())
        print(f"✅ Resultado nodo {name}: {result_dict}")
        if not isinstance(result_dict, dict):
            raise TypeError(f"❌ Nodo {name} devolvió {type(result_dict)} en vez de dict")
        merged = {**state.model_dump(), **result_dict}
        return State(**merged)
    return wrapped


def load_state_tool_wrapper(state_dict_or_state: dict | State, config=None) -> dict:
    if isinstance(state_dict_or_state, State):
        state = state_dict_or_state
    elif isinstance(state_dict_or_state, dict):
        state = State(**state_dict_or_state)
    else:
        raise TypeError(f"Se esperaba dict o State, pero llegó {type(state_dict_or_state)}")

    session_id = state.session_id
    if session_id is None:
        raise ValueError("❌ No se puede obtener el state: session_id es None")

    loaded_state_dict = get_state_tool(session_id)  # dict con el estado cargado

    current_state_dict = state.model_dump()

    merged_state = {}
    for key in loaded_state_dict.keys():
        val_current = current_state_dict.get(key)
        val_loaded = loaded_state_dict.get(key)

        # Si el valor actual es None, usamos el cargado. Si no, respetamos el actual
        merged_state[key] = val_loaded if val_current is None else val_current

    return merged_state


def wrap_save_message_tool(name: str = "save_message") -> Callable[[State], State]:
    def wrapped(state: State) -> State:
        print(f"\n🚀 Ejecutando nodo: {name}")
        print(f"📥 Entrada State para {name}: {state}")

        # Mensaje de usuario (input)
        message_content = getattr(state, "input", "")
        message_type = getattr(state, "message_type", "human")

        result_dict = save_message_tool(state, message_content, message_type)

        print(f"✅ Resultado nodo {name}: {result_dict}")

        if not isinstance(result_dict, dict):
            raise TypeError(f"❌ Nodo {name} devolvió {type(result_dict)} en vez de dict")

        merged = {**state.model_dump(), **result_dict}
        return State(**merged)

    return wrapped


def wrap_save_bot_message_tool(name: str = "save_bot_message") -> Callable[[State], State]:
    def wrapped(state: State) -> State:
        print(f"\n🚀 Ejecutando nodo: {name}")
        print(f"📥 Entrada State para {name}: {state}")

        # Mensaje bot (response)
        message_content = getattr(state, "response", "")
        message_type = "ai"

        result_dict = save_message_tool(state, message_content, message_type)

        print(f"✅ Resultado nodo {name}: {result_dict}")

        if not isinstance(result_dict, dict):
            raise TypeError(f"❌ Nodo {name} devolvió {type(result_dict)} en vez de dict")

        merged = {**state.model_dump(), **result_dict}
        return State(**merged)

    return wrapped


def build_kai_graph():
    print("🧠 Entrando a build_kai_graph()")

    graph = StateGraph(State)

    print("🔧 Añadiendo nodos...")

    graph.add_node("load_state", wrap_tool(load_state_tool_wrapper, "load_state"))  # type: ignore
    graph.add_node("save_state", wrap_tool_dict_input(save_state_tool, "save_state"))  # type: ignore PASAR dict aquí
    graph.add_node("extract_info", wrap_tool(extract_user_info_tool, "extract_info"))  # type: ignore
    graph.add_node("save_user", wrap_tool(save_user_tool, "save_user"))  # type: ignore

    graph.add_node("save_message", wrap_save_message_tool())  # type: ignore # nodo para guardar mensaje usuario
    graph.add_node("save_bot_message", wrap_save_bot_message_tool())  # type: ignore # nodo para guardar mensaje bot
    graph.add_node("get_history", wrap_tool(get_history_tool, "get_history"))  # type: ignore # solo obtiene historial

    graph.add_node("retrieve_context", wrap_tool(retrieve_context_tool, "retrieve_context"))  # type: ignore
    graph.add_node("build_prompt", wrap_tool(build_prompt_tool, "build_prompt"))  # type: ignore
    graph.add_node("check_sent", wrap_tool(check_already_sent_tool, "check_sent"))  # type: ignore
    graph.add_node("call_gemini", wrap_tool(call_gemini_tool, "call_gemini"))  # type: ignore
    graph.add_node("check_AB", wrap_tool(check_AB_tool, "check_AB"))  # type: ignore

    graph.add_node("end", lambda state: (
        print("🏁 Nodo final alcanzado"),
        state
    )[1])  # solo un parámetro en lambda

    graph.set_entry_point("load_state")

    graph.add_edge("load_state", "extract_info")
    graph.add_edge("extract_info", "save_user")

    # Guardar mensaje recibido (usuario)
    graph.add_edge("save_user", "save_message")

    # Obtener historial actualizado tras guardar mensaje usuario
    graph.add_edge("save_message", "get_history")

    graph.add_edge("get_history", "retrieve_context")
    graph.add_edge("retrieve_context", "build_prompt")
    graph.add_edge("build_prompt", "check_sent")

    def after_check_sent(state: State) -> str:
        return "end" if state.already_sent_solution else "call_gemini"
    graph.add_conditional_edges("check_sent", after_check_sent)

    def after_call_gemini(state: State) -> str:
        return "save_bot_message" if not state.already_sent else "check_AB"
    graph.add_conditional_edges("call_gemini", after_call_gemini)

    graph.add_edge("save_bot_message", "check_AB")
    graph.add_edge("check_AB", "save_state")
    graph.add_edge("save_state", "end")
    graph.add_edge("end", END)

    print("✅ Grafo construido correctamente\n")
    return graph.compile()
