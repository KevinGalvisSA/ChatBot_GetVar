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

        updates = {}
        fields = ["name", "phone", "company", "rol"]

        for field in fields:
            current_value = getattr(state, field, None)
            new_value = extracted.get(field)
            updates[field] = current_value or new_value

        updates["user"] = bool(updates["name"] and updates["phone"])
        updates["output"] = extractor.validate_extracted_info(extracted)

        print("⬅️ Salida (updates):", updates)

        return updates if isinstance(updates, dict) else {}

    except Exception as e:
        print(f"❌ Error dentro de extract_user_info_tool: {e}")
        return {}
