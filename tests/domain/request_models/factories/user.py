from factory import Factory, Faker

from lebonplantapi.domain.request_models import UserCreation


class UserCreationFactory(Factory):
    class Meta:
        model = UserCreation

    name = Faker("name")
