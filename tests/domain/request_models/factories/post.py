from factory import Factory, Faker

from lebonplantapi.domain.request_models import PostCreation


class PostCreationFactory(Factory):
    class Meta:
        model = PostCreation

    body = Faker("paragraph")
    picture_link = Faker("image_url")
    posted_at = Faker("date_time_this_year")
    title = Faker("sentence")
    author_id = Faker("random_int")
