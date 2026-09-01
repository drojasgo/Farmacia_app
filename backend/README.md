# Backend D'asaro — FastAPI + PostgreSQL

API RESTful del e-commerce de vitaminas y suplementos D'asaro.

## Stack

| Componente        | Uso                                        |
|-------------------|--------------------------------------------|
| FastAPI           | Framework web / OpenAPI                     |
| SQLAlchemy 2.0    | ORM async                                   |
| asyncpg           | Driver PostgreSQL async                     |
| Alembic           | Migraciones de esquema                      |
| pydantic-settings | Configuración por variables de entorno      |
| passlib / jose    | Hashing de contraseñas y JWT                |

> Requiere **Python 3.11+** (recomendado). La máquina de desarrollo tiene 3.8;
> conviene instalar una versión más reciente antes de continuar.

## Estructura

```
backend/
├── requirements.txt
├── .env.example          # copiar a .env
└── app/
    ├── main.py           # instancia FastAPI + lifespan (ping a la BD)
    ├── core/
    │   ├── config.py     # Settings (pydantic-settings)
    │   └── database.py    # engine async, sesión, Base ORM, get_db
    └── api/
        └── v1/
            ├── router.py            # agrega los routers de la v1
            └── endpoints/
                └── health.py        # /health y /health/db
```

## Puesta en marcha

1. Levantar PostgreSQL (desde la raíz del repo):

   ```bash
   cp .env.example .env
   docker compose up -d
   ```

2. Crear el entorno virtual e instalar dependencias:

   ```bash
   cd backend
   python -m venv .venv
   # Windows PowerShell:
   .venv\Scripts\Activate.ps1
   # Linux/macOS:
   source .venv/bin/activate

   pip install -r requirements.txt
   ```

3. Configurar variables de entorno del backend:

   ```bash
   cp .env.example .env
   # editar SECRET_KEY y, si corre fuera de Docker, POSTGRES_HOST/PORT
   python -c "import secrets; print(secrets.token_hex(32))"   # generar SECRET_KEY
   ```

4. Ejecutar la API:

   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

5. Verificar:

   - http://localhost:8000/            → info básica
   - http://localhost:8000/docs        → Swagger UI
   - http://localhost:8000/api/v1/health      → estado del servicio
   - http://localhost:8000/api/v1/health/db   → conexión a PostgreSQL

## Notas de conexión

- `docker-compose.yml` publica PostgreSQL en el puerto **5433** del host
  (`POSTGRES_PORT`). Por eso `.env.example` usa `POSTGRES_HOST=localhost` y
  `POSTGRES_PORT=5433` cuando el backend corre en la máquina.
- Si más adelante el backend se conteneriza en la misma red de Docker, usar
  `POSTGRES_HOST=db` y `POSTGRES_PORT=5432`.
- `config.py` arma la URL `postgresql+asyncpg://…`. También se puede definir
  `DATABASE_URL` directamente y tendrá prioridad.

## Próximos pasos

- Modelos ORM en `app/models/` (empezando por `usuarios`, ya en `db/init/01_schema.sql`).
- Migraciones con Alembic (`alembic init`).
- Módulo de autenticación (JWT) y hashing con passlib.
- Routers de catálogo, órdenes, encuesta nutricional y portal educativo.
