from factory import Factory, Faker, Sequence, SubFactory
from factory.fuzzy import FuzzyChoice

from lebonplantapi.domain.entities import Product, ProductCategory

from .user import UserFactory


class ProductFactory(Factory):
    class Meta:
        model = Product

    category = FuzzyChoice(list(ProductCategory))
    description = Faker("paragraph")
    id = Sequence(int)
    name = Faker("name")
    picture_link = Faker("image_url")
    price = Faker("pyfloat")
    vendor = SubFactory(UserFactory)
