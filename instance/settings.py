from typing import Optional, Any

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    application_name: str = "lebonplantapi"
    env_name: str

    application_version: str = Field(env="APP_VERSION")

    fastapi_debug: bool = False

    log_level: str = "INFO"
    babel_default_locale: str = "en"

    expose_documentation: bool = False
    openapi_version: str = "3.0.3"
    api_title: str = "lebonplantapi"
    api_version: str = "1"

    openapi_path: str = "openapi.json"
    swagger_ui_path: str = "swagger"
    redoc_path: str = "redoc"

    openapi_url: Optional[str] = Field(None, const=True)
    swagger_ui_url: Optional[str] = Field(None, const=True)
    redoc_url: Optional[str] = Field(None, const=True)

    sqlalchemy_database_uri: str
    sqlalchemy_connect_timeout: int = 5

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)

        if self.expose_documentation:
            docs_prefix = f"/{self.application_name}/docs"
            self.openapi_url: str = f"{docs_prefix}/{self.openapi_path}"
            self.swagger_ui_url: str = f"{docs_prefix}/{self.swagger_ui_path}"
            self.redoc_url: str = f"{docs_prefix}/{self.redoc_path}"


settings = Settings()
