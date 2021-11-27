import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from lebonplantapi.adapters.database.models import Product, ProductCategory, User


pytestmark = [
    pytest.mark.asyncio,
    pytest.mark.usefixtures("db"),
]


class TestProduct:
    async def test_ok(self, session_autoclose: AsyncSession) -> None:
        product = Product(
            category=ProductCategory.GRAINS,
            description=None,
            name="New root, Who dis ?",
            picture_link="http://www.onlyfans.com/germinating",
            price=9.99,
            vendor=User(id=5, name="Germinating"),
        )
        session_autoclose.add(product)
        await session_autoclose.flush()
