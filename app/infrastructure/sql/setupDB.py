import os
from time import sleep
from typing import Callable, List, TypeVar
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage

from app.domain.model.messageStorage import MessageStorage

load_dotenv()
Kai_Agent_DB = os.getenv("DB_HOST")

# 🛠️ Engine y sesión SQLAlchemy
engine = create_engine(Kai_Agent_DB, pool_recycle=600, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ✅ Probar conexión inicial
try:
    with engine.connect() as conn:
        print("✅ Conectado correctamente a la base de datos.")
except Exception as e:
    print(f"❌ Error conectando a la base de datos: {e}")

# 🔁 Función de reintento genérica
T = TypeVar("T")
def execute_try(func: Callable[[], T], max_retries: int = 1) -> T:
    retries = 0
    last_error = None
    while retries < max_retries:
        try:
            return func()
        except OperationalError as e:
            last_error = e
            if "MySQL server has gone away" in str(e):
                retries += 1
                sleep(1 * retries)
                print(f"🔄 Reintentando conexión ({retries}/{max_retries})...")
            else:
                break
    raise last_error  # type: ignore

# 🧠 Clase para gestionar historial de chat
class ChatMessageHistory:
    def __init__(self, session_id: str, id_customer: int = 0, limit: int = 15):
        self.session_id = session_id
        self.id_customer = id_customer
        self.limit = limit

    def get_messages(self) -> List[BaseMessage]:
        def _get():
            db = SessionLocal()
            try:
                rows = (
                    db.query(MessageStorage)
                    .filter(MessageStorage.session_id == self.session_id)
                    .order_by(MessageStorage.id.desc())
                    .limit(self.limit)
                    .all()
                )
                messages = []
                for row in reversed(rows):  # Reversar para orden cronológico
                    if row.message_type == "human": # type: ignore
                        messages.append(HumanMessage(content=row.message))  # type: ignore
                    elif row.message_type == "ai": # type: ignore
                        messages.append(AIMessage(content=row.message))  # type: ignore
                return messages
            finally:
                db.close()
        return execute_try(_get)

    def add_messages(self, message: BaseMessage) -> None:
        def _add():
            db = SessionLocal()
            try:
                msg_type = (
                    "ai" if isinstance(message, AIMessage)
                    else "human" if isinstance(message, HumanMessage)
                    else "unknown"
                )
                if msg_type == "unknown":
                    raise ValueError(f"Tipo de mensaje no soportado: {type(message)}")

                msg = MessageStorage(
                    id_customer=self.id_customer,
                    session_id=self.session_id,
                    message=message.content,
                    message_type=msg_type,
                )
                db.add(msg)
                db.commit()
            except Exception as e:
                db.rollback()
                print(f"❌ Error al guardar mensaje: {e}")
            finally:
                db.close()
        execute_try(_add)

    def add_user_message(self, content: str) -> None:
        self.add_messages(HumanMessage(content=content))

    def add_ai_message(self, content: str) -> None:
        self.add_messages(AIMessage(content=content))

# 📚 Extra: historial formateado como texto
def get_formatted_history(session_id: str, id_customer= 0, limit: int = 15) -> str:
    history = ChatMessageHistory(session_id=session_id, limit=limit)
    messages = history.get_messages()
    result = ""
    for m in messages:
        rol = "🧑 Usuario" if isinstance(m, HumanMessage) else "🤖 Bot"
        result += f"{rol}: {m.content}\n"
    return result
