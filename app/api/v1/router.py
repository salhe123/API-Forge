from fastapi import APIRouter

from app.api.v1 import auth, health, items
from app.core.config import get_settings

api_v1_router = APIRouter()


@api_v1_router.get("/")
def api_root() -> dict:
    settings = get_settings()
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "docs": "/docs",
    }


api_v1_router.include_router(health.router, tags=["health"])
api_v1_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_v1_router.include_router(items.router, prefix="/items", tags=["items"])
