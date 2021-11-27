from lebonplantapi.domain.entities import User
from lebonplantapi.domain.errors import UserNotFoundError
from lebonplantapi.domain.ports.user_repository import UserRepositoryPort


class GetUser:
    def __init__(self, user_repository: UserRepositoryPort, user_id: int) -> None:
        self.user_repository = user_repository
        self.user_id = user_id

    async def execute(self) -> User:
        user = await self.user_repository.get_user(self.user_id)
        if user is None:
            raise UserNotFoundError()
        return user
