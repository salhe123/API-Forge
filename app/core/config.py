from functools import lru_cache


class Settings:
    app_name = "API Forge"
    app_description = "Expert-level FastAPI workshop: forge production APIs."
    app_version = "0.1.0"
    api_v1_prefix = "/api/v1"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
