import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from lebonplantapi.adapters.database.mappers import (
    map_from_user_creation,
    map_to_user_entity,
)

from tests.adapters.database.factories import UserFactory
from tests.domain.request_models.factories import UserCreationFactory


pytestmark = [
    pytest.mark.asyncio,
    pytest.mark.usefixtures("db"),
]


class TestMapToUser:
    def test__ok(self) -> None:
        user = UserFactory.build()
        entity = map_to_user_entity(user)

        assert entity is not None
        assert entity.id == user.id
        assert entity.name == user.name


class TestMapFromUserCreation:
    async def test__ok(self, session_autoclose: AsyncSession) -> None:
        user_creation = UserCreationFactory()
        user = map_from_user_creation(user_creation)

        session_autoclose.add(user)
        await session_autoclose.flush()
        await session_autoclose.refresh(user)

        assert user is not None
        assert user.name == user_creation.name
