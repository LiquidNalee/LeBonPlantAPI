from abc import ABCMeta

from pydantic import BaseModel


class ResponseModel(BaseModel, metaclass=ABCMeta):
    class Config:
        orm_mode = True
        use_enum_values = True


class RequestModel(BaseModel, metaclass=ABCMeta):
    class Config:
        orm_mode = True
        use_enum_values = True
