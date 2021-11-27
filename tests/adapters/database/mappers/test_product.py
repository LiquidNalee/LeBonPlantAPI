import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from lebonplantapi.adapters.database.mappers import (
    map_from_product_creation,
    map_to_product_entity,
)

from tests.adapters.database.factories import ProductFactory, UserFactory
from tests.domain.request_models.factories import ProductCreationFactory


pytestmark = [
    pytest.mark.asyncio,
    pytest.mark.usefixtures("db"),
]


class TestMapToProduct:
    def test__ok(self) -> None:
        product = ProductFactory.build()
        entity = map_to_product_entity(product)

        assert entity is not None
        assert entity.id == product.id
        assert entity.name == product.name


class TestMapFromProductCreation:
    async def test__ok(self, session_autoclose: AsyncSession) -> None:
        product_creation = ProductCreationFactory()

        product = map_from_product_creation(product_creation)

        user = UserFactory.build(id=product.vendor_id)
        session_autoclose.add(user)

        session_autoclose.add(product)
        await session_autoclose.flush()
        await session_autoclose.refresh(product)

        assert product is not None
        assert product.name == product_creation.name
