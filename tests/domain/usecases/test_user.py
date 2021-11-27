from random import randint
from unittest.mock import Mock, call

import pytest

from lebonplantapi.adapters.database import UserRepository
from lebonplantapi.domain.errors import UserNotFoundError
from lebonplantapi.domain.usecases import GetUser, ListUsers

from tests.domain.entities.factories import UserFactory


pytestmark = pytest.mark.asyncio


class TestUserUseCases:
    @pytest.fixture
    def mock_user_repository(self) -> Mock:
        return Mock(spec=UserRepository)

    async def test_list_users__ok(self, mock_user_repository: Mock) -> None:
        users = UserFactory.build_batch(10)
        mock_user_repository.list_users.return_value = users

        users_result = await ListUsers(mock_user_repository).execute()
        assert users_result == users

    async def test_get_user__ok(self, mock_user_repository: Mock) -> None:
        user_id = randint(0, 626)

        await GetUser(mock_user_repository, user_id).execute()

        assert mock_user_repository.get_user.call_args_list == [call(user_id)]

    async def test_get_user__not_found(self, mock_user_repository: Mock) -> None:
        mock_user_repository.get_user.return_value = None

        with pytest.raises(UserNotFoundError):
            await GetUser(mock_user_repository, 626).execute()
