from abc import ABC, abstractmethod
from typing import List, Optional

from lebonplantapi.domain import entities
from lebonplantapi.domain.request_models import UserCreation


class UserRepositoryPort(ABC):
    @abstractmethod
    async def list_users(self) -> List[entities.User]:
        """Return a list of all users."""
        ...

    @abstractmethod
    async def get_user(self, user_id: int) -> Optional[entities.User]:
        """Search for a user by id."""
        ...

    @abstractmethod
    async def save_user(self, user: UserCreation) -> None:
        """Add a new user."""
        ...
