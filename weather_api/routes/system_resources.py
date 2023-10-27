from fastapi import APIRouter
from fastapi import Depends
from fastapi import Response
from healthcheck import HealthCheck

from weather_api.dependencies import get_met_service
from weather_api.services.met_service import MetService
from weather_api.config import settings

router = APIRouter()


@router.get("/health",
            summary="Check if this service is alive",
            description="Returns a simple message to indicate that this service is alive",
            tags=["health"])
async def liveness() -> dict[str, str]:
    return {"message": "Ok"}


@router.get("/ready",
            summary="Check if this service is ready to receive requests",
            description="Returns a message describing the status of this service",
            tags=["health"])
async def ready(met: MetService = Depends(get_met_service)) -> Response:
    health = HealthCheck()

    met_result: tuple[bool, str] = await met.health_check()
    health.add_check(lambda: (met_result[0], met_result[1]))
    health.add_section("version", settings.version)

    message, status_code, headers = health.run()
    return Response(content=message, headers=headers, status_code=status_code)
