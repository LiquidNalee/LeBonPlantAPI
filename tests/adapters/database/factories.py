from factory import Faker, Sequence
from factory.alchemy import SQLAlchemyModelFactory

from lebonplantapi.adapters.database.models import User
from lebonplantapi.adapters.database.settings import session


class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = session
        sqlalchemy_session_persistence = None

    id = Sequence(int)
    name = Faker("name")
