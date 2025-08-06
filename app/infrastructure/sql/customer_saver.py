# app/infrastructure/sql/customer_saver.py

from app.domain.model.customer import Customer
from app.infrastructure.sql.setupDB import SessionLocal

def get_or_create_customer(name: str, phone: int) -> Customer:
    print(f"🔍 Buscando o creando cliente ➜ name: {name}, phone: {phone}")
    session = SessionLocal()
    try:
        customer = session.query(Customer).filter_by(phone=phone).first()
        if customer:
            print(f"✅ Cliente encontrado: {customer}")
            return customer

        new_customer = Customer(name=name or "Sin nombre", phone=phone)
        session.add(new_customer)
        session.commit()
        session.refresh(new_customer)
        print(f"🆕 Cliente creado: {new_customer}")
        return new_customer
    except Exception as e:
        session.rollback()
        print(f"❌ Error en get_or_create_customer: {e}")
        raise
    finally:
        session.close()


def update_customer_info(customer: Customer, name: str = None, company: str = None, rol: str = None) -> None:
    print(f"🔄 Verificando actualización para cliente ID: {customer.id}")
    session = SessionLocal()
    try:
        updated = False

        if name and customer.name != name:
            customer.name = name
            print(f"📝 Nombre actualizado a: {name}")
            updated = True

        if company and customer.company != company:
            customer.company = company
            print(f"🏢 Empresa actualizada a: {company}")
            updated = True

        if rol and customer.rol != rol:
            customer.rol = rol
            print(f"👔 Rol actualizado a: {rol}")
            updated = True

        if updated:
            session.merge(customer)
            session.commit()
            print("✅ Cliente actualizado con nuevos datos.")
        else:
            print("ℹ️ No se realizaron cambios.")
    except Exception as e:
        session.rollback()
        print(f"❌ Error al actualizar cliente: {e}")
        raise
    finally:
        session.close()

