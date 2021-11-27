from random import randint

import pytest

from lebonplantapi.adapters.database import ProductRepository

from tests.domain.request_models.factories import ProductCreationFactory

from .factories import ProductFactory, UserFactory

pytestmark = [
    pytest.mark.asyncio,
    pytest.mark.usefixtures("db"),
]


class TestProductRepository:
    async def test_list_products__ok(self) -> None:
        ProductFactory.create_batch(10)

        products = await ProductRepository().list_products()

        assert len(products) == 10

    async def test_get_product__ok(self) -> None:
        product_id = randint(0, 626)
        product = ProductFactory(id=product_id)

        result = await ProductRepository().get_product(product_id)

        assert result is not None
        assert result.id == product_id
        assert result.name == product.name

    async def test_get_product__ko(self) -> None:
        product_id = randint(0, 626)
        ProductFactory(id=product_id)

        product = await ProductRepository().get_product(product_id + 1)

        assert product is None

    async def test_save_product__ok(self) -> None:
        product_creation = ProductCreationFactory()
        UserFactory(id=product_creation.vendor_id)

        await ProductRepository().save_product(product_creation)

        products = await ProductRepository().list_products()
        assert len(products) == 1
        assert products[0].name == product_creation.name
