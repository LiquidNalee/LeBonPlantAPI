from abc import ABC, abstractmethod
from typing import List, Optional

from lebonplantapi.domain import entities
from lebonplantapi.domain.request_models.product import ProductCreation


class ProductRepositoryPort(ABC):
    @abstractmethod
    async def list_products(self) -> List[entities.Product]:
        """Return a list of all products."""
        ...

    @abstractmethod
    async def get_product(self, product_id: int) -> Optional[entities.Product]:
        """Search for a product by id."""
        ...

    @abstractmethod
    async def save_product(self, product: ProductCreation) -> None:
        """Add a new product."""
        ...
