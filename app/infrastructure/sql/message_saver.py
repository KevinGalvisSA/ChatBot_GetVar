# app/infrastructure/sql/message_history.py

from sqlalchemy.orm import sessionmaker
from app.domain.model.messageStorage import MessageStorage
from app.infrastructure.sql.setupDB import ChatMessageHistory, engine
from langchain_core.language_models import BaseLanguageModel

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def save_message(id_customer: int, session_id: str, content: str, message_type: str) -> None:
    print(f"💾 Guardando mensaje ➜ customer_id={id_customer}, session_id={session_id}, type={message_type}")
    db = SessionLocal()
    try:
        message = MessageStorage(
            id_customer=id_customer,
            session_id=session_id,
            message=content,
            message_type=message_type
        )
        db.add(message)
        db.commit()
        db.refresh(message)
        print(f"✅ Mensaje guardado: {message}")
    except Exception as e:
        db.rollback()
        print(f"❌ Error al guardar mensaje: {e}")
        raise
    finally:
        db.close()


def handle_conversation_flow(session_id: str, id_customer: int, user_input: str, model: BaseLanguageModel) -> str:
    history = ChatMessageHistory(session_id=session_id, id_customer=id_customer)
    history.add_user_message(user_input)
    messages = history.get_messages()
    response = model.generate_response(messages)
    history.add_ai_message(response)
    return response
