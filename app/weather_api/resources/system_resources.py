from fastapi import APIRouter
from fastapi import Response
from healthcheck import HealthCheck

from weather_api.version import __version__

router = APIRouter()


@router.get("/health", tags=["health"])
async def liveness() -> dict[str, str]:
    return {"message": "Ok"}


@router.get("/ready", tags=["health"])
async def ready() -> Response:
    health = HealthCheck()
    health.add_section("version", __version__)

    message, status_code, headers = health.run()
    return Response(content=message, headers=headers, status_code=status_code)
