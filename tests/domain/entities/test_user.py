from lebonplantapi.domain.entities import User


class TestUser:
    def test__ok(self) -> None:
        User(id=1, name="Jean-Michel")
