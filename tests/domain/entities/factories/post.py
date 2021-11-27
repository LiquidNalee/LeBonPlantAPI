from factory import Factory, Faker, Sequence, SubFactory

from lebonplantapi.domain.entities import Post

from .user import UserFactory


class PostFactory(Factory):
    class Meta:
        model = Post

    body = Faker("paragraph")
    picture_link = Faker("image_url")
    posted_at = Faker("date_time_this_year")
    id = Sequence(int)
    title = Faker("sentence")
    author = SubFactory(UserFactory)
