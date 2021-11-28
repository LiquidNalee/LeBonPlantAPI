from abc import ABC, abstractmethod
from typing import List

from lebonplantapi.domain import entities
from lebonplantapi.domain.request_models import CommentCreation


class CommentRepositoryPort(ABC):
    @abstractmethod
    async def list_comments_by_post_id(self, post_id: int) -> List[entities.Comment]:
        """Return a list of all comments."""
        ...

    @abstractmethod
    async def save_comment(self, comment: CommentCreation) -> None:
        """Add a new comment."""
        ...
