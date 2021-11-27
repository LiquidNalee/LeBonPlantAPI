from lebonplantapi.domain.ports.product_repository import ProductRepositoryPort
from lebonplantapi.domain.request_models.product import ProductCreation


class SaveProduct:
    def __init__(
        self, product_repository: ProductRepositoryPort, product: ProductCreation
    ) -> None:
        self.product_repository = product_repository
        self.product = product

    async def execute(self) -> None:
        await self.product_repository.save_product(self.product)
