from random import randint
from unittest.mock import Mock, call

import pytest

from lebonplantapi.adapters.database.product_repository import ProductRepository
from lebonplantapi.domain.errors import ProductNotFoundError
from lebonplantapi.domain.usecases.product.get import GetProduct
from lebonplantapi.domain.usecases.product.list import ListProducts

from tests.domain.entities.factories import ProductFactory


pytestmark = pytest.mark.asyncio


class TestProductUseCases:
    @pytest.fixture
    def mock_product_repository(self) -> Mock:
        return Mock(spec=ProductRepository)

    async def test_list_products__ok(self, mock_product_repository: Mock) -> None:
        products = ProductFactory.build_batch(10)
        mock_product_repository.list_products.return_value = products

        products_result = await ListProducts(mock_product_repository).execute()
        assert products_result == products

    async def test_get_product__ok(self, mock_product_repository: Mock) -> None:
        product_id = randint(0, 626)

        await GetProduct(mock_product_repository, product_id).execute()

        assert mock_product_repository.get_product.call_args_list == [call(product_id)]

    async def test_get_product__not_found(self, mock_product_repository: Mock) -> None:
        mock_product_repository.get_product.return_value = None

        with pytest.raises(ProductNotFoundError):
            await GetProduct(mock_product_repository, 626).execute()
