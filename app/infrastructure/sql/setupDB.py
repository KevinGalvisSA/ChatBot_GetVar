from time import sleep
from typing import Callable, List, TypeVar
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_community.chat_message_histories import SQLChatMessageHistory

from app.domain.model.messageStorage import MessageStorage  # 👈 Tu modelo propio

import os
load_dotenv()

# Cargar cadena de conexión desde .env
Kai_Agent_DB = os.getenv("DB_HOST")

# Crear el engine con conexión persistente
engine = create_engine(Kai_Agent_DB, pool_recycle=600, pool_pre_ping=True)

# Probar conexión al iniciar
try:
    with engine.connect() as conn:
        print("✅ Conectado correctamente a la base de datos.")
except Exception as e:
    print(f"❌ No se pudo conectar a la base de datos: {e}")

# Mecanismo de reintento
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

# Clase personalizada que usa tu modelo MessageStorage
class ChatMessageHistory(SQLChatMessageHistory):
    def __init__(self, session_id, limit=15, connection=engine):
        super().__init__(session_id=session_id, connection=connection)
        self.session_id = session_id
        self.connection = connection
        self.limit = limit

        # 👇 Esta es la clave: indicarle a LangChain que use tu modelo
        self.sql_model_class = MessageStorage
        self.session_id_field_name = "session_id"

    def get_messages(self) -> List[BaseMessage]:
        """Recuperar mensajes con reintento y orden"""
        def get_messages_db():
            with self._make_sync_session() as session:
                result = (
                    session.query(self.sql_model_class)
                    .filter(getattr(self.sql_model_class, self.session_id_field_name) == self.session_id)
                    .order_by(self.sql_model_class.id.asc())  # ascendente para orden cronológico
                    .limit(self.limit)
                )
                messages = [self.converter.from_sql_model(r) for r in result]
                return messages
        return execute_try(get_messages_db)

    def add_messages(self, message: BaseMessage) -> None:
        """Guardar mensaje en DB con reintento"""
        def add_message_db():
            with self._make_sync_session() as session:
                model_instance = self.converter.to_sql_model(message, self.session_id)
                session.add(model_instance)
                session.commit()
                print(f"[DB] Guardado mensaje en sesión {self.session_id}: {message.content}")
        execute_try(add_message_db)

    def add_user_message(self, content: str) -> None:
        """Guardar mensaje del usuario"""
        print(f"👤 Guardando mensaje del usuario: {content}")
        self.add_messages(HumanMessage(content=content))

    def add_ai_message(self, content: str) -> None:
        """Guardar mensaje del asistente"""
        print(f"🤖 Guardando mensaje de la IA: {content}")
        self.add_messages(AIMessage(content=content))
