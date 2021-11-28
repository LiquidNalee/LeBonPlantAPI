from lebonplantapi.domain import entities
from lebonplantapi.domain.request_models import CommentCreation

from ..models.comment import Comment
from .user import map_to_user_entity


def map_to_comment_entity(comment: Comment) -> entities.Comment:
    return entities.Comment(
        author=map_to_user_entity(comment.author),
        body=comment.body,
        id=comment.id,
        posted_at=comment.posted_at,
        post=map_to_comment_entity(comment.post),
    )


def map_from_comment_creation(comment: CommentCreation) -> Comment:
    return Comment(
        author_id=comment.author_id,
        body=comment.body,
        id=comment.id,
        posted_at=comment.posted_at,
        post_id=comment.post_id,
    )
