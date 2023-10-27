from fastapi import FastAPI

from weather_api.routes import system_resources, weather_routes
from weather_api.config import settings


def get_application() -> FastAPI:
    api = FastAPI(
        title="Weather API",
        version=settings.version,
        root_path=settings.api_root_path,
    )

    api.include_router(system_resources.router)
    api.include_router(weather_routes.router)
    return api


app = get_application()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "weather_api.__main__:app", host=settings.server_host, port=settings.server_port
    )
