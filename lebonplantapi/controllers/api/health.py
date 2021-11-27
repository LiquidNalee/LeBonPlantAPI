from fastapi import APIRouter, HTTPException
from fastapi.responses import ORJSONResponse

from lebonplantapi.adapters.circuit_breakers import circuit_breaker_registry
from lebonplantapi.controllers.api.schemas.health import (
    PingResponseModel,
    ReadyResponseModel,
    VersionResponseModel,
)
from instance import Settings, settings


router = APIRouter()


@router.get("/liveness", response_model=PingResponseModel, status_code=200)
def liveness() -> ORJSONResponse:
    """Liveness probe."""
    return ORJSONResponse(
        content=PingResponseModel().dict(), headers={"Cache-Control": "no-cache"}
    )


@router.get("/readiness", response_model=ReadyResponseModel)
def readiness() -> ORJSONResponse:
    """Readyness probe."""
    content = ReadyResponseModel(
        **{
            cb.id: cb.state.name.lower()
            for cb in circuit_breaker_registry.get_circuits()
        }
    )
    status = 200 if len(circuit_breaker_registry.get_open_circuits()) == 0 else 500
    return ORJSONResponse(
        status_code=status,
        content=content.dict(),
        headers={"Cache-Control": "no-cache"},
    )


@router.get("/version", response_model=VersionResponseModel, status_code=200)
def version(app_settings: Settings = settings) -> VersionResponseModel:
    """Version probe."""
    if not app_settings.application_version:
        raise HTTPException(status_code=404, detail="Version not found")
    return VersionResponseModel(version=app_settings.application_version)
