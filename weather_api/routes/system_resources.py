from fastapi import APIRouter
from fastapi import Depends
from fastapi import Response
from healthcheck import HealthCheck

from weather_api.dependencies import get_met_service
from weather_api.services.met_service import MetService
from weather_api.config import settings

router = APIRouter()


@router.get("/health", tags=["health"])
async def liveness() -> dict[str, str]:
    return {"message": "Ok"}


@router.get("/ready", tags=["health"])
async def ready(met: MetService = Depends(get_met_service)) -> Response:
    health = HealthCheck()

    met_result: tuple[bool, str] = await met.health_check()
    health.add_check(lambda: (met_result[0], met_result[1]))
    health.add_section("version", settings.version)

    message, status_code, headers = health.run()
    return Response(content=message, headers=headers, status_code=status_code)
