from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from space_comms_digital_twin.api.rest.routers import simulation, quantum, optimization, health, metrics
from space_comms_digital_twin.config import settings
from space_comms_digital_twin.utils.logger import get_logger

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    yield
    logger.info(f"Shutting down {settings.app_name}")


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health.router, tags=["health"])
    app.include_router(metrics.router, tags=["metrics"])
    app.include_router(simulation.router, prefix="/api/v1/simulation", tags=["simulation"])
    app.include_router(quantum.router, prefix="/api/v1/quantum", tags=["quantum"])
    app.include_router(optimization.router, prefix="/api/v1/optimization", tags=["optimization"])

    return app


app = create_app()
