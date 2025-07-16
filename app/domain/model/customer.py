from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import MEDIUMINT

id = Column(MEDIUMINT(unsigned=True), primary_key=True, autoincrement=True)


Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customer'

    id = Column(MEDIUMINT, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=True)

    def __repr__(self):
        return f"<Customer(id={self.id}, name='{self.name}', phone='{self.phone}')>"
