from fastapi import FastAPI

from instance import settings
from lebonplantapi import controllers
from lebonplantapi.adapters import database
from lebonplantapi.logging import configure_logging


def create_app(name: str = __name__) -> FastAPI:

    app = FastAPI(
        title=name,
        version=settings.application_version,
        openapi_url=settings.openapi_url,
        docs_url=settings.swagger_ui_url,
        redoc_url=settings.redoc_url,
        debug=settings.fastapi_debug,
    )

    if not settings.fastapi_debug:
        configure_logging(settings.log_level)

    controllers.init_app(app)
    database.init_db()

    return app
