from lebonplantapi.domain import entities
from lebonplantapi.domain.request_models import ProductCreation
from lebonplantapi.domain.request_models.product import ProductCreationCategory

from ..models.product import Product, ProductCategory
from . import map_to_user_entity


FROM_PRODUCT_CATEGORY_TO_ENTITY = {
    ProductCategory.BOOKS: entities.ProductCategory.BOOKS,
    ProductCategory.FERTILIZERS: entities.ProductCategory.FERTILIZERS,
    ProductCategory.GRAINS: entities.ProductCategory.GRAINS,
    ProductCategory.INSTALLATIONS: entities.ProductCategory.INSTALLATIONS,
    ProductCategory.TOOLS: entities.ProductCategory.TOOLS,
}

FROM_ENTITY_TO_PRODUCT_CATEGORY = {
    ProductCreationCategory.BOOKS: ProductCategory.BOOKS,
    ProductCreationCategory.FERTILIZERS: ProductCategory.FERTILIZERS,
    ProductCreationCategory.GRAINS: ProductCategory.GRAINS,
    ProductCreationCategory.INSTALLATIONS: ProductCategory.INSTALLATIONS,
    ProductCreationCategory.TOOLS: ProductCategory.TOOLS,
}


def map_product_category_to_entity(
    category: ProductCategory,
) -> entities.ProductCategory:
    return FROM_PRODUCT_CATEGORY_TO_ENTITY[category]


def map_to_product_entity(product: Product) -> entities.Product:
    return entities.Product(
        category=map_product_category_to_entity(product.category),
        description=product.description,
        id=product.id,
        name=product.name,
        picture_link=product.picture_link,
        price=product.price,
        vendor=map_to_user_entity(product.vendor),
    )


def map_from_product_category(category: ProductCreationCategory) -> ProductCategory:
    return FROM_ENTITY_TO_PRODUCT_CATEGORY[category]


def map_from_product_creation(product: ProductCreation) -> Product:
    return Product(
        category=map_from_product_category(product.category),
        description=product.description,
        name=product.name,
        picture_link=product.picture_link,
        price=product.price,
        vendor_id=product.vendor_id,
    )
