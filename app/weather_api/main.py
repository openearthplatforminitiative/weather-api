from fastapi import FastAPI

from weather_api.routes import system_resources, weather_routes
from weather_api.version import __version__


def get_application() -> FastAPI:
    api = FastAPI(title="Weather API", version=__version__, root_path_in_servers=False)

    api.include_router(system_resources.router)
    api.include_router(weather_routes.router)
    return api


app = get_application()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("weather_api.main:app", host="0.0.0.0", port=8080)
