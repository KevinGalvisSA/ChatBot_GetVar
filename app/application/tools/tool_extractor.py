# app/application/tools/tool_extractor.py

from app.infrastructure.factories.extract_info import InfoExtractor
from app.domain.model.state import State

extractor = InfoExtractor()

def extract_user_info_tool(state: State) -> dict:
    try:
        print("\n🧠 Nodo: extract_user_info_tool")
        # print("📥 Tipo de state:", type(state))
        # print("➡️ Entrada:", getattr(state, "input", None))

        input_text = state.input or ""
        extracted = extractor.extract(input_text)

        print("Elementos que extrae el 'extractor': ",extracted)

        updates = {}

        for field in ["name", "company", "rol"]:
            new_value = extracted.get(field)
            if new_value:  # Solo actualizamos si viene en el input
                updates[field] = new_value

        # El teléfono nunca se actualiza desde el input. Solo si no hay uno en el state.
        if not state.phone and extracted.get("phone"):
            updates["phone"] = extracted["phone"]

        # Solo marcamos como user si hay nombre y teléfono
        final_name = updates.get("name") or state.name
        final_phone = updates.get("phone") or state.phone

        print("nombre del usuario Final: ", final_name)
        print("telefono del usuario final:", final_phone)

        updates["user"] = bool(final_name and final_phone)

        # Mensaje de validación para el bot
        updates["output"] = extractor.validate_extracted_info({
            "name": final_name,
            "phone": final_phone
        })

        print("⬅️ Salida (updates):", updates)
        return updates

    except Exception as e:
        print(f"❌ Error dentro de extract_user_info_tool: {e}")
        return {}
