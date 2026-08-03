# Dependency Injection Module (`app/dependencies/`)

## Purpose
The `app/dependencies/` module houses all reusable FastAPI `Depends()` dependency injection factories, decoupling route handlers from authentication checks, session management, and request parameter parsing.

## Responsibilities
- **`auth.py`**: Validates bearer tokens (`get_current_user`) and evaluates role authorization requirements (`get_current_active_admin`).
- **`database.py`**: Yields scoped database `AsyncSession` instances (`get_db`).
- **`pagination.py`**: Parses, validates, and calculates pagination `page`, `size`, and `offset` query parameters.
- **`common.py`**: Extracts header attributes such as `X-Request-ID`.

## What Belongs Here
- Pure FastAPI dependency functions injectable into router endpoint signatures via `Depends()`.

## What Should NOT Belong Here
- Router endpoint handlers or Pydantic DTO models.
- Low-level JWT cryptography or raw SQL queries.
