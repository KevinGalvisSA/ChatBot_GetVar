from app.domain.model.state import State
from app.infrastructure.sql.customer_saver import get_or_create_customer, update_customer_info

def save_user_tool(state: State) -> dict:
    """
    Tool que guarda el usuario en la base de datos si tiene información mínima.
    Si el usuario ya existe y se detecta algún cambio en su info, lo actualiza.
    """
    print("\n📌 [save_user_tool] Ejecutando tool...")
    print(f"🔎 State ➜ name: {state.name}, phone: {state.phone}, company: {state.company}, rol: {state.rol}")

    user_saved = False

    if state.name and state.phone:
        print("📥 Buscando o creando usuario...")
        customer = get_or_create_customer(state.name, state.phone)

        # Detectar si hay cambios
        needs_update = (
            (state.name and customer.name != state.name) or
            (state.company and customer.company != state.company) or
            (state.rol and customer.rol != state.rol)
        )

        if needs_update:
            print("🛠️ Cambios detectados. Actualizando información del cliente...")
            update_customer_info(
                customer,
                name=state.name,
                company=state.company,
                rol=state.rol
            )
        else:
            print("✅ No se detectaron cambios. Cliente ya actualizado.")

        print(f"✅ Usuario procesado correctamente (ID: {customer.id})")
        user_saved = True
    else:
        print("⚠️ No se pudo guardar el usuario: falta nombre o teléfono.")

    print(f"📤 [save_user_tool] Finalizando ➜ user_saved: {user_saved}\n")
    return {"user_saved": user_saved}
