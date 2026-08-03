# API v1 Versioning Module (`app/api/v1/`)

## Purpose
The `app/api/v1/` module serves as the primary master aggregation router for Version 1 API endpoints, combining sub-routers under `/api/v1`.

## Responsibilities
- Aggregates domain sub-routers (`auth.router`, `users.router`, `jobs.router`, etc.).
- Enforces API semantic versioning boundaries.
