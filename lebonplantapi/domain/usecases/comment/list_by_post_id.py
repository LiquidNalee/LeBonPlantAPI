from typing import List

from lebonplantapi.domain.entities import Comment
from lebonplantapi.domain.ports.comment_repository import CommentRepositoryPort


class ListCommentsByPostID:
    def __init__(self, comment_repository: CommentRepositoryPort, post_id: int) -> None:
        self.comment_repository = comment_repository
        self.post_id = post_id

    async def execute(self) -> List[Comment]:
        comments = await self.comment_repository.list_comments_by_post_id(
            post_id=self.post_id
        )
        return comments
