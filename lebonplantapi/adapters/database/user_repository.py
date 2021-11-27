from typing import List, Optional

from sqlalchemy import select

from lebonplantapi.adapters.database.helpers import db_accessor
from lebonplantapi.adapters.database.mappers import (
    map_from_user_creation,
    map_to_user_entity,
)
from lebonplantapi.adapters.database.models import User
from lebonplantapi.adapters.database.settings import session
from lebonplantapi.domain import entities
from lebonplantapi.domain.ports import UserRepositoryPort
from lebonplantapi.domain.request_models import UserCreation


class UserRepository(UserRepositoryPort):
    @db_accessor()
    async def list_users(self) -> List[entities.User]:
        result = await session.execute(select(User))
        users = result.scalars().all()
        user_entities = [map_to_user_entity(user) for user in users]

        return user_entities

    @db_accessor()
    async def get_user(self, user_id: int) -> Optional[entities.User]:
        result = await session.execute(select(User).filter_by(id=user_id))
        user = result.scalar()
        user_entity = map_to_user_entity(user) if user is not None else None

        return user_entity

    @db_accessor(commit=True)
    async def save_user(self, user_creation: UserCreation) -> None:
        user = map_from_user_creation(user_creation)
        session.add(user)
