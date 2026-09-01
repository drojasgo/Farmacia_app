"""Punto de entrada de la API de D'asaro (FastAPI).

Ejecutar en desarrollo:
    uvicorn app.main:app --reload --port 8000
"""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import __version__
from app.api.v1.router import api_router
from app.core.config import settings
from app.core.database import check_database_connection, dispose_engine

logging.basicConfig(level=logging.INFO if settings.DEBUG else logging.WARNING)
logger = logging.getLogger("dasaro")


@asynccontextmanager
async def lifespan(_: FastAPI):
    # --- Arranque ---
    try:
        await check_database_connection()
        logger.info("Conexion a PostgreSQL verificada correctamente.")
    except Exception as exc:  # noqa: BLE001
        logger.error("No se pudo conectar a PostgreSQL: %s", exc)
        # No abortamos el arranque: /health/db reportara el problema.
    yield
    # --- Apagado ---
    await dispose_engine()
    logger.info("Pool de conexiones liberado.")


app = FastAPI(
    title=settings.APP_NAME,
    version=__version__,
    description="API del e-commerce D'asaro (vitaminas y suplementos).",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
    lifespan=lifespan,
)

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_PREFIX)


@app.get("/", tags=["root"], summary="Informacion basica de la API")
async def root() -> dict:
    return {
        "name": settings.APP_NAME,
        "version": __version__,
        "docs": "/docs",
        "api": settings.API_V1_PREFIX,
    }
