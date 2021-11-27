from datetime import datetime

from lebonplantapi.domain.request_models import PostCreation


class TestPostCreation:
    def test__ok(self) -> None:
        PostCreation(
            body="This is fine.",
            picture_link="https://www.google.com/?search=picture_of_dog_on_fire",
            posted_at=datetime.now(),
            title="I am fine",
            author_id=45,
        )
