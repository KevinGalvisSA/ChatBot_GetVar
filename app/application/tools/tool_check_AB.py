# app/application/tools/tool_check_AB.py

import re
from app.domain.model.state import State

def check_AB_tool(state: State) -> dict:
    """
    Tool que evalúa si el bot ya ofreció las opciones A y B (venta o capacitación).
    """
    print("\n📌 [check_AB_tool] Ejecutando tool...")
    response_text = (state.response or "").lower().replace("ó", "o")
    print(f"🔎 Texto analizado: {response_text}")

    contiene_a = bool(re.search(r'\bopcion a\b', response_text))
    contiene_b = bool(re.search(r'\bopcion b\b', response_text))

    print(f"🔍 ¿Contiene 'opcion a'? ➜ {contiene_a}")
    print(f"🔍 ¿Contiene 'opcion b'? ➜ {contiene_b}")

    options_ab_sent = contiene_a or contiene_b
    print(f"📤 [check_AB_tool] Resultado ➜ options_ab_sent: {options_ab_sent}\n")

    return {"options_ab_sent": options_ab_sent}
