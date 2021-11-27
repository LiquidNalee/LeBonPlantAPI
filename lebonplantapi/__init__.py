from fastapi import FastAPI

from lebonplantapi import controllers
from lebonplantapi.logging import configure_logging
from instance import settings


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
    return app
