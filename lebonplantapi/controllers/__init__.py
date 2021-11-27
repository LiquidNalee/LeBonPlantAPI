from fastapi import FastAPI

from instance import settings
from lebonplantapi.controllers.api import health, post, product, user


def init_app(app: FastAPI) -> None:
    prefix = f"/{settings.application_name}"

    app.include_router(health.router, prefix=prefix)
    app.include_router(user.router, prefix=prefix)
    app.include_router(product.router, prefix=prefix)
    app.include_router(post.router, prefix=prefix)
