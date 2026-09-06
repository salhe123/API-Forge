from functools import lru_cache
import os


class Settings:
    app_name = "API Forge"
    app_description = "Expert-level FastAPI workshop: forge production APIs."
    app_version = "0.1.0"
    api_v1_prefix = "/api/v1"
    database_url = os.getenv("DATABASE_URL", "sqlite:///./api_forge.db")
    secret_key = os.getenv("SECRET_KEY", "change-me-in-production")
    algorithm = "HS256"
    access_token_expire_minutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))


@lru_cache()
def get_settings() -> Settings:
    return Settings()
