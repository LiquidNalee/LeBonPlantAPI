from lebonplantapi.domain.ports.post_repository import PostRepositoryPort
from lebonplantapi.domain.request_models.post import PostCreation


class SavePost:
    def __init__(self, post_repository: PostRepositoryPort, post: PostCreation) -> None:
        self.post_repository = post_repository
        self.post = post

    async def execute(self) -> None:
        await self.post_repository.save_post(self.post)
