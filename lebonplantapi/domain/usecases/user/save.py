from lebonplantapi.domain.ports.user_repository import UserRepositoryPort
from lebonplantapi.domain.request_models.user import UserCreation


class SaveUser:
    def __init__(self, user_repository: UserRepositoryPort, user: UserCreation) -> None:
        self.user_repository = user_repository
        self.user = user

    async def execute(self) -> None:
        await self.user_repository.save_user(self.user)
