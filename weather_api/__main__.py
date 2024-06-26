import pathlib

from fastapi import FastAPI
from fastapi.openapi.docs import get_redoc_html
from prometheus_fastapi_instrumentator import Instrumentator

from weather_api.config import settings
from weather_api.openapi import openapi
from weather_api.routes import system_resources, weather_routes


def get_application() -> FastAPI:
    this_dir = pathlib.Path(__file__).parent

    api = FastAPI(
        root_path=settings.api_root_path,
        redoc_url=None,
    )
    api.include_router(weather_routes.router)
    api.include_router(system_resources.router)

    api.openapi_schema = openapi.custom_openapi(api, this_dir / "example_code")
    Instrumentator().instrument(api).expose(api)
    return api


app = get_application()


@app.get("/redoc", include_in_schema=False)
def redoc():
    return get_redoc_html(
        openapi_url=f"{settings.api_root_path}/openapi.json",
        title="Weather API",
        redoc_favicon_url="https://www.openepi.io/favicon.ico",
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "weather_api.__main__:app",
        host=settings.server_bind_host,
        port=settings.server_bind_port,
    )
