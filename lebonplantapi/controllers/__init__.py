from fastapi import FastAPI

from instance import settings
from lebonplantapi.controllers.api import health


def init_app(app: FastAPI) -> None:
    app.include_router(health.router, prefix=f"/{settings.application_name}/v1")
