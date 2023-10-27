from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    version: str = "0.0.1"
    server_port: int = 8080
    server_host: str = "0.0.0.0"

    api_root_path: str = "/"

    met_api_url: str = "https://api.met.no/weatherapi"


settings = Settings()
