from sqlalchemy import Column, String

from .base import Base


class User(Base):
    __tablename__ = "user"
    __table_args__ = {"schema": "lebonplantapi"}

    name = Column(String(50), nullable=False)
