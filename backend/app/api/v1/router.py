"""Router agregador de la API v1.

A medida que se implementen los modulos (catalogo, usuarios, ordenes,
encuesta nutricional, portal educativo) se incluyen aqui sus routers.
"""

from fastapi import APIRouter

from app.api.v1.endpoints import health

api_router = APIRouter()
api_router.include_router(health.router)

# Ejemplos para los proximos modulos:
# from app.api.v1.endpoints import auth, usuarios, productos, ordenes
# api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
# api_router.include_router(usuarios.router, prefix="/usuarios", tags=["usuarios"])
# api_router.include_router(productos.router, prefix="/productos", tags=["catalogo"])
# api_router.include_router(ordenes.router, prefix="/ordenes", tags=["ordenes"])
