from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.v1.router import api_v1_router
from app.core.config import get_settings
from app.core.exceptions import NotFoundError
from app.db.session import init_db


@asynccontextmanager
async def lifespan(application: FastAPI):
    if not getattr(application.state, "testing", False):
        init_db()
    yield


def create_app(testing: bool = False) -> FastAPI:
    settings = get_settings()
    application = FastAPI(
        title=settings.app_name,
        description=settings.app_description,
        version=settings.app_version,
        lifespan=lifespan,
    )
    application.state.testing = testing

    @application.exception_handler(NotFoundError)
    async def not_found_handler(_request: Request, exc: NotFoundError) -> JSONResponse:
        return JSONResponse(status_code=404, content={"detail": exc.detail})

    @application.get("/")
    def hello() -> dict:
        return {"message": "Hello API Forge"}

    application.include_router(api_v1_router, prefix=settings.api_v1_prefix)
    return application


app = create_app()
