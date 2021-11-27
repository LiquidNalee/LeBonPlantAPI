from fastapi import APIRouter, HTTPException
from fastapi.responses import ORJSONResponse

from lebonplantapi.controllers.api.schemas.user import (
    UserCreationRequest,
    UserListResponseModel,
    UserResponseModel,
)
from lebonplantapi.domain.entities import User
from lebonplantapi.domain.errors import UserNotFoundError
from lebonplantapi.domain.request_models import UserCreation
from lebonplantapi.domain.usecases import ListUsers, SaveUser
from lebonplantapi.domain.usecases.user import GetUser
from lebonplantapi.registry import user_repository


router = APIRouter()


@router.get(
    "/user",
    response_class=ORJSONResponse,
    status_code=200,
)
async def list_users() -> UserListResponseModel:
    """Return all users."""
    users = await ListUsers(user_repository).execute()
    user_responses = [UserResponseModel.from_orm(user) for user in users]
    return UserListResponseModel(content=user_responses)


@router.get(
    "/user/{user_id}",
    response_model=UserResponseModel,
    response_class=ORJSONResponse,
    status_code=200,
)
async def get_user(user_id: int) -> User:
    """Return a user."""
    try:
        result = await GetUser(user_repository, user_id).execute()
    except UserNotFoundError:
        raise HTTPException(status_code=404, detail="User not found")
    return result


@router.post(
    "/user",
    response_class=ORJSONResponse,
    status_code=200,
)
async def save_user(user_creation_request: UserCreationRequest) -> None:
    """Add a new user."""
    user_creation = UserCreation(**user_creation_request.dict())
    await SaveUser(user_repository, user_creation).execute()
