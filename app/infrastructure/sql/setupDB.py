from time import sleep
from typing import Callable, List, TypeVar
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage

from app.domain.model.messageStorage import MessageStorage  # Tu modelo personalizado

import os
load_dotenv()

# 🔗 Cargar cadena de conexión desde .env
Kai_Agent_DB = os.getenv("DB_HOST")

# 🛠️ Crear el engine con conexión persistente
engine = create_engine(Kai_Agent_DB, pool_recycle=600, pool_pre_ping=True)

# ✅ Probar conexión
try:
    with engine.connect() as conn:
        print("✅ Conectado correctamente a la base de datos.")
except Exception as e:
    print(f"❌ No se pudo conectar a la base de datos: {e}")

# 🔄 Mecanismo de reintento
T = TypeVar('T')
def execute_try(func: Callable[[], T], max_retries: int = 3) -> T:
    retries = 0
    last_error = None
    while retries < max_retries:
        try:
            return func()
        except OperationalError as e:
            last_error = e
            if "MySQL server has gone away" in str(e) and retries < max_retries - 1:
                retries += 1
                sleep(1 * retries)
                print(f"🔄 Reintentando conexión a la base de datos (intento {retries}/{max_retries})")
                continue
            raise e
    raise last_error

# ✅ Clase personalizada que usa tu modelo MessageStorage y guarda message_type correctamente
from sqlalchemy.orm import sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class ChatMessageHistory:
    def __init__(self, session_id: str, id_customer: int = 0, limit: int = 15):
        self.session_id = str(session_id)
        self.id_customer = id_customer
        self.limit = limit

    def get_messages(self) -> List[BaseMessage]:
        def get_messages_db():
            db = SessionLocal()
            try:
                rows = (
                    db.query(MessageStorage)
                    .filter(MessageStorage.session_id == self.session_id)
                    .order_by(MessageStorage.id.asc())
                    .limit(self.limit)
                    .all()
                )
                messages = []
                for row in rows:
                    if row.message_type == "human":
                        messages.append(HumanMessage(content=row.message))
                    elif row.message_type == "ai":
                        messages.append(AIMessage(content=row.message))
                    else:
                        print(f"⚠️ Tipo de mensaje desconocido: {row.message_type}")
                return messages
            finally:
                db.close()
        return execute_try(get_messages_db)

    def add_messages(self, message: BaseMessage) -> None:
        def add_message_db():
            db = SessionLocal()
            try:
                # Determinar el tipo del mensaje
                if isinstance(message, AIMessage):
                    message_type = "ai"
                elif isinstance(message, HumanMessage):
                    message_type = "human"
                else:
                    raise ValueError(f"Tipo de mensaje no soportado: {type(message)}")

                # Crear la instancia del modelo
                model_instance = MessageStorage(
                    id_customer=self.id_customer,
                    session_id=self.session_id,
                    message=message.content,
                    message_type=message_type
                )

                print(f"[DEBUG] Modelo a guardar: {vars(model_instance)}")
                db.add(model_instance)
                db.commit()
                print(f"[DB] Guardado mensaje en sesión {self.session_id}: {message.content}")
            except Exception as e:
                db.rollback()
                print(f"[ERROR] Fallo al guardar mensaje: {e}")
            finally:
                db.close()
        execute_try(add_message_db)

    def add_user_message(self, content: str) -> None:
        print(f"👤 Guardando mensaje del usuario: {content}")
        self.add_messages(HumanMessage(content=content))

    def add_ai_message(self, content: str) -> None:
        print(f"🤖 Guardando mensaje de la IA: {content}")
        self.add_messages(AIMessage(content=content))
