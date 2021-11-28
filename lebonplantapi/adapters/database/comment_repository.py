from typing import List

from sqlalchemy import select

from lebonplantapi.adapters.database.helpers import db_accessor
from lebonplantapi.adapters.database.mappers import (
    map_from_comment_creation,
    map_to_comment_entity,
)
from lebonplantapi.adapters.database.models import Comment
from lebonplantapi.adapters.database.settings import session
from lebonplantapi.domain import entities
from lebonplantapi.domain.ports import CommentRepositoryPort
from lebonplantapi.domain.request_models import CommentCreation


class CommentRepository(CommentRepositoryPort):
    @db_accessor()
    async def list_comments_by_post_id(self, post_id: int) -> List[entities.Comment]:
        result = await session.execute(select(Comment).filter_by(post_id=post_id))
        comments = result.scalars().all()
        comment_entities = [map_to_comment_entity(comment) for comment in comments]

        return comment_entities

    @db_accessor(commit=True)
    async def save_comment(self, comment_creation: CommentCreation) -> None:
        comment = map_from_comment_creation(comment_creation)
        session.add(comment)
