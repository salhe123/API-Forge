from fastapi import APIRouter

from app.api.v1 import health, items

api_v1_router = APIRouter()
api_v1_router.include_router(health.router, tags=["health"])
api_v1_router.include_router(items.router, prefix="/items", tags=["items"])
