from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional

from lebonplantapi.controllers.api.schemas.product import ProductCreationRequest


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

    @classmethod
    def from_request(cls, request: ProductCreationRequest) -> "ProductCreation":
        args = request.dict()
        args.update({"category": ProductCreationCategory[request.category.value]})
        product_creation = ProductCreation(**args)
        return product_creation
