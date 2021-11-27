from factory import Factory, Faker

from lebonplantapi.domain.entities import User


class UserFactory(Factory):
    class Meta:
        model = User

    id = Faker("random_int")
    name = Faker("name")
