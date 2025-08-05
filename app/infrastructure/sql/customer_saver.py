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
    Actualiza los campos 'company' y 'rol' del cliente si se proporcionan nuevos valores
    distintos a los actuales.
    """
    print(f"🔄 [update_customer_info] Verificando actualización para cliente ID: {customer.id}")
    session = SessionLocal()
    try:
        updated = False

        if company and customer.company != company:
            print(f"🏢 Empresa actual: {customer.company} ➜ Nueva: {company}")
            customer.company = company
            updated = True

        if rol and customer.rol != rol:
            print(f"👔 Rol actual: {customer.rol} ➜ Nuevo: {rol}")
            customer.rol = rol
            updated = True

        if updated:
            session.merge(customer)
            session.commit()
            print("✅ Cliente actualizado con nuevos datos.")
        else:
            print("ℹ️ No se realizó ninguna actualización (los datos eran iguales).")

    except Exception as e:
        print(f"❌ Error al actualizar cliente: {e}")
        session.rollback()
        raise e
    finally:
        session.close()
