from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional

from lebonplantapi.domain.entities import User


class ProductCategory(Enum):
    BOOKS = auto()
    FERTILIZERS = auto()
    GRAINS = auto()
    INSTALLATIONS = auto()
    TOOLS = auto()


@dataclass
class Product:
    category: ProductCategory
    description: Optional[str]
    id: int
    name: str
    picture_link: str
    price: float
    vendor: User
