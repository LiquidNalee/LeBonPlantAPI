from lebonplantapi.domain import entities
from lebonplantapi.domain.request_models import UserCreation

from ..models.user import User


def map_to_user_entity(user: User) -> entities.User:
    return entities.User(
        id=user.id,
        name=user.name,
    )


def map_from_user_creation(user: UserCreation) -> User:
    return User(name=user.name)
