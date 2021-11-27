from datetime import datetime

from lebonplantapi.adapters.helpers.pydantic import GenericModelList
from lebonplantapi.controllers.api.schemas.base import RequestModel, ResponseModel
from lebonplantapi.controllers.api.schemas.user import UserResponseModel


class PostResponseModel(ResponseModel):
    body: str
    picture_link: str
    posted_at: datetime
    title: str
    author: UserResponseModel


class PostListResponseModel(GenericModelList[PostResponseModel]):
    ...


class PostCreationRequest(RequestModel):
    body: str
    picture_link: str
    posted_at: datetime
    title: str
    author_id: int
