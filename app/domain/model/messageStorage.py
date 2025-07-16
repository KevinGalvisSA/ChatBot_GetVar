from sqlalchemy.dialects.mysql import MEDIUMINT
from sqlalchemy import Column, BigInteger, Text, ForeignKey, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class MessageStorage(Base):
    __tablename__ = "messageStorage"

    id = Column(MEDIUMINT(unsigned=True), primary_key=True, autoincrement=True)
    id_customer = Column(MEDIUMINT(unsigned=True), ForeignKey("customer.id"), nullable=False)
    session_id = Column(BigInteger, nullable=False)
    message = Column(Text, nullable=False)
    type = Column(String(20), nullable=False)  # 👈 Añadir esta columna obligatoriamente
