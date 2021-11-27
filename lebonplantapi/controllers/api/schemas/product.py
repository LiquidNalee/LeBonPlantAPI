from lebonplantapi.adapters.helpers.pydantic import GenericModelList
from lebonplantapi.controllers.api.schemas.base import RequestModel, ResponseModel


class ProductResponseModel(ResponseModel):
    id: int
    name: str


class ProductListResponseModel(GenericModelList[ProductResponseModel]):
    ...


class ProductCreationRequest(RequestModel):
    name: str
