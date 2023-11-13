from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    version: str = "0.0.1"
    server_port: int = 8080
    server_host: str = "0.0.0.0"

    api_root_path: str = "/"

    met_api_url: str = "https://api.met.no/weatherapi"
    api_description: str = 'This is a RESTful service that provides accurate and up-to-date weather information based on data sourced from <a href="https://api.met.no">https://api.met.no</a>. <br/>The data are freely available for use under a <a href="https://api.met.no/doc/License">Creative Commons license</a>.'


settings = Settings()
