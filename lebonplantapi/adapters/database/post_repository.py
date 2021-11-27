from typing import List, Optional

from sqlalchemy import select

from lebonplantapi.adapters.database.helpers import db_accessor
from lebonplantapi.adapters.database.mappers import (
    map_from_post_creation,
    map_to_post_entity,
)
from lebonplantapi.adapters.database.models import Post
from lebonplantapi.adapters.database.settings import session
from lebonplantapi.domain import entities
from lebonplantapi.domain.ports import PostRepositoryPort
from lebonplantapi.domain.request_models import PostCreation


class PostRepository(PostRepositoryPort):
    @db_accessor()
    async def list_posts(self) -> List[entities.Post]:
        result = await session.execute(select(Post))
        posts = result.scalars().all()
        post_entities = [map_to_post_entity(post) for post in posts]

        return post_entities

    @db_accessor()
    async def get_post(self, post_id: int) -> Optional[entities.Post]:
        result = await session.execute(select(Post).filter_by(id=post_id))
        post = result.scalar()
        post_entity = map_to_post_entity(post) if post is not None else None

        return post_entity

    @db_accessor(commit=True)
    async def save_post(self, post_creation: PostCreation) -> None:
        post = map_from_post_creation(post_creation)
        session.add(post)
