from typing import Generator, Generic, List, TypeVar

from pydantic import BaseModel
from pydantic.generics import GenericModel


ElmType = TypeVar("ElmType", bound=BaseModel)


class GenericModelList(GenericModel, Generic[ElmType]):
    __root__: List[ElmType]

    def __init__(self, content: List[ElmType]):
        super().__init__(__root__=content)

    def __iter__(self) -> Generator:
        yield from self.__root__
