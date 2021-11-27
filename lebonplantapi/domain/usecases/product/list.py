from typing import List

from lebonplantapi.domain.entities import Product
from lebonplantapi.domain.ports.product_repository import ProductRepositoryPort


class ListProducts:
    def __init__(self, product_repository: ProductRepositoryPort) -> None:
        self.product_repository = product_repository

    async def execute(self) -> List[Product]:
        products = await self.product_repository.list_products()
        return products
