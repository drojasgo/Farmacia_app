"""Configuracion central de la aplicacion.

Carga las variables desde ``backend/.env`` (o el entorno del sistema) usando
pydantic-settings. En el resto del proyecto se importa la instancia ``settings``.
"""

from __future__ import annotations

import json
from functools import lru_cache
from typing import List, Optional

from pydantic import Field, PostgresDsn, computed_field, field_validator
from typing_extensions import Annotated
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # --- Aplicacion ---
    APP_NAME: str = "D'asaro API"
    APP_ENV: str = "development"
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"

    # --- Seguridad / JWT ---
    SECRET_KEY: str = Field(min_length=16)
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # --- Base de datos ---
    POSTGRES_DB: str = "farmacia"
    POSTGRES_USER: str = "farmacia_user"
    POSTGRES_PASSWORD: str = "farmacia_pass"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5433
    # Si se define, tiene prioridad sobre los campos POSTGRES_* de arriba.
    DATABASE_URL: Optional[PostgresDsn] = None

    # --- CORS ---
    # NoDecode evita que pydantic-settings intente json.loads() sobre el valor
    # del .env; asi el validador de abajo recibe la cadena tal cual.
    BACKEND_CORS_ORIGINS: Annotated[List[str], NoDecode] = []

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def _split_cors_origins(cls, value: object) -> object:
        """Acepta lista JSON, cadena separada por comas o lista de Python."""
        if value is None or value == "":
            return []
        if isinstance(value, str):
            raw = value.strip()
            if raw.startswith("["):
                return json.loads(raw)
            return [item.strip() for item in raw.split(",") if item.strip()]
        return value

    @computed_field  # type: ignore[prop-decorator]
    @property
    def sqlalchemy_database_uri(self) -> str:
        """URL de conexion async para SQLAlchemy (driver asyncpg)."""
        if self.DATABASE_URL is not None:
            return str(self.DATABASE_URL)
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    @property
    def is_production(self) -> bool:
        return self.APP_ENV.lower() == "production"


@lru_cache
def get_settings() -> Settings:
    """Devuelve una unica instancia de Settings (cacheada)."""
    return Settings()  # type: ignore[call-arg]


settings = get_settings()
