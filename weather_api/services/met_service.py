from httpx import AsyncClient, Client
from pydantic import TypeAdapter

from weather_api.config import settings
from weather_api.models.met.sunrise_types import METJSONSunrise
from weather_api.models.met.weather_types import METJSONForecast


class MetService:
    @staticmethod
    async def get_weatherforecast(
        lat: float,
        lon: float,
        altitude: int,
    ) -> METJSONForecast:
        async with AsyncClient() as client:
            response = await client.get(
                f"{settings.met_api_url}/locationforecast/2.0/complete",
                params={"lat": lat, "lon": lon, "altitude": altitude},
            )
            return TypeAdapter(METJSONForecast).validate_python(response.json())

    @staticmethod
    async def get_sunrise(lat: float, lon: float, date: str) -> METJSONSunrise:
        async with AsyncClient() as client:
            response = await client.get(
                f"{settings.met_api_url}/sunrise/3.0/sun",
                params={"lat": lat, "lon": lon, "date": date},
            )
            return TypeAdapter(METJSONSunrise).validate_python(response.json())

    @staticmethod
    def met_healthcheck() -> tuple[bool, str]:
        with Client() as client:
            response = client.get(
                f"{settings.met_api_url}/locationforecast/2.0/healthz"
            )
            if response.status_code == 200:
                return True, "Met API is healthy"
            return False, "Met API is unhealthy"
