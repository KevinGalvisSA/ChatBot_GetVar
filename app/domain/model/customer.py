from sqlalchemy import Column, String
from sqlalchemy.dialects.mysql import MEDIUMINT
from app.domain.model.base import Base

class Customer(Base):
    __tablename__ = 'customer'

    id = Column(MEDIUMINT(unsigned=True), primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=True)

    def __repr__(self):
        return f"<Customer(id={self.id}, name='{self.name}', phone='{self.phone}')>"
