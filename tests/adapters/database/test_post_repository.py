from random import randint

import pytest

from lebonplantapi.adapters.database import PostRepository

from tests.domain.request_models.factories import PostCreationFactory

from .factories import PostFactory, UserFactory


pytestmark = [
    pytest.mark.asyncio,
    pytest.mark.usefixtures("db"),
]


class TestPostRepository:
    async def test_list_posts__ok(self) -> None:
        PostFactory.create_batch(10)

        posts = await PostRepository().list_posts()

        assert len(posts) == 10

    async def test_get_post__ok(self) -> None:
        post_id = randint(0, 626)
        post = PostFactory(id=post_id)

        result = await PostRepository().get_post(post_id)

        assert result is not None
        assert result.id == post_id
        assert result.title == post.title

    async def test_get_post__ko(self) -> None:
        post_id = randint(0, 626)
        PostFactory(id=post_id)

        post = await PostRepository().get_post(post_id + 1)

        assert post is None

    async def test_save_post__ok(self) -> None:
        post_creation = PostCreationFactory()
        UserFactory(id=post_creation.author_id)

        await PostRepository().save_post(post_creation)

        posts = await PostRepository().list_posts()
        assert len(posts) == 1
        assert posts[0].title == post_creation.title
