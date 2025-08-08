# app/domain/model/stateStorage.py
from sqlalchemy import Column, Integer, String, Text, BigInteger, JSON, Boolean, TIMESTAMP, func
from app.domain.model.base import Base

class StateStorage(Base):
    __tablename__ = "state"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(BigInteger, nullable=False)
    input = Column(Text, nullable=True)
    customer_id = Column(Integer, nullable=True)
    name = Column(String(255), nullable=True)
    phone = Column(BigInteger, nullable=True)
    company = Column(String(255), nullable=True)
    rol = Column(String(255), nullable=True)
    user = Column(Boolean, nullable=False, default=False)
    user_saved = Column(Boolean, nullable=False, default=False)
    context = Column(JSON, nullable=True)
    history_messages = Column(JSON, nullable=True)
    prompt = Column(Text, nullable=True)
    response = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)
    already_sent_solution = Column(Boolean, nullable=False, default=False)
    options_ab_sent = Column(Boolean, nullable=False, default=False)
    already_sent = Column(Boolean, nullable=False, default=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
