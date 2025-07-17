# app/domain/model/messageStorage.py
from sqlalchemy import Column, String
from sqlalchemy.dialects.mysql import INTEGER
from app.domain.model.base import Base

class MessageStorage(Base):
    __tablename__ = 'message_store'

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    id_customer = Column(INTEGER, nullable=False)
    session_id = Column(String(50), nullable=False)
    message = Column(String(1000), nullable=False)
    message_type = Column(String(50), nullable=False)

    def __repr__(self):
        return (
            f"<MessageStorage(id={self.id}, id_customer={self.id_customer}, "
            f"session_id='{self.session_id}', message='{self.message}', "
            f"message_type='{self.message_type}')>"
        )
