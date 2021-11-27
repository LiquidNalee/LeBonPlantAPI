from lebonplantapi.controllers.api.schemas.base import ResponseModel


class PingResponseModel(ResponseModel):
    app: str = "ok"


class ReadyResponseModel(ResponseModel):
    db: str


class VersionResponseModel(ResponseModel):
    version: str
