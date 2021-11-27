from datetime import datetime

from lebonplantapi.domain.entities import Post, User


class TestPost:
    def test__ok(self) -> None:
        Post(
            id=1,
            body="This is fine.",
            picture_link="https://www.google.com/?search=picture_of_dog_on_fire",
            posted_at=datetime.now(),
            title="I am fine",
            author=User(id=45, name="Covfefe loving dog"),
        )
