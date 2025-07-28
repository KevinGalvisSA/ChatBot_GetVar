from sqlalchemy import INTEGER, Column, String, BigInteger, TIMESTAMP
from sqlalchemy.sql import func
from app.domain.model.base import Base

class Customer(Base):
    __tablename__ = "customer"

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    phone = Column(BigInteger, nullable=False)
    createdBy = Column(INTEGER, nullable=True)
    updatedBy = Column(INTEGER, nullable=True)
    createdAt = Column(TIMESTAMP, nullable=False, server_default=func.now())
    updatedAt = Column(TIMESTAMP, nullable=False, server_default=func.now())
    company = Column(String(100), nullable=True)
    rol = Column(String(100), nullable=True)

    def __repr__(self):
        return f"<Customer(id={self.id}, name='{self.name}', phone='{self.phone}', company='{self.company}', rol='{self.rol}')>"
    