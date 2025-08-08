# app/application/tools/tool_save_user.py

from app.domain.model.state import State
from app.infrastructure.sql.customer_saver import get_or_create_customer, update_customer_info

def save_user_tool(state: State) -> dict:
    print("\n📌 [save_user_tool] Ejecutando tool...")

    user_saved = False
    customer_id = state.customer_id  # Mantener el existente si no se encuentra/crea nuevo

    # Solo se requiere teléfono para crear, nombre puede ser None
    if state.phone:
        print("📥 Buscando o creando usuario...")
        # Si name es None, se pasa None
        customer = get_or_create_customer(state.name, state.phone)
        customer_id = customer.id

        print("Este es el customer:", customer)

        # Actualizar info solo si se pasa en state y es diferente
        updates = {}
        if state.company and state.company != customer.company:
            updates["company"] = state.company
        if state.rol and state.rol != customer.rol:
            updates["rol"] = state.rol
        # Solo actualizar nombre si viene en state y es distinto y no es None
        if state.name and state.name != customer.name:
            updates["name"] = state.name

        if updates:
            print("🛠️ Cambios detectados. Actualizando información del cliente...")
            update_customer_info(customer, **updates)
        else:
            print("✅ No se detectaron cambios. Cliente ya actualizado.")

        print(f"✅ Usuario procesado correctamente (ID: {customer.id})")
        user_saved = True
    else:
        print("⚠️ No se pudo guardar el usuario: falta teléfono.")

    print(f"📤 [save_user_tool] Finalizando ➜ user_saved: {user_saved}, customer_id: {customer_id}\n")
    return {"user_saved": user_saved, "customer_id": customer_id}
