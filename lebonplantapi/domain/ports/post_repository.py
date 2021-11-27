from abc import ABC, abstractmethod
from typing import List, Optional

from lebonplantapi.domain import entities
from lebonplantapi.domain.request_models import PostCreation


class PostRepositoryPort(ABC):
    @abstractmethod
    async def list_posts(self) -> List[entities.Post]:
        """Return a list of all posts."""
        ...

    @abstractmethod
    async def get_post(self, post_id: int) -> Optional[entities.Post]:
        """Search for a post by id."""
        ...

    @abstractmethod
    async def save_post(self, post: PostCreation) -> None:
        """Add a new post."""
        ...
