from lebonplantapi.domain.request_models import UserCreation


class TestUserCreation:
    def test__ok(self) -> None:
        UserCreation(name="Jean-Pierre")
