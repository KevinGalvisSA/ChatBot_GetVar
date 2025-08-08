# app/application/tools/tool_check_sent.py

import re
from app.domain.model.state import State

def check_already_sent_tool(state: State) -> dict:
    """
    Tool que revisa si la solución ya fue enviada previamente.
    """
    print("\n📌 [check_already_sent_tool] Ejecutando tool...")
    response_text = (state.response or "").lower().replace("ó", "o")
    # print(f"🔎 Texto analizado: {response_text}")

    contiene_a = bool(re.search(r'\bsolucion a\b', response_text))
    contiene_b = bool(re.search(r'\bsolucion b\b', response_text))

    print(f"🔍 ¿Contiene 'solucion a'? ➜ {contiene_a}")
    print(f"🔍 ¿Contiene 'solucion b'? ➜ {contiene_b}")

    already_sent = contiene_a or contiene_b
    print(f"📤 [check_already_sent_tool] Resultado ➜ already_sent_solution: {already_sent}\n")

    return {"already_sent_solution": already_sent}
