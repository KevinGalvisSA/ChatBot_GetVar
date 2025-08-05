from app.domain.model.state import State
from app.application.prompts.base_prompt import build_prompt

def build_prompt_tool(state: State) -> dict:
    """
    Tool que construye el prompt a partir del estado actual.
    """
    print("\n🧱 [build_prompt_tool] Generando prompt...")

    print(f"🧩 Estado previo al prompt ➜ input: {state.input}, context: {state.context}")

    try:
        prompt = build_prompt(state)
        print(f"✅ Prompt generado:\n{prompt}\n")
    except Exception as e:
        prompt = "⚠️ Error al construir el prompt."
        print(f"❌ Error en build_prompt: {e}")

    return {
        "prompt": prompt
    }
