from factory import Factory, Faker, Sequence

from lebonplantapi.domain.entities import User


class UserFactory(Factory):
    class Meta:
        model = User

    id = Sequence(int)
    name = Faker("name")
