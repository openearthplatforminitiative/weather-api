from fastapi import APIRouter
from fastapi import Response
from healthcheck import HealthCheck

from weather_api.config import settings
from weather_api.services.met_service import MetService

router = APIRouter()
health = HealthCheck()
health.add_section("version", settings.version)
health.add_check(MetService.met_healthcheck)


@router.get(
    "/health",
    summary="Check if this service is alive",
    description="Returns a simple message to indicate that this service is alive",
    tags=["health"],
)
async def liveness() -> dict[str, str]:
    return {"message": "Ok"}


@router.get(
    "/ready",
    summary="Check if this service is ready to receive requests",
    description="Returns a message describing the status of this service",
    tags=["health"],
)
async def ready() -> Response:
    message, status_code, headers = health.run()
    return Response(content=message, headers=headers, status_code=status_code)
