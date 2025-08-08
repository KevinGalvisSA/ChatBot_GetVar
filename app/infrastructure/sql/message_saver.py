# app/infrastructure/sql/message_saver.py

from app.domain.model.messageStorage import MessageStorage
from app.infrastructure.sql.setupDB import SessionLocal

def save_message(id_customer: int, session_id: str, content: str, message_type: str) -> MessageStorage:
    print(f"💾 Guardando mensaje ➜ customer_id={id_customer}, session_id={session_id}, type={message_type}")
    session = SessionLocal()
    try:
        message = MessageStorage(
            id_customer=id_customer,
            session_id=session_id,
            message=content,
            message_type=message_type
        )
        session.add(message)
        session.commit()
        session.refresh(message)
        print(f"✅ Mensaje guardado: {message}")
        return message
    except Exception as e:
        session.rollback()
        print(f"❌ Error al guardar mensaje: {e}")
        raise
    finally:
        session.close()


def get_messages_by_session(session_id: int, id_customer: int, limit: int = 15) -> list[MessageStorage]:
    print(f"📜 Obteniendo historial ➜ session_id={session_id}, customer_id={id_customer}")
    session = SessionLocal()
    try:
        query = (
            session.query(MessageStorage)
            .filter_by(session_id=session_id, id_customer=id_customer)
            .order_by(MessageStorage.id.desc())  # orden inverso para traer los últimos
        )
        if limit:
            query = query.limit(limit)
        messages = query.all()
        messages.reverse()  # para que queden en orden cronológico ascendente
        print(f"✅ {len(messages)} mensajes encontrados")
        return messages
    except Exception as e:
        print(f"❌ Error al obtener historial: {e}")
        raise
    finally:
        session.close()
