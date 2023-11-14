from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Query

from weather_api.models.met import sunrise_types as sunrise
from weather_api.models.met import weather_types as weather
from weather_api.services.met_service import MetService

router = APIRouter()


@router.get(
    "/locationforecast",
    summary="Get weather forecast",
    description="Returns the weather forecast for the next 9 days for the given location",
    tags=["weather"],
    response_model_exclude_none=True,
)
async def get_forecast(
    lat: Annotated[float, Query(title="lat", description="Latitude", example=60.10)],
    lon: Annotated[float, Query(title="lat", description="Longitude", example=9.58)],
    altitude: Annotated[
        int | None,
        Query(
            title="altitude",
            description="Altitude above sea level in meters.",
            example=100,
        ),
    ] = 0,
) -> weather.METJSONForecast:
    return await MetService.get_weatherforecast(lat, lon, altitude)


@router.get(
    "/sunrise",
    summary="Get sunrise and sunset information",
    description="Returns the sunrise time and sunset time for the given location",
    tags=["weather"],
    response_model_exclude_none=True,
)
async def get_sunrise(
    lat: Annotated[float, Query(title="lat", description="Latitude", example=60.10)],
    lon: Annotated[float, Query(title="lat", description="Longitude", example=9.58)],
    date: Annotated[
        str | None, Query(title="date", description="Date", example="2021-10-10")
    ] = datetime.today().strftime("%Y-%m-%d"),
) -> sunrise.METJSONSunrise:
    return await MetService.get_sunrise(lat, lon, date)
