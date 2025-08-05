from app.domain.model.state import State
from app.infrastructure.sql.customer_saver import get_or_create_customer, update_customer_info

def save_user_tool(state: State) -> dict:
    """
    Tool que guarda el usuario en la base de datos si tiene información mínima.
    """
    print("\n📌 [save_user_tool] Ejecutando tool...")
    print(f"🔎 State inicial ➜ name: {state.name}, phone: {state.phone}, company: {state.company}, rol: {state.rol}")

    user_saved = False

    if state.name and state.phone:
        print("📥 Intentando guardar o buscar usuario en la base de datos...")
        customer = get_or_create_customer(state.name, state.phone)

        print("🛠️ Intentando actualizar datos del usuario (si aplica)...")
        update_customer_info(customer, company=state.company, rol=state.rol)

        print(f"✅ Usuario procesado correctamente (ID: {customer.id})")
        user_saved = True
    else:
        print("⚠️ No se pudo guardar el usuario: falta nombre o teléfono.")

    print(f"📤 [save_user_tool] Finalizando con ➜ user_saved: {user_saved}\n")
    return {"user_saved": user_saved}
