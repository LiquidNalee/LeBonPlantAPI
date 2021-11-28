from lebonplantapi.domain.ports.comment_repository import CommentRepositoryPort
from lebonplantapi.domain.request_models.comment import CommentCreation


class SaveComment:
    def __init__(
        self, comment_repository: CommentRepositoryPort, comment: CommentCreation
    ) -> None:
        self.comment_repository = comment_repository
        self.comment = comment

    async def execute(self) -> None:
        await self.comment_repository.save_comment(self.comment)
