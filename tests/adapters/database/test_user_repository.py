from random import randint

import pytest

from lebonplantapi.adapters.database import UserRepository

from tests.domain.request_models.factories import UserCreationFactory

from .factories import UserFactory


pytestmark = [
    pytest.mark.asyncio,
    pytest.mark.usefixtures("db"),
]


class TestUserRepository:
    async def test_list_users__ok(self) -> None:
        UserFactory.create_batch(10)

        users = await UserRepository().list_users()

        assert len(users) == 10

    async def test_get_user__ok(self) -> None:
        user_id = randint(0, 626)
        user = UserFactory(id=user_id)

        result = await UserRepository().get_user(user_id)

        assert result is not None
        assert result.id == user_id
        assert result.name == user.name

    async def test_get_user__ko(self) -> None:
        user_id = randint(0, 626)
        UserFactory(id=user_id)

        user = await UserRepository().get_user(user_id + 1)

        assert user is None

    async def test_save_user__ok(self) -> None:
        user_creation = UserCreationFactory()

        await UserRepository().save_user(user_creation)

        users = await UserRepository().list_users()
        assert len(users) == 1
        assert users[0].name == user_creation.name
