from typing import List, Optional

from sqlalchemy import select

from lebonplantapi.adapters.database.helpers import db_accessor
from lebonplantapi.adapters.database.mappers import (
    map_from_product_creation,
    map_to_product_entity,
)
from lebonplantapi.adapters.database.models import Product
from lebonplantapi.adapters.database.settings import session
from lebonplantapi.domain import entities
from lebonplantapi.domain.ports import ProductRepositoryPort
from lebonplantapi.domain.request_models import ProductCreation


class ProductRepository(ProductRepositoryPort):
    @db_accessor()
    async def list_products(self) -> List[entities.Product]:
        result = await session.execute(select(Product))
        products = result.scalars().all()
        product_entities = [map_to_product_entity(product) for product in products]

        return product_entities

    @db_accessor()
    async def get_product(self, product_id: int) -> Optional[entities.Product]:
        result = await session.execute(select(Product).filter_by(id=product_id))
        product = result.scalar()
        product_entity = map_to_product_entity(product) if product is not None else None

        return product_entity

    @db_accessor(commit=True)
    async def save_product(self, product_creation: ProductCreation) -> None:
        product = map_from_product_creation(product_creation)
        session.add(product)
