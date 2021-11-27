from lebonplantapi.domain.entities import Product, ProductCategory, User


class TestProduct:
    def test__ok(self) -> None:
        Product(
            id=1,
            category=ProductCategory.GRAINS,
            description="He ain't no grain, I am the one",
            name="Da Grain",
            picture_link="https://www.picture_of_another_very_rude_grain.plant",
            price=2000000000000000000000.02,
            vendor=User(id=7, name="Jean-Bond"),
        )
