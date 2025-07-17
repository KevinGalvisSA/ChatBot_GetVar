from sqlalchemy.orm import sessionmaker
from app.domain.model.messageStorage import MessageStorage
from app.infrastructure.sql.setupDB import engine

# Crear una sesión local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def save_message(id_customer: int, session_id: int, content: str, message_type: str):
    """
    Guarda un mensaje en la base de datos.

    Args:
        id_customer (int): ID del cliente que envía o recibe el mensaje.
        session_id (int): ID de la sesión de conversación.
        content (str): Contenido textual del mensaje.
        message_type (str): Tipo de mensaje, por ejemplo 'ai' o 'human'.
    """
    db = SessionLocal()
    try:
        print(f"🛠️ DEBUG ➜ id_customer={id_customer}, session_id={session_id}, message_type={message_type}")
        
        new_message = MessageStorage(
            id_customer=id_customer,
            session_id=str(session_id),
            message=content,
            message_type=message_type  # ✅ usa el nombre real del campo
        )

        print(f"🧪 DEBUG ➜ Objeto a guardar: {vars(new_message)}")

        db.add(new_message)
        db.commit()

        print(f"✅ Mensaje guardado exitosamente: {content}")
    except Exception as e:
        db.rollback()
        print(f"❌ Error guardando en messageStorage: {e}")
    finally:
        db.close()
