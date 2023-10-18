import aiohttp
from pydantic import TypeAdapter

from weather_api.config import settings
from weather_api.models.met.sunrise_types import METJSONSunrise
from weather_api.models.met.weather_types import METJSONForecast


class MetService:
    async def get_weatherforecast(
        self,
        lat: float,
        lon: float,
    ) -> METJSONForecast:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{settings.met_api_url}/locationforecast/2.0/complete",
                params={"lat": lat, "lon": lon},
            ) as response:
                return TypeAdapter(METJSONForecast).validate_python(
                    await response.json()
                )

    async def get_sunrise(self, lat: float, lon: float, date: str) -> METJSONSunrise:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{settings.met_api_url}/sunrise/3.0/sun",
                params={"lat": lat, "lon": lon, "date": date},
            ) as response:
                return TypeAdapter(METJSONSunrise).validate_python(
                    await response.json()
                )
