"""Endpoints de diagnostico: estado del servicio y de la base de datos."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app import __version__
from app.core.config import settings
from app.core.database import get_db

router = APIRouter(tags=["health"])


@router.get("/health", summary="Estado general del servicio")
async def health() -> dict:
    return {
        "status": "ok",
        "app": settings.APP_NAME,
        "env": settings.APP_ENV,
        "version": __version__,
    }


@router.get("/health/db", summary="Verifica la conexion a PostgreSQL")
async def health_db(db: AsyncSession = Depends(get_db)) -> dict:
    result = await db.execute(text("SELECT 1"))
    return {"status": "ok", "database": "reachable", "result": result.scalar_one()}
