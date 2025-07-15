from time import sleep
from typing import Callable, List, TypeVar
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import OperationalError
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage
from langchain_community.chat_message_histories import SQLChatMessageHistory

import os

load_dotenv(override=True)

Kai_Agent_DB = os.getenv("DB_HOST")

engine = create_engine(
        Kai_Agent_DB,
        pool_recycle=600,
        pool_pre_ping=True
)

T = TypeVar('T')

def execute_try(func: Callable[[], T], max_retries: int = 3) -> T:
        """
        Ejecuta una función que reinta en el caso hay un error en la conexión.

        Args:
                func: Función que desea ejecutar.
                max_retries: Número máximos de intentos.

        Returns:
                Resultado de la función si tiene éxito.
        Raises:
                OperationalError: Si todos los intentos fallan.

        """
        retries = 0
        last_error = None

        while retries < max_retries:
                try:
                        return func()
                except OperationalError as e:
                        last_error = e 
                        if  "MySQL server has gone away" in str(e) and retries < max_retries - 1:
                                retries +=1 
                                sleep(1 * retries)
                                print(f"Reitando conexión a la base de datos (intento {retries}/{max_retries})")  
                                continue
                raise e
        raise last_error        

class ChatMessageHistory(SQLChatMessageHistory):
        def __init__(self, session_id, limit=15, connection=engine):
                super().__init__(session_id=session_id, connection=connection)
                self.session_id = session_id
                self.connection = connection
                self.limit = limit

        @property
        def message(self) -> List[BaseMessage]:
                """Retrieve all messages from db with retry mechanism""" 
                def get_messages_db():
                        with self._make_sync_session() as session:
                                result = (
                                        session.query(self.sql_model_class)
                                        .where (
                                                getattr(self.sql_model_class.id.desc(), self.session_id_field_name)
                                                == self.session_id
                                        )
                                        .order_by(self.sql_model_class.id.desc()).limit(self.limit)
                                )
                                messages = []
                                for record in result:
                                        messages.append(self.converter.from_sql_model(record))
                                        return messages[::-1]
                
                        return execute_try(get_messages_db)
        
        def get_messages(self) -> List[BaseMessage]:
                return self.messages
        def add_messages(self, message: BaseMessage) -> None:
                """ Appen the message to the record in db with retry mechanism. """
                def add_message_db():
                        with self._make_async_session() as session:
                                session.add(self.converter.to_sql_model(message, self.session_id))
                                session.commit()
                        return None
                execute_try(add_message_db)

        def user_message_db(self, message: BaseMessage) -> None:
         """Add a user message to the store with the retry mechanism."""
         self.add_messages(message)
        
        def ai_message_db(self, message: BaseMessage) -> None:
                """ Add a AI message to the store with the retry mechanism. """
                self.add_message(message)

