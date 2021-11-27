from random import randint
from typing import List
from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient
from pytest_mock import MockerFixture

from lebonplantapi import registry
from lebonplantapi.domain.entities import User

from tests.domain.entities.factories import UserFactory


class TestUserController:
    @pytest.fixture
    def test_user_batch(self) -> List[User]:
        count = randint(1, 45)
        return UserFactory.build_batch(count)

    @pytest.fixture
    def test_user_batch_ids(self, test_user_batch: List[User]) -> List[int]:
        return [user.id for user in test_user_batch]

    @pytest.fixture
    def mock_get_user(
        self,
        test_user_batch: List[User],
        test_user_batch_ids: List[int],
        mocker: MockerFixture,
    ) -> Mock:
        return mocker.patch.object(
            registry.user_repository,
            "get_user",
            side_effect=lambda user_id: test_user_batch[
                test_user_batch_ids.index(user_id)
            ]
            if user_id in test_user_batch_ids
            else None,
        )

    @pytest.fixture
    def mock_list_users(
        self, test_user_batch: List[User], mocker: MockerFixture
    ) -> Mock:
        return mocker.patch.object(
            registry.user_repository,
            "list_users",
            return_value=test_user_batch,
        )

    def test_get_user__ok(
        self,
        client: TestClient,
        test_user_batch: List[User],
        mock_get_user: Mock,
    ) -> None:
        user = test_user_batch[1]
        ret = client.get(f"/lebonplantapi/user/{user.id}")
        content = ret.json()

        assert ret.status_code == 200
        assert content is not None
        assert content["name"] == user.name

    def test_get_user__not_found(
        self,
        client: TestClient,
        test_user_batch: List[User],
        test_user_batch_ids: List[int],
        mock_get_user: Mock,
    ) -> None:
        max_id = sorted(test_user_batch_ids, reverse=True)[0]
        ret = client.get(f"/lebonplantapi/user/{max_id + 4}")

        assert ret.status_code == 404

    def test_list_users__ok(
        self, client: TestClient, test_user_batch: List[User], mock_list_users: Mock
    ) -> None:
        ret = client.get("/lebonplantapi/user")
        content = ret.json()

        assert ret.status_code == 200
        assert content is not None
        assert len(content) == len(test_user_batch)
