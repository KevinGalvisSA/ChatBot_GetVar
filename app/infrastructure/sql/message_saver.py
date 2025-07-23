from sqlalchemy.orm import sessionmaker
from app.domain.model.messageStorage import MessageStorage
from app.infrastructure.sql.setupDB import ChatMessageHistory, engine

# Crear una sesión local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def save_message(id_customer: int, id_session: int, content: str, message_type: str):
    """
    Guarda un mensaje en la base de datos.

    Args:
        id_customer (int): ID del cliente que envía o recibe el mensaje.
        id_session (int): ID de la sesión de conversación.
        content (str): Contenido textual del mensaje.
        message_type (str): Tipo de mensaje, por ejemplo 'ai' o 'human'.
    """
    db = SessionLocal()
    try:
        print(f"🛠️ DEBUG ➜ id_customer={id_customer}, id_session={id_session}, message_type={message_type}")
        
        new_message = MessageStorage(
            id_customer=id_customer,
            id_session=str(id_session),
            message=content,
            message_type=message_type
        )

        print(f"🧪 DEBUG ➜ Objeto a guardar: {vars(new_message)}")

        db.add(new_message)
        db.commit()
        db.refresh(new_message)  # 🔄 Opcional: actualiza con valores generados como ID

        print(f"✅ Mensaje guardado exitosamente: {new_message}")
    except Exception as e:
        db.rollback()
        print(f"❌ Error guardando en messageStorage: {e}")
    finally:
        db.close()


def handle_conversation_flow(id_session: str, id_customer: int, user_input: str, model) -> str:
    history = ChatMessageHistory(id_session=id_session, id_customer=id_customer)
    history.add_user_message(user_input)
    messages = history.get_messages()
    response = model.generate_response(messages)
    history.add_ai_message(response)
    return response
