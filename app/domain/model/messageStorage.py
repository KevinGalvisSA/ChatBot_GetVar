# app/domain/model/messageStorage.py
from sqlalchemy import Column, Enum, String, Text
from sqlalchemy.dialects.mysql import INTEGER
from app.domain.model.base import Base

class MessageStorage(Base):
    __tablename__ = 'messageStorage'

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    id_customer = Column(INTEGER, nullable=False)
    session_id = Column(String(50), nullable=False, index=True)
    message = Column(Text, nullable=False)  # Texto real del mensaje
    message_type = Column(Enum('human', 'ai', name='message_type_enum'), nullable=False)  # Tipo de mensaje

    def __repr__(self):
        return (
            f"<MessageStorage(id={self.id}, id_customer={self.id_customer}, "
            f"session_id='{self.session_id}', message='{self.message}', "
            f"message_type='{self.message_type}')>"
        )
