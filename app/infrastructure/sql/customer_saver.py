from app.domain.model.customer import Customer
from app.infrastructure.sql.setupDB import SessionLocal

def get_or_create_customer(name: str, phone: int) -> Customer:
    print(f"🔍 [get_or_create_customer] Buscando o creando cliente ➜ name: {name}, phone: {phone}")
    
    session = SessionLocal()
    try:
        customer = session.query(Customer).filter(Customer.phone == phone).first()

        if customer:
            print(f"✅ Cliente encontrado ➜ ID: {customer.id}, Nombre: {customer.name}, Teléfono: {customer.phone}")
            return customer

        # Crear nuevo cliente
        new_customer = Customer(name=name or "Sin nombre", phone=phone)
        session.add(new_customer)
        session.commit()
        session.refresh(new_customer)

        print(f"🆕 Cliente creado ➜ ID: {new_customer.id}, Nombre: {new_customer.name}, Teléfono: {new_customer.phone}")
        return new_customer
    except Exception as e:
        print(f"❌ Error en get_or_create_customer: {e}")
        session.rollback()
        raise e
    finally:
        session.close()

def update_customer_info(customer: Customer, company: str = None, rol: str = None):
    """
    Actualiza los campos 'company' y 'rol' del cliente si están vacíos y se proporcionan nuevos valores.
    """
    print(f"🔄 [update_customer_info] Verificando actualización para cliente ID: {customer.id}")
    session = SessionLocal()
    try:
        updated = False

        if company and not customer.company:
            customer.company = company
            print(f"🏢 Actualizando empresa a: {company}")
            updated = True

        if rol and not customer.rol:
            customer.rol = rol
            print(f"👔 Actualizando rol a: {rol}")
            updated = True

        if updated:
            session.merge(customer)  # O session.add(customer), ambos funcionan
            session.commit()
            print("✅ Cliente actualizado con nuevos datos.")
        else:
            print("ℹ️ No se realizó ninguna actualización (ya existían los datos).")

    except Exception as e:
        print(f"❌ Error al actualizar cliente: {e}")
        session.rollback()
        raise e
    finally:
        session.close()
