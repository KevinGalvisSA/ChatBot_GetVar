from app.domain.model.customer import Customer
from app.infrastructure.sql.setupDB import SessionLocal
from datetime import datetime

def get_or_create_customer(name: str, phone_number: int) -> Customer | None:
    db = SessionLocal()
    try:
        customer = db.query(Customer).filter_by(phone_number=phone_number).first()
        if not customer:
            now = datetime.now()
            customer = Customer(
                name=name,
                phone_number=phone_number,
                createdBy=0,
                updatedBy=0,
                createdAt=now,
                updatedAt=now
            )
            db.add(customer)
            db.commit()
            db.refresh(customer)
        return customer
    except Exception as e:
        print(f"❌ Error en get_or_create_customer: {e}")
        return None
    finally:
        db.close()
