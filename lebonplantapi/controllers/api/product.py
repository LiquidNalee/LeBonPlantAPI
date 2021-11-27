from fastapi import APIRouter, HTTPException
from fastapi.responses import ORJSONResponse

from lebonplantapi.controllers.api.schemas.product import (
    ProductCreationRequest,
    ProductListResponseModel,
    ProductResponseModel,
)
from lebonplantapi.domain.entities import Product
from lebonplantapi.domain.errors import ProductNotFoundError
from lebonplantapi.domain.request_models import ProductCreation
from lebonplantapi.domain.usecases import ListProducts, SaveProduct
from lebonplantapi.domain.usecases.product import GetProduct
from lebonplantapi.registry import product_repository


router = APIRouter()


@router.get(
    "/product",
    response_class=ORJSONResponse,
    status_code=200,
)
async def list_products() -> ProductListResponseModel:
    """Return all products."""
    products = await ListProducts(product_repository).execute()
    product_responses = [ProductResponseModel.from_orm(product) for product in products]
    return ProductListResponseModel(content=product_responses)


@router.get(
    "/product/{product_id}",
    response_model=ProductResponseModel,
    response_class=ORJSONResponse,
    status_code=200,
)
async def get_product(product_id: int) -> Product:
    """Return a product."""
    try:
        result = await GetProduct(product_repository, product_id).execute()
    except ProductNotFoundError:
        raise HTTPException(status_code=404, detail="Product not found")
    return result


@router.post(
    "/product",
    response_class=ORJSONResponse,
    status_code=200,
)
async def save_product(product_creation_request: ProductCreationRequest) -> None:
    """Add a new product."""
    product_creation = ProductCreation.from_request(product_creation_request)
    await SaveProduct(product_repository, product_creation).execute()
