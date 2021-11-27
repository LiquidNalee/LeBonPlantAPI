from lebonplantapi.adapters.helpers.pydantic import GenericModelList
from lebonplantapi.controllers.api.schemas.base import RequestModel, ResponseModel


class UserResponseModel(ResponseModel):
    id: int
    name: str


class UserListResponseModel(GenericModelList[UserResponseModel]):
    ...


class UserCreationRequest(RequestModel):
    name: str
