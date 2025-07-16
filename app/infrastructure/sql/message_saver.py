# app/infrastructure/sql/message_saver.py
from app.domain.model.messageStorage import MessageStorage
from sqlalchemy.orm import sessionmaker
from app.infrastructure.sql.setupDB import engine

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def save_message(id_customer: int, session_id: int, content: str):
    db = SessionLocal()
    try:
        new_message = MessageStorage(
            id_customer=id_customer,
            session_id=session_id,
            message=content
        )
        db.add(new_message)
        db.commit()
        print(f"✅ Mensaje guardado: {content}")
    except Exception as e:
        db.rollback()
        print(f"❌ Error guardando mensaje: {e}")
    finally:
        db.close()
