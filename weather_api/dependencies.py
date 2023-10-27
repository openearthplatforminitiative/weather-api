from weather_api.services.met_service import MetService


def get_met_service() -> MetService:
    return MetService()
