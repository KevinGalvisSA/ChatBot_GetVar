# app/application/tools/tool_save_user.py

from app.domain.model.state import State
from app.infrastructure.sql.customer_saver import get_or_create_customer, update_customer_info

def save_user_tool(state: State) -> dict:
    print("\n📌 [save_user_tool] Ejecutando tool...")
    print(f"🔎 State ➜ name: {state.name}, phone: {state.phone}, company: {state.company}, rol: {state.rol}")

    user_saved = False
    customer_id = state.customer_id  # Mantener el existente si no se encuentra/crea nuevo

    if state.name and state.phone:
        print("📥 Buscando o creando usuario...")
        customer = get_or_create_customer(state.name, state.phone)
        customer_id = customer.id  # ✅ Guardamos el ID en variable

        # Solo actualizamos si en el input vino nueva info
        updates = {}
        if state.company and state.company != customer.company:
            updates["company"] = state.company
        if state.rol and state.rol != customer.rol:
            updates["rol"] = state.rol
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
        print("⚠️ No se pudo guardar el usuario: falta nombre o teléfono.")

    print(f"📤 [save_user_tool] Finalizando ➜ user_saved: {user_saved}, customer_id: {customer_id}\n")
    # ✅ Ahora devolvemos también el ID para que se guarde en el state
    return {"user_saved": user_saved, "customer_id": customer_id}
