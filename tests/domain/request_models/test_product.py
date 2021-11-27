from lebonplantapi.domain.request_models import ProductCreation, ProductCreationCategory


class TestProductCreation:
    def test__ok(self) -> None:
        ProductCreation(
            category=ProductCreationCategory.GRAINS,
            description="I am a grain you sunavabitch",
            name="The Rude Grain",
            picture_link="https://www.picture_of_a_very_rude_grain.plant",
            price=2000000000000000000000.01,
            vendor_id=7,
        )
