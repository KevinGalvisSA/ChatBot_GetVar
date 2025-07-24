import re
from app.domain.model.customer import Customer
from app.infrastructure.sql.setupDB import SessionLocal
from datetime import datetime

def is_valid_name(name: str) -> bool:
    return bool(name.strip())

def is_valid_phone(phone: str | int) -> bool:
    return bool(re.fullmatch(r"\d{7,15}", str(phone)))

def get_customer_if_valid(name: str, phone: str | int) -> Customer | None:
    """
    Retorna un cliente existente si el nombre y teléfono son válidos y el cliente ya está registrado.
    """
    if not is_valid_name(name):
        print("❌ Nombre inválido.")
        return None
    if not is_valid_phone(phone):
        print("❌ Teléfono inválido.")
        return None

    try:
        phone = int(phone)
    except ValueError:
        print("❌ Teléfono no es un número válido.")
        return None

    db = SessionLocal()
    try:
        customer = db.query(Customer).filter_by(phone=phone).first()
        if customer:
            return customer
        else:
            print("⚠️ Cliente no encontrado.")
            return None
    except Exception as e:
        print(f"❌ Error al buscar cliente: {e}")
        return None
    finally:
        db.close()
