from enum import auto
from typing import Optional

from lebonplantapi.adapters.helpers.pydantic import GenericModelList
from lebonplantapi.controllers.api.schemas.base import RequestModel, ResponseModel
from lebonplantapi.controllers.api.schemas.user import UserResponseModel
from lebonplantapi.domain import entities
from lebonplantapi.extensions.enum import AutoNamedEnum


class ProductResponseModelCategory(AutoNamedEnum):
    BOOKS = auto()
    FERTILIZERS = auto()
    GRAINS = auto()
    INSTALLATIONS = auto()
    TOOLS = auto()

    @classmethod
    def validate(cls, v: entities.ProductCategory) -> "ProductResponseModelCategory":
        if not isinstance(v, entities.ProductCategory):
            raise TypeError("value is not a valid entities.ProductCategory")
        return cls(v.name)


class ProductResponseModel(ResponseModel):
    category: ProductResponseModelCategory
    description: Optional[str]
    id: int
    name: str
    picture_link: str
    price: float
    vendor: UserResponseModel


class ProductListResponseModel(GenericModelList[ProductResponseModel]):
    ...


class ProductCreationRequestCategory(AutoNamedEnum):
    BOOKS = auto()
    FERTILIZERS = auto()
    GRAINS = auto()
    INSTALLATIONS = auto()
    TOOLS = auto()

    @classmethod
    def validate(cls, v: str) -> "ProductCreationRequestCategory":
        if not isinstance(v, str):
            raise TypeError("value is not a valid str")
        return cls(v)


class ProductCreationRequest(RequestModel):
    category: ProductCreationRequestCategory
    description: Optional[str]
    name: str
    picture_link: str
    price: float
    vendor_id: int
