from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional


class ProductCreationCategory(Enum):
    BOOKS = auto()
    FERTILIZERS = auto()
    GRAINS = auto()
    INSTALLATIONS = auto()
    TOOLS = auto()


@dataclass
class ProductCreation:
    category: ProductCreationCategory
    description: Optional[str]
    name: str
    picture_link: str
    price: float
    vendor_id: int
