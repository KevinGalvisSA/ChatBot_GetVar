from app.domain.model.customer import Customer
from app.infrastructure.sql.setupDB import SessionLocal
from datetime import datetime

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