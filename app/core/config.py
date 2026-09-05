from functools import lru_cache


class Settings:
    app_name = "API Forge"
    app_description = "Expert-level FastAPI workshop: forge production APIs."
    app_version = "0.1.0"
    api_v1_prefix = "/api/v1"
    database_url = "sqlite:///./api_forge.db"
    secret_key = "change-me-in-production"
    algorithm = "HS256"
    access_token_expire_minutes = 60


@lru_cache()
def get_settings() -> Settings:
    return Settings()
