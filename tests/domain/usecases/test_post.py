from random import randint
from unittest.mock import Mock, call

import pytest

from lebonplantapi.adapters.database import PostRepository
from lebonplantapi.domain.errors import PostNotFoundError
from lebonplantapi.domain.usecases import GetPost, ListPosts

from tests.domain.entities.factories import PostFactory


pytestmark = pytest.mark.asyncio


class TestPostUseCases:
    @pytest.fixture
    def mock_post_repository(self) -> Mock:
        return Mock(spec=PostRepository)

    async def test_list_posts__ok(self, mock_post_repository: Mock) -> None:
        posts = PostFactory.build_batch(10)
        mock_post_repository.list_posts.return_value = posts

        posts_result = await ListPosts(mock_post_repository).execute()
        assert posts_result == posts

    async def test_get_post__ok(self, mock_post_repository: Mock) -> None:
        post_id = randint(0, 626)

        await GetPost(mock_post_repository, post_id).execute()

        assert mock_post_repository.get_post.call_args_list == [call(post_id)]

    async def test_get_post__not_found(self, mock_post_repository: Mock) -> None:
        mock_post_repository.get_post.return_value = None

        with pytest.raises(PostNotFoundError):
            await GetPost(mock_post_repository, 626).execute()
