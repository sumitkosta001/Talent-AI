# API Routers Module (`app/routers/`)

## Purpose
The `app/routers/` module defines HTTP transport routes using FastAPI `APIRouter` instances, mapping REST endpoints to services and schemas.

## Responsibilities
- Maps URL paths, HTTP verbs (`GET`, `POST`, `PUT`, `DELETE`), and OpenAPI documentation tags.
- Injects FastAPI dependencies (`Depends(get_db)`, `Depends(get_current_user)`).
- Validates request payloads against Pydantic schemas and delegates business logic to `app/services/`.

## What Belongs Here
- Pure `APIRouter` definitions, path operations, status codes, and OpenAPI documentation descriptions.

## What Should NOT Belong Here
- Direct SQL queries or ORM database session commits (belong in `app/repositories/`).
- Core business calculations or third-party API SDK calls (belong in `app/services/` or `app/integrations/`).
