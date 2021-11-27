import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from lebonplantapi.adapters.database.models import User


pytestmark = [
    pytest.mark.asyncio,
    pytest.mark.usefixtures("db"),
]


class TestUser:
    async def test_ok(self, session_autoclose: AsyncSession) -> None:
        user = User(name="Jean-Christophe")
        session_autoclose.add(user)
        await session_autoclose.flush()
