from fastapi import APIRouter, HTTPException
from fastapi.responses import ORJSONResponse

from lebonplantapi.controllers.api.schemas.post import (
    PostCreationRequest,
    PostListResponseModel,
    PostResponseModel,
)
from lebonplantapi.domain.entities import Post
from lebonplantapi.domain.errors import PostNotFoundError
from lebonplantapi.domain.request_models import PostCreation
from lebonplantapi.domain.usecases import ListPosts, SavePost
from lebonplantapi.domain.usecases.post import GetPost
from lebonplantapi.registry import post_repository


router = APIRouter()


@router.get(
    "/post",
    response_class=ORJSONResponse,
    status_code=200,
)
async def list_posts() -> PostListResponseModel:
    """Return all posts."""
    posts = await ListPosts(post_repository).execute()
    post_responses = [PostResponseModel.from_orm(post) for post in posts]
    return PostListResponseModel(content=post_responses)


@router.get(
    "/post/{post_id}",
    response_model=PostResponseModel,
    response_class=ORJSONResponse,
    status_code=200,
)
async def get_post(post_id: int) -> Post:
    """Return a post."""
    try:
        result = await GetPost(post_repository, post_id).execute()
    except PostNotFoundError:
        raise HTTPException(status_code=404, detail="Post not found")
    return result


@router.post(
    "/post",
    response_class=ORJSONResponse,
    status_code=200,
)
async def save_post(post_creation_request: PostCreationRequest) -> None:
    """Add a new post."""
    post_creation = PostCreation(**post_creation_request.dict())
    await SavePost(post_repository, post_creation).execute()
