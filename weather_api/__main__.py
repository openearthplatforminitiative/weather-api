import pathlib

from fastapi import FastAPI
from fastapi.openapi.docs import get_redoc_html
from fastapi.staticfiles import StaticFiles
from prometheus_fastapi_instrumentator import Instrumentator

from weather_api.config import settings
from weather_api.openapi import openapi
from weather_api.routes import system_resources, weather_routes


def get_application() -> FastAPI:
    this_dir = pathlib.Path(__file__).parent

    app = FastAPI(
        redoc_url=None,
    )

    api = FastAPI()
    api.include_router(weather_routes.router)
    api.include_router(system_resources.router)

    app.mount(
        f"/static",
        StaticFiles(directory=this_dir / "assets"),
        name="static",
    )
    app.mount(f"{settings.api_root_path}", api)

    app.openapi_schema = openapi.custom_openapi(app, this_dir / "example_code")
    Instrumentator().instrument(app).expose(app)
    return app


application = get_application()


@application.get("/redoc", include_in_schema=False)
def redoc():
    return get_redoc_html(
        openapi_url=f"{settings.api_root_path}/openapi.json",
        title="Weather API",
        redoc_favicon_url="https://www.openepi.io/favicon.ico",
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "weather_api.__main__:application",
        host=settings.server_bind_host,
        port=settings.server_bind_port,
    )
