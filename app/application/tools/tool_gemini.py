# app/application/tools/tool_gemini.py

from app.domain.model.state import State
from app.infrastructure.factories.gemini_integration import answer_with_gemini

def call_gemini_tool(state: State) -> dict:
    """
    Tool que envía el prompt a Gemini y guarda la respuesta.
    """
    print("\n🤖 [call_gemini_tool] Ejecutando tool...")

    prompt = state.prompt or "No prompt definido."
    chunks = state.context or []  # 👈 Asegúrate de pasar la lista de chunks

    print(f"📨 Prompt enviado a Gemini:\n{prompt}\n")
    print(f"📚 Chunks enviados: {len(chunks)}")

    try:
        result = answer_with_gemini(prompt, chunks)  # ✅ ahora sí pasan ambos
        print(f"✅ Respuesta recibida de Gemini:\n{result}\n")
    except Exception as e:
        result = "⚠️ Ocurrió un error al consultar Gemini."
        print(f"❌ Error al llamar a Gemini: {e}")

    return {
        "response": result
    }
