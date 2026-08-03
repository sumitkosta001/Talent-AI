# Database Architecture Module (`app/database/`)

## Purpose
The `app/database/` module manages PostgreSQL database connection pooling, async session factories, ORM base metadata, and schema initialization hooks.

## Responsibilities
- **`base.py`**: Root `Base` DeclarativeBase entity class for SQLAlchemy 2.0.
- **`connection.py`**: Asynchronous PostgreSQL engine manager (`asyncpg` driver).
- **`session.py`**: FastAPI dependency injector yielding scoped `AsyncSession` instances.
- **`init_db.py`**: Database table bootstrap and initial seed script hooks.

## What Belongs Here
- Database connection configuration, async session lifecycle context managers, and base declarative metadata.

## What Should NOT Belong Here
- Domain-specific model declarations (belong in `app/models/`).
- SQL queries and CRUD operations (belong in `app/repositories/`).
- Alembic database migration scripts (belong in root `alembic/` directory).
