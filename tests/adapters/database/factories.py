from factory import Faker, Sequence, SubFactory
from factory.alchemy import SQLAlchemyModelFactory
from factory.fuzzy import FuzzyChoice

from lebonplantapi.adapters.database.models import Post, Product, ProductCategory, User
from lebonplantapi.adapters.database.settings import session


class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = session
        sqlalchemy_session_persistence = None

    id = Sequence(int)
    name = Faker("name")


class ProductFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Product
        sqlalchemy_session = session
        sqlalchemy_session_persistence = None

    category = FuzzyChoice(list(ProductCategory))
    description = Faker("paragraph")
    name = Faker("name")
    picture_link = Faker("image_url")
    price = Faker("pyfloat")
    vendor = SubFactory(UserFactory)


class PostFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Post
        sqlalchemy_session = session
        sqlalchemy_session_persistence = None

    body = Faker("paragraph")
    picture_link = Faker("image_url")
    posted_at = Faker("date_time_this_year")
    title = Faker("sentence")
    author = SubFactory(UserFactory)
