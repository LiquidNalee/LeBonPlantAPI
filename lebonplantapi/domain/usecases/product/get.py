from lebonplantapi.domain.entities import Product
from lebonplantapi.domain.errors import ProductNotFoundError
from lebonplantapi.domain.ports.product_repository import ProductRepositoryPort


class GetProduct:
    def __init__(
        self, product_repository: ProductRepositoryPort, product_id: int
    ) -> None:
        self.product_repository = product_repository
        self.product_id = product_id

    async def execute(self) -> Product:
        product = await self.product_repository.get_product(self.product_id)
        if product is None:
            raise ProductNotFoundError()
        return product
