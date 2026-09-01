"""Conexion a PostgreSQL con SQLAlchemy 2.0 (async / asyncpg).

Expone:
- ``engine``            : motor async global.
- ``AsyncSessionLocal``: fabrica de sesiones.
- ``Base``             : clase base declarativa para los modelos ORM.
- ``get_db``           : dependencia de FastAPI que entrega una sesion por request.
- ``check_database_connection`` : ping usado en el arranque.
"""

from __future__ import annotations

from typing import AsyncGenerator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings

# El motor mantiene un pool de conexiones reutilizable durante la vida del proceso.
engine = create_async_engine(
    settings.sqlalchemy_database_uri,
    echo=settings.DEBUG,
    pool_pre_ping=True,   # descarta conexiones muertas antes de usarlas
    pool_size=5,
    max_overflow=10,
    future=True,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


class Base(DeclarativeBase):
    """Base declarativa compartida por todos los modelos ORM."""


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependencia de FastAPI: abre una sesion, la cierra al terminar el request."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise


async def check_database_connection() -> None:
    """Ejecuta ``SELECT 1`` para verificar que la base de datos responde."""
    async with engine.connect() as conn:
        await conn.execute(text("SELECT 1"))


async def dispose_engine() -> None:
    """Libera el pool de conexiones (llamar al apagar la app)."""
    await engine.dispose()
