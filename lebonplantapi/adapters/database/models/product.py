import enum

from sqlalchemy import Column, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .base import Base


class ProductCategory(enum.Enum):
    BOOKS = enum.auto()
    FERTILIZERS = enum.auto()
    GRAINS = enum.auto()
    INSTALLATIONS = enum.auto()
    TOOLS = enum.auto()


class Product(Base):
    __tablename__ = "product"
    __table_args__ = {"schema": "lebonplantapi"}

    category = Column(Enum(ProductCategory), nullable=False)
    description = Column(String(3000), nullable=True)
    name = Column(String(255), nullable=False)
    picture_link = Column(String(255), nullable=False)
    price = Column(Float(precision=2), nullable=False)
    vendor_id = Column(Integer, ForeignKey("lebonplantapi.user.id"), nullable=False)

    vendor = relationship("User", lazy="joined")
