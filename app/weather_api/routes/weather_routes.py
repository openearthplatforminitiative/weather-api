from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Query, Depends

from weather_api.dependencies import get_met_service
from weather_api.models.met import sunrise_types as sunrise
from weather_api.models.met import weather_types as weather
from weather_api.services.met_service import MetService

router = APIRouter()


@router.get(
    "/locationforecast",
    response_model=weather.METJSONForecast,
    response_model_exclude_none=True,
)
async def get_forecast(
    lat: Annotated[float, Query(title="lat", description="Latitude", example=60.10)],
    lon: Annotated[float, Query(title="lat", description="Longitude", example=9.58)],
    met_service: MetService = Depends(get_met_service),
) -> weather.METJSONForecast:
    return await met_service.get_weatherforecast(lat, lon)


@router.get(
    "/sunrise",
    response_model=sunrise.METJSONSunrise,
    response_model_exclude_none=True,
)
async def get_sunrise(
    lat: Annotated[float, Query(title="lat", description="Latitude", example=60.10)],
    lon: Annotated[float, Query(title="lat", description="Longitude", example=9.58)],
    date: Annotated[
        str | None, Query(title="date", description="Date", example="2021-10-10")
    ] = datetime.today().strftime("%Y-%m-%d"),
    met_service: MetService = Depends(get_met_service),
) -> sunrise.METJSONSunrise:
    return await met_service.get_sunrise(lat, lon, date)
