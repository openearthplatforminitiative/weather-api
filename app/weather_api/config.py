from pydantic import BaseSettings


class Settings(BaseSettings):
    env: str = "dev"
    server_port: int = 8080
    server_host: str = "0.0.0.0"
