from factory import Factory, Faker
from factory.fuzzy import FuzzyChoice

from lebonplantapi.domain.request_models import ProductCreation, ProductCreationCategory


class ProductCreationFactory(Factory):
    class Meta:
        model = ProductCreation

    category = FuzzyChoice(list(ProductCreationCategory))
    description = Faker("paragraph")
    name = Faker("name")
    picture_link = Faker("image_url")
    price = Faker("pyfloat")
    vendor_id = Faker("random_int")
