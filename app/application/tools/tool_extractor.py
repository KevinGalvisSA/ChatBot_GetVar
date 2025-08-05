from app.infrastructure.factories.extract_info import InfoExtractor
from app.domain.model.state import State

extractor = InfoExtractor()

def extract_user_info_tool(state: State) -> dict:
    try:
        print("\n🧠 Nodo: extract_user_info_tool")
        print("📥 Tipo de state:", type(state))
        print("➡️ Entrada:", getattr(state, "input", None))

        input_text = state.input or ""
        extracted = extractor.extract(input_text)

        # Preparar dict con actualizaciones
        updates = {}

        if not state.name and extracted.get("name"):
            updates["name"] = extracted["name"]
        if not state.phone and extracted.get("phone"):
            updates["phone"] = extracted["phone"]
        if not state.company and extracted.get("company"):
            updates["company"] = extracted["company"]
        if not state.rol and extracted.get("rol"):
            updates["rol"] = extracted["rol"]

        # Indicador de si se tiene la info mínima
        updates["user"] = bool(
            updates.get("name", state.name) and updates.get("phone", state.phone)
        )

        # Mensaje de validación opcional
        updates["output"] = extractor.validate_extracted_info(extracted)

        print("⬅️ Salida (updates):", updates)

        # Validación final
        if not isinstance(updates, dict):
            raise TypeError(f"❌ ERROR: se esperaba dict, se recibió {type(updates)}")

        return updates

    except Exception as e:
        print(f"❌ Error dentro de extract_user_info_tool: {e}")
        return {}  # Siempre retornar dict para evitar romper el grafo
