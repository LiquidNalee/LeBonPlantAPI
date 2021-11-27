from random import randint
from typing import List
from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient
from pytest_mock import MockerFixture

from lebonplantapi import registry
from lebonplantapi.domain.entities import Post

from tests.domain.entities.factories import PostFactory


class TestPostController:
    @pytest.fixture
    def test_post_batch(self) -> List[Post]:
        count = randint(1, 45)
        return PostFactory.build_batch(count)

    @pytest.fixture
    def test_post_batch_ids(self, test_post_batch: List[Post]) -> List[int]:
        return [post.id for post in test_post_batch]

    @pytest.fixture
    def mock_get_post(
        self,
        test_post_batch: List[Post],
        test_post_batch_ids: List[int],
        mocker: MockerFixture,
    ) -> Mock:
        return mocker.patch.object(
            registry.post_repository,
            "get_post",
            side_effect=lambda post_id: test_post_batch[
                test_post_batch_ids.index(post_id)
            ]
            if post_id in test_post_batch_ids
            else None,
        )

    @pytest.fixture
    def mock_list_posts(
        self, test_post_batch: List[Post], mocker: MockerFixture
    ) -> Mock:
        return mocker.patch.object(
            registry.post_repository,
            "list_posts",
            return_value=test_post_batch,
        )

    def test_get_post__ok(
        self,
        client: TestClient,
        test_post_batch: List[Post],
        mock_get_post: Mock,
    ) -> None:
        post = test_post_batch[0]
        ret = client.get(f"/lebonplantapi/post/{post.id}")
        content = ret.json()

        assert ret.status_code == 200
        assert content is not None
        assert content["title"] == post.title

    def test_get_post__not_found(
        self,
        client: TestClient,
        test_post_batch: List[Post],
        test_post_batch_ids: List[int],
        mock_get_post: Mock,
    ) -> None:
        max_id = sorted(test_post_batch_ids, reverse=True)[0]
        ret = client.get(f"/lebonplantapi/post/{max_id + 4}")

        assert ret.status_code == 404

    def test_list_posts__ok(
        self,
        client: TestClient,
        test_post_batch: List[Post],
        mock_list_posts: Mock,
    ) -> None:
        ret = client.get("/lebonplantapi/post")
        content = ret.json()

        assert ret.status_code == 200
        assert content is not None
        assert len(content) == len(test_post_batch)
