from lebonplantapi.domain.entities import Post
from lebonplantapi.domain.errors import PostNotFoundError
from lebonplantapi.domain.ports.post_repository import PostRepositoryPort


class GetPost:
    def __init__(self, post_repository: PostRepositoryPort, post_id: int) -> None:
        self.post_repository = post_repository
        self.post_id = post_id

    async def execute(self) -> Post:
        post = await self.post_repository.get_post(self.post_id)
        if post is None:
            raise PostNotFoundError()
        return post
