# farmacia_app

Base de datos de ejemplo (PostgreSQL) que modela los usuarios registrados de una farmacia,
con la informacion personal necesaria para su gestion (documento, contacto, EPS, alergias, etc.).

## Estructura

```
farmacia_app/
├── docker-compose.yml     # Servicio de PostgreSQL
├── .env.example           # Variables de entorno (copiar a .env)
└── db/
    └── init/
        ├── 01_schema.sql  # Definicion de tablas, tipos e indices
        └── 02_seed.sql    # Datos ficticios de prueba
```

## Uso

```bash
cp .env.example .env
docker compose up -d
```

Los scripts en `db/init/` se ejecutan automaticamente la primera vez que se crea el volumen.

Conectarse con psql:

```bash
docker compose exec db psql -U farmacia_user -d farmacia
```

Consultar los usuarios de ejemplo:

```sql
SELECT id, primer_nombre, primer_apellido, correo_electronico, estado FROM usuarios;
```

## Reiniciar desde cero

```bash
docker compose down -v   # elimina el volumen y fuerza a re-ejecutar los scripts de init
docker compose up -d
```

## Nota

Los datos en `02_seed.sql` son ficticios y los `password_hash` son valores de relleno,
no hashes reales. No usar esta base de datos ni sus credenciales de ejemplo en produccion.
