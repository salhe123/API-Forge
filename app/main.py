from contextlib import asynccontextmanager
import logging
import time
import uuid
from typing import Type

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.v1.router import api_v1_router
from app.core.config import get_settings
from app.core.exceptions import (
    AuthenticationError,
    ConflictError,
    ForbiddenError,
    NotFoundError,
)
from app.db.session import init_db

logger = logging.getLogger("api_forge")

_ERROR_STATUS = {
    NotFoundError: 404,
    ConflictError: 409,
    ForbiddenError: 403,
    AuthenticationError: 401,
}


@asynccontextmanager
async def lifespan(application: FastAPI):
    if not getattr(application.state, "testing", False):
        init_db()
    yield


def _add_error_handler(application: FastAPI, exc_class: Type[Exception], status_code: int) -> None:
    @application.exception_handler(exc_class)
    async def handler(_request: Request, exc: Exception) -> JSONResponse:
        headers = None
        if status_code == 401:
            headers = {"WWW-Authenticate": "Bearer"}
        return JSONResponse(
            status_code=status_code,
            content={"detail": getattr(exc, "detail", str(exc))},
            headers=headers,
        )


def create_app(testing: bool = False) -> FastAPI:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
    settings = get_settings()
    application = FastAPI(
        title=settings.app_name,
        description=settings.app_description,
        version=settings.app_version,
        lifespan=lifespan,
    )
    application.state.testing = testing
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @application.middleware("http")
    async def add_request_id(request: Request, call_next):
        request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response

    @application.middleware("http")
    async def log_requests(request: Request, call_next):
        started = time.perf_counter()
        response = await call_next(request)
        elapsed_ms = (time.perf_counter() - started) * 1000
        logger.info(
            "%s %s -> %s (%.1fms)",
            request.method,
            request.url.path,
            response.status_code,
            elapsed_ms,
        )
        return response

    for exc_class, status_code in _ERROR_STATUS.items():
        _add_error_handler(application, exc_class, status_code)

    @application.exception_handler(StarletteHTTPException)
    async def http_exception_handler(_request: Request, exc: StarletteHTTPException) -> JSONResponse:
        if exc.status_code == 404:
            return JSONResponse(status_code=404, content={"detail": "Not found"})
        headers = None
        if exc.status_code == 401:
            headers = {"WWW-Authenticate": "Bearer"}
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
            headers=headers,
        )

    @application.get("/")
    def hello() -> dict:
        return {"message": "Hello API Forge"}

    application.include_router(api_v1_router, prefix=settings.api_v1_prefix)
    return application


app = create_app()
