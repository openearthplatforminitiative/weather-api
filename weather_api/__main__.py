import hashlib
import logging
import pathlib
from http import HTTPStatus

from fastapi import FastAPI, Request
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

    logging.basicConfig(level=logging.INFO)
    Instrumentator().instrument(api).expose(api)
    return api


app = get_application()
request_logger = logging.getLogger()


@app.middleware("http")
async def log_request(request: Request, call_next):
    hashed_subject = "anonymous"
    if "X-Subject" in request.headers:
        hashed_subject = hashlib.sha256(
            request.headers["X-Subject"].encode("utf-8")
        ).hexdigest()[:20]

    response = await call_next(request)

    request_logger.info(
        f"{request.client.host}:{request.client.port} - [{hashed_subject}] - \"{request.method} {request.url.path} HTTP/{request.scope.get('http_version', '1.1')}\" "
        f"{response.status_code} {HTTPStatus(response.status_code).phrase}"
    )
    return response


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
        access_log=False,
    )
