from typing import List

from lebonplantapi.domain.entities import User
from lebonplantapi.domain.ports.user_repository import UserRepositoryPort


class ListUsers:
    def __init__(self, user_repository: UserRepositoryPort) -> None:
        self.user_repository = user_repository

    async def execute(self) -> List[User]:
        users = await self.user_repository.list_users()
        return users
