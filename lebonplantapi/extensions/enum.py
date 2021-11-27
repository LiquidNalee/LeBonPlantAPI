from abc import abstractmethod
from enum import Enum
from typing import Any, Callable, Generator


class AutoNamedEnum(str, Enum):
    def _generate_next_value_(  # type: ignore
        name, start, count, last_values  # noqa: N805
    ):
        return name

    @classmethod
    def __get_validators__(cls) -> Generator[Callable, None, None]:
        yield cls.validate

    @classmethod
    @abstractmethod
    def validate(cls, v: Any) -> Any:
        ...
