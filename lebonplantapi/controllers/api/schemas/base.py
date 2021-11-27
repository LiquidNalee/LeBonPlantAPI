from abc import ABCMeta

from pydantic import BaseModel


class ResponseModel(BaseModel, metaclass=ABCMeta):
    class Config:
        orm_mode = True
