
from sqlalchemy import INTEGER, Column, String, BigInteger, TIMESTAMP

# from sqlalchemy.dialects.mysql import MEDIUMINT
from app.domain.model.base import Base


class Customer(Base):
    __tablename__ = "customer"

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    phone_number = Column(BigInteger, nullable=False)
    createdBy = Column(INTEGER)
    updatedBy = Column(INTEGER)
    createdAt = Column(TIMESTAMP, nullable=False)
    updatedAt = Column(TIMESTAMP, nullable=False)


    def __repr__(self):
        return f"<Customer(id={self.id}, name='{self.name}', phone='{self.phone}')>"
