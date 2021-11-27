import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from lebonplantapi.adapters.database.mappers import (
    map_from_post_creation,
    map_to_post_entity,
)

from tests.adapters.database.factories import PostFactory, UserFactory
from tests.domain.request_models.factories import PostCreationFactory


pytestmark = [
    pytest.mark.asyncio,
    pytest.mark.usefixtures("db"),
]


class TestMapToPost:
    def test__ok(self) -> None:
        post = PostFactory.build()
        entity = map_to_post_entity(post)

        assert entity is not None
        assert entity.id == post.id
        assert entity.title == post.title


class TestMapFromPostCreation:
    async def test__ok(self, session_autoclose: AsyncSession) -> None:
        post_creation = PostCreationFactory()

        post = map_from_post_creation(post_creation)

        user = UserFactory.build(id=post.author_id)
        session_autoclose.add(user)

        session_autoclose.add(post)
        await session_autoclose.flush()
        await session_autoclose.refresh(post)

        assert post is not None
        assert post.title == post_creation.title
