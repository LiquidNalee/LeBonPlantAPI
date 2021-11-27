from random import randint
from typing import List
from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient
from pytest_mock import MockerFixture

from lebonplantapi import registry
from lebonplantapi.domain.entities import Product

from tests.domain.entities.factories import ProductFactory


class TestProductController:
    @pytest.fixture
    def test_product_batch(self) -> List[Product]:
        count = randint(1, 45)
        return ProductFactory.build_batch(count)

    @pytest.fixture
    def test_product_batch_ids(self, test_product_batch: List[Product]) -> List[int]:
        return [product.id for product in test_product_batch]

    @pytest.fixture
    def mock_get_product(
        self,
        test_product_batch: List[Product],
        test_product_batch_ids: List[int],
        mocker: MockerFixture,
    ) -> Mock:
        return mocker.patch.object(
            registry.product_repository,
            "get_product",
            side_effect=lambda product_id: test_product_batch[
                test_product_batch_ids.index(product_id)
            ]
            if product_id in test_product_batch_ids
            else None,
        )

    @pytest.fixture
    def mock_list_products(
        self, test_product_batch: List[Product], mocker: MockerFixture
    ) -> Mock:
        return mocker.patch.object(
            registry.product_repository,
            "list_products",
            return_value=test_product_batch,
        )

    def test_get_product__ok(
        self,
        client: TestClient,
        test_product_batch: List[Product],
        mock_get_product: Mock,
    ) -> None:
        product = test_product_batch[1]
        ret = client.get(f"/lebonplantapi/product/{product.id}")
        content = ret.json()

        assert ret.status_code == 200
        assert content is not None
        assert content["name"] == product.name

    def test_get_product__not_found(
        self,
        client: TestClient,
        test_product_batch: List[Product],
        mock_get_product: Mock,
    ) -> None:
        ret = client.get(f"/lebonplantapi/product/{len(test_product_batch) + 4}")

        assert ret.status_code == 404

    def test_list_products__ok(
        self,
        client: TestClient,
        test_product_batch: List[Product],
        mock_list_products: Mock,
    ) -> None:
        ret = client.get("/lebonplantapi/product")
        content = ret.json()

        assert ret.status_code == 200
        assert content is not None
        assert len(content) == len(test_product_batch)
