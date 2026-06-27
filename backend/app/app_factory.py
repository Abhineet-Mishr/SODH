from __future__ import annotations

import logging

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .config import APP_NAME, LOG_DIR
from .routers.convert import router as convert_router
from .routers.deduplicate import router as deduplicate_router
from .routers.download import router as download_router
from .routers.review import router as review_router
from .routers.research_suggestions import router as research_suggestions_router
from .services.cleanup import cleanup_expired_artifacts

logger = logging.getLogger(__name__)
LOG_DIR.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "literature_toolkit.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)


def create_app() -> FastAPI:
    """Build and configure the FastAPI application."""
    app = FastAPI(title=APP_NAME)
    app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
    app.include_router(convert_router)
    app.include_router(deduplicate_router)
    app.include_router(review_router)
    app.include_router(download_router)
    app.include_router(research_suggestions_router)

    @app.on_event("startup")
    def _startup_cleanup() -> None:
        cleanup_expired_artifacts()

    @app.exception_handler(HTTPException)
    async def _http_exception_handler(_: Request, exc: HTTPException) -> JSONResponse:
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

    @app.exception_handler(RequestValidationError)
    async def _validation_exception_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
        return JSONResponse(status_code=422, content={"detail": "Invalid request", "errors": exc.errors()})

    @app.exception_handler(Exception)
    async def _unhandled_exception_handler(_: Request, exc: Exception) -> JSONResponse:
        logger.exception("unhandled_error")
        return JSONResponse(status_code=500, content={"detail": "Unexpected processing error"})

    return app
