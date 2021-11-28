from fastapi import APIRouter, HTTPException
from fastapi.responses import ORJSONResponse

from lebonplantapi.controllers.api.schemas.comment import (
    CommentCreationRequest,
    CommentListResponseModel,
    CommentResponseModel,
)
from lebonplantapi.domain.entities import Comment
from lebonplantapi.domain.errors import CommentNotFoundError
from lebonplantapi.domain.request_models import CommentCreation
from lebonplantapi.domain.usecases import ListComments, SaveComment
from lebonplantapi.domain.usecases.comment import GetComment
from lebonplantapi.registry import comment_repository


router = APIRouter()


@router.get(
    "/comment/{comment_id}",
    response_model=CommentResponseModel,
    response_class=ORJSONResponse,
    status_code=200,
)
async def get_comment(comment_id: int) -> Comment:
    """Return a comment."""
    try:
        result = await GetComment(comment_repository, comment_id).execute()
    except CommentNotFoundError:
        raise HTTPException(status_code=404, detail="Comment not found")
    return result


@router.post(
    "/comment",
    response_class=ORJSONResponse,
    status_code=200,
)
async def save_comment(comment_creation_request: CommentCreationRequest) -> None:
    """Add a new comment."""
    comment_creation = CommentCreation(**comment_creation_request.dict())
    await SaveComment(comment_repository, comment_creation).execute()
