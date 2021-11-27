from lebonplantapi.domain import entities
from lebonplantapi.domain.request_models import PostCreation

from ..models.post import Post
from .user import map_to_user_entity


def map_to_post_entity(post: Post) -> entities.Post:
    return entities.Post(
        author=map_to_user_entity(post.author),
        body=post.body,
        id=post.id,
        picture_link=post.picture_link,
        posted_at=post.posted_at,
        title=post.title,
    )


def map_from_post_creation(post: PostCreation) -> Post:
    return Post(
        author_id=post.author_id,
        body=post.body,
        picture_link=post.picture_link,
        posted_at=post.posted_at,
        title=post.title,
    )
