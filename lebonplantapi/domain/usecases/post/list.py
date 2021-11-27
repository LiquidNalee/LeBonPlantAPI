from typing import List

from lebonplantapi.domain.entities import Post
from lebonplantapi.domain.ports.post_repository import PostRepositoryPort


class ListPosts:
    def __init__(self, post_repository: PostRepositoryPort) -> None:
        self.post_repository = post_repository

    async def execute(self) -> List[Post]:
        posts = await self.post_repository.list_posts()
        return posts
