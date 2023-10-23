from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    env: str = "dev"
    server_port: int = 8080
    server_host: str = "0.0.0.0"

    met_api_url: str = "https://api.met.no/weatherapi"


settings = Settings()
